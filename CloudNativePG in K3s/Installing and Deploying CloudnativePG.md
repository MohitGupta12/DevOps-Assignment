
**Install Helm:**
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh
``````

**Add CloudNativePG Helm Repository:**
```
helm repo add cnpg https://cloudnative-pg.github.io/charts
```

**Deploy CloudNativePG:**
```
helm install cnpg cloudnativepg/cloudnativepg
helm upgrade --install database --namespace database --create-namespace cnpg/cluster
```
