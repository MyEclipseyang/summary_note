### Tomcat
> 当客户请求某个资源时，HTTP服务器会用一个ServletRequest对象把客户的请求信息封 装起来，然后调用Servlet容器的service方法，Servlet容器拿到请求后，根据请求的URL 和Servlet的映射关系，找到相应的Servlet，如果Servlet还没有被加载，就用反射机制创 建这个Servlet，并调用Servlet的init方法来完成初始化，接着调用Servlet的service方法 来处理请求，把ServletResponse对象返回给HTTP服务器，HTTP服务器会把响应发送给客户端

#### 1.核心功能
- 处理Socket连接  (对应组件 Connectot负责对外交流)
- 管理Servlet    (对应组件 Container负责内部处理)

#### 2.Tomcat架构设计
- 连接器Coyoto(Tomcat的连接器框架)

> 客户端通过Coyote与服务器建立连接、发送请求并接受响应,Coyote 将Socket 输入转换封装为 Request 对象，交由Catalina 容器进行处理，处理请求完成后, Catalina 通过Coyote 提供的Response 对象将结果写入输出流 。

- 容器Catalina(**核心**：Tomcat的Servlet容器框架)

- Jasper(JSP引擎)

- JavaEL(EL表达式)

- Naming(命名服务)

- Juli(日志服务)