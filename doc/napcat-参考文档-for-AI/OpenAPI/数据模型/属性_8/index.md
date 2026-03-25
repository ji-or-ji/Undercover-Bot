### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» result|any|true|none||骰子结果|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|type|dice|

<h2 id="tocS_OB11MessageFace">OB11MessageFace</h2>

<a id="schemaob11messageface"></a>
<a id="schema_OB11MessageFace"></a>
<a id="tocSob11messageface"></a>
<a id="tocsob11messageface"></a>

```json
{
  "type": "face",
  "data": {
    "id": "string",
    "resultId": "string",
    "chainCount": 0
  }
}

```

QQ表情消息段
