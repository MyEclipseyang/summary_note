### 状态模式（state）
#### 1.什么是状态模式
> WIKI: 状态模式是一种允许对象在内部状态改变时改变它的行为的行为型设计模式。

#### 2.示例

> 假如当前有一个任务，任务的状态有待审核、审核通过、审核失败（创建任务默认时待审核状态）

#### 3.程序实例

```java
public interface IState {

    /**
     * 状态的行为
     */
    void observe();

    /**
     * 切换状态需要做些什么
     */
    void onEnterState();
}
```

<!--more-->

```java
public abstract class BaseState implements IState{
    protected PatternTask task;

    public BaseState(PatternTask task) {
        this.task = task;
    }

    @Override
    public void observe() {
        System.out.println(String.format("State-observe:%s", task));
    }
}
```

未审核状态

```java
public class UnAuthState extends BaseState {

    public UnAuthState(PatternTask task) {
        super(task);
    }

    @Override
    public void onEnterState() {
        task.setAuthState(PatternTask.AuthStateEnum.UN_AUTH.getDescription());
    }
}
```

审核通过

```java
public class AuthenticatedState extends BaseState {

    public AuthenticatedState(PatternTask task) {
        super(task);
    }

    @Override
    public void onEnterState() {
        task.setAuthState(PatternTask.AuthStateEnum.AUTHENTICATED.getDescription());
    }
}
```

审核未通过

```java
public class UnPassedState extends BaseState {

    public UnPassedState(PatternTask task) {
        super(task);
    }

    @Override
    public void onEnterState() {
        task.setAuthState(PatternTask.AuthStateEnum.UN_PASS_AUTH.getDescription());
    }
}
```

任务实体

```java
@Data
public class PatternTask {
    public enum AuthStateEnum{
        UN_AUTH(1, "待审核"),
        AUTHENTICATED(2, "审核通过"),
        UN_PASS_AUTH(3, "审核失败");

        private int index;
        private String description;
        AuthStateEnum(int index, String description){
            this.index = index;
            this.description = description;
        }

        public int getIndex() {
            return index;
        }

        public String getDescription() {
            return description;
        }
    }

    private IState state;

    public PatternTask(){
        // 初始化默认的任务状态
        state = new UnAuthState(this);
        this.state.onEnterState();
    }

    // 改变状态
    public void changeStateTo(IState state){
        this.state = state;
        this.state.onEnterState();
    }

    // 查看状态
    public void observeState(){
        this.state.observe();
    }

    private String id;

    private String name;

    private String content;

    /**
     * 审核状态
     */
    private String authState;
}
```

测试

```java
@Test
public void test(){
    PatternTask task = new PatternTask();
    task.observeState();

    task.changeStateTo(new UnPassedState(task));
    task.observeState();

    task.changeStateTo(new AuthenticatedState(task));
    task.observeState();
}
```

测试输出

> State-observe:PatternTask(state=com.zyy.state.impl.UnAuthState@73a8dfcc, id=null, name=null, content=null, authState=待审核)
> State-observe:PatternTask(state=com.zyy.state.impl.UnPassedState@ea30797, id=null, name=null, content=null, authState=审核失败)
> State-observe:PatternTask(state=com.zyy.state.impl.AuthenticatedState@7e774085, id=null, name=null, content=null, authState=审核通过)

#### 4.总结

可以通过名字就知道该模式适合当业务中的实体存在较多状态变化时使用，例如常见的购物订单的状态变化以及上例。使用该模式避免了在状态变化时的硬编码或存在大量的逻辑判断而导致代码的可阅读性以及可扩展性降低。