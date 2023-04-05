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
import time

from typing import Tuple
from logging import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from yaml.loader import SafeLoader

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from requests.exceptions import HTTPError

LOGIN_URL="https://bemadbox.com/box/beboxin_es"
RESERVE_URL="https://bemadbox.com/booking/73643/athlete/crossfit_teruel/reservas/"
LOG: Logger

def main():
    """Execute main procedure for this script, which will ."""
    # args = get_arguments()
    global LOG
    # LOG = get_logger(args.log_level)
    LOG = get_logger('INFO')
    crossfit_date_url, regex=get_crossfit_web_date()
    myCrossfitEmail, myCrossfitPassword=get_user_data()
    login_web_crosffit(LOGIN_URL, myCrossfitEmail, myCrossfitPassword, crossfit_date_url, regex)
    
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
    today_date=datetime.date.ctime(datetime.date.today()+ datetime.timedelta(days=-2))
    print(today_date) # Here we get the type of day that is

    if re.search("^Mon*", today_date):
        print("It's Monday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=-2))
        regex='<h4>CROSSFIT\/INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*'
        
    elif re.search("^Tue*", today_date):
        print("It's Tuesday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=2))
        regex=r"<h4>INICIACION<\\/h4>\\s*<p>20:15 - 21:15<\\/p>\\s*<input type=\"hidden\" name=\"event_id\" value=\"(\\d*)\""
        
    else: 
        with open("test.log", "a+") as myfile:
            myfile.write("[ERROR] Not executed on monday or tuesday\n")
        sys.exit("[ERROR] Not executed on monday or tuesday\n")
        
    crossfit_date=_convert_format(date_class)
    LOG.info(f"Date used for web url: {crossfit_date}") # D-M-Y for link address
    crossfit_date_url=RESERVE_URL+crossfit_date
    return crossfit_date_url, regex

def _convert_format(s: str):
    y, d, m = s.split("-")
    return "-".join((m, d, y))

def get_user_data() -> Tuple[str, str]:
    with open("Project_Crossfit/scripts/credentials.yaml") as stream:
        try:
            data = yaml.load(stream, Loader=SafeLoader)
            myCrossfitEmail= data['fb_user']['email']
            myCrossfitPassword = data['fb_user']['password']
            datos=(myCrossfitEmail, myCrossfitPassword)
        except yaml.YAMLError as exc:
            print(exc)
        return datos


def login_web_crosffit(LOGIN_URL,myCrossfitEmail, myCrossfitPassword, crossfit_date_url, regex):
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    driver.find_element(By.ID, "usr").send_keys(myCrossfitEmail)
    driver.find_element(By.ID, "pass").send_keys(myCrossfitPassword)
    driver.find_element(By.CLASS_NAME, "btn").click()
    driver.get(crossfit_date_url)
    driver.find_element(By.ID, "usr").send_keys(myCrossfitEmail)
    driver.find_element(By.ID, "pass").send_keys(myCrossfitPassword)
    driver.find_element(By.CLASS_NAME, "btn").click()
    respone=requests.get(crossfit_date_url)
    # Webscrapping -> filter to get id from button Iniciación at 20:15
    time.sleep(5) # Añadido para que cargue toda la página
    driver.get(crossfit_date_url)
    wait = WebDriverWait(driver, 10)
    algo=driver.page_source
    f = open("xml.log","w+")
    f.write(driver.page_source)
    file= open("xml.log", 'r')
    file_lines=file.read()
    algo2=" "+'"'+"'"+algo+"'"+'"'
    webscraping_xml(algo, file_lines,algo2, regex)
    
def reserve_spot_web_crosffit(crossfit_date_url):
    driver = webdriver.Chrome()
    driver.get(crossfit_date_url)
    driver.find_element(By.CLASS_NAME, "btn").click()
    
def webscraping_xml(algo, file_lines, algo2, regex):
    #x = re.search('<h4>CROSSFIT\/INICIACION<\/h4>\\n\s*<p>20:15 - 21:15.*name=\"event_id\" value=\"\d*\"', algo)
    # print(re.search('CROSSFIT\/INICIACION', algo))
    # print(re.search('<h4>CROSSFIT\/INICIACION<\/h4>', algo))
    # print(re.match('<h4>CROSSFIT\/INICIACION<\/h4>', algo))
    
    
    # Posible solución, invocar un script de bash y pasarle un txt y la regex y así ahorrar complejidad con grep
    
    print(type(algo))
    matches = re.finditer(regex, algo, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    
    matches=re.finditer(regex, file_lines, re.MULTILINE)
    print("ESTO??")
    for elemento in matches:
        print(elemento)
    print("AAAAAAAAAAAAAAAAAAAAAAAA")

    print(list(matches))
    matchRegexOne = re.search('<h4>CROSSFIT\/INICIACION<\/h4>\s*<p>20:15 - 21:15<\/p>(\s*.*)*', file_lines, re.MULTILINE)
    if matchRegexOne:
        match2 = match.group(0)
        print(match2)
        matchRegexTwo = re.search(r'value="(\d+)"', match2, re.MULTILINE)
        if matchRegexTwo:
            eventIdValue = matchRegexTwo.group(1)
            print(eventIdValue)
        else:
            print("No se encontró el valor de event_id.")

if __name__ == "__main__":
    main()