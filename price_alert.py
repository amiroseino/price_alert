import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Function to get the current forex price
def get_forex_price(pair):
    try:
        ticker = yf.Ticker(pair + "=X")
        forex_price = ticker.history(period="1m")['Close'].iloc[-1]
        return forex_price
    except Exception as e:
        print(f"Failed to fetch {pair} price: {e}")
        return None

# Function to send an email notification
def send_email(sender_email, receiver_email, password, price, pair):
    subject = f"{pair} Price Alert"
    body = f"The current price of {pair} has reached {price}"

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

# Function to check the forex price periodically and send email if the price meets the target
def check_price_periodically(sender_email, receiver_email, password, target_price, pair):
    while True:
        current_price = get_forex_price(pair)
        if current_price:
            print(f"Current {pair} Price: {current_price}")
            if current_price >= target_price:
                send_email(sender_email, receiver_email, password, current_price, pair)
                break
        time.sleep(60)  # Check the price every 60 seconds

# Function to start the price check thread
def start_price_check():
    sender_email = sender_email_entry.get()
    receiver_email = receiver_email_entry.get()
    password = password_entry.get()
    target_price = float(price_entry.get())
    pair = forex_combobox.get()
    Thread(target=check_price_periodically, args=(sender_email, receiver_email, password, target_price, pair)).start()

# Function to update the current price in the target price entry box
def update_current_price(event):
    pair = forex_combobox.get()
    current_price = get_forex_price(pair)
    if current_price:
        price_entry.delete(0, tk.END)
        price_entry.insert(0, f"{current_price:.2f}")

# Setting up the GUI
root = tk.Tk()
root.title("Forex Price Alert")

ttk.Label(root, text="Sender Email:").grid(column=0, row=0, padx=10, pady=5)
sender_email_entry = ttk.Entry(root, width=30)
sender_email_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(root, text="Receiver Email:").grid(column=0, row=1, padx=10, pady=5)
receiver_email_entry = ttk.Entry(root, width=30)
receiver_email_entry.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(root, text="Email Password:").grid(column=0, row=2, padx=10, pady=5)
password_entry = ttk.Entry(root, width=30, show="*")
password_entry.grid(column=1, row=2, padx=10, pady=5)

ttk.Label(root, text="Forex Pair:").grid(column=0, row=3, padx=10, pady=5)
forex_combobox = ttk.Combobox(root, values=["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"], width=27)
forex_combobox.grid(column=1, row=3, padx=10, pady=5)
forex_combobox.set("EURUSD")  # Set default value
forex_combobox.bind("<<ComboboxSelected>>", update_current_price)  # Bind event

ttk.Label(root, text="Target Price:").grid(column=0, row=4, padx=10, pady=5)
price_entry = ttk.Entry(root, width=30)
price_entry.grid(column=1, row=4, padx=10, pady=5)

start_button = ttk.Button(root, text="Start Price Check", command=start_price_check)
start_button.grid(column=0, row=5, columnspan=2, pady=10)

root.mainloop()
