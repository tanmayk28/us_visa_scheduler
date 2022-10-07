import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from consts import LOCAL_USE, HUB_ADDRESS, STEP_TIME, COUNTRY_CODE, USERNAME, PASSWORD, REGEX_CONTINUE


def get_driver():
    if LOCAL_USE:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        driver = webdriver.Remote(command_executor=HUB_ADDRESS, options=webdriver.ChromeOptions())
    return driver


class LoginCtl(object):
    driver = get_driver()

    @classmethod
    def login(cls):
        # Bypass reCAPTCHA
        cls.driver.get(f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv")
        time.sleep(STEP_TIME)
        a = cls.driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
        a.click()
        time.sleep(STEP_TIME)

        print("Login start...")
        href = cls.driver.find_element(By.XPATH, '//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
        href.click()
        time.sleep(STEP_TIME)
        Wait(cls.driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))

        print("\tclick bounce")
        a = cls.driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
        a.click()
        time.sleep(STEP_TIME)

        last_yatry_cookie = cls.do_login_action()
        return last_yatry_cookie

    @classmethod
    def do_login_action(cls):
        print("\tinput email")
        user = cls.driver.find_element(By.ID, 'user_email')
        user.send_keys(USERNAME)
        time.sleep(random.randint(1, 3))

        print("\tinput pwd")
        pw = cls.driver.find_element(By.ID, 'user_password')
        pw.send_keys(PASSWORD)
        time.sleep(random.randint(1, 3))

        print("\tclick privacy")
        box = cls.driver.find_element(By.CLASS_NAME, 'icheckbox')
        box .click()
        time.sleep(random.randint(1, 3))

        print("\tcommit")
        btn = cls.driver.find_element(By.NAME, 'commit')
        btn.click()
        time.sleep(random.randint(1, 3))

        Wait(cls.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, REGEX_CONTINUE)))
        print("\tlogin successful!")

        return "_yatri_session=" + cls.driver.get_cookie("_yatri_session")["value"]
