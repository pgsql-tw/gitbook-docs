# CREATE TABLE：LIKE 複製選項

[返回 CREATE TABLE 主頁](sql-createtable.md)。

<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-COMMENTS"></a>

## `INCLUDING COMMENTS` [#](#sql-createtable-parms-like-opt-comments) <a href="#sql-createtable-parms-like-opt-comments" id="sql-createtable-parms-like-opt-comments"></a>

會複製所複製欄位、檢查限制條件、非 null 限制條件、索引與擴充統計資訊的註解。預設行為是排除註解，使新資料表中對應的物件沒有註解。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-COMPRESSION"></a>

## `INCLUDING COMPRESSION` [#](#sql-createtable-parms-like-opt-compression) <a href="#sql-createtable-parms-like-opt-compression" id="sql-createtable-parms-like-opt-compression"></a>

會複製欄位的壓縮方法。預設行為是排除壓縮方法，使欄位具有預設的壓縮方法。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-CONSTRAINTS"></a>

## `INCLUDING CONSTRAINTS` [#](#sql-createtable-parms-like-opt-constraints) <a href="#sql-createtable-parms-like-opt-constraints" id="sql-createtable-parms-like-opt-constraints"></a>

會複製 `CHECK` 限制條件。欄位限制條件與資料表限制條件之間不做區分。非 null 限制條件一律會複製到新資料表。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-DEFAULTS"></a>

## `INCLUDING DEFAULTS` [#](#sql-createtable-parms-like-opt-defaults) <a href="#sql-createtable-parms-like-opt-defaults" id="sql-createtable-parms-like-opt-defaults"></a>

會複製所複製欄位定義的預設值運算式。否則不會複製預設值運算式，使新資料表中所複製的欄位具有 null 預設值。請注意，複製呼叫了修改資料庫之函式（例如 `nextval`）的預設值，可能會在原始資料表與新資料表之間建立功能上的連結。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-GENERATED"></a>

## `INCLUDING GENERATED` [#](#sql-createtable-parms-like-opt-generated) <a href="#sql-createtable-parms-like-opt-generated" id="sql-createtable-parms-like-opt-generated"></a>

會複製所複製欄位定義的任何產生運算式，以及 stored／virtual 的選擇。預設情況下，新欄位會是一般的基本欄位。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-IDENTITY"></a>

## `INCLUDING IDENTITY` [#](#sql-createtable-parms-like-opt-identity) <a href="#sql-createtable-parms-like-opt-identity" id="sql-createtable-parms-like-opt-identity"></a>

會複製所複製欄位定義的任何識別規格。新資料表的每個識別欄位都會建立一個新的序列，與舊資料表所關聯的序列分開。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-INDEXES"></a>

## `INCLUDING INDEXES` [#](#sql-createtable-parms-like-opt-indexes) <a href="#sql-createtable-parms-like-opt-indexes" id="sql-createtable-parms-like-opt-indexes"></a>

原始資料表上的索引、`PRIMARY KEY`、`UNIQUE` 與 `EXCLUDE` 限制條件會建立在新資料表上。新索引與限制條件的名稱會依照預設規則選擇，不論原本的名稱為何。（此行為可避免新索引可能發生的名稱重複失敗。）
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-STATISTICS"></a>

## `INCLUDING STATISTICS` [#](#sql-createtable-parms-like-opt-statistics) <a href="#sql-createtable-parms-like-opt-statistics" id="sql-createtable-parms-like-opt-statistics"></a>

擴充統計資訊會複製到新資料表。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-STORAGE"></a>

## `INCLUDING STORAGE` [#](#sql-createtable-parms-like-opt-storage) <a href="#sql-createtable-parms-like-opt-storage" id="sql-createtable-parms-like-opt-storage"></a>

會複製所複製欄位定義的 `STORAGE` 設定。預設行為是排除 `STORAGE` 設定，使新資料表中所複製的欄位具有型別特定的預設設定。關於 `STORAGE` 設定的更多資訊，請參閱[第 66.2 節](../../internals/storage/storage-toast.md)。
<a id="SQL-CREATETABLE-PARMS-LIKE-OPT-ALL"></a>

## `INCLUDING ALL` [#](#sql-createtable-parms-like-opt-all) <a href="#sql-createtable-parms-like-opt-all" id="sql-createtable-parms-like-opt-all"></a>

`INCLUDING ALL` 是選取所有可用個別選項的縮寫形式。（在 `INCLUDING ALL` 之後寫上個別的 `EXCLUDING` 子句，以選取除了某些特定選項以外的所有選項，可能會很有用。）


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtable.html)（原文版本：18.6；核對日期：2026-10-04）
