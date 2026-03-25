### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» cmd|body|string| 是 |命令字|
|» data|body|string| 是 |十六进制数据|
|» rsp|body|any| 是 |是否等待响应|
|»» *anonymous*|body|string| 否 |none|
|»» *anonymous*|body|boolean| 否 |none|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": "123456",
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
