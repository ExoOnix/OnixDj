# Use the official Python image as the base image
FROM python:3.13-slim


# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./backend/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (ensure this is after dependencies are installed)
COPY ./backend/ /app/

# Expose the application port for development
EXPOSE 8000

# Start the development server with auto-reload
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
