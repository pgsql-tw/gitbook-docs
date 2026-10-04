<a id="SQL-CREATEPUBLICATION"></a><a id="id-1.9.3.77.1"></a>

## CREATE PUBLICATION

CREATE PUBLICATION — 定義新的發佈

<a id="id-1.9.3.77.4"></a>

## 語法

```

CREATE PUBLICATION name
    [ FOR ALL TABLES
      | FOR publication_object [, ... ] ]
    [ WITH ( publication_parameter [= value] [, ... ] ) ]

where publication_object is one of:

    TABLE table_and_columns [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ... ] ) ] [ WHERE ( expression ) ]
```

<a id="id-1.9.3.77.5"></a>

## 說明

`CREATE PUBLICATION` 會在目前的資料庫中新增一個發佈。發佈名稱必須與目前資料庫中任何現有發佈的名稱不同。

發佈本質上是一組資料表，其資料變更預定要透過邏輯複寫來複寫。關於發佈在邏輯複寫架構中扮演的角色，請參閱
[第 29.1 節](../../server-administration/logical-replication/logical-replication-publication.md)。

<a id="id-1.9.3.77.6"></a>

## 參數

<a id="SQL-CREATEPUBLICATION-PARAMS-NAME"></a>

*`name`* [#](#SQL-CREATEPUBLICATION-PARAMS-NAME)
:   新發佈的名稱。
<a id="SQL-CREATEPUBLICATION-PARAMS-FOR-TABLE"></a>

`FOR TABLE` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLE)
:   指定要加入發佈的資料表清單。若在資料表名稱前指定
    `ONLY`，則只有該資料表會被加入發佈。若未指定 `ONLY`，
    則會加入該資料表及其所有後代資料表（若有的話）。
    也可以選擇在資料表名稱後指定 `*`，以明確表示包含後代資料表。
    不過，這不適用於分割資料表。分割資料表的分割區一律被隱含地視為發佈的一部分，因此它們永遠不會被明確加入發佈。

    若指定了選擇性的 `WHERE` 子句，它會定義一個
    *資料列篩選器*運算式。
    *`expression`*
    求值結果為 false 或 null 的資料列將不會被發佈。請注意，運算式周圍必須加上括號。它對
    `TRUNCATE` 命令沒有作用。

    指定欄位清單時，只有所列出的欄位會被複寫。
    欄位清單也可以包含儲存式產生欄位。若省略欄位清單，該發佈預設會複寫所有非產生欄位（包括未來新增的欄位）。若
    `publish_generated_columns`
    設為 `stored`，儲存式產生欄位也可以被複寫。指定欄位清單對
    `TRUNCATE` 命令沒有作用。關於欄位清單的細節，請參閱
    [第 29.5 節](../../server-administration/logical-replication/logical-replication-col-lists.md)。

    只有持久性的基底資料表與分割資料表可以成為發佈的一部分。暫存資料表、無日誌資料表、外部資料表、具體化檢視表與一般檢視表都不能成為發佈的一部分。

    當發佈同時也發佈
    `FOR TABLES IN SCHEMA` 時，不支援指定欄位清單。

    當分割資料表被加入發佈時，其所有現有及未來的分割區都會被隱含地視為該發佈的一部分。因此，即使是直接在分割區上執行的操作，也會透過其祖先資料表所屬的發佈來發佈。
<a id="SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES"></a>

`FOR ALL TABLES` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES)
:   將該發佈標記為會複寫資料庫中所有資料表（包括未來建立的資料表）之變更的發佈。
<a id="SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA"></a>

`FOR TABLES IN SCHEMA` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)
:   將該發佈標記為會複寫指定綱要清單中所有資料表（包括未來建立的資料表）之變更的發佈。

    當發佈同時也發佈帶有欄位清單的資料表時，不支援指定綱要。

    只有存在於該綱要中的持久性基底資料表與分割資料表，才會被納入為發佈的一部分。該綱要中的暫存資料表、無日誌資料表、外部資料表、具體化檢視表與一般檢視表都不會成為發佈的一部分。

    當分割資料表透過綱要層級的發佈來發佈時，其所有現有及未來的分割區都會被隱含地視為該發佈的一部分，不論它們是否來自該發佈的綱要。
    因此，即使是直接在分割區上執行的操作，也會透過其祖先資料表所屬的發佈來發佈。
