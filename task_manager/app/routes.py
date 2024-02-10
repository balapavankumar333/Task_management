from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask import jsonify
from app import app, db
from app.models import Task
from flask import Blueprint     

users_task = Blueprint('users_task', __name__)


from datetime import datetime

@users_task.route("/task", methods=['POST'])
def create_task():
    try:
        data = request.json
        if data is None:
            return jsonify({'message': "Request must contain JSON data"}, 400)

        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        
        # Convert due_date string to datetime object
        due_date_str = data.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        if not title:
            return jsonify({'message': "Title is required"}, 400)
        
        # Handle user_id if provided, default to None otherwise
        user_id = data.get('user_id')


        new_task = Task(title=title, description=description, status=status, due_date=due_date,user_id=user_id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': "Task created successfully"}, 201)
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f"Something went wrong: {str(e)}"}, 400)

    except Exception as e:
        return jsonify({'message': f"An error occurred: {str(e)}"}, 500)


@users_task.route('/task', methods=['GET'])
def get_task():
    tasks = Task.query.all()
    task_data = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
    return jsonify(task_data)



@users_task.route('/task/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.json
    title = data.get('title')
    description = data.get('description')
    # Update task attributes
    if title:
        task.title = title
    if description:
        task.description = description
    # You can similarly update other attributes like status and due_date
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})



@users_task.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})
