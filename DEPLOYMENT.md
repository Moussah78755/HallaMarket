# Google Cloud Deployment Guide: HallaMarket

This guide outlines the steps to deploy the HallaMarket backend and dashboard to **Google Cloud Run**.

## Prerequisites
1. [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install) installed and configured.
2. A Google Cloud Project with billing enabled.
3. [Docker](https://www.docker.com/) installed (if building locally).

## 1. Setup Project
Initialize your project and enable the necessary services:
```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project [YOUR_PROJECT_ID]

# Enable Cloud Run and Artifact Registry APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## 2. Deploy Backend (FastAPI)
Navigate to the `backend` directory and deploy to Cloud Run:
```bash
cd backend

# Deploy using Cloud Build and Cloud Run
gcloud run deploy hallamarket-backend \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=[YOUR_GEMINI_API_KEY]
```
*Note: The backend URL will be provided after successful deployment. Update the dashboard API URL with this value.*

## 3. Deploy Dashboard (React/Vite)
Navigate to the `dashboard` directory and deploy:
```bash
cd ../dashboard

# Build and deploy the frontend container
gcloud run deploy hallamarket-dashboard \
    --source . \
    --region us-central1 \
    --allow-unauthenticated
```

## 4. Production Database Considerations
- **SQLite Warning**: The current deployment uses SQLite, which is stored inside the container. In Cloud Run, containers are stateless and will reset on restart.
- **Recommendation**: For production persistence, migrate the database to **Google Cloud SQL (PostgreSQL)** and update the `DATABASE_URL` in `backend/app/database.py`.

## 5. Security & Scaling
- **CORS**: Ensure your backend `main.py` is configured to allow the dashboard's production URL.
- **Autoscaling**: Cloud Run will automatically scale from 0 to N based on traffic, ensuring cost-efficiency during low-activity periods.
