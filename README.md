# PDF Document Manager

A locally hosted web application for managing PDF documents (plans and specifications) with project organization.

## Features

- Import PDF documents via drag-and-drop or file upload
- Organize documents by project with customizable metadata
- Automatic file organization in a structured folder system
- SQLite database integration for project and document tracking
- Responsive design that works on desktop and mobile devices
- Completely offline operation with no cloud dependencies

## Screenshots

![Project List](screenshots/project_list.png)
![Project Details](screenshots/project_details.png)
![Document Upload](screenshots/document_upload.png)

## Requirements

- Python 3.6+
- Flask and related packages (see requirements.txt)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### Option 1: Using virtualenv (recommended)

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/pdf-document-manager.git
   cd pdf-document-manager
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/main.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Option 2: Using Docker

1. Make sure Docker is installed on your system

2. Build and run the Docker container:
   ```
   docker build -t pdf-document-manager .
   docker run -p 5000:5000 -v pdf_data:/app/uploads pdf-document-manager
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Creating a New Project

1. Click "New Project" in the navigation bar
2. Fill in the project details (name, number, location, etc.)
3. Click "Save Project"

### Uploading Documents

1. Navigate to a project's detail page
2. Use the drag-and-drop area or click "Select Files" to choose PDF files
3. Select the document type (plan or specification)
4. Upload the files

### Viewing Documents

1. Navigate to a project's detail page
2. Click on the "Plans" or "Specifications" tab
3. Click "View" on any document to open it in the browser

## Project Structure

```
pdf_manager/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routes/
│   │   ├── project_routes.py
│   │   └── document_routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── projects/
│   │   │   ├── list.html
│   │   │   ├── create.html
│   │   │   ├── view.html
│   │   │   └── edit.html
│   │   └── documents/
│   │       ├── upload.html
│   │       └── view.html
│   ├── forms.py
│   └── main.py
├── uploads/
│   └── projects/
│       └── [project_id]/
│           ├── plans/
│           └── specs/
├── venv/
├── requirements.txt
├── README.md
└── pdf_manager.db
```

## Database Schema

### Projects Table
- id (INTEGER, primary key)
- project_name (TEXT, not null)
- project_number (TEXT, not null)
- location (TEXT)
- client_name (TEXT)
- start_date (DATE)
- description (TEXT)
- created_at (DATETIME)
- updated_at (DATETIME)

### Documents Table
- id (INTEGER, primary key)
- project_id (INTEGER, foreign key to projects.id)
- file_name (TEXT, not null)
- file_path (TEXT, not null)
- file_type (TEXT, not null) - 'plan' or 'specification'
- upload_date (DATETIME)

## Customization

### Changing Upload Directory

Edit the `UPLOAD_FOLDER` configuration in `src/main.py`:

```python
app.config['UPLOAD_FOLDER'] = '/path/to/your/upload/directory'
```

### Changing Maximum Upload Size

Edit the `MAX_CONTENT_LENGTH` configuration in `src/main.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## Troubleshooting

### Application Won't Start

- Ensure Python 3.6+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is already in use

### Upload Issues

- Verify the uploads directory has write permissions
- Check that the file size doesn't exceed the maximum limit (default: 16MB)
- Ensure the file is a valid PDF

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request
