### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» msgId|string|true|none||消息ID|
|» elementId|string|true|none||元素ID|
|» fileName|string|true|none||文件名|
|» fileSize|string|true|none||文件大小|
|» isDir|boolean|true|none||是否为目录|

#### 枚举值

|属性|值|
|---|---|
|type|onlinefile|

<h2 id="tocS_OB11MessagePoke">OB11MessagePoke</h2>

<a id="schemaob11messagepoke"></a>
<a id="schema_OB11MessagePoke"></a>
<a id="tocSob11messagepoke"></a>
<a id="tocsob11messagepoke"></a>

```json
{
  "type": "poke",
  "data": {
    "type": "string",
    "id": "string"
  }
}

```

戳一戳消息段
