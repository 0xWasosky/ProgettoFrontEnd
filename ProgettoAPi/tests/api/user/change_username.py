import requests


url = "http://192.168.1.109:5000/user/change_username"

cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzY2OTM4Nzg0fQ.6KJA03wvkH4ASoliddYjrnBTn-JbvOSrNB_Pg2hva9c"
}

data = {"username": "new"}

response = requests.post(url, cookies=cookie, json=data)

print(response.json())
