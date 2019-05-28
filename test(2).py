import requests


html = requests.get('http://httpbin.org/get')
print(html.text)