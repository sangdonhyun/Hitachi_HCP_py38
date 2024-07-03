
import xmltojson
import json
import requests

# Sample URL to fetch the html page
url = "http://www.naver.com"

# Headers to mimic the browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# Get the page through get() method
html_response = requests.get(url=url, headers=headers)
print(html_response.text)
# Save the page content as sample.html
with open("sample.html", "w", encoding='utf-8') as html_file:
    html_file.write(html_response.text)


with open('sample.html', encoding='utf-8') as f:
    html = f.read()
    json_ = xmltojson.parse(html)

json_str = json.dumps(json_, indent=4)
print(json_str)
