### 备忘录模式（Memento）

#### 1.什么是备忘录模式

> Memento模式是用来提供一种恢复先前状态能力的一种软件设计模式。

#### 2.例如

恒星会随着时间的流逝而缓慢衰变，从主序星=》红巨星=》白矮星=》超新星=》死亡，当恒星处于某个阶段想退回到前某一个阶段时，我们就可以用到该模式

<!-- more -->

#### 3.具体实现

```java
/**
 * 恒星的演变阶段
 */
public enum  StarStatus {
    SUN("sun"),
    RED_GIANT("red giant"),
    WHITE_DWARF("white dwarf"),
    SUPERNOVA("supernova"),
    DEAD("dead star");

    private final String description;

    StarStatus(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
```

```java
/**
 * 定义行星在不同状态下可以恢复的属性的接口
 * @param <T> 年龄数据类型
 * @param <V> 重量数据类型
 */
public interface StarMemento <T,V>{

    StarStatus getStarStatus();

    T getStarAge();

    V getMessTons();

}
```

> 关键是`getMemento`和`setMemento`方法

```java
public class Star {
    private StarStatus starStatus;
    private int startAge;
    private int massTons;

    public Star(StarStatus starStatus, int startAge, int startMass) {
        this.starStatus = starStatus;
        this.startAge = startAge;
        this.massTons = startMass;
    }

    /**
     * 时间飞逝（每次一年）
     */
    public void timeAddOneYear() {
        startAge += 1;
        massTons *= 8;
        switch (starStatus) {
            case SUN:
                starStatus = StarStatus.RED_GIANT;
                break;
            case RED_GIANT:
                starStatus = StarStatus.WHITE_DWARF;
                break;
            case WHITE_DWARF:
                starStatus = StarStatus.SUPERNOVA;
                break;
            case SUPERNOVA:
            case DEAD:
                starStatus = StarStatus.DEAD;
                massTons = 0;
                break;
            default:
                // do nothing
                break;
        }
    }

    public void setMemento(StarMemento<Integer, Integer> starMemento) {
        this.starStatus = starMemento.getStarStatus();
        this.startAge = starMemento.getStarAge();
        this.massTons = starMemento.getMessTons();
    }

    public StarMemento<Integer, Integer> getMemento() {
        InnerStarMemento innerStarMemento = new InnerStarMemento();
        innerStarMemento.setStarStatus(this.starStatus);
        innerStarMemento.setStartAge(this.startAge);
        innerStarMemento.setMassTons(this.massTons);
        return innerStarMemento;
    }

    @Override
    public String toString() {
        return String.format("%s age: %d years mass: %d tons", starStatus.toString(), startAge, massTons);
    }

    static class InnerStarMemento implements StarMemento<Integer, Integer> {
        private StarStatus starStatus;
        private int startAge;
        private int massTons;

        public void setStarStatus(StarStatus starStatus) {
            this.starStatus = starStatus;
        }

        public void setStartAge(int startAge) {
            this.startAge = startAge;
        }

        public void setMassTons(int massTons) {
            this.massTons = massTons;
        }

        @Override
        public StarStatus getStarStatus() {
            return starStatus;
        }

        @Override
        public Integer getStarAge() {
            return startAge;
        }

        @Override
        public Integer getMessTons() {
            return massTons;
        }
    }
}
```

#### 4.撤回操作

```java
@Test
public void test() {
    Stack<StarMemento<Integer, Integer>> mementoStack = new Stack<>();

    System.out.println("时光飞逝...");
    Star star = new Star(StarStatus.SUN, 100, 10000);
    System.out.println(star);
    mementoStack.push(star.getMemento());

    for (int i = 0; i < 4; i++) {
        star.timeAddOneYear();
        System.out.println(star);
        // 将内部静态类实例保存
        mementoStack.push(star.getMemento());
    }

    System.out.println("时光倒流...");
    while (!mementoStack.empty()) {
        star.setMemento(mementoStack.pop());
        System.out.println(star);
    }

}
```

> 时光飞逝...
> SUN age: 100 years mass: 10000 tons
> RED_GIANT age: 101 years mass: 80000 tons
> WHITE_DWARF age: 102 years mass: 640000 tons
> SUPERNOVA age: 103 years mass: 5120000 tons
> DEAD age: 104 years mass: 40960000 tons
> 时光倒流...
> DEAD age: 104 years mass: 40960000 tons
> SUPERNOVA age: 103 years mass: 5120000 tons
> WHITE_DWARF age: 102 years mass: 640000 tons
> RED_GIANT age: 101 years mass: 80000 tons
> SUN age: 100 years mass: 10000 tons

#### 5.总结

该模式其实就是把要保存的状体数据借助内部类InnerStarMemento保存起来，并借助栈来进行撤回