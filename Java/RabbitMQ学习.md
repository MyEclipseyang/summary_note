#### RabbitMQ学习

##### 安装Server

```shell
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

##### client

```xml
<dependency>
    <groupId>com.rabbitmq</groupId>
    <artifactId>amqp-client</artifactId>
    <version>5.11.0</version>
</dependency>
```

<!-- more -->

##### 代码案例

```java
/**
 * 任务发布者
 */
public class Boss {

    private static final String QUEUE_NAME = "task_queue";

    public static void main(String[] args) {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("47.95.2.220");
        connectionFactory.setPort(8070);

        try(Connection connection = connectionFactory.newConnection();
            Channel channel = connection.createChannel();
        ){
            channel.queueDeclare(QUEUE_NAME, true, false, false, null);
            String msg = String.join(" ", args);
            channel.basicPublish("", QUEUE_NAME, MessageProperties.PERSISTENT_TEXT_PLAIN, msg.getBytes());
            System.out.println(" [x] Sent '" + msg + "'");
        } catch (TimeoutException | IOException e) {
            e.printStackTrace();
        }
    }
}
```

```java
public abstract class BaseWorker {
    private static final String QUEUE_NAME = "task_queue";

    protected abstract void doWork(String msg) throws InterruptedException;

    public void startWork() throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("47.95.2.220");
        connectionFactory.setPort(8070);

        Connection connection = connectionFactory.newConnection();
        Channel channel = connection.createChannel();
        // Server发生异常或重启时，持久化改任务队列
        boolean durable = true;
        channel.queueDeclare(QUEUE_NAME, durable, false,false,null);
        System.out.println("waiting for message");

        // 一件任务没干完别再给派活了
        channel.basicQos(1);
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String receiveMsg = new String(delivery.getBody(), StandardCharsets.UTF_8);
            System.out.println("receive msg " + receiveMsg);
            long deliveryTag = delivery.getEnvelope().getDeliveryTag();
            try {
                doWork(receiveMsg);
                // 告诉Boss这次派发的任务彻底完成了
                channel.basicAck(deliveryTag, false);
                System.out.println("receive msg " + receiveMsg + "and finish work!");
            } catch (InterruptedException e) {
                System.out.println("receive msg " + receiveMsg + "处理失败，Cause:" + e.getMessage());
                // 执行该任务时发生异常，将该任务重新加入任务队列
                channel.basicReject(deliveryTag, true);
            }
        };

        channel.basicConsume(QUEUE_NAME,false, deliverCallback, (consumerTag) -> {});
    }
}
```

```java
/**
 * 懒惰的工人
 */
public class LazyWork extends BaseWorker{

    @Override
    protected void doWork(String msg) throws InterruptedException {
        int dotCount = 0;
        for(char ch : msg.toCharArray()){
            if (ch == '.') {
                dotCount++;
                Thread.sleep(1000);
            }
            if(dotCount > 10) throw new InterruptedException("dot's length too large!");
        }
    }

    public static void main(String[] args) throws IOException, TimeoutException {
        LazyWork lazyWork = new LazyWork();
        lazyWork.startWork();
    }
}
```

```java
public class GreatWork extends BaseWorker{
    @Override
    protected void doWork(String msg) throws InterruptedException {
        for(char ch : msg.toCharArray()){
            if (ch == '.') {
                Thread.sleep(1000);
            }
        }
    }

    public static void main(String[] args) throws IOException, TimeoutException {
        GreatWork greatWork = new GreatWork();
        greatWork.startWork();
    }
}
```