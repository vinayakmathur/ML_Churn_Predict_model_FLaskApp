from flask import Flask, request, jsonify, render_template_string
import pyodbc

app = Flask(__name__)

server = 'DESKTOP-5P9F26K\\SQLEXPRESS'
database = 'DB'
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

def insert_name_to_db(name,gender):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.Users (name,gender) VALUES (?, ?)", (name,gender))
    conn.commit()
    conn.close()

# HTML form page
@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
        
        <h2 align = 'center'> Welcome to My First Flask Project, Excited to see you here!!</h2>
        <h2>Please enter Your Name and Gender (comma-separated)</h2>                         
        <form method="POST" action="/check_names">
            <input name="names" style="width:300px;" placeholder="e.g. vinayak, ram, shyam">
           <input name="genders" style="width:300px;" placeholder="e.g. male, male, female"><br><br>
            <button type="submit">Submit</button>
        </form>
    ''')

# POST handler for form and API


@app.route('/check_names', methods=['POST'])
def check_names():
    if request.is_json:
        data = request.get_json()
        names = data.get('names', [])
        genders = data.get('genders', [])
    else:
        # fallback to form data
        names = request.form.get('names', '').split(',')
        genders = request.form.get('genders', '').split(',')

    names = [n.strip() for n in names if n.strip()]
    genders = [g.strip() for g in genders if g.strip()]

    responses = []
    stranger_count = 0
    known_count = 0

    for i, name in enumerate(names):
        gender = genders[i] if i < len(genders) else 'unknown'
        insert_name_to_db(name, gender)

        if name.lower() == 'vinayak':
            responses.append(f"Hello vinayak! ({gender})")
            known_count += 1
        else:
            responses.append(f"Hello Stranger! ({name}, {gender})")
            stranger_count += 1

    if request.is_json:
        # Return JSON for API calls
        return jsonify({
            "messages": responses,
            "stranger_count": stranger_count,
            "known_count": known_count,
            "total_names": len(names)
        })
    else:
        # Return HTML for form submissions
        return render_template_string('''
            <h2>Response:</h2>
            <ul>
                {% for msg in messages %}
                    <li>{{ msg }}</li>
                {% endfor %}
            </ul>
            <p><strong>Total Names:</strong> {{ total }}</p>
            <p><strong>Strangers:</strong> {{ stranger_count }}</p>
            <p><strong>Known (vinayak):</strong> {{ known_count }}</p>

            <!-- chart code here -->

            <br><a href="/">Go back</a>
        ''', messages=responses, stranger_count=stranger_count, known_count=known_count, total=len(names))



    if request.method == 'POST':
        if request.form:  # Submitted via form
            names = request.form.get('names', '').split(',')
            gender = request.form.get('gender', '').split(',')
            names = [name.strip() for name in names if name.strip()]
        elif request.is_json:  # Submitted via JSON
            data = request.get_json()
            names = data.get('names', [])
            genders = data.get('genders', [])

    names = [name.strip() for name in names if name.strip()]
    genders = [gender.strip() for gender in genders if gender.strip()]

    responses = []
    stranger_count = 0
    known_count = 0

    for i, name in enumerate(names):
        gender = genders[i] if i < len(genders) else 'unknown'
        insert_name_to_db(name,gender)
        if name.lower() != 'vinayak':
            responses.append(f"Hello vinayak! ({gender})")
            known_count += 1
        else:
            responses.append(f"Hello Stranger! ({name}, {gender})")
            stranger_count += 1


    # If from form, show HTML
    if request.form:
        return render_template_string('''
            <h2>Response:</h2>
            <ul>
                {% for msg in messages %}
                    <li>{{ msg }}</li>
                {% endfor %}
            </ul>
            <p><strong>Total names submitted:</strong> {{ total }}</p>
            <p><strong>Stranger Count:</strong> {{ stranger_count }}</p>
            <a href="/">Go back</a>
        ''', messages=responses, stranger_count=stranger_count, total=len(names))

    # If from API client, return JSON
    return jsonify({
        "messages": responses,
        "stranger_count": stranger_count,
        "total_names": len(names)
    })

if __name__ == '__main__':
    app.run(debug=True)
