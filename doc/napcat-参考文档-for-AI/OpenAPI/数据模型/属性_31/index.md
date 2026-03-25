### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» data|string|true|none||XML数据|

#### 枚举值

|属性|值|
|---|---|
|type|xml|

<h2 id="tocS_OB11PostSendMsg">OB11PostSendMsg</h2>

<a id="schemaob11postsendmsg"></a>
<a id="schema_OB11PostSendMsg"></a>
<a id="tocSob11postsendmsg"></a>
<a id="tocsob11postsendmsg"></a>

```json
{
  "message_type": "private",
  "user_id": "string",
  "group_id": "string",
  "message": [
    {
      "type": "[",
      "data": {}
    }
  ],
  "messages": [
    {
      "type": "[",
      "data": {}
    }
  ],
  "auto_escape": true,
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

```

OneBot 11 发送消息请求
