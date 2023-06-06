import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib
from email.message import EmailMessage


def amazon(link):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }

    page = requests.get(link, headers=headers)

    bs = BeautifulSoup(page.content, 'html.parser')

    price = bs.find(class_='a-offscreen').get_text()

    product = bs.find(id="productTitle").get_text().strip()

    if '(' in product:
        end = product.index('(')
    else:
        end = len(product)

    product = product[:end].strip()

    for i in range(len(price)):
        if price[i] == '₹':
            start_ind = i
        if price[i] == '.':
            end_ind = i
            break

    price = int(price[start_ind + 1:end_ind].replace(',', ''))

    return [price, product]


print(amazon(input()))

