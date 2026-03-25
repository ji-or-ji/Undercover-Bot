## POST 上传群文件

POST /upload_group_file

上传资源路径或URL指定的文件到指定群聊的文件系统中

> Body 请求参数

```json
{
  "group_id": "123456",
  "file": "/path/to/file",
  "name": "test.txt"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» group_id|body|string| 是 |群号|
|» file|body|string| 是 |资源路径或URL|
|» name|body|string| 是 |文件名|
|» folder|body|string| 否 |父目录 ID|
|» folder_id|body|string| 否 |父目录 ID (兼容性字段)|
|» upload_file|body|boolean| 是 |是否执行上传|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "file_id": "file_uuid_123"
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
