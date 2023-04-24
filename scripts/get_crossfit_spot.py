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

LOGIN_URL="https://bemadbox.com/box/beboxin_es"
RESERVE_URL="https://bemadbox.com/booking/73643/athlete/crossfit_teruel/reservas/"
LOG: Logger

def main():
    """Using selenium and chrome autologin into corssfit webpage and reserve spot at deserved class."""
    global LOG
    LOG = get_logger('INFO')
    crossfit_date_url=get_crossfit_reserve_day()
    my_crossfit_email, my_crossfit_password=get_user_data()
    login_web_crossfit(LOGIN_URL, my_crossfit_email, my_crossfit_password, crossfit_date_url)

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

def get_crossfit_reserve_day() -> str:
    """
    Used to get the date which will be used for the url reserve day.

    Returns:
        * `str`: date of the crossfit class on D-M-Y format.
        * `str`: Regex.
    """
    today_date=datetime.date.ctime(datetime.date.today()+ datetime.timedelta(days=1))
    today_date_print=_convert_format_date(str(datetime.date.today() + datetime.timedelta(days=1)))

    if re.search("^Mon*", today_date):
        LOG.info(f"It's Monday {today_date_print}")
        date_class=str(datetime.date.today() + datetime.timedelta(days=2))

    elif re.search("^Tue*", today_date):
        LOG.info(f"It's Tuesday {today_date_print}")
        date_class=str(datetime.date.today() + datetime.timedelta(days=2))

    else: 
        with open("test.log", "a+") as myfile:
            LOG.error(f"Not executed on monday or tuesday: {today_date_print}")
        exit()
    
    crossfit_date=_convert_format_date(date_class)
    LOG.info(f"Date used for url reserve: {crossfit_date}")
    crossfit_date_url=RESERVE_URL+crossfit_date
    return crossfit_date_url

def _convert_format_date(s: str) -> str:
    y, d, m = s.split("-")
    return "-".join((m, d, y))

def get_user_data() -> Tuple[str, str]:
    """
    Extract user data for login from yaml file
    """
    with open("Project_Crossfit/scripts/credentials.yaml") as stream:
        try:
            data = yaml.load(stream, Loader=SafeLoader)
            myCrossfitEmail= data['fb_user']['email']
            myCrossfitPassword = data['fb_user']['password']
            datos=(myCrossfitEmail, myCrossfitPassword)
        except yaml.YAMLError as exc:
            print(exc)
        return datos


def login_web_crossfit(LOGIN_URL,myCrossfitEmail, myCrossfitPassword, crossfit_date_url) -> None:
    """
    Used to automatically login into the crossfit webpage, login and reserve a spot in the selected class.
    based on the date of execution and regex provided
    """
    driver = webdriver.Chrome()
    
    _log_in_url(LOGIN_URL, driver, myCrossfitEmail, myCrossfitPassword)
    _log_in_url(crossfit_date_url, driver, myCrossfitEmail, myCrossfitPassword)
    
    time.sleep(2)
    driver.get(crossfit_date_url)
    
    with open("xml.log", "w+") as f:
        f.write(driver.page_source)
    with open("xml.log", "r") as file:
        file_lines = file.read()
        
    event_id_value = _webscraping_xml(file_lines)
    try: 
        driver.find_element(By.CSS_SELECTOR, f"li.li{event_id_value} button").click()
    except Exception as e:
        LOG.error(f"Al pulsar el botón: {e}")
        exit()

    os.remove("xml.log")    
    print(figlet_format("Succesfull", font= "standard"))

def _webscraping_xml(file_lines) -> str:
    """
    Used to find the button element and it's ID for the selected class.
    """
    regex_list=[r'<h4>INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*', r'<h4>CROSSFIT\/INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*']
    
    for regex in regex_list:
        matchRegexOne = re.search(regex, file_lines, re.MULTILINE)
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
    

def _log_in_url(url, driver, myCrossfitEmail, myCrossfitPassword) -> None:
    """
    Used to log in the specified url.
    Will raise an error for status codes other than 200
    """
    try:
        driver.get(url)
        driver.find_element(By.ID, "usr").send_keys(myCrossfitEmail)
        driver.find_element(By.ID, "pass").send_keys(myCrossfitPassword)
        driver.find_element(By.CLASS_NAME, "btn").click()
    except requests.exceptions.HTTPError as err:
        LOG.error(f"HTTP error occurred: {err} \n Trying to acces url: {url}")
    except Exception as err:
        LOG.error(f"Other error occurred: {err} \n Trying to acces url: {url}")
    else:
        return

if __name__ == "__main__":
    main()