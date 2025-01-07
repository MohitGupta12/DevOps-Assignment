### The Assignment

Write a [FastAPI](https://fastapi.tiangolo.com/) server to create a highly available [K3s](https://k3s.io/) cluster on [Azure Virtual Machine](https://learn.microsoft.com/en-us/python/api/overview/azure/compute?view=azure-python) using just simple API endpoints. Deploy CloudNativePG in the K3s cluster using [Helm charts](https://helm.sh/).

#### Your task is to:

- Create a [K3s cluster with High Availability using Embedded etcd](https://docs.k3s.io/datastore/ha-embedded?_highlight=hig) for fault tolerance.
- Deploy the [CloudNativePG](https://github.com/cloudnative-pg/charts) to the K3s cluster using Helm charts. The PostgreSQL database should have an HTTP endpoint to connect.
- Configure DNS to point a custom domain name to the K3s cluster's load balancer IP.

