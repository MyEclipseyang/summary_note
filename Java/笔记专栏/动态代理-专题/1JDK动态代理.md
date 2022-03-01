## JDK动态代理

### 1.相关的类

> 每个代理对象都会拥有一个调用处理器(InvocationHandler), 当代理对象执行方法时便会执行invoke方法

```java
public interface InvocationHandler {
    
  public Object invoke(Object proxy, Method method, Object[] args) throws Throwable;
}
```

> Proxy类负责创建代理对象

```java
public class Proxy implements java.io.Serializable {
	
    /**
     * @param interfaces 代理类需要实现的接口 需注意代理接口和代理类时传参有所不同
     * @param h 调用处理器
     */
    public static Object newProxyInstance(ClassLoader loader,
                                          Class<?>[] interfaces,
                                          InvocationHandler h)
        throws IllegalArgumentException
    {
    	...
    }
}
```

### 2.简单使用

#### 2.1代理接口

```
public interface IHelloService {

    void sayHello();
}
```

```java
public class IHelloInvocationHandler implements InvocationHandler {

    // command
    private final HelloCommandEnum commandEnum;

    public IHelloInvocationHandler(HelloCommandEnum commandEnum) {
        this.commandEnum = commandEnum;
    }

    @Override
    public Object invoke(Object object, Method method, Object[] args) {
        // 代理之后想要做的事情
        if (HelloCommandEnum.BEFORE == commandEnum) {
            System.out.println("before");
        }

        System.out.println("say hello - by proxy-" + method.getName());

        if (HelloCommandEnum.AFTER == commandEnum) {
            System.out.println("after");
        }

        // 根据需要返回不同类型的信息
        return null;
    }
}
```

```java
public class InvocationMain {

   public static void main(String[] args) {
     IHelloInvocationHandler myInvocationHandler = new IHelloInvocationHandler(HelloCommandEnum.BEFORE);

     IHelloService helloService = (IHelloService) Proxy.newProxyInstance(IHelloService.class.getClassLoader(), new Class[] { IHelloService.class }, myInvocationHandler);

        helloService.sayHello();
    }
}
```

> 输出：
>
> before
> say hello - by proxy-sayHello

#### 2.2代理类

> 需要注意，仅仅使用JDK动态代理并不能直接代理未实现任何接口的类，而创建代理对象时也只能强转为某一该类实现接口的类型

##### 错误示例

```java
public class MorningClass {

    public void say() {
        System.out.println("good morning !!!");
    }
}
```

```java
public static void main(String[] args) {
    MorningClass morningClass = new MorningClass();

    MorningInvocationHandler morningInvocationHandler = new MorningInvocationHandler(morningClass, CommandEnum.AFTER);

    MorningClass morningProxy = (MorningClass) Proxy.newProxyInstance(morningClass.getClass().getClassLoader(), morningClass.getClass().getInterfaces(), morningInvocationHandler);

    morningProxy.say();
}
```

![image-20220111153203532](https://gitee.com/BossZyy/note_img/raw/master/data/image-20220111153203532.png)

MorningClass类未实现任何接口，如果尝试创建该类的代理对象会提示类型无法强转

##### 正确示例

```java
public class HelloServiceImpl implements IHelloService{

    @Override
    public void sayHello() {
        System.out.println("Hello !!");
    }
}
```

```java
public class HelloImplInvocationHandler implements InvocationHandler {

    private final Object target;

    private final CommandEnum commandEnum;

    public HelloImplInvocationHandler(Object target, CommandEnum commandEnum) {
        this.target = target;
        this.commandEnum = commandEnum;
    }

    /**
     * @param proxy 代理对象
     */
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        if (CommandEnum.BEFORE == commandEnum) {
            System.out.println("before");
        }
		// 执行被代理对象的方法
        Object invokeResult = method.invoke(target, args);

        if (CommandEnum.AFTER == commandEnum) {
            System.out.println("after");
        }
        return invokeResult;
    }
}
```

```java
public static void main(String[] args) {
    HelloServiceImpl helloServiceImpl = new HelloServiceImpl();

    HelloImplInvocationHandler h = new HelloImplInvocationHandler(helloServiceImpl, CommandEnum.AFTER);

    IHelloService helloServiceImplProxy = (IHelloService) Proxy.newProxyInstance(helloServiceImpl.getClass().getClassLoader(), helloServiceImpl.getClass().getInterfaces(), h);

    helloServiceImplProxy.sayHello();
}
```

> 输出：
>
> Hello !!
> after

通过简单使用案例可以看出JDK动态代理使用的套路，无论你想代理接口或类你首先需要实现**InvocationHandler**，编写你代理之后想要做的事情。而使用时需要通过**Proxy.newProxyInstance**来创建一个代理对象，该对象执行任何方法都会调用你创建代理对象时传入的调用处理器的invoke方法，从而执行你的代理逻辑。