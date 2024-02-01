from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# RUN THIS COMMAND TO GET A REPORT
# pytest test_file.py --html=report.html

LOGIN_URL = "http://127.0.0.1:5000/login"

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome() #new instance of chrome
    yield driver 
    driver.quit()

# REUSABLE LOG-IN FUNCTION ###################################################################
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

# NAVIGATE TO THE SETTINGS PAGE ################################################################### 

def login_and_navigate_to_settings(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "westbrook00"

    login(browser, my_email, my_password)

    head_present = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "head"))
    )
    #can also use EC.text_to_be_present_in_element_located    
    
    assert head_present, "Login successful, 'head' element not found"  

    settings_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "settings"))
    )
    settings_link.click()

    uElement = WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID, "account-settings-form"))
    )

    assert uElement, "Navigated to the Settings page successfully, did not navigate to the settings page "
     
######################################################################

#HOMEPAGE_URL = "http://127.0.0.1:5000" put this at the top if needed

#   Logging through the homepage.html
#def test_homepage(browser):
#    browser.get(MAIN_PAGE_URL)
#    chose_login = WebDriverWait(browser,10).until(
#        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
#    )
     
#    chose_login.click()
     
#    try:
        # Adjust the selector to match an element present only when logged in
#        email_present = WebDriverWait(browser, 10).until(
#            EC.presence_of_element_located((By.ID, "email"))
#        )
        # If the above line does not throw an exception, the login is considered successful
#        assert email_present, "Found the Login option!"
#    except TimeoutException:
#        assert False, "Did not find the Login in option"  # For real tests, this could raise an exception or fail the test

#Reusable function to perform the login action
    






