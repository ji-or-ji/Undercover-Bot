### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» qq|string|true|none||QQ号或all|
|» name|string|false|none||显示名称|

#### 枚举值

|属性|值|
|---|---|
|type|at|

<h2 id="tocS_OB11MessageContact">OB11MessageContact</h2>

<a id="schemaob11messagecontact"></a>
<a id="schema_OB11MessageContact"></a>
<a id="tocSob11messagecontact"></a>
<a id="tocsob11messagecontact"></a>

```json
{
  "type": "contact",
  "data": {
    "type": "qq",
    "id": "string"
  }
}

```

联系人消息段
