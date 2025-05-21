from flask import Flask,jsonify,request
from database import db
from routes.project_routes import project_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from flask_jwt_extended import JWTManager
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'
jwt = JWTManager(app)


db.init_app(app)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(task_bp, url_prefix='/tasks')

# def generate_token(user_id):
#     payload = {
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
#         'iat': datetime.datetime.utcnow(),
#         'sub': user_id
#     }
#     return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# def verify_token(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'message': 'Token is missing'}), 401
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid'}), 401
#         return f(*args, **kwargs)
#     return decorated

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
