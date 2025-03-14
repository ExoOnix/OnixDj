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
FROM node:22.13.1-slim AS build

RUN apt update && apt install -y openjdk-17-jdk


# Enable pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and pnpm-lock.yaml files to the working directory
COPY ./frontend/package.json /app/
COPY ./frontend/package-lock.json /app/

## Install dependencies
RUN npm install --shamefully-hoist

# Copy the rest of the application files to the working directory
COPY ./frontend ./
COPY --from=schema_builder /app/api-schema.yml ./

RUN npm run genclient

# Build the application
RUN npm run build

# Create a new stage for the production image
FROM node:22.13.1-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the output from the build stage to the working directory
COPY --from=build /app/.output ./

# Define environment variables
ENV HOST=0.0.0.0 NODE_ENV=production
ENV NODE_ENV=production

# Expose the port the application will run on
EXPOSE 3000

# Start the application
CMD ["node","/app/server/index.mjs"]
