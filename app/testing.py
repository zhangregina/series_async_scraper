import requests
from parsel import Selector
from config import DEFAULT_HEADERS

url = "https://rezka.ag/series/thriller/page/{}/"
ALL_COMPANIES_URL_XPATH = '//div[@class="b-content__inline_item-cover"]/a/@href'
# payload = {}
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-GB,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#
# }
for i in range(1,5):
    urlse = url.format(i)
    response = requests.request("GET", urlse, headers=DEFAULT_HEADERS)
    content = response.text
    tree = Selector(text=content)
    all_url = tree.xpath(ALL_COMPANIES_URL_XPATH).extract()
    for b in all_url:
        print(b)