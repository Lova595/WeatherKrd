import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


URL = 'https://sinoptik.ua/погода-краснодар/'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                     'application/signed-exchange;v=b3;q=0.9',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.'
                         '0.0.0 Safari/537.36'}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_main = soup.find_all('div', class_='main')
    items_temperature = soup.find_all('table', class_='weatherDetails')
    ready_main = []
    for item in items_main:
        ready_main.append({
            'day_week': f"День недели: {item.find(class_='day-link').get_text(strip=True).strip()}",
            'date': f"Дата: {item.find('p', class_='date').get_text(strip=True)} "
                    f"{item.find('p', class_='month').get_text(strip=True)}",
            'min': f"Минимальная температура: {item.find(class_='min').get_text(strip=True).split('.')[1]}",
            'max': f"Максимальная температура: {item.find(class_='max').get_text(strip=True).split('.')[1]}",
            'description': '\n ' + item.find(
                class_=f"weatherIco {item.find('img', class_='weatherImg').get('src').split('/m/')[1][:4]}").get(
                'title')
        })
    ready_temperature = []
    for item in items_temperature:
        ready_temperature.append(
            f'{item.find("tr", class_="temperature").get_text(strip=True)}')
        ready_temperature.append(
            f'{item.find("tr", class_="temperatureSens").get_text(strip=True)}')
    return ready_main, ready_temperature


def get_descriptions_weather(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='wDescription clearfix')
    ready = []
    for item in items:
        ready.append({
            'description': item.find("div", class_="description").get_text(strip=True)
        })
    return ready


def get_descriptions_calendar(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='oDescription clearfix')
    ready = []
    for item in items:
        ready.append(item.find(class_="description").get_text(strip=True))
    return ready


def game_guess_temp(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    item = soup.find('p', class_='today-temp').get_text(strip=True)
    return int(item[:-2])


def get_phrase_day(url='https://quote-citation.com/random'):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    item = soup.find('div', class_='quote-text').get_text(strip=True)
    return item


def start(flag):
    today = get_html(URL)
    day = datetime.today() + timedelta(days=1)
    tomorrow = get_html(URL+day.strftime('%Y-%m-%d'))
    if flag == 'today':
        content_today, temperature_today = get_content(today.text)
        description_today = get_descriptions_weather(today.text)
        folk_today = get_descriptions_calendar(today.text)
        return content_today, temperature_today, description_today, folk_today
    elif flag == 'tomorrow':
        content_tomorrow, temperature_tomorrow = get_content(tomorrow.text)
        description_tomorrow = get_descriptions_weather(tomorrow.text)
        folk_tomorrow = get_descriptions_calendar(tomorrow.text)
        return content_tomorrow, temperature_tomorrow, description_tomorrow, folk_tomorrow
