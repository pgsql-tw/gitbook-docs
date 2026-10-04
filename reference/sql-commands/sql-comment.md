<a id="SQL-COMMENT"></a><a id="id-1.9.3.52.1"></a>

## COMMENT

COMMENT — 定義或變更物件的註解

<a id="id-1.9.3.52.4"></a>

## 語法

```

COMMENT ON
{
  ACCESS METHOD object_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  CAST (source_type AS target_type) |
  COLLATION object_name |
  COLUMN relation_name.column_name |
  CONSTRAINT constraint_name ON table_name |
  CONSTRAINT constraint_name ON DOMAIN domain_name |
  CONVERSION object_name |
  DATABASE object_name |
  DOMAIN object_name |
  EXTENSION object_name |
  EVENT TRIGGER object_name |
  FOREIGN DATA WRAPPER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  INDEX object_name |
  LARGE OBJECT large_object_oid |
  MATERIALIZED VIEW object_name |
  OPERATOR operator_name (left_type, right_type) |
  OPERATOR CLASS object_name USING index_method |
  OPERATOR FAMILY object_name USING index_method |
  POLICY policy_name ON table_name |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  PUBLICATION object_name |
  ROLE object_name |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  RULE rule_name ON table_name |
  SCHEMA object_name |
  SEQUENCE object_name |
  SERVER object_name |
  STATISTICS object_name |
  SUBSCRIPTION object_name |
  TABLE object_name |
  TABLESPACE object_name |
  TEXT SEARCH CONFIGURATION object_name |
  TEXT SEARCH DICTIONARY object_name |
  TEXT SEARCH PARSER object_name |
  TEXT SEARCH TEMPLATE object_name |
  TRANSFORM FOR type_name LANGUAGE lang_name |
  TRIGGER trigger_name ON table_name |
  TYPE object_name |
  VIEW object_name
} IS { string_literal | NULL }

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

<a id="id-1.9.3.52.5"></a>

## 說明

`COMMENT` 會儲存、取代或移除資料庫物件上的註解。

每個物件只會儲存一個註解字串。對同一物件執行新的 `COMMENT` 命令，會取代現有的註解。指定 `NULL` 或空字串（`''`）會移除註解。物件被移除時，其註解也會自動移除。

會在要加上註解的物件上取得 `SHARE UPDATE EXCLUSIVE` 鎖定。

對於大多數種類的物件，只有物件的擁有者可以設定註解。角色沒有擁有者，因此 `COMMENT ON ROLE` 的規則是：你必須是超級使用者才能對超級使用者角色加上註解，或者必須具有 `CREATEROLE` 權限並在目標角色上被授予 `ADMIN OPTION`。同樣地，存取方法也沒有擁有者；你必須是超級使用者才能對存取方法加上註解。當然，超級使用者可以對任何東西加上註解。

可以使用 psql 的 `\d` 系列命令檢視註解。其他用來擷取註解的使用者介面，可以建構在 psql 所使用的相同內建函式之上，也就是 `obj_description`、`col_description` 與 `shobj_description`（請參閱[表 9.82](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-COMMENT-TABLE)）。

<a id="id-1.9.3.52.6"></a>

## 參數

*`object_name`*<br>*`relation_name`*.*`column_name`*<br>*`aggregate_name`*<br>*`constraint_name`*<br>*`function_name`*<br>*`operator_name`*<br>*`policy_name`*<br>*`procedure_name`*<br>*`routine_name`*<br>*`rule_name`*<br>*`trigger_name`*
:   要加上註解之物件的名稱。位於綱要中之物件（資料表、函式等）的名稱可以用綱要限定。對欄位加上註解時，*`relation_name`* 必須指向資料表、檢視表、複合型別或外部資料表。

*`table_name`*<br>*`domain_name`*
:   對限制條件、觸發程序、規則或政策建立註解時，這些參數指定定義該物件之資料表或網域的名稱。

*`source_type`*
:   轉型之來源資料型別的名稱。

*`target_type`*
:   轉型之目標資料型別的名稱。

*`argmode`*
:   函式、程序或彙總函式之引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。請注意，`COMMENT` 實際上並不理會 `OUT` 引數，因為只需要輸入引數就能決定函式的身分。因此，列出 `IN`、`INOUT` 與 `VARIADIC` 引數就足夠了。

*`argname`*
:   函式、程序或彙總函式之引數的名稱。請注意，`COMMENT` 實際上並不理會引數名稱，因為只需要引數的資料型別就能決定函式的身分。

*`argtype`*
:   函式、程序或彙總函式之引數的資料型別。

*`large_object_oid`*
:   大型物件的 OID。

*`left_type`*<br>*`right_type`*
:   運算子之引數的資料型別（可選擇以綱要限定）。對於前置運算子缺少的那個引數，請寫 `NONE`。

`PROCEDURAL`
:   這是贅字。

*`type_name`*
:   轉換的資料型別名稱。

*`lang_name`*
:   轉換的語言名稱。

*`string_literal`*
:   新的註解內容，以字串常值寫出。空字串（`''`）會移除註解。

`NULL`
:   寫 `NULL` 可移除註解。

<a id="id-1.9.3.52.7"></a>

## 注意事項

目前沒有用於檢視註解的安全機制：連線到資料庫的任何使用者，都可以看到該資料庫中物件的所有註解。對於資料庫、角色與資料表空間等共享物件，註解是全域儲存的，因此連線到叢集中任何資料庫的任何使用者，都可以看到共享物件的所有註解。因此，請勿在註解中放置與安全攸關的資訊。

<a id="id-1.9.3.52.8"></a>

## 範例

為資料表 `mytable` 加上註解：

```

