from flask import Flask
from sqlalchemy.sql import func
from factory import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.now())

    def __repr__(self):
        return '<Email %r>' % self.email


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    urgency = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.now())

    comments = db.relationship('Comment', backref='comments', lazy=True)


    def __repr__(self):
        return '<id: %r, email: %r, subject: %r>' % (self.id ,self.email, self.subject)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),
                          nullable=False)
    message = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.now())

    def __repr__(self):
        return '<Comment for %r>' % self.ticket_id
