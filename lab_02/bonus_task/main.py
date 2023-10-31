import random
import time
from datetime import timedelta

import psycopg2
import requests
from bs4 import BeautifulSoup as bs
from credentials import DBNAME, HOST, PASSWORD, PORT, USER
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

fake = Faker()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)


def connect(
    database: str, host: str, username: str, password: str, port: int = 5432
) -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor] | None:
    """
    This function makes connection with database
    :return: tuple with connector ad cursor
    """
    try:
        con = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            port=port,
            host=host,
        )
        cur = con.cursor()
        con.set_session(autocommit=True)
        return con, cur
    except Exception as connection_error:
        print(f'The error is: {str(connection_error)}')
        return None


class MarketingAgency:
    """Class "Marketing Agency" represents a schema with containing tables with data"""

    def __init__(self, rows: int) -> None:
        """
        Initiating connection to the db, stating the number of rows of data to be generated
        :param rows: Number of rows to be generated
        """
        self.con, self.cur = connect(
            database=DBNAME,
            host=HOST,
            port=PORT,
            username=USER,
            password=PASSWORD,
        )
        self.rows = rows

    def last_row_number(self, table: str) -> int:
        """
        Counts the length of table
        :param table: the name of a table
        :return: number of rows in the table
        """
        self.cur.execute('SELECT COUNT(*) FROM %s' % table)
        return self.cur.fetchone()[0]

    def clients(self) -> None:
        """
        Fills table "clients" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('clients')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO clients (client_id, first_name, surname, company, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    fake.first_name(),
                    fake.last_name(),
                    fake.company(),
                    fake.email(),
                    fake.phone_number(),
                ),
            )

    def filming_equipment(self) -> None:
        """
        Fills table "filming_equipment" with data according to its columns
        :return:None
        """
        table_len = self.last_row_number('filming_equipment')

        page = 1
        data: [str] = []
        query = self.cur.execute(
            'SELECT equipment_name FROM filming_equipment'
        )
        result = [title[0] for title in self.cur.fetchall()]
        while len(data) + 1 < self.rows:
            url = f'https://www.amazon.com/s?k=camera&s=price-desc-rank&page={page}&crid=1IKESJ1ZISMFL&qid=1695817413&sprefix=camer%2Caps%2C186'
            driver.get(url)
            time.sleep(5)

            try:
                for title in driver.find_elements(
                    By.CSS_SELECTOR,
                    "span[class*='a-size-medium a-color-base a-text-normal']",
                ):
                    if title.text not in result:
                        data.append(title.text)
            except NoSuchElementException:
                break

            if len(data) + 1 >= self.rows:
                break

            page += 1

        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO filming_equipment VALUES (%s, %s, %s, %s)',
                (
                    table_len + row,
                    data[row],
                    'camera',
                    random.uniform(150, 2000),
                ),
            )

    def inventory(self) -> None:
        """
        Fills table "inventory" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('inventory')

        data: [str] = []
        page = 1
        url = f'https://www.filmtools.com/new-products?page={page}'
        driver.get(url)
        query = self.cur.execute('SELECT tool_name FROM inventory')
        result = [title[0] for title in self.cur.fetchall()]

        while len(data) + 1 < self.rows:
            url = f'https://www.filmtools.com/new-products?page={page}'
            driver.get(url)
            time.sleep(5)

            query = self.cur.execute('SELECT tool_name FROM inventory')
            for title in driver.find_elements(
                By.CSS_SELECTOR, "div[class*='isp_product_title'"
            ):
                if title.text not in result:
                    data.append(title.text)

            if len(data) + 1 >= self.rows:
                break

            page += 1

        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO inventory (tool_id, tool_name, tool_type, tool_property, tool_price) VALUES (%s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    data[row].replace('SmallRig ', ''),
                    random.choice(('accessory', 'inventory')),
                    fake.first_name(),
                    round(random.uniform(0, 5000), 2),
                ),
            )

    def locations(self) -> None:
        """
        Fills table "locations" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('locations')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO locations (location_id, location_name, location_address, location_town, location_country, location_accessibility) VALUES (%s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    fake.street_name(),
                    fake.address(),
                    fake.city(),
                    fake.country(),
                    random.choice(
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
                ),
            )

    def media_files(self) -> None:
        """
        Fills table "media_files" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('media_files')
        for row in range(1, self.rows + 1):
            file = fake.file_path()
            self.cur.execute(
                'INSERT INTO media_files (file_id, file_name, file_type, file_creation_date, file_path) VALUES (%s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    file.split('/')[2].split('.')[0],
                    file.split('.')[1],
                    fake.date_time_this_year(),
                    file,
                ),
            )

    def schedule(self) -> None:
        """
        Fills table "schedule" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('schedule')
        for row in range(1, self.rows + 1):
            date = fake.date_time_this_year()
            self.cur.execute(
                'INSERT INTO schedule (task_id, task_name, task_start, task_finish) VALUES (%s, %s, %s, %s)',
                (
                    table_len + row,
                    random.choice(
                        (
                            'shoot',
                            'consultation',
                            'design',
                            'contract',
                        )
                    ),
                    date,
                    date
                    + timedelta(
                        days=random.random(),
                        hours=random.random(),
                        minutes=random.random(),
                    ),
                ),
            )

    def marketing_brief(self) -> None:
        """
        Fills table "marketing_brief" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('marketing_brief')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO marketing_brief (brief_id, brief_aim, brief_target_audience, brief_budget, brief_deadline, client_id, file_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    random.choice(
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
                    random.choice(
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
                    random.uniform(0.1, 5.0),
                    fake.date_time_this_year(),
                    random.randint(1, self.last_row_number('clients')),
                    random.randint(1, self.last_row_number('media_files')),
                ),
            )

    def production_centre(self) -> None:
        """
        Fills table "production_centre" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('production_centre')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO production_centre (production_centre_id, production_centre_name, production_centre_address, production_centre_town, production_centre_country, production_centre_contact_person, production_centre_email, production_centre_phone, creative_team_id, task_id, brief_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    fake.company(),
                    fake.street_address(),
                    fake.city(),
                    fake.country(),
                    fake.name(),
                    fake.email(),
                    fake.phone_number(),
                    random.randint(
                        1, self.last_row_number('creative_team_specialists')
                    ),
                    random.randint(1, self.last_row_number('schedule')),
                    random.randint(1, self.last_row_number('marketing_brief')),
                ),
            )

    def creative_team_specialists(self) -> None:
        """
        Fills table "creative_team_specialists" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('creative_team_specialists')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO creative_team_specialists VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    fake.first_name(),
                    fake.last_name(),
                    random.choice(('f', 'm')),
                    random.randint(18, 65),
                    fake.job(),
                    fake.email(),
                    fake.phone_number(),
                    random.randint(
                        1, self.last_row_number('filming_equipment')
                    ),
                    random.randint(1, self.last_row_number('media_files')),
                    random.randint(1, self.last_row_number('schedule')),
                    random.randint(1, self.last_row_number('actors')),
                    random.randint(1, self.last_row_number('locations')),
                ),
            )

    def actors(self) -> None:
        """
        Fills table "actors" with data according to its columns
        :return: None
        """
        table_len = self.last_row_number('actors')
        for row in range(1, self.rows + 1):
            self.cur.execute(
                'INSERT INTO actors (actor_id, actor_first_name, actor_surname, actor_sex, actor_age, actor_specialization, actor_email, actor_phone, tool_id, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    table_len + row,
                    fake.first_name(),
                    fake.last_name(),
                    random.choice(('f', 'm')),
                    random.randint(16, 80),
                    random.choice(
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
                    fake.email(),
                    fake.phone_number(),
                    random.randint(1, self.last_row_number('inventory')),
                    random.randint(1, self.last_row_number('locations')),
                ),
            )


if __name__ == '__main__':
    marketing_agency = MarketingAgency(rows=int(input()))
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
