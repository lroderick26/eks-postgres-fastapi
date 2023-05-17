## Kubernetes EKS 

## Update kubeconfig

`aws eks update-kubeconfig --region us-west-1 --name lwt-eks-dev`

### Create Namespace

`kubectl apply -f ./namespace.yaml`

## Apply secrets for postgres

`kubectl apply -f ./secrets.yaml`

## Create the database

