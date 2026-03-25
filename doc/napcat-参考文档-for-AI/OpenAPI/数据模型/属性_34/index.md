### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|group_id|number|true|none||群号|
|user_id|number|true|none||QQ号|
|nickname|string|true|none||昵称|
|card|string|false|none||名片|
|sex|string|false|none||性别|
|age|number|false|none||年龄|
|join_time|number|false|none||入群时间戳|
|last_sent_time|number|false|none||最后发言时间戳|
|level|string|false|none||等级|
|qq_level|number|false|none||QQ等级|
|role|string|false|none||角色 (owner/admin/member)|
|title|string|false|none||头衔|
|area|string|false|none||地区|
|unfriendly|boolean|false|none||是否不良记录|
|title_expire_time|number|false|none||头衔过期时间|
|card_changeable|boolean|false|none||是否允许修改名片|
|shut_up_timestamp|number|false|none||禁言截止时间戳|
|is_robot|boolean|false|none||是否为机器人|
|qage|number|false|none||Q龄|

<h2 id="tocS_OB11Group">OB11Group</h2>

<a id="schemaob11group"></a>
<a id="schema_OB11Group"></a>
<a id="tocSob11group"></a>
<a id="tocsob11group"></a>

```json
{
  "group_all_shut": 0,
  "group_remark": "string",
  "group_id": 0,
  "group_name": "string",
  "member_count": 0,
  "max_member_count": 0
}

```

OneBot 11 群信息
