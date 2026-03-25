## POST 处理快速操作

POST /.handle_quick_operation

处理来自事件上报的快速操作请求

> Body 请求参数

```json
{
  "context": {},
  "operation": {}
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» context|body|object| 是 |事件上下文|
|»» time|body|number| 是 |事件发生时间|
|»» self_id|body|number| 是 |收到事件的机器人 QQ 号|
|»» post_type|body|string| 是 |上报类型|
|»» message_type|body|string| 否 |消息类型|
|»» sub_type|body|string| 否 |消息子类型|
|»» user_id|body|string| 是 |发送者 QQ 号|
|»» group_id|body|string| 否 |群号|
|»» message_id|body|number| 否 |消息 ID|
|»» message_seq|body|number| 否 |消息序列号|
|»» real_id|body|number| 否 |真实消息 ID|
|»» sender|body|object| 否 |none|
|»»» user_id|body|string| 是 |用户ID|
|»»» nickname|body|string| 是 |昵称|
|»»» sex|body|string| 否 |性别|
|»»» age|body|number| 否 |年龄|
|»»» card|body|string| 否 |群名片|
|»»» level|body|string| 否 |群等级|
|»»» role|body|string| 否 |群角色|
|»» message|body|object| 否 |消息内容|
|»» message_format|body|string| 否 |消息格式|
|»» raw_message|body|string| 否 |原始消息内容|
|»» font|body|number| 否 |字体|
|»» notice_type|body|string| 否 |通知类型|
|»» meta_event_type|body|string| 否 |元事件类型|
|» operation|body|object| 是 |快速操作内容|
|»» reply|body|any| 否 |OneBot 11 消息混合类型|
|»»» *anonymous*|body|[anyOf]| 否 |[OneBot 11 消息段]|
|»»»» *anonymous*|body|[OB11MessageText](#schemaob11messagetext)| 否 |纯文本消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» text|body|string| 是 |纯文本内容|
|»»»» *anonymous*|body|[OB11MessageFace](#schemaob11messageface)| 否 |QQ表情消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» id|body|string| 是 |表情ID|
|»»»»»» resultId|body|string| 否 |结果ID|
|»»»»»» chainCount|body|number| 否 |连击数|
|»»»» *anonymous*|body|[OB11MessageMFace](#schemaob11messagemface)| 否 |商城表情消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» emoji_package_id|body|number| 是 |表情包ID|
|»»»»»» emoji_id|body|string| 是 |表情ID|
|»»»»»» key|body|string| 是 |表情key|
|»»»»»» summary|body|string| 是 |表情摘要|
|»»»» *anonymous*|body|[OB11MessageAt](#schemaob11messageat)| 否 |@消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» qq|body|string| 是 |QQ号或all|
|»»»»»» name|body|string| 否 |显示名称|
|»»»» *anonymous*|body|[OB11MessageReply](#schemaob11messagereply)| 否 |回复消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» id|body|string| 否 |消息ID的短ID映射|
|»»»»»» seq|body|number| 否 |消息序列号，优先使用|
|»»»» *anonymous*|body|[OB11MessageImage](#schemaob11messageimage)| 否 |图片消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|any| 是 |none|
|»»»»»» *anonymous*|body|object| 否 |文件消息段基础数据|
|»»»»»»» file|body|string| 是 |文件路径/URL/file:///|
|»»»»»»» path|body|string| 否 |文件路径|
|»»»»»»» url|body|string| 否 |文件URL|
|»»»»»»» name|body|string| 否 |文件名|
|»»»»»»» thumb|body|string| 否 |缩略图|
|»»»»»» *anonymous*|body|object| 否 |none|
|»»»»»»» summary|body|string| 否 |图片摘要|
|»»»»»»» sub_type|body|number| 否 |图片子类型|
|»»»» *anonymous*|body|[OB11MessageRecord](#schemaob11messagerecord)| 否 |语音消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|[FileBaseData](#schemafilebasedata)| 是 |文件消息段基础数据|
|»»»»»» file|body|string| 是 |文件路径/URL/file:///|
|»»»»»» path|body|string| 否 |文件路径|
|»»»»»» url|body|string| 否 |文件URL|
|»»»»»» name|body|string| 否 |文件名|
|»»»»»» thumb|body|string| 否 |缩略图|
|»»»» *anonymous*|body|[OB11MessageVideo](#schemaob11messagevideo)| 否 |视频消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|[FileBaseData](#schemafilebasedata)| 是 |文件消息段基础数据|
|»»»»»» file|body|string| 是 |文件路径/URL/file:///|
|»»»»»» path|body|string| 否 |文件路径|
|»»»»»» url|body|string| 否 |文件URL|
|»»»»»» name|body|string| 否 |文件名|
|»»»»»» thumb|body|string| 否 |缩略图|
|»»»» *anonymous*|body|[OB11MessageFile](#schemaob11messagefile)| 否 |文件消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|[FileBaseData](#schemafilebasedata)| 是 |文件消息段基础数据|
|»»»»»» file|body|string| 是 |文件路径/URL/file:///|
|»»»»»» path|body|string| 否 |文件路径|
|»»»»»» url|body|string| 否 |文件URL|
|»»»»»» name|body|string| 否 |文件名|
|»»»»»» thumb|body|string| 否 |缩略图|
|»»»» *anonymous*|body|[OB11MessageIdMusic](#schemaob11messageidmusic)| 否 |ID音乐消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» type|body|string| 是 |音乐平台类型|
|»»»»»» id|body|any| 是 |音乐ID|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»» *anonymous*|body|[OB11MessageCustomMusic](#schemaob11messagecustommusic)| 否 |自定义音乐消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» type|body|string| 是 |音乐平台类型|
|»»»»»» id|body|null| 是 |none|
|»»»»»» url|body|string| 是 |点击后跳转URL|
|»»»»»» audio|body|string| 否 |音频URL|
|»»»»»» title|body|string| 否 |音乐标题|
|»»»»»» image|body|string| 是 |封面图片URL|
|»»»»»» content|body|string| 否 |音乐简介|
|»»»» *anonymous*|body|[OB11MessagePoke](#schemaob11messagepoke)| 否 |戳一戳消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» type|body|string| 是 |戳一戳类型|
|»»»»»» id|body|string| 是 |戳一戳ID|
|»»»» *anonymous*|body|[OB11MessageDice](#schemaob11messagedice)| 否 |骰子消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» result|body|any| 是 |骰子结果|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»» *anonymous*|body|[OB11MessageRPS](#schemaob11messagerps)| 否 |猜拳消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» result|body|any| 是 |猜拳结果|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»» *anonymous*|body|[OB11MessageContact](#schemaob11messagecontact)| 否 |联系人消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» type|body|string| 是 |联系人类型|
|»»»»»» id|body|string| 是 |联系人ID|
|»»»» *anonymous*|body|[OB11MessageLocation](#schemaob11messagelocation)| 否 |位置消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» lat|body|any| 是 |纬度|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»» lon|body|any| 是 |经度|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»» title|body|string| 否 |标题|
|»»»»»» content|body|string| 否 |内容|
|»»»» *anonymous*|body|[OB11MessageJson](#schemaob11messagejson)| 否 |JSON消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» data|body|any| 是 |JSON数据|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»»» *anonymous*|body|object| 否 |none|
|»»»»»» config|body|object| 否 |none|
|»»»»»»» token|body|string| 是 |token|
|»»»» *anonymous*|body|[OB11MessageXml](#schemaob11messagexml)| 否 |XML消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» data|body|string| 是 |XML数据|
|»»»» *anonymous*|body|[OB11MessageMarkdown](#schemaob11messagemarkdown)| 否 |Markdown消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» content|body|string| 是 |Markdown内容|
|»»»» *anonymous*|body|[OB11MessageMiniApp](#schemaob11messageminiapp)| 否 |小程序消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» data|body|string| 是 |小程序数据|
|»»»» *anonymous*|body|[OB11MessageNode](#schemaob11messagenode)| 否 |合并转发消息节点|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» id|body|string| 否 |转发消息ID|
|»»»»»» user_id|body|any| 否 |发送者QQ号|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»» uin|body|any| 否 |发送者QQ号(兼容go-cqhttp)|
|»»»»»»» *anonymous*|body|number| 否 |none|
|»»»»»»» *anonymous*|body|string| 否 |none|
|»»»»»» nickname|body|string| 是 |发送者昵称|
|»»»»»» name|body|string| 否 |发送者昵称(兼容go-cqhttp)|
|»»»»»» content|body|object| 是 |消息内容 (OB11MessageMixType)|
|»»»»»» source|body|string| 否 |消息来源|
|»»»»»» news|body|[object]| 否 |none|
|»»»»»»» text|body|string| 是 |新闻文本|
|»»»»»» summary|body|string| 否 |摘要|
|»»»»»» prompt|body|string| 否 |提示|
|»»»»»» time|body|string| 否 |时间|
|»»»» *anonymous*|body|[OB11MessageForward](#schemaob11messageforward)| 否 |合并转发消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» id|body|string| 是 |合并转发ID|
|»»»»»» content|body|object| 否 |消息内容 (OB11Message[])|
|»»»» *anonymous*|body|[OB11MessageOnlineFile](#schemaob11messageonlinefile)| 否 |在线文件消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» msgId|body|string| 是 |消息ID|
|»»»»»» elementId|body|string| 是 |元素ID|
|»»»»»» fileName|body|string| 是 |文件名|
|»»»»»» fileSize|body|string| 是 |文件大小|
|»»»»»» isDir|body|boolean| 是 |是否为目录|
|»»»» *anonymous*|body|[OB11MessageFlashTransfer](#schemaob11messageflashtransfer)| 否 |QQ闪传消息段|
|»»»»» type|body|string| 是 |none|
|»»»»» data|body|object| 是 |none|
|»»»»»» fileSetId|body|string| 是 |文件集ID|
|»»» *anonymous*|body|string| 否 |none|
|»»» *anonymous*|body|any| 否 |OneBot 11 消息段|
|»»»» *anonymous*|body|[OB11MessageText](#schemaob11messagetext)| 否 |纯文本消息段|
|»»»» *anonymous*|body|[OB11MessageFace](#schemaob11messageface)| 否 |QQ表情消息段|
|»»»» *anonymous*|body|[OB11MessageMFace](#schemaob11messagemface)| 否 |商城表情消息段|
|»»»» *anonymous*|body|[OB11MessageAt](#schemaob11messageat)| 否 |@消息段|
|»»»» *anonymous*|body|[OB11MessageReply](#schemaob11messagereply)| 否 |回复消息段|
|»»»» *anonymous*|body|[OB11MessageImage](#schemaob11messageimage)| 否 |图片消息段|
|»»»» *anonymous*|body|[OB11MessageRecord](#schemaob11messagerecord)| 否 |语音消息段|
|»»»» *anonymous*|body|[OB11MessageVideo](#schemaob11messagevideo)| 否 |视频消息段|
|»»»» *anonymous*|body|[OB11MessageFile](#schemaob11messagefile)| 否 |文件消息段|
|»»»» *anonymous*|body|[OB11MessageIdMusic](#schemaob11messageidmusic)| 否 |ID音乐消息段|
|»»»» *anonymous*|body|[OB11MessageCustomMusic](#schemaob11messagecustommusic)| 否 |自定义音乐消息段|
|»»»» *anonymous*|body|[OB11MessagePoke](#schemaob11messagepoke)| 否 |戳一戳消息段|
|»»»» *anonymous*|body|[OB11MessageDice](#schemaob11messagedice)| 否 |骰子消息段|
|»»»» *anonymous*|body|[OB11MessageRPS](#schemaob11messagerps)| 否 |猜拳消息段|
|»»»» *anonymous*|body|[OB11MessageContact](#schemaob11messagecontact)| 否 |联系人消息段|
|»»»» *anonymous*|body|[OB11MessageLocation](#schemaob11messagelocation)| 否 |位置消息段|
|»»»» *anonymous*|body|[OB11MessageJson](#schemaob11messagejson)| 否 |JSON消息段|
|»»»» *anonymous*|body|[OB11MessageXml](#schemaob11messagexml)| 否 |XML消息段|
|»»»» *anonymous*|body|[OB11MessageMarkdown](#schemaob11messagemarkdown)| 否 |Markdown消息段|
|»»»» *anonymous*|body|[OB11MessageMiniApp](#schemaob11messageminiapp)| 否 |小程序消息段|
|»»»» *anonymous*|body|[OB11MessageNode](#schemaob11messagenode)| 否 |合并转发消息节点|
|»»»» *anonymous*|body|[OB11MessageForward](#schemaob11messageforward)| 否 |合并转发消息段|
|»»»» *anonymous*|body|[OB11MessageOnlineFile](#schemaob11messageonlinefile)| 否 |在线文件消息段|
|»»»» *anonymous*|body|[OB11MessageFlashTransfer](#schemaob11messageflashtransfer)| 否 |QQ闪传消息段|
|»» auto_escape|body|boolean| 否 |是否作为纯文本发送|
|»» at_sender|body|boolean| 否 |是否 @ 发送者|
|»» delete|body|boolean| 否 |是否撤回该消息|
|»» kick|body|boolean| 否 |是否踢出发送者|
|»» ban|body|boolean| 否 |是否禁言发送者|
|»» ban_duration|body|number| 否 |禁言时长|
|»» approve|body|boolean| 否 |是否同意请求/加群|
|»» remark|body|string| 否 |好友备注|
|»» reason|body|string| 否 |拒绝理由|

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
