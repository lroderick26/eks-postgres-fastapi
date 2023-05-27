# API Setup

## Requirements

### Credentials
Add your aws credentials into GitHub secrets in order to be able to access them within the container and to push the image to the ECR repository

### ECR Repository
You'll need to have created an ECR repository to push the image you create to

## Local Testing/Running
You can test things locally using docker compose. Be sure you've installed it locally before getting things going.

1. Create the network we're going to use for this as well as the initial data pipeline:

`docker network create my-network`

2. Run the docker-compose up command to bring up the api and the db

`docker-compose up -d --build`
