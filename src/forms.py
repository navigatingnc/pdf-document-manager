from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProjectForm(FlaskForm):
    """Form for creating and editing projects"""
    project_name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    project_number = StringField('Project Number', validators=[DataRequired(), Length(max=50)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    client_name = StringField('Client Name', validators=[Optional(), Length(max=100)])
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Project')

class DocumentUploadForm(FlaskForm):
    """Form for uploading PDF documents"""
    file_type = StringField('File Type', validators=[DataRequired()])
    files = MultipleFileField('PDF Files', validators=[
        FileRequired('Please select at least one file'),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    submit = SubmitField('Upload Files')
