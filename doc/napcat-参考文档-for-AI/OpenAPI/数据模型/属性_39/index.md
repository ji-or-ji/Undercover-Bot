### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|self_id|number|true|none||发送者QQ号|
|user_id|number|true|none||接收者QQ号|
|time|number|true|none||时间戳|
|real_seq|string|true|none||消息序号|
|message_type|string|true|none||消息类型|
|sender|object|true|none||none|
|» user_id|number|true|none||用户QQ号|
|» nickname|string|true|none||用户昵称|
|» card|string|false|none||用户名片|
|» role|string|false|none||用户角色|
|raw_message|string|true|none||原始消息|
|font|number|true|none||字体大小|
|sub_type|string|true|none||子类型|
|message|object|true|none||消息内容|
|message_format|string|true|none||消息格式|
|post_type|string|true|none||发布类型|
|group_id|number|true|none||群号|
|group_name|string|true|none||群名称|
