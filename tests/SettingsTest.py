from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# RUN THIS COMMAND TO GET A REPORT
# pytest SettingsTest.py --html=report.html

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

# CASE 1 : NAVIGATE TO THE SETTINGS PAGE #==========================================================
#===================================================================================================

# initial email    : vinu.ubc@gmail.com
# initial password : yarvp04117

## navigates to log in page and logs in, clicks the settings page, checks for the account settings form.
def test_navigate_to_settings(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "yarvp04117"

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

# CASE 2 : CHANGE ACCOUNT  FIRST NAME #=============================================================
#===================================================================================================
# clicks firstname
# 
def test_change_first_name(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "yarvp04117"

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

    firstname_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "firstname"))
    )

    firstname_field.clear()
    firstname_field.send_keys("vinu-test-test")                                                                                                           # CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your account has been updated successfully" 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 3 : CHANGE ACCOUNT LAST NAME #===============================================================
#===================================================================================================
def test_change_last_name(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "yarvp04117"

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

    lastname_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "lastname"))
    )

    lastname_field.clear()
    lastname_field.send_keys("last-test-test")                                                                                                          #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your account has been updated successfully" 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 4 : CHANGE ACCOUNT EMAIL #===================================================================
#===================================================================================================
def test_change_email(browser):
    my_email = "vinu.ubc@gmail.com"
    my_password = "yarvp04117"

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

    email_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "email"))
    )

    email_field.clear()
    email_field.send_keys("ubcubc@gmail.com")                                                                                                          #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your account has been updated successfully" 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 5 : (SHOULD FAIL) CHANGE ACCOUNT DETAILS #===================================================
#===================================================================================================
#CHANGE EMAIL###########################################
def test_shouldFAIL_account_settings(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                          # CHANGE
    my_password = "yarvp04117"

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

    lastname_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "lastname"))
    )

    lastname_field.clear()
    lastname_field.send_keys("last-test-test")                                                                                                          #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your account has been updated successfully" 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 6 : CHANGE PASSWORD #========================================================================
#===================================================================================================
def test_change_password(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "yarvp04117"

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
    
    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    password_form_displayed = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "password-settings-form"))  # Adjust the ID based on your actual HTML
    )
    assert password_form_displayed, "Password form was not displayed after clicking the Password section"
    #
    current_password_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "current-password"))
    )
    current_password_field.clear()  # Clear any pre-filled text
    current_password_field.send_keys("yarvp04117")  # Replace with the actual current password
    #
    new_password_field = browser.find_element(By.ID, "new-password")
    new_password_field.clear()  # It's good practice to clear the field before entering text
    new_password_field.send_keys("1234")  # Replace with the desired new password
    #
    confirm_new_password_field = browser.find_element(By.ID, "confirm-new-password")
    confirm_new_password_field.clear()  # Clear any pre-filled text
    confirm_new_password_field.send_keys("1234")  # Repeat the new password
                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 7 : (SHOULD FAIL) CURRENT PASSWORD DOES NOT MATCH #==========================================
#===================================================================================================
def test_shouldFAIL_CURRENT_password_nomatch(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "1234"

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

    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    currentPW_field = browser.find_element(By.ID, "current-password")
    newPW_field = browser.find_element(By.ID, "new-password")
    confirmNewPW_field = browser.find_element(By.ID, "confirm-new-password")
    

    currentPW_field.send_keys("12345")
    newPW_field.send_keys("1234")      
    confirmNewPW_field.send_keys("1234")                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"

# CASE 8 : (SHOULD FAIL) NEW PASSWORD DO NOTH MATCH #===============================================
#===================================================================================================
def test_shouldFAIL_new_password_nomatch(browser):
    my_email = "ubcubc@gmail.com"                                                                                                                       # CHANGE
    my_password = "1234"

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

    password_link = WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.ID, "password-settings-link"))
    )
    password_link.click()

    currentPW_field = browser.find_element(By.ID, "current-password")
    newPW_field = browser.find_element(By.ID, "new-password")
    confirmNewPW_field = browser.find_element(By.ID, "confirm-new-password")
    

    currentPW_field.send_keys("1234")
    newPW_field.send_keys("123")      
    confirmNewPW_field.send_keys("1234")                                                                                                        #CHANGE

    save_changes_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_changes_button.click()

    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))  #finds the flash ID and compared the messages after
    )

    expected_message = "Your password has been updated successfully." 
    actual_message = flash_message.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in flash message: '{actual_message}'"




