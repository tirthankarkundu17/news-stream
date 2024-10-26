from gnews import GNews


class NewsFetcher:
    def __init__(self, start_date, end_date, country=""):
        self.gnews_client = GNews(start_date=start_date, end_date=end_date, country=country)

    def get_latest_google_news(self):
        return self.gnews_client.get_news('latest news')
