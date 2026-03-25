### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|real_seq|string|false|none||真实序列号|
|temp_source|number|false|none||临时会话来源|
|message_sent_type|string|false|none||消息发送类型|
|target_id|number|false|none||目标ID|
|self_id|number|false|none||机器人QQ号|
|time|number|true|none||消息时间戳|
|message_id|number|true|none||消息ID|
|message_seq|number|true|none||消息序列号|
|real_id|number|true|none||真实ID|
|user_id|any|true|none||发送者QQ号|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|number|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|group_id|any|false|none||群号|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|number|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|group_name|string|false|none||群名称|
|message_type|string|true|none||消息类型|
|sub_type|string|false|none||消息子类型|
|sender|[OB11Sender](#schemaob11sender)|true|none||OneBot 11 发送者信息|
|message|any|true|none||消息内容|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|[[OB11MessageData](#schemaob11messagedata)]|false|none||[OneBot 11 消息段]|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|message_format|string|true|none||消息格式|
|raw_message|string|true|none||原始消息|
|font|number|true|none||字体|
|post_type|string|false|none||上报类型|
|raw|object|false|none||原始消息对象|
|emoji_likes_list|[object]|false|none||表情点赞列表|
|» emoji_id|string|true|none||表情ID|
|» emoji_type|string|true|none||表情类型|
|» likes_cnt|string|true|none||点赞数|

#### 枚举值

|属性|值|
|---|---|
|message_type|private|
|message_type|group|
|sub_type|friend|
|sub_type|group|
|sub_type|normal|
|message_format|array|
|message_format|string|

<h2 id="tocS_OB11MessageText">OB11MessageText</h2>

<a id="schemaob11messagetext"></a>
<a id="schema_OB11MessageText"></a>
<a id="tocSob11messagetext"></a>
<a id="tocsob11messagetext"></a>

```json
{
  "type": "text",
  "data": {
    "text": "string"
  }
}

```

纯文本消息段
