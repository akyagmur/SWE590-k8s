# SWE590 CLOUD COMPUTING APPLICATIONS TERM PROJECT

## Zulip Chat App Kubernetes Deployment

- Lami Kaan Kosesoy
- Ali Kenan Yagmur

The aim of this project is to deploy Zulip Chat App on Kubernetes.
The application is deployed on a Kubernetes cluster with 1 master and 2 worker nodes.
Currently, the application is up and running at https://k8s.uzmankaza.com.

# Installation, Configuration and Deployment

### 1. Install Docker and Kubernetes on Ubuntu Server

Install docker and kubernetes on your master and worker nodes. You can use the following commands:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold docker-ce kubelet kubeadm kubectl
```

### 2. Create Kubernetes Cluster

On your master node, run the following command to create a kubernetes cluster.

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Note down the kubeadm join command with the token and the master IP address. You will need this to join the worker nodes to the cluster.

Setup local kubeconfig:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Install a pod network (Flannel):

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

On each worker node, join the cluster:

```bash
sudo kubeadm join [master-ip]:6443 --token [token] --discovery-token-ca-cert-hash [hash]
```
Test if the nodes are joined to the cluster:

```bash
kubectl get nodes
```

### 3. Deploy Application

Save your Kubernetes configuration files (zulip.rc.yml and zulip-svc.yml) in the master node.

```bash
kubectl apply -f ./
```
Verify that the pods are running:

```bash
kubectl get pods
```

### 4. Verify Deployment

See the logs of the zulip pod:

```bash
kubectl describe pod [pod-name]
```

### 5. Setup Reverse Proxy via Nginx

Install nginx on the master node:

```bash
sudo apt-get install nginx
```

Install certbot:

```bash
sudo apt-get install certbot python-certbot-nginx
```

Obtain a certificate:

```bash
sudo certbot certonly -d site.com 
```
This will create a new directory in /etc/letsencrypt/live/site.com and store the certificate files in that directory.


Create a new nginx configuration file:

```bash
sudo nano /etc/nginx/conf.d/site.com.conf
```

Add the following configuration to the file:

```conf
server {
    listen 443 ssl;

    ssl_certificate /etc/letsencrypt/live/site.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/site.com/privkey.pem;

    location / {
        proxy_pass https://35.229.151.156:30443; # this ip changes every time I restart the vm
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the new configuration:

```bash
systemctl reload nginx
```

### 5. Debugging

If you have any problems with the deployment, you can delete the cluster and start over.

```bash
kubeadm reset
```

For debugging, you can use the following commands:


```bash
kubectl pods describe [pod-name]
```

```bash
kubectl logs [pod-name]
```

### 6. Accessing the Application Containers

You can access the application containers using the following command:

```bash
kubectl exec -it [pod-name] -- /bin/bash
```