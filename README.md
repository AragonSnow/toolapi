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

## 2. 正则表达式（/regex）
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
#### 3.1.1 参数
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| s  | "" | 是 | 要替换的数据 |
| f  | "" | 是 | 必须是replace |
| p  | "" | 是 | 要替换的关键词,支持正则 |
| t  | "" | 是 | 替换后的内容 |
| r  | "" | 否 | 返回的内容选择是json和纯文本, 默认是返回json,json会先显示转义字符，纯文本不会 |
#### 3.1.2 返回
<font color='red'> 如果r = json,返回值如下：</font><br>
| 参数 | 解释 |
| :------ | :---- |
| 原始字符串 | 输入的内容 |
| 处理后字符串  |  替换后的字符串 |
| 状态  |  运行的状态, 非OK都是异常 |
<font color='red'> 如果r = text,直接返回文本</font><br>

#### 3.1.3  用例
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
## 4 条件(condition)
### 4.1 判断(judge)
判断并返回布尔值
#### 4.1.1 参数
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| s  | "" | 是 | 输入的公式 |
| f  | "" | 是 | 必须是judge |
#### 4.1.2 返回

| 参数 | 解释 |
| :---- | :---- |
| 公式 | 输入的内容 |
| 结果  |  判断结果 |
| 状态  |  运行的状态, 非OK都是异常 |
#### 4.1.3 用例
```
https://toolapi.us-south.cf.appdomain.cloud/condition?f=judge&s=1%20%3E%202
返回：
{
    "公式": "1 > 2",
    "结果": false,
    "状态": "OK"
}
https://toolapi.us-south.cf.appdomain.cloud/condition?f=judge&s=%272%27%3E%271%27
返回：
{
    "公式": "'2'>'1'",
    "结果": true,
    "状态": "OK"
}

```
## 5 加密/解密(Encrypt/Decrypt)
目前仅支持RSA 的PKCS1_v1_5加解密
### 5.1 RSA加密
#### 5.1.1 参数
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| data  | "" | 是 | 要加密的数据 |
| key  | "" | 是 | 加密的公钥，必须以-----BEGIN PUBLIC KEY-----开头，以-----END PUBLIC KEY-----结尾 |
| f  | "" | 是 | 必须是encode |
#### 5.1.2 返回
加密后的密文
#### 5.1.3 方法
支持POST和GET
#### 5.1.4 用例
##### 5.1.4.1 GET
[点我测试](https://toolapi.us-south.cf.appdomain.cloud/rsa?f=encode&key=-----BEGIN%20PRIVATE%20KEY-----MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANrKAX5%2B%2B8LosMeeSFYvouaeKu7uQSwN3b9b9aLBwaF%2Bu9VDG9luUoF57Ll8QMn7XyXTZmhjr8tMvsfRQqMx7yf%2Fu9SAeKNvzUNKJsIqPdXreuNV6HbXz5IR0Yk31Exap7JbsSpu2fp5DQiI6GJvnWIUcEKWe7MEfhPf8R4dqB7LAgMBAAECgYEAjjWbPwN%2B1TO2JCoHzq1r7waD1YXbqqzgo488XCwglb3wjS%2FvnCaPTkVXz0CqRB81uzpraBLTowshPnQQIk9EqMCz7%2BwSfbeZH8v7xUVcExcxJZZlaTPogAZiDnYXiD6LzWzKmxsPn1EkRvemH5jNBGhCFq2IBw%2By%2Bkd%2FEMz26QECQQD9rUzVgf4RkkLE88u%2F4DtNedRNif2v7pFq2Fj9BvnrnJv8t1pHh6geyIeZnHS%2Bycc8qFRwgjbVUnls0MzqiS%2BLAkEA3Mrq2fTkdQObx4963KMxefTqHKz8bFGfy4kmqVHnxg0SHNI41QI8CkTviYWyrqW7VeWf20tMFaEFOgnNnJq1wQJBAKggMlsTE3s7z4rO9YvOph8cDmvxd7QhTjlc9%2BWCuSLBodRlBK2BqBf22YAiZHGKM8Ts30HN21%2BYkKdg317V2y8CQQC5LQKdPDPjI9yiGWcM513WkB9NX5PxcN%2FZP7UKKyR9SXcYbwO1OsOKRVi0%2BUnsChm9J%2FHTZSpxtXOBwrkMkADBAkEAh0ALcGYRjArv0V033k9DEsmfjr2ArdeJBUk5UT4PFHoVvwe3MR5rJLeVybzi2ulLCsCKMCrBKDy45vLgdSZ44g%3D%3D-----END%20PRIVATE%20KEY-----&data=123456)
```
key:-----BEGIN PRIVATE KEY-----MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANrKAX5++8LosMeeSFYvouaeKu7uQSwN3b9b9aLBwaF+u9VDG9luUoF57Ll8QMn7XyXTZmhjr8tMvsfRQqMx7yf/u9SAeKNvzUNKJsIqPdXreuNV6HbXz5IR0Yk31Exap7JbsSpu2fp5DQiI6GJvnWIUcEKWe7MEfhPf8R4dqB7LAgMBAAECgYEAjjWbPwN+1TO2JCoHzq1r7waD1YXbqqzgo488XCwglb3wjS/vnCaPTkVXz0CqRB81uzpraBLTowshPnQQIk9EqMCz7+wSfbeZH8v7xUVcExcxJZZlaTPogAZiDnYXiD6LzWzKmxsPn1EkRvemH5jNBGhCFq2IBw+y+kd/EMz26QECQQD9rUzVgf4RkkLE88u/4DtNedRNif2v7pFq2Fj9BvnrnJv8t1pHh6geyIeZnHS+ycc8qFRwgjbVUnls0MzqiS+LAkEA3Mrq2fTkdQObx4963KMxefTqHKz8bFGfy4kmqVHnxg0SHNI41QI8CkTviYWyrqW7VeWf20tMFaEFOgnNnJq1wQJBAKggMlsTE3s7z4rO9YvOph8cDmvxd7QhTjlc9+WCuSLBodRlBK2BqBf22YAiZHGKM8Ts30HN21+YkKdg317V2y8CQQC5LQKdPDPjI9yiGWcM513WkB9NX5PxcN/ZP7UKKyR9SXcYbwO1OsOKRVi0+UnsChm9J/HTZSpxtXOBwrkMkADBAkEAh0ALcGYRjArv0V033k9DEsmfjr2ArdeJBUk5UT4PFHoVvwe3MR5rJLeVybzi2ulLCsCKMCrBKDy45vLgdSZ44g==-----END PRIVATE KEY-----
data:123456
f:encode
返回：xvDXgDh18KhAl8u6bc87q9GAlDWarbX2U+z1QBrbAXqu6H71Yy/24g9iSPOP5YrGnjLcKwuBENn0Lioe97LQyrYUYxOPbecPWhHmhpLg+QxSlSDfqkp0L2SCHwa+9NlQqUWvCy8ID9mYuHpYu+I5yHMps6twqZWKVEr7Qyk6hy8=

```
##### 5.1.4.1 POST
```
url:https://toolapi.us-south.cf.appdomain.cloud/rsa
Request Payload:
data=1234&f=encode&key=-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDaygF+fvvC6LDHnkhWL6Lmniru
7kEsDd2/W/WiwcGhfrvVQxvZblKBeey5fEDJ+18l02ZoY6/LTL7H0UKjMe8n/7vU
gHijb81DSibCKj3V63rjVeh218+SEdGJN9RMWqeyW7Eqbtn6eQ0IiOhib51iFHBC
lnuzBH4T3/EeHageywIDAQAB
-----END PUBLIC KEY-----
返回：EWRyaIxVrcm0+MFOT8zINkYuOA8ktOunr4jNmxxAlA4oIzPi3b6YYB6jCDDhasmpjFVDI1aYlr6yNyOUZg6EodD0ian+kGn/c008EwVhYojPaw7tShr6nsAZA2UtE5OneKqOu/bQVmLOgwMIWZcWqhKgJ5ncMNrRw0bET+dSuh0=
```
### 5.2 RSA解密
#### 5.1.1 参数
| 参数 | 默认值 | 是否必要参数 | 解释 |
| :----: | :---: | :------------- | :---- |
| data  | "" | 是 | 要解密的数据 |
| key  | "" | 是 | 私钥 必须以-----BEGIN PRIVATE KEY-----开头，以-----END PRIVATE KEY-----结尾|
| f  | "" | 是 | 必须是decode |
#### 5.1.2 返回
解密后的文本
#### 5.1.3 方法
支持POST和GET
#### 5.1.4 用例
##### 5.1.4.1 GET
[点我测试](https://toolapi.us-south.cf.appdomain.cloud/rsa?f=decode&key=-----BEGIN%20PRIVATE%20KEY-----MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANrKAX5%2B%2B8LosMeeSFYvouaeKu7uQSwN3b9b9aLBwaF%2Bu9VDG9luUoF57Ll8QMn7XyXTZmhjr8tMvsfRQqMx7yf%2Fu9SAeKNvzUNKJsIqPdXreuNV6HbXz5IR0Yk31Exap7JbsSpu2fp5DQiI6GJvnWIUcEKWe7MEfhPf8R4dqB7LAgMBAAECgYEAjjWbPwN%2B1TO2JCoHzq1r7waD1YXbqqzgo488XCwglb3wjS%2FvnCaPTkVXz0CqRB81uzpraBLTowshPnQQIk9EqMCz7%2BwSfbeZH8v7xUVcExcxJZZlaTPogAZiDnYXiD6LzWzKmxsPn1EkRvemH5jNBGhCFq2IBw%2By%2Bkd%2FEMz26QECQQD9rUzVgf4RkkLE88u%2F4DtNedRNif2v7pFq2Fj9BvnrnJv8t1pHh6geyIeZnHS%2Bycc8qFRwgjbVUnls0MzqiS%2BLAkEA3Mrq2fTkdQObx4963KMxefTqHKz8bFGfy4kmqVHnxg0SHNI41QI8CkTviYWyrqW7VeWf20tMFaEFOgnNnJq1wQJBAKggMlsTE3s7z4rO9YvOph8cDmvxd7QhTjlc9%2BWCuSLBodRlBK2BqBf22YAiZHGKM8Ts30HN21%2BYkKdg317V2y8CQQC5LQKdPDPjI9yiGWcM513WkB9NX5PxcN%2FZP7UKKyR9SXcYbwO1OsOKRVi0%2BUnsChm9J%2FHTZSpxtXOBwrkMkADBAkEAh0ALcGYRjArv0V033k9DEsmfjr2ArdeJBUk5UT4PFHoVvwe3MR5rJLeVybzi2ulLCsCKMCrBKDy45vLgdSZ44g%3D%3D-----END%20PRIVATE%20KEY-----&data=EWRyaIxVrcm0%2BMFOT8zINkYuOA8ktOunr4jNmxxAlA4oIzPi3b6YYB6jCDDhasmpjFVDI1aYlr6yNyOUZg6EodD0ian%2BkGn%2Fc008EwVhYojPaw7tShr6nsAZA2UtE5OneKqOu%2FbQVmLOgwMIWZcWqhKgJ5ncMNrRw0bET%2BdSuh0%3D)
```
key:-----BEGIN PRIVATE KEY-----MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANrKAX5++8LosMeeSFYvouaeKu7uQSwN3b9b9aLBwaF+u9VDG9luUoF57Ll8QMn7XyXTZmhjr8tMvsfRQqMx7yf/u9SAeKNvzUNKJsIqPdXreuNV6HbXz5IR0Yk31Exap7JbsSpu2fp5DQiI6GJvnWIUcEKWe7MEfhPf8R4dqB7LAgMBAAECgYEAjjWbPwN+1TO2JCoHzq1r7waD1YXbqqzgo488XCwglb3wjS/vnCaPTkVXz0CqRB81uzpraBLTowshPnQQIk9EqMCz7+wSfbeZH8v7xUVcExcxJZZlaTPogAZiDnYXiD6LzWzKmxsPn1EkRvemH5jNBGhCFq2IBw+y+kd/EMz26QECQQD9rUzVgf4RkkLE88u/4DtNedRNif2v7pFq2Fj9BvnrnJv8t1pHh6geyIeZnHS+ycc8qFRwgjbVUnls0MzqiS+LAkEA3Mrq2fTkdQObx4963KMxefTqHKz8bFGfy4kmqVHnxg0SHNI41QI8CkTviYWyrqW7VeWf20tMFaEFOgnNnJq1wQJBAKggMlsTE3s7z4rO9YvOph8cDmvxd7QhTjlc9+WCuSLBodRlBK2BqBf22YAiZHGKM8Ts30HN21+YkKdg317V2y8CQQC5LQKdPDPjI9yiGWcM513WkB9NX5PxcN/ZP7UKKyR9SXcYbwO1OsOKRVi0+UnsChm9J/HTZSpxtXOBwrkMkADBAkEAh0ALcGYRjArv0V033k9DEsmfjr2ArdeJBUk5UT4PFHoVvwe3MR5rJLeVybzi2ulLCsCKMCrBKDy45vLgdSZ44g==-----END PRIVATE KEY-----

data:EWRyaIxVrcm0+MFOT8zINkYuOA8ktOunr4jNmxxAlA4oIzPi3b6YYB6jCDDhasmpjFVDI1aYlr6yNyOUZg6EodD0ian+kGn/c008EwVhYojPaw7tShr6nsAZA2UtE5OneKqOu/bQVmLOgwMIWZcWqhKgJ5ncMNrRw0bET+dSuh0=
f:decode
返回：1234

```
##### 5.1.4.1 POST
```
url:https://toolapi.us-south.cf.appdomain.cloud/rsa
Request Payload:
data={{d}}&f=decode&key=-----BEGIN PRIVATE KEY-----
MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANrKAX5++8LosMee
SFYvouaeKu7uQSwN3b9b9aLBwaF+u9VDG9luUoF57Ll8QMn7XyXTZmhjr8tMvsfR
QqMx7yf/u9SAeKNvzUNKJsIqPdXreuNV6HbXz5IR0Yk31Exap7JbsSpu2fp5DQiI
6GJvnWIUcEKWe7MEfhPf8R4dqB7LAgMBAAECgYEAjjWbPwN+1TO2JCoHzq1r7waD
1YXbqqzgo488XCwglb3wjS/vnCaPTkVXz0CqRB81uzpraBLTowshPnQQIk9EqMCz
7+wSfbeZH8v7xUVcExcxJZZlaTPogAZiDnYXiD6LzWzKmxsPn1EkRvemH5jNBGhC
Fq2IBw+y+kd/EMz26QECQQD9rUzVgf4RkkLE88u/4DtNedRNif2v7pFq2Fj9Bvnr
nJv8t1pHh6geyIeZnHS+ycc8qFRwgjbVUnls0MzqiS+LAkEA3Mrq2fTkdQObx496
3KMxefTqHKz8bFGfy4kmqVHnxg0SHNI41QI8CkTviYWyrqW7VeWf20tMFaEFOgnN
nJq1wQJBAKggMlsTE3s7z4rO9YvOph8cDmvxd7QhTjlc9+WCuSLBodRlBK2BqBf2
2YAiZHGKM8Ts30HN21+YkKdg317V2y8CQQC5LQKdPDPjI9yiGWcM513WkB9NX5Px
cN/ZP7UKKyR9SXcYbwO1OsOKRVi0+UnsChm9J/HTZSpxtXOBwrkMkADBAkEAh0AL
cGYRjArv0V033k9DEsmfjr2ArdeJBUk5UT4PFHoVvwe3MR5rJLeVybzi2ulLCsCK
MCrBKDy45vLgdSZ44g==
-----END PRIVATE KEY-----
返回：1234
```