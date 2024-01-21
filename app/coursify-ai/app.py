from mailbox import Message
from flask import flash
from datetime import datetime
import os
import re
import random
import string
from click import wrap_text
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for, Response, send_file, make_response, redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from flask_cors import CORS
import openai 
import matplotlib.pyplot as plt
from io import BytesIO
from pymongo import MongoClient
from gridfs import GridFS
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




app = Flask(__name__, template_folder='my_templates')
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
openai.api_key = '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'


app.secret_key = 'coursifyai1234'

serializer = URLSafeTimedSerializer(app.secret_key)




# Setup MongoDB connection
client = MongoClient('mongodb+srv://Remy:1234@cluster0.vgzdbrr.mongodb.net/')
db = client['generated_pdfs']
db2=client['Login_details']
fs = GridFS(db)
users_collection=db2.users


# User model
class User(UserMixin):
    def __init__(self, user_id, email):
        self.user_id = str(user_id)
        self.email = email

    def get_id(self):
        return self.user_id

# User Loader
@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(user_id=user["_id"], email=user["email"])
@app.route('/')
def home():
    # If the user is authenticated, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Otherwise, show the homepage with login and register options
    return render_template('homepage.html')

SENDGRID_API_KEY = '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'  

   
    # Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save user to MongoDB
        user_id = users_collection.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
            "verified": False
        }).inserted_id

        token = serializer.dumps(email, salt='email-confirmation-salt')

        # Send verification email
        confirm_url = url_for('confirm_email', token=token, _external=True)
        subject = "Please confirm your email"
        send_email(email, subject, confirm_url)

        flash('A confirmation email has been sent.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
# Send Email Function
def send_email(to_email, subject, confirm_url):
    html_content = render_template('email_verification.html', confirm_url=confirm_url)
    message = Mail(
        from_email='your-email@example.com',  # Replace with your verified sender email
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Email Confirmation Route
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(
            token, 
            salt='email-confirmation-salt', 
            max_age=3600  # Token expires after 1 hour
        )
    except (SignatureExpired, BadSignature):
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))

    user = users_collection.find_one({"email": email})
    if user and not user['verified']:
        users_collection.update_one({"_id": user['_id']}, {"$set": {"verified": True}})
        flash('Your account has been activated!', 'success')
    else:
        flash('Account already activated or not found.', 'success')
    return redirect(url_for('login'))

# Login Route
# Updated Login Route with "Remember Me"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form  # Check if 'Remember Me' is checked

        user = users_collection.find_one({"email": email})
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user_id=user["_id"], email=email)
            login_user(user_obj, remember=remember)
            return redirect(url_for('index'))

        flash('Invalid credentials. Please try again.')

    return render_template('login.html')


@app.route('/index')
@login_required
def index():
    # Dashboard page after successful login
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


    
@app.route('/settings.html')
@login_required  # Ensure that the user is logged in
def settings_html():
    user_id = current_user.get_id()
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:

        return render_template('settings.html', user=user)
    else:
        flash("User not found.")
        return redirect(url_for('index'))



@app.route('/share/<file_id>')
def share_file(file_id):
    # converts id to objectid
    file_id = ObjectId(file_id)

    # Retrieve the file from GridFS
    file = fs.get(file_id)

    # Create a response with the file data
    response = make_response(file.read())
    response.mimetype = 'application/pdf'

    # Set the Content-Disposition header to make the file downloadable
    response.headers.set('Content-Disposition', 'attachment', filename=file.filename)

    return response


def extract_text_from_pdf(pdf_path):
    # This function extracts text from a PDF using PdfReader
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/content')
def my_content():
    # Get a list of all files in GridFS
    files = fs.find()

    # Create a list to store file data
    file_data = []

    # Loop through all files
    for file in files:
        # Get the file name and the file id (used to retrieve the file later)
        file_data.append({"filename": file.filename, "_id": str(file._id)})

    # Render a template and pass the file data to it
    return render_template('content.html', file_data=file_data)

