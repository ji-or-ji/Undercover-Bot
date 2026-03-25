### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» fileSetId|string|true|none||文件集ID|

#### 枚举值

|属性|值|
|---|---|
|type|flashtransfer|

<h2 id="tocS_OB11MessageForward">OB11MessageForward</h2>

<a id="schemaob11messageforward"></a>
<a id="schema_OB11MessageForward"></a>
<a id="tocSob11messageforward"></a>
<a id="tocsob11messageforward"></a>

```json
{
  "type": "forward",
  "data": {
    "id": "string",
    "content": {}
  }
}

```

合并转发消息段
