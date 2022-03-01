## 除G1和Parallel的分代

<img src="https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/img/jsgct_dt_001_armgnt_gn.png" alt="Description of Figure 3-2 follows" style="zoom:150%;" />

初始化时，多余的内存被虚拟分配并没有占用实际的物理内存，只有在需要的时候才会分配物理内存。所有分配的内存被划分为年轻代和年老代。年轻代由Eden区和survivor区组成，空着的那一个survivor区是从Eden区存活对象的目的地，另一个则是下次回收完存活对象的目的地。在两个survivor区来回移动的过程中，有些移动次数较多的对象会被移动到年老代。

#### 1.垃圾回收状况查看

> 启动参数 -verbose:gc

```
[GC 325407K->83000K(776768K), 0.2300771 secs]
[GC 325816K->83372K(776768K), 0.2454258 secs]
[Full GC 267628K->83769K(776768K), 1.8479984 secs]
```

两次minor GC和一次major GC，325407K （垃圾回收前的存活对象大小），83000K（回收后的存活对象大小）

776768K（survivor区可用的内存大小）

>  -XX:+PrintGCDetails

```
[GC [DefNew: 64575K->959K(64576K), 0.0457646 secs] 196016K->133633K(261184K), 0.0459067 secs]
```

DefNew代表年轻代的回收情况，后面代表整体的回收情况，数值意义如上。

> ```
> -XX:+PrintGCDetails
> ```

```
111.042: [GC 111.042: [DefNew: 8128K->8128K(8128K), 0.0000505 secs]111.042: [Tenured: 18154K->2311K(24576K), 0.1290354 secs] 26282K->2311K(32704K), 0.1293306 secs]
```

这次返回多了时间戳，更方便看出垃圾回收的频率，Tenured代表年老代

#### 2.分代大小设置

<img src="https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/img/jsgct_dt_006_prm_gn_sz.png" alt="Description of Figure 4-1 follows" style="zoom:150%;" />

-Xmx设置总可用内存大小，如果-Xms设置的大小小于最大值，Xmx - Xms的值将会给Virtual区，注意该区并不占用实际的物理内存，只是在虚拟机需要内存时提供空间（Virtual区空间将会减少）。

> 以下描述与Parallel无关

一般情况下，virtual区容量会变化以此来保证空闲区大小保持在一个具体的范围内，这个范围由以下参数控制

| Parameter        | Default Value |
| ---------------- | ------------- |
| MinHeapFreeRatio | 40            |
| MaxHeapFreeRatio | 70            |
| -Xms             | 6656k         |
| -Xmx             | calculated    |

如果空闲内存大小小于40%，分代区将会扩展以维持在40%，如果大于70%空闲区将会收缩。