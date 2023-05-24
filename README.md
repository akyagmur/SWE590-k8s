# SWE590 CLOUD COMPUTING APPLICATIONS TERM PROJECT

## Zulip Chat App Kubernetes Deployment

- Lami Kaan Kosesoy
- Ali Kenan Yagmur

# Installation, Configuration and Deployment

### 1. Install Docker and Kubernetes on Ubuntu Server

Install docker and kubernetes on your master and worker nodes. You can use the following commands to install docker and kubernetes on your nodes.

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