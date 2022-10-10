from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from anketa.job_profile import Profile
from platform import platform


def setup_driver_windows():
    chrome_bin_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_driver_path = "chromedriver.exe"
    options = Options()
    options.binary_location = chrome_bin_path
    options.add_argument("--window-size=375,667")
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
    return driver


def setup_driver_unix():
    options = Options()
    options.add_argument("--window-size=375,667")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--disable-gpu")
    chromdriver = "/media/private/telegramBot/utils/chromedriver"
    driver = webdriver.Chrome(executable_path=chromdriver, chrome_options=options)
    return driver


def send_my_profile_for(job_name):
    driver = setup_driver_windows if "Win" in platform() else setup_driver_unix
    profile = Profile(job_name, driver())
    profile.fill()
    profile.send()
    return profile.result()


if __name__ == "__main__":
    name = "Инженер - программист отдела разработки и технического оснащения"
    send_my_profile_for(name)
