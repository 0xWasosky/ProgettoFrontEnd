import requests


url = "http://127.0.0.1:5000/files/add"

cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzcwMDI3MjUzfQ.lpJgtOi9WgIHdHgSxtfSmi6GiQW3o6Ggd1QtAIzfhJc"
}


response = requests.put(
    url, cookies=cookie, files={"file": open("sample-15s.mp3", "rb").read()}
)


print(response.headers)
print(response.json())
