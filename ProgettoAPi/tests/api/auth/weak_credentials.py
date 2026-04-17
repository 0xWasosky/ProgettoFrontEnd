import requests


data = {"username": "1", "password": "1"}


url = "http://127.0.0.1:5000///auth/register"


response = requests.post(url, json=data)


print(response.content)
print(response.headers)
print(response.cookies.get("token"))
print(response.status_code)
