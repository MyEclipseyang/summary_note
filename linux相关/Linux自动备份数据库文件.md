### 自动备份数据库文件

参考自：https://www.cnblogs.com/kesimin/p/11138230.html

#### 1.创建备份目录

> 我是以root身份登陆的

```shell
mkdir -p /bak/mysqlbak
```

#### 2.编写运行脚本

> 注意：mysql5.x不允许显式的输入数据库密码，所以这里需要额外的配置
>
> vim /etc/my.conf,添加

```shell
[mysqldump]
user=你的mysql用户名
password=你的mysql密码
```
<!-- more -->

```shell
vim /usr/sbin/bakmysql.sh
```

```shell
#!/bin/bash
#NAME:bakmysql.sh
#This is a ShellScript For Auto DB Backup And Delete Old Backup
#
backupdir=/bak/mysqlbak
database_name=bugtext
time=` date +%Y%m%d%H `
/usr/bin/mysqldump $database_name| gzip > $backupdir/$database_name$time.sql.gz
#
find $backupdir -name $database_name"*.sql.gz"  -type f -mtime +7 -exec rm '{} \;' > /dev/null 2>&1

```

- `backupdir` mysql备份地址
- `time=` date +%Y%m%d%H ``也可以写为`time="$(date +"%Y%m%d$H")"`其中```符号是TAB键上面的符号，不是ENTER左边的'符号，还有date后要有一个空格。
- `database_name` 要备份的数据库的名
- `type f` 表示查找普通类型的文件，f表示普通文件。
- `mtime +7` 按照文件的更改时间来查找文件，+5表示文件更改时间距现在7天以前；如果是 -mmin +5 表示文件更改时间距现在5分钟以前。
- `exec rm {} \` 表示执行一段shell命令，exec选项后面跟随着所要执行的命令或脚本，然后是一对儿{}，一个空格和一个，最后是一个分号。
- `/dev/null 2>&1` 把标准出错重定向到标准输出，然后扔到/DEV/NULL下面去。通俗的说，就是把所有标准输出和标准出错都扔到垃圾桶里面；其中的& 表示让该命令在后台执行。

#### 3.为脚本添加执行权限

chmod +x /user/sbin/bakmysql.sh

#### 4.设置crontab定时执行
> 编辑`crontab`文件，一般在`/etc`下
```shell
00 3 * * * root /usr/sbin/bakmysql.sh
#表示每天3点00分执行备份
```

> 注：crontab配置文件格式如下：
> 分　时　日　月　周　 命令

#### 5.重启crontab

systemctl crontab.service restart

#### 6.附录

> 在第五步中博主写的是：/etc/rc.d/init.d/crond restart ，执行后发现提示找不到路径
>
> 后来发现执行路径下有一个文档：README
>
> 你是否在寻找 /etc/rc.d/init.d目录下的启动启动脚本？他们已经没了，接下来向你解释发生了什么。以前的脚本文件已经本地的服务文件所代替。服务文件提供与init脚本非常相似的功能。利用服务文件只需调用“systemctl”，它将输出所有当前正在运行服务（和其他单元）。使用“systemctllist-unit-files”以获取所有已知单元文件的列表，包括停下来的，未启用的，隐藏的。使用“systemctl startfoobar.service”和“systemctl stop foobar.service”分别启动或停止服务。详情请参阅systemctl(1)
>
> 注意以前的启动脚本依然在系统中工作，一个启动脚本例如/etc/rc.d/init.d/footbar在系统中肯定会有一个footbar.service

> 原文：
>
> You are looking for the traditional init scripts in /etc/rc.d/init.d,and they are gone?Here's an explanation on what's going on:
>
> You are running a systemd-based OS where traditional init scripts havebeen replaced by native systemd services files. Service files providevery similar functionality to init scripts. To make use of servicefiles simply invoke "systemctl", which will output a list of allcurrently running services (and other units). Use "systemctllist-unit-files" to get a listing of all known unit files, includingstopped, disabled and masked ones. Use "systemctl startfoobar.service" and "systemctl stop foobar.service" to start or stop aservice, respectively. For further details, please refer to systemctl(1).
>
> Note that traditional init scripts continue to function on a systemd system. An init script /etc/rc.d/init.d/foobar is implicitly mapped into a service unit foobar.service during system initialization.
>
> Thank you!
>
> Further reading: