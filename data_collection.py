import requests
from bs4 import BeautifulSoup
from db import store_data_in_db  # Import the function to store data

def scrape_health_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    return [p.get_text() for p in paragraphs]

def fetch_health_data(api_url, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)
    return response.json()

def save_health_data(url):
    health_data = scrape_health_data(url)
    store_data_in_db(health_data)  # Store the scraped data in the database 