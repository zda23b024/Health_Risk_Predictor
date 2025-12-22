# Health_Risk_Predictor

A simple health risk predictor web app (Flask backend + React frontend).

## Quick overview
- Backend: Flask app in `backend/` exposing REST endpoints for health logs, stats, and prediction (`/health/predict`).
- Frontend: React app in `frontend-react/` with simple pages for register/login, logging entries, and prediction.
- ML: A Random Forest model is used for risk prediction and stored at `backend/ml/random_forest.pkl`.

---

## Running locally (recommended for development)

1) Backend (local dev server)

- Open PowerShell in `backend/` and (optional) set up a virtual environment.
- Install dependencies:

  npm: none — backend uses pip

  ```powershell
  pip install -r requirements.txt
  ```

- Start the backend server (dev):

  ```powershell
  python -m app
  ```

  By default the backend listens on host port 5000. When running with Docker we map container port 5000 to host port 5001 to avoid conflicts.

2) Frontend (local dev server)

- Open PowerShell in `frontend-react/`.
- Install dependencies and start dev server:

  ```powershell
  npm install
  $env:REACT_APP_API_URL = "http://localhost:5001"  # point to backend port used by docker or your local backend
  $env:PORT = "3001"  # optional: change dev server port
  npm start
  ```

- Open the UI in your browser at: http://localhost:3001

---

## Running with Docker (production-like)

- The project includes a `docker-compose.yml` that maps the services to host ports you can open in your browser:

  - Frontend -> http://localhost:3001
  - Backend API -> http://localhost:5001

- To run with Docker (ensure Docker Desktop is running):

  ```powershell
  docker compose up --build -d
  ```

- Check status and logs:

  ```powershell
  docker compose ps
  docker compose logs -f backend
  docker compose logs -f frontend
  ```

---

## Endpoints of interest
- POST `/auth/register` — Register (returns token and user). Registration now auto-logs in (no email verification required).
- POST `/auth/login` — Login (username or email).
- POST `/health/predict` — Predict health risk (requires Bearer token). Payload: `{ weight, height, steps, water_intake, sleep_hours }`.

---

## Notes & troubleshooting
- If Docker fails to connect (Windows named pipe error), ensure Docker Desktop is running and healthy. Run `docker info` / `docker version` to confirm.
- The frontend dev server reads `REACT_APP_API_URL` at start time; set it to where your backend is listening (http://localhost:5001 when using the provided compose file).
- The backend uses a local SQLite DB at `backend/health.db`. The DB file is mounted into the container by `docker-compose` so data persists between runs.

---

## Video Presentation
-The video presentation is found in the drive link below 
-https://drive.google.com/drive/folders/1jaYCTagF0QM-m6wTJxdf3CMaU-vcCJVy?usp=sharing
