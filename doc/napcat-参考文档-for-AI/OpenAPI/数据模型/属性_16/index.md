### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» data|any|true|none||JSON数据|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|object|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» config|object|false|none||none|
|»» token|string|true|none||token|

#### 枚举值

|属性|值|
|---|---|
|type|json|

<h2 id="tocS_OB11MessageLocation">OB11MessageLocation</h2>

<a id="schemaob11messagelocation"></a>
<a id="schema_OB11MessageLocation"></a>
<a id="tocSob11messagelocation"></a>
<a id="tocsob11messagelocation"></a>

```json
{
  "type": "location",
  "data": {
    "lat": "string",
    "lon": "string",
    "title": "string",
    "content": "string"
  }
}

```

位置消息段
