# tCheck/__init__.py
import os
from flask import Flask, url_for, render_template # Added render_template
from flask_wtf.csrf import CSRFProtect
from tCheck.extensions import db # Import the db instance from extensions


def create_app(test_config=None):
    """
    Flask application factory function.
    Initializes the Flask app, configures it, sets up extensions,
    and registers blueprints.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        # SQLAlchemy configuration for SQLite
        # This is the path to your SQLite database file
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'tCheck.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False, # Suppresses a warning and saves memory
    )

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Load configuration from config.py if not in testing mode
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test configuration if provided
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Flask extensions
    # db (SQLAlchemy) is initialized here with the app instance
    db.init_app(app)

    # Define a simple index route
    @app.route('/')
    def index():
        # Using render_template for consistency, though a simple string works too
        # You'll likely want a full HTML page here later
        login_url = url_for('auth.login')
        return render_template('index.html', login_url=login_url)

    # Register CLI commands (e.g., for database initialization)
    # This 'commands' module will contain the init-db command for SQLAlchemy
    from . import commands
    app.cli.add_command(commands.init_db_command)
    app.cli.add_command(commands.seed_db_command) # Keep your seed command
    # app.cli.add_command(commands.create_admin_command) # If you add more

    # Register Blueprints for different parts of your application
    from . import auth
    app.register_blueprint(auth.bp)

    from . import tasks # Assuming 'tasks' blueprint exists and is still needed
    app.register_blueprint(tasks.bp)

    # You'll likely want a main dashboard blueprint too
    #from .views import main # Assuming you put dashboard logic in views/main.py
    #app.register_blueprint(main.main_bp)


    return app

