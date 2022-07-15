"""
This file was automatically generated of service
https://automatic-fox.ru/service/generator/web-scraper.
"""
# Enable logging
import logging
logging.basicConfig(
    format="%(asctime)s : %(lineno)d : %(name)s : %(levelname)s : %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
import requests
import json
from bs4 import BeautifulSoup
from dataclasses import dataclass

HEADERS = {
    "User-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36"
}

books = []

@dataclass
class BookItem:
    url: str
    title: str
    price: str
    description: str
    attribute: dict


    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "attribute": self.attribute
        }


def dump_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


def book(url):
    response = requests.get(url, headers=HEADERS)
    logger.info(f"{response} {url}")
    soup = BeautifulSoup(response.text, "html.parser")

    attrs = dict()

    table = soup.select_one(".table.table-striped")

    for tr in table.select("tr"):
        key = tr.select_one("th").text
        value = tr.select_one("td").text
        attrs[key] = value

    book_item = BookItem(
        url=url,
        title=soup.h1.text,
        price=soup.select_one("p.price_color").text,
        description=soup.select_one("#product_description + p").text,
        attribute=attrs
    )

    books.append(book_item.to_dict())

    dump_data("data.json", books)

def inspect(url):
    pass

def next_page(url):
    response = requests.get(url, headers=HEADERS)
    logger.info(f"{response} {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    for product in soup.select("ol li h3 a[title]"):
        rel_url = requests.compat.urljoin(url, product['href'])
        try:
            book(rel_url)
        except Exception:
            inspect(rel_url)


    next = soup.select_one("ul.pager li.next a")
    if next:
        rel_url2 = requests.compat.urljoin(url, next['href'])
        return next_page(rel_url2)


def main():
    logger.info("Work start")
    next_page("http://books.toscrape.com/index.html")
    logger.info("Work end")


if __name__ == '__main__':
    main()