### Mybatis的简单使用

#### 1.不依赖其他框架

```groovy
implementation 'org.mybatis:mybatis:3.4.x'
```

##### 1.1mapper接口

```java
public interface GreatPeopleMapper {

    GreatPeopleDomain selectById(Integer id);
}
```

##### 1.2与mapper接口对应的mapper文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.zyy.mapper.GreatPeopleMapper">

    <resultMap id="baseMap" type="com.zyy.domain.GreatPeopleDomain">
        <id column="id" property="id"/>
        <result column="name" property="name"/>
        <result column="sex" property="sex"/>
        <result column="famous" property="famous"/>
        <result column="brithday_year" property="birthdayYear"/>
        <result column="died_year" property="diedYear"/>
        <result column="died_reason" property="diedReason"/>
        <result column="force" property="force"/>
        <result column="intelligence" property="intelligence"/>
    </resultMap>

    <select id="selectById" resultMap="baseMap">
        select * from great_people where id = #{id}
    </select>
</mapper>
```

##### 1.3全局配置文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>

    <properties resource="com/zyy/mybatis.properties"/>
    
    <settings>
         <setting name="logImpl" value="STDOUT_LOGGING"/>
    </settings>

    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${driver}"/>
                <property name="url" value="${url}"/>
                <property name="username" value="${username}"/>
                <property name="password" value="${password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="com/zyy/mapper/GreatPeopleMapper.xml"/>
    </mappers>
</configuration>
```

##### 1.4使用

```java
public class MybatisStartTest {

    private SqlSessionFactory factory;

    @Before
    public void before() throws IOException {
        try (Reader resourceAsReader = Resources.getResourceAsReader("com/zyy/mybatis-config.xml")){

            factory = new SqlSessionFactoryBuilder().build(resourceAsReader);
        } catch (IOException e) {
            throw new IOException("解析配置文件失败！");
        }
    }

    @Test
    public void testGenerateFromFile() {

        try (SqlSession sqlSession = factory.openSession()){
            GreatPeopleMapper greatPeopleMapper = sqlSession.getMapper(GreatPeopleMapper.class);
            GreatPeopleDomain greatPeopleDomain = greatPeopleMapper.selectById(1);

            System.out.println(greatPeopleDomain);
            Assert.assertEquals("success", "伊籍", greatPeopleDomain.getName());
        }
    }
}
```

#### 2.结合Spring

##### 2.1添加依赖

```groovy
implementation 'org.mybatis:mybatis-spring:2.x.x'
```

##### 2.2mapper接口

```java
public interface UserMapper {
  @Select("SELECT * FROM users WHERE id = #{userId}")
  User getUser(@Param("userId") String userId);
}
```

##### 2.3配置bean

```java
@Configuration
public class MyBatisConfig {
  @Bean
  public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
    SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
    factoryBean.setDataSource(dataSource);
    return factoryBean.getObject();
  }
    
  @Bean
  public UserMapper userMapper() throws Exception {
    SqlSessionTemplate sqlSessionTemplate = new SqlSessionTemplate(sqlSessionFactory());
    return sqlSessionTemplate.getMapper(UserMapper.class);
  }
}
```

##### 2.4使用

```java
@Service
public class FooServiceImpl implements FooService {

  @Autowired
  private UserMapper userMapper;
    
  public User doSomeBusinessStuff(String userId) {
    return this.userMapper.getUser(userId);
  }
}
```

#### 3.结合SpringBoot

