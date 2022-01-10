### jdk12

> Ubuntu 20

#### 1.编译需要装的依赖

> sudo apt-get install libfontconfig1-dev

> cd /${jdk源码目录}

#### 2.编译前准备

> bash configure --enable-debug --with-jvm-variants=server

#### 3.编译

> make images

#### 报错信息1

```shell
In function ‘char* strncpy(char*, const char*, size_t)’,
    inlined from ‘static jint Arguments::parse_each_vm_init_arg(const JavaVMInitArgs*, bool*, JVMFlag::Flags)’ at /home/hx/OpenJDK12/src/hotspot/share/runtime/arguments.cpp:2472:29:
/usr/include/x86_64-linux-gnu/bits/string_fortified.h:106:34: error: ‘char* __builtin_strncpy(char*, const char*, long unsigned int)’ output truncated before terminating nul copying as many bytes from a string as its length [-Werror=stringop-truncation]
  106 |   return __builtin___strncpy_chk (__dest, __src, __len, __bos (__dest));
   ... (rest of output omitted
```

> 直接百度，根据 https://segmentfault.com/a/1190000022669252的做法
>
> 引发错误的原因是这段[-Werror=stringop-truncation]，GCC在8.0之后的版本加入了 stringop truncation的验证警告，这里是因为出现了警告导致编译不通过，那就禁止 掉警告再进行编译。
>
> gcc -v
>
> gcc version 9.3.0 (Ubuntu 9.3.0-17ubuntu1~20.04) 

#### 解决1

```shell
# gcc版本问题。默认安装gcc9，重新安装gcc7
sudo apt-get install gcc-7 gcc-7-multilib g++-7 g++-7-multilib

ll /usr/bin/gcc*
ll /usr/bin/g++*

# 将gcc软连接到gcc7
rm -rf /usr/bin/gcc
ln -s /usr/bin/gcc-7 /usr/bin/gcc
rm -rf /usr/bin/g++
ln -s /usr/bin/g++-7 /usr/bin/g++

cd /${jdk源码目录}

make clean
make dist-clean

# 重新设置编译配置信息
bash configure --disable-warnings-as-errors --enable-debug --with-jvm-variants=server

make images
```

#### 报错信息2

> process terminaled (kill 9)
>
> 编译debug模式时需要的内存较多导致swap空间的内存不足

#### 解决2

> 编译release或增大swap空间内存
