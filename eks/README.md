## Kubernetes EKS 

The files in this folder are intended to be run on the kubernetes cluster once you've followed the steps to get the EKS
cluster up and running. 

The order of operations should be followed in the order below: 

1. Update kubeconfig
2. Create the namespace
3. Create the secrets we need for our deployments
4. Bring up the postgres database
5. Bring up the batch job
6. Bring up the api deployment

### Update kubeconfig

In order to be able to use kubectl command line, you'll need to update your local kubeconfig file from AWS using the 
aws cli. 

`aws eks update-kubeconfig --region us-west-1 --name lwt-eks-dev`

### Create Namespace

`kubectl apply -f ./namespace.yaml`

### Apply secrets for postgres

`kubectl apply -f ./secrets.yaml`

### Create the database

`kubectl apply -f ./postgres/postgres.yaml`

### Create the batch job once the database is up and stable

`kubectl apply -f ./cronjob/cron.yaml`

### Create the api

`kubectl apply -f ./api/api-deployment.yaml`

## Get the external IP of the API and/or other services
If not running a load balancer, to find where the API is running externally (on the node), you'll need the nodeport's IP address. To get it, 
run: 

1. Get the port where the nodeport is mapped:
`kubectl get services -n lwtdemo`

You should see something like this that shows you the port is mpaped to the nodeport's 31092 port

```buildoutcfg
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
fastapi-svc        NodePort    10.100.37.137    <none>        8000:31092/TCP   8d
postgres-service   ClusterIP   10.100.255.135   <none>        5432/TCP         18h
```

2.  Then find the node's external IP

`kubectl get node -o wide`

```buildoutcfg
NAME                                         STATUS   ROLES    AGE   VERSION                INTERNAL-IP    EXTERNAL-IP     OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
ip-123-45-6-789.us-west-1.compute.internal   Ready    <none>   8d    v1.24.11-eks-a59e1f0   123.45.6.789   55.55.555.555   Amazon Linux 2   5.10.178-162.673.amzn2.x86_64   containerd://1.6.19
```
3. The resulting address should be reachable externally: `http://55.55.555.555:31092/docs#/`


## Running direct SQL on the DB

First, exec into the pod itself (replace with the actual postgres pod name)
```
kubectl exec --stdin --tty pod-name-db -n lwtdemo -- /bin/bash
```

Then run this to start the psql command line replacing your username
``` 
psql -d lwtdemo -U username
```

