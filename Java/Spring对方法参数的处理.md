### Spring对方法参数的处理

```java
/**
 * @author zyy
 * @title: TestMethodResolver
 * @description: TODO
 * @date 2020/9/3 15:47
 */
public class TestMethodResolver implements HandlerMethodArgumentResolver {
    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return false;
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
        return null;
    }
}
```

#### 1.supportsParameter

> 检查该参数的类型是否可以被该类处理

#### 2.resolveArgument

> 返回处理后的实例