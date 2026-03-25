### 属性

allOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|object|false|none||最后一条消息|
|» self_id|number|true|none||发送者QQ号|
|» user_id|number|true|none||接收者QQ号|
|» time|number|true|none||时间戳|
|» real_seq|string|true|none||消息序号|
|» message_type|string|true|none||消息类型|
|» sender|object|true|none||none|
|»» user_id|number|true|none||用户QQ号|
|»» nickname|string|true|none||用户昵称|
|»» card|string|false|none||用户名片|
|»» role|string|false|none||用户角色|
|» raw_message|string|true|none||原始消息|
|» font|number|true|none||字体大小|
|» sub_type|string|true|none||子类型|
|» message|object|true|none||消息内容|
|» message_format|string|true|none||消息格式|
|» post_type|string|true|none||发布类型|
|» group_id|number|true|none||群号|
|» group_name|string|true|none||群名称|

and

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|object|false|none||OneBot 11 消息信息|
|» message_id|number|true|none||消息ID|
|» message_seq|number|true|none||消息序列号|
|» emoji_likes_list|[object]|true|none||none|
|»» emoji_id|string|true|none||表情符号ID|
|»» emoji_type|string|true|none||表情符号类型|
|»» likes_cnt|string|true|none||点赞数|

<h2 id="tocS_OB11Notify">OB11Notify</h2>

<a id="schemaob11notify"></a>
<a id="schema_OB11Notify"></a>
<a id="tocSob11notify"></a>
<a id="tocsob11notify"></a>

```json
{
  "request_id": 0,
  "invitor_uin": 0,
  "invitor_nick": "string",
  "group_id": 0,
  "group_name": "string",
  "message": "string",
  "checked": true,
  "actor": 0,
  "requester_nick": "string"
}

```

OneBot 11 通知信息