<a id="SQL-CREATEPUBLICATION-PARAMS-WITH"></a>

`WITH ( publication_parameter [= value] [, ... ] )` [#](#SQL-CREATEPUBLICATION-PARAMS-WITH)
:   此子句指定發佈的選擇性參數。支援下列參數：

    <a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH"></a>

    `publish` (`string`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)
    :   此參數決定新的發佈會將哪些 DML 操作發佈給訂閱者。其值是以逗號分隔的操作清單。允許的操作有
        `insert`、`update`、
        `delete` 與 `truncate`。
        預設是發佈所有動作，
        因此此選項的預設值為
        `'insert, update, delete, truncate'`。

        此參數只影響 DML 操作。特別是，邏輯複寫的初始資料同步（請參閱[第 29.9.1 節](../../server-administration/logical-replication/logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)）
        在複製現有的資料表資料時，不會考慮此參數。
    <a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS"></a>

    `publish_generated_columns` (`enum`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS)
    :   指定是否應該複寫與該發佈相關聯之資料表中的產生欄位。可能的值為
        `none` 與 `stored`。

        預設值為 `none`，表示與該發佈相關聯之資料表中的產生欄位不會被複寫。

        若設為 `stored`，則與該發佈相關聯之資料表中的儲存式產生欄位會被複寫。

        <a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS-NOTE"></a>

        ### 注意

        若訂閱者是 18 之前的版本，則即使發佈者的
        `publish_generated_columns` 參數為 `stored`，
        初始資料表同步也不會複製產生欄位。

        關於產生欄位之邏輯複寫的更多細節，請參閱[第 29.6 節](../../server-administration/logical-replication/logical-replication-gencols.md)。
    <a id="SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT"></a>

    `publish_via_partition_root` (`boolean`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT)
    :   此參數控制分割資料表（或其任何分割區）的變更要如何發佈。設為 `true` 時，
        變更會使用根分割資料表的識別與結構來發佈。設為 `false`（預設值）時，
        變更會使用實際發生變更之個別分割區的識別與結構來發佈。啟用此選項可讓變更被複寫到非分割資料表中，或複寫到分割結構與發佈者不同的分割資料表中。

        可能會有一個訂閱結合多個發佈的情況。若某個分割資料表被任何設定了
        `publish_via_partition_root = true` 的已訂閱發佈所發佈，則此分割資料表（或其分割區）上的變更，將會使用此分割資料表的識別與結構來發佈，而非個別分割區的識別與結構。

        此參數也會影響如何為分割區選擇資料列篩選器與欄位清單；詳情請見下文。

        若啟用此選項，直接在分割區上執行的 `TRUNCATE` 操作不會被複寫。

指定 `boolean` 型別的參數時，可以省略
`=` *`value`*
部分，這等同於指定 `TRUE`。

<a id="id-1.9.3.77.7"></a>

## 注意事項

若未指定 `FOR TABLE`、`FOR ALL TABLES` 或
`FOR TABLES IN SCHEMA`，則該發佈一開始的資料表集合是空的。若資料表或綱要要在之後才加入，這會很有用。

建立發佈並不會開始複寫。它只是為未來的訂閱者定義分組與篩選的邏輯。

要建立發佈，執行命令的使用者必須具備目前資料庫的
`CREATE` 權限。
（當然，超級使用者會略過此檢查。）

要將資料表加入發佈，執行命令的使用者必須擁有該資料表的擁有權。`FOR ALL TABLES` 與
`FOR TABLES IN SCHEMA` 子句要求執行命令的使用者必須是超級使用者。

加入會發佈 `UPDATE`
和／或 `DELETE` 操作之發佈的資料表，必須定義
`REPLICA IDENTITY`。否則，這些資料表上將不允許那些操作。

任何欄位清單都必須包含 `REPLICA IDENTITY` 欄位，
`UPDATE` 或 `DELETE`
操作才能被發佈。若發佈只發佈 `INSERT` 操作，則欄位清單沒有任何限制。

資料列篩選運算式（亦即 `WHERE` 子句）必須只包含
`REPLICA IDENTITY` 所涵蓋的欄位，
`UPDATE` 與 `DELETE` 操作才能被發佈。對於 `INSERT` 操作的發佈，
`WHERE` 運算式中可以使用任何欄位。資料列篩選器只允許簡單的運算式，不能包含使用者定義函式、使用者定義運算子、使用者定義型別、使用者定義定序、非 immutable 的內建函式，或對系統欄位的引用。

屬於 `REPLICA IDENTITY` 的產生欄位，
必須透過在欄位清單中列出它們，或啟用 `publish_generated_columns` 選項來明確發佈，
`UPDATE` 與 `DELETE` 操作才能被發佈。

若指定了
`FOR TABLES IN SCHEMA`，且該資料表屬於所引用的綱要，則該資料表上的資料列篩選器就成為多餘的。

對於已發佈的分割資料表，若發佈參數 `publish_via_partition_root` 為 true，
每個分割區的資料列篩選器取自已發佈的分割資料表；若為 false（預設值），則取自分割區本身。
關於資料列篩選器的細節，請參閱[第 29.4 節](../../server-administration/logical-replication/logical-replication-row-filter.md)。
同樣地，對於已發佈的分割資料表，若發佈參數 `publish_via_partition_root` 為 true，
每個分割區的欄位清單取自已發佈的分割資料表；若為 false，則取自分割區本身。

對於 `INSERT ... ON CONFLICT` 命令，發佈會發佈該命令所產生的操作。視結果而定，它可能會以 `INSERT` 或
`UPDATE` 的形式發佈，也可能完全不被發佈。

對於 `MERGE` 命令，發佈會針對每一筆插入、更新或刪除的資料列，發佈一個
`INSERT`、`UPDATE` 或 `DELETE`。

將資料表 `ATTACH` 到某個分割樹中，而該分割樹的根是透過 `publish_via_partition_root`
設為 `true` 的發佈來發佈時，並不會使該資料表的現有內容被複寫。

`COPY ... FROM` 命令會以
`INSERT` 操作的形式發佈。

DDL 操作不會被發佈。

`WHERE` 子句運算式會以複寫連線所使用的角色來執行。

<a id="id-1.9.3.77.8"></a>

## 範例

建立一個發佈兩個資料表中所有變更的發佈：

```

CREATE PUBLICATION mypublication FOR TABLE users, departments;
```

建立一個發佈作用中部門所有變更的發佈：

```

CREATE PUBLICATION active_departments FOR TABLE departments WHERE (active IS TRUE);
```

建立一個發佈所有資料表中所有變更的發佈：

```

CREATE PUBLICATION alltables FOR ALL TABLES;
```

建立一個只發佈單一資料表中 `INSERT`
操作的發佈：

```

CREATE PUBLICATION insert_only FOR TABLE mydata
    WITH (publish = 'insert');
```

建立一個發佈資料表
`users`、`departments` 的所有變更，以及綱要
`production` 中所有資料表之所有變更的發佈：

```

CREATE PUBLICATION production_publication FOR TABLE users, departments, TABLES IN SCHEMA production;
```

建立一個發佈綱要 `marketing` 與
`sales` 中所有資料表之所有變更的發佈：

```

CREATE PUBLICATION sales_publication FOR TABLES IN SCHEMA marketing, sales;
```

建立一個發佈資料表 `users` 的所有變更，
但只複寫欄位 `user_id` 與
`firstname` 的發佈：

```

CREATE PUBLICATION users_filtered FOR TABLE users (user_id, firstname);
```

<a id="id-1.9.3.77.9"></a>

## 相容性

`CREATE PUBLICATION` 是 PostgreSQL
的擴充語法。

<a id="id-1.9.3.77.10"></a>

## 另請參閱

[ALTER PUBLICATION](sql-alterpublication.md), [DROP PUBLICATION](sql-droppublication.md), [CREATE SUBSCRIPTION](sql-createsubscription.md), [ALTER SUBSCRIPTION](sql-altersubscription.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createpublication.html)（原文版本：18.6；核對日期：2026-10-04）
