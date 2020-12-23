import pandas as pd
from pprint import pprint
import requests


url = "https://finviz.com/quote.ashx?t=AAPl"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


if __name__ == "__main__":

    r = requests.get(url, headers=headers)

    df = pd.read_html(r.text)
    pprint(df[5])
