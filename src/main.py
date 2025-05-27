import os
import sys
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Set up the application path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-pdf-manager')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdf_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize database
from src.models import db
db.init_app(app)

# Import models
from src.models.models import Project, Document

# Import forms
from src.forms import ProjectForm, DocumentUploadForm

# Import routes
from src.routes.project_routes import project_bp
from src.routes.document_routes import document_bp

# Register blueprints
app.register_blueprint(project_bp)
app.register_blueprint(document_bp)

@app.route('/')
def index():
    """Home page route"""
    return redirect(url_for('project.list_projects'))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
