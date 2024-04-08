from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pytest test_fpw.py --html=report.html
# pytest test_rpw.py --html=report.html


LANDING_URL = "http://127.0.0.1:5000/"
LOGIN_URL = "http://127.0.0.1:5000/login"


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

# checks if the forgot password link is there
def test_landing_log(browser):
    browser.get(LANDING_URL)
    login_button = browser.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    login_form = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID, "login-form"))
    )
    fpw_link = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID, "fpw"))
    )      

    # assert login_form, "Navigated to the Login page successfully, did not navigate to the Login page "
    assert fpw_link, "Navigated to the Login page successfully, did not navigate to the Login page "

# checks if the forgot password link is there
def test_fpw(browser):
    browser.get(LANDING_URL)
    login_button = browser.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    fpw_button = browser.find_element(By.ID, "fpwlink")
    fpw_button.click()

    # login_form = WebDriverWait(browser,5).until(
    #     EC.presence_of_element_located((By.ID, "login-form"))
    # )
    # fpw_link = WebDriverWait(browser,5).until(
    #     EC.presence_of_element_located((By.ID, "fpw"))
    # )
    fpw_form = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "forgotpw-form"))
    )

    # assert login_form, "Navigated to the Login page successfully, did not navigate to the Login page "
    assert fpw_form, "Navigated to the Forgot password page successfully, did not navigate to the Forgot password page "

#enter the email to reset the password and check the flash message
def test_enter_email(browser):
    browser.get(LANDING_URL)
    login_button = browser.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    fpw_button = browser.find_element(By.ID, "fpwlink")
    fpw_button.click()

    fpw_form = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "forgotpw-form"))
    )

    
    my_email = "vinu.ubc@gmail.com"
    

    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(my_email)

    resetpw_button = browser.find_element(By.ID, "resetpw_btn")
    resetpw_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "An email has been sent with instructions to reset your password." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"
    # assert resetpw_button, "found the reset password button, did not find the reset password button "
