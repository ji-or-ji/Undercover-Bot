### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» id|string|false|none||消息ID的短ID映射|
|» seq|number|false|none||消息序列号，优先使用|

#### 枚举值

|属性|值|
|---|---|
|type|reply|

<h2 id="tocS_OB11Message">OB11Message</h2>

<a id="schemaob11message"></a>
<a id="schema_OB11Message"></a>
<a id="tocSob11message"></a>
<a id="tocsob11message"></a>

```json
{
  "real_seq": "string",
  "temp_source": 0,
  "message_sent_type": "string",
  "target_id": 0,
  "self_id": 0,
  "time": 0,
  "message_id": 0,
  "message_seq": 0,
  "real_id": 0,
  "user_id": 0,
  "group_id": 0,
  "group_name": "string",
  "message_type": "private",
  "sub_type": "friend",
  "sender": {
    "user_id": 0,
    "nickname": "string",
    "card": "string",
    "role": "string",
    "sex": "string",
    "age": 0,
    "area": "string",
    "level": "string",
    "title": "string"
  },
  "message": [
    {
      "type": "[",
      "data": {}
    }
  ],
  "message_format": "array",
  "raw_message": "string",
  "font": 0,
  "post_type": "string",
  "raw": {},
  "emoji_likes_list": [
    {
      "emoji_id": "string",
      "emoji_type": "string",
      "likes_cnt": "string"
    }
  ]
}

```

OneBot 11 完整消息对象
