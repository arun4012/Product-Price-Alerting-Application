import smtplib
from email.message import EmailMessage

def alert_system(product, link, receiver_mail_id):
    email_id = 'autopricetracker@gmail.com'
    email_pass = 'PriceTracker@00'

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert'
    msg['From'] = email_id
    msg['To'] = receiver_mail_id # receiver address
    msg.set_content(f'Hey, price of {product} dropped!\n{link}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)


email = input()
product = "Samsung Galaxy M32 (Black, 6GB RAM, 128GB Storage) 6 Months Free Screen Replacement for Prime"
link = input()
alert_system(product, link, email)