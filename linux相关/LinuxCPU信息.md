### LinuxCPU信息

#### ㈠ 概念

#####       ① 物理CPU  

​       实际Server中插槽上的CPU个数
​       物理cpu数量，可以数不重复的 physical id 有几个      

#####       ② 逻辑CPU      

​       Linux用户对 /proc/cpuinfo 这个文件肯定不陌生. 它是用来存储cpu硬件信息的
​       信息内容分别列出了processor 0 – n 的规格。这里需要注意，如果你认为n就是真实的cpu数的话, 就大错特错了
​       一般情况，我们认为一颗cpu可以有多核，加上intel的超线程技术(HT), 可以在逻辑上再分一倍数量的cpu core出来
​       逻辑CPU数量=物理cpu数量 x cpu cores 这个规格值 x 2(如果支持并开启ht)
​       备注一下：Linux下top查看的CPU也是逻辑CPU个数       

#####       ③ CPU核数     

​       一块CPU上面能处理数据的芯片组的数量、比如现在的i5 760,是双核心四线程的CPU、而 i5 2250 是四核心四线程的CPU       
​       一般来说，物理CPU个数×每颗核数就应该等于逻辑CPU的个数，如果不相等的话，则表示服务器的CPU支持超线程技术   

#### ㈡ 查看CPU信息    

​     vendor id    如果处理器为英特尔处理器，则字符串是 GenuineIntel。
​     processor   包括这一逻辑处理器的唯一标识符。
​     physical id  包括每个物理封装的唯一标识符。
​     core id         保存每个内核的唯一标识符。
​     siblings        列出了位于相同物理封装中的逻辑处理器的数量。
​     cpu cores    包含位于相同物理封装中的内核数量。

1. 拥有相同 physical id 的所有逻辑处理器共享同一个物理插座，每个 physical id 代表一个唯一的物理封装。

2. Siblings 表示位于这一物理封装上的逻辑处理器的数量，它们可能支持也可能不支持超线程（HT）技术。
3. 每个 core id 均代表一个唯一的处理器内核，所有带有相同 core id 的逻辑处理器均位于同一个处理器内核上。简单的说：“siblings”指的是一个物理CPU有几个逻辑CPU，”cpu cores“指的是一个物理CPU有几个核。
4. 如果有一个以上逻辑处理器拥有相同的 core id 和 physical id，则说明系统支持超线程（HT）技术。
5. 如果有两个或两个以上的逻辑处理器拥有相同的 physical id，但是 core id不同，则说明这是一个多内核处理器。cpu cores条目也可以表示是否支持多内核。

#### ㈢ 下面举例说明

#####     ① 查看物理CPU的个数

```shell
cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l 
2
```

#####     ② 查看逻辑CPU的个数

```shell
cat /proc/cpuinfo |grep "processor"|wc -l 
24
```

#####     ③ 查看CPU是几核

```shell
cat /proc/cpuinfo |grep "cores"|uniq 
6
```

 我这里应该是2个CPU,每个CPU有6个core,应该是Intel的CPU,支持超线程,所以显示24 

