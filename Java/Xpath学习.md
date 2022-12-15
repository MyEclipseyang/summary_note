Xpath学习

> http://www.zvon.org/xxl/XPathTutorial/Output_chi/example8.html

### 1.绝对位置
使用符号 /
例如 /html/body

### 2.相对位置
使用符号 //
例如 //table/tr

### 3.获取标签下所有的子标签
使用符号 *
例如 //table/*

### 4.选择所有的有3个祖先元素的BBB元素
/*/*/*/BBB

### 5.选择所有元素
//*

### 6.选择AAA的第一个BBB子元素
/AAA/BBB[1]

### 7.选择AAA的最后一个BBB子元素
/AAA/BBB[last()]

### 8.选择所有的id属性
//@id
【】匹配到的数据
<AAA>
    <BBB 【id = "b1"】/>
    <BBB 【id = "b2"】/>
    <BBB name = "bbb"/>
    <BBB/>
</AAA>

### 9.选择有id属性的BBB元素
//BBB[@id]

### 10.选择有任意属性的BBB元素
//BBB[@*]

### 11.选择没有属性的BBB元素
//BBB[not(@*)]

### 12.选择含有属性id且其值为'b1'的BBB元素
//BBB[@id='b1']

### 13.选择含有属性name且其值(在用normalize-space函数去掉前后空格后)为'bbb'的BBB元素
//BBB[normalize-space(@name)='bbb']

### 14.选择含有2个BBB子元素的元素
//*[count(BBB)=2]

### 15.选择含有2个子元素的元素
//*[count(*)=2]