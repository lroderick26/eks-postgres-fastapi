variable "region" {
    description = "AWS region we want to create resources in"
    default = "us-west-1"
}

variable "account_id" {
    description = "AWS account ID"
}

variable "env_name" {
    description = "Environment name"
    type = string
}

variable "domain_name" {
  type = string
}

variable "project_name" {
    description = "Project name"
    type = string
}


### VPC ###
variable "private_subnets" {
    description = "Private subnets"
}

variable "public_subnets" {
    description = "Public subnets"
}


variable "enable_nat_gateway"  {
}

variable "single_nat_gateway"  {
}

variable "enable_dns_hostnames"  {
}

### EKS ###
variable "eks_node_disk_size" {
}

variable "eks_node_desired_capacity" {
  description = "EKS Desired node Capacity for the Autoscaling Group"
}

variable "eks_node_min_capacity" {
  description = "Mininum capacity for worker nodes"
  type        = number
}

variable "eks_node_max_capacity" {
  description = "Max capacity for worker nodes"
  type        = number
}

variable "eks_node_instance_type" {
  description = "The EC2 instance type for the worker nodes"
  type        = string
}


variable "enable_storage_node" {
  description = "enable storage optimized node group"
  default     = false
  type        = bool
}