@app.route('/share_via_email', methods=['POST'])
def share_via_email():
    # Get the recipient's email address and the file id from the form data
    recipient = request.form.get('email')
    file_id = request.form.get('file_id')

    # Generate the shareable URL
    share_url = url_for('share_file', file_id=file_id, _external=True)

    # Create a new email message
    msg = Message('Your Shared File',
                  sender='coursify@outlook.com',
                  recipients=[recipient])

    # Add the shareable URL to the email body
    msg.body = f'Here is the file you requested: {share_url}'

    # Send the email

@app.route('/content')
def content():
    return render_template('content.html')



@app.route('/ai.html')
def ai_html():
    return render_template('ai.html')
@app.route('/api/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['message']
        print("User input received:", user_input)  # Debugging log

        
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        print("Response from OpenAI:", response)  # Debugging log

        ai_reply = response['choices'][0]['message']['content']
        print("AI Reply:", ai_reply)  # Debugging log

        return jsonify({'reply': ai_reply})
    except Exception as e:
        print("An error occurred:", e)  # Debugging log
        return jsonify({'error': str(e)}), 500

def is_latex(text):

    return bool(re.search(r"\$.*\$", text))

def render_latex(formula, fontsize=12, dpi=150):

    # Configure Matplotlib to use LaTeX for rendering
    plt.rcParams['text.usetex'] = True
    
    # Set up a Matplotlib figure and text
    fig = plt.figure()
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.patch.set_alpha(0)
    # Use the formula within a TeX environment
    ax.text(0, 0, f"\\begin{{equation}}{formula}\\end{{equation}}", fontsize=fontsize)
    
    # Save the figure to a BytesIO buffer
    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, transparent=True, format='png')
    plt.close(fig)
    buffer.seek(0)
    return buffer


def sanitize_filename(text):
    # Remove invalid filename characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in text if c in valid_chars)
    # Truncate the filename if it's too long
    return sanitized[:255]


def wrap_text(text, max_width, font_name, font_size):
    # Function to wrap text
    wrapped_text = []
    words = text.split()

    while words:
        line = ''
        while words and stringWidth(line + words[0], font_name, font_size) <= max_width:
            line += (words.pop(0) + ' ')
        wrapped_text.append(line)

    return wrapped_text
