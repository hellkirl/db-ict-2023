from pymongo import MongoClient

import random
import time
from datetime import timedelta

import requests
from bs4 import BeautifulSoup as bs
from lab_02.bonus_task.credentials import MNG_HOST, MNG_PORT
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

fake = Faker()

client = MongoClient(host=MNG_HOST, port=int(MNG_PORT))
db = client['lab']

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)


class MarketingAgencyMongo:
    """Class "Marketing Agency" represents a db with containing collections with data"""

    def __init__(self, docs: int) -> None:
        """
        Initiating connection to the db, stating the number of docs of data to be generated
        :param docs: Number of docs to be generated
        """
        self.docs = docs

    def last_doc_number(self, collection: str) -> int:
        """
        Counts the length of collection
        :param collection: the name of a collection
        :return: number of docs in the collection
        """
        return len(list(client['lab'][collection].find()))

    def clients(self) -> None:
        """
        Fills collection "clients" with data according to its keys
        :return: None
        """
        id = self.last_doc_number('clients')
        for doc in range(1, self.docs + 1):
            db['clients'].insert_one(
                {
                    '_id': id + doc,
                    'name': fake.first_name(),
                    'surname': fake.last_name(),
                    'company': fake.company(),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                }
            )

    def filming_equipment(self) -> None:
        """
        Fills collection "filming_equipment" with data according to its keys
        :return:None
        """
        collection_len = self.last_doc_number('filming_equipment')

        page = 1
        data: [str] = []
        query = [
            collection['name']
            for collection in list(client['lab']['filming_equipment'].find())
        ]
        while len(data) + 1 < self.docs:
            url = f'https://www.amazon.com/s?k=camera&s=price-desc-rank&page={page}&crid=1IKESJ1ZISMFL&qid=1695817413&sprefix=camer%2Caps%2C186'
            driver.get(url)
            time.sleep(5)

            try:
                for title in driver.find_elements(
                    By.CSS_SELECTOR,
                    "span[class*='a-size-medium a-color-base a-text-normal']",
                ):
                    if title.text not in query:
                        data.append(title.text)
            except NoSuchElementException:
                break

            if len(data) + 1 >= self.docs:
                break

            page += 1

        for doc in range(1, self.docs + 1):
            db['filming_equipment'].insert_one(
                {
                    '_id': collection_len + doc,
                    'name': data[doc],
                    'type': 'camera',
                    'price': random.uniform(150, 2000),
                }
            )

    def inventory(self) -> None:
        """
        Fills collection "inventory" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('inventory')

        data: [str] = []
        page = 1
        url = f'https://www.filmtools.com/new-products?page={page}'
        driver.get(url)
        query = [
            collection['name']
            for collection in client['lab']['inventory'].find()
        ]

        while len(data) + 1 < self.docs:
            url = f'https://www.filmtools.com/new-products?page={page}'
            driver.get(url)
            time.sleep(5)

            query = [
                collection['name']
                for collection in client['lab']['inventory'].find()
            ]
            for title in driver.find_elements(
                By.CSS_SELECTOR, "div[class*='isp_product_title'"
            ):
                if title.text not in query:
                    data.append(title.text)

            if len(data) + 1 >= self.docs:
                break

            page += 1

        for doc in range(1, self.docs + 1):
            db['inventory'].insert_one(
                {
                    '_id': collection_len + doc,
                    'name': data[doc].replace('SmallRig ', ''),
                    'type': random.choice(('accessory', 'inventory')),
                    'property': fake.first_name(),
                    'price': round(random.uniform(0, 5000), 2),
                }
            )

    def locations(self) -> None:
        """
        Fills collection "locations" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('locations')
        for doc in range(1, self.docs + 1):
            db['locations'].insert_one(
                {
                    '_id': collection_len + doc,
                    'street': fake.street_name(),
                    'address': fake.address(),
                    'city': fake.city(),
                    'country': fake.country(),
                    'accessibility': random.choice(
                        (
                            'by foot',
                            'by car',
                            'by helicopter',
                            'by plane',
                            'by ship',
                            'by public transport',
                            'by train',
                        )
                    ),
                }
            )

    def media_files(self) -> None:
        """
        Fills collection "media_files" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('media_files')
        for doc in range(1, self.docs + 1):
            file = fake.file_path()
            db['media_files'].insert_one(
                {
                    '_id': collection_len + doc,
                    'file_name': file.split('/')[2].split('.')[0],
                    'file_type': file.split('.')[1],
                    'creation_date': fake.date_time_this_year(),
                    'path': file,
                }
            )

    def schedule(self) -> None:
        """
        Fills collection "schedule" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('schedule')
        for doc in range(1, self.docs + 1):
            date = fake.date_time_this_year()
            db['schedule'].insert_one(
                {
                    '_id': collection_len + doc,
                    'task_name': random.choice(
                        (
                            'shoot',
                            'consultation',
                            'design',
                            'contract',
                        )
                    ),
                    'start_date': date,
                    'end_date': date
                    + timedelta(
                        days=random.random(),
                        hours=random.random(),
                        minutes=random.random(),
                    ),
                }
            )

    def marketing_brief(self) -> None:
        """
        Fills collection "marketing_brief" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('marketing_brief')
        for doc in range(1, self.docs + 1):
            db['marketing_brief'].insert_one(
                {
                    '_id': collection_len + doc,
                    'target': random.choice(
                        [
                            business.text.split()[0]
                            for business in bs(
                                requests.get(
                                    'https://www.marketingtutor.net/types-of-business-industries/'
                                ).content,
                                'html.parser',
                            ).find_all('h3')
                        ]
                    ),
                    'audience': random.choice(
                        [
                            l[1]
                            for l in [
                                client.text.split('. ')
                                for client in bs(
                                    requests.get(
                                        'https://www.insightly.com/blog/types-of-customers/',
                                        headers={
                                            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
                                        },
                                    ).content,
                                    'html.parser',
                                )
                                .find('div', class_='post-content e-content')
                                .find_all('h3')
                            ]
                            if len(l) != 1
                        ]
                    ),
                    'budget': random.uniform(0.1, 5.0),
                    'deadline': fake.date_time_this_year(),
                    'client_id': random.randint(
                        1, self.last_doc_number('clients')
                    ),
                    'agency_id': random.randint(
                        1, self.last_doc_number('production_centre')
                    ),
                    'file_id': random.randint(
                        1, self.last_doc_number('media_files')
                    ),
                }
            )

    def production_centre(self) -> None:
        """
        Fills collection "production_centre" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('production_centre')
        for doc in range(1, self.docs + 1):
            db['production_centre'].insert_one(
                {
                    '_id': collection_len + doc,
                    'company': fake.company(),
                    'address': fake.street_address(),
                    'city': fake.city(),
                    'country': fake.country(),
                    'contact': fake.name(),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                    'creative_team_id': random.randint(
                        1, self.last_doc_number('creative_team_specialists')
                    ),
                    'task_id': random.randint(
                        1, self.last_doc_number('schedule')
                    ),
                    'brief_id': random.randint(
                        1, self.last_doc_number('marketing_brief')
                    ),
                }
            )

    def creative_team_specialists(self) -> None:
        """
        Fills collection "creative_team_specialists" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('creative_team_specialists')
        for doc in range(1, self.docs + 1):
            db['creative_team_specialists'].insert_one(
                {
                    '_id': collection_len + doc,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'sex': random.choice(('f', 'm')),
                    'age': random.randint(18, 65),
                    'specialty': fake.job(),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                    'equipment_id': random.randint(
                        1, self.last_doc_number('filming_equipment')
                    ),
                    'file_id': random.randint(
                        1, self.last_doc_number('media_files')
                    ),
                    'task_id': random.randint(
                        1, self.last_doc_number('schedule')
                    ),
                    'actor_id': random.randint(
                        1, self.last_doc_number('actors')
                    ),
                    'location_id': random.randint(
                        1, self.last_doc_number('locations')
                    ),
                }
            )

    def actors(self) -> None:
        """
        Fills collection "actors" with data according to its keys
        :return: None
        """
        collection_len = self.last_doc_number('actors')
        for doc in range(1, self.docs + 1):
            db['actors'].insert_one(
                {
                    '_id': collection_len + doc,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'sex': random.choice(('f', 'm')),
                    'age': random.randint(16, 80),
                    'genre': random.choice(
                        (
                            'drama',
                            'comedy',
                            'thriller',
                            'horror',
                            'musical',
                            'action',
                            'western',
                            'family',
                            'fantasy',
                            'adventure',
                            'crime',
                            'mystery',
                        )
                    ),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                    'location_id': random.randint(
                        1, self.last_doc_number('locations')
                    ),
                    'tool_id': random.randint(
                        1, self.last_doc_number('inventory')
                    ),
                }
            )


if __name__ == '__main__':
    marketing_agency = MarketingAgencyMongo(docs=int(input()))
    try:
        methods = (
            'clients',
            'locations',
            'filming_equipment',
            'inventory',
            'media_files',
            'schedule',
            'actors',
            'marketing_brief',
            'production_centre',
            'creative_team_specialists',
        )
        for method in methods:
            exec(f'marketing_agency.{method}()')
    except Exception as error:
        raise 'Something occurred. Please, try again...'
