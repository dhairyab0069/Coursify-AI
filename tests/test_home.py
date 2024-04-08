from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pytest test_home.py --html=report.html


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

def test_landing_log(browser):
    browser.get(LANDING_URL)
    login_button = browser.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    login_form = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID, "login-form"))
    )

    assert login_form, "Navigated to the Login page successfully, did not navigate to the Login page "

def test_landing_reg(browser):
    browser.get(LANDING_URL)
    reg_button = browser.find_element(By.LINK_TEXT, "Register")
    reg_button.click()

    login_form = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID, "register-form"))
    )

    assert login_form, "Navigated to the Resgistration page successfully, did not navigate to the Registration page"

def test_log(browser):
    browser.get(LOGIN_URL)
    login_button = browser.find_element(By.LINK_TEXT, "Login")
    

    login_form = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID, "login-form"))
    )
    assert login_form, "Navigated to the Login page successfully, did not navigate to the Login page "

    my_email = "vinu.ubc@gmail.com"
    my_password = "yarvp04117"

    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")

    email_input.send_keys(my_email)
    password_input.send_keys(my_password)

    login_button.click()

    form_present = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "head"))
    )
    assert form_present, "Login successful, 'head' element not found"


