ARG NODE_VERSION=22.13.1

# Create build stage
FROM node:${NODE_VERSION}-slim AS build

RUN apt update && apt install -y openjdk-17-jdk


# Enable pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and pnpm-lock.yaml files to the working directory
COPY ./package.json /app/
COPY ./package-lock.json /app/

## Install dependencies
RUN npm install --shamefully-hoist

# Copy the rest of the application files to the working directory
COPY . ./
COPY ./api-schema.yml ./

RUN npm run genclient

# Build the application
RUN npm run build

# Create a new stage for the production image
FROM node:${NODE_VERSION}-slim

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
