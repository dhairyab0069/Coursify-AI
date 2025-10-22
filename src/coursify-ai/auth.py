"""
Authentication routes: Login, Registration, Password Reset
No email verification required
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from bson.objectid import ObjectId
from itsdangerous import SignatureExpired, BadSignature

from extensions import bcrypt, serializer
import extensions
from models import User
from utils import validate_password


# ============================================================================
# REGISTRATION - No Email Verification
# ============================================================================

def register():
    """Register a new user"""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        birth_day = int(request.form.get('birth_day'))
        birth_month = int(request.form.get('birth_month'))
        birth_year = int(request.form.get('birth_year'))

        # Check if user already exists
        user = extensions.users_collection.find_one({"email": email})
        if user:
            flash('Email already exists. Please login or use a different email.', 'danger')
            return redirect(url_for('register'))

        # Validate password
        password_error = validate_password(password)
        if password_error:
            flash(password_error, 'danger')
            return redirect(url_for('register'))

        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        birth_date = datetime(birth_year, birth_month, birth_day)

        extensions.users_collection.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
            "birth_date": birth_date,
            "verified": True,  # Auto-verified (no email needed)
            "created_at": datetime.utcnow()
        })

        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ============================================================================
# LOGIN
# ============================================================================

def login():
    """Login a user"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = extensions.users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user_id=str(user["_id"]), email=email)
            login_user(user_obj, remember='remember' in request.form)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')


# ============================================================================
# LOGOUT
# ============================================================================

def logout():
    """Logout current user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ============================================================================
# PASSWORD RESET - Uses Birthdate Verification (No Email)
# ============================================================================

def forgot_password():
    """Forgot password - verify identity with birthdate"""
    if request.method == 'POST':
        email = request.form.get('email')
        birth_day = request.form.get('birth_day')
        birth_month = request.form.get('birth_month')
        birth_year = request.form.get('birth_year')

        user = extensions.users_collection.find_one({"email": email})

        if user:
            # Verify identity using birthdate
            user_birthdate = user.get('birth_date')
            input_birthdate = datetime(int(birth_year), int(birth_month), int(birth_day))

            if user_birthdate.date() == input_birthdate.date():
                # Identity verified, create reset token
                token = serializer.dumps(email, salt='password-reset-salt')
                reset_url = url_for('reset_password', token=token, _external=True)

                flash('Identity verified! You can now reset your password.', 'success')
                return redirect(reset_url)
            else:
                flash('Birth date does not match our records.', 'danger')
        else:
            flash('No account found with that email address.', 'danger')

    return render_template('forgot_password.html')


def reset_password(token):
    """Reset password after identity verification"""
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('The password reset link has expired or is invalid.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if new_password != confirm_new_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('reset_password', token=token))

        password_error = validate_password(new_password)
        if password_error:
            flash(password_error, 'danger')
            return redirect(url_for('reset_password', token=token))

        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        extensions.users_collection.update_one({"email": email}, {"$set": {"password": hashed_new_password}})

        flash('Your password has been reset successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)


# ============================================================================
# SETTINGS - Update Account
# ============================================================================

@login_required
def update_account_settings():
    """Update user account settings"""
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    email = request.form.get('email')

    user_id = current_user.get_id()
    user = extensions.users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        updates = {}
        if user.get('first_name') != first_name:
            updates['first_name'] = first_name
        if user.get('last_name') != last_name:
            updates['last_name'] = last_name
        if user.get('email') != email:
            updates['email'] = email

        if updates:
            extensions.users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
            flash('Your account has been updated successfully', 'success')
        else:
            flash('No changes were made to your account.', 'info')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('settings'))


@login_required
def change_password():
    """Change user password"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')

    user_id = current_user.get_id()
    user = extensions.users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return redirect(url_for('settings'))

    if not bcrypt.check_password_hash(user['password'], current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('settings'))

    if new_password != confirm_new_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('settings'))

    password_error = validate_password(new_password)
    if password_error:
        flash(password_error, 'danger')
        return redirect(url_for('settings'))

    hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    extensions.users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": hashed_new_password}})

    flash('Your password has been updated successfully.', 'success')
    return redirect(url_for('settings'))