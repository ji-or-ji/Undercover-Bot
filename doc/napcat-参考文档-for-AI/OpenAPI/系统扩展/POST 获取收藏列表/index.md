## POST 获取收藏列表

POST /get_collection_list

> Body 请求参数

```json
{
  "category": "0",
  "count": "50"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» category|body|string| 是 |分类ID|
|» count|body|string| 是 |获取数量|

> 返回示例

> 业务响应

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "errCode": 0,
    "errMsg": "",
    "collectionSearchList": {
      "collectionItemList": [
        {
          "cid": "123456",
          "type": 8,
          "status": 1,
          "author": {
            "type": 2,
            "numId": "123456",
            "strId": "昵称",
            "groupId": "123456",
            "groupName": "群名",
            "uid": "123456"
          },
          "bid": 1,
          "category": 1,
          "createTime": "1769169157000",
          "collectTime": "1769413477691",
          "modifyTime": "1769413477691",
          "sequence": "1769413476735",
          "shareUrl": "",
          "customGroupId": 0,
          "securityBeat": false,
          "summary": {
            "textSummary": null,
            "linkSummary": null,
            "gallerySummary": null,
            "audioSummary": null,
            "videoSummary": null,
            "fileSummary": null,
            "locationSummary": null,
            "richMediaSummary": {
              "title": "",
              "subTitle": "",
              "brief": "text",
              "picList": [],
              "contentType": 1,
              "originalUri": "",
              "publisher": "",
              "richMediaVersion": 0
            }
          }
        }
      ],
      "hasMore": false,
      "bottomTimeStamp": "1769413477691"
    }
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
