### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» id|string|true|none||合并转发ID|
|» content|object|false|none||消息内容 (OB11Message[])|

#### 枚举值

|属性|值|
|---|---|
|type|forward|

<h2 id="tocS_OB11MessageIdMusic">OB11MessageIdMusic</h2>

<a id="schemaob11messageidmusic"></a>
<a id="schema_OB11MessageIdMusic"></a>
<a id="tocSob11messageidmusic"></a>
<a id="tocsob11messageidmusic"></a>

```json
{
  "type": "music",
  "data": {
    "type": "qq",
    "id": "string"
  }
}

```

ID音乐消息段
