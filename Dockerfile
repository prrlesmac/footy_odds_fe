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
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "app.py"]
