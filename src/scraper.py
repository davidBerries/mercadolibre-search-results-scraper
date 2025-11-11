thonimport requests
import json
from bs4 import BeautifulSoup

class MercadoLibreScraper:
    def __init__(self, search_url, max_items=100):
        self.search_url = search_url
        self.max_items = max_items
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def get_page_data(self, page_url):
        response = requests.get(page_url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_url}")
            return None
        return BeautifulSoup(response.text, 'html.parser')

    def parse_product_data(self, soup):
        products = []
        product_elements = soup.find_all('li', {'class': 'ui-search-layout__item'})
        for product_element in product_elements:
            title = product_element.find('h2', {'class': 'ui-search-item__title'})
            price = product_element.find('span', {'class': 'price-tag-fraction'})
            product_data = {
                'title': title.text if title else 'No title',
                'price': price.text if price else 'No price',
                'url': product_element.find('a')['href'],
            }
            products.append(product_data)
        return products

    def scrape(self):
        all_products = []
        page_num = 1
        while len(all_products) < self.max_items:
            page_url = f"{self.search_url}?page={page_num}"
            soup = self.get_page_data(page_url)
            if not soup:
                break
            products = self.parse_product_data(soup)
            all_products.extend(products)
            if len(products) == 0:
                break
            page_num += 1
        return all_products

if __name__ == '__main__':
    search_url = 'https://www.mercadolibre.com.ar/jm/search?from=home&keyword=termicos'
    scraper = MercadoLibreScraper(search_url)
    data = scraper.scrape()
    with open('data/sample_output.json', 'w') as f:
        json.dump(data, f, indent=4)