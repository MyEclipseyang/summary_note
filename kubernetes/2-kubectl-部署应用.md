### kubectl-部署应用

#### 1.kubectl basics

> kubectl

> kubectl version

> kubectl get nodes
>
> kubectl get nodes --help

#### 2.Deploy our app

 We need to provide the deployment name and app image location (include the full repository url for images hosted outside Docker hub).

> kubectl create deployment
>
> kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1

The command lead to:

- searched for a suitable node where an instance of the application could be run
- scheduled the application to run on that Node
- configured the cluster to reschedule the instance on a new Node when needed

> kubectl get deployment

Then we see that there are some deployments running a single instance of your app. The instance is running inside a Docker container on your node.

#### 3.View our app

Pods that are running inside Kubernetes are running on a private, isolated network. By default they are visible from other pods and services within the same kubernetes cluster, but not outside that network. When we use `kubectl`, we're interacting through an API endpoint to communicate with our application.

The `kubectl` command can create a proxy that will forward communications into the cluster-wide, private network. The proxy can be terminated by pressing control-C and won't show any output while its running.

> kubectl proxy

We now have a connection between our host (the online terminal) and the Kubernetes cluster. The proxy enables direct access to the API from these terminals.

You can see all those APIs hosted through the proxy endpoint. For example, we can query the version directly through the API using the `curl` command:

```shell
curl http://localhost:8001/version
```

The API server will automatically create an endpoint for each pod, based on the pod name, that is also accessible through the proxy.

First we need to get the Pod name, and we'll store in the environment variable POD_NAME:

```shell
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
```

