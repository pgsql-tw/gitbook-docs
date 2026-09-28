<a id="id-1.9.3.151.1"></a>

## IMPORT FOREIGN SCHEMA

IMPORT FOREIGN SCHEMA — 從外部伺服器匯入資料表定義

## 語法

```

IMPORT FOREIGN SCHEMA remote_schema
    [ { LIMIT TO | EXCEPT } ( table_name [, ...] ) ]
    FROM SERVER server_name
    INTO local_schema
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

<a id="SQL-IMPORTFOREIGNSCHEMA-DESCRIPTION"></a>

## 說明

`IMPORT FOREIGN SCHEMA` 會建立外部資料表，用來代表存在於外部伺服器上的資料表。新建立的外部資料表會由發出此指令的使用者擁有，並會建立正確的欄位定義與選項，以符合遠端資料表。

依預設，外部伺服器上某個特定綱要中現有的所有資料表與檢視表都會被匯入。你也可以選擇將資料表清單限制為指定的子集合，或排除特定的資料表。新建立的外部資料表都會建立在目標綱要中，該綱要必須已經存在。

若要使用 `IMPORT FOREIGN SCHEMA`，使用者必須擁有該外部伺服器的 `USAGE` 權限，以及目標綱要的 `CREATE` 權限。

<a id="id-1.9.3.151.6"></a>

## 參數

*`remote_schema`*
:   要匯入資料的遠端綱要。遠端綱要的確切意義取決於所使用的外部資料包裝器。

`LIMIT TO ( table_name [, ...] )`
:   僅匯入名稱符合所給定資料表名稱之一的外部資料表。存在於外部綱要中的其他資料表都會被忽略。

`EXCEPT ( table_name [, ...] )`
:   將指定的外部資料表排除於匯入之外。除了此處所列出的資料表以外，外部綱要中現有的所有資料表都會被匯入。

*`server_name`*
:   要匯入資料的外部伺服器。

*`local_schema`*
:   匯入的外部資料表將建立於其中的綱要。

`OPTIONS ( option 'value' [, ...] )`
:   匯入期間所使用的選項。可用的選項名稱與值，因各個外部資料包裝器而異。

<a id="SQL-IMPORTFOREIGNSCHEMA-EXAMPLES"></a>

## 範例

從伺服器 `film_server` 上的遠端綱要 `foreign_films` 匯入資料表定義，並在本地綱要 `films` 中建立外部資料表：

```

IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;
```

同上，但只匯入 `actors` 與 `directors` 這兩個資料表（若它們存在）：

```

IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;
```

<a id="SQL-IMPORTFOREIGNSCHEMA-COMPATIBILITY"></a>

## 相容性

`IMPORT FOREIGN SCHEMA` 指令符合 SQL 標準，但 `OPTIONS` 子句是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.151.9"></a>

## 另請參閱

[CREATE FOREIGN TABLE](sql-createforeigntable.md), [CREATE SERVER](sql-createserver.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-importforeignschema.html)（原文版本：18.6；核對日期：2026-09-28）
