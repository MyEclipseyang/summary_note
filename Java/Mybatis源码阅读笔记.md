### Mybatis源码阅读笔记

#### 解析mybatis-config.xml文件

##### 测试代码

```java
public static void main(String[] args) throws IOException {
        InputStream resource = Resources.getResourceAsStream("mybatis-config.xml");
    	// 从此处开始分析
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(resource);
        SqlSession sqlSession = sqlSessionFactory.openSession();

        GreatPeopleMapper greatPeopleMapper = sqlSession.getMapper(GreatPeopleMapper.class);
        GreatPeople greatPeople = greatPeopleMapper.selectByPrimaryKey(1);

        System.out.println(greatPeople);
    }
```

###### 1. 将文件流解析为org.w3c.dom.Document对象

分析：Mybatis将配置文件处理成文件流，将文件流传入SqlSessionFactoryBuilder的build方法中

> SqlSessionFactoryBuilder.java

<img src="D:\zyyProject\summary_command_notes\md_img\image-20201119172716698.png" alt="image-20201119172716698" style="zoom:150%;" />

![image-20201119172906827](D:\zyyProject\summary_command_notes\md_img\image-20201119172906827.png)

> XMLConfigBuilder.java

在build方法中将文件流传入XMLConfigBuilder类中来处理

![image-20201119173230726](D:\zyyProject\summary_command_notes\md_img\image-20201119173230726.png)

而该类又将文件流交给了XPathParser去处理

> XPathParser.java

![image-20201119174323144](D:\zyyProject\summary_command_notes\Java\Mybatis源码阅读笔记.assets\image-20201119174323144.png)

通过XPathParser的构造方法将文件流处理成一个org.w3c.dom.Document对象并作为一个属性保存到XPathParser中

> XMLConfigBuilder.java

<img src="D:\zyyProject\summary_command_notes\Java\Mybatis源码阅读笔记.assets\image-20201119175713105.png" alt="image-20201119175713105" style="zoom:150%;" />

最后将含有org.w3c.dom.Document对象的XPathParser作为一个属性保存到XMLConfigBuilder中

> 总结：最终是把文件流转变成了(当然其中还有其他的逻辑处理)一个XMLConfigBuilder对象

###### 2.解析document中的具体内容