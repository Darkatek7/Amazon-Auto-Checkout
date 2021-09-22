from selenium import webdriver
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


def open_url(url, driver):
    l.info("opening: " + url)
    driver.get(url)

def close_driver(driver):
    l.info("closing driver")
    driver.close()
    driver.quit()

def click_element(name, xpath, driver): # xpath of element to click
    l.info("clicking element: " + name)
    try:
        ActionChains(driver).move_to_element(driver.find_element_by_xpath(xpath)).click().perform()
        return True
    except NoSuchElementException:
        return False

def get_driver():
    l.info("getting driver")
    options = Options()
    options.add_argument("--log-level=3") # disable selenium logs
    options.add_argument("--lang=en-AT")
    options.add_argument('--disable-translate')
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--disable-xss-auditor")
    options.add_argument("--disable-web-security")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    prefs = {"enable_do_not_track": True}
    options.add_experimental_option("prefs", prefs)

    try:
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
    except fake_useragent.FakeUserAgentError:
        pass

    driver = webdriver.Chrome('chromedriver', options=options)

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

def element_is_enabled(xpath, driver):
    try:
        l = driver.find_element_by_xpath(xpath)

        if l.is_enabled():
            return True
        else:
            return False
    except NoSuchElementException:
        return False

def get_parent_of_element(xpath, driver):
    try:
        l = driver.find_element_by_xpath(xpath)
        parent = l.find_element_by_xpath("..")
        return parent
    except NoSuchElementException:
        return ""

def get_subelement(xpath, parent):
    try:
        l = parent.find_element_by_xpath(xpath)
        return l
    except NoSuchElementException:
        return ""

def wait_for_element_to_be_clickable(name, xpath, driver):
    l.info("clicking element: " + name)
    try:
        WebDriverWait(driver, 3)\
            .until(ec.element_to_be_clickable((By.XPATH, xpath))).click()
        return True
    except TimeoutException:
        return False

def element_is_displayed(xpath, driver):
    return driver.find_element_by_xpath(xpath).is_displayed()
