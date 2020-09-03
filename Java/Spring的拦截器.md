### Spring的拦截器

```java
/**
 * @author zyy
 * @title: TestIntercept
 * @description: TestIntercept
 * @date 2020/9/3 15:16
 */
public class TestIntercept implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        return false;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
```

#### 1.preHandle

> 触发拦截器时，先顺序执行所有拦截器的preHandle()方法，当其中一个拦截器返回true时则执行下一个拦截器的preHandle()方法,反之则代表该请求没有通过拦截器。

#### 2.postHandle

> 当该拦截器的preHandle()返回true后接着执行该方法

#### 3.afterCompletion

> 当所有拦截器执行完后执行该方法，从最后执行完的拦截器开始