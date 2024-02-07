import requests

proxy_list = []


def download_proxy_list():
    response = requests.get("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")
    for i in response.text.splitlines():
        proxy_list.append("http://" + i)
