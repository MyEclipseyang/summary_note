### Mybatis源码分析

#### 1.解析配置文件

```java
	@Before
    public void before() throws IOException {
        try (Reader resourceAsReader = Resources.getResourceAsReader("com/zyy/mybatis-config.xml")){

            factory = new SqlSessionFactoryBuilder().build(resourceAsReader);
        } catch (IOException e) {
            throw new IOException("解析配置文件失败！");
        }
    }
```

##### 1.1SqlSessionFactoryBuilder.java

![文件解析步骤](https://gitee.com/BossZyy/note_img/raw/master/image-20220105174555556.png)

- 将文件流解析为**XMLConfigBuilder**对象
- 执行**XMLConfigBuilder**的**parse**方法构建**Configuration**对象
- 传入**Configuration**对象构建**SqlSessionFactory**

##### 1.2Configuration对象的构建

```java
public class XMLConfigBuilder extends BaseBuilder {
  
  public Configuration parse() {
    if (parsed) {
      throw new BuilderException("Each XMLConfigBuilder can only be used once.");
    }
    parsed = true;
    parseConfiguration(parser.evalNode("/configuration"));
    return configuration;
  }

  private void parseConfiguration(XNode root) {
    try {
      // issue #117 read properties first
      propertiesElement(root.evalNode("properties"));
      Properties settings = settingsAsProperties(root.evalNode("settings"));
      loadCustomVfs(settings);
      loadCustomLogImpl(settings);
      typeAliasesElement(root.evalNode("typeAliases"));
      pluginElement(root.evalNode("plugins"));
      objectFactoryElement(root.evalNode("objectFactory"));
      objectWrapperFactoryElement(root.evalNode("objectWrapperFactory"));
      reflectorFactoryElement(root.evalNode("reflectorFactory"));
      settingsElement(settings);
      // read it after objectFactory and objectWrapperFactory issue #631
      environmentsElement(root.evalNode("environments"));
      databaseIdProviderElement(root.evalNode("databaseIdProvider"));
      typeHandlerElement(root.evalNode("typeHandlers"));
      mapperElement(root.evalNode("mappers"));
    } catch (Exception e) {
      throw new BuilderException("Error parsing SQL Mapper Configuration. Cause: " + e, e);
    }
  }	
}
```

> 解析各个标签构建**Configuration**对象的过程可参照官方文档进行理解
>
> https://mybatis.org/mybatis-3/zh/configuration.html
