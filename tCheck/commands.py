# my_app/commands.py
import click
from flask.cli import with_appcontext
from tCheck.extensions import db # Import the SQLAlchemy db instance
from tCheck.models import User, ListTemplate, ListItemTemplate, UserListAssignment, UserCompletedItem # Import your models

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables using SQLAlchemy."""
    db.drop_all() # Drops all tables defined by your SQLAlchemy models
    db.create_all() # Creates all tables defined by your SQLAlchemy models
    click.echo('Initialized the database using SQLAlchemy.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with test data."""
    # Clear existing data (for testing purposes only!)
    click.echo("🔄 Clearing existing data...")
    UserCompletedItem.query.delete()
    UserListAssignment.query.delete()
    ListItemTemplate.query.delete()
    ListTemplate.query.delete()
    User.query.delete()
    db.session.commit()

    click.echo("🧪 Creating users...")
    # Create Users
    manager = User(username="manager1", is_manager=True)
    manager.set_pin("1234")
    user = User(username="user1", is_manager=False)
    user.set_pin("5678")
    db.session.add_all([manager, user])
    db.session.commit()

    click.echo("📋 Creating list templates...")
    # Create List Templates
    checklist1 = ListTemplate(
        name="Daily Tasks",
        description="Routine daily checks",
        creator_id=manager.id,
        is_public=True
    )
    checklist2 = ListTemplate(
        name="Weekly Maintenance",
        description="Weekly maintenance tasks",
        creator_id=manager.id,
        is_public=True
    )
    db.session.add_all([checklist1, checklist2])
    db.session.commit()

    click.echo("🧩 Adding items to templates...")
    # Add Items to Template 1
    items1 = [
        ListItemTemplate(
            list_template_id=checklist1.id,
            description="Check door locks",
            requires_input=False,
            item_order=1
        ),
        ListItemTemplate(
            list_template_id=checklist1.id,
            description="Log temperature",
            requires_input=True,
            input_type="number",
            item_order=2
        ),
        ListItemTemplate(
            list_template_id=checklist1.id,
            description="Sanitize surfaces",
            requires_input=False,
            item_order=3
        )
    ]

    # Add Items to Template 2
    items2 = [
        ListItemTemplate(
            list_template_id=checklist2.id,
            description="Inspect fire extinguishers",
            requires_input=False,
            item_order=1
        ),
        ListItemTemplate(
            list_template_id=checklist2.id,
            description="Backup server",
            requires_input=False,
            item_order=2
        )
    ]
    db.session.add_all(items1 + items2)
    db.session.commit()

    click.echo("👥 Assigning users to lists...")
    # Assign User to both Templates
    assignment1 = UserListAssignment(user_id=user.id, list_template_id=checklist1.id)
    assignment2 = UserListAssignment(user_id=user.id, list_template_id=checklist2.id)
    db.session.add_all([assignment1, assignment2])
    db.session.commit()

    click.echo("✅ Marking some items as completed...")
    # Simulate completed items
    completed_items = [
        UserCompletedItem(
            user_id=user.id,
            list_item_template_id=items1[0].id
        ),
        UserCompletedItem(
            user_id=user.id,
            list_item_template_id=items1[1].id,
            input_value="22.5"
        ),
        UserCompletedItem(
            user_id=user.id,
            list_item_template_id=items2[0].id
        )
    ]
    db.session.add_all(completed_items)
    db.session.commit()

    click.echo("✅ Database seeded with mock data.")