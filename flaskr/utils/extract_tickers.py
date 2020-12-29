import csv
import json
import re


tickers = dict()
filename = "../static/data/ListingSecurityList.csv"
with open(filename, 'r', encoding='cp1251') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        pattern_to_search = "(Облигации)|(Инвестиционные паи)|(s_sec)"
        if not re.search(pattern_to_search, row[4]) and not row[3]:
            if re.search('Депозитарные расписки', row[4]):
                index_company_name = row[5].find('акций') + 6
                company_name = row[5][index_company_name:]
                if re.search('класса', company_name):
                    index_company_name = company_name.find('класса') + 9
                    company_name = company_name[index_company_name:]
            else:
                company_name = row[2]

            ticker = row[6]
            if '@' in ticker:
                ticker = ticker.replace('@', '.')
            tickers[ticker] = company_name


with open('../static/data/tickers.json', 'w') as outfile:
    json.dump(tickers, outfile, sort_keys=True)
