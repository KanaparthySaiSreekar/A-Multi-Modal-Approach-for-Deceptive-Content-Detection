from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
import time
import requests
from datetime import *

googlenews = GoogleNews(lang="en")
# RSS feed link = https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en


class newsFeed:

    def __init__(self):
        self.search_query = ""
        self.date = ""
        # self.location = ""

    def get_next_date(self, given_date):
        next_day = given_date.day
        next_month = given_date.month
        next_year = given_date.year
        if given_date.day >= 30:
            next_day = 1
            if given_date.month == 12:
                next_month = 1
                next_year = given_date.year + 1
            else:
                next_month = given_date.month + 1
        else:
            next_day = given_date.day + 1
        next_date = date(next_year, next_month, next_day)
        return next_date

    def get_summary(self, val_string):
        html = f"""{val_string}"""
        soup = BeautifulSoup(html, "html.parser")
        text = ""
        try:
            list_items = soup.ol.find_all("li")
            text_list = [item.get_text(strip=True) for item in list_items]
            text = " ".join(text_list)
        except:
            a_tag = soup.find("a")
            text = a_tag.get_text(strip=True)
        return text

    def get_top_news(self, feed_contents=None):
        global googlenews
        if feed_contents is not None:
            today_news = feed_contents
        else:
            googlenews.get_news()
            today_news = googlenews.results()

        news_cards = []
        for item in today_news:
            news = dict()
            news["title"] = item["title"]
            news["link"] = item["link"]

            if "summary_detail" in item and "value" in item["summary_detail"]:
                news["summary"] = self.get_summary(item["summary_detail"]["value"])
            else:
                # If 'summary_detail' key is not present, set the summary to None or handle accordingly
                news["summary"] = None

            if "published" in item:
                news["published"] = item["published"]
            # news["published"] = item["published"]
            else:
                # If 'published' key is not present, set it to None or handle accordingly
                news["published"] = None
            # news["source"] = item["source"]["title"]
            if "source" in item and "title" in item["source"]:
                news["source"] = item["source"]["title"]
            else:
                # If 'source' key is not present, set it to None or handle accordingly
                news["source"] = None
            # news["source_link"] = item["source"]["href"]
            if "source" in item and "title" in item["source"]:
                news["source"] = item["source"]["title"]
            else:
                # If 'source' key is not present or doesn't have 'title', set it to None or handle accordingly
                news["source"] = None

            # news["summary"] = self.get_summary(item["summary_detail"]["value"])
            if "source" in item and "href" in item["source"]:
                news["source_link"] = item["source"]["href"]
            else:
                # If 'source' key is not present or doesn't have 'href', set it to None or handle accordingly
                news["source_link"] = None
            news_cards.append(news)

        # first_news_item = today_news[0]
        # publisher_details = [
        #     first_news_item["feed"]["link"],
        #     first_news_item["feed"]["publisher"],
        #     first_news_item["feed"]["rights"],
        # ]
        # for i in news_cards:
        #     print(i)
        # if today_news:
        #     first_news_item = today_news[0]
        #     publisher_details = [
        #         first_news_item["feed"].get("link"),
        #         first_news_item["feed"].get("publisher"),
        #         first_news_item["feed"].get("rights"),
        #     ]
        # else:
        #     # If no news items are available, set publisher details to None or handle accordingly
        #     publisher_details = [None, None, None]
        first_news_item = today_news[0] if today_news else {}
        publisher_details = [
            first_news_item.get("link"),
            first_news_item.get("publisher"),
            first_news_item.get("rights"),
        ]
        return publisher_details, news_cards

    def get_all_news_by_location(self, country):
        global googlenews
        googlenews = GoogleNews(lang="en")

    def get_all_news_by_date(self, dat, dx=None):
        # global googlenews
        # given_date = date(int(dat[0]), int(dat[1]), int(dat[2]))
        # current = datetime.now()
        # current_date = date(current.year, current.month, current.day)
        # next_date = self.get_next_date(given_date)
        # difference_days = (next_date - given_date).days
        # if dx is None:
        #     dx = "news"
        # if difference_days <= 0:
        #     feed_contents = googlenews.top_news()
        #     return self.get_top_news(feed_contents=feed_contents)
        global googlenews
        given_date = date(int(dat[0]), int(dat[1]), int(dat[2]))
        current = datetime.now()
        current_date = date(current.year, current.month, current.day)
        next_date = self.get_next_date(given_date)
        difference_days = (next_date - given_date).days
        if dx is None:
            dx = "news"
        if difference_days <= 0:
            feed_contents = googlenews.top_news()
            return self.get_top_news(feed_contents=feed_contents)

        # Perform the search without specifying the date range
        feed_contents = googlenews.search(dx)
        return self.get_top_news(feed_contents=feed_contents)

        # feed_contents = googlenews.search(
        #     dx,
        #     from_=f"{given_date.year}-{given_date.month}-{given_date.day}",
        #     to_=f"{next_date.year}-{next_date.month}-{next_date.day}",
        # )
        # return self.get_top_news(feed_contents=feed_contents)

    def get_all_news_by_topic(self, topic):
        global googlenews
        feed_contents = googlenews.search(query=topic)
        return self.get_top_news(feed_contents=feed_contents)

    def run(self, query, give_date, location):
        self.search_query = query
        self.date = give_date
        self.location = location
        if self.location != "":
            self.get_all_news_by_location(self.location)
        if self.date != "":
            if self.search_query != "":
                return self.get_all_news_by_date(self.date, self.search_query)
            else:
                return self.get_all_news_by_date(self.date)
        elif self.search_query != "":
            return self.get_all_news_by_topic(self.search_query)
        else:
            return self.get_top_news()
