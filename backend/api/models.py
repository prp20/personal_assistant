from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120))
    role = db.Column(db.String(120))
    location = db.Column(db.String(120))
    status = db.Column(db.String(50))
    application_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
