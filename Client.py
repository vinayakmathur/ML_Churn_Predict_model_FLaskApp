import requests

response = requests.post(
    "http://localhost:5000/check_names",
    json={
        "names": ["vinayak", "ram", "shyam"],
        "genders": ["male", "male", "male"]
    }
)

print(response.json())  # Will parse JSON successfully now

print("Status Code:", response.status_code)
print("Response Text:", repr(response.text)) 
