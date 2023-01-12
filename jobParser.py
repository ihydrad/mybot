import config
import customlog
import os
import re
import requests
import sqlite3

from datetime import datetime
from time import time
from bs4 import BeautifulSoup as bs


class JobParserDB():
    def __init__(self, table_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.table = table_name.lower()
        db_path = os.path.join(config.work_dir, "jobs.db")
        self.db = sqlite3.connect(db_path)

        if not self._table_exist:
            self._create_table()
        self.db = sqlite3.connect(db_path)

    @property
    def _table_exist(self):
        query = f"""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='{self.table}';
        """
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()

        return res

    def _create_table(self):
        table_create_query = f"""
            CREATE TABLE {self.table}
                                    (id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    salary_max REAL NOT NULL,
                                    salary_low REAL NOT NULL,
                                    create_date TIMESTAMP,
                                    close_date INTEGER);
        """
        cursor = self.db.cursor()
        cursor.execute(table_create_query)
        cursor.close()

    # TODO переделать
    @staticmethod
    def _calc_salary(salary: str, level: str):
        try:
            low, max = salary.replace(' ', '').strip('руб.').split('-')
        except ValueError:
            pattern = r"\d+\s*\d+"
            res = re.search(pattern, salary)
            res = res.group(0)
            res = res.replace(" ", "")
            return res
        if level == "low":
            return int(low)
        elif level == "max":
            return int(max)

    def _is_exist_job(self, table, job):
        query = f'SELECT close_date FROM {table} WHERE name="{job}";'
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()

        if not res:
            return False

        last_closed = res[-1][0]

        if last_closed is None:
            return True

        threshold_time = int(time()) - last_closed

        if threshold_time > config.job_add_threshold:
            return False

        return True

    def _db_fetchall(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()

        return res

    def _db_fetch(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()

        return res

    def _db_create_jobs(self, new_jobs: list, parsed_data: dict):
        query = """
            INSERT INTO {table}
            (name, salary_low, salary_max, create_date, close_date)
            VALUES
            ("{name}", {salary_low}, {salary_max}, {create_date}, {close_date});
        """

        cursor = self.db.cursor()

        for job in new_jobs:
            if self._is_exist_job(self.table, job) is False:

                query = query.format(table=self.table,
                                     name=job,
                                     salary_low=self._calc_salary(parsed_data[job], "low"),
                                     salary_max=self._calc_salary(parsed_data[job], "max"),
                                     create_date=int(time()),
                                     close_date="null"
                                     )

                cursor.execute(query)

            self.db.commit()
            cursor.close()

    def _db_close_jobs(self, removed_jobs: set):
        query = """
            UPDATE {table}
            SET close_date = {close_date}
            WHERE name == "{name}" AND close_date IS NULL;
        """
        cursor = self.db.cursor()

        for job in removed_jobs:
            query = query.format(table=self.table,
                                 name=job,
                                 close_date=int(time())
                                 )

            cursor.execute(query)
            self.db.commit()
            cursor.close()

    def db_get_all_active_jobs(self):
        query = f"""
            SELECT id, name, create_date FROM {self.table}
            WHERE close_date IS NULL;"""
        return self._db_fetchall(query)

    def db_get_all_closed_jobs(self):
        query = f"""
            SELECT id, name, create_date, close_date FROM {self.table}
            WHERE close_date IS NOT NULL;"""
        return self._db_fetchall(query)

    def db_get_all_job(self):
        query = f"SELECT id, name, create_date, close_date FROM {self.table};"
        return self._db_fetchall(query)

    def db_get_name_by_id(self, id):
        query = f"SELECT name FROM {self.table} WHERE id=={id};"
        return self._db_fetch(query)

    def db_get_salary_by_id(self, id):
        query = f"SELECT salary_low, salary_max FROM {self.table} WHERE id=={id};"
        return self._db_fetch(query)

    def db_update(self, myjobs, parsed_data):
        self._db_create_jobs(myjobs['added'], parsed_data)
        self._db_close_jobs(myjobs['removed'])

    def _close_db(self):
        self.db.close()


class JobParser(JobParserDB, customlog.LoggerFile):
    url = "https://vkomandu.ufanet.ru/vacancy/"

    def __init__(self, city, *args, **kwargs):
        super().__init__(*args, table_name=city, name=city, **kwargs)
        self.city = city
        self.name = config.cityes.get(city, None)
        self.__filter = None
        self.jobs_list = set()

    @property
    def filter_list(self):
        return self.__filter

    @filter_list.setter
    def filter_list(self, value: list):
        if isinstance(value, list):
            self.__filter = value
        else:
            raise Exception("Value must be type of list")

    def get_from_web(self) -> dict:
        data = dict()
        html = requests.get(JobParser.url + self.city).text
        soup = bs(html, 'html.parser')
        maindiv = soup.find("div", {"class": "main__list-vacancies vacancies"})
        vac = maindiv.find_all("div", {"class": "vacancy__item__wrap vacancy"})
        for item in vac:
            title = item.find("div", {"class": "vacancy__title"}).getText().strip()
            salary = item.find("div", {"class": "vacancy__salary"}).getText().strip()
            data[title] = salary
        return data

    @staticmethod
    def check_item_in_filter(item: str, filter_list: list) -> bool:
        return bool(any([filter_item.lower() in item.lower()
                         for filter_item in filter_list]))

    def get_cleared(self, listData: list) -> list:
        if not self.filter_list:
            return listData

        return [item for item in listData
                if self.check_item_in_filter(item, self.filter_list)]

    def prep_data(self) -> dict:
        sorted_data = dict()
        sorted_data['jobs'] = set(self.get_cleared(self.raw_data.keys()))
        sorted_data['removed'] = self.jobs_list - sorted_data['jobs']
        sorted_data['added'] = sorted_data['jobs'] - self.jobs_list
        self.jobs_list = sorted_data['jobs'].copy()

        if not (sorted_data['jobs'] | sorted_data['removed']):
            return 0
        return sorted_data

    @staticmethod
    def conv_salary(salary) -> str:
        msg = ''
        salary = list(map(int, salary))
        salary = list(map(lambda x: int(x/1000), salary))
        if salary[0] != salary[1]:
            msg = str(salary[0])+'-'+str(salary[1])+' тыс.руб.'
        else:
            msg = str(salary[0])+' тыс.руб.'
        return msg

    def days_pass(self, start_time: int):
        time_now = datetime.fromtimestamp(time())
        time_created = datetime.fromtimestamp(start_time)
        return (time_now - time_created).days

    def fmt(self, name, state, salary=None) -> str:
        txt = ''
        if state == '+':
            txt = f'<b>{name}</b>'
        elif state == '-':
            txt = f'<s>{name}</s>'
        else:
            txt = f'{name}'
        return txt + f"\n<i>{self.conv_salary(salary)}</i>" + '\n' + '-'*45

    def get_jobs(self) -> tuple:
        for id, name, _, closed_time in self.db_get_all_closed_jobs():
            if not self.days_pass(closed_time):
                salary = self.db_get_salary_by_id(id)

                yield id, self.fmt(name=name,
                                   state="-",
                                   salary=salary)

        for id, name, create_time in self.db_get_all_active_jobs():
            salary = self.db_get_salary_by_id(id)

            yield id, self.fmt(name=name,
                               state=None if self.days_pass(create_time) else "+",
                               salary=salary)

    def update(self, filter: list) -> bool:
        try:
            self.logger.debug("Cheking...")
            self.raw_data = self.get_from_web()
        except Exception as e:
            self.logger.debug(str(e))
            return False
        else:
            self.filter_list = filter
            data = self.prep_data()

            if not data:
                return False

            if (data['added'] | data['removed']):
                self.db_update(data, self.raw_data)
                return True

    def __repr__(self):
        return self.name
