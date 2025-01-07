### Deploying CloudNativePG
Firstly to install CNPG you should have "Helm" install on your server node,
you can check by using

```
helm version
```

**Install Helm:**
In my case, it was not installed so i used these commands to install helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh
``````

**Add CloudNativePG Helm Repository:**
To deploy CNPG via charts we have to first add its repo to my node  
```
helm repo add cnpg https://cloudnative-pg.github.io/charts
```

**Deploy CloudNativePG:**
Then we can simply deploy it, usually it's recommended to make a namespace for it
```
helm install cnpg cloudnativepg/cloudnativepg
helm upgrade --install database --namespace database --create-namespace cnpg/cluster
```
