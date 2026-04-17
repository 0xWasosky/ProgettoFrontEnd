import requests


url = "http://127.0.0.1:5000/files/image/get"


cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzc0MTAxNzQ2fQ.JHRMGBXBGMozMabniGDVN4gLoi8-51ME8wyYY7B3GEA"
}


response = requests.get(url, cookies=cookie, json={"id": 1000})


with open("response.jpeg", "wb") as f:
    f.write(response.content)
