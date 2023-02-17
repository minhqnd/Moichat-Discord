import requests

async def send(word):
    url = "http://tudientv.com/dictfunctions.php"
    payload = {
        "action": 'getmeaning',
        "entry": word
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        return "Không thể lấy dữ liệu từ API"