COMMENT ON TABLE mytable IS 'This is my table.';
```

再將它移除：

```

COMMENT ON TABLE mytable IS NULL;
```

更多範例：

```

COMMENT ON ACCESS METHOD gin IS 'GIN index access method';
COMMENT ON AGGREGATE my_aggregate (double precision) IS 'Computes sample variance';
COMMENT ON CAST (text AS int4) IS 'Allow casts from text to int4';
COMMENT ON COLLATION "fr_CA" IS 'Canadian French';
COMMENT ON COLUMN my_table.my_column IS 'Employee ID number';
COMMENT ON CONVERSION my_conv IS 'Conversion to UTF8';
COMMENT ON CONSTRAINT bar_col_cons ON bar IS 'Constrains column col';
COMMENT ON CONSTRAINT dom_col_constr ON DOMAIN dom IS 'Constrains col of domain';
COMMENT ON DATABASE my_database IS 'Development Database';
COMMENT ON DOMAIN my_domain IS 'Email Address Domain';
COMMENT ON EVENT TRIGGER abort_ddl IS 'Aborts all DDL commands';
COMMENT ON EXTENSION hstore IS 'implements the hstore data type';
COMMENT ON FOREIGN DATA WRAPPER mywrapper IS 'my foreign data wrapper';
COMMENT ON FOREIGN TABLE my_foreign_table IS 'Employee Information in other database';
COMMENT ON FUNCTION my_function (timestamp) IS 'Returns Roman Numeral';
COMMENT ON INDEX my_index IS 'Enforces uniqueness on employee ID';
COMMENT ON LANGUAGE plpython IS 'Python support for stored procedures';
COMMENT ON LARGE OBJECT 346344 IS 'Planning document';
COMMENT ON MATERIALIZED VIEW my_matview IS 'Summary of order history';
COMMENT ON OPERATOR ^ (text, text) IS 'Performs intersection of two texts';
COMMENT ON OPERATOR - (NONE, integer) IS 'Unary minus';
COMMENT ON OPERATOR CLASS int4ops USING btree IS '4 byte integer operators for btrees';
COMMENT ON OPERATOR FAMILY integer_ops USING btree IS 'all integer operators for btrees';
COMMENT ON POLICY my_policy ON mytable IS 'Filter rows by users';
COMMENT ON PROCEDURE my_proc (integer, integer) IS 'Runs a report';
COMMENT ON PUBLICATION alltables IS 'Publishes all operations on all tables';
COMMENT ON ROLE my_role IS 'Administration group for finance tables';
COMMENT ON ROUTINE my_routine (integer, integer) IS 'Runs a routine (which is a function or procedure)';
COMMENT ON RULE my_rule ON my_table IS 'Logs updates of employee records';
COMMENT ON SCHEMA my_schema IS 'Departmental data';
COMMENT ON SEQUENCE my_sequence IS 'Used to generate primary keys';
COMMENT ON SERVER myserver IS 'my foreign server';
COMMENT ON STATISTICS my_statistics IS 'Improves planner row estimations';
COMMENT ON SUBSCRIPTION alltables IS 'Subscription for all operations on all tables';
COMMENT ON TABLE my_schema.my_table IS 'Employee Information';
COMMENT ON TABLESPACE my_tablespace IS 'Tablespace for indexes';
COMMENT ON TEXT SEARCH CONFIGURATION my_config IS 'Special word filtering';
COMMENT ON TEXT SEARCH DICTIONARY swedish IS 'Snowball stemmer for Swedish language';
COMMENT ON TEXT SEARCH PARSER my_parser IS 'Splits text into words';
COMMENT ON TEXT SEARCH TEMPLATE snowball IS 'Snowball stemmer';
COMMENT ON TRANSFORM FOR hstore LANGUAGE plpython3u IS 'Transform between hstore and Python dict';
COMMENT ON TRIGGER my_trigger ON my_table IS 'Used for RI';
COMMENT ON TYPE complex IS 'Complex number data type';
COMMENT ON VIEW my_view IS 'View of departmental costs';
COMMENT ON VIEW my_view IS NULL;
```

<a id="id-1.9.3.52.9"></a>

## 相容性

SQL 標準中沒有 `COMMENT` 命令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-comment.html)（原文版本：18.6；核對日期：2026-10-04）
