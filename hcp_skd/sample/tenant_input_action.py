import xmltojson
import json
import requests
import requests, bs4
import pandas as pd

# Sample URL to fetch the html page
url = "https://geeksforgeeks-example.surge.sh"

# Headers to mimic the browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# Get the page through get() method
# html_response = requests.get(url=url, headers=headers)

# Save the page content as sample.html
# with open("sample.html", "w") as html_file:
#     html_file.write(html_response.text)

# with open("tenant_input_action.html", "r") as html_file:
#     html = html_file.read()
#     json_ = xmltojson.parse(html)
#
# with open("data.json", "w") as file:
#     json.dump(json_, file)
#
# print(json_)

with open('tenant_input_action.html', encoding='utf-8') as f:
    html = f.read()
response = bs4.BeautifulSoup(html, 'html.parser')
print(response)
# target = response.find('table', {'id':'test_table', 'class':'type07'})
# target