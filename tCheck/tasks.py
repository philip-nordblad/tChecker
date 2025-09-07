from flask import (Blueprint, flash, redirect, render_template, url_for, request, session, jsonify, g)

from werkzeug.security import generate_password_hash, check_password_hash
from tCheck.extensions import db
from tCheck.models import ListTemplate, UserCompletedItemLog, ListItemTemplate

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():



    publicLists = ListTemplate.query.filter_by(is_public=True).all()

    # need to keep the track of the logs which have been completed by the user
    user_id = session.get('user_id')
    if user_id:
        g.user_id = user_id
    else:
        g.user_id = None 
        
    logs = UserCompletedItemLog.query.filter_by(user_id=user_id).all() if user_id else []
    
    g.completed_item_ids = {log.list_item_template_id for log in logs}



    return render_template('tasks/dashboard.html',lists=publicLists, logs=logs)


@bp.route('/create_list', methods=['GET', 'POST'])
def create_list():

    user_id = session.get('user_id')
    if user_id is None:
        flash('You must be logged in to create a list.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            list_name = request.form.get('list_name').strip()
            list_description = request.form.get('list_description').strip()
            is_public = request.form.get('is_public') == 'on'

            # Basic validation
            if not list_name:
                flash('List name is required.', 'error')
                return redirect(url_for('tasks.create_list'))
            
            existing_list = ListTemplate.query.filter_by(name=list_name).first()

            if existing_list:
                flash(f'List name "{list_name}" already exists. Please choose a different name.', 'error')
                return redirect(url_for('tasks.create_list'))
            
            new_list = ListTemplate(
                name=list_name,
                description=list_description,
                creator_id=user_id,
                is_public=is_public
            )
            db.session.add(new_list)
            db.session.flush()  # Flush to get the new_list.id

            #process items
            item_descriptions = request.form.getlist('item_description[]')
            item_orders = request.form.getlist('item_order[]')
            requires_inputs = request.form.getlist('requires_input[]')
            item_input_types = request.form.getlist('input_type[]')


            # process items

            for i, description in enumerate(item_descriptions):
                if description.strip():  # Only add non-empty descriptions
                    requires_input = str(i) in requires_inputs
                    input_type = item_input_types[i] if i < len(item_input_types) else 'text'

                    new_item = ListItemTemplate(
                        list_template_id=new_list.id,
                        description=description.strip(),
                        requires_input=requires_input,
                        input_type=input_type if requires_input else None,
                        item_order = i + 1
                    )
                    db.session.add(new_item)

            db.session.commit()
            flash(f'List "{list_name}" created successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash('Error creating list. Please try again.', 'error')
            print(f"Error: {e} ")
            return render_template('tasks/create_list.html')
        

    return render_template('tasks/create_list.html')


           
                



@bp.route('/complete_item', methods=['POST', 'GET'])
def complete_item():
    print("Complete Item Endpoint Hit")
    data = request.get_json(silent=True)
    print(data)

    item_id = data.get('item_id')
    user_id = session.get('user_id')
    input_value = data.get('item_input', '')

    if user_id is None:
        return jsonify({'status': 'error', 'message': 'User not logged in.'}), 401

    # Always insert a log entry (no uniqueness restriction)
    new_log_entry = UserCompletedItemLog(
        list_item_template_id=item_id,
        user_id=user_id,
        action="completed",
        input_value=input_value
    )
    db.session.add(new_log_entry)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Item logged as completed.'}), 200
