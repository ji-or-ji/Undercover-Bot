## POST 上传文件流

POST /upload_file_stream

以流式方式上传文件数据到机器人

> Body 请求参数

```json
{
  "stream_id": "uuid-1234-5678",
  "chunk_data": "SGVsbG8gV29ybGQ=",
  "chunk_index": 0,
  "total_chunks": 1,
  "file_size": 11
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» stream_id|body|string| 是 |流 ID|
|» chunk_data|body|string| 否 |分块数据 (Base64)|
|» chunk_index|body|number| 否 |分块索引|
|» total_chunks|body|number| 否 |总分块数|
|» file_size|body|number| 否 |文件总大小|
|» expected_sha256|body|string| 否 |期望的 SHA256|
|» is_complete|body|boolean| 否 |是否完成|
|» filename|body|string| 否 |文件名|
|» reset|body|boolean| 否 |是否重置|
|» verify_only|body|boolean| 否 |是否仅验证|
|» file_retention|body|number| 是 |文件保留时间 (毫秒)|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "type": "stream",
    "stream_id": "uuid-1234-5678",
    "status": "chunk_received",
    "received_chunks": 1,
    "total_chunks": 1
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
