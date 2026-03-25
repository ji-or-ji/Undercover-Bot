### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» emoji_package_id|number|true|none||表情包ID|
|» emoji_id|string|true|none||表情ID|
|» key|string|true|none||表情key|
|» summary|string|true|none||表情摘要|

#### 枚举值

|属性|值|
|---|---|
|type|mface|

<h2 id="tocS_OB11MessageMarkdown">OB11MessageMarkdown</h2>

<a id="schemaob11messagemarkdown"></a>
<a id="schema_OB11MessageMarkdown"></a>
<a id="tocSob11messagemarkdown"></a>
<a id="tocsob11messagemarkdown"></a>

```json
{
  "type": "markdown",
  "data": {
    "content": "string"
  }
}

```

Markdown消息段
