# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application on:
EXPOSE 8080

# Run the application
# CMD ["python", "rescue_interactive.py"]
CMD ["python", "flask_web_app.py"]