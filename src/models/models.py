from datetime import datetime
from src.models import db

class Project(db.Model):
    """Project metadata model"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_number = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    client_name = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Document model
    documents = db.relationship('Document', backref='project', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Project {self.project_name}>'


class Document(db.Model):
    """Document files model"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'plan' or 'specification'
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.file_name}>'
