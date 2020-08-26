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

#### 6.退出容器

> 1. 退出不关闭容器：Ctrl + P + Q
> 2. 退出并关闭容器：exit

#### 7.在本机和容器之间传输文件

> 本机到容器  docker cp  /home/zyy/a.txt  容器id:/home/zs
>
> 容器到本机 docker cp  容器id:/home/zs   /home/zyy/a.txt