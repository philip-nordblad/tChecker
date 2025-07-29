from flask import (Blueprint, flash, redirect, render_template, url_for, request, session, jsonify, g)

from werkzeug.security import generate_password_hash, check_password_hash
from tCheck.extensions import db
from tCheck.models import ListTemplate

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    #user_id = g.user.id if g.user else None

    lists = []

    publicLists = ListTemplate.query.filter_by(is_public=True).all()


    print(type(publicLists))

    if not lists:
        mock_public_lists_data = [
            {
                'id': 1,
                'name': 'Daily Habits',
                'description': 'A list of things to do every day to stay productive and healthy.'
            },
            {
                'id': 2,
                'name': 'Weekend Chores',
                'description': 'Tasks for a productive weekend, including home maintenance and errands.'
            },
            {
                'id': 3,
                'name': 'Reading List',
                'description': 'Books I want to read this year, covering various genres and topics.'
            },
            {
                'id': 4,
                'name': 'Project Alpha Milestones',
                'description': 'Key deliverables and deadlines for Project Alpha.'
            }
        ]
        lists = mock_public_lists_data

    return render_template('tasks/dashboard.html',lists=publicLists)


@bp.route('/create_list', methods=['GET', 'POST'])
def create_list():

    if request.method == 'POST':

        list_title = request.form.get('title')


