# CREATE PUBLICATION 發佈參數

[返回 CREATE PUBLICATION 主頁](sql-createpublication.md)。

<a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH"></a>

## `publish` (`string`) [#](#sql-createpublication-params-with-publish) <a href="#sql-createpublication-params-with-publish" id="sql-createpublication-params-with-publish"></a>

此參數決定新的發佈會將哪些 DML 操作發佈給訂閱者。其值是以逗號分隔的操作清單。允許的操作有
`insert`、`update`、
`delete` 與 `truncate`。
預設是發佈所有動作，
因此此選項的預設值為
`'insert, update, delete, truncate'`。

此參數只影響 DML 操作。特別是，邏輯複寫的初始資料同步（請參閱[第 29.9.1 節](../../server-administration/logical-replication/logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)）
在複製現有的資料表資料時，不會考慮此參數。
<a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS"></a>

## `publish_generated_columns` (`enum`) [#](#sql-createpublication-params-with-publish-generated-columns) <a href="#sql-createpublication-params-with-publish-generated-columns" id="sql-createpublication-params-with-publish-generated-columns"></a>

指定是否應該複寫與該發佈相關聯之資料表中的產生欄位。可能的值為
`none` 與 `stored`。

預設值為 `none`，表示與該發佈相關聯之資料表中的產生欄位不會被複寫。

若設為 `stored`，則與該發佈相關聯之資料表中的儲存式產生欄位會被複寫。

<a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS-NOTE"></a>

### 注意 [#](#sql-createpublication-params-with-publish-generated-columns-note) <a href="#sql-createpublication-params-with-publish-generated-columns-note" id="sql-createpublication-params-with-publish-generated-columns-note"></a>

若訂閱者是 18 之前的版本，則即使發佈者的
`publish_generated_columns` 參數為 `stored`，
初始資料表同步也不會複製產生欄位。

關於產生欄位之邏輯複寫的更多細節，請參閱[第 29.6 節](../../server-administration/logical-replication/logical-replication-gencols.md)。
<a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT"></a>

## `publish_via_partition_root` (`boolean`) [#](#sql-createpublication-params-with-publish-via-partition-root) <a href="#sql-createpublication-params-with-publish-via-partition-root" id="sql-createpublication-params-with-publish-via-partition-root"></a>

此參數控制分割資料表（或其任何分割區）的變更要如何發佈。設為 `true` 時，
變更會使用根分割資料表的識別與結構來發佈。設為 `false`（預設值）時，
變更會使用實際發生變更之個別分割區的識別與結構來發佈。啟用此選項可讓變更被複寫到非分割資料表中，或複寫到分割結構與發佈者不同的分割資料表中。

可能會有一個訂閱結合多個發佈的情況。若某個分割資料表被任何設定了
`publish_via_partition_root = true` 的已訂閱發佈所發佈，則此分割資料表（或其分割區）上的變更，將會使用此分割資料表的識別與結構來發佈，而非個別分割區的識別與結構。

此參數也會影響如何為分割區選擇資料列篩選器與欄位清單；詳情請見下文。

若啟用此選項，直接在分割區上執行的 `TRUNCATE` 操作不會被複寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createpublication.html)（原文版本：18.6；核對日期：2026-10-04）
