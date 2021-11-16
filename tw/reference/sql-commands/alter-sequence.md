# ALTER SEQUENCE

ALTER SEQUENCE — change the definition of a sequence generator

### 語法

```
ALTER SEQUENCE [ IF EXISTS ] name
    [ AS data_type ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ START [ WITH ] start ]
    [ RESTART [ [ WITH ] restart ] ]
    [ CACHE cache ] [ [ NO ] CYCLE ]
    [ OWNED BY { table_name.column_name | NONE } ]
ALTER SEQUENCE [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER SEQUENCE [ IF EXISTS ] name RENAME TO new_name
ALTER SEQUENCE [ IF EXISTS ] name SET SCHEMA new_schema
```

### 說明

ALTER SEQUENCE 變更現有序列産生器的參數。ALTER SEQUENCE 指令中未特別設定的任何參數都會保留其先前的設定。

您必須擁有該序列才能使用 ALTER SEQUENCE。要變更序列的綱要，您還必須對新綱要具有 CREATE 權限。要變更擁有者，您還必須是新擁有角色直接或間接成員，並且該角色必須對序列的綱要具有 CREATE 權限。（這些限制強制要求變更擁有者不會透過刪除和重新建立序列來執行任何操作。但是，超級使用者無論如何都可以變更任何序列的所有權。）

### 參數

_`name`_

要變更的序列名稱（選擇性加上綱要）。

`IF EXISTS`

如果序列不存在，請不要拋出錯誤。 在這種情況下發出 NOTICE。

_`data_type`_

可選擇性子句 AS data\_type 變更序列的資料型別。有效型別為 smallint，integer 和 bigint。

僅當先前的最小值和最大值是舊資料型別的最小值或最大值時，變更資料型別會自動變更序列的最小值和最大值（換句話說，如果序列是使用 NO MINVALUE 或 NO MAXVALUE，不論明確或隱含）。否則，將保留最小值和最大值，除非新值作為同一指令的一部分發出。如果最小值和最大值不適合新資料型別，則會産生錯誤。

_`increment`_

INCREMENT BY 增量子句是可選的。正值將產生遞增序列，負值將產生遞減序列。如果未指定，將保留舊的增量值。

_`minvalue`_\
`NO MINVALUE`

可選擇性子句 MINVALUE minvalue 決定序列可以産生的最小值。如果指定 NO MINVALUE，則將分別使用預設值 1 和遞增和遞減資料型別的最小值。如果未指定任何選項，則將保持目前的最小值。

_`maxvalue`_\
`NO MAXVALUE`

可選擇性子句 MAXVALUE maxvalue 決定序列的最大值。如果指定 NO MAXVALUE，則將分別使用資料型別最大值的預設值，以及遞增和遞減序列的預設值 -1。如果未指定任何選項，則將保持目前的最大值。

_`start`_

可選擇性子句 START WITH start 變更序列記錄的起始值。這對目前序列值沒有影響；它只是設定未來 ALTER SEQUENCE RESTART 指令將使用的值。

_`restart`_

可選擇性子句 RESTART \[WITH restart] 變更序列的目前值。這與使用 is\_called = false 呼叫 setval 函數類似：下一次呼叫 nextval 將回傳指定的值。寫入沒有重啟值的 RESTART 相當於提供由 CREATE SEQUENCE 記錄的起始值或 ALTER SEQUENCE START WITH 最後設定的起始值。

與 setval 使用相反，序列上的 RESTART 操作是交易事務的，並阻止平行事務從同一序列中取得數字。如果這不是需要的操作模式，則應使用 setval。

_`cache`_

此子句 CACHE 高速快取使序列號碼能夠預先分配並儲存在記憶體中，以便更快地存取。最小值為 1（一次只能産生一個值，即沒有快取）。如果未指定，將保留舊的快取值。

`CYCLE`

可選擇性的 CYCLE 關鍵字可用於使序列在分別透過遞增或遞減達到 maxvalue 或 minvalue 時循環繞回。如果達到限制，則産生的下一個數字將分別為 minvalue 或 maxvalue。

`NO CYCLE`

如果指定了可選擇性的 NO CYCLE 關鍵字，則在序列達到其最大值後對 nextval 的任何呼叫都將回傳錯誤。如果未指定 CYCLE 或 NO CYCLE，則將保持舊的循環行為。

`OWNED BY` _`table_name`_._`column_name`_\
`OWNED BY NONE`

OWNED BY 選項使序列與特定的資料表欄位相關連，這樣如果移除該欄位（或其整個資料表），序列也將自動移除。如果指定了，則此關連將替換先前為序列指定的任何關連。指定的資料表必須具有相同的擁有者，並且與序列位於相同的綱要中。指定 OWNED BY NONE 將移除任何現有關連，使序列「獨立」。

_`new_owner`_

序列新擁有者的使用者名稱。

_`new_name`_

序列的新名稱。

_`new_schema`_

序列的新綱要。

### 注意

ALTER SEQUENCE 不會立即影響具有預先分配（快取）序列值的後端（除了目前後端）的 nextval 結果。在注意到變更的序列産生參數之前，它們將使用所有快取的值。目前的後端將立即受到影響。

ALTER SEQUENCE 不會影響序列的 currval 狀態。（在 PostgreSQL 8.3 之前，有時會影響到。）

ALTER SEQUENCE 阻止同時間的 nextval，currval，lastval 和 setval 呼叫。

由於歷史原因，ALTER TABLE 也可以用於序列；但是序列允許的 ALTER TABLE 的語法就只有上面列出的形式。

### 範例

將序列 serial 從 105 重新啟動：

```
ALTER SEQUENCE serial RESTART WITH 105;
```

### 相容性

ALTER SEQUENCE 符合 SQL 標準，除了 AS，START WITH，OWNED BY，OWNER TO，RENAME TO 和 SET SCHEMA 子句之外，它們是 PostgreSQL 的延伸功能。

### 參閱

[CREATE SEQUENCE](create-sequence.md), [DROP SEQUENCE](drop-sequence.md)
