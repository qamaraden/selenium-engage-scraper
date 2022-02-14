from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import requests
import json
import os

def slack_alert(title, colour):

    uri = os.getenv("SLACK_WEBHOOK")
    data = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            }
        ]
    }
    r = requests.post(uri, json.dumps(data)).content
    if r == "b'ok'":
        print("Successfully posted to Slack")

def get_options():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    return chrome_options

driver = webdriver.Chrome(ChromeDriverManager().install(), options=get_options())

# Github credentials
username = os.getenv("username")
password = os.getenv("password")


# head to github login page
driver.get("https://engage.bath.ac.uk/learn/login/index.php")
# find username/email field and send the username itself to the input field
driver.find_element_by_id("username").send_keys(username)
# find password input field and insert password as well
driver.find_element_by_id("password").send_keys(password)
# click login button
driver.find_element_by_name("submit").click()

# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
# get the errors (if there are)
errors = driver.find_elements_by_class_name("flash-error")
# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")
    
driver.implicitly_wait(20)
driver.maximize_window
driver.find_element_by_xpath("/html/body/div[2]/nav/div/button").click()
driver.implicitly_wait(20)
driver.find_element_by_xpath("//span[contains(.,'Software Engineering 1 - November 2021')]").click()
driver.implicitly_wait(20)
driver.find_element_by_xpath("/html/body/div[1]/div[3]/nav[1]/ul/li[4]/a/div/div/span[2]").click()
driver.implicitly_wait(20)
check = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/section[1]/div[1]/table/tbody/tr[3]/td[1]")
# print(check.text)

if (check.text == '-'):
    print("No new results")
else:
    slack_alert(":white_check_mark: Grades are up on Engage", "green")
 
driver.close()
