### 第二章 简单的HTTP协议

#### HTTP的请求方法

> GET POST PUT DELETE HEAD (HTTP1.1 OPTION TRACE CONNECT) 已废弃1.1之后：LINK UNLINK

```http
GET /index.html HTTP/1.1
Host: hackr.jp
```

```http
POST /submit.cgi HTTP/1.1
HOST: hackr.jp
Content-Length: 1560
```

#### 持久连接节省通信量和管线化

|      | 文档大小 | 请求方式 | 请求次数 |
| ---- | :------: | :------: | :------: |
| 以前 |   较小   |   同步   |   一次   |
| 现在 |   较大   |   异步   |   多次   |

- 在目前的web应用中如果不使用持久连接就会造成大量不必要的TCP连接和断开带来的资源消耗。持久连接的特点是只要一方没有明确提出断开，则保持TCP连接状态。
- 管线化实现了在一次TCP连接中能发起多次HTTP请求

#### 使用Cookie进行状态管理

> HTTP是无状态协议，不对之前发生过的请求和响应的状态进行管理

针对在web应用中需要对用户的状态进行保存，引入了Cookie技术，客户端获取从服务段返回的头部信息里Set-Cookie信息并在下次请求放入请求报文中发送。

- ##### 请求报文（没有 Cookie 信息的状态）

```http
GET /reader/ HTTP/1.1
Host: hackr.jp
```

- ##### 首部字段内没有Cookie的相关信息

  响应报文（服务器端生成 Cookie 信息）

```http
HTTP/1.1 200 OK
Date: Thu, 12 Jul 2012 07:12:20 GMT
Server: Apache
＜Set-Cookie: sid=1342077140226724; path=/; expires=Wed,
10-Oct-12 07:12:20 GMT＞
Content-Type: text/plain; charset=UTF-8
```

- ##### 请求报文（自动发送保存着的 Cookie 信息）

```http
GET /image/ HTTP/1.1
Host: hackr.jp
Cookie: sid=1342077140226724
```

