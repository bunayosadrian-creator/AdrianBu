import requests


classmate_url = "https://jasminerose-2.onrender.com/student"

response = requests.get(classmate_url)


if response.status_code == 200:
    data = response.json()
    
    print(" Classmate's API Data ")
    
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Data received:", data)
else:
    print("Failed to reach classmate's API.")
    print("Status Code:", response.status_code)