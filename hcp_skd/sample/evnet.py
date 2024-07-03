import bs4
import xmltojson

with open('event.html', encoding='utf-8') as f:
    html = f.read()
soup = bs4.BeautifulSoup(html, 'html.parser')
print(soup)

