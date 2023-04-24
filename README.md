# CrossFit Class Reservation Script

This script uses Selenium to automate the login and class reservation process on a CrossFit gym website.

## Requirements
To run this script, you need to have the following software installed:

* Python 3.x
* Selenium
* ChromeDriver

You can install Selenium and other required packages with pip:

pip install selenium

You can download ChromeDriver from the following link:
https://chromedriver.chromium.org/downloads

Make sure to download the version that matches your Chrome browser version.

## Usage
Before running the script, you need to fill in the necessary information in the credentials.yaml file. This includes your login credentials.

Once you have filled in the configuration file, you can run the script with the following command:

python reserve_class.py
The script will then open a Chrome browser, navigate to the gym's website, log in with your credentials, and reserve the class you specified in the configuration file.

## Disclaimer
This script is for educational purposes only. Use it at your own risk. The author is not responsible for any misuse of this script.