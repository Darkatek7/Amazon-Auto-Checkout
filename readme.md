# Amazon Purchase Script 

# Use at your own risk. Read thoroughly

This is a Python script that checks if an item is in stock and under a certain price limit. The script will then purchase the item with limited captcha solving abilities. 

Example: script to buy a PS5 on Amazon

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA (an option is to disable but this will **expose your account to security problems**)
 * **Behavior is dependent on your default shipping address and payment method. Use at your own risk**


Requirements: 
--- 
* Python 3 
* Python modules in `requirements.txt` 
* [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) in same directory 

--- 

## Logic/Behavior: 
 
 1. Starts Selenium 
 2. Loops the following until all attributes of the item are correct: 
    1. Verifies item is in stock 
    2. Verifies the price is less than the set maximum
 4. Logs in 
 5. Adds to cart 
 6. Checks out  


---

## Copy `.env`

```
$ cp .env.sample .env
```


## Run

```
$ pip install -r requirements.txt 
$ python3 main.py
```
