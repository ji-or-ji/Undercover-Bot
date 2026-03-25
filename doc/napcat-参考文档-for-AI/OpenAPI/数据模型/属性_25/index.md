### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» result|any|true|none||猜拳结果|

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
|type|rps|

<h2 id="tocS_OB11MessageRecord">OB11MessageRecord</h2>

<a id="schemaob11messagerecord"></a>
<a id="schema_OB11MessageRecord"></a>
<a id="tocSob11messagerecord"></a>
<a id="tocsob11messagerecord"></a>

```json
{
  "type": "record",
  "data": {
    "file": "string",
    "path": "string",
    "url": "string",
    "name": "string",
    "thumb": "string"
  }
}

```

语音消息段
