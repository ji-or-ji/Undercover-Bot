### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|type|string|true|none||none|
|data|any|true|none||none|

allOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|object|false|none||文件消息段基础数据|
|»» file|string|true|none||文件路径/URL/file:///|
|»» path|string|false|none||文件路径|
|»» url|string|false|none||文件URL|
|»» name|string|false|none||文件名|
|»» thumb|string|false|none||缩略图|

and

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» *anonymous*|object|false|none||none|
|»» summary|string|false|none||图片摘要|
|»» sub_type|number|false|none||图片子类型|

#### 枚举值

|属性|值|
|---|---|
|type|image|

<h2 id="tocS_OB11MessageJson">OB11MessageJson</h2>

<a id="schemaob11messagejson"></a>
<a id="schema_OB11MessageJson"></a>
<a id="tocSob11messagejson"></a>
<a id="tocsob11messagejson"></a>

```json
{
  "type": "json",
  "data": {
    "data": "string",
    "config": {
      "token": "string"
    }
  }
}

```

JSON消息段
