# Setup Guide

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)

## Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/ExoOnix/OnixDj.git
   cd OnixDj
   ```
2. **Setup environment variables**
   ```sh
   cp .envs/local/.env.example .envs/local/.env
   cp .envs/production/.env.example .envs/production/.env
   ```
3. **Run the development setup**
   ```sh
   make dev
   ```
   This will:
   - Start backend
   - Start frontend
   - Start mailhog
   - Start nginx
   - Start postgresql
4. **Access the application**
   Open [http://localhost](http://localhost)
## Running in Production
To run the application in production mode:
```sh
make prod
```
This will:
- Build all containers and serve them.

   
