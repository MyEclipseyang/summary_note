## 使用阿里巴巴的Arthas

### 1.练习1 实现热编译

#### 1.1启动

> Arthas java -jar arthas-boot.jar
>
> 指定连接一个Java进程

#### 1.2找到指定类并查看类的信息

> ```shell
> sc *LoginCon*
> sc -d edp.davinci.controller.LoginController
> ```

#### 1.3反编译类并输出到本地

> ```shell
> jad --source-only com.example.demo.arthas.user.UserController > /tmp/UserController.java
> ```

#### 1.4修改文件

> ```shell
> vim /tmp/UserController.java
> ```

#### 1.5重新编译.java文件

>  mc -c 2dda6444  /temp/LoginController.java    -d /temp/

#### 1.6重新加载.class文件

>  mc -c 2dda6444  /temp/LoginController.java    -d /temp/  2dda6444 是该类的类加载器的hash值
>
> 