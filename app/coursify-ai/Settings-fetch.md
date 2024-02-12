Fetching Data from the Login_detail database to the Settings page.

Binding of the user information into the settings page happens in the settings rout using Jinja2

@app.route('/settings.html')
@login_required # Ensure that the user is logged in
def settings_html():
user_id = current_user.get_id()
user = users_collection.find_one({"\_id": ObjectId(user_id)})
if user:

        return render_template('settings.html', user=user)
    else:
        flash("User not found.")
        return redirect(url_for('index'))

1. the user ID is fetched from the "current_user" which is from Flask-Login.
2. query is made to the collection on MongoDB using the "user_id"
3. if a user is found, render_template is called which is where Jinja2 is used to render settings.html
4. The 'user' object is passed to the template as a context variable.
5. jinja2 syntax to access the user's properties: {{ user.get('first_name', '') }}

---

client feed back:

- to make the 'change password' function fully functional
- add the difficulty level to the settings.

Password Function

- Have a form in HTML that sends POST requests to the '/change_password' route (FOLLOW THE SAME PATH TO CHANGE ACCOUNT SETTINGS)

  - user enters current, new, confirm password
  - figure out how to fetch the stored password from the database for the current user, it will be hashed.
  - I will have to use the same hashing algo used when storing the original password for the current password entered.
  - check if the hash of the entered current password matches the stored hash.
  - Provide clear error messages for texts that do not match.

- All forms should have the method of submission 'POST' in order to communicate the information chnaged by the user to the form.
- EXAMPLE : form action="{{ url_for('change_password') }}" method="post" || @app.route('/change_password', methods=['POST'])
- This must be done for ALL settings.

Minor changes:

- change the third settings option from "AI assitant" to "preferences" - Add notification settings - Add the difficulty level
- Add an avatar as the default profile picture.

Flask : package in python. web framework, collection of tools and libraries.

1. Give the "save changes" button an action within the form: action="{{ url_for('update_account') }}"
2. Form Submission has to be handled in flask.
3. Flask route:

@app.route('/update_account', methods=['POST])           || @app.ropute() is a decorator that tells flask what URL should trigger the function that is written next. 'POST' requests are for submitting post data
@login_required                                          || only authenticated users can access
def update_account_info();                               || method
first_name = request.form.get('firstname')               || data form the users form is fetched
last_name = request.form.get('lastname')
email = request.form.get('email')

    user_id = current_user.get_id()                                                       || gets the current user's ID

    user = users_collection.find_one({"_id": ObjectId(user_id)})                          || fetches the user's pre-existing data from the DB

    if user:

      updates = {}                                                                        || The changes are held in this empty dictionary
      if user.get('first_name') != first_name:                                            || compares each user data to the data submitted from the form
          updates['first_name'] = first_name                                              || if any changes are found, the changes are added to the empty dictionary

      if user.get('last_name') != last_name:
          updates['last_name'] = last_name

      if user.get('email') != email:
          updates['email'] = email

      if updates:
          users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates})      || update the data in the DB if the updates directory is not empty
          flash('Your account has been updated successfully.')                            || flash sends messages to the user
      else:
          flash('No changes were made to your account.')

    else:

      flash('User not found.')
      return redirect(url_for('settings_html'))

    return redirect (url_for('settings_html'))

4. Changing the email through settings page.

    1. varify if the email is valid
    2. have the user do email carification.

5. Change password



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