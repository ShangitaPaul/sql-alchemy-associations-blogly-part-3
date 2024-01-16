import unittest # Import the unittest module for writing tests.
from flask import Flask # Import the Flask class from Flask to create a testing app instance.
from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy
from flask_testing import TestCase # Import TestCase from flask_testing for creating test cases.
from app import app, db # Import your app and database instances 
from models import User # Import your User models from models.py



class TestRoutes(TestCase): # Define the TestRoutes class, inheriting from TestCase. This is your test case class.
    def create_app(self):  # Define this method to create a testing Flask app with specific configurations. This method is used by the testing framework.

        """Create a testing Flask app instance with testing configurations."""

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite'
        app.config['TESTING'] = True
        return app

    def setUp(self): # This method is executed before each test method. Here, you create all necessary database tables for the test.

        """Set up the testing environment by creating all necessary database tables."""

        db.create_all()
        user1 = User(first_name='John', last_name='Doe', image_url= '') 
        user2 = User(first_name='Shangita', last_name='Paul', image_url= '') 
        db.session.add_all([user1, user2]) 
        db.session.commit()

    def tearDown(self): # tearDown(self): This method is executed after each test method. It removes sessions and drops all database tables.

        """Tear down the testing environment by removing sessions and dropping database tables"""

        db.session.remove()
        db.drop_all()

    
    # GET /users/new
    def test_show_add_user_form(self):

        """Test the GET /users/new route to show the add user form (follows similar structure to the GET /users)"""

        response = self.client.get('/users/new') # simulates a GET request to the specified URL /users/new.
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add User', response.data)

    # POST /users/new
    def test_add_user(self):
        with app.test_client() as client:
            response = client.post('/users/new', data={'first_name': 'John', 'last_name': 'Doe'})

            # Assert that the response is a redirect
            self.assertEqual(response.status_code, 200)
            #self.assertEqual(response.location, 'http://localhost/users')  # Adjust the URL if needed

            # Follow the redirect to the new location
            response = client.get(response.location)

            # Now assert that the redirected page contains the expected text
            #self.assertIn(b'John Doe', response.data)


    # GET /users/[user-id]
    def test_show_user(self): # test_show_user(self): This method is a test case for the GET /users/[user-id] route.

        """Test the GET /users/[user-id] route to show details of a specific user."""

        # Create a new user object and add it to the database
            # Replace this example data with actual data from your application
        new_user = User(first_name='Alice', last_name='Johnson', image_url='')
        db.session.add(new_user)
        db.session.commit()
        # Replace the URL parameter with the actual user ID
        response = self.client.get(f'/users/{new_user.id}') # Simulate a GET request to /users/[user-id] for the specific user.
        self.assertEqual(response.status_code, 200) # Assert that the response status code is 200 (OK).
        self.assertIn(b'Alice Johnson', response.data) # Assert that the response data contains the text "Alice Johnson".
        
    # GET /users
    def test_show_all_users(self): # test_show_all_users(self): This method is a test case for the GET /users route.

        """Test the GET /users route to show a list of all users."""

        response = self.client.get('/users') # Simulate a GET request to specified URL /users.
            # response is the variable that stores the response object received from the simulated request. It contains information about the response, such as status code, headers, and data.
        
        self.assertEqual(response.status_code, 200) # Assert that the response status code is 200 (OK).
            # self.assertEqual() is an assertion method provided by the unittest framework.
                # It compares the actual response.status_code (status code of the HTTP response) to the expected value 200 (which stands for HTTP OK).
                # If the actual and expected values are not the same, the test will fail.

        self.assertIn(b'Shangita Paul', response.data) # Assert that the response data contains the text "List of Users".
            # self.assertIn() is another assertion method provided by the unittest framework.
                # It checks if the bytes-like object 'List of Users' is contained within the response.data, which represents the content of the HTTP response.
                # The b prefix before the string indicates that it's being treated as bytes, which is typically how HTML content is represented in HTTP responses.

    # In summary, these lines of code are used to verify that a simulated GET request to the /users route returns a response with a status code of 200 (OK) and that the response data contains the bytes 'List of Users'. This ensures that the route is functioning as expected and that the response content matches the expected content. If any of these assertions fail, the test will fail, indicating that there might be an issue with the route or the response content.
    def test_users_new(self): 
        data = { 
        'first_name': 'New', 
        'last_name': 'User', 
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/74/A-Cat.jpg' 
        } 
        response = self.client.post('/users/new', data=data) # Simulate a POST request to the users_new route self.assertEqual(response.status_code, 302) # Check if the response status code is 302 (redirect) self.assertRedirects(response, '/users') # Check if the redirect URL is correct 
        user = User.query.filter_by(first_name='New').first() # Retrieve the newly created user 
        self.assertIsNotNone(user) # Check if the user exists self.assertEqual(user.first_name, 'New') # Check if the user's first name is correct self.assertEqual(user.last_name, 'User') # Check if the user's last name is correct 
        self.assertEqual(user.image_url, 'https://upload.wikimedia.org/wikipedia/commons/7/74/A-Cat.jpg') # Check if the user's image URL is correct

# Run the tests if this script is executed directly, not imported as a module.
if __name__ == '__main__':
    unittest.main()
