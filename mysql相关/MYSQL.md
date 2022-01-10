### 高性能MYSQL

#### 大纲

##### 1.什么是索引？

为更快的对表数据访问而构建的数据存储结构

> B-tree indexes、Full-text search indexes、Hash indexes、R-tree indexes....

##### 2.索引的数据结构？

> Innodb: B+Tree

##### 2.Innodb和Myisam存储引擎的区别？

|                                        | **MyISAM**   | **InnoDB**       |
| -------------------------------------- | ------------ | ---------------- |
| B-tree indexes                         | Yes          | Yes              |
| Backup/point-in-time recovery (note 1) | Yes          | Yes              |
| Cluster database support               | No           | No               |
| Clustered indexes                      | No           | **Yes**          |
| Compressed data                        | Yes (note 1) | **Yes**          |
| Data caches                            | No           | **Yes**          |
| Encrypted data                         | Yes          | Yes              |
| Foreign key support                    | No           | **Yes**          |
| Full-text search indexes               | Yes          | **Yes (note 2)** |
| Geospatial data type support           | Yes          | Yes              |
| Geospatial indexing support            | Yes          | **Yes (note 3)** |
| Hash indexes                           | No           | **No (note 4)**  |
| Index caches                           | Yes          | Yes              |
| Locking granularity                    | Table        | **Row**          |
| MVCC                                   | No           | **Yes**          |
| Replication support (note 1)           | Yes          | Yes              |
| Storage limits                         | 256TB        | **64TB**         |
| T-tree indexes                         | No           | No               |
| Transactions                           | No           | **Yes**          |
| Update statistics for data dictionary  | Yes          | Yes              |

note1: Compressed MyISAM tables are supported only when using the compressed row format. Tables using the compressed row format with MyISAM are read only.

note2: Support for FULLTEXT indexes is available in MySQL 5.6 and later.

note3: Support for geospatial indexing is available in MySQL 5.7 and later.

**note4**: InnoDB utilizes hash indexes internally for its Adaptive Hash Index feature.

