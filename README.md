# eks-workshop



## Steps

Create a cloud9 environment. 
Attach 'Instance Profile'  with Admin access to the Cloud9 EC2 instance.

Clone this git repository in Cloud9 IDE.

```bash
git clone https://github.com/anchit-nishant/eks-workshop.git
```

Create a docker image

```bash
cd ~/environment/eks-workshop/
docker build -t app .
docker images
```
Run the image locally

```bash
docker run -d -p 5000:5000 app
curl localhost:5000
```

Create ECR resource in AWS and push your image.

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ecr endpoint>

docker tag app:latest <ecr endpoint>/<repo Name>:latest

docker push <ecr endpoint>/<repo Name>:latest
```

Setup eksctl

```bash
aws --version

curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version

```

Install kubectl

```bash
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.9/2020-08-04/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin

```

Create EKS cluster through eksctl Cli

```bash
eksctl create cluster \
    --name <cluster-name> \
    --version 1.17 \
    --region <region> \
    --nodegroup-name linux-nodes \
    --nodes 3 \
    --nodes-min 1 \
    --nodes-max 4 \
    --ssh-access \
    --ssh-public-key <keypair name> \
    --managed

```

Edit the deployment.yaml file with the ECR image URI.


Apply the manifest file.
```bash
cd ~/environment/eks-workshop/
kubectl apply -f deployment.yaml

kubectl get pods -o wide

kubectl get svc

```

Test the application with the Network Load Balancer.


## Configuring Container insights.

Attach "CloudWatchAgentServerPolicy" policy to the instance profile attached to the Kubernetes worker nodes through console.


```bash
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/<cluster-name>/;s/{{region_name}}/<region>/" | kubectl apply -f -   

kubectl get pods --all-namespaces -o wide 

kubectl describe pod <pod-name> -n amazon-cloudwatch

kubectl logs <pod-name> -n amazon-cloudwatch

```

## Deleting resources.

Remove the extra policy added to the instance profile.

```bash
eksctl delete cluster <cluster name> -r <region>

```

Remove Cloud9 environment.