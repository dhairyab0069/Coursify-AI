from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAIN_PAGE_URL = "http://127.0.0.1:5000" 
LOGIN_PAGE_URL = "http://127.0.0.1:5000/login"

# The fixture 'browser' is set to have a 'function' scope, 
# meaning every function requesting the 'browser'
# a new instance of the Chrome browser will be created.
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome() #new instance of chrome
    yield driver 
    driver.quit()

####################################################################
def test_homepage(browser):
    browser.get(MAIN_PAGE_URL)
    chose_login = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
     
    chose_login.click()
     
    try:
        # Adjust the selector to match an element present only when logged in
        email_present = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        # If the above line does not throw an exception, the login is considered successful
        assert email_present, "Found the Login option!"
    except TimeoutException:
        assert False, "Did not find the Login in option"  # For real tests, this could raise an exception or fail the test


####################################################################

def test_login(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "westbrook00"

    login(browser, my_email, my_password)

    try:
        # Adjust the selector to match an element present only when logged in
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "head"))
        )
        # If the above line does not throw an exception, the login is considered successful
        print("Login successful!")  # For real tests, use assert statements instead of print
    except TimeoutException:
        print("Login failed or timed out.")  # For real tests, this could raise an exception or fail the test

######################################################################
            

#Reusable function to perform the login action
def login(browser, email, password):

    browser.get(LOGIN_PAGE_URL) #navigates the browser to the login page
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")

    email_input.send_keys(email)
    password_input.send_keys(password)


    # waiting 10 seconds for the login button to appear.
    # WebDriverWait is a is a class in Selenium that facilitates the implementation of explicit waits.
    # locating and clicking the submit button
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.btn-block"))
        #EC stands for "Expected Conditions." It's a module in Selenium that provides 
        # a set of predefined conditionsto use with WebDriverWait. Presense_of_element_located
        # is one of those predefined conditions
    )

    login_button.click();
    #browser.execute_script("arguments[0].click();", login_button)



    






