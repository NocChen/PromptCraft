"""app/__init__.py: This file initializes the Flask application and its extensions."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize Flask app
app = Flask(__name__)

# Set secret key for Flask sessions from environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Set SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Initialize Flask-Login manager
login_manager = LoginManager(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import routes after initializing app to avoid circular imports
from ai_prompt_tool import routes
