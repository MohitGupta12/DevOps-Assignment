
# Endpoint for CNPG database
To create a Public Endpoint for our CNPG database we have to make a Load balancing service that has our database pods as its endpoint, then we can make it public using Ingress controller.

### **Service to expose our database**
We can create a simple Load balancing service on port 5432 cause of our Postgres database
```cnpg-svc.yml
apiVersion: v1
kind: Service
metadata:
  name: cnpg-svc
spec:
  selector:
    cnpg.io/cluster: database-cluster
  ports:
  - protocol: TCP
    port: 5432
    targetPort: 5432
  type: LoadBalancer
```

```
kubectl apply -f cnpg-svc
```

*NOTE: we can use different selector based on our preference or we could also add custom labels to pods and use that as selector, this selector works in my case* 
### **Create Ingress Resource:** 

Now to expose that cnpg-svc service to Public we have to create a ingress that will allow external public request to our service

- https://cnpg.db.com/cnpg --> Ingress --> k8s service --> CNPG Pods

``` ingress.yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: db-ingress
  namespace: database
spec:
  ingressClassName: nginx
  rules:
  - host: db.com
    http:
      paths:
      - path: /cnpg
        pathType: Prefix
        backend:
          service:
	        name: cnpg-svc
            port: 
              number:5432 
```

```
kubectl apply -f ingress.yaml 
```

*Note: Here we are using `db.com` as our domain name to test this we can redirect it to our local host, for this we could just add our localhost ip and domain name to our `/etc/hosts`* 

### **Deploy Ingress Controller**

To make our Ingress resource work we have to use a ingress controller, there are many different flavors of ingress controller but we will be using Nginx Ingress controller

**Installation :**
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm search repo ingress-nginx --versions
```

**Deployment :** 

To Deploy our controller we will be using manifest files and we will keep track of those files as change in our controller can be a become bottleneck for our error 
{ This File tracking system is not useful in our case, but we are still doing it to maintain the Best Practices }

So first we will need to get chart and controller version compatible with our distribution 
We can install and see all the nginx controller version with these commands
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm search repo ingress-nginx --versions
```

Once we get them we can make them `env` variables to easily track them
```
CHART_VERSION="4.4.0"
APP_VERSION="1.5.1"
```

Now to create our manifest file we can use helm template command and redirect them to a file in our manifest folder
```
mkdir ./kubernetes/ingress/controller/nginx/manifests/

helm template ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--version ${CHART_VERSION} \
--namespace ingress-nginx \
> ./ingress/controller/nginx/manifests/nginx-ingress.${APP_VERSION}.yaml
```


Now Finally we can use simple apply command with our manifest file to create our controller
```
kubectl create namespace ingress-nginx
kubectl apply -f ./ingress/controller/nginx/manifests/nginx-ingress.${APP_VERSION}.yaml
```

Once controller is in status is completed we can use the public domain to access our CNPG database