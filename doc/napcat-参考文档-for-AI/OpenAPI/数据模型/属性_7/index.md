### 属性

anyOf

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageText](#schemaob11messagetext)|false|none||纯文本消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageFace](#schemaob11messageface)|false|none||QQ表情消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageMFace](#schemaob11messagemface)|false|none||商城表情消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageAt](#schemaob11messageat)|false|none||@消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageReply](#schemaob11messagereply)|false|none||回复消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageImage](#schemaob11messageimage)|false|none||图片消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageRecord](#schemaob11messagerecord)|false|none||语音消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageVideo](#schemaob11messagevideo)|false|none||视频消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageFile](#schemaob11messagefile)|false|none||文件消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageIdMusic](#schemaob11messageidmusic)|false|none||ID音乐消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageCustomMusic](#schemaob11messagecustommusic)|false|none||自定义音乐消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessagePoke](#schemaob11messagepoke)|false|none||戳一戳消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageDice](#schemaob11messagedice)|false|none||骰子消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageRPS](#schemaob11messagerps)|false|none||猜拳消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageContact](#schemaob11messagecontact)|false|none||联系人消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageLocation](#schemaob11messagelocation)|false|none||位置消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageJson](#schemaob11messagejson)|false|none||JSON消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageXml](#schemaob11messagexml)|false|none||XML消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageMarkdown](#schemaob11messagemarkdown)|false|none||Markdown消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageMiniApp](#schemaob11messageminiapp)|false|none||小程序消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageNode](#schemaob11messagenode)|false|none||合并转发消息节点|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageForward](#schemaob11messageforward)|false|none||合并转发消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageOnlineFile](#schemaob11messageonlinefile)|false|none||在线文件消息段|

or

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[OB11MessageFlashTransfer](#schemaob11messageflashtransfer)|false|none||QQ闪传消息段|

<h2 id="tocS_OB11MessageDice">OB11MessageDice</h2>

<a id="schemaob11messagedice"></a>
<a id="schema_OB11MessageDice"></a>
<a id="tocSob11messagedice"></a>
<a id="tocsob11messagedice"></a>

```json
{
  "type": "dice",
  "data": {
    "result": 0
  }
}

```

骰子消息段
