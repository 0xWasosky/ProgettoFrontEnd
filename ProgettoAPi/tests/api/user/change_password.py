import requests



url = "http://127.0.0.1:5000///user/change_password"


cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzc0MTAxNzQ2fQ.JHRMGBXBGMozMabniGDVN4gLoi8-51ME8wyYY7B3GEA"
}

data = {"old_password": "MyPassword123.123213", "new_password": "MyPassword123.123213"}

response = requests.post(url, cookies=cookie, json=data)

print(response.json())
print(response.headers)
