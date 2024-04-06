import requests
from bs4 import BeautifulSoup
import re
import csv
import smtplib
import datetime
import time
import schedule
import matplotlib.pyplot as plt
import numpy as np

# Function to scrape product information
def scrape_product_info(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate, br, zstd", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    
    title = soup2.find(id="productTitle").get_text().strip()
    price = soup2.find(class_="a-price-whole").get_text().strip()

    # Clean up the data 
    price = re.sub(r'[^0-9]', '', price)

    # Convert to integer 
    price = int(price)

    return title, price

# Function to save product info to CSV
def save_to_csv(title, price):
    today = datetime.date.today()
    data = [title, price, today]

    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Function to check price and visualize historical prices
def check_price():
    URL = 'https://www.amazon.in/boAt-Launched-Airdopes-141-ANC/dp/B0C7QS9M38/ref=sr_1_7?crid=35JZ99A216173&dib=eyJ2IjoiMSJ9.JSxLeYYjVbx3nRdXglU9fEEjk6R8_NlbyhUOYowEp94jlIIEEqTWlrFxT8E30shIGzjK9ArsAIjzmAHJ09N7t8JOVgpmyWNtenR3Ql-Rby7aimn-7Y-040o9e0HYDm1kFF0UqsDMtJ9eBOXXyS8LxJ43NI5y3K0hN6duYF_J-4hm8WwC9keAJiSdZDqsA4ogkVbqBCwfRPQzuXwI5015UDKP0SVsAo_qQxGNC8YFh3xVlLI28yz3P11OsM3xQWg61nMymaH6Xjs92zGiHjm5fWibIr2gutkBJQSuX4QDnpY.20eLM_pXOONYsErrdIZR4Y_1z0dtPn94lYahQJnwz2I&dib_tag=se&keywords=boat+airdopes&qid=1712325351&s=electronics&sprefix=boat+a%2Celectronics%2C221&sr=1-7'
    
    title, price = scrape_product_info(URL)
    save_to_csv(title, price)

    if price < 1300:
        send_mail()

    # Visualize historical prices
    with open('AmazonWebScraperDataset.csv', 'r', newline='', encoding='UTF8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        rows = list(reader)
    
    dates = [datetime.datetime.strptime(row[2], '%Y-%m-%d') for row in rows]
    prices = [int(row[1]) for row in rows]

    # Plot historical prices
    plt.figure(figsize=(14, 6))

    # Line plot
    plt.subplot(1, 2, 1)
    plt.plot(dates, prices, marker='o', linestyle='-')
    plt.title('Historical Prices of Product')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Heatmap
    plt.subplot(1, 2, 2)
    heatmap_data = np.array(prices).reshape(-1, 1)
    plt.imshow(heatmap_data, cmap='YlGnBu', aspect='auto')
    plt.colorbar(label='Price (INR)')
    plt.title('Price Heatmap')
    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.tight_layout()
    plt.show()

# Function to send email notification

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login('email@email.com','password')
    #replace email@email.com and password accordingly....
    subject = "The Earphone you want is below 1300! Now is your chance to buy!"
    body = "Jeeva, This is the moment we have been waiting for. Now is your chance to pick up the earphone of your dreams. Don't mess it up! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data+analyst+tshirt&qid=1626655184&sr=8-3"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail('sendemail@email.com',msg)
    #replace sendemail@email.com to your emiail

# Schedule price check every day at a specific time
schedule.every().day.at("08:00").do(check_price)

# Run the scheduling loop
while True:
    schedule.run_pending()
    time.sleep(1)
