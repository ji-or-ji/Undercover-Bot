### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|birthday_year|number|false|none||出生年份|
|birthday_month|number|false|none||出生月份|
|birthday_day|number|false|none||出生日期|
|phone_num|string|false|none||手机号|
|email|string|false|none||邮箱|
|category_id|number|false|none||分组ID|
|user_id|number|true|none||QQ号|
|nickname|string|true|none||昵称|
|remark|string|false|none||备注|
|sex|string|false|none||性别|
|level|number|false|none||等级|
|age|number|false|none||年龄|
|qid|string|false|none||QID|
|login_days|number|false|none||登录天数|
|categoryName|string|false|none||分组名称|
|categoryId|number|false|none||分组ID|

<h2 id="tocS_OB11LatestMessage">OB11LatestMessage</h2>

<a id="schemaob11latestmessage"></a>
<a id="schema_OB11LatestMessage"></a>
<a id="tocSob11latestmessage"></a>
<a id="tocsob11latestmessage"></a>

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
  "group_name": "string"
}

```

最后一条消息
