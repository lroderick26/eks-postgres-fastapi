# EKS-Postgres-FastAPI

This project is a demo of how AWS EKS, PostgresDB and FastAPI can be used all together. It is part of a larger presentation that will be (or already has been) done at the Lesbians Who Tech & Allies Pride Summit 2023. 

## How to Use

Please read the readmes in each section before beginning. 

### Order of Operations

1. /terraform: Terraform to create your AWS Resources 
2. /eks: YAML files to create your deployments
3. /cronjob: To create your image for the batch job (the idea with the name is that it could eventually be turned into a cronjob)
4. /api: To create your image for the FastAPI 

## Technologies

### AWS
<br>
<img src="https://futurumresearch.com/wp-content/uploads/2020/01/aws-logo-1280x720.png" width="300">
<br>

* Sign up for an [acccount](https://portal.aws.amazon.com/billing/signup) <br>
* Download the [AWS CLI](https://aws.amazon.com/cli/)

### Terraform
<br>
<img src="https://creazilla-store.fra1.digitaloceanspaces.com/icons/3254444/terraform-icon-md.png" width="300">
<br>

* Download terraform from their [website](https://developer.hashicorp.com/terraform)

### PostgresDB
<br>
<img src="https://1000logos.net/wp-content/uploads/2020/08/PostgreSQL-Logo.jpg" width="300">
<br>

* Learn more about [PostgresDB](https://www.postgresql.org/docs/current/intro-whatis.html)

### Python
<br>
<img src="https://cdn.icon-icons.com/icons2/2699/PNG/512/python_vertical_logo_icon_168039.png" width="200">
<br>

### FastAPI
<br>
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="300">
<br>

* Learn more about [FastAPI here](https://fastapi.tiangolo.com/lo/) 
