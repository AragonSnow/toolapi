# toolapi
# 这是什么?
一个简单的工具API
项目仓库[https://github.com/AragonSnow/toolapi](https://github.com/AragonSnow/toolapi)<br>
如果有更多api需求，可以留言给我添加
# 功能
## 1 时间戳转换（/timestamp）
目前仅支持GMT+8 北京时间
### 1.1 参数
|  参数   | 默认值  | 是否必要参数 | 解释 |
| :----: | :---: | :---- | :---- |
| t  | now | 是 |要转换成时间戳的北京时间 |
| ts  | null | 是 | 要转换成北京时间的时间戳 |
| form  | %Y-%m-%d %H:%M:%S | 否 | 输出的时间格式 |
### 1.2 返回值
|  参数  | 解释 |
| :----: | :---- |
| 时间戳 | 转换的时间戳 |
| 时间  |  格式化输出的北京时间 |
| 状态  |  运行的状态, 非OK都是异常 |
### 1.3 用例
```
https://toolapi.us-south.cf.appdomain.cloud/timestamp  
返回现在北京时间
{
    "时间戳": 1586917839,
    "时间": "2020-04-15 10:30:39",
    "状态": "OK"
}
```
```
https://toolapi.us-south.cf.appdomain.cloud/timestamp?ts=1586921249
如果参数带时间戳，会忽略其他参数转换成北京时间
{
    "时间戳": "1586921249",
    "时间": "2020-04-15 11:27:29",
    "状态": "OK"
}
```
```
https://toolapi.us-south.cf.appdomain.cloud/timestamp?t=2020-04-15+11%3a00%3a09
北京时间返回时间戳
{
    "时间戳": 1586919609,
    "时间": "2020-04-15 11:00:09",
    "状态": "OK"
}
```

## 2. 正则表达是（/regex）
正则匹配参数并返回匹配结果
### 2.1 参数
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| data  | "" | 是 | 要匹配的数据 |
| p  | "" | 是 | 正则表达式 |
### 2.2 返回值
|  参数  | 解释 |
| :----: | :---- |
| 数据 | 匹配的结果 |
| 状态  |  运行的状态, 非OK都是异常 |
### 2.3 用例
```
https://toolapi.us-south.cf.appdomain.cloud/regex?data=%7b"code"%3a0%2c"msg"%3a"成功"%2c"data"%3a%7b"users"%3a%5b%7b"name"%3a"张三"%2c"gender"%3a"male"%2c"age"%3a12%7d%2c%7b"name"%3a"李四"%2c"gender"%3a"female"%2c"age"%3a15%7d%2c%7b"name"%3a"王五"%2c"gender"%3a"male"%2c"age"%3a22%7d%2c%7b"name"%3a"赵六"%2c"gender"%3a"male"%2c"age"%3a24%7d%5d%2c"goods"%3a%5b%7b"name"%3a"apple"%2c"price"%3a15%2c"num"%3a200%7d%2c%7b"name"%3a"pear"%2c"price"%3a18%2c"num"%3a100%7d%2c%7b"name"%3a"banana"%2c"price"%3a16%2c"num"%3a210%7d%5d%7d%7d&p=name"%3a"(.%2b%3f)"

测试数据：
{"code":0,"msg":"成功","data":{"users":[{"name":"张三","gender":"male","age":12},{"name":"李四","gender":"female","age":15},{"name":"王五","gender":"male","age":22},{"name":"赵六","gender":"male","age":24}],"goods":[{"name":"apple","price":15,"num":200},{"name":"pear","price":18,"num":100},{"name":"banana","price":16,"num":210}]}}

正则表达式： name":"(.+?)"

返回结果：
{
    "数据": {
        "1": "张三",
        "2": "李四",
        "3": "王五",
        "4": "赵六",
        "5": "apple",
        "6": "pear",
        "7": "banana"
    },
    "状态": "OK"
}
```
## 3 字符串处理(string)
目前实现字符串替换功能
### 3.1 字符串替换(replace)
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| s  | "" | 是 | 要替换的数据 |
| f  | "" | 是 | 必须是replace |
| p  | "" | 是 | 要替换的关键词,支持正则 |
| t  | "" | 是 | 替换后的内容 |
| r  | "" | 否 | 返回的内容选择是json和纯文本, 默认是返回json,json会先显示转义字符，纯文本不会 |
### 3.2 字符串替换(replace)
|  参数  | 解释 |
| :----: | :---- |
| 原始字符串 | 输入的内容 |
| 处理后字符串  |  替换后的字符串 |
| 状态  |  运行的状态, 非OK都是异常 |
text
直接返回替换后的字符串
### 3.1.3  用例
```
返回json
https://toolapi.us-south.cf.appdomain.cloud/string?p=%E4%BA%BA&t=%E5%AD%97%E7%AC%A6%E4%B8%B2&f=replace&r=json&s={%22text%22:%22%E6%88%91%E6%98%AF%E4%BA%BA%22}
s = {"text":"我是人"}
f = replace
p = 人
t = 字符串
r = json   (可不用，默认)
返回
{
    "原始字符串": "{\"text\":\"我是人\"}",
    "处理后字符串": "{\"text\":\"我是字符串\"}",
    "状态": "OK"
}
```
```
返回文本
https://toolapi.us-south.cf.appdomain.cloud/string?p=%E4%BA%BA&t=%E5%AD%97%E7%AC%A6%E4%B8%B2&f=replace&r=text&s={%22text%22:%22%E6%88%91%E6%98%AF%E4%BA%BA%22}
s = {"text":"我是人"}
f = replace
p = 人
t = 字符串
r = text
返回
{"text":"我是字符串"}
```