import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import aops_login
import time
from datetime import datetime,timedelta

def parse_rows(all_rows,driver,wait):
    rows = all_rows.find_elements_by_class_name("alc-report-problem-table-row")
    today= datetime.date(datetime.now())
    today -= timedelta(1)
    questions = {"correct":0,"incorrect":0}
    at_bottom = False
    while at_bottom == False:
        all_rows = aops_login.clickable((By.CLASS_NAME,"alc--rows"),wait)
        rows = all_rows.find_elements_by_class_name("alc-report-problem-table-row")
        time_of_question = datetime.strptime(rows[-1].find_element_by_class_name("alc-time").text,"%Y-%m-%d %H:%M:%S")
        if today==datetime.date(time_of_question):
            driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element_by_class_name("aops-loader"))
        else:
            at_bottom = True
    for row in rows:
        time_of_question = datetime.strptime(row.find_element_by_class_name("alc-time").text,"%Y-%m-%d %H:%M:%S")
        if today==datetime.date(time_of_question):
            result = row.find_element_by_class_name("alc-result").text
            if result == "$":
                questions["correct"]+=1
            else:
                questions["incorrect"]+=1
    return questions
            

def get_to_progress(driver,wait):
    time.sleep(1)
    driver.get("https://www.aops.com/alcumus/report/me")
    questions = parse_rows(aops_login.clickable((By.CLASS_NAME,"alc--rows"),wait),driver,wait)
    
    
def main(chromedriver_path,url):
    driver = aops_login.set_up_driver(chromedriver_path)
    driver = aops_login.login(driver,url,get_to_progress)


if __name__ == "__main__":
    main("/Users/shorya/Downloads/chromedriver_81","https://aops.com")