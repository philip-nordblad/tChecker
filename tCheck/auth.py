from flask import (Blueprint, flash, redirect, render_template, url_for, request, session, jsonify)

from werkzeug.security import generate_password_hash, check_password_hash
from tCheck.extensions import db
from .forms import RegistrationForm, LoginForm
from tCheck.models import User




bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        pin_code = form.pin_code.data

        error = None

        if not username:
            error = 'Username is required.'
        elif not pin_code:
            error = 'PIN code is required.'
        elif len(pin_code) != 4:
            error = 'PIN must be 4 digits.'

        if error is None:
            try:
                all_users = User.query.all()

                for v in all_users:
                    if v.check_pin(pin_code):
                        error = "Not Unique Pin Code, Try Again."
                        break

                if error is None:
                    new_user = User(username=username)
                    new_user.set_pin(pin_code)
                    db.session.add(new_user)
                    db.session.commit()

                    flash(f'Registration successful for {username}!', 'success')
                    return redirect(url_for('auth.login'))
            except db.IntegrityError as e:
                print(e)
                error = f'Username {username} already exists.'


        flash(error or 'Registration failed')

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('auth/login.html', form=form)


    # AJAX POST handling
    data = request.get_json()
    error = None

    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400

    # Initialize attempt counter

    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    # Check attempt limit
    
    if session['login_attempts'] >= 3:
        return jsonify({
            'success': False,
            'error': 'Too many failed attempts. Please try again later.',
            'status': 429
        }), 429


    # Get PIN from request
    input_pin = str(data.get('pin', '')).strip()
    if not input_pin:
        return jsonify({
            'success': False,
            'error': 'PIN is required',
            'status': 400
        }), 400

    all_users = User.query.all()
    authenticated_user = None

    print(f"pin vs input_pin: {data.get('pin')} vs {input_pin}")
    for u in all_users:
        if u.check_pin(input_pin):
            session['login_attempts'] += 1
            authenticated_user = u
            break
        else:
            print()

    if authenticated_user:
        # Successful login
        session.clear()
        session['user_id'] = authenticated_user.id
        session['username'] = authenticated_user.username
        session['login_attempts'] = 0

        return jsonify({
            'success': True,
            'username': authenticated_user.username,
            'redirect': url_for('tasks.dashboard')
        })
    else:
        # Failed login
        session['login_attempts'] += 1
        return jsonify({
            'success': False,
            'error': 'Invalid PIN',
            'attempts_remaining': 3 - session['login_attempts'],
            'status': 401
        }), 401




@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))