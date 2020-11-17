### Freemarker初学记录

#### 1.pom添加依赖

```xml
<!-- https://mvnrepository.com/artifact/org.freemarker/freemarker -->
<dependency>
    <groupId>org.freemarker</groupId>
    <artifactId>freemarker</artifactId>
    <version>2.3.30</version>
</dependency>
```

#### 2.实例化Configuration

> 这里使用单例(饿汉)来实现初始化Configuration

```JAVA
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateExceptionHandler;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;

public class SingletonConfiguration {

    private static SingletonConfiguration instance;

    private static Configuration configuration;

    static {
        try {
            instance = new SingletonConfiguration();
        } catch (IOException | URISyntaxException e) {
            System.out.println("初始化Freemarker Configuration失败！");
            e.printStackTrace();
        }
    }

    private SingletonConfiguration() throws IOException, URISyntaxException {
        URL resource = SingletonConfiguration.class.getClassLoader().getResource("templates");

        if (resource == null) {
            throw new FileNotFoundException("加载模板文件失败！");
        }

        configuration = new Configuration(Configuration.VERSION_2_3_29);
        // 设置模板文件位置
        configuration.setDirectoryForTemplateLoading(new File(resource.toURI()));
        configuration.setDefaultEncoding("UTF-8");
        configuration.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);
        configuration.setWrapUncheckedExceptions(true);

        // -----为了保持向后兼容而维持默认值为true，目前新应用程序应该设置为false-----
        // 出现异常不需要Freemarker再抛出一次 2.3.22后设置为true异常信息将会抛出两次
        configuration.setLogTemplateExceptions(false);
        configuration.setFallbackOnNullLoopVariable(false);
        // -----为了保持向后兼容而维持默认值为true，目前新应用程序应该设置为false-----
    }

    public static SingletonConfiguration getInstance() {

        return instance;
    }

    public Template getTemplate(String templateFileName) throws IOException {
        return configuration.getTemplate(templateFileName);
    }
}

```

#### 3.获取Template并填充data-modal

```java
    public static void main(String[] args) throws IOException, TemplateException {
        SingletonConfiguration configuration = SingletonConfiguration.getInstance();

        Template template = configuration.getTemplate("first.ftl");

        SystemUser user = new SystemUser();
        user.setUsername("zyy");
		// 输出到控制台
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(System.out);
        template.process(user, outputStreamWriter);
    }
```

```java
    public static void main(String[] args) throws IOException, TemplateException {
        SingletonConfiguration configuration = SingletonConfiguration.getInstance();

        Template template = configuration.getTemplate("first.ftl");

        SystemUser user = new SystemUser();
        user.setUsername("zyy");
		
        // 使用BufferWriter将填充好的Template输出到文件
        
        // 之所以BufferWriter比直接使用FileWriter邪刃操作性能好的原因在于：BufferWriter是积攒到一定量的时候再写入文件
        // 中，而不是一个一个的写入文件
        Writer writer = new BufferedWriter(new FileWriter("D:/first.html"));
        template.process(user, writer);
    }
```

