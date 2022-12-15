## 创建systemctl任务

### 1.创建文件

```shell
/etc/systemd/system/brec.service
```

### 2，写入内容

```shell
[Unit]
Description=BililiveRecorder
After=network.target

[Service]
ExecStart=录播姬所在位置/BililiveRecorder.Cli run --bind "http://*:2356" --http-basic-user "用户名" --http-basic-pass "密码" "录播工作目录"

[Install]
WantedBy=multi-user.target
```

### 3.重载服务
> 每次修改了 brec.service 文件后都需要运行这个命令重载一次。

```shell
sudo systemctl daemon-reload
```

### 4.日志

```shell
sudo journalctl -u brec.service
```