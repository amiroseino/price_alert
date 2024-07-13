import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Function to get the current coin price
def get_coin_price(coin):
    try:
        ticker = yf.Ticker(coin)
        coin_price = ticker.history(period="1m")['Close'].iloc[-1]
        return coin_price
    except Exception as e:
        print(f"Failed to fetch {coin} price: {e}")
        return None

# Function to send an email notification
def send_email(sender_email, receiver_email, password, price, coin):
    subject = f"{coin} Price Alert"
    body = f"The current price of {coin} has reached ${price}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email has been sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to check the coin price periodically and send email if the price meets the target
def check_price_periodically(sender_email, receiver_email, password, target_price, coin):
    while True:
        current_price = get_coin_price(coin)
        if current_price:
            print(f"Current {coin} Price: ${current_price}")
            if current_price >= target_price:
                send_email(sender_email, receiver_email, password, current_price, coin)
                break
        time.sleep(60)  # Check the price every 60 seconds

# Function to start the price check thread
def start_price_check():
    sender_email = sender_email_entry.get()
    receiver_email = receiver_email_entry.get()
    password = password_entry.get()
    target_price = float(price_entry.get())
    coin = coin_entry.get()
    Thread(target=check_price_periodically, args=(sender_email, receiver_email, password, target_price, coin)).start()

# Setting up the GUI
root = tk.Tk()
root.title("Price Alert")

ttk.Label(root, text="Sender Email:").grid(column=0, row=0, padx=10, pady=5)
sender_email_entry = ttk.Entry(root, width=30)
sender_email_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(root, text="Receiver Email:").grid(column=0, row=1, padx=10, pady=5)
receiver_email_entry = ttk.Entry(root, width=30)
receiver_email_entry.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(root, text="Email Password:").grid(column=0, row=2, padx=10, pady=5)
password_entry = ttk.Entry(root, width=30, show="*")
password_entry.grid(column=1, row=2, padx=10, pady=5)

ttk.Label(root, text="Coin Ticker:").grid(column=0, row=3, padx=10, pady=5)
coin_entry = ttk.Entry(root, width=30)
coin_entry.grid(column=1, row=3, padx=10, pady=5)

ttk.Label(root, text="Target Price:").grid(column=0, row=4, padx=10, pady=5)
price_entry = ttk.Entry(root, width=30)
price_entry.grid(column=1, row=4, padx=10, pady=5)

start_button = ttk.Button(root, text="Start Price Check", command=start_price_check)
start_button.grid(column=0, row=5, columnspan=2, pady=10)

root.mainloop()
