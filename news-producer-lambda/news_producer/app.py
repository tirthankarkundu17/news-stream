import json
from datetime import datetime, timedelta

from news_fetcher import NewsFetcher
from redpanda import RedPanda


def handler(event, context):
    current_datetime = datetime.now()
    redpanda = RedPanda(topic="news-raw")

    # Calculate the datetime 2 hours ago
    two_hours_ago = current_datetime - timedelta(hours=2)

    fetcher = NewsFetcher(start_date=two_hours_ago, end_date=current_datetime)
    news_list = fetcher.get_latest_google_news()
    for news in news_list:
        redpanda.produce("news", news)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "News produced successfully"}),
    }
