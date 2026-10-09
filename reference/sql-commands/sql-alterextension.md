<a id="SQL-ALTEREXTENSION"></a><a id="id-1.9.3.11.1"></a>

## ALTER EXTENSION

ALTER EXTENSION — 變更擴充功能的定義

<a id="id-1.9.3.11.4"></a>

## 語法

```

ALTER EXTENSION name UPDATE [ TO new_version ]
ALTER EXTENSION name SET SCHEMA new_schema
ALTER EXTENSION name ADD member_object
ALTER EXTENSION name DROP member_object

where member_object is:

  ACCESS METHOD object_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  CAST (source_type AS target_type) |
  COLLATION object_name |
  CONVERSION object_name |
  DOMAIN object_name |
  EVENT TRIGGER object_name |
  FOREIGN DATA WRAPPER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  MATERIALIZED VIEW object_name |
  OPERATOR operator_name (left_type, right_type) |
  OPERATOR CLASS object_name USING index_method |
  OPERATOR FAMILY object_name USING index_method |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  SCHEMA object_name |
  SEQUENCE object_name |
  SERVER object_name |
  TABLE object_name |
  TEXT SEARCH CONFIGURATION object_name |
  TEXT SEARCH DICTIONARY object_name |
  TEXT SEARCH PARSER object_name |
  TEXT SEARCH TEMPLATE object_name |
  TRANSFORM FOR type_name LANGUAGE lang_name |
  TYPE object_name |
  VIEW object_name

and aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

<a id="id-1.9.3.11.5"></a>

## 說明

`ALTER EXTENSION` 會變更已安裝之擴充功能的定義。它有以下幾種子形式：

`UPDATE`
:   此形式會將擴充功能更新到較新的版本。擴充功能必須提供合適的更新腳本（或一系列腳本），能將目前安裝的版本修改為所要求的版本。

`SET SCHEMA`
:   此形式會將擴充功能的物件移到另一個綱要。擴充功能必須是*可重新定位*的，此命令才能成功。

`ADD member_object`
:   此形式會將現有物件加入擴充功能。這主要用於擴充功能的更新腳本中。之後該物件會被視為擴充功能的成員；值得注意的是，它只能透過移除擴充功能來移除。

`DROP member_object`
:   此形式會從擴充功能中移除一個成員物件。這主要用於擴充功能的更新腳本中。該物件不會被移除，只是與擴充功能解除關聯。

關於這些操作的更多資訊，請參閱[第 36.17 節](../../server-programming/extend/extend-extensions.md)。

你必須是擴充功能的擁有者，才能使用 `ALTER EXTENSION`。`ADD`/`DROP` 形式還要求你是被加入／被移除之物件的擁有者。

<a id="id-1.9.3.11.6"></a>

## 參數

*`name`*
:   已安裝之擴充功能的名稱。

*`new_version`*
:   擴充功能所要的新版本。可以寫成識別字或字串常值。若未指定，`ALTER EXTENSION UPDATE` 會嘗試更新到擴充功能控制檔中所列的預設版本。

*`new_schema`*
:   擴充功能的新綱要。

*`object_name`*<br>*`aggregate_name`*<br>*`function_name`*<br>*`operator_name`*<br>*`procedure_name`*<br>*`routine_name`*
:   要加入擴充功能或從擴充功能中移除之物件的名稱。資料表、彙總函式、網域、外部資料表、函式、運算子、運算子類別、運算子家族、程序、常式、序列、文字搜尋物件、型別與檢視表的名稱可以用綱要限定。

*`source_type`*
:   轉型的來源資料型別名稱。

*`target_type`*
:   轉型的目標資料型別名稱。

*`argmode`*
:   函式、程序或彙總函式引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。請注意，`ALTER EXTENSION` 實際上並不理會 `OUT` 引數，因為只需要輸入引數就能確定函式的身分。因此只要列出 `IN`、`INOUT` 與 `VARIADIC` 引數就足夠了。

*`argname`*
:   函式、程序或彙總函式引數的名稱。請注意，`ALTER EXTENSION` 實際上並不理會引數名稱，因為只需要引數的資料型別就能確定函式的身分。

*`argtype`*
:   函式、程序或彙總函式引數的資料型別。

*`left_type`*<br>*`right_type`*
:   運算子引數的資料型別（可選擇以綱要限定）。對於前置運算子缺少的那個引數，請寫 `NONE`。

`PROCEDURAL`
:   這是贅字。

*`type_name`*
:   轉換的資料型別名稱。

*`lang_name`*
:   轉換的語言名稱。

<a id="id-1.9.3.11.7"></a>

## 範例

將 `hstore` 擴充功能更新到 2.0 版：

```

ALTER EXTENSION hstore UPDATE TO '2.0';
```

將 `hstore` 擴充功能的綱要變更為 `utils`：

```

ALTER EXTENSION hstore SET SCHEMA utils;
```

將現有函式加入 `hstore` 擴充功能：

```

ALTER EXTENSION hstore ADD FUNCTION populate_record(anyelement, hstore);
```

<a id="id-1.9.3.11.8"></a>

## 相容性

`ALTER EXTENSION` 是 PostgreSQL 對 SQL 標準的擴充語法。

<a id="SQL-ALTEREXTENSION-SEE-ALSO"></a>

## 另請參閱

[CREATE EXTENSION](sql-createextension.md), [DROP EXTENSION](sql-dropextension.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterextension.html)（原文版本：18.6；核對日期：2026-10-05）
