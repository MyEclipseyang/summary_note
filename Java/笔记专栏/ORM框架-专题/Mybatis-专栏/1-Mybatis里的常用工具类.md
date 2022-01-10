### Mybatis里的常用工具类

> 参考Mybatis 3源码深度解析 姜荣波[著]

#### 1.SQL类

> 可以很方便地在Java代码中动态构建SQL语句

```java
  @Test
    public void testJoinSql() throws SQLException {
        SQL sql = new SQL()
                .SELECT("name, died_year")
                .FROM("great_people").LIMIT(10);
        Connection connection = DriverManager.getConnection(url, user, pass);
        PreparedStatement preparedStatement = connection.prepareStatement(sql.toString());
        ResultSet resultSet = preparedStatement.executeQuery();
        while (resultSet.next()) {
            System.out.println(String.format("姓名：%s\t去世：%s", resultSet.getString("name"), resultSet.getString("died_year")));
        }

        resultSet.close();
        connection.close();
    }
```

<!-- more -->

#### 2.ScriptRunner

> 读取脚本文件中的SQL语句并执行

```java
    @Test
    public void testScriptRunner() throws SQLException, IOException {
        // 一般是在使用h2数据库时用来做数据库的初始化工作
        Connection connection = DriverManager.getConnection(url, user, pass);
        ScriptRunner scriptRunner = new ScriptRunner(connection);
        scriptRunner.runScript(Resources.getResourceAsReader("resources/init_db.sql"));
    }
```

#### 3.SQLRunner

> 操作数据库的工具类，对JDBC做了很好的封装，结合SQL工具类，能够很方便地通过Java代码执行SQL语句并检索SQL执行结果

```java
    @Test
    public void testSqlRunner() throws SQLException {
        Connection connection = DriverManager.getConnection(url, user, pass);
        SqlRunner sqlRunner = new SqlRunner(connection);
        String sqlStr = new SQL()
                .SELECT("name, died_year")
                .FROM("great_people")
                .WHERE("id = ?").toString();
        Map<String, Object> stringObjectMap = sqlRunner.selectOne(sqlStr, 1);

        System.out.println(JSON.toJSONString(stringObjectMap));
    }
```

#### 4.MetaObject

> 优雅地获取和设置对象的属性值

```java
	private	User userEntity;

	@Before
    public void before() {
        List<Order> orders = new ArrayList<>(2);
        orders.add(new Order("1", "订单1", 10D));
        orders.add(new Order("2", "订单2", 10.21D));
        userEntity = new User("zyy", 21, orders);
    }

    @Test
    public void testMetaObject() {
        MetaObject metaObject = SystemMetaObject.forObject(userEntity);
        if (metaObject.hasSetter("ttt")) {
            metaObject.setValue("ttt", "test");
        }
        metaObject.setValue("username", "lht");
        Object username = metaObject.getValue("username");
        System.out.println(username);
    }
```

#### 5.MetaClass

> MetaClass用于获取类相关的信息

```java
    @Test
    public void testObjectClazz() throws InvocationTargetException, IllegalAccessException {
        MetaClass userClazz = MetaClass.forClass(User.class, new DefaultReflectorFactory());
        // 获取所有的Getter 包括父类和实现的接口的
        String[] getterNames = userClazz.getGetterNames();
        for (String getterName : getterNames) {
            System.out.println(getterName);
        }
        // 判断方法是否存在
        boolean usernameGet = userClazz.hasGetter("username");
        boolean usernameSet = userClazz.hasSetter("username");
        boolean usernameNoArgConstructor = userClazz.hasDefaultConstructor();
        System.out.println(String
                .format("username属性是否有Getter：%b,是否有Setter：%b,是否有默认的构造方法：%b"
                        ,usernameGet, usernameSet, usernameNoArgConstructor));
        // 获取Setter的参数类型 和 Getter的返回类型
        Class<?> usernameGetType = userClazz.getGetterType("username");
        Class<?> usernameSetType = userClazz.getSetterType("username");
        System.out.println(String.format("usernameSetType：%s,usernameGetType：%s",usernameSetType, usernameGetType));
        // 获取Getter Setter方法
        Invoker usernameGetterInvoker = userClazz.getGetInvoker("username");
        Invoker usernameSetterInvoker = userClazz.getSetInvoker("username");
        String invokeReturn1 = (String)usernameGetterInvoker.invoke(userEntity, null);
        System.out.println("invokeReturn1:" + invokeReturn1);
        usernameSetterInvoker.invoke(userEntity, new String[]{"invokeZyy"});
        String invokeReturn2 = (String)usernameGetterInvoker.invoke(userEntity, null);
        System.out.println("invokeReturn2:" + invokeReturn2);
    }
```

