import os.path, sys
import pytest
from time import sleep

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cur_dir, os.pardir))

from jobParser import JobParser

jobs_list = [
        {
        "C++ developer": "200000 - 250000 руб.",
        "Python developer": "150000 - 200000",
        "QA eng": "100000",
    },
]


class JobParserDummy(JobParser):
    def __init__(self, city, jobs):
        super().__init__(city)
        self.jobs_list = jobs

    def get_from_web(self):
        return self.jobs_list

    @staticmethod
    def get_output_count(data):
        items = data.strip().split("-------------------------")
        return len([item for item in items if item])

@pytest.fixture(scope="session", params=jobs_list)
def dummy(rm_db, request):
    return JobParserDummy("Dummy", request.param)

@pytest.fixture()
def jobs_updated(dummy):
    _ = dummy.get_fmt_jobs()

@pytest.fixture(scope="session")
def rm_db():
    try:
        os.remove("jobs.db")
    except:
        pass

def test_count_new_jobs(dummy):
     assert len(dummy.jobs) == dummy.get_output_count(dummy.get_fmt_jobs()), "Разное количество вакансий на входе и на выходе"

def test_remove_job(dummy, jobs_updated):
    dummy.jobs.pop("C++ developer")
    assert "<s>" in dummy.get_fmt_jobs(), "Отсутствует удаленная вакансия в результате"

def test_add_job(dummy, jobs_updated):
    dummy.jobs["Java dev"] = "250000"
    out = dummy.get_fmt_jobs()
    assert "<b>" in out, "Отсутствует новая вакансия в результате"

salary_list = ["237500руб.", "237500  руб.", "23 7500руб.", "237500р.", "237500", "237500 - 250000"]

@pytest.mark.parametrize("salary", salary_list)
def test_low_salary(dummy, jobs_updated, salary):
    query_loe_salary = f'SELECT salary_low FROM Dummy WHERE name == "{salary}"'
    dummy.jobs[f"{salary}"] = salary
    _ = dummy.get_fmt_jobs()
    cursor = dummy.db.cursor()
    cursor.execute(query_loe_salary)
    salary_low = cursor.fetchone()
    cursor.close()
    assert 237500 == int(salary_low[0]), "Отстуствует зарплата у вакансии"

@pytest.mark.parametrize("salary", salary_list)
def test_hi_salary(dummy, jobs_updated, salary):
    query_hi_salary = f'SELECT salary_max FROM Dummy WHERE name == "{salary}"'
    dummy.jobs[f"{salary}"] = salary
    _ = dummy.get_fmt_jobs()
    cursor = dummy.db.cursor()
    cursor.execute(query_hi_salary)
    salary_hi = cursor.fetchone()
    cursor.close()
    if "-" in salary:
        assert 250000 == int(salary_hi[0])
    else:
        assert 237500 == int(salary_hi[0])
    

