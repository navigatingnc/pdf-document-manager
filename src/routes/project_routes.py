from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models import db
from src.models.models import Project
from src.forms import ProjectForm

project_bp = Blueprint('project', __name__, url_prefix='/projects')

@project_bp.route('/')
def list_projects():
    """List all projects"""
    projects = Project.query.all()
    return render_template('projects/list.html', projects=projects)

@project_bp.route('/new', methods=['GET', 'POST'])
def create_project():
    """Create a new project"""
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            project_name=form.project_name.data,
            project_number=form.project_number.data,
            location=form.location.data,
            client_name=form.client_name.data,
            start_date=form.start_date.data,
            description=form.description.data
        )
        db.session.add(project)
        db.session.commit()
        
        # Create project directories
        import os
        from src.main import app
        project_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'projects/{project.id}')
        plans_dir = os.path.join(project_dir, 'plans')
        specs_dir = os.path.join(project_dir, 'specs')
        
        os.makedirs(plans_dir, exist_ok=True)
        os.makedirs(specs_dir, exist_ok=True)
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('project.view_project', project_id=project.id))
    
    return render_template('projects/create.html', form=form)

@project_bp.route('/<int:project_id>')
def view_project(project_id):
    """View a specific project"""
    project = Project.query.get_or_404(project_id)
    return render_template('projects/view.html', project=project)

@project_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    """Edit a project"""
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.view_project', project_id=project.id))
    
    return render_template('projects/edit.html', form=form, project=project)

@project_bp.route('/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    # Delete project directories
    import os
    import shutil
    from src.main import app
    project_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'projects/{project_id}')
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('project.list_projects'))
