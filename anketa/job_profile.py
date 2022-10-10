from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import anketa.unswers as unswers
from time import sleep


class Profile:
    def __init__(self, name, driver) -> None:
        self.name = name
        self.driver = driver

    def __get_item(self, item_name):
        self.driver.get(unswers.url_ufa)
        WebDriverWait(self.driver, 10)
        sleep(5)
        items = self.driver.find_elements(By.CLASS_NAME, "vacancy__title")
        for item in items:
            if item_name in item.text:
                return item.find_element(By.XPATH, '..')

    def open(self):
        vacancy = self.__get_item(self.name)
        btns = vacancy.find_elements(By.TAG_NAME, "button")
        for btn in btns:
            if "Заполнить анкету" in btn.text:
                btn.click()

    def __set_element_by_js(self, type_elem, elem, val):
        self.driver.execute_script(
                                    "arguments[0].value = arguments[1]",
                                    self.driver.find_element(type_elem, elem),
                                    val
                                   )

    def __sel_drop_menu(self, type_elem, elem, val):
        select_type = Select(self.driver.find_element(type_elem, elem))
        select_type.select_by_visible_text(val)

    def fill_page1(self):
        self.driver.find_element(By.NAME, "another_vacancies").send_keys(unswers.another_vacancies)
        self.driver.find_element(By.NAME, "surname").send_keys(unswers.surname)
        self.driver.find_element(By.NAME, "name").send_keys(unswers.name)
        self.driver.find_element(By.NAME, "fat_name").send_keys(unswers.fat_name)
        self.driver.find_element(By.NAME, "citizenship").send_keys(unswers.citizenship)
        self.driver.find_element(By.NAME, "adress_registration").send_keys(unswers.adress_registration)
        self.driver.find_element(By.NAME, "adress_residence").send_keys(unswers.adress_registration)
        self.driver.find_element(By.NAME, "email").send_keys(unswers.email)
        self.__set_element_by_js(By.ID, "id_phone", unswers.phone) # +7(999)999-99-99
        self.__set_element_by_js(By.ID, "id_birthday", unswers.birthday)

    def __fill_work(self, id, cur):
        if cur:
            self.driver.find_element(By.NAME, "current_work").click()
        self.__set_element_by_js(By.NAME, f"works-{id}-work_time", unswers.cur_work_time[id])
        self.driver.find_element(By.NAME, f"works-{id}-comp_name").send_keys(unswers.cur_work_name[id])
        self.driver.find_element(By.NAME, f"works-{id}-comp_func").send_keys(unswers.works0comp_func[id])
        self.driver.find_element(By.NAME, f"works-{id}-post").send_keys(unswers.works0post[id])
        self.driver.find_element(By.NAME, f"works-{id}-dis_reason").send_keys(unswers.reason0[id])


    def __add_work_click(self):
        target_block = self.driver.find_element(By.ID, "formset-works")
        buttons = target_block.find_elements(By.CLASS_NAME, "button_blue")
        for button in buttons:
            if "добавить" in button.text:
                button.click()

    def fill_page2(self):
        self.__set_element_by_js(By.ID, "id_educations-0-ed_time", unswers.id_educations0_time)
        self.driver.find_element(By.NAME, "educations-0-institution").send_keys(unswers.educations0)
        self.driver.find_element(By.NAME, "educations-0-speciality").send_keys(unswers.speciality)
        self.driver.find_element(By.NAME, "graph").send_keys(unswers.graph)
        self.__sel_drop_menu(By.ID, 'id_educations-0-ed_type', 'очная')
        for i in range(len(unswers.cur_work_time)):
            if i:
                self.__add_work_click()
            self.__fill_work(id=i, cur=True if not i else False)
        self.__fill_recommendation(give=False, reason="Не хочу раскрывать свои намерения")
        self.driver.find_element(By.NAME, "salary_min").send_keys(unswers.salary_min)
        self.driver.find_element(By.NAME, "salary_opt").send_keys(unswers.salary_opt)
        self.driver.find_element(By.NAME, "skills").send_keys(unswers.skills)

    def fill_page3(self):
        self.driver.find_element(By.NAME, "wishes").send_keys(unswers.wishes)
        self.__set_check_box_menu("ms", "0")
        self.__set_check_box_menu("how_about_us_parts", "Совет друзей")
        for i in range(6):
            self.driver.find_element(By.NAME, f"test_question-{i}-ball").send_keys(unswers.q[i])
            self.__submit_page()
        for i in range(5):
            self.driver.find_element(By.NAME, f"test_sentence-{i}-ball").send_keys(unswers.s[i])
        self.driver.find_element(By.ID, "i687").click()

    def __set_check_box_menu(self, name, val):
        all = self.driver.find_elements(By.NAME, name)
        for item in all:
            if item.get_attribute("value") == val:
                item.click()

    def __fill_recommendation(self, give, reason):
        res = self.driver.find_elements(By.NAME, "recommendation_exist")
        if res:
            for item in res:
                val = item.get_attribute("value")
                val = False if val == "False" else True
                if val == give:
                    item.click()
                    if not give:
                        self.driver.find_element(By.NAME, "dis_rec_reas").send_keys(reason)
                    else:
                        pass

    def __submit_page(self):
        self.driver.find_element(By.ID, "submit-resume").click()    

    def send(self):
        self.__submit_page()

    def fill(self):
        self.open()
        self.fill_page1()
        print("fill_page1 is ok")
        self.__submit_page()
        self.fill_page2()
        print("fill_page2 is ok")
        self.__submit_page()
        self.fill_page3()
        print("fill_page3 is ok")

    def result(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except:
            return "Не удалось получить результат"

