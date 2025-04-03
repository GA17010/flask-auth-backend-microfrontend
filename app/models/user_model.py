from app.database import db
from flask import current_app
from datetime import datetime
import pytz

class User(db.Model):
    """
    User Model
    This model represents a user in the application and is used for database interactions.
    Attributes:
        id (int): The primary key for the user.
        full_name (str): The full name of the user. This field is required.
        company (str): The company name associated with the user. This field is optional.
        password (str): The hashed password of the user. This field is required.
        email (str): The unique email address of the user. This field is required.
        created_at (datetime): The timestamp when the user was created. Defaults to the current UTC time.
        updated_at (datetime): The timestamp when the user was last updated. Automatically updated on changes.
    Methods:
        set_password(password):
            Hashes and sets the user's password.
            Args:
                password (str): The plain text password to be hashed and set.
            Raises:
                RuntimeError: If bcrypt is not initialized in the Flask app context.
        check_password(password):
            Verifies the provided password against the stored hashed password.
            Args:
                password (str): The plain text password to verify.
            Returns:
                bool: True if the password matches, False otherwise.
        __repr__():
            Returns a string representation of the user instance.
            Returns:
                str: A string containing the user's id, full name, and email.
        to_dict():
            Converts the user instance to a dictionary representation.
            Returns:
                dict: A dictionary containing the user's id, full name, company, created_at, and updated_at.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/El_Salvador')))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/El_Salvador')), onupdate=datetime.now(pytz.timezone('America/El_Salvador')))

    def set_password(self, password):
        if not hasattr(current_app, 'bcrypt'):
            raise RuntimeError("bcrypt is not initialized in the Flask app context.")
        self.password = current_app.bcrypt.generate_password_hash(password).decode("utf-8")
        if not hasattr(current_app, 'bcrypt'):
            raise RuntimeError("bcrypt is not initialized in the current application context.")
        return current_app.bcrypt.check_password_hash(self.password, password)
    
    def check_password(self, password):
        return current_app.bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User id={self.id}, full_name={self.full_name}, email={self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'company': self.company,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
