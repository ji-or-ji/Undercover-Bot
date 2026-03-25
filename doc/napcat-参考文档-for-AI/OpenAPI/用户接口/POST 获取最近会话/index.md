## POST 获取最近会话

POST /get_recent_contact

获取最近会话

> Body 请求参数

```json
{
  "count": 10
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» count|body|any| 是 |获取的数量|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": [
    {
      "peerUin": "123456",
      "peerName": "测试",
      "msgTime": "1734567890",
      "msgId": "12345",
      "lastestMsg": {}
    }
  ],
  "message": "",
  "wording": "",
  "stream": "normal-action"
}
```

```json
{
  "status": "failed",
  "retcode": 1400,
  "data": null,
  "message": "请求参数错误或业务逻辑执行失败",
  "wording": "请求参数错误或业务逻辑执行失败",
  "stream": "normal-action"
}
```

```json
{
  "status": "failed",
  "retcode": 1401,
  "data": null,
  "message": "权限不足",
  "wording": "权限不足",
  "stream": "normal-action"
}
```

```json
{
  "status": "failed",
  "retcode": 1404,
  "data": null,
  "message": "资源不存在",
  "wording": "资源不存在",
  "stream": "normal-action"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|业务响应|Inline|

### 返回数据结构

#### 枚举值

|属性|值|
|---|---|
|stream|stream-action|
|stream|normal-action|
