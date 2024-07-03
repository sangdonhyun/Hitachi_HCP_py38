import bs4
import xmltojson

with open('tenant_detail.html', encoding='utf-8') as f:
    html = f.read()
bs_ = bs4.BeautifulSoup(html, 'html.parser')
print(bs_)
#
# with open("tenant_input_action.html", "r") as html_file:
#     html = html_file.read()
#     json_ = xmltojson.parse(html)

# print(json)

#
# table = bs_.find('table', {'class': 'filterSortPageTableData tableExpand'})
# # print(table)
#
# print(table.select('td.span.ellipses'))

tenant=bs_.select('#titleRow_54b198e5-b0aa-467e-b6bd-ce4a14564eac > td.titleLeft.arrow.name > span.ellipses')
print(tenant)
tenant=bs_.select('#titleRow_54b198e5-b0aa-467e-b6bd-ce4a14564eac > td.titleLeft.objects > span')
print(tenant)
tenant=bs_.select('#titleRow_54b198e5-b0aa-467e-b6bd-ce4a14564eac > td.titleRight.storageUsed > div:nth-child(1)')
print(tenant)



