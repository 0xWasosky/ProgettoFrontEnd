import requests

BASE_URL = "http://127.0.0.1:5000"
ENDPOINT = "/files/yearbook"

cookie = {
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEwMDAsICJleHAiOiAxNzc0MTAxNzQ2fQ.JHRMGBXBGMozMabniGDVN4gLoi8-51ME8wyYY7B3GEA"
}


if __name__ == "__main__":
    url = BASE_URL + ENDPOINT
    response = requests.get(url, cookies=cookie)

    print("URL:", url)
    print("Status code:", response.status_code)
    print("Headers:", response.headers)
    print("Body preview:", response.content[:200])
    with open("x.pdf", 'wb') as f:
        f.write(response.content)
        
