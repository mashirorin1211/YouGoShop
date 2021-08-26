import requests
import urllib #解析 URL 中的參數(query)
from abc import ABC, abstractclassmethod
# from bs4 import BeautifulSoup

class Website(ABC):
    def __init__(self):
        pass
    def search(self, keyword):
        self.keyword = keyword

class Shopee(Website):
    def search(self, keyword):
        referer = f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
            'x-api-source': 'pc',
            'referer': referer,
        }
        result = []
        search_api_url = 'https://shopee.tw/api/v4/search/search_items'
        query_args = f"by=relevancy&keyword={keyword}&limit=100&newest=0&order=asc&page_type=search&version=2"
        url = search_api_url + '?' + query_args
        response = requests.get(url, headers=headers)
        items = response.json()['items']
        for i in range(100):
            title = items[i]['item_basic']['name']
            price = int(items[i]['item_basic']['price'])//100000
            photo = 'https://cf.shopee.tw/file/' + str(items[i]['item_basic']['image']) + '_tn'
            link = 'https://shopee.tw/product/' + str(items[i]['item_basic']['shopid']) + '/' + str(items[i]['item_basic']['itemid'])
            source = 'https://shopee.tw/favicon.ico'
            result.append(
                dict(product_title=title, product_price=price, product_photo=photo, product_page=link, product_source=source)
            )
        return result
    def get_campaigns(self):
        result = []
        campaign_url = 'https://shopee.tw/api/v2/campaigns/get_items?campaign_type=0&limit=100'
        response = requests.get(campaign_url)
        res = response.json()['data']
        campaigns = res['items']
        limit = res['total']
        for i in range(limit):
            name = campaigns[i]['name']
            link = campaigns[i]['landing_page']
            photo = 'https://cf.shopee.tw/file/' + str(campaigns[i]['banner'])
            source = 'https://shopee.tw/favicon.ico'
            result.append(
                dict(campaign_name=name, campaign_link=link, campaign_photo=photo, campaign_source=source)
            )
        return result