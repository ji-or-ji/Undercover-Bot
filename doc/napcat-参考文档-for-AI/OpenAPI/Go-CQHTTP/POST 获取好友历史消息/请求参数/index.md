### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» user_id|body|string| 是 |用户QQ|
|» message_seq|body|string| 否 |起始消息序号|
|» count|body|number| 是 |获取消息数量|
|» reverse_order|body|boolean| 是 |是否反向排序|
|» disable_get_url|body|boolean| 是 |是否禁用获取URL|
|» parse_mult_msg|body|boolean| 是 |是否解析合并消息|
|» quick_reply|body|boolean| 是 |是否快速回复|
|» reverseOrder|body|boolean| 是 |是否反向排序(旧版本兼容)|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "messages": []
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
