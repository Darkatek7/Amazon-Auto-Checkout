import undetected_chromedriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import fake_useragent
from logger import logger as l


def get_driver():
    l.info("getting driver")
    driver = webdriver.Chrome()

    driver.implicitly_wait(3)
    driver.set_page_load_timeout(10)

    return driver


def element_exists(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False


def element_exists_id(id, driver):
    try:
        driver.find_element_by_id(id)
        return True
    except NoSuchElementException:
        return False


def get_subelement(xpath, parent):
    try:
        l = parent.find_element_by_xpath(xpath)
        return l
    except NoSuchElementException:
        return ""


def wait_for_element_to_be_clickable(name, xpath, driver):
    l.info("clicking element: " + name)
    try:
        WebDriverWait(driver, 3) \
            .until(ec.element_to_be_clickable((By.XPATH, xpath))).click()
        return True
    except TimeoutException:
        return False
