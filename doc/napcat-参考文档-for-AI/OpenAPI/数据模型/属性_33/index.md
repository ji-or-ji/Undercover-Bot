### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
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
|nickname|string|true|none||发送者昵称|
|card|string|false|none||群名片|
|role|string|false|none||角色|
|sex|string|false|none||性别|
|age|number|false|none||年龄|
|area|string|false|none||地区|
|level|string|false|none||等级|
|title|string|false|none||头衔|

<h2 id="tocS_OB11GroupMember">OB11GroupMember</h2>

<a id="schemaob11groupmember"></a>
<a id="schema_OB11GroupMember"></a>
<a id="tocSob11groupmember"></a>
<a id="tocsob11groupmember"></a>

```json
{
  "group_id": 0,
  "user_id": 0,
  "nickname": "string",
  "card": "string",
  "sex": "string",
  "age": 0,
  "join_time": 0,
  "last_sent_time": 0,
  "level": "string",
  "qq_level": 0,
  "role": "string",
  "title": "string",
  "area": "string",
  "unfriendly": true,
  "title_expire_time": 0,
  "card_changeable": true,
  "shut_up_timestamp": 0,
  "is_robot": true,
  "qage": 0
}

```

OneBot 11 群成员信息
