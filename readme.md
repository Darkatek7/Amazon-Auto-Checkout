# Amazon Auto Checkout 

# Use at your own risk. Read thoroughly

This is a Python script that checks if an item is in stock and under a certain price limit. The script will then purchase the item with limited captcha solving abilities. 

Example: script to buy a PS5 on Amazon

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA (an option is to disable but this will **expose your account to security problems**)
 * Make sure you amazon shopping cart is empty
 * **Behavior is dependent on your default shipping address and payment method. Use at your own risk**


Requirements: 
--- 
* Python 3.9 
* Python modules in `requirements.txt` 
* [Google Chrome](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop)
* [WebDriver for the specific Chrome version](https://sites.google.com/chromium.org/driver/downloads?authuser=0) in same directory

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

## Requirements

 * install [Python 3.9](https://www.python.org/downloads/release/python-397/)
 ```
 py -m pip install -r requirements.txt
 ```

---

## Copy `.env`

* rename the ".env.sample" file to ".env" and edit it as you need.

```
cp .env.sample .env
nano .env
```


## Run

```
py main.py
```
