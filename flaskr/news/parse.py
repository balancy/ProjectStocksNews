from bs4 import BeautifulSoup
import datetime
import json
import requests
import config


def get_tickers():
    """
    Gets stocks tickers from the json file.
    :return: tickers in the form of dictionary
    """

    filename = config.TICKERS_FILENAME
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_html(url):
    """
    Gets html response text.
    :param url: html url
    :return: html response text
    """

    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Network Error")
        return False


def get_one_record_news(one_news, tickers_spb):
    """
    Gets one parsed news in the form of dictionary
    :param one_news: link to one news
    :param tickers_spb: flag to see if ticker traded on SPB stocks exchange
    :return: dictionary
    """

    one_news = one_news.find('div', class_='article__content')

    title = one_news.find('a').text.strip()
    url = one_news.find('a')['href']
    summary = one_news.find('p', class_='article__summary').text
    date = one_news.find('span', class_='article__timestamp')['data-est']
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

    ticker = one_news.find('span', class_='ticker__symbol')
    ticker = ticker.text if ticker else ''

    change = one_news.find('bg-quote', class_='ticker__change')
    change = float(change.text[:-1]) if change else 0.0

    author = one_news.find('span', class_='article__author')
    author = author.text if author else ''

    is_on_spb = True if ticker in tickers_spb else False

    one_record_dict = {'title': title, 'url': url, 'summary': summary, 'date': date, 'ticker': ticker,
                       'change': change, 'author': author, 'is_on_spb': is_on_spb}

    return one_record_dict


def get_news():
    """
    Parsing all news from site RSS.
    :return: all news in the form of list of dictionaries
    """

    list_news = list()
    html = get_html(config.RSS_URL)
    if html:
        tickers_spb = get_tickers()
        soup = BeautifulSoup(html, 'html.parser')
        try:
            all_news = soup.find('div', class_='collection__elements '
                                               'j-scrollElement').find_all('div', class_='element element--article')
            for one_news in all_news:
                record_one_news = get_one_record_news(one_news, tickers_spb)
                list_news.append(record_one_news)

        except AttributeError:
            pass
    return list_news
