volatile引发的思考
> 基于jdk1.8

> https://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.3.1.4

按照官网的说法，加上volatile标识符后Java Memory Model能确保所有的线程获取变量时能拿到一致的值

官方给出的示例如下（反面案例，不使用volatile的下场
```java
public class VolatileRun {

    private static int p1 = 0, p2 = 0;

    private static void one() {
        p1++;
        p2++;
    }

    private static void two() {
        System.out.println(p1 + "--" + p2);
    }
    
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            while (true) {
                one();
            }
        });
        Thread t2 = new Thread(() -> {
            do {
                two();
            } while (p1 < 10000);

        });

        t1.start();
        t2.start();
        System.out.println("--all stared--");
        try {
            t1.join();
            t2.join();
        } catch (Exception e) {
            System.out.println("join error");
        }
    }
}

// 输出
// 出现了不一致的情况，为嘛捏

//    2589--3210
//    4999--5054
//    5631--5631
//    6144--6406
//    7485--7596
//    8452--8503
//    9727--9795
```
根据官方的说法是因为方法one和方法two是同时被两个线程异步调用，而且一个线程对共享变量读一个线程又同时去写，在这种情况下就触发了**指令重排序**，而指令重排会让程序的结果变得很诡异，
比如上述代码我们期望输出的应该如下才对
```text
1--1
2--2
3--3
...
n--n
```
因为我们期望程序的执行逻辑是
```text
Thread 1
p1++
p2++
p1++
p2++
p1++
p2++
...
```
但是实际输出的值却和期望的值大相径庭，这是因为我们没有正确的使用异步导致了data race(数据竞争参见Happens-before Order)触发了编译器的优化，所以我们的代码执行起来的时候并不是我们所期望的那样，有可能是
```text
Thread 1
p1++
p1++
p1++
p1++
p1++
p2++
p2++
...
```
> 指令重排序是Java Memeory Model中对Actions order的规定而产生的一种行为（或者叫优化）。参见<a href="https://docs.oracle.com/javase/specs/jls/se8/html/jls-17.html#jls-17.4.5">Happens-before Order</a>

加上volatile后会发生什么?
```java
private static volatile int p1 = 0, p2 = 0;

// 1489--2147
// 3584--3784
// 4466--4490
// 4874--5047
// 5969--6064
// 6510--6544
// 6655--6655
// 7219--7249
// 7945--7982
```
发现依然没能按照我们的期望进行输出，加上volatile后虽然解决了指令重排问题，但是导致输出怪异的根本原因是我们没有控制好并发，而且官方文档表示只要代码处理好并发问题并不需要考虑指令重排的问题
> Once the determination that the code is correctly synchronized is made, the programmer does not need to worry that reorderings will affect his or her code.
比如上述代码，如果我们想p1和p2的输出一致，应该保证在获取p1和p2这个时间段内不应该允许其他线程对p1和p2进行写操作
```java
    private static synchronized void one() {
        p1++;
        p2++;
    }

    private static synchronized void two() {
        System.out.println(p1 + "--" + p2);
    }
```
最简单的修复这段代码的并发问题是添加synchronized标识，现在输出的p1和p2总会保持一致。