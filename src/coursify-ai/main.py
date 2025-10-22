"""
Coursify-AI - Main Application
Educational content generation platform with AI
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from bson.objectid import ObjectId

# Import extensions and models
from config import Config
from extensions import cors, bcrypt, login_manager, init_mongodb
import extensions
from models import User, load_user

# Import route functions
import auth
import api
import generators


# ============================================================================
# CREATE FLASK APP
# ============================================================================

print("Initializing Coursify-AI...")

app = Flask(__name__, template_folder='my_templates')
app.config.from_object(Config)

# Initialize extensions
cors.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize MongoDB
init_mongodb(app)

# Set user loader
login_manager.user_loader(load_user)

print("✓ Flask app initialized")


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def home():
    """Homepage"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('homepage.html')


@app.route('/index')
@login_required
def index():
    """Dashboard"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'mongodb': 'connected'}), 200


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth.login()


@app.route('/logout')
def logout():
    return auth.logout()


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return auth.forgot_password()


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return auth.reset_password(token)


# ============================================================================
# SETTINGS ROUTES
# ============================================================================

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    user_id = current_user.get_id()
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return render_template('settings.html', user=user)
    else:
        flash("User not found.", 'danger')
        return redirect(url_for('index'))


@app.route('/update_account_settings', methods=['POST'])
@login_required
def update_account_settings():
    return auth.update_account_settings()


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    return auth.change_password()


# ============================================================================
# CONTENT GENERATION ROUTES
# ============================================================================

@app.route('/generate_content', methods=['POST'])
@login_required
def generate_content():
    """Generate PDF or Slides"""
    length = request.form.get('length', type=int, default=100)
    prompt = request.form.get('topics', default='')
    difficulty = request.form.get('difficulty', type=int, default=1)
    content_format = request.form.get('format', default='pdf')

    if content_format == 'pdf':
        return generators.generate_pdf(prompt, length, difficulty)
    elif content_format == 'slides':
        return generators.generate_slides(prompt, length, difficulty)
    else:
        return jsonify(success=False, error="Invalid format selected")


# ============================================================================
# QUIZ ROUTES
# ============================================================================

@app.route('/quiz_generate')
def quiz_generate():
    """Quiz generation page"""
    return render_template('quiz.html')


@app.route('/quiz-generator-page', methods=['POST'])
@login_required
def quiz_generator_page():
    """Generate quiz from form"""
    topic = request.form.get('topic')
    subject = request.form.get('subject')
    mcqs = request.form.get('mcqs', 0)
    true_false = request.form.get('true-false', 0)
    short_questions = request.form.get('short-questions', 0)
    long_questions = request.form.get('long-questions', 0)

    return generators.generate_quiz_from_form(topic, subject, mcqs, true_false, short_questions, long_questions)


@app.route('/generate_quiz/<file_id>')
@login_required
def generate_quiz(file_id):
    """Generate quiz from uploaded file"""
    return generators.generate_quiz_from_file(file_id)


# ============================================================================
# FILE ROUTES
# ============================================================================

@app.route('/content')
@login_required
def my_content():
    """Display user's content"""
    files = extensions.fs.find({"user_id": current_user.get_id()}).sort("_id", -1)
    file_data = []
    for file in files:
        file_data.append({"filename": file.filename, "_id": str(file._id)})
    return render_template('content.html', file_data=file_data)


@app.route('/pdf/<filename>')
@login_required
def get_pdf(filename):
    return api.get_pdf(filename)


@app.route('/presentation/<filename>')
@login_required
def get_presentation(filename):
    return api.get_presentation(filename)


@app.route('/get_doc/<file_id>')
@login_required
def get_doc(file_id):
    return api.get_doc(file_id)


@app.route('/delete/<file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    return api.delete_file(file_id)


@app.route('/share/<file_id>')
def share_file(file_id):
    return api.share_file(file_id)


@app.route('/check_file/<filename>', methods=['GET'])
@login_required
def check_file(filename):
    return api.check_file(filename)


# ============================================================================
# REVIEW ROUTES
# ============================================================================

@app.route('/submit_review', methods=['POST'])
@login_required
def submit_review():
    return api.submit_review()


@app.route('/reviews')
@login_required
def reviews():
    return api.get_reviews()


@app.route('/check_review_existence', methods=['GET'])
@login_required
def check_review_existence():
    return api.check_review_existence()


@app.route('/delete_review', methods=['POST'])
@login_required
def delete_review():
    return api.delete_review()


@app.route('/ratings')
@login_required
def ratings():
    return api.get_ratings()


# ============================================================================
# CHATBOT API
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    return api.chat()


# ============================================================================
# STATIC PAGES
# ============================================================================

@app.route('/ai.html')
def ai_html():
    return render_template('ai.html')


@app.route('/preview/<filename>')
@login_required
def preview():
    return render_template('preview.html')


@app.route('/faq.html')
def faq():
    return render_template('faq.html')


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("="*60)
    print("✓ Coursify-AI ready to start!")
    print("="*60)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)