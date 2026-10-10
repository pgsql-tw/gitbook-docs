<a id="SQL-ALTERSEQUENCE"></a><a id="id-1.9.3.30.1"></a>

## ALTER SEQUENCE

ALTER SEQUENCE — 變更序列產生器的定義

<a id="id-1.9.3.30.4"></a>

## 語法

```

ALTER SEQUENCE [ IF EXISTS ] name
    [ AS data_type ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ [ NO ] CYCLE ]
    [ START [ WITH ] start ]
    [ RESTART [ [ WITH ] restart ] ]
    [ CACHE cache ]
    [ OWNED BY { table_name.column_name | NONE } ]
ALTER SEQUENCE [ IF EXISTS ] name SET { LOGGED | UNLOGGED }
ALTER SEQUENCE [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SEQUENCE [ IF EXISTS ] name RENAME TO new_name
ALTER SEQUENCE [ IF EXISTS ] name SET SCHEMA new_schema
```

<a id="id-1.9.3.30.5"></a>

## 說明

`ALTER SEQUENCE` 會變更現有序列產生器的參數。在 `ALTER SEQUENCE` 命令中未特別設定的任何參數，都會保留先前的設定。

你必須是該序列的擁有者才能使用 `ALTER SEQUENCE`。若要變更序列的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，且該角色必須擁有該序列所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法透過刪除並重新建立該序列來做到的事。不過，超級使用者無論如何都可以變更任何序列的擁有權。）

<a id="id-1.9.3.30.6"></a>

## 參數

*`name`*
:   要變更之序列的名稱（可選擇以綱要限定）。

`IF EXISTS`
:   序列不存在時不擲出錯誤；此情況會發出 notice。

*`data_type`*
:   選擇性的 `AS data_type` 子句會變更序列的資料型別。有效的型別為 `smallint`、`integer` 與 `bigint`。

    變更資料型別時，若且唯若先前的最小值與最大值是舊資料型別的最小值或最大值（換句話說，若序列是以 `NO
    MINVALUE` 或 `NO MAXVALUE` 建立的，無論是隱含或明確指定），才會自動變更序列的最小值與最大值。否則，最小值與最大值會保留，除非在同一個命令中提供了新的值。若最小值與最大值無法容納於新的資料型別中，則會產生錯誤。

*`increment`*
:   `INCREMENT BY increment` 子句是選擇性的。正值會產生遞增序列，負值則產生遞減序列。若未指定，將維持舊的遞增值。

*`minvalue`*<br>`NO MINVALUE`
:   選擇性的 `MINVALUE minvalue` 子句決定序列可以產生的最小值。若指定 `NO
    MINVALUE`，則遞增序列與遞減序列分別使用預設值 1 與該資料型別的最小值。若兩個選項都未指定，將維持目前的最小值。

*`maxvalue`*<br>`NO MAXVALUE`
:   選擇性的 `MAXVALUE maxvalue` 子句決定序列的最大值。若指定 `NO
    MAXVALUE`，則遞增序列與遞減序列分別使用預設值該資料型別的最大值與 -1。若兩個選項都未指定，將維持目前的最大值。

`CYCLE`
:   選擇性的 `CYCLE` 關鍵字可以用來讓序列在遞增序列或遞減序列分別達到 *`maxvalue`* 或 *`minvalue`* 時循環回頭。若達到限制，下一個產生的數字將分別是 *`minvalue`* 或 *`maxvalue`*。

`NO CYCLE`
:   若指定了選擇性的 `NO CYCLE` 關鍵字，則遞增序列達到其最大值、或遞減序列達到其最小值之後，任何對 `nextval` 的呼叫都會傳回錯誤。若 `CYCLE` 與 `NO
    CYCLE` 都未指定，將維持舊的循環行為。

*`start`*
:   選擇性的 `START WITH start` 子句會變更序列所記錄的起始值。這對*目前的*序列值沒有任何影響；它只是設定未來的 `ALTER SEQUENCE RESTART` 命令將使用的值。

*`restart`*
:   選擇性的 `RESTART [ WITH restart ]` 子句會變更序列的目前值。這類似於以 `is_called` = `false` 呼叫 `setval` 函式：指定的值將由*下一次* `nextval` 呼叫傳回。只寫 `RESTART` 而不提供 *`restart`* 值，等同於提供由 `CREATE SEQUENCE` 記錄、或最後一次由 `ALTER SEQUENCE START WITH` 設定的起始值。

    與 `setval` 呼叫不同，對序列執行的 `RESTART` 操作是交易性的，並且會阻擋並行交易從同一個序列取得數字。若這不是所需的操作模式，應該使用 `setval`。

*`cache`*
:   `CACHE cache` 子句可讓序列號碼預先配置並儲存在記憶體中，以加快存取速度。最小值為 1（一次只能產生一個值，亦即不快取）。若未指定，將維持舊的快取值。

`SET { LOGGED | UNLOGGED }`
:   此形式會將序列從無日誌變更為有日誌，或反之（請參閱 [CREATE SEQUENCE](sql-createsequence.md)）。它不能套用於暫存序列。

`OWNED BY` *`table_name`*.*`column_name`*<br>`OWNED BY NONE`
:   `OWNED BY` 選項會使序列與特定的資料表欄位相關聯，使得當該欄位（或其整個資料表）被移除時，序列也會自動被移除。若有指定，此關聯會取代該序列先前指定的任何關聯。指定的資料表必須與序列有相同的擁有者，並位於相同的綱要中。指定 `OWNED BY NONE` 會移除任何現有的關聯，使序列成為「獨立的」序列。

*`new_owner`*
:   序列新擁有者的使用者名稱。

*`new_name`*
:   序列的新名稱。

*`new_schema`*
:   序列的新綱要。

<a id="id-1.9.3.30.7"></a>

## 注意事項

對於目前後端以外、已經預先配置（快取）序列值的後端，`ALTER SEQUENCE` 不會立即影響其 `nextval` 結果。這些後端會先用完所有已快取的值，才會察覺到已變更的序列產生參數。目前的後端則會立即受到影響。

`ALTER SEQUENCE` 不會影響序列的 `currval` 狀態。（在 PostgreSQL 8.3 之前，有時會影響。）

`ALTER SEQUENCE` 會阻擋並行的 `nextval`、`currval`、`lastval` 與 `setval` 呼叫。

由於歷史因素，`ALTER TABLE` 也可以用於序列；但允許用於序列的 `ALTER TABLE` 形式，僅限於與上述形式等效者。

<a id="id-1.9.3.30.8"></a>

## 範例

從 105 重新開始名為 `serial` 的序列：

```

ALTER SEQUENCE serial RESTART WITH 105;
```

<a id="id-1.9.3.30.9"></a>

## 相容性

`ALTER SEQUENCE` 符合 SQL 標準，但 `AS`、`START WITH`、`OWNED BY`、`OWNER TO`、`RENAME TO` 與 `SET SCHEMA` 子句除外，這些是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.30.10"></a>

## 另請參閱

[CREATE SEQUENCE](sql-createsequence.md), [DROP SEQUENCE](sql-dropsequence.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altersequence.html)（原文版本：18.6；核對日期：2026-10-10）
