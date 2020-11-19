### linux 设置中文版man手册

#### 下载中文man包

wget https://src.fedoraproject.org/repo/pkgs/man-pages-zh-CN/manpages-zh-1.5.2.tar.bz2/cab232c7bb49b214c2f7ee44f7f35900/manpages-zh-1.5.2.tar.bz2

#### 解压并安装

```shell
yum install bzip2
tar jxvf  manpages-zh-1.5.2.tar.bz2
cd manpages-zh-1.5.2
./configure --disable-zhtw #默认安装 
make && make install
```

#### 新建cman命令作为中文查询

```shell
cd ~
vi .bash_profile
echo "alias cman='man -M /usr/local/share/man/zh_CN'" >> .bash_profile
source .bash_profile #更新bash_profile 使其生效
```

