from flask import Flask, Blueprint,request, jsonify, abort
from config import Config
from models import User,Task,StatusEnum
from database import db
# from app import generate_token
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity


# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


@user_bp.route('/users/users-post', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        abort(400, description="Missing name or email")

    User.validate_email(email)

    user = User(name=name, email=email)
    db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    return jsonify(user.to_dict()), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = [user.to_dict() for user in pagination.items]

    return jsonify({
        'users': users,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    active_tasks_count = Task.query.filter(
        Task.user_id == user.id,
        Task.status != StatusEnum.DONE
    ).count()

    if active_tasks_count > 0:
        return jsonify({
            'error': 'Cannot delete user assigned to pending or in-progress tasks'
        }), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
