### Mybatis源码分析

1.解析配置文件

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

上图~

![image-20220105174555556](https://gitee.com/BossZyy/note_img/raw/master/image-20220105174555556.png)
