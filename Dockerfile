FROM python:3.10.9

# Install cron and any other dependencies
RUN apt-get update

# Set working directory
WORKDIR /

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 8050

# Define the command to run the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "wsgi:app"]
