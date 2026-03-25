### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» type|string|true|none||音乐平台类型|
|» id|any|true|none||音乐ID|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|type|music|
|type|qq|
|type|163|
|type|kugou|
|type|migu|
|type|kuwo|

<h2 id="tocS_OB11MessageImage">OB11MessageImage</h2>

<a id="schemaob11messageimage"></a>
<a id="schema_OB11MessageImage"></a>
<a id="tocSob11messageimage"></a>
<a id="tocsob11messageimage"></a>

```json
{
  "type": "image",
  "data": {
    "file": "string",
    "path": "string",
    "url": "string",
    "name": "string",
    "thumb": "string",
    "summary": "string",
    "sub_type": 0
  }
}

```

图片消息段
