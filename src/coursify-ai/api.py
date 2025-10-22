"""
API Routes: Chatbot, File Operations, Reviews, Ratings
"""
import io
from datetime import datetime
from flask import jsonify, request, make_response, send_file, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from gridfs import NoFile

from extensions import fs, reviews_collection, users_collection
from utils import llm


# ============================================================================
# CHATBOT API
# ============================================================================

def chat():
    """Chatbot API endpoint"""
    try:
        user_input = request.json['message']
        print("User input received:", user_input)

        system_prompt = """You are an AI assistant for Coursify.ai, an educational content generation platform.
        Help users with:
        - Generating content (PDFs, slides, quizzes)
        - Navigating to 'My Content' section
        - Updating account settings
        - Understanding features
        Be helpful, clear, and friendly."""

        ai_reply = llm.generate(user_input, system_prompt)

        if ai_reply is None:
            return jsonify({'error': 'Failed to generate response from LLM'}), 500

        print("AI Reply:", ai_reply)
        return jsonify({'reply': ai_reply})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({'error': str(e)}), 500


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def get_pdf(filename):
    """Download a PDF from GridFS"""
    if current_user.is_authenticated:
        grid_out = fs.find_one({'filename': filename, 'user_id': current_user.user_id})

        if grid_out:
            response = make_response(grid_out.read())
            response.mimetype = 'application/pdf'
            return response
        else:
            return "File not found", 404
    else:
        return "Unauthorized", 401


def get_presentation(filename):
    """Download a presentation from GridFS"""
    if current_user.is_authenticated:
        grid_out = fs.find_one({'filename': filename, 'user_id': current_user.user_id})

        if grid_out:
            response = make_response(grid_out.read())
            response.mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return response
        else:
            abort(404, description="Presentation file not found")
    else:
        abort(401, description="Unauthorized")


def get_doc(file_id):
    """Download a document from GridFS"""
    try:
        file_id = ObjectId(file_id)
        grid_out = fs.get(file_id)
        return send_file(io.BytesIO(grid_out.read()), download_name=grid_out.filename, as_attachment=True)
    except NoFile:
        return jsonify({'error': 'File not found'}), 404


def delete_file(file_id):
    """Delete a file from GridFS"""
    file_id = ObjectId(file_id)
    fs.delete(file_id)
    flash('File deleted successfully!', 'success')
    return redirect(url_for('my_content'))


def share_file(file_id):
    """Share a file with a unique URL"""
    file_id = ObjectId(file_id)
    file = fs.get(file_id)
    response = make_response(file.read())
    response.mimetype = 'application/pdf'
    response.headers.set('Content-Disposition', 'attachment', filename=file.filename)
    return response


def check_file(filename):
    """Check if a file exists"""
    try:
        file = fs.get_last_version(filename=filename)
        if file:
            return jsonify(success=True, message="File exists in the database.")
    except:
        return jsonify(success=False, message="File does not exist in the database.")


# ============================================================================
# REVIEWS
# ============================================================================

@login_required
def submit_review():
    """Submit a review for a file"""
    form_data = request.form
    star_rating = form_data.get('star_rating')
    review_text = form_data.get('review_text')
    subject = form_data.get('subject')
    file_id = form_data.get('file_id')

    user_id = ObjectId(current_user.get_id())
    user_details = users_collection.find_one({"_id": user_id})

    if not user_details:
        flash('User not found.', 'danger')
        return redirect(url_for('my_content'))

    first_name = user_details.get('first_name', '')
    last_name = user_details.get('last_name', '')

    # Check if review already exists
    if reviews_collection.find_one({"user_id": user_id, "file_id": file_id}):
        flash('You have already reviewed this file.', 'info')
        return redirect(url_for('my_content'))

    review = {
        "user_id": user_id,
        "file_id": file_id,
        "first_name": first_name,
        "last_name": last_name,
        "star_rating": star_rating,
        "review_text": review_text,
        "subject": subject,
        "timestamp": datetime.utcnow()
    }

    reviews_collection.insert_one(review)
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('my_content'))


@login_required
def get_reviews():
    """Display all reviews"""
    all_reviews = reviews_collection.find().sort("timestamp", -1)
    return render_template('reviews.html', reviews=all_reviews)


@login_required
def check_review_existence():
    """Check if a review exists for a file"""
    file_id = request.args.get('file_id')
    user_id = ObjectId(current_user.get_id())

    existing_review = reviews_collection.find_one({"user_id": str(user_id), "file_id": file_id})
    if existing_review:
        return jsonify({"reviewExists": True})
    else:
        return jsonify({"reviewExists": False})


@login_required
def delete_review():
    """Delete a review"""
    file_id = request.form.get('file_id')
    user_id = current_user.get_id()
    reviews_collection.delete_one({"user_id": user_id, "file_id": file_id})
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('get_reviews'))


# ============================================================================
# RATINGS
# ============================================================================

def calculate_ratings():
    """Calculate star ratings and average"""
    all_reviews = list(reviews_collection.find())
    star_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_rating = 0
    total_count = 0

    for review in all_reviews:
        rating = review.get('star_rating')
        if rating is not None and rating != '' and rating != 0:
            rating = int(rating)
            star_counts[rating] += 1
            total_rating += rating
            total_count += 1

    average_rating = total_rating / total_count if total_count else 0
    return star_counts, average_rating


@login_required
def get_ratings():
    """Get star ratings and average rating"""
    star_counts, average_rating = calculate_ratings()
    return jsonify({'star_counts': star_counts, 'average_rating': average_rating})