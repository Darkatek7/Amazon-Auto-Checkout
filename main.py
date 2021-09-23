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
    functions.add_to_cart(driver)
    functions.place_order(driver)

if __name__ == '__main__':
    driver = browser.get_driver()
    driver = call_login(driver)

    try:
        done = False
        while(not done):
            try:
                in_stock = functions.check_item_stock(driver)

                if in_stock:
                    driver.quit()
                    driver = browser.get_driver()
                    driver = call_login(driver)
                    raise Exception("Renewed user agent")

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