def content(prompt, length):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
def call_openai_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
    
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Create a subdirectory for PDFs if it doesn't exist
    pdf_directory = os.path.join(os.getcwd(), 'pdfs')
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Process form data
    length = request.form.get('length', type=int, default=100)
    prompt = request.form.get('topics', default='')
    difficulty = request.form.get('difficulty',type=int,default = 1)

    pdf_basename = sanitize_filename(prompt)

    # Ensure the filename is not empty
    pdf_basename = pdf_basename if pdf_basename else 'generated_file'

    # Add a timestamp or random string to the filename to ensure uniqueness
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    pdf_filename = f"{pdf_basename}_{timestamp}_{unique_suffix}.pdf"

    if difficulty == 1:
        diff = "basic"
    elif difficulty == 2:
        diff = "intermediate"
    elif difficulty == 3:
        diff = "advanced"

    
    toc = call_openai_api("Give Table of contents for topic: " +prompt+"(such that there are max 5 topics and each topic has two sub topics. Topics should be upper Case and subtopics otherwise. Dont Start with heading : Table of contents, just show contents with difficulty " + diff)
    if toc is None:
        return jsonify(success=False, error="Failed to generate text from OpenAI API")
    



    
    # Define font properties and margins
    font_name = "Helvetica"
    font_size = 12
    left_margin = 72
    top_margin = 720
    line_height = 14
    page_width, page_height = letter
    bottom_margin = 72
    content_width = page_width - 2 * left_margin

    # Generate PDF
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont(font_name, font_size)
    toc_dict = {}
    current_topic = ""

    

    y_position = top_margin
    c.drawString(left_margin, y_position, "Table of Contents")
    y_position -= line_height
    for line in toc.split('\n'):
        
        is_topic = line.isupper()  # Assuming topics are in uppercase
        contains_latex = is_latex(line)  # Renamed the variable here

        if contains_latex:
            # Process LaTeX content
            latex_image_io = render_latex(line[1:-1])  # Remove $ symbols
            c.drawImage(latex_image_io, left_margin, y_position, width=200, height=100, preserveAspectRatio=True, anchor='n')
            y_position -= 100  # Adjust for image height
        else:
            # Format as a main topic or subtopic
            if is_topic:
                
                c.setFont("Helvetica-Bold", 14)
                y_position -= 20  # Extra space before a main topic
            else:
                if current_topic:  # Ensure there is a current topic
                    toc_dict[current_topic].append(line.strip())
                c.setFont("Helvetica", 12)
                line = "   " + line  # Indent subtopics

            # Add line to PDF
            c.drawString(left_margin, y_position, line)
            y_position -= line_height

        if y_position < 100:  # Check for end of page and create a new one if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = top_margin
    
    c.showPage()
    c.setFont("Helvetica", 12)
    y_position = top_margin

    
    lines = toc.split('\n')
    
    print(lines)
    for line in lines:
        is_topic = line.isupper()  # Assuming topics are in uppercase
        contains_latex = is_latex(line)  # Renamed the variable here

        if contains_latex:
            # Process LaTeX content
            latex_image_io = render_latex(line[1:-1])  # Remove $ symbols
            c.drawImage(latex_image_io, left_margin, y_position, width=200, height=100, preserveAspectRatio=True, anchor='n')
            y_position -= 100  # Adjust for image height
            
        else:
            # Format as a main topic or subtopic
            if is_topic:
                c.setFont("Helvetica-Bold", 14)
                wrapped_text = wrap_text(line, content_width, font_name, 14)
                print(wrapped_text)
                
            else:
                
                c.setFont("Helvetica", 12)
                c.drawString(left_margin, y_position, line)
                y_position -= line_height 
                prompt2 = content("explain in 3 lines about the following topic " +line + "related to " + prompt,length)
                if prompt2 is None:
                    return jsonify(success=False, error="Failed to generate text from OpenAI API")
                wrapped_text = wrap_text(prompt2, content_width, font_name, 12)
                print ("sub topic done")
                
            for text_line in wrapped_text:
                if y_position < bottom_margin:  # Check if we need a new page
                    c.showPage()
                    c.setFont(font_name, 12)
                    y_position = top_margin
                c.drawString(left_margin, y_position, text_line)
                y_position -= line_height 
    
    c.save()

    # Respond with the URL of the PDF
    pdf_url = url_for('get_pdf', filename=pdf_filename)
    return jsonify(success=True, pdf_url=pdf_url)



@app.route('/pdf/<filename>')
def get_pdf(filename):
     directory = os.path.join(os.getcwd(), 'pdfs')   
     file_path = os.path.join(directory, filename)
     if os.path.exists(file_path):
         return send_from_directory(directory, filename)
     else:
         return "File not found", 404

    
  
  #can be used to check if file is in database  
@app.route('/check_file/<filename>', methods=['GET'])
def check_file(filename):
    try:
        file = fs.get_last_version(filename=filename)
        if file:
            return jsonify(success=True, message="File exists in the database.")
    except:
        return jsonify(success=False, message="File does not exist in the database.")
    

@app.route("/chatbot", methods=["POST"])
def chatbot():
    # Get the message from the POST request
    message = request.json.get("message")

    # Set OpenAI API key (if not already set globally)
    openai.api_key = 'your-api-key'

    # Send the message to OpenAI's API and receive the response
    completion = openai.Completion.create(
        engine="text-davinci-003",  # Use the text-davinci-003 model
        prompt=message,
        max_tokens=150  # Adjust max_tokens if necessary
    )

    if completion.choices and completion.choices[0].text.strip() != "":
        return completion.choices[0].text.strip()
    else:
        return 'Failed to Generate response!'
    
   # User Loader
@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(user_id=user["_id"], email=user["email"])

    
if __name__ == '__main__':
    app.debug = True
    app.run()
    
