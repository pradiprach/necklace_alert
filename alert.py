from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

import requests
import os
from bs4 import BeautifulSoup


def send_alert():
    my_email = os.environ.get("SMTP_EMAIL")
    password = os.environ.get("SMTP_PASSWORD")
    to_email = os.environ.get("TO_EMAIL")

    msg = f"Mom Temple Haar Available! Buy Now!"
    message = MIMEMultipart()
    message['From'] = my_email
    message['To'] = to_email
    message['Subject'] = msg
    message.attach(MIMEText(msg, 'plain'))

    with SMTP("smtp-relay.brevo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=message.as_string())


def check_availability():
    URL = "https://preetjewellery.com/product/new-copper-haar/"
    response = requests.get(url=URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    button = soup.select_one("button.single_add_to_cart_button.button.alt")
    if button is not None and button.text == "Add to cart":
        send_alert()
    else:
        print("Stock not available!")


if __name__ == "__main__":
    check_availability()
