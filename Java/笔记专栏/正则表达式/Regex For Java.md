## Regex For Java

> 正则表达式在每种语言基本上都会支持，但要注意不同的语言对正则表达式的书写有不同的要求 

### 1.Java中的正则规则

#### 1.1匹配字符

|      |  表达式  |           描述           |
| :--: | :------: | :----------------------: |
|  1   |    .     |       匹配任何字符       |
|  2   |  ^regex  | 文本必须以规定的规则开始 |
|  3   |  refex$  | 文本必须以规定的规则结束 |
|  4   |  [abc]   |   字符集，匹配a、b、c    |
|  5   |  [^abc]  |  匹配a、b、c之外的字符   |
|  6   | [a-d1-7] | 匹配a到d和1-7之间的字符  |
|  7   |   X\|Z   |         匹配X、Z         |
|  8   |    XZ    |          匹配XZ          |
|  9   |    $     |     检查一行是否结束     |

#### 1.2规则缩写

|      | 表达式 |               描述               |
| :--: | :----: | :------------------------------: |
|  1   |   \d   |      任何数字， [0-9]的简写      |
|  2   |   \D   |      非数字，\[^0-9]的简写       |
|  3   |   \s   | 空白字符,  [ \t\n\x0b\r\f]的简写 |
|  4   |   \S   |            非空格字符            |
|  5   |   \w   |  单词字符,  [a-zA-Z_0-9]的简写   |
|  6   |   \W   |         非单词字符 \[^\w]         |
| 7 | \b | 匹配一个单词边界，在一个字字符 [a-zA-Z0-9_]. |

#### 1.3规则重复次数

|      | 表达式 |               描述               |
| :--: | :----: | :------------------------------: |
|  1   |   *    |   出现零次或多次， {0,}的简写    |
|  2   |   +    |  出现一次或更多次， {1,}的简写   |
|  3   |   ？   | 没有出现或出现一次，{0，1}的简写 |
|  4   |  {x}   |            出现了x次             |
|  5   | {x,y}  |       出现了x到y之间的次数       |
|  6   |   *?   |          规则的最小匹配          |

### 2.Java中的正则实现

#### 2.1通过String类

```java
package com.regex;

public class RegEx {

    public static void main(String[] args) {

        String s1 = "a";
        System.out.println("s1=" + s1);

        // Check the entire s1
        // Match any character
        // Rule .
        // ==> true
        boolean match = s1.matches(".");
        System.out.println("-Match . " + match);

        s1 = "abc";
        System.out.println("s1=" + s1);

        // Check the entire s1
        // Match any character
        // Rule .
        // ==> false (Because s1 has three characters)
        match = s1.matches(".");
        System.out.println("-Match . " + match);

        // Check the entire s1
        // Match with any character 0 or more times
        // Combine the rules . and *
        // ==> true
        match = s1.matches(".*");
        System.out.println("-Match .* " + match);

        String s2 = "m";
        System.out.println("s2=" + s2);

        // Check the entire s2
        // Start by m
        // Rule ^
        // ==> true
        match = s2.matches("^m");
        System.out.println("-Match ^m " + match);

        s2 = "mnp";
        System.out.println("s2=" + s2);

        // Check the entire s2
        // Start by m
        // Rule ^
        // ==> false (Because s2 has three characters)
        match = s2.matches("^m");
        System.out.println("-Match ^m " + match);

        // Start by m
        // Next any character, appearing one or more times.
        // Rule ^ and. and +
        // ==> true
        match = s2.matches("^m.+");
        System.out.println("-Match ^m.+ " + match);

        String s3 = "p";
        System.out.println("s3=" + s3);

        // Check s3 ending with p
        // Rule $
        // ==> true
        match = s3.matches("p$");
        System.out.println("-Match p$ " + match);

        s3 = "2nnp";
        System.out.println("s3=" + s3);

        // Check the entire s3
        // End of p
        // ==> false (Because s3 has 4 characters)
        match = s3.matches("p$");
        System.out.println("-Match p$ " + match);

        // Check out the entire s3
        // Any character appearing once.
        // Followed by n, appear one or up to three times.
        // End by p: p $
        // Combine the rules: . , {X, y}, $
        // ==> true

        match = s3.matches(".n{1,3}p$");
        System.out.println("-Match .n{1,3}p$ " + match);

        String s4 = "2ybcd";
        System.out.println("s4=" + s4);

        // Start by 2
        // Next x or y or z
        // Followed by any one or more times.
        // Combine the rules: [abc]. , +
        // ==> true
        match = s4.matches("2[xyz].+");

        System.out.println("-Match 2[xyz].+ " + match);

        String s5 = "2bkbv";

        // Start any one or more times
        // Followed by a or b, or c: [abc]
        // Next z or v: [zv]
        // Followed by any
        // ==> true
        match = s5.matches(".+[abc][zv].*");

        System.out.println("-Match .+[abc][zv].* " + match);
    }
}
```

