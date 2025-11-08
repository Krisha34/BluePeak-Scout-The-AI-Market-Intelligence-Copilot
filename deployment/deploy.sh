#!/bin/bash
# Deployment script for Google Cloud Platform

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
BACKEND_IMAGE="gcr.io/${PROJECT_ID}/bluepeak-backend"
FRONTEND_IMAGE="gcr.io/${PROJECT_ID}/bluepeak-frontend"

echo "======================================"
echo "BluePeak Compass - GCP Deployment"
echo "======================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed"
    exit 1
fi

# Set project
echo "Setting GCP project to ${PROJECT_ID}..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "Enabling required GCP APIs..."
gcloud services enable \
    run.googleapis.com \
    containerregistry.googleapis.com \
    secretmanager.googleapis.com \
    redis.googleapis.com

# Build and push backend
echo "Building backend Docker image..."
cd backend
docker build -t ${BACKEND_IMAGE}:latest .
docker push ${BACKEND_IMAGE}:latest
cd ..

# Build and push frontend
echo "Building frontend Docker image..."
cd frontend
docker build -t ${FRONTEND_IMAGE}:latest .
docker push ${FRONTEND_IMAGE}:latest
cd ..

# Create secrets (if not exists)
echo "Creating secrets..."
gcloud secrets create anthropic-api-key --data-file=- <<< "${ANTHROPIC_API_KEY}" || true
gcloud secrets create supabase-url --data-file=- <<< "${SUPABASE_URL}" || true
gcloud secrets create supabase-key --data-file=- <<< "${SUPABASE_KEY}" || true

# Deploy Redis instance
echo "Deploying Redis instance..."
gcloud redis instances create bluepeak-redis \
    --size=1 \
    --region=${REGION} \
    --redis-version=redis_7_0 \
    || echo "Redis instance already exists"

# Get Redis IP
REDIS_IP=$(gcloud redis instances describe bluepeak-redis --region=${REGION} --format="value(host)")

# Deploy backend to Cloud Run
echo "Deploying backend to Cloud Run..."
gcloud run deploy bluepeak-backend \
    --image ${BACKEND_IMAGE}:latest \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars "REDIS_HOST=${REDIS_IP}" \
    --set-secrets "ANTHROPIC_API_KEY=anthropic-api-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_KEY=supabase-key:latest" \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10

# Get backend URL
BACKEND_URL=$(gcloud run services describe bluepeak-backend --region=${REGION} --format="value(status.url)")

# Deploy frontend to Cloud Run
echo "Deploying frontend to Cloud Run..."
gcloud run deploy bluepeak-frontend \
    --image ${FRONTEND_IMAGE}:latest \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars "NEXT_PUBLIC_API_URL=${BACKEND_URL}/api/v1" \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 5

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe bluepeak-frontend --region=${REGION} --format="value(status.url)")

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo "Backend URL: ${BACKEND_URL}"
echo "Frontend URL: ${FRONTEND_URL}"
echo ""
echo "Access your application at: ${FRONTEND_URL}"
echo "======================================"
