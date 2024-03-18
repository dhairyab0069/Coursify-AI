import unittest
from unittest.mock import patch
from flask_testing import TestCase
from app import app, User, users_collection
import bcrypt
import xmlrunner

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Create a test user
        password = "password123".encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": hashed_password.decode('utf-8'),
            "birth_date": "1990-01-01",  
            "gender": "Male",
            "verified": True
        }
        users_collection.insert_one(test_user)

    def tearDown(self):
        # Remove the test user
        users_collection.delete_one({"email": "john.doe@example.com"})

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('homepage.html')

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')

    def test_register_user(self):
        response = self.client.post('/register', data={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'birth_day': '1',
        'birth_month': '1',
        'birth_year': '1990',
        'gender': 'Female',
        'submit': 'Register'
     }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
        self.assertIn(b'Registration successful. Welcome!', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')

    def test_login_user(self):
        response = self.client.post('/login', data={
            'email': 'john.doe@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_logout_user(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('homepage.html')

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))