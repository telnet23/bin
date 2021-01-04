import csv
import os
import requests
import sys

from lxml import etree

endpoint = os.environ.get('EBAY_ENDPOINT')
default_params = {
    'SECURITY-APPNAME': os.environ.get('EBAY_APPID'),
    'OPERATION-NAME': 'findItemsByKeywords',
    'paginationInput.pageNumber': 1,
    'outputSelector(0)': 'AspectHistogram',
    'outputSelector(1)': 'CategoryHistogram',
    'outputSelector(2)': 'ConditionHistogram',
    'outputSelector(3)': 'SellerInfo',
    'outputSelector(4)': 'StoreInfo',
}

if len(sys.argv) > 1:
    keywords_list = sys.argv[1:]
    csvfile = open(keywords_list[0] + '.csv', 'w')
else:
    keywords_list = [keywords.strip() for keywords in sys.stdin.readlines()]
    csvfile = sys.stdout

fieldnames = []
rows = []

for keywords in keywords_list:
    params = default_params.copy()
    params['keywords'] = keywords

    while True:
        print('GET', params, file=sys.stderr)
        response = requests.get(endpoint, params=params)

        root = etree.fromstring(response.content)
        for element in root.iter():
            element.tag = element.tag.split('}', 1)[1]

        for item in root.findall('searchResult/item'):
            tree = etree.ElementTree(item)
            row = {}
            for element in item.iter():
                key = tree.getelementpath(element)
                value = element.text
                if key == '.' or value == '' or value is None:
                    continue
                if key not in fieldnames:
                    fieldnames.append(key)
                row[key] = element.text
            row['X-Keywords'] = keywords
            rows.append(row)
            #print(row, file=sys.stderr)

        pageNumber = root.find('paginationOutput/pageNumber').text
        totalPages = root.find('paginationOutput/totalPages').text
        print('Page', pageNumber, 'of', totalPages, file=sys.stderr)

        params['paginationInput.pageNumber'] += 1
        if params['paginationInput.pageNumber'] > min(int(totalPages), 100):
            break

    rows.append({})

fieldnames.append('X-Keywords')
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(rows)
