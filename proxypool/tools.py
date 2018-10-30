import requests
from fake_useragent import UserAgent
from requests.exceptions import ConnectionError

ua = UserAgent()
base_headers = {"User-Agent" : ua.random}
def get_page(url, options = {}):
    """
    """
    headers = dict(base_headers, **options)
    print("正在抓取", url)
    try:
        response = requests.get(url, headers = headers)
        print("抓取成功", url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print("抓取失败", url)
        return None


