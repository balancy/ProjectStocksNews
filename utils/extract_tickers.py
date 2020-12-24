import csv
import json
import re


tickers = dict()
filename = "../static/data/ListingSecurityList.csv"
with open(filename, 'r', encoding='cp1251') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        pattern_to_search = "Акции иностранного эмитента"
        type_of_field = row[5]
        if re.search(pattern_to_search, row[5]):
            ticker = row[6]
            if '@' in ticker:
                ticker = ticker.replace('@', '.')
            tickers[ticker] = row[2]


with open('../static/data/tickers.json', 'w') as outfile:
    json.dump(tickers, outfile)
