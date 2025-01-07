
**Service to expose our database**
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

**Install NGINX Ingress Controller:**
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm search repo ingress-nginx --versions
```

**Deploy Nginx Ingress Controller**
```
CHART_VERSION="4.4.0"
APP_VERSION="1.5.1"

mkdir ./kubernetes/ingress/controller/nginx/manifests/

helm template ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--version ${CHART_VERSION} \
--namespace ingress-nginx \
> ./ingress/controller/nginx/manifests/nginx-ingress.${APP_VERSION}.yaml

kubectl create namespace ingress-nginx
kubectl apply -f ./ingress/controller/nginx/manifests/nginx-ingress.${APP_VERSION}.yaml

```


**Create Ingress Resource:**
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
      - backend:
          serviceName: cnpg-svc
          servicePort: 5432 
```

```
kubectl apply -f ingress.yaml 
```

