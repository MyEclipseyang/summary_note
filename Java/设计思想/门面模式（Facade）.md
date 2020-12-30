### 门面模式（Facade）

#### 1.什么是门面模式

为一个子系统中的一系列接口提供一个统一的接口。外观定义了一个更高级别的接口以便子系统更容易使用。

#### 2.实例

例如一个项目需要的人员有产品经理、研发经理、前端、后端、测试等共同协作来完成，而从甲方的角度看来只需要拿钱启动项目最后验收项目即可

#### 3.程序示例

```java
public interface IProjectWorker {

    void startDailyWork();

    void pauseToRest();

    void endDailyWork();

    String getName();
}
```

<!--more-->

```java
public abstract class BaseProjectWorker implements IProjectWorker{
    private String name;
    protected BaseProjectWorker(String name){
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }
}
```

```java
public class FrontProgrammer extends BaseProjectWorker{

    protected FrontProgrammer(String name) {
        super(name);
    }

    @Override
    public void startDailyWork() {
        System.out.println("[FrontProgrammer] 开始编写前端页面");
    }

    @Override
    public void pauseToRest() {
        System.out.println("[FrontProgrammer] 休息去喝咖啡");
    }

    @Override
    public void endDailyWork() {
        System.out.println("[FrontProgrammer] 结束编写前端页面");
    }
}
```

```java
public class BackProgrammer extends BaseProjectWorker{

    protected BackProgrammer(String name) {
        super(name);
    }

    @Override
    public void startDailyWork() {
        System.out.println("[FrontProgrammer] 开始编写后端页面");
    }

    @Override
    public void pauseToRest() {
        System.out.println("[FrontProgrammer] 休息去喝茶");
    }

    @Override
    public void endDailyWork() {
        System.out.println("[FrontProgrammer] 结束编写后端页面");
    }

}
```

```java
public class TestProgrammer extends BaseProjectWorker{

    protected TestProgrammer(String name) {
        super(name);
    }

    @Override
    public void startDailyWork() {
        System.out.println("[TestProgrammer] 开始测试");
    }

    @Override
    public void pauseToRest() {
        System.out.println("[TestProgrammer] 休息去喝咖啡");
    }

    @Override
    public void endDailyWork() {
        System.out.println("[TestProgrammer] 结束测试");
    }
}
```

```java
public class ProjectFacade {
    private List<IProjectWorker> workers;
    public ProjectFacade(){
        workers = new ArrayList<>();
        workers.add(new FrontProgrammer("一号前端"));
        workers.add(new FrontProgrammer("二号前端"));
        workers.add(new BackProgrammer("一号后端"));
        workers.add(new BackProgrammer("二号后端"));
        workers.add(new BackProgrammer("三号后端"));
        workers.add(new TestProgrammer("一号测试"));
    }

    public void startProject(){
        workers.forEach(IProjectWorker::startDailyWork);
    }

    public void endProject(){
        workers.forEach(IProjectWorker::endDailyWork);
    }
}
```

#### 4.测试

```java
@Test
public void test(){
    // 同样也是提供给用户的接口
    ProjectFacade projectFacade = new ProjectFacade();

    projectFacade.startProject();

    projectFacade.endProject();
}
```

#### 5.测试输出

> [FrontProgrammer] 开始编写前端页面
> [FrontProgrammer] 开始编写前端页面
> [FrontProgrammer] 开始编写后端页面
> [FrontProgrammer] 开始编写后端页面
> [FrontProgrammer] 开始编写后端页面
> [TestProgrammer] 开始测试
> [FrontProgrammer] 结束编写前端页面
> [FrontProgrammer] 结束编写前端页面
> [FrontProgrammer] 结束编写后端页面
> [FrontProgrammer] 结束编写后端页面
> [FrontProgrammer] 结束编写后端页面
> [TestProgrammer] 结束测试

#### 6.总结

接口的多个子类完成一项工作的时候适合使用门面模式的思想去封装下，提高了系统的易用性和用户的产品体验