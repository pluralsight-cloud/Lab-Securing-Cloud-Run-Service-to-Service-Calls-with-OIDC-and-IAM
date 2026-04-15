#!/bin/bash

PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
REPO=cloudrun-repo
IMAGE=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/app:latest

gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION || true


gcloud builds submit ./app --tag $IMAGE

echo "IMAGE=$IMAGE"
