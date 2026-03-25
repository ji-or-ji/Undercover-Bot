### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» id|string|true|none||表情ID|
|» resultId|string|false|none||结果ID|
|» chainCount|number|false|none||连击数|

#### 枚举值

|属性|值|
|---|---|
|type|face|

<h2 id="tocS_OB11MessageFileBase">OB11MessageFileBase</h2>

<a id="schemaob11messagefilebase"></a>
<a id="schema_OB11MessageFileBase"></a>
<a id="tocSob11messagefilebase"></a>
<a id="tocsob11messagefilebase"></a>

```json
{
  "data": {
    "file": "string",
    "path": "string",
    "url": "string",
    "name": "string",
    "thumb": "string"
  }
}

```

文件消息基础接口
