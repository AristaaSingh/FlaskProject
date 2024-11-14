from app import db
from datetime import datetime


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    module_code = db.Column(db.String(10))
    deadline_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    is_complete = db.Column(db.Boolean)
