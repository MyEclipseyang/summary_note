### kubectl-了解应用

#### Kubernetes Pods

在模块 [2](https://kubernetes.io/zh/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/)创建 Deployment 时, Kubernetes 添加了一个 **Pod** 来托管你的应用实例。Pod 是 Kubernetes 抽象出来的，表示一组一个或多个应用程序容器（如 Docker），以及这些容器的一些共享资源。这些资源包括:

- 共享存储，当作卷
- 网络，作为唯一的集群 IP 地址
- 有关每个容器如何运行的信息，例如容器映像版本或要使用的特定端口。

Pod 为特定于应用程序的“逻辑主机”建模，并且可以包含相对紧耦合的不同应用容器。例如，Pod 可能既包含带有 Node.js 应用的容器，也包含另一个不同的容器，用于提供 Node.js 网络服务器要发布的数据。Pod 中的容器共享 IP 地址和端口，始终位于同一位置并且共同调度，并在同一工作节点上的共享上下文中运行。

Pod是 Kubernetes 平台上的原子单元。 当我们在 Kubernetes 上创建 Deployment 时，该 Deployment 会在其中创建包含容器的 Pod （而不是直接创建容器）。每个 Pod 都与调度它的工作节点绑定，并保持在那里直到终止（根据重启策略）或删除。 如果工作节点发生故障，则会在群集中的其他可用工作节点上调度相同的 Pod。

![img](kubectl-了解应用.assets/module_03_pods.svg)

#### 工作节点

一个 pod 总是运行在 **工作节点**。工作节点是 Kubernetes 中的参与计算的机器，可以是虚拟机或物理计算机，具体取决于集群。每个工作节点由主节点管理。工作节点可以有多个 pod ，Kubernetes 主节点会自动处理在群集中的工作节点上调度 pod 。 主节点的自动调度考量了每个工作节点上的可用资源。

每个 Kubernetes 工作节点至少运行:

- Kubelet，负责 Kubernetes 主节点和工作节点之间通信的过程; 它管理 Pod 和机器上运行的容器。
- 容器运行时（如 Docker），负责从仓库中提取容器镜像，解压缩容器以及运行应用程序。

<img src="kubectl-了解应用.assets/module_03_nodes.svg" alt="img"  />

### Explore your app

#### Check application configuration

et’s verify that the application we deployed in the previous scenario is running. We’ll use the `kubectl get` command and look for existing Pods:

```shell
kubectl get pods
```

Next, to view what containers are inside that Pod and what images are used to build those containers we run the `describe pods` command:

```shell
kubectl describe pods
```

We see here details about the Pod’s container: IP address, the ports used and a list of events related to the lifecycle of the Pod.

#### Show the app in the terminal

Recall that Pods are running in an isolated, private network - so we need to proxy access to them so we can debug and interact with them. To do this, we'll use the `kubectl proxy` command to run a proxy in a second terminal window.

```shell
kubectl proxy
```

Now again, we'll get the Pod name and query that pod directly through the proxy. To get the Pod name and store it in the POD_NAME environment variable:

```shell
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}') echo Name of the Pod: $POD_NAME
```

To see the output of our application, run a `curl` request.

```shell
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/proxy/
```

The url is the route to the API of the Pod.

#### View the container logs

Anything that the application would normally send to `STDOUT` becomes logs for the container within the Pod. We can retrieve these logs using the `kubectl logs` command:

```shell
kubectl logs $POD_NAME
```

*Note: We don’t need to specify the container name, because we only have one container inside the pod.*

#### Executing command on the container

We can execute commands directly on the container once the Pod is up and running. For this, we use the `exec` command and use the name of the Pod as a parameter. Let’s list the environment variables:

```shell
kubectl exec $POD_NAME env
```

Again, worth mentioning that the name of the container itself can be omitted since we only have a single container in the Pod.

Next let’s start a bash session in the Pod’s container:

```shell
kubectl exec -ti $POD_NAME bash
```

We have now an open console on the container where we run our NodeJS application. The source code of the app is in the server.js file:

```shell
cat server.js
```

You can check that the application is up by running a curl command:

```shell
curl localhost:8080
```

*Note: here we used localhost because we executed the command inside the NodeJS Pod. If you cannot connect to localhost:8080, check to make sure you have run the kubectl exec command and are launching the command from within the Pod*

To close your container connection type `exit`.