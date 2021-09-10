### Linux的上传和下载

#### 1.scp

```shell
#把本地的source.txt文件拷贝到192.168.0.10机器上的/home/work目录下
scp /home/work/source.txt work@192.168.0.10:/home/work/

#把192.168.0.10机器上的source.txt文件拷贝到本地的/home/work目录下
scp work@192.168.0.10:/home/work/source.txt /home/work/  

#把192.168.0.10机器上的source.txt文件拷贝到192.168.0.11机器的/home/work目录下
scp work@192.168.0.10:/home/work/source.txt work@192.168.0.11:/home/work/  

scp -r /home/work/sourcedir work@192.168.0.10:/home/work/   #拷贝文件夹，加-r参数
```

#### 2.rz & sz

```shell
yum install lrzsz

# 下载文件到本地
sz /home/app/hs_err_pid32230.log

# 上传文件到服务器
rz
```

