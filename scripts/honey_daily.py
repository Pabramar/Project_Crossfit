#!/usr/bin/env python3

import datetime
import json
import logging
import os

import re
import requests
import sys
import yaml
import time


from typing import Tuple
from logging import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from yaml.loader import SafeLoader
from pyfiglet import figlet_format
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

LOGIN_URL="https://dashboard.honeygain.com/login"
RESERVE_URL="https://bemadbox.com/booking/73643/athlete/crossfit_teruel/reservas/"
LOG: Logger

def main():
    """Using selenium and chrome autologin into corssfit webpage and reserve spot at deserved class."""
    global LOG
    LOG = get_logger('INFO')
    today_date_print=str(datetime.date.today())
    LOG.info(f"Execution date: {today_date_print}")
    my_crossfit_email, my_crossfit_password=get_user_data()
    login_web_crossfit(LOGIN_URL, my_crossfit_email, my_crossfit_password, today_date_print)

def get_logger(level) -> Logger:
    """Create a logger"""
    # Create a custom logger
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + '.log')

    c_handler.setLevel(getattr(logging, level))
    f_handler.setLevel(logging.DEBUG)

    # Create formatter and add it to handlers
    c_formatter = logging.Formatter('[%(levelname)s] [%(name)s] %(message)s')
    f_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

    c_handler.setFormatter(c_formatter)
    f_handler.setFormatter(f_formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger

def get_user_data() -> Tuple[str, str]:
    """
    Extract user data for login from yaml file
    """
    with open("Project_Crossfit/scripts/credentials.yaml") as stream:
        try:
            data = yaml.load(stream, Loader=SafeLoader)
            HoneyEmail= data['fb_user']['email']
            HoneyPassword = data['fb_user']['password']
            datos=(HoneyEmail, HoneyPassword)
        except yaml.YAMLError as exc:
            print(exc)
        return datos


def login_web_crossfit(LOGIN_URL,HoneyEmail, HoneyPassword, today_date_print) -> None:
    """
    Used to automatically login into the crossfit webpage, login and reserve a spot in the selected class.
    based on the date of execution and regex provided
    """
    driver = webdriver.Chrome()
    
    _log_in_url(LOGIN_URL, driver, HoneyEmail, HoneyPassword)
    
    time.sleep(2)
    # Get actual address
    driver.get(adress)
    
    with open("xml.log", "w+") as f:
        f.write(driver.page_source)
    with open("xml.log", "r") as file:
        file_lines = file.read()
        
    event_id_value = _webscraping_xml(file_lines)
    try: 
        driver.find_element(By.CSS_SELECTOR, f"li.li{event_id_value} button").click()
        LOG.info(f"Element id found: {event_id_value}, pressed button date: {today_date_print}")
    except Exception as e:
        LOG.error(f"Al pulsar el botón: {e}")
        exit()

    os.remove("xml.log")    
    print(figlet_format("Succesfull", font= "standard"))

def _webscraping_xml() -> str:
    """
    Used to find the button element and it's ID for the selected class.
    """
    regex=[r'<h4>INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*', r'<h4>CROSSFIT\/INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*']
    
            matchRegexOne = re.search(regex, re.MULTILINE)
            if matchRegexOne:
                match2 = matchRegexOne.group(0)
                matchRegexTwo = re.search(r'value="(\d+)"', match2, re.MULTILINE)
                if matchRegexTwo:
                    eventIdValue = matchRegexTwo.group(1)
                    return eventIdValue
                else:
                    LOG.error("Event_id value not found.")
                    os.remove("xml.log")
                    exit()
            else:
                LOG.error("Regex didn't match.")
                os.remove("xml.log")
                exit()
    

def _log_in_url(url, driver, HoneyEmail, HoneyPassword) -> None:
    """
    Used to log in the specified url.
    Will raise an error for status codes other than 200
    """
    try:
        driver.get(url)
        driver.find_element(By.ID, "usr").send_keys(HoneyEmail)
        driver.find_element(By.ID, "pass").send_keys(HoneyPassword)
        driver.find_element(By.CLASS_NAME, "btn").click()
        LOG.info(f"Succesfully logged in: {url}")
    except requests.exceptions.HTTPError as err:
        LOG.error(f"HTTP error occurred: {err} \n Trying to acces url: {url}")
    except Exception as err:
        LOG.error(f"Other error occurred: {err} \n Trying to acces url: {url}")
    else:
        return

if __name__ == "__main__":
    main()