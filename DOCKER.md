# Docker / docker-compose for Health_Risk_Predictor

This file explains how to build and run the project using Docker and docker-compose.

Summary
- Backend (Flask + SQLite + model) runs in a container and is exposed on host port 5001 (container internal port 5000).
- Frontend (React built and served by nginx) runs in a container and is exposed on host port 3001 (container internal port 80).
- The frontend is built with REACT_APP_API_URL pointing to `http://localhost:5001` by default (so it talks to the backend on the host port 5001).

Quick start (Docker Desktop required)

1. Build and start (from repository root):

   docker-compose up --build -d

2. Access the frontend: http://localhost:3001

3. API base URL: http://localhost:5001

Notes & tips
- The backend image runs `gunicorn` bound to port 5000 inside the container; docker-compose maps that to host port 5001 to avoid conflicts with your local 5000 instance.
- The frontend build embeds `REACT_APP_API_URL` at build time. By default `docker-compose.yml` sets it to `http://localhost:5001`. To change it:
  - Edit `docker-compose.yml` and change the `REACT_APP_API_URL` build arg for the `frontend` service, then rebuild (`docker-compose build frontend` and then `docker-compose up -d`).

Persisted data
- `./backend/health.db` is mounted into the backend container so your data persists across container restarts. The `./backend/ml` folder is mounted as well so you can iterate on the model file locally.

Stopping & removing
- Stop: `docker-compose down`
- Stop and remove images: `docker-compose down --rmi all --volumes`

If you want, I can:
- run and verify the containers on your machine now (I can start docker-compose and check endpoints), or
- add a small compose override file for development (mounting source code into containers for live reloading).

