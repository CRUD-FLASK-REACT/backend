from flask import Blueprint, request, jsonify
from .models import db, Task, Comment

bp = Blueprint('main', __name__)

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks]), 200

@bp.route('/tasks', methods=['POST'])
def add_task():
    title = request.json.get('title', None)
    if not title:
        return jsonify({"error": "Task title is required"}), 400
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201

@bp.route('/tasks/<int:task_id>/comments', methods=['GET', 'POST'])
def comments(task_id):
    if request.method == 'GET':
        comments = Comment.query.filter_by(task_id=task_id).all()
        return jsonify([{'id': c.id, 'text': c.text} for c in comments]), 200
    if request.method == 'POST':
        text = request.json.get('text', '')
        comment = Comment(task_id=task_id, text=text)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'id': comment.id, 'text': comment.text}), 201

@bp.route('/tasks/<int:task_id>/comments/<int:comment_id>', methods=['PUT', 'DELETE'])
def comment_modify(task_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()
    if request.method == 'PUT':
        comment.text = request.json['text']
        db.session.commit()
        return jsonify({'id': comment.id, 'text': comment.text}), 200
    if request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        return '', 204

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Admin endpoint to clear all tasks
@bp.route('/reset-tasks', methods=['POST'])
def reset_tasks():
    Task.query.delete()
    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'All tasks deleted.'}), 200

# Test route to check route registration
@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, this is the /test route!'}), 200
