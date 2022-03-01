### JVM

#### 1.查看java进程

```sh
[app@ZF-YDZFKF-MPOS-FRONT-2067e1 logs]$ jps
110960 Jps
5446 Bootstrap
```

#### 2.查看各年代大小与GC情况

```sh
[app@ZF-YDZFKF-MPOS-FRONT-2067e1 logs]$ jstat -gcutil 5446 1000
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   
  0.00   5.80  62.90  36.31  96.34  94.21     79    8.220     0    0.000    8.220
  0.00   5.80  62.90  36.31  96.34  94.21     79    8.220     0    0.000    8.220
  0.00   5.80  63.00  36.31  96.34  94.21     79    8.220     0    0.000    8.220
```

#### 3.查看各年代空间分配大小信息

```sh
[app@ZF-YDZFKF-MPOS-FRONT-2067e1 logs]$ jmap -heap 5446

Heap Configuration:
   MinHeapFreeRatio         = 40
   MaxHeapFreeRatio         = 70
   MaxHeapSize              = 2147483648 (2048.0MB)
   NewSize                  = 1073741824 (1024.0MB)
   MaxNewSize               = 1073741824 (1024.0MB)
   OldSize                  = 1073741824 (1024.0MB)
   NewRatio                 = 2
   SurvivorRatio            = 6
   MetaspaceSize            = 536870912 (512.0MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 536870912 (512.0MB)
   G1HeapRegionSize         = 0 (0.0MB)

Heap Usage:
New Generation (Eden + 1 Survivor Space):
   capacity = 939524096 (896.0MB)
   used     = 593332648 (565.8461074829102MB)
   free     = 346191448 (330.15389251708984MB)
   63.15246735300337% used
Eden Space:
   capacity = 805306368 (768.0MB)
   used     = 585550896 (558.4248504638672MB)
   free     = 219755472 (209.5751495361328MB)
   72.71156907081604% used
From Space:
   capacity = 134217728 (128.0MB)
   used     = 7781752 (7.421257019042969MB)
   free     = 126435976 (120.57874298095703MB)
   5.797857046127319% used
To Space:
   capacity = 134217728 (128.0MB)
   used     = 0 (0.0MB)
   free     = 134217728 (128.0MB)
   0.0% used

```

