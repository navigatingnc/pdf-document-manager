from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.utils import secure_filename
import os
from src.models import db
from src.models.models import Document, Project
from src.forms import DocumentUploadForm

document_bp = Blueprint('document', __name__, url_prefix='/documents')

@document_bp.route('/upload/<int:project_id>', methods=['GET', 'POST'])
def upload_documents(project_id):
    """Upload documents for a project"""
    project = Project.query.get_or_404(project_id)
    form = DocumentUploadForm()
    
    if form.validate_on_submit():
        file_type = form.file_type.data
        
        if file_type not in ['plan', 'specification']:
            flash('Invalid file type. Must be "plan" or "specification".', 'danger')
            return redirect(request.url)
        
        # Determine the target directory based on file type
        from src.main import app
        project_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'projects/{project_id}')
        target_dir = os.path.join(project_dir, 'plans' if file_type == 'plan' else 'specs')
        
        # Ensure directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        # Process each uploaded file
        files = request.files.getlist('files')
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(target_dir, filename)
                
                # Save the file
                file.save(file_path)
                
                # Create document record in database
                document = Document(
                    project_id=project_id,
                    file_name=filename,
                    file_path=file_path,
                    file_type=file_type
                )
                db.session.add(document)
        
        db.session.commit()
        flash(f'{len(files)} document(s) uploaded successfully!', 'success')
        return redirect(url_for('project.view_project', project_id=project_id))
    
    return render_template('documents/upload.html', form=form, project=project)

@document_bp.route('/<int:document_id>')
def view_document(document_id):
    """View a specific document"""
    document = Document.query.get_or_404(document_id)
    return render_template('documents/view.html', document=document)

@document_bp.route('/<int:document_id>/delete', methods=['POST'])
def delete_document(document_id):
    """Delete a document"""
    document = Document.query.get_or_404(document_id)
    project_id = document.project_id
    
    # Delete the file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete the database record
    db.session.delete(document)
    db.session.commit()
    
    flash('Document deleted successfully!', 'success')
    return redirect(url_for('project.view_project', project_id=project_id))

@document_bp.route('/api/upload/<int:project_id>', methods=['POST'])
def api_upload_documents(project_id):
    """API endpoint for uploading documents via drag-and-drop"""
    project = Project.query.get_or_404(project_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    file_type = request.form.get('file_type')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file_type not in ['plan', 'specification']:
        return jsonify({'error': 'Invalid file type. Must be "plan" or "specification".'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        
        # Determine the target directory based on file type
        from src.main import app
        project_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'projects/{project_id}')
        target_dir = os.path.join(project_dir, 'plans' if file_type == 'plan' else 'specs')
        
        # Ensure directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        file_path = os.path.join(target_dir, filename)
        
        # Save the file
        file.save(file_path)
        
        # Create document record in database
        document = Document(
            project_id=project_id,
            file_name=filename,
            file_path=file_path,
            file_type=file_type
        )
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'document_id': document.id,
            'file_name': document.file_name,
            'file_type': document.file_type
        }), 200
    
    return jsonify({'error': 'Invalid file format. Only PDF files are allowed.'}), 400
