from flask import Blueprint, request, jsonify
from models import Task, StatusEnum
from database import db


task_bp = Blueprint('task_bp', __name__)

def has_circular_dependency(task, depends_on_task):
    visited = set()

    def visit(t):
        if t.id in visited:
            return False
        visited.add(t.id)
        if t.id == task.id:
            return True
        for dep in t.dependencies:
            if visit(dep):
                return True
        return False

    return visit(depends_on_task)


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    required_fields = ['title', 'project_id', 'user_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    task = Task(
        title=data['title'],
        status=StatusEnum.TODO,
        project_id=data['project_id'],
        user_id=data['user_id']
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully',
        'task': {'id': task.id, 'title': task.title, 'status': task.status.value}
    }), 201

@task_bp.route('/tasks', methods=['GET'])
def list_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Task.query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [{
        'id': t.id,
        'title': t.title,
        'status': t.status.value,
        'project_id': t.project_id,
        'user_id': t.user_id
    } for t in pagination.items]

    return jsonify({
        'tasks': tasks,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200



@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({'id': task.id, 'title': task.title, 'status': task.status.value})

@task_bp.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_status = data['status']

    if task.status != StatusEnum.DONE:
        task.status = StatusEnum(new_status)
        db.session.commit()
        return jsonify({'message': 'Status updated'})
    return jsonify({'error': 'Cannot update completed task'}), 400

@task_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def list_tasks_by_user(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': t.id, 'title': t.title} for t in tasks])

@task_bp.route('/tasks/status/<status>', methods=['GET'])
def list_tasks_by_status(status):
    try:
        enum_status = StatusEnum(status)
    except ValueError:
        return jsonify({'error': 'Invalid status'}), 400
    tasks = Task.query.filter_by(status=enum_status).all()
    return jsonify([{'id': t.id, 'title': t.title} for t in tasks])

@task_bp.route('/tasks/<int:task_id>/dependencies', methods=['POST'])
def add_dependency(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    depends_on_id = data.get('depends_on_id')
    depends_on_task = Task.query.get_or_404(depends_on_id)

    if has_circular_dependency(task, depends_on_task):
        return jsonify({'error': 'Circular dependency detected'}), 400

    task.dependencies.append(depends_on_task)
    db.session.commit()
    return jsonify({'message': 'Dependency added'}), 201



