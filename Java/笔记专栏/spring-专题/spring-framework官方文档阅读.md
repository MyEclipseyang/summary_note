spring-framework官方文档阅读

### 1.往Spring管理的单例对象中注入非单例
> 1.4.6 Method injection <br/>
> 官方介绍了三种方法（实现ApplicationContextAware接口、xml方式和注解）

> 例如每次调用process方法都需要一个新的Command实例
#### 1.1 注解方式
```java
public abstract class CommandManager {

    public Object process(Object commandState) {
        Command command = createCommand();
        command.setState(commandState);
        return command.execute();
    }

    @Lookup
    protected abstract Command createCommand();
}
```