#### 2.2Pattern和Matcher

##### 2.2.1获取匹配结果

```java
@Test
public void testPatternAndMatcher() {
    Pattern p = Pattern.compile("a*b");
    Matcher m = p.matcher("aaaaab");
    log.info("result={}", m.matches());
}
```

##### 2.2.2获取更过匹配结果

![image-20220505153420917](C:/Users/zyy/AppData/Roaming/Typora/typora-user-images/image-20220505153420917.png)

```java
@Test
public void testUnNameGroup() {

    final String TEXT = "This \t is a \t\t\t String";

    // Spaces appears one or more time.
    String regex = "\\s+";

    Pattern pattern = Pattern.compile(regex);

    Matcher matcher = pattern.matcher(TEXT);

    int i = 0;
    while (matcher.find()) {
        System.out.print("start" + i + " = " + matcher.start());
        System.out.print(" end" + i + " = " + matcher.end());
        System.out.println(" group" + i + " = " + matcher.group());
        i++;
    }

}
```

##### 2.2.3分组

```java
@Test
public void testGroup() {
    // A regular expression
    String regex = "\\s+=\\d+";

    // Writing as three group, by marking ()
    String regex2 = "(\\s+)(=)(\\d+)";

    // Two group
    String regex3 = "(\\s+)(=\\d+)";
}
```

分组可以嵌套，因此需要一个规则索引组。 整个模式被定义为组0，其余组介绍如下类似图：

![image-20220505154750189](C:/Users/zyy/AppData/Roaming/Typora/typora-user-images/image-20220505154750189.png)

##### 2.2.4给规则分组命名

```java
/**
 * JDK >= 7.0
 */
@Test
public void testNameGroup() {
    final String TEXT = " int a = 100;float b= 130;float c= 110 ; ";

    // Use (?<groupName>pattern) to define a group named: groupName
    // Defined group named declare: using (?<declare>...)
    // And a group named value: use: (?<value>..)
    String regex = "(?<declare>\\s*(int|float)\\s+[a-z]\\s*)=(?<value>\\s*\\d+\\s*);";

    Pattern pattern = Pattern.compile(regex);

    Matcher matcher = pattern.matcher(TEXT);

    while (matcher.find()) {
        String group = matcher.group();
        System.out.println(group);
        System.out.println("declare: " + matcher.group("declare"));
        System.out.println("value: " + matcher.group("value"));
        System.out.println("------------------------------");
    }
}
```

##### 2.2.5最小范围匹配

> *？的最佳实践

```java
/**
 * Java >= 7.0
 * use *?
 */
@Test
public void testMinMatch() {
    String TEXT = "<a href='http://HOST/file/FILE1'>File 1</a>"
            + "<a href='http://HOST/file/FILE2'>File 2</a>";

    // Define group named fileName.
    // *? ==> ? after a quantifier makes it a reluctant quantifier.
    // It tries to find the smallest match.
    String normalRegex = "/file/(?<fileName>.*)'>";
    String minMatchRegex = "/file/(?<fileName>.*?)'>";

    Pattern normalPattern = Pattern.compile(normalRegex);
    Matcher normalMatcher = normalPattern.matcher(TEXT);
    while (normalMatcher.find()) {
        System.out.println("normalMatcher-File Name = " + normalMatcher.group("fileName"));
    }

    System.out.println("-------------");

    Pattern minMatchPattern = Pattern.compile(minMatchRegex);
    Matcher minMatchMatcher = minMatchPattern.matcher(TEXT);
    while (minMatchMatcher.find()) {
        System.out.println("minMatchMatcher-File Name = " + minMatchMatcher.group("fileName"));
    }
}
```

> normalMatcher-File Name = FILE1'>File 1\</a>\<a href='http://HOST/file/FILE2
> 
> minMatchMatcher-File Name = FILE1
> minMatchMatcher-File Name = FILE2

### 3.小试牛刀

```java
@Test
public void simpleTest() {
    String prefix = "ACT";
    String testStr = "ACT0001";
    String regex = "^" + prefix + "(?<num>\\d+$)";
    Matcher matcher = Pattern.compile(regex).matcher(testStr);

    if (matcher.matches()) {
        Assert.assertEquals("TEST FAILED", "0001", matcher.group("num"));
    }
}
```
