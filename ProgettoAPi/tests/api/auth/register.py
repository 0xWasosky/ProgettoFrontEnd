import requests


data = {"username": "MyPersonalUsername1", "password": "MyPassword123.123213"}


# Use local backend while developing.
url = "http://127.0.0.1:5000/auth/register"
#url = "http://93.186.254.153/auth/register"

response = requests.post(url, json=data, timeout=10)


print(response.content)
print(response.headers)
print(response.cookies.get("token"))
print(response.status_code)
