

# **K3s Cluster Setup:**

### **Install K3s:**
This command will install k3s on your machine with hostname k3s-master-01 and as a server
```
curl -sfL https://get.k3s.io | sh -s - server --node-name k3s-master-01
```

### **Join Nodes to the Cluster:** 
To Add nodes to you cluster you will use these following commands to add agent and server nodes

- For Agent node
```
curl -sfL https://get.k3s.io | K3S_TOKEN K107f719c90198ea38021d2be4e03b9268eaf839c0530b84b5446b0a555399a2957::server:5452d9379bb78dcdd97431b9a067613e K3S_URL=https://172.31.23.9:6443 sh - 
```

- For Server node
```
curl -sfL https://get.k3s.io | K3S_TOKEN K107f719c90198ea38021d2be4e03b9268eaf839c0530b84b5446b0a555399a2957::server:5452d9379bb78dcdd97431b9a067613e K3S_URL=https://172.31.23.9:6443 sh -s - server
```



