### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» type|string|true|none||联系人类型|
|» id|string|true|none||联系人ID|

#### 枚举值

|属性|值|
|---|---|
|type|contact|
|type|qq|
|type|group|

<h2 id="tocS_OB11MessageCustomMusic">OB11MessageCustomMusic</h2>

<a id="schemaob11messagecustommusic"></a>
<a id="schema_OB11MessageCustomMusic"></a>
<a id="tocSob11messagecustommusic"></a>
<a id="tocsob11messagecustommusic"></a>

```json
{
  "type": "music",
  "data": {
    "type": "qq",
    "id": null,
    "url": "string",
    "audio": "string",
    "title": "string",
    "image": "string",
    "content": "string"
  }
}

```

自定义音乐消息段
