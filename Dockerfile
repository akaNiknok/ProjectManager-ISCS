# Use the official Python image as a base image
FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  # Prevents Python from writing .pyc files
ENV PYTHONUNBUFFERED=1         # Ensures output is shown in the Docker logs

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/
WORKDIR /app/ProjectManager

# Expose the port Django runs on (default is 8000)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]