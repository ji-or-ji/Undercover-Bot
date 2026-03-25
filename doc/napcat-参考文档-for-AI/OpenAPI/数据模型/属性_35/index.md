### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|group_all_shut|number|true|none||是否全员禁言|
|group_remark|string|true|none||群备注|
|group_id|number|true|none||群号|
|group_name|string|true|none||群名称|
|member_count|number|false|none||成员人数|
|max_member_count|number|false|none||最大成员人数|

<h2 id="tocS_OB11ActionMessage">OB11ActionMessage</h2>

<a id="schemaob11actionmessage"></a>
<a id="schema_OB11ActionMessage"></a>
<a id="tocSob11actionmessage"></a>
<a id="tocsob11actionmessage"></a>

```json
{
  "self_id": 0,
  "user_id": 0,
  "time": 0,
  "real_seq": "string",
  "message_type": "string",
  "sender": {
    "user_id": 0,
    "nickname": "string",
    "card": "string",
    "role": "string"
  },
  "raw_message": "string",
  "font": 0,
  "sub_type": "string",
  "message": {},
  "message_format": "string",
  "post_type": "string",
  "group_id": 0,
  "group_name": "string",
  "message_id": 0,
  "message_seq": 0,
  "emoji_likes_list": [
    {
      "emoji_id": "string",
      "emoji_type": "string",
      "likes_cnt": "string"
    }
  ]
}

```

OneBot 11 消息信息
