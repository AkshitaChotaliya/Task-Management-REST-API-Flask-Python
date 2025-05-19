from flask import Blueprint, request, jsonify
from models import Project, Task
from database import db


project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(name=data['name'], description=data.get('description'))
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id}), 201

@project_bp.route('/projects', methods=['GET'])
def list_projects():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Project.query.paginate(page=page, per_page=per_page, error_out=False)
    projects = pagination.items

    return jsonify({
        'projects': [{'id': p.id, 'name': p.name} for p in projects],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    })



@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'name': project.name, 'description': project.description})

@project_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def list_project_tasks(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status.value} for t in tasks])