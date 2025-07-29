# my_app/models.py
from datetime import datetime
from tCheck.extensions import db # Import the SQLAlchemy db instance
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user' # Explicitly set table name to match your schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False) # Store hashed passwords!
    is_manager = db.Column(db.Boolean, default=False)

    # Relationships
    created_list_templates = db.relationship('ListTemplate', backref='creator', lazy=True)
    assigned_lists = db.relationship('UserListAssignment', backref='user_assignee', lazy=True)
    completed_items = db.relationship('UserCompletedItem', backref='user_completer', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_pin(self, pin_hash):
        """Hashes the given password and stores it."""
        self.pin_hash = generate_password_hash(pin_hash,method='pbkdf2:sha256')

    def check_pin(self, pin_hash):
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.pin_hash, pin_hash)

    def to_dict(self):
        """Converts the User object to a dictionary (EXCLUDING password)."""
        return {
            'id': self.id,
            'username': self.username,
            'is_manager': self.is_manager
        }



class ListTemplate(db.Model):
    __tablename__ = 'list_template'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    # Relationship to list items within this template
    items = db.relationship('ListItemTemplate', backref='list_template', lazy=True, order_by='ListItemTemplate.item_order')
    # Relationship to user assignments for this template
    assignments = db.relationship('UserListAssignment', backref='assigned_template', lazy=True)

    def __repr__(self):
        return f'<ListTemplate {self.name}>'

class ListItemTemplate(db.Model):
    __tablename__ = 'list_item_template'
    id = db.Column(db.Integer, primary_key=True)
    list_template_id = db.Column(db.Integer, db.ForeignKey('list_template.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requires_input = db.Column(db.Boolean, default=False)
    input_type = db.Column(db.String(50)) # e.g., 'text', 'number', 'date'
    item_order = db.Column(db.Integer, nullable=False)

    # Relationship to user completed items for this specific item template
    completed_by_users = db.relationship('UserCompletedItem', backref='item_template', lazy=True)

    def __repr__(self):
        return f'<ListItemTemplate {self.description}>'

class UserListAssignment(db.Model):
    __tablename__ = 'user_list_assignment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    list_template_id = db.Column(db.Integer, db.ForeignKey('list_template.id'), nullable=False)

    # Ensure a user is assigned to a list template only once
    __table_args__ = (db.UniqueConstraint('user_id', 'list_template_id', name='_user_list_assignment_uc'),)

    def __repr__(self):
        return f'<UserListAssignment UserID:{self.user_id} ListTemplateID:{self.list_template_id}>'

class UserCompletedItem(db.Model):
    __tablename__ = 'user_completed_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    list_item_template_id = db.Column(db.Integer, db.ForeignKey('list_item_template.id'), nullable=False)
    input_value = db.Column(db.Text) # To store the actual input if requires_input is true
    completed_at = db.Column(db.DateTime, default=datetime.utcnow) # When it was completed

    # Ensure a user completes a specific item template only once (or you might allow multiple completions
    # if it's a recurring task, then remove this unique constraint and add a timestamp to distinguish)
    __table_args__ = (db.UniqueConstraint('user_id', 'list_item_template_id', name='_user_completed_item_uc'),)

    def __repr__(self):
        return f'<UserCompletedItem UserID:{self.user_id} ItemTemplateID:{self.list_item_template_id}>'
