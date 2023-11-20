mysql_note

### 字符集设置
字符集有以下四个级别:
服务器级别
数据库级别
表级别
列级别

> 按需配置mysql的字符集，这里统一使用utf8
设置字符集的命令如下
```shell
## set variable_name=variable_value;
set character_set_server=utf8;
```
#### 查看字符集配置
```text
mysql> show variables like 'char%'; 
+--------------------------+---------------------------------------------------------+
| Variable_name            | Value                                                   |
+--------------------------+---------------------------------------------------------+
| character_set_client     | utf8                                                    |
| character_set_connection | utf8                                                    |
| character_set_database   | utf8                                                    |
| character_set_filesystem | binary                                                  |
| character_set_results    | utf8                                                    |
| character_set_server     | utf8                                                    |
| character_set_system     | utf8                                                    |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 5.7\share\charsets\ |
+--------------------------+---------------------------------------------------------+
```

#### 查看字符集比较规则
```text
mysql> show variables like 'collat%'; 
+----------------------+-----------------+
| Variable_name        | Value           |
+----------------------+-----------------+
| collation_connection | utf8_general_ci |
| collation_database   | utf8_general_ci |
| collation_server     | utf8_general_ci |
+----------------------+-----------------+
```
