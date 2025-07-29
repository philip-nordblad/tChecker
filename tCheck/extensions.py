# my_app/extensions.py
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy here, but don't bind it to an app yet.
# It will be bound in the create_app factory.
db = SQLAlchemy()
