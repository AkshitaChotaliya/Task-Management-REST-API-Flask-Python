from models import db, User, Project, Task
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = User(name='Alice', email='alice@example.com')
    u2 = User(name='Bob', email='bob@example.com')
    p1 = Project(name='Website Redesign', description='Revamp marketing site')

    db.session.add_all([u1, u2, p1])
    db.session.commit()

    t1 = Task(title='Setup hosting', user_id=u1.id, project_id=p1.id)
    t2 = Task(title='Design homepage', user_id=u2.id, project_id=p1.id)

    db.session.add_all([t1, t2])
    db.session.commit()

    print("Seed data inserted successfully.")
