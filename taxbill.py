
import csv
import os
import re
import sys

from bs4 import BeautifulSoup

fields = {
    'Bill #': 'String',
    'Unique ID': 'String',
    'District': 'String',
    'Name': 'String',
    'Care Of': 'String',
    'Address': 'String',
    'Property Location': 'String',
    'MBL': 'String',
    'Volume & Page': 'String',
    'Gross Assessment': 'Integer',
    'Exemptions': 'Integer',
    'Net Assessment': 'Integer',
    'Town Mill Rate': 'String',
    'Town Benefit': 'String',
    'Elderly Benefit (C)': 'String',
    '_BNUM': 'Integer',
    '_MAP': 'String',
    '_LOT': 'String'
}

def find(div, field):
    try:
        expression = re.compile(re.escape(field))
        text = div.find('td', text=expression).find_next('td').text
        text = re.sub(r'\s+', ' ', text).strip()
        if fields[field] == 'Integer':
            text = text.replace(',', '')
        return text
    except AttributeError:
        return None

if __name__ == '__main__':
    fieldnames = list(fields.keys())
    # The .csvt file makes QGIS import the data types correctly
    with open('taxbill.csvt', 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(fields[field] for field in fieldnames)
    with open('taxbill.csv', 'w') as fp:
        fieldnames2 = (fieldname.replace(' ', '') for fieldname in fieldnames)
        writer = csv.DictWriter(fp, fieldnames=fieldnames2)
        writer.writeheader()
        for filename in os.listdir():
            print(filename, file=sys.stderr)
            soup = BeautifulSoup(open(filename, 'rb'), 'lxml')
            div = soup.find('div', {'class': 'detail-info'})
            row = {field: find(div, field) for field in fields}
            if not row.get('Unique ID'):
                continue
            row['_BNUM'] = filename
            if row.get('MBL'):
                row['_MAP'], row['_LOT'] = row['MBL'].split(None, 1)
            writer.writerow(row)
