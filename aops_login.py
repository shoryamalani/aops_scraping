#import chromedriver_binary
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
def set_up_driver(chromedriver_path):
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(chromedriver_path)
    return driver

def get_creds():
    config = configparser.ConfigParser()
    config.read('aops_creds.ini')
    return {"login":config["login_creds"]["login"],"password":config["login_creds"]["password"]}

def clickable(el,wait):
    return wait.until(expected_conditions.element_to_be_clickable(el))

def input_creds(driver,creds,wait):
    clickable((By.ID,"login-username"),wait).send_keys(creds["login"])
    clickable((By.ID,"login-password"),wait).send_keys(creds["password"])
    clickable((By.ID,"login-button"),wait).click()
    
    return driver
    
    
def start_login(driver,url,wait):
    driver.get(url)
    clickable((By.CLASS_NAME,"login-button"),wait).click()
    creds = get_creds()
    driver = input_creds(driver,creds,wait)
    return driver

def login(driver,url,func=None):
    with driver:
        wait = WebDriverWait(driver,10)
        start_login(driver,url,wait)
        if func:
            func(driver,wait)
        return driver
    

def main(chromedriver_path,url):
    driver = set_up_driver(chromedriver_path)
    login(driver,url)

if __name__ == "__main__":
    main("/Users/shorya/Downloads/chromedriver_81","https://aops.com")