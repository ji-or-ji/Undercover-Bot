### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» group_id|body|string| 是 |群号|
|» content|body|string| 是 |公告内容|
|» image|body|string| 否 |公告图片路径或 URL|
|» pinned|body|any| 是 |是否置顶 (0/1)|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|
|» type|body|any| 是 |类型 (默认为 1)|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|
|» confirm_required|body|any| 是 |是否需要确认 (0/1)|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|
|» is_show_edit_card|body|any| 是 |是否显示修改群名片引导 (0/1)|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|
|» tip_window_type|body|any| 是 |弹窗类型 (默认为 0)|
|»» *anonymous*|body|number| 否 |none|
|»» *anonymous*|body|string| 否 |none|

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
