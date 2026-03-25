### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|object|true|none||none|
|» lat|any|true|none||纬度|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» lon|any|true|none||经度|

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|string|false|none||none|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|»» *anonymous*|number|false|none||none|

continued

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» title|string|false|none||标题|
|» content|string|false|none||内容|

#### 枚举值

|属性|值|
|---|---|
|type|location|

<h2 id="tocS_OB11MessageMFace">OB11MessageMFace</h2>

<a id="schemaob11messagemface"></a>
<a id="schema_OB11MessageMFace"></a>
<a id="tocSob11messagemface"></a>
<a id="tocsob11messagemface"></a>

```json
{
  "type": "mface",
  "data": {
    "emoji_package_id": 0,
    "emoji_id": "string",
    "key": "string",
    "summary": "string"
  }
}

```

商城表情消息段
