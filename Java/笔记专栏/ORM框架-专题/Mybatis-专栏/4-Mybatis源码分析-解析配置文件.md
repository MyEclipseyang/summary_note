### Mybatis源码分析

#### 1.解析配置文件

> 解析文件创建SqlSessionFactory

```java
	@Before
    public void before() throws IOException {
        try (Reader resourceAsReader = Resources.getResourceAsReader("com/zyy/mybatis-config.xml")){

            factory = new SqlSessionFactoryBuilder().build(resourceAsReader);
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
      // mybatis一些行为的配置
      Properties settings = settingsAsProperties(root.evalNode("settings"));
      loadCustomVfs(settings);
      // 日志设置
      loadCustomLogImpl(settings);
      // 别名设置
      typeAliasesElement(root.evalNode("typeAliases"));
      // 插件设置
      pluginElement(root.evalNode("plugins"));
      // mybatis创建对象的工厂
      objectFactoryElement(root.evalNode("objectFactory"));
      // 将普通的java对象包装成ObjectWrapper实例
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

> 具体如何解析各个标签来构建**Configuration**对象的过程可参照官方文档进行理解
>
> https://mybatis.org/mybatis-3/zh/configuration.html
>
> https://mybatis.org/mybatis-3/zh/sqlmap-xml.html （mapper标签）

在不结合spring使用mybatis时，我们需要通过xml配置文件来配置myatis的各种行为(如指定事务管理器、类型处理器等)，还需要编写sql映射文件，该文件类型也为xml格式，所以mybatis启动首先要做的便是加载指定的配置文件并解析其内容，当然除了配置文件mybatis还会读取并解析配置文件中指定的sql映射文件。

#### 2.SqlSession对象的构建

```java
@Test
public void testGenerateFromFile() {

    try (SqlSession sqlSession = factory.openSession()){
        GreatPeopleMapper greatPeopleMapper = sqlSession.getMapper(GreatPeopleMapper.class);
        GreatPeopleDomain greatPeopleDomain = greatPeopleMapper.selectById(1);

        System.out.println(greatPeopleDomain);
        Assert.assertEquals("success", "伊籍", greatPeopleDomain.getName());
    }
}
```

```java
public class DefaultSqlSessionFactory implements SqlSessionFactory {

  @Override
  public SqlSession openSession() {
    return openSessionFromDataSource(configuration.getDefaultExecutorType(), null, false);
  }
    
  private SqlSession openSessionFromDataSource(ExecutorType execType, TransactionIsolationLevel level, boolean autoCommit) {
    Transaction tx = null;
    try {
      final Environment environment = configuration.getEnvironment();
      final TransactionFactory transactionFactory = getTransactionFactoryFromEnvironment(environment);
      tx = transactionFactory.newTransaction(environment.getDataSource(), level, autoCommit);
      // 构建执行器
      final Executor executor = configuration.newExecutor(tx, execType);
      // 构建sqlSession
      return new DefaultSqlSession(configuration, executor, autoCommit);
    } catch (Exception e) {
      closeTransaction(tx); // may have fetched a connection so lets call close()
      throw ExceptionFactory.wrapException("Error opening session.  Cause: " + e, e);
    } finally {
      ErrorContext.instance().reset();
    }
  }
}
```

我们通常会调用SqlSessionFactory不带参数的openSession方法来创建一个SqlSession

```java
public class Configuration {
  public Executor newExecutor(Transaction transaction, ExecutorType executorType) {
    executorType = executorType == null ? defaultExecutorType : executorType;
    executorType = executorType == null ? ExecutorType.SIMPLE : executorType;
    Executor executor;
    if (ExecutorType.BATCH == executorType) {
      executor = new BatchExecutor(this, transaction);
    } else if (ExecutorType.REUSE == executorType) {
      executor = new ReuseExecutor(this, transaction);
    } else {
      executor = new SimpleExecutor(this, transaction);
    }
    if (cacheEnabled) {
      executor = new CachingExecutor(executor);
    }
    executor = (Executor) interceptorChain.pluginAll(executor);
    return executor;
  }
}
```

构建执行器，默认返回的是一个带缓存行为的SimpleExecutor，当一个新鲜的SqlSession被创建出来时也就标志着mybatis已经准备好来执行sql了。

#### 3.执行sql

```java
public interface GreatPeopleMapper {

    GreatPeopleDomain selectById(Integer id);
}
```

经过充分的前期准备，现在终于到了关键的地方-执行sql。一般我们会通过以下代码来获取可以执行方法拿到数据的mapper实例

```java
GreatPeopleMapper greatPeopleMapper = sqlSession.getMapper(GreatPeopleMapper.class);
GreatPeopleDomain greatPeopleDomain = greatPeopleMapper.selectById(1);
```

但是GreatPeopleMapper明明是个接口，为什么通过sqlSession获得的实例直接就能执行接口里的方法呢？其实这里mybatis使用了JDK动态代理技术，getMapper方法拿到的其实是代理后的实例。

> 最终是由MapperProxyFactory类创建代理对象并返回，也就是说无论执行接口的哪个方法最终执行的都是MapperProxy类的invoke

```java
public class MapperRegistry {
    public <T> T getMapper(Class<T> type, SqlSession sqlSession) {
      final MapperProxyFactory<T> mapperProxyFactory = (MapperProxyFactory<T>) knownMappers.get(type);
      if (mapperProxyFactory == null) {
        throw new BindingException("Type " + type + " is not known to the MapperRegistry.");
      }
      try {
        return mapperProxyFactory.newInstance(sqlSession);
      } catch (Exception e) {
        throw new BindingException("Error getting mapper instance. Cause: " + e, e);
      }
    }
}
```

```java
public class MapperProxyFactory<T> {

  private final Class<T> mapperInterface;
  private final Map<Method, MapperMethodInvoker> methodCache = new ConcurrentHashMap<>();

  public MapperProxyFactory(Class<T> mapperInterface) {
    this.mapperInterface = mapperInterface;
  }

  public Class<T> getMapperInterface() {
    return mapperInterface;
  }

  public Map<Method, MapperMethodInvoker> getMethodCache() {
    return methodCache;
  }

  @SuppressWarnings("unchecked")
  protected T newInstance(MapperProxy<T> mapperProxy) {
    // 创建代理对象并返回
    return (T) Proxy.newProxyInstance(mapperInterface.getClassLoader(), new Class[] { mapperInterface }, mapperProxy);
  }

  public T newInstance(SqlSession sqlSession) {
    final MapperProxy<T> mapperProxy = new MapperProxy<>(sqlSession, mapperInterface, methodCache);
    return newInstance(mapperProxy);
  }

}
```
