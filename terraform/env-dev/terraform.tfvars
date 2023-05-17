account_id = "781127853046"
env_name = "dev"
domain_name = ""
project_name = "lwt"

# VPC variables
private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
public_subnets  = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
cidr_block = "10.0.0.0/16"
enable_nat_gateway   = true
single_nat_gateway   = true
enable_dns_hostnames = true

# EKS variables

eks_node_disk_size         = 20
eks_node_desired_capacity  = "1"
eks_node_max_capacity      = "3"
eks_node_min_capacity      = "1"
eks_node_instance_type     = "t3.small"
eks_cluster_master_version = "1.25"
eks_add_ons                = "update"