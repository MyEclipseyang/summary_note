### Version Number模式

#### 1.介绍

保证对同一个实体的同步更新

#### 2.代码示例

```java
@Data
@AllArgsConstructor
public class Book implements Cloneable{
    private String id;
    private String name;

    private Long version;

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

<!-- more -->

```java
public class BookRepository {
    private Map<String, Book> bookMap = new HashMap<>();
    public BookRepository(){
        bookMap.put("1", new Book("1", "Head First Java", 1L));
    }

    public boolean updateById(Book newBook) throws Exception {
        Book oldBook = bookMap.get(newBook.getId());
        if(oldBook == null){
            throw new Exception("不存在该书籍！");
        }
        if(!newBook.getVersion().equals(oldBook.getVersion())){
            throw new Exception("存在版本冲突！");
        }
        newBook.setVersion(newBook.getVersion() + 1);
        bookMap.put(newBook.getId(), newBook);
        return true;
    }

    public Book getById(String id){
        try {
            return (Book) bookMap.get(id).clone();
        } catch (CloneNotSupportedException e) {
            return null;
        }
    }
}
```

#### 3.测试

```java
@Test
public void test(){
    BookRepository bookRepository = new BookRepository();
    Book zsBook = bookRepository.getById("1");
    Book lsBook = bookRepository.getById("1");

    //张三改动提交
    zsBook.setName("Head First Design Pattern");
    try {
        bookRepository.updateById(zsBook);
    } catch (Exception e) {
        System.out.println(e.getMessage());
    }
    System.out.println(bookRepository.getById("1"));

    System.out.println("--------------");
    //李四之后也改动提交
    lsBook.setName("Head First Java1");
    try {
        bookRepository.updateById(lsBook);
    } catch (Exception e) {
        System.out.println(e.getMessage());
    }
    System.out.println(bookRepository.getById("1"));
}
```

> Book(id=1, name=Head First Design Pattern, version=2)
>
> --------------
>
> 存在版本冲突！
> Book(id=1, name=Head First Design Pattern, version=2)