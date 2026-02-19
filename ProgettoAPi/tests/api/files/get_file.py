import requests


url = "http://127.0.0.1:5000/files/get"


cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzcwMDI3MjUzfQ.lpJgtOi9WgIHdHgSxtfSmi6GiQW3o6Ggd1QtAIzfhJc"
}


response = requests.get(url, cookies=cookie, json={"id": 1000})


with open("response.mp3", "wb") as f:
    f.write(response.content)
