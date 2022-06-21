import requests
import re

url = "https://www.fabiaoqing.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
}
response = requests.get(url=url, headers=headers)
html = response.text
URLS = re.findall('<a href="(.*?)" class=".*?" title=".*?">', html)
for URL in URLS:
    print(URL)