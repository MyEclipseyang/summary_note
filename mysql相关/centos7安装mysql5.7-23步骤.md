切换目录

cd /usr

创建目录

mkdir mysql
cd mysql

下载 Mysql Yum

wget http://repo.mysql.com/mysql57-community-release-el7-8.noarch.rpm

安装 Yum

rpm -ivh mysql57-community-release-el7-8.noarch.rpm

安装 Mysql

yum install mysql-server

运行 Mysql

service mysqld start

获取初始密码

grep "password" /var/log/mysqld.log
#### 下面是返回的内容，密码也末尾
2018-08-21T08:06:46.998346Z 1 [Note] A temporary password is generated for root@localhost: y3h2rpgryw.E

修改密码
复制代码

### 使用临时密码登陆
mysql -u root -p

### 由于 5.7 处于安全考虑，不让设置简单密码，要先更改其密码机制
set global validate_password_policy=LOW;
### 设置密码长度
set global validate_password_length=6;
### 修改密码
SET PASSWORD = PASSWORD('111111');
ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
flush privileges;

复制代码
远程和本地访问

use mysql;
update user set host = '%' where user = 'root';
### 使配置生效
flush privileges;

设置字符集

### 登陆数据库后
set character_set_database=utf8;
flush privileges;

一些文件的存放目录
复制代码

### 配置文件
/etc/my.cnf
### 数据库文件目录
/var/lib/mysql
### 日志记录文件
/var/log/ mysqld.log
### 服务启动脚本
/usr/lib/systemd/system/mysqld.service
### socket文件
/var/run/mysqld/mysqld.pid