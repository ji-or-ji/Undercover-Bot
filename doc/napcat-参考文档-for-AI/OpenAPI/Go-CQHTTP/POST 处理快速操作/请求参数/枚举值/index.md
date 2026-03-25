#### 枚举值

|属性|值|
|---|---|
|»»»»» type|text|
|»»»»» type|face|
|»»»»» type|mface|
|»»»»» type|at|
|»»»»» type|reply|
|»»»»» type|image|
|»»»»» type|record|
|»»»»» type|video|
|»»»»» type|file|
|»»»»» type|music|
|»»»»»» type|qq|
|»»»»»» type|163|
|»»»»»» type|kugou|
|»»»»»» type|migu|
|»»»»»» type|kuwo|
|»»»»» type|music|
|»»»»»» type|qq|
|»»»»»» type|163|
|»»»»»» type|kugou|
|»»»»»» type|migu|
|»»»»»» type|kuwo|
|»»»»»» type|custom|
|»»»»» type|poke|
|»»»»» type|dice|
|»»»»» type|rps|
|»»»»» type|contact|
|»»»»»» type|qq|
|»»»»»» type|group|
|»»»»» type|location|
|»»»»» type|json|
|»»»»» type|xml|
|»»»»» type|markdown|
|»»»»» type|miniapp|
|»»»»» type|node|
|»»»»» type|forward|
|»»»»» type|onlinefile|
|»»»»» type|flashtransfer|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {},
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
