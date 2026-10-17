<a id="BKI-COMMANDS"></a>

## 68.4. BKI 命令 [#](#BKI-COMMANDS)

`create` *`tablename`* *`tableoid`* [`bootstrap`] [`shared_relation`] [`rowtype_oid` *`oid`*] (*`name1`* = *`type1`* [`FORCE NOT NULL` | `FORCE NULL` ] [, *`name2`* = *`type2`* [`FORCE NOT NULL` | `FORCE NULL` ], ...])
:   建立名為 *`tablename`* 的資料表，其 OID 為
    *`tableoid`*，
    並具有括號中所列的欄位。

    `bootstrap.c` 直接支援下列欄位型別：`bool`、
    `bytea`、`char`（1 位元組）、
    `name`、`int2`、
    `int4`、`regproc`、`regclass`、
    `regtype`、`text`、
    `oid`、`tid`、`xid`、
    `cid`、`int2vector`、`oidvector`、
    `_int4`（陣列）、`_text`（陣列）、
    `_oid`（陣列）、`_char`（陣列）、
    `_aclitem`（陣列）。雖然可以建立含有其他型別欄位的資料表，
    但必須等到 `pg_type` 已建立並填入適當的項目之後才能這麼做。
    （這實際上表示初始建置（bootstrap）目錄中只能使用這些欄位型別，
    而非初始建置目錄則可以包含任何內建型別。）

    指定 `bootstrap` 時，資料表只會建立在磁碟上；
    不會為它在 `pg_class`、`pg_attribute` 等目錄中寫入任何內容。
    因此，在以費力的方式（使用 `insert` 命令）建立這些項目之前，
    一般的 SQL 操作將無法存取該資料表。此選項用於建立
    `pg_class` 等目錄本身。

    若指定了 `shared_relation`，資料表會以共享方式建立。
    資料表的資料列型別 OID（`pg_type` OID）可以選擇性地
    透過 `rowtype_oid` 子句指定；若未指定，會自動為它產生一個 OID。
    （若指定了 `bootstrap`，`rowtype_oid` 子句就沒有作用，
    但仍可為了文件記錄而提供。）

`open` *`tablename`*
:   開啟名為
    *`tablename`*
    的資料表以插入資料。任何目前已開啟的資料表都會被關閉。

`close` *`tablename`*
:   關閉已開啟的資料表。必須提供資料表名稱作為交叉核對。

`insert` `(` [*`oid_value`*] *`value1`* *`value2`* ... `)`
:   使用 *`value1`*、*`value2`* 等作為欄位值，
    在已開啟的資料表中插入一筆新的資料列。

    NULL 值可以使用特殊關鍵字 `_null_` 指定。
    看起來不像識別字或數字字串的值必須以單引號括住。
    （要在值中包含單引號，請將它寫兩次。
    字串中也允許使用跳脫字串風格的反斜線跳脫。）

`declare` [`unique`] `index` *`indexname`* *`indexoid`* `on` *`tablename`* `using` *`amname`* `(` *`opclass1`* *`name1`* [, ...] `)`
:   在名為 *`tablename`* 的資料表上，使用
    *`amname`* 存取方法，建立名為 *`indexname`*、OID 為
    *`indexoid`* 的索引。要建立索引的欄位稱為 *`name1`*、*`name2`* 等，
    所使用的運算子類別則分別為 *`opclass1`*、*`opclass2`* 等。
    此命令會建立索引檔並為它建立適當的目錄項目，但不會初始化索引內容。

`declare toast` *`toasttableoid`* *`toastindexoid`* `on` *`tablename`*
:   為名為
    *`tablename`*
    的資料表建立 TOAST 資料表。TOAST 資料表被指派的 OID 為
    *`toasttableoid`*，
    其索引被指派的 OID 為
    *`toastindexoid`*。
    與 `declare index` 相同，索引的填入會延後進行。

`build indices`
:   填入先前已宣告的索引。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bki-commands.html)（原文版本：18.6；核對日期：2026-10-17）
