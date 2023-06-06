import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib
from email.message import EmailMessage


def alert_system(product, link, receiver_mail_id):

    email_id = 'autopricetracker@gmail.com'
    email_pass = 'PriceTracker@22'

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert'
    msg['From'] = email_id
    msg['To'] = receiver_mail_id  # receiver address
    msg.set_content(f'Hey, price of {product} dropped!\n{link}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)

    print("Notification Sent")


def add_product(receiver_mail_id, product, set_price, price, link):

    with open("price.csv", "a") as file:
        writer = csv.writer(file, lineterminator="\n")
        fields = ["Timestamp", "Email", "Product", "Set Price", "Price", "URL"]
        writer.writerow(fields)

        timestamp = f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp, receiver_mail_id, product, int(set_price), price, link])


def amazon(link):

    try:

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

        price = bs.find(class_='a-offscreen').get_text().strip()

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

    except:

        return None


def flipkart(link):

    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close'
        }

        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(class_='B_NuCI').get_text()
        product = str(title)
        product = product.strip()

        price = soup.find(class_='_30jeq3 _16Jk6d').get_text()
        price = price.replace('₹', '')
        price = price.replace(',', '')
        price = int(price)

        return [price, product]

    except:

        return None

