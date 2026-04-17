import requests


url = "http://127.0.0.1:5000/files/image/add"

cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzc0MTAxNzQ2fQ.JHRMGBXBGMozMabniGDVN4gLoi8-51ME8wyYY7B3GEA"
}


response = requests.put(
    url, cookies=cookie, files={"file": open("image.jpeg", "rb").read()}
)


print(response.headers)
print(response.json())
