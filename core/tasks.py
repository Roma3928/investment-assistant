from celery.utils.log import get_task_logger
from investment.celery import app
from scraper import InvestmintClient, HTMLExtractor
from core.models import Company, CompanyCategory, Promotion

logger = get_task_logger(__name__)


@app.task(name='fetch-investment-promotions', bind=True)
def fetch_promotions(self):
    cli = InvestmintClient()

    for exchange, promotion_fetcher in zip(cli.exchanges, cli.promotions):
        for promotion in HTMLExtractor.extract_chart(promotion_fetcher()):
            print(f'{promotion!r}')
            if not promotion.company.name:
                continue
            try:
                company, created = Company.objects.update_or_create(
                    name=promotion.company.name,
                    exchange=exchange,
                    defaults={
                        'name': promotion.company.name,
                        'exchange': exchange,
                        'symbol': promotion.company.symbol,
                        'url': promotion.company.url,
                        'rate': promotion.price,
                        'income': promotion.income,
                    }
                )

                Promotion.objects.update_or_create(
                    company__name=company.name,
                    defaults={
                        'company': company,
                        'buy_to': promotion.buy_to,
                        'register': promotion.register,
                        'price': promotion.price,
                        'lot': promotion.lot,
                        'dividend': promotion.dividend,
                        'income': promotion.income,
                    }
                )
            except Exception as e:
                logger.info(e)


@app.task(name='fetch-company-information', bind=True)
def fetch_company_information(self):
    pass
