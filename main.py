import functions
import browser
import os
import sys
from logger import logger as l

def call_login(driver):
    try:
        functions.login(driver)
    except Exception as e:
        l.error('Error Could not login: {}'.format(e))
        driver.quit()
        driver = browser.get_driver()
        call_login(driver)
    finally:
        return driver

def run_checkout(driver):
    functions.check_item_stock(driver)
    functions.add_to_cart(driver)
    functions.place_order(driver)


if __name__ == '__main__':
    driver = browser.get_driver()
    driver = call_login(driver)

    try:
        done = False
        while(not done):
            try:
                run_checkout(driver)
                done = True
            except KeyboardInterrupt:
                done = True
            except BaseException:
                pass
    except Exception as e:
        l.error('{}'.format(e))
    finally:
        l.info('Closing Chromium')
        try:
            driver.close()
        except BaseException:
            pass
        l.info('Closed Chromium')

    l.info('ALL DONE')