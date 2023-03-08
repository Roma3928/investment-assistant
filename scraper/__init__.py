import json
import logging
import unicodedata
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from scraper.types import News, Company, Promotion


class InvestmintClient:
    URL = 'https://investmint.ru'

    def __init__(self):
        self.promotions = (
            self.fetch_promotions,
            self.fetch_spb_promotion
        )
        self.exchanges = (
            'Московская биржа',
            'СПб биржа'
        )

    def get(self, path):
        logging.info(f'Getting: {path} !\n')
        request = Request(
            f'{self.URL}/{path}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
            }
        )
        with urlopen(request) as response:
            return response.read().decode()

    def fetch_news(self):
        return self.get('news')

    def fetch_promotions(self):
        return self.get('')

    def fetch_spb_promotion(self):
        return self.get('?exchange=spb')

    def fetch_company_by_symbol(self, symbol):
        return self.get(symbol)


class HTMLExtractor:

    @staticmethod
    def extract_news(html):
        soup = BeautifulSoup(html, "html.parser")
        news_box = soup.find('div', class_="box")

        dates = [unicodedata.normalize("NFKD", p.get_text()) for p in news_box.find_all('p')]
        count = 0
        for date, ul in zip(dates, news_box.find_all('ul')):
            for li in ul.find_all('li'):
                a = li.find('a')
                count += 1
                yield News(
                    id=count,
                    title=a.get_text(),
                    link=a['href'],
                    date=date
                )

    @staticmethod
    def extract_chart(html):
        soup = BeautifulSoup(html, "html.parser")
        chart_table = soup.find('table', id="dividendnext")
        headers = [header.get_text(strip=True) for header in chart_table.find_all('th')]

        for row in chart_table.find_all('tr'):
            obj = {}
            for i, cell in enumerate(row.find_all('td')):
                if i == 0:
                    a = cell.find(href=True)
                    txt = a.div.get_text(strip=True)
                    symbol = a.span.get_text(strip=True)

                    obj.update({
                        headers[i]: txt,
                        'url': a['href'],
                        'symbol': symbol
                    })
                else:
                    obj[headers[i]] = unicodedata.normalize("NFKD", cell.get_text(strip=True))

            yield Promotion(
                company=Company(
                    name=obj.get(headers[0]),
                    symbol=obj.get('symbol'),
                    url=obj.get('url')
                ),
                buy_to=obj.get(headers[1]),
                register=obj.get(headers[2]),
                price=obj.get(headers[3]),
                lot=obj.get(headers[4]),
                dividend=obj.get(headers[5]),
                income=obj.get(headers[6]),
            )

    @staticmethod
    def extract_company_info(html):
        soup = BeautifulSoup(html, "html.parser")
        print(soup)


        yield


if __name__ == '__main__':

    cli = InvestmintClient()

    for symbol in ['peg-spb']:  # , 'bspbp', 'qiwi']:
        for news in HTMLExtractor.extract_company_info(cli.fetch_company_by_symbol(symbol)):
            print(news)
