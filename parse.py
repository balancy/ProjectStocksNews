import json
import requests
import datetime
from bs4 import BeautifulSoup


def get_tickers():
    """get the list of all tickers"""
    filename = "resources/tickers.json"
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_html(url):
    """getting response from url"""
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Network Error")
        return False


def get_news():
    """getting news from the feed rss"""

    list_news = list()
    html = get_html("https://www.marketwatch.com/markets?mod=top_nav")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            all_news = soup.find('div', class_='collection__elements '
                                               'j-scrollElement').findAll('div', class_='article__content')
            for one_news in all_news:
                title = one_news.find('a').text.strip()
                url = one_news.find('a')['href']
                summary = one_news.find('p', class_='article__summary').text
                date = one_news.find('span', class_='article__timestamp')['data-est']
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

                try:
                    ticker = one_news.find('span', class_='ticker__symbol').text
                except AttributeError:
                    ticker = ''

                try:
                    change = one_news.find('bg-quote', class_='ticker__change').text
                except AttributeError:
                    change = ''

                try:
                    author = one_news.find('span', class_='article__author').text
                except AttributeError:
                    author = ''

                list_news.append({'title': title, 'url': url, 'summary': summary, 'date': date, 'ticker': ticker,
                                  'change': change, 'author': author})

        except AttributeError:
            pass
    return list_news


if __name__ == "__main__":
    news = get_news()
    for _ in news:
        for key in _.keys():
            print(f"{key}: {_[key]}")
        print()
