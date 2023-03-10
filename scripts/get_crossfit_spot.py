#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import os
import re
import requests
import sys
import yaml

from typing import Tuple
from logging import Logger
from selenium import webdriver
from yaml.loader import SafeLoader
# from requests.exceptions import HTTPError

LOGIN_URL="https://bemadbox.com/booking/beboxin_es"
RESERVE_URL="https://bemadbox.com/booking/73643/athlete/crossfit_teruel/reservas/"
LOG: Logger

def main():
    """Execute main procedure for this script, which will ."""
    # args = get_arguments()
    # global LOG
    # LOG = get_logger(args.log_level)

def get_arguments():
    """
    Gets an argument given script inputs
    returns: parser.parse_args()
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description='Get user data and log level')
    parser.add_argument('-u', '--username', type=str, help='User', required=True)
    parser.add_argument('-p', '--password', type=str, help='Password', required=True)
    parser.add_argument('-l', '--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Logging level. Default: INFO')

    return parser.parse_args()

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

def func1() -> Tuple[list, list]:
    """
    Use  to get .

    Arguments:
        * `args`: Diff args

    Returns:
        * `list`: List of 
        * `list`: List of 
    """

    
    LOG.debug(f": {len()}")

    # Get all_plans from all_projects
    algo = []
    for alg in algo:
        try:
            request = requests.get(url_api_commits, auth=(args.username, args.password), headers=HEADERS_AUTH)
            ## HEADERS_AUTH = {'Content-Type': 'application/json'} si no tiene API no usar
        except requests.request.exceptions.HTTPError as e:
            response_json = json.loads(e.response.content)
            if e.response.status_code == 404:
                LOG.error(f"Failed  , http response code: {e.response.status_code}, message: {response_json['message']}")
            else:
                LOG.error(f"Failed  , http response code: {e.response.status_code}, message: {response_json['message']}")

# Function to check if antiquity major of 3 months (90 days) # Optional parameter months default 3 months
def _is_greater_than_months(built_plan_date: str, months: int = 3) -> bool:
    """
    Used to compare if the date is older than 3 months.

    Arguments:
        * `built_plan_date `: Date of 
        * `months`: Number of months to compare. Default: 3

    Returns:
        * `bool`: True if the date is older than the months specified
    """
    dt_now = datetime.now()
    
    # Cambio de formato de la fecha obtenida de en ISO 8601
    dt_ = datetime(*map(int, re.split(r'[^\d]', built_plan_date)[:-1]))
    return (dt_now - dt_).days > months * 30

if __name__ == "__main__":
    main()
    
'''
As webpage doesn't have API will probably use



pip install html-to-json



import requests
import json
import html_to_json

username = 'vgtgayan'
base_url = 'https://www.kaggle.com/'
url = base_url+str(username)

r = requests.get(url)
print(r.status_code)

html_string = r.text
output_json = html_to_json.convert(html_string)
print(output_json)



'''

def get_crossfit_web_date() -> str:
    """
    Used to get the date which will be used for the url.

    Returns:
        * `str`: Contains date of the crossfit class on D-M-Y format.
    """
    today_date=datetime.date.ctime(datetime.date.today())
    print(today_date) # Here we get the type of day that is

    if re.search("^Mon*", today_date):
        print("It's Monday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=1))
        
    elif re.search("^Tue*", today_date):
        print("It's Tuesday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=2))
        
    else: 
        with open("test.log", "a+") as myfile:
            myfile.write("[ERROR] Not executed on monday or tuesday\n")
        sys.exit("[ERROR] Not executed on monday or tuesday\n")
        
    crossfit_date_web=_convert_format(date_class)
    LOG.info(f"Date used for web url:{crossfit_date_web}") # D-M-Y for link address
    return crossfit_date_web

def _convert_format(s: str):
    y, d, m = s.split("-")
    return "-".join((m, d, y))


with open("Project_Crossfit/scripts/credentials.yaml") as stream:
    try:
        data = yaml.load(stream, Loader=SafeLoader)
        myCrossfitEmail= data['fb_user']['email']
        myCrossfitPassword = data['fb_user']['password']
        
    except yaml.YAMLError as exc:
        print(exc)
