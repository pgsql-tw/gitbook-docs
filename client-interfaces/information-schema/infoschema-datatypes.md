## 35.2. 資料型別 [#](#INFOSCHEMA-DATATYPES)

資訊結構描述檢視表的欄位使用在資訊結構描述中定義的特殊資料型別。這些型別
定義為一般內建型別上的簡單 domain。請勿將這些型別用於資訊結構描述以外的工作；
不過，若應用程式會從資訊結構描述選取資料，就必須能處理它們。

這些型別如下：

`cardinal_number`
:   非負整數。

`character_data`
:   字串（沒有指定最大長度）。

`sql_identifier`
:   字串。此型別用於 SQL 識別字；`character_data` 型別則用於其他任何種類的
    文字資料。

`time_stamp`
:   `timestamp with time zone` 型別上的 domain。

`yes_or_no`
:   可包含 `YES` 或 `NO` 的字串 domain。此型別用於表示資訊結構描述中的
    Boolean（true/false）資料。（資訊結構描述在 SQL 標準加入 `boolean`
    型別之前就已制定，因此必須使用這項慣例以維持向後相容。）

資訊結構描述中的每個欄位都使用這五種型別之一。

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-datatypes.html)】
