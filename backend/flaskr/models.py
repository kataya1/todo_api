from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, description):

        self.description = description
        self.completed = False
        self.created_at = datetime.now()
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return f'Todo {self.id} task:{self.description} created at:{self.created_at} completed: {self.completed}'

    def __repr__(self):
        return {
            'id': self.id,
            'task': self.description,
            'created at': self.created_at,
            'completed': self.completed,
        }