> Adaptive Hash Index: 由系统变量innodb-adaptive-hash-index控制，默认是开启，会缓存常访问行的索引页
>
> [MySQL :: MySQL 5.7 Reference Manual :: 14.5.3 Adaptive Hash Index](https://dev.mysql.com/doc/refman/5.7/en/innodb-adaptive-hash.html)

##### 3.什么是聚集索引非聚集索引?

##### 4.Innodb聚集索引和普通索引的索引差异？

##### 5.如何避免回表查询?什么是覆盖索引？

##### 6.B+ Tree索引和Hash索引区别？

哈希索引：

> （hash index）基于哈希表实现，只有精确匹配索引所有列的查询才有效(4)。对于每一行数据，存储引擎都会对所有的索引列计算一个哈希码（hash code），哈希码是一个较小的值，并且不同键值的 行计算出来的哈希码也不一样。哈希索引将所有的哈希码存储在索引 中，同时在哈希表中保存指向每个数据行的指针。

##### 7.为什么Innodb必须要有主键，并且推荐使用整型的自增主键？

##### 8.为什么非主键索引的叶子节点存储的是主键值？

#### 1.事务

一**组**原子性的SQL查询

#### 2.更好的选择数据类型

##### 2.1更小的通常更好

一般情况下，应该尽量使用可以正确存储数据的最小数据类型 。更小的数据类型通常更快，因为它们占用更少的磁盘、内存和 CPU缓存，并且处理时需要的CPU周期也更少。

##### 2.2简单就好

简单数据类型的操作通常需要更少的CPU周期。

##### 2.3尽量避免NULL

如果查询中包含可为NULL的列，对MySQL来说更难优化，因 为可为NULL的列使得索引、索引统计和值比较都更复杂。可为NULL 的列会使用更多的存储空间，在MySQL里也需要特殊处理。

通常把可为NULL的列改为NOT NULL带来的性能提升比较小，所 以（调优时）没有必要首先在现有schema中查找并修改掉这种情 况，除非确定这会导致问题。

当然也有例外，例如值得一提的是，InnoDB使用单独的位 （bit）存储NULL值，所以对于稀疏数据(4)有很好的空间效率。但这 一点不适用于MyISAM。

#### 3.数据类型

##### 3.1整数类型

|           |      可表示数的范围       |
| --------- | :-----------------------: |
| TINYINT   |  −2^（8−1）~ 2^（8−1）−1  |
| SMALLINT  | −2^（16−1）~ 2^（16−1）−1 |
| MEDIUMINT | −2^（24−1）~ 2^（24−1）−1 |
| INT       | −2^（32−1）~ 2^（32−1）−1 |
| BIGINT    | −2^（64−1）~ 2^（64−1）−1 |
| UNSIGNED  |           0~255           |

**NOTE**: MySQL可以为**整数类型**指定宽度，例如INT（11），对大多数应用 这是没有意义的：它不会限制值的合法范围，只是规定了MySQL的一 些交互工具（例如MySQL命令行客户端）用来显示字符的个数。对于 存储和计算来说，INT（1）和INT（20）是相同的。

##### 3.2实数类型

|         |                           占用空间                           |
| ------- | :----------------------------------------------------------: |
| FLOAT   |                           4个字节                            |
| DOUBLE  |                           8个字节                            |
| DECIMAL | 每9个数字占用4个字节,小数点占用一个字节（二进制字符串存储）例如：DECIMAL(18,2) 占用9个字节 |

#### 4.索引

> 想在一本书中找到某个特定主题，一般会先看 书的“索引”，找到对应的页码。在MySQL中，存储引擎用类似的方法使用索引，其先在索引中找到对应值，然后根据匹配的索引记录找到对应的数据行。

##### 4.1索引的类型

###### B-TREE

> https://blog.csdn.net/yin767833376/article/details/81511377

> B-Tree是为磁盘等外存储设备设计的一种平衡查找树
>
> 系统从磁盘读取数据到内存时是以磁盘块（block）为基本单位的，位于同一个磁盘块中的数据会被一次性读取出来，而不是需要什么取什么。
>
> InnoDB存储引擎中有页（Page）的概念，页是其磁盘管理的最小单位。而系统一个磁盘块的存储空间往往没有这么大，因此InnoDB每次申请磁盘空间时都会是若干地址连续磁盘块来达到页的大小16KB。InnoDB在把磁盘数据读入到磁盘时会以页为基本单位，在查询数据时如果一个页中的每条数据都能有助于定位数据记录的位置，这将会减少磁盘I/O次数，提高查询效率。

我们使用术语“B-Tree”(Balance Tree)，是因为MySQL在CREATE TABLE和其他语句中也使用该关键字，不过，底层的存储引擎也可能使用不同的存储结 构，即使其名字是BTREE，例如InnoDB使用的是B+Tree数据结构。

> B-Tree索引适用于全键值、键值范围或键前缀查找

```sql
CREATE TABLE People (
	last_name varchar(50) not null,
	first_name varchar(50) not null,
	birth date not null,
	gender enum('m', 'f') not null,
	key(last_name, first_name, dob)
); 
```

全值匹配

> 全值匹配指的是和索引中的所有列进行匹配，例如前面提到的 索引可用于查找姓名为Cuba Allen、出生于1960-01-01的人。

匹配最左前缀

> 前面提到的索引可用于查找所有姓为Allen的人，即只使用**索引的第一列**。

匹配列前缀

> 也可以只匹配某一列的值的开头部分。例如前面提到的索引可 用于查找所有以J开头的姓的人。这里也只使用了**索引的第一列**。

匹配范围值

> 例如前面提到的索引可用于查找姓在Allen和Barrymore之间的 人。这里也只使用了**索引的第一列**。

精确匹配某一列并范围匹配另外一列

> 前面提到的索引也可用于查找所有姓为Allen，并且名字是字 母K开头（比如Kim、Karl等）的人。即第一列last_name全匹配， 第二列frst_name范围匹配。

只访问索引的查询

> B-Tree通常可以支持“只访问索引的查询”，即查询只需要访问索引，而无须访问数据行。后面我们将单独讨论这种“覆盖索引”的 优化。

**NOTE:**

>  因为索引树中的节点是有序的，所以除了按值查找之外，索引还可 以用于查询中的ORDER BY操作
>
> 不能跳过索引中的列。
>
> 如果查询中有某个列的范围查询，则其右边所有列都无法使用索引 优化查找。

##### 4.2索引失效

如果查询中的列不是独立的，则MySQL就不会使用 索引。“独立的列”是指索引列不能是表达式的一部分，也不能是函数的 参数。

```sql
select * from table where age + 1 = 10
```

我们应该养 成简化WHERE条件的习惯，始终将索引列单独放在比较符号的一侧。

