# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install Celery
# RUN pip install celery
RUN python3 -m pip install celery

# Copy the Celery configuration file into the container
COPY ./file_upload_service/celery.py /app/

# Set the environment variable for the Celery command
ENV C_FORCE_ROOT=1


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container at /app
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define environment variables
ENV DJANGO_SETTINGS_MODULE=file_upload_service.settings

# Start the server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
