### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|request_id|number|true|none||请求ID|
|invitor_uin|number|true|none||邀请者QQ|
|invitor_nick|string|true|none||邀请者昵称|
|group_id|number|true|none||群号|
|group_name|string|true|none||群名称|
|message|string|true|none||附言|
|checked|boolean|true|none||是否已处理|
|actor|number|true|none||操作者QQ|
|requester_nick|string|true|none||申请者昵称|

<h2 id="tocS_OB11User">OB11User</h2>

<a id="schemaob11user"></a>
<a id="schema_OB11User"></a>
<a id="tocSob11user"></a>
<a id="tocsob11user"></a>

```json
{
  "birthday_year": 0,
  "birthday_month": 0,
  "birthday_day": 0,
  "phone_num": "string",
  "email": "string",
  "category_id": 0,
  "user_id": 0,
  "nickname": "string",
  "remark": "string",
  "sex": "string",
  "level": 0,
  "age": 0,
  "qid": "string",
  "login_days": 0,
  "categoryName": "string",
  "categoryId": 0
}

```

OneBot 11 用户信息
