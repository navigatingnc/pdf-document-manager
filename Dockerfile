FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create upload directories
RUN mkdir -p uploads/projects

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "src/main.py"]