#### 6.ObjectFactory

> ObjectFactory是MyBatis中的对象工厂，MyBatis每次创建Mapper映射结果对象的新实例时，都会用一个对象工厂(ObjectFactory)实例来完成。
>
> ObjectFactory接口只有一个默认的实现，即DefaultObjectFactory，默认的对象工厂需要做的仅仅是实例化目标类，要么通过默认构造方法，要么在参数映射存在的时候通过参数构造方法来实例化。

```java
    @Test
    public void testObjectFactory(){
        ObjectFactory objectFactory = new DefaultObjectFactory();
        User user = objectFactory.create(User.class);
        user.setUsername("zyy");
        System.out.println(user);
    }
```

##### MyBatis中使用ObjectFactory实例创建Mapper映射结果对象的目的是什么呢？

> 实际上，这是MyBatis提供的一种扩展机制。有些情况下，在得到映射结果之前我们需要处理一些逻辑，或者在执行该类的有参构造方法时，在传入参数之前，要对参数进行一些处理，这时我们可以通过自定义ObjectFactory来实现。

```java
public class ZyyObjectFactory extends DefaultObjectFactory {

    @SuppressWarnings("unchecked")
    @Override
    public <T> T create(Class<T> type) {
        if(type == User.class){
            User user = super.create(User.class);
            user.setUsername("createByZyyObjectFactory");
            return (T) user;
        }
        return super.create(type);
    }
}
    @Test
    public void testCustomObjectFactory(){
        ObjectFactory objectFactory = new ZyyObjectFactory();
        User user = objectFactory.create(User.class);
        System.out.println(user);
        // 输出 User(username=createByZyyObjectFactory, age=null, orderList=null)
    }
```

#### 7.ProxyFactory

> ProxyFactory是MyBatis中的代理工厂，主要用于创建动态代理对象，ProxyFactory接口有两个实现，分别为CglibProxyFactory和JavassistProxyFactory。从实现类的名称可以看出，MyBatis支持两种动态代理策略，分别为Cglib和Javassist动态代理。
>
> ProxyFactory主要用于实现MyBatis的懒加载功能。当开启懒加载后，MyBatis创建Mapper映射结果对象后，会通过ProxyFactory创建映射结果对象的代理对象。当我们调用代理对象的Getter方法获取数据时，会执行CglibProxyFactory或JavassistProxyFactory中定义的拦截逻辑，然后执行一次额外的查询

```java
   @Test
    public void testProxyFactory(){
        ProxyFactory proxyFactory = new JavassistProxyFactory();
        ObjectFactory objectFactory = new ZyyObjectFactory();
        @SuppressWarnings("unchecked")
        Object proxy = proxyFactory
                .createProxy(userEntity,
                        mock(ResultLoaderMap.class),
                        mock(Configuration.class),
                        objectFactory,
                        Collections.EMPTY_LIST,
                        Collections.EMPTY_LIST);
        System.out.println(proxy);

        User user = (User) proxy;
        System.out.println(user.getUsername());
        System.out.println(user.getAge());
    }
```

#### 8.PropertyCopier

> 对实体的属性进行复制

```java
  @Test
    public void testPropertyCopier(){
        User user = new User();

        PropertyCopier.copyBeanProperties(User.class, userEntity, user);
        System.out.println(user);
    }
```

