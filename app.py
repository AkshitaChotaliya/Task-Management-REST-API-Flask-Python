from flask import Flask
from database import db
from routes.project_routes import project_bp
from routes.task_routes import task_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(project_bp)
app.register_blueprint(task_bp)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
