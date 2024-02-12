import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Default image URL for user profile images
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    """Site user."""

    # Define table name for User model
    __tablename__ = "users"

    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    # Define relationship with Post model
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""
        # Combine first name and last name to form full name
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    # Define table name for Post model
    __tablename__ = "posts"

    # Define columns for the Post table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)  # Set default value to current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return formatted date."""
        # Format the creation date to a friendlier format
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

def connect_db(app):
    """Connect this database to the Flask app.

    Args:
        app (Flask): The Flask app to connect to the database.

    This should be called first in the Flask app.
    """
    # Set the Flask app for the SQLAlchemy instance and initialize the app with SQLAlchemy
    db.app = app
    db.init_app(app)
