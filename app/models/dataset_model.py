from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)

class datasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_entry = db.Column(db.DateTime, default =datetime.utcnow)
    date_dataset =db.Column(db.Date, nullable=False)
    description =db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.id