### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|status|string|true|none||状态 (ok/failed)|
|retcode|number|true|none||返回码|
|data|any|false|none||业务数据（具体结构由各接口定义）|
|message|string|false|none||消息|
|wording|string|false|none||提示|
|stream|string|false|none||流式响应|

#### 枚举值

|属性|值|
|---|---|
|stream|stream-action|
|stream|normal-action|

<h2 id="tocS_EmptyData">EmptyData</h2>

<a id="schemaemptydata"></a>
<a id="schema_EmptyData"></a>
<a id="tocSemptydata"></a>
<a id="tocsemptydata"></a>

```json
null

```

无数据
