### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|message_type|string|false|none||消息类型|
|user_id|string|false|none||用户QQ号|
|group_id|string|false|none||群号|
|message|[OB11MessageMixType](#schemaob11messagemixtype)|true|none||OneBot 11 消息混合类型|
|messages|[OB11MessageMixType](#schemaob11messagemixtype)|false|none||OneBot 11 消息混合类型|
|auto_escape|any|false|none||是否作为纯文本发送|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|boolean|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|source|string|false|none||消息来源|
|news|[object]|false|none||none|
|» text|string|true|none||文本|
|summary|string|false|none||摘要|
|prompt|string|false|none||提示|
|time|string|false|none||时间|

#### 枚举值

|属性|值|
|---|---|
|message_type|private|
|message_type|group|

<h2 id="tocS_OB11Sender">OB11Sender</h2>

<a id="schemaob11sender"></a>
<a id="schema_OB11Sender"></a>
<a id="tocSob11sender"></a>
<a id="tocsob11sender"></a>

```json
{
  "user_id": 0,
  "nickname": "string",
  "card": "string",
  "role": "string",
  "sex": "string",
  "age": 0,
  "area": "string",
  "level": "string",
  "title": "string"
}

```

OneBot 11 发送者信息
