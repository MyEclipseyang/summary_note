### Spring Schedule Cron

#### 1.Cron表达式使用格式

| Seconds | Minutes | Hours | DayofMonth | Month | DayofWeek  | [Year]    |
| ------- | ------- | ----- | ---------- | ----- | ---------- | --------- |
| 秒      | 分      | 时    | 月中的某天 | 月    | 周中的某天 | [年 可选] |

| 字段名   | 允许的值        | 允许的特殊字符    |
| -------- | --------------- | ----------------- |
| 秒       | 0-59            | ， - * /          |
| 分       | 0-59            | ， - * /          |
| 小时     | 0-23            | ， - * /          |
| 月内日期 | 1-32            | ， - * ？ / L W C |
| 月       | 1-12 或 JAN-DEC | ， - * /          |
| 周内日期 | 1-7 或 SUN-SAT  | ， - * ？ / L C # |
| 年       | 留空，1980-2099 | ， - * /          |

#### 2.特殊符号代表的含义

> 1. \*：匹配该域的任意值；如*用在分所在的域，表示每分钟都会触发事件。
> 2. ?：匹配该域的任意值。月份的天河周的天互相冲突，必须将其中一个设置为?
> 3. -：匹配一个特定的范围值；如时所在的域的值是10-12，表示10、11、12点的时候会触发事件。
> 4. ,：匹配多个指定的值；如周所在的域的值是2,4,6，表示在周一、周三、周五就会触发事件(1表示周日，2表示周一，3表示周二，以此类推，7表示周六)。
> 5. /：左边是开始触发时间，右边是每隔固定时间触发一次事件，如秒所在的域的值是5/15，表示5秒、20秒、35秒、50秒的时候都触发一次事件。
> 6. L：last，最后的意思，如果是用在天这个域，表示月的最后一天，如果是用在周所在的域，如6L，表示某个月最后一个周五。（外国周日是星耀日，周一是月耀日，一周的开始是周日，所以1L=周日，6L=周五。）
> 7. W：weekday，工作日的意思。如天所在的域的值是15W，表示本月15日最近的工作日，如果15日是周六，触发器将触发上14日周五。如果15日是周日，触发器将触发16日周一。如果15日不是周六或周日，而是周一至周五的某一个，那么它就在15日当天触发事件。
> 8. \#：用来指定每个月的第几个星期几，如6#3表示某个月的第三个星期五

#### 3.简单举例

> 每分钟执行一次： 0 0/1 * * * *

> 每天执行一次：0 0 0 0/1 * *

> 每个月执行一次：0 0 0 0 1/1 *