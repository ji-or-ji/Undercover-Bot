### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» type|string|true|none||音乐平台类型|
|» id|null|true|none||none|
|» url|string|true|none||点击后跳转URL|
|» audio|string|false|none||音频URL|
|» title|string|false|none||音乐标题|
|» image|string|true|none||封面图片URL|
|» content|string|false|none||音乐简介|

#### 枚举值

|属性|值|
|---|---|
|type|music|
|type|qq|
|type|163|
|type|kugou|
|type|migu|
|type|kuwo|
|type|custom|

<h2 id="tocS_OB11MessageData">OB11MessageData</h2>

<a id="schemaob11messagedata"></a>
<a id="schema_OB11MessageData"></a>
<a id="tocSob11messagedata"></a>
<a id="tocsob11messagedata"></a>

```json
{
  "type": "text",
  "data": {
    "text": "string"
  }
}

```

OneBot 11 消息段
