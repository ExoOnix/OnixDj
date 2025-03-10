# Use the official Python image as the base image
FROM python:3.13-slim AS schema_builder


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

RUN python3 manage.py spectacular --file ./api-schema.yml

# Create build stage
FROM node:22.13.1

RUN apt update && apt install -y openjdk-17-jdk

# Set the working directory
WORKDIR /app

COPY ./frontend ./
COPY --from=schema_builder /app/api-schema.yml /api-schema.yml


# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=3000

# Expose the application port
EXPOSE $PORT

# Start the development server
CMD sh -c "cp /api-schema.yml /app/api-schema.yml && npm i && npm run genclient && npm run dev"