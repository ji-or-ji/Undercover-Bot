## POST 获取群相册列表

POST /get_qun_album_list

> Body 请求参数

```json
{
  "group_id": "123456",
  "attach_info": ""
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» group_id|body|string| 是 |群号|
|» attach_info|body|string| 否 |附加信息（用于分页，从上一次返回结果中获取）|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "album_list": [
      {
        "album_id": "album_1",
        "album_name": "测试相册",
        "cover_url": "http://example.com/cover.jpg",
        "create_time": 1734567890
      }
    ],
    "attach_info": "",
    "has_more": false
  },
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
