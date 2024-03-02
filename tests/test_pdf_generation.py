# tests/test_pdf_generation.py
import os
import sys
import unittest
from unittest.mock import patch
from flask_testing import TestCase
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
from flask_mail import Mail, Message
from pptx import Presentation
from flask import Flask, send_file, abort


# Adjust the path to include the directory where app.py resides
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app', 'coursify-ai'))

from app import create_app,generate_pdf  # Adjust the import according to your application structure

class TestPDFGeneration(TestCase):
    
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    
    def test_generate_pdf(self):
        prompt = "Sample Prompt"
        length = 1000
        difficulty = 2
        
        response = generate_pdf(prompt, length, difficulty)
        
        self.assertTrue(response['success'])
        self.assertIsNotNone(response['pdf_url'])
        # Add more assertions to validate the generated PDF and its contents
    
    def test_generate_pdf_with_invalid_prompt(self):
        prompt = ""
        length = 1000
        difficulty = 2
        
        response = generate_pdf(prompt, length, difficulty)
        
        self.assertFalse(response['success'])
        self.assertEqual(response['error'], "Failed to generate text from OpenAI API")
    
    def test_generate_pdf_with_invalid_subtopic(self):
        prompt = "Sample Prompt"
        length = 1000
        difficulty = 2
        
        # Mock the call to OpenAI API to return None for subtopic
        with patch('your_module.call_openai_api') as mock_call_openai_api:
            mock_call_openai_api.return_value = None
            
            response = generate_pdf(prompt, length, difficulty)
        
        self.assertFalse(response['success'])
        self.assertEqual(response['error'], "Failed to generate text from OpenAI API")
    
    # Add more test cases as needed
if __name__ == '__main__':
    unittest.main()
