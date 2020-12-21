### Callback模式

#### 1.什么是Callback(回调)模式

> 将特定代码作为参数传递给其他代码（一般为方法），由其他代码决定在特定的时间执行

#### 2.例子

> 比如常见的web应用里，你发送一个请求后必须等待响应数据返回后才能对数据进行操作

#### 3.程序示例

> 等待作业做完然后检查作业

```java
@FunctionalInterface
public interface DoThingLater {

    void doThing();
}
```

<!-- more -->

```java
public interface Task {

    default void doExecute(DoThingLater doThingLater){
        executeTask();
        // 执行完任务再执行DoThingLater的方法
        doThingLater.doThing();
    }

    void executeTask();
}
```

```java
public class HomeworkTask implements Task{

    @Override
    public void executeTask() {
        System.out.println("做家庭作业");
    }
}

```

```java
@Test
public void test(){
    new com.zyy.a1nogofpattern.callback.HomeworkTask().doExecute(()-> System.out.println("检查作业"));
}
```

> 做家庭作业
> 检查作业

#### 4.总结

该模式将任务执行代码和处理返回数据的代码解耦，提高了应用程序的灵活性。