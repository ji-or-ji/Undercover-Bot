### 属性

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[[OB11MessageData](#schemaob11messagedata)]|false|none||[OneBot 11 消息段]|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|string|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageData](#schemaob11messagedata)|false|none||OneBot 11 消息段|

<h2 id="tocS_OB11MessageNode">OB11MessageNode</h2>

<a id="schemaob11messagenode"></a>
<a id="schema_OB11MessageNode"></a>
<a id="tocSob11messagenode"></a>
<a id="tocsob11messagenode"></a>

```json
{
  "type": "node",
  "data": {
    "id": "string",
    "user_id": 0,
    "uin": 0,
    "nickname": "string",
    "name": "string",
    "content": {},
    "source": "string",
    "news": [
      {
        "text": "string"
      }
    ],
    "summary": "string",
    "prompt": "string",
    "time": "string"
  }
}

```

合并转发消息节点
