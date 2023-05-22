# Terraform for Infrastructure
We will use terraform to help us deploy a managed kubernetes cluster in AWS. 


## EKS
Relies heavily on the tutorial on the official Terraform website: https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks
 and based on the code from https://github.com/hashicorp/learn-terraform-provision-eks-cluster/tree/main

## VPC

## Prerequisites

You'll need a few accessories to make things work: 

* AWS account & the AWS CLI installed and configured 
* Terraform: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

i.e. via elevated terminal on PC `choco install terraform`

* `kubectl` command line

## Run

To run:

1. Check your AWS credentials in the AWS CLI and/or export your AWS credentials i.e. 

`export AWS_ACCESS_KEY_ID=123LKJS23`

`export AWS_SECRET_ACCESS_KEY=ksjfs&(823bjs`

2. Initialize terraform 

`terraform init`

3. Plan your terraform commands out to make sure things run

`terraform plan -out=./plan.zip`

4. Apply the plan if everything looks good

`terraform apply ./plan.zip`

## Costs and Destroy


Note: after changes are applied, you will be subject to costs in your AWS account. 


If needed, you can also destroy these resources using the same plan

`terraform destroy ./plan.zip`

## Post Deployment

1. Let's check via the AWS cli that the cluster is up
`aws eks describe-cluster --name lwt-eks-dev`

2. We'll want to work with the cluster directly to deploy applications like postgres and our APIs, so we need to make sure we have the right configurations to access it

`aws eks update-kubeconfig --name lwt-eks-dev --region us-west-1`

This updates your local kubeconfig allowing for easy access to your cluster

3. Let's take a look at our nodes and pods

`kubectl get nodes` --> gets your nodes

`kubectl get pods -o wide` --> gets all pods