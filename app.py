from flask import Flask, request, render_template_string
import joblib
import numpy as np
import pyodbc
from datetime import datetime

app = Flask(__name__)
model = joblib.load('churn_model.pkl')

# SQL Server config
server = 'DESKTOP-5P9F26K\\SQLEXPRESS'
database = 'DB'
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

def log_prediction(tenure, monthly, total, prediction):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dbo.ChurnPredictionLog (tenure, monthly_charges, total_charges, prediction)
        VALUES (?, ?, ?, ?)
    """, (tenure, monthly, total, prediction))
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template_string('''
        <h2>Telco Churn Prediction</h2>
        <form method="POST" action="/predict">
            Tenure Months: <input name="tenure" type="number" step="0.1"><br>
            Monthly Charges: <input name="monthly" type="number" step="0.1"><br>
            Total Charges: <input name="total" type="number" step="0.1"><br><br>
            <button type="submit">Predict</button>
        </form>
    ''')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        tenure = float(request.form['tenure'])
        monthly = float(request.form['monthly'])
        total = float(request.form['total'])

        features = np.array([[tenure, monthly, total]])
        prediction = model.predict(features)[0]

        result = 'Churn' if prediction == 1 else 'No Churn'

        # Log to database
        log_prediction(tenure, monthly, total, result)

        return f"<h3>Prediction: {result}</h3><a href='/'>Try again</a>"
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == '__main__':
    app.run(debug=True)
