from celery.utils.log import get_task_logger
from investment.celery import app
from scraper import InvestmintClient, HTMLExtractor
from news.models import News

logger = get_task_logger(__name__)


@app.task(name='fetch-investment-news', bind=True)
def fetch_news(self):
    last_news = News.objects.all().last()
    print(f'{last_news!r}')
    cli = InvestmintClient()
    for news in HTMLExtractor.extract_news(cli.fetch_news()):
        print(news)
        if last_news and last_news.url == news.link:
            break

        News.objects.create(
            title=news.title,
            url=news.link,
            date=news.date,
        )
