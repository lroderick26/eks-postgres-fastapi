## Kubernetes EKS 

## Update kubeconfig

`aws eks update-kubeconfig --region us-west-1 --name lwt-eks-dev`

### Create Namespace

`kubectl apply -f ./namespace.yaml`

## Set up ingress controller

`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/aws/deploy.yaml`

## Apply secrets for postgres

`kubectl apply -f ./secrets.yaml`

## Create the database

`kubectl apply -f ./postgres/postgres.yaml`

## Create the api

`kubectl apply -f ./api/api-deployment.yaml`