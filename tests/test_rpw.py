from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pytest test_fpw.py --html=report.html


LANDING_URL = "http://127.0.0.1:5000/"
LOGIN_URL = "http://127.0.0.1:5000/login"
RPW_URL = "http://127.0.0.1:5000/reset_forgot_password/InZpbnUudWJjQGdtYWlsLmNvbSI.ZgowyQ.aTXYIovB6AHkV7uz7hPRizDPX6g" #link from email


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome() #new instance of chrome
    yield driver 
    driver.quit()

# REUSABLE LOG-IN FUNCTION #========================================================================
def login(browser, email, password): 
    browser.get(LOGIN_URL) #navigate to login.html and skip homepage.html
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")

    email_input.send_keys(email)
    password_input.send_keys(password)

    #wait 10 seconds
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.btn-block"))
    )

    login_button.click();

def test_reset_password_page(browser):
    browser.get(RPW_URL)
    #id is new_password
    new_password = "Yasdasd123$" 

    new_password_input = browser.find_element(By.ID, "new_password")
    new_password_input.send_keys(new_password)
    
    confirm_new_password_input = browser.find_element(By.ID, "confirm_new_password")
    confirm_new_password_input.send_keys(new_password)

    resetpw_button = browser.find_element(By.ID, "respw_btn")
    resetpw_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    # the user is redirected to the login page here

    expected_message = "Your password has been reset successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"



