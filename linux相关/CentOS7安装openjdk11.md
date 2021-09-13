### CentOS7安装openjdk11

#### 1.安装

```shell
yum install -y java-11-openjdk
```

#### 2.配置

```shell
which java
```

> /usr/bin/java

```shell
ls -lr /usr/bin/java
```

> lrwxrwxrwx. 1 root root 22 9月  12 23:12 /usr/bin/java -> /etc/alternatives/java

```shell
ls -lrt /etc/alternatives/java
```

> lrwxrwxrwx. 1 root root 64 9月  12 23:12 /etc/alternatives/java -> /usr/lib/jvm/java-11-openjdk-11.0.12.0.7-0.el7_9.x86_64/bin/java

#### 3.设置JAVA_HOME

```
vi /etc/profile
```

> export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.3.7-0.el7_6.aarch64
> export JRE_HOME=$JAVA_HOME/jre
> export CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
> export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH

```
source /etc/profile
```

