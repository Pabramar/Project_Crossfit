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
    Honey_email, Honey_password=get_user_data()
    login_web(LOGIN_URL, Honey_email, Honey_password, today_date_print)

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
    with open("scripts/credentials_honey.yaml") as stream:
        try:
            data = yaml.load(stream, Loader=SafeLoader)
            Honey_email= data['honey_user']['email']
            Honey_password = data['honey_user']['password']
            datos=(Honey_email, Honey_password)
        except yaml.YAMLError as exc:
            print(exc)
        return datos


def login_web(LOGIN_URL,Honey_email, Honey_password, today_date_print) -> None:
    """
    Used to automatically login into the crossfit webpage, login and reserve a spot in the selected class.
    based on the date of execution and regex provided
    """
    driver = webdriver.Chrome()

    _log_in_url(LOGIN_URL, driver, Honey_email, Honey_password)

    # Get actual address
    current_url = driver.current_url
    while current_url == LOGIN_URL:
        _log_in_url(LOGIN_URL, driver, Honey_email, Honey_password)
    LOG.info(f"Actual url: {current_url}")
    driver.get(current_url)
         
    try: 
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button.sc-gWHAAX.jwDkLI").click()
        LOG.info(f"Lucky Pot claimed.")
    except Exception as e:
        LOG.error(f"Al pulsar el botón: {e}")
        exit()
        
    print(figlet_format("Succesfull", font= "standard"))

def _log_in_url(LOGIN_URL, driver, Honey_email, Honey_password) -> None:
    """
    Used to log in the specified url.
    Will raise an error for status codes other than 200
    """
    try:
        driver.get(LOGIN_URL)
        driver.find_element(By.CSS_SELECTOR, "button.sc-gWHAAX.dnroEd").click()
        driver.find_element(By.ID, "email").send_keys(Honey_email)
        driver.find_element(By.ID, "password").send_keys(Honey_password)
        driver.find_element(By.CSS_SELECTOR, "button.sc-gWHAAX.bqmTxx").click()
        LOG.info(f"Succesfully logged in: {LOGIN_URL}")
    except requests.exceptions.HTTPError as err:
        LOG.error(f"HTTP error occurred: {err} \n Trying to acces url: {LOGIN_URL}")
    except Exception as err:
        LOG.error(f"Other error occurred: {err} \n Trying to acces url: {LOGIN_URL}")
    else:
        return

if __name__ == "__main__":
    main()