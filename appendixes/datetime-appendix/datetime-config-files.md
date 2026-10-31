<a id="DATETIME-CONFIG-FILES"></a>

## B.4. 日期／時間設定檔 [#](#datetime-config-files) <a href="#datetime-config-files" id="datetime-config-files"></a>

<a id="id-1.11.3.7.2"></a>

由於時區縮寫沒有完善的標準，
PostgreSQL 提供了一種方式，讓你自訂
日期時間輸入所接受的縮寫集合。
這些縮寫有兩個來源：

1. [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 執行期參數通常
   設定為 IANA 時區資料庫中某個項目的名稱。
   若該時區有廣泛使用的時區縮寫，這些縮寫會出現
   在 IANA 資料中，而 PostgreSQL 會
   優先依照 IANA 資料所給定的意義
   辨識這些縮寫。
   例如，若 `timezone` 設定
   為 `America/New_York`，則 `EST`
   會被理解為 UTC-5，`EDT` 會被
   理解為 UTC-4。（若 [DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 設定為
   偏好非數字時區縮寫的樣式，這些 IANA 縮寫也會用於
   日期時間輸出。）
2. 若在目前的 IANA 時區中找不到某個縮寫，
   則會在
   [timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) 執行期參數所指定的清單中尋找。
   `timezone_abbreviations` 清單主要
   用於讓日期時間輸入能夠辨識目前時區以外
   其他時區的縮寫。（這些縮寫
   不會用於日期時間輸出。）

雖然任何資料庫使用者都可以變更 `timezone_abbreviations` 參數，
但它可以使用的值
由資料庫管理員控制——這些值
實際上是儲存在安裝目錄的
`.../share/timezonesets/` 中的設定檔名稱。
藉由新增或修改該目錄中的檔案，管理員
可以設定時區縮寫的本地政策。

`timezone_abbreviations` 可以設定為
`.../share/timezonesets/` 中的任何檔名，只要該檔名
完全由英文字母組成。（禁止在 `timezone_abbreviations` 中使用非英文字母
字元，可以防止讀取
預定目錄以外的檔案，以及讀取編輯器
備份檔與其他無關的檔案。）

時區縮寫檔可以包含空白行，以及
以 `#` 開頭的註解。非註解行必須符合下列
其中一種格式：

```

zone_abbreviation offset
zone_abbreviation offset D
zone_abbreviation time_zone_name
@INCLUDE file_name
@OVERRIDE
```

*`zone_abbreviation`* 就是要定義的
縮寫。*`offset`* 是一個整數，表示
與 UTC 相差的秒數，正值表示位於
格林威治以東，負值表示以西。例如，-18000 表示格林威治以西五個
小時，也就是北美東岸標準時間。
`D` 表示該時區名稱代表當地
日光節約時間，而不是標準時間。

或者，也可以給定 *`time_zone_name`*，參照
IANA 時區資料庫中定義的時區名稱。系統會查閱該時區的定義，
確認此縮寫目前或過去是否在
該時區中使用；若是，就使用適當的意義——也就是
在要判定其值的時間戳記當時正在使用的意義；若
當時並未使用，則採用在那之前最近一次使用的意義；若只在
那之後才使用，則採用最早的意義。對於處理
意義在歷史上曾經變動的縮寫，此行為是不可或缺的。也允許
以一個不會出現該縮寫的時區名稱來定義縮寫；
此時使用該縮寫就等同於
直接寫出該時區名稱。

### 提示

定義一個與 UTC 的偏移量從未改變的縮寫時，
建議使用簡單的整數 *`offset`*，
因為處理這類縮寫的成本遠低於
需要查閱時區定義的縮寫。

`@INCLUDE` 語法可以引入
`.../share/timezonesets/` 目錄中的另一個檔案。引入可以巢狀進行，
但深度有限。

`@OVERRIDE` 語法表示檔案中後續的項目
可以覆寫先前的項目（通常是從
引入的檔案取得的項目）。若沒有此語法，同一個
時區縮寫的衝突定義會被視為錯誤。

在未經修改的安裝中，檔案 `Default` 包含
全球大部分地區所有不互相衝突的時區縮寫。
另外也為澳洲與印度地區提供了
`Australia` 與 `India` 檔案：這些檔案會先引入
`Default` 檔案，再視需要新增或修改縮寫。

為了方便參考，標準安裝也包含
`Africa.txt`、`America.txt` 等檔案，其中包含
依據 IANA 時區資料庫已知正在使用的每個時區縮寫的
資訊。這些檔案中的時區名稱
定義可以視需要複製貼上到自訂
設定檔中。請注意，這些檔案無法直接
作為 `timezone_abbreviations` 的設定值來參照，因為
其名稱中含有句點。

### 注意 [#](#zhu-yi) <a href="#zhu-yi" id="zhu-yi"></a>

若讀取時區縮寫集合時發生錯誤，則不會套用新的
值，並保留舊的集合。若錯誤發生在
啟動資料庫時，則啟動會失敗。

### 注意 [#](#xiao-xin) <a href="#xiao-xin" id="xiao-xin"></a>

{% hint style="warning" %}
設定檔中定義的時區縮寫會覆寫
PostgreSQL 內建的非時區意義。
例如，`Australia` 設定檔定義了
`SAT`（表示南澳標準時間）。當此
檔案生效時，`SAT` 將不會被辨識為
星期六的縮寫。
{% endhint %}

### 注意 [#](#xiao-xin-1) <a href="#xiao-xin-1" id="xiao-xin-1"></a>

{% hint style="warning" %}
若你修改 `.../share/timezonesets/` 中的檔案，
必須自行負責備份——一般的資料庫傾印
不會包含此目錄。
{% endhint %}

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datetime-config-files.html)（原文版本：18.6；核對日期：2026-10-22）
