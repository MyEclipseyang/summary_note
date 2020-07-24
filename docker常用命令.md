#### 1.拉取镜像

> docker pull daocloud.io/library/tomcat:8.5.15-jre8

![image-20200720092437923](C:\Users\zyy\AppData\Roaming\Typora\typora-user-images\image-20200720092437923.png)

#### 2.修改容器的名字

> docker tag imageId [name:tag]
>
> docker tag b8dfe9ade316 tomcat:8.5

![image-20200720092607591](C:\Users\zyy\AppData\Roaming\Typora\typora-user-images\image-20200720092607591.png)

#### 3.运行

> docker run -d -p 8080:8080 --name tomcat b8dfe9ade316 

#### 4.查看运行的容器

> docker ps

![image-20200720092756496](C:\Users\zyy\AppData\Roaming\Typora\typora-user-images\image-20200720092756496.png)

#### 5.进入容器

> docker exec -it containerId bash
>
> docker exec -it ba94d39bb1cd bash

![image-20200720092915500](C:\Users\zyy\AppData\Roaming\Typora\typora-user-images\image-20200720092915500.png)