### Gradle学习

#### 1.api compile implementation

> 三者都是用来引入第三方依赖

- api 和 compile作用一样，但是compile将在gradle高版本弃用
- implementation 表示引入的第三方包只能在该项目下使用，依赖该项目的并无法使用