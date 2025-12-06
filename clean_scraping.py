import requests
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os

def chrome_driver():
    driver_path = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=ChromeService(driver_path), options=options)

driver = chrome_driver()

company_names = []
company_websites = []
company_phones = []
company_emails = []

url = "https://ukbusinessportal.co.uk/category/cleaning/"
driver.get(url)
time.sleep(10)

source_code = driver.page_source
soup = BeautifulSoup(source_code, 'html.parser')

company_details = soup.find_all('div', class_="pl-4")

for info in company_details:
    # Name
    name = info.find('h3').get_text(strip=True) if info.find('h3') else None
    
    # Website
    website_tag = info.find('a', href=re.compile(r'^https'))
    website = website_tag.get('href').strip() if website_tag else None
    
    # Phone
    phone_tag = info.find('a', href=re.compile(r'^tel'))
    phone = phone_tag.get('href').replace("tel:", "").strip() if phone_tag else None
    
    # Email
    email_tag = info.find('a', href=re.compile(r'^mailto'))
    email = email_tag.get('href').replace("mailto:", "").strip() if email_tag else None
    
    # Append inside the loop
    company_names.append(name)
    company_websites.append(website)
    company_phones.append(phone)
    company_emails.append(email)

# Build DataFrame
df = pd.DataFrame({
    'name': company_names,
    'website': company_websites,
    'email': company_emails,
    'phone': company_phones
})

df.to_csv('cleaning_info.csv', index=False)
print(f"Successful: {len(df)} rows scraped")