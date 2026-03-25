### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» user_id|body|string| 是 |对方 QQ 号|
|» remark|body|string| 是 |备注内容|

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
  "message": "备注设置失败（好友不存在或非法输入）",
  "wording": "备注设置失败（好友不存在或非法输入）",
  "stream": "normal-action"
}
```
