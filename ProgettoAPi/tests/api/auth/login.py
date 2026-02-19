import requests


data = {"username": "1", "password": "ciao"}


url = "http://127.0.0.1:5000///auth/login"


response = requests.post(url, json=data)


print(response.content)
print(response.headers)
print(response.cookies)
print(response.status_code)
