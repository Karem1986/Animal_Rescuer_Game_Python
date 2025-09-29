# Use a Python base image
FROM python:slim-trixie

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Following container security best practices by creating a dedicated system user with no root access. This minimizes riskS.
RUN groupadd -r rescue && useradd --no-log-init -r -g rescue rescue
RUN chown -R rescue:rescue /app
USER rescue

# Expose the application on:
EXPOSE 8080

# Run the application
# CMD ["python", "rescue_interactive.py"]
CMD ["python", "app/index.py"]