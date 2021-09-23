import os
import sys
import time
import browser
from random import randint
from dotenv import load_dotenv
from logger import logger as l
from amazoncaptcha import AmazonCaptcha
from selenium.common.exceptions import NoSuchElementException

load_dotenv(verbose=True)
dotenv_path = '.env'
load_dotenv(dotenv_path)

MAIL = os.environ.get('MAIL', None)
PASSWORD = os.environ.get('PASSWORD', None)
ITEM_URL = os.environ.get('ITEM_URL', None)
CART_URL = os.environ.get('CART_URL', None)
MAX_PRICE = float(os.environ.get('MAX_PRICE', None))
SHOP_URL = os.environ.get('SHOP_URL', None)
MIN_DELAY = float(os.environ.get('MIN_DELAY', None))
MAX_DELAY = float(os.environ.get('MAX_DELAY', None))
# RUNS_BEFORE_AGENT_SWITCH = int(os.environ.get('RUNS_BEFORE_AGENT_SWITCH', None)) 


# is beeing called for logging you in to Amazon
def login(driver):
    l.info('Attempting to sign-in')
    driver.get(SHOP_URL)

    if(browser.element_exists_id('captchacharacters', driver) or browser.element_exists_id('image-captcha-section', driver)):
        validate_captcha(driver)
        driver.get(SHOP_URL)

    driver.find_element_by_id("nav-link-accountList").click()
    driver.find_element_by_id('ap_email').send_keys(MAIL)
    driver.find_element_by_id('continue').click()
    driver.find_element_by_id('ap_password').send_keys(PASSWORD)
    driver.find_element_by_id('signInSubmit').click()
    l.info('Successfully signed-in as: {}'.format(driver.find_element_by_id("nav-link-accountList").text.split(' ')[1].split('\n')[0]))

# keeps refreshing until Item is in Stock, seller is your seller and its price is lower then your max price
def check_item_stock(driver):
    l.info("Refreshing page")
    outOfStock = True
    driver.get(ITEM_URL)
    l.info("Finished refreshing page")
    while(outOfStock):
        try:
            l.info("Checking item stock")
            driver.find_element_by_id("outOfStock")
            l.warn("Item is outOfStock")
            time.sleep(randint(MIN_DELAY, MAX_DELAY))
            driver.refresh()
        except NoSuchElementException as e:
            try:
                l.info("Item is in-stock!")
                if verify_price_within_limit(driver):
                    outOfStock = False
                time.sleep(randint(MIN_DELAY, MAX_DELAY))
                driver.refresh()
                continue
            except NoSuchElementException as e:
                time.sleep(randint(MIN_DELAY, MAX_DELAY))
                driver.refresh()
                continue
            
    return

# solve amazon captcha
def validate_captcha(driver):
    time.sleep(1)
    l.info("Solving CAPTCHA")
    captcha = AmazonCaptcha.fromdriver(driver)
    solution = captcha.solve()
    driver.find_element_by_id('captchacharacters').send_keys(solution)
    time.sleep(1)
    driver.find_element_by_class_name('a-button-text').click()
    time.sleep(1)

#checks if the item price is in your price range
def verify_price_within_limit(driver):
    try:
        price = driver.find_element_by_id('priceblock_ourprice').text
    except Exception:
        l.error('Error verifying price: No Price shown')
        return False

    l.info(f'price of item is:  {price}')
    l.info('limit value is: {}'.format(MAX_PRICE))

    price = get_clean_price(price)

    if price >= MAX_PRICE: #replace price characters to look like this (eg. 1420.99) (no money symbol, no thousands seperator and '.' as a Cent seperator)
        l.warn('Too Expensive.')
        return False

    l.info('Price is in range')
    return True

#gets clean price value to compare with max price value
def get_clean_price(price):
    l.info(f"getting clean price: {price}")
    price = price.replace('', '')
    if '$' in price:
        price = price.replace('$', '')
    if '€' in price:
        price = price.replace('€', '')

    price = price[ : -3] 

    numeric_filter = filter(str.isdigit, price)
    price = "".join(numeric_filter)
    
    l.info(f"clean price: {price}")
    return float(price)

# adds the item to our cart
def add_to_cart(driver):
    l.info("Attempting to add to cart")
    try:
        driver.find_element_by_id("add-to-cart-button").click()
        browser.wait_for_element_to_be_clickable("no warranty", "//input[@aria-labelledby='attachSiNoCoverage-announce']", driver)
    except:
        try:
            # sometimes, amazon has a box called "Other Sellers on Amazon"
            # underneath the regular buy-box. This will select the first
            # option if it's available
            driver.find_element_by_id("mbc-buybutton-addtocart-1").click()
        except BaseException:
            try:
                l.info('Checking if See-all-buying-choices loop')
                driver.find_element_by_id(
                    "buybox-see-all-buying-choices").click()
                l.info("See-all-buying-choices loop")
            except BaseException:
                try:
                    # check if amazon wants us to sub
                    l.info("Check if subscription is offered")
                    driver.find_element_by_id("newAccordionRow").click()
                    l.info("Selected one time purchase")
                except BaseException:
                    l.info("No subscription offered")
                    pass

                # not under except clause here because
                # add-to-cart-button can be on either a standard
                # page, or after "one time purchase" is selected
                try:
                    driver.find_element_by_id("add-to-cart-button").click()
                except:
                    raise Exception("Failed to add to cart")

    l.info("Successfully added to cart")

def place_order(driver):
    #Purchases the item using default settings
    l.info("Proceeding to checkout")
    try:
        driver.find_element_by_id("sc-buy-box-ptc-button").click()
        l.info("Placing the order")
        count = 0
        while( count != 3 ):
            try:
                driver.find_element_by_id("submitOrderButtonId").click()
                l.success("Successfully placed order!")
                return
            except BaseException as err:
                count += 1
                l.error("Failed to place order: {}".format(err))
                l.info("Retrying {}".format(count))
        l.info("Page Source: {}".format(driver.page_source))
        raise Exception("Failed to find submit order button")

    except BaseException as err:
        l.error("Failed to proceed to checkout: {}".format(err))
    
    raise Exception("Failed to complete checkout")