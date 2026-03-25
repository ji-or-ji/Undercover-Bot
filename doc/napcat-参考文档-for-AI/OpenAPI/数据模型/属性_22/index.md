### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» id|string|false|none||转发消息ID|
|» user_id|any|false|none||发送者QQ号|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» uin|any|false|none||发送者QQ号(兼容go-cqhttp)|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» nickname|string|true|none||发送者昵称|
|» name|string|false|none||发送者昵称(兼容go-cqhttp)|
|» content|object|true|none||消息内容 (OB11MessageMixType)|
|» source|string|false|none||消息来源|
|» news|[object]|false|none||none|
|»» text|string|true|none||新闻文本|
|» summary|string|false|none||摘要|
|» prompt|string|false|none||提示|
|» time|string|false|none||时间|

#### 枚举值

|属性|值|
|---|---|
|type|node|

<h2 id="tocS_OB11MessageOnlineFile">OB11MessageOnlineFile</h2>

<a id="schemaob11messageonlinefile"></a>
<a id="schema_OB11MessageOnlineFile"></a>
<a id="tocSob11messageonlinefile"></a>
<a id="tocsob11messageonlinefile"></a>

```json
{
  "type": "onlinefile",
  "data": {
    "msgId": "string",
    "elementId": "string",
    "fileName": "string",
    "fileSize": "string",
    "isDir": true
  }
}

```

在线文件消息段
