# COMMENT

COMMENT — 定義或變更物件的註解

## 語法

```text
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
  PUBLICATION object_name |
  ROLE object_name |
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
} IS 'text'

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## 說明

COMMENT 儲存有關資料庫物件的註解。

每個物件僅能儲存一個註解字串，因此要修改註解，請為同一物件發出新的 COMMENT 指令。 要刪除註解，請寫入 NULL 代替文字字串。當物件被移除時，註解也會自動移除。

對於大多數類型的物件，只有物件的擁有者才能設定註解。角色本身沒有擁有者，因此 COMMENT ON ROLE 的規則是您必須是超級使用者才能對超級使用者角色註解，或具有 CREATEROLE 權限才能對非超級使用者角色註解。 同樣，存取方法也沒有擁有者；所以您必須是超級使用者才能對存取方法留下註解。 當然，超級使用者可以對任何物件註解。

可以使用psql的 \d 系列指令查看註解。其他使用者界面要檢索註解的話，可以使用 psql 相同內建函數的建置，即 obj\_description，col\_description 和 shobj\_description（請參閱[表格 9.68](../../the-sql-language/functions-and-operators/system-information-functions.md#table-9-68-comment-information-functions)）。

## 參數

_`object_name`_  
_`relation_name`_._`column_name`_  
_`aggregate_name`_  
_`constraint_name`_  
_`function_name`_  
_`operator_name`_  
_`policy_name`_  
_`rule_name`_  
_`trigger_name`_

要註釋的物件名稱。Table、aggregate、collation、conversion、domain、foreign table、function、index、operator、operator class、sequence、statistics、text search object、type、view 的名稱，並且可以是指定 schema。在對欄位進行註釋時，relation\_name 必須引用資料表、檢視表、複合型別或外部資料表。

_`table_name`_  
_`domain_name`_

在 constraint、trigger、rule 或 policy 上建立註釋時，這些參數指定定義該物件的資料表或 domain 名稱。

_`source_type`_

來源資料型別轉換的名稱。

_`target_type`_

目標資料型別轉換的名稱。

_`argmode`_

函數或彙總函數的模式：IN，OUT，INOUT 或 VARIADIC。如果省略，則預設為 IN。請注意，COMMENT 實際上並不關心 OUT 參數，因為只需要輸入參數來決定函數的識別。因此，列出 IN，INOUT 和 VARIADIC 參數就足夠了。

_`argname`_

函數或彙總參數的名稱。請注意，COMMENT 實際上並不關心參數名稱，因為只需要參數資料型別來決定函數的識別。

_`argtype`_

函數或彙總參數的資料型別。

_`large_object_oid`_

large object 的 OID。

_`left_type`_  
_`right_type`_

運算子參數的資料型別（可加上綱要名稱）。使用 NONE 表示缺少前綴或後綴運算子的參數。

`PROCEDURAL`

這是一個噪音詞。

_`type_name`_

轉換的資料型別名稱。

_`lang_name`_

變換語言的名稱。

_`text`_

新的註解，寫成字串文字；或 NULL 以刪除註解。

## 注意

目前並沒有用於查看註解的安全機制：連線到資料庫的任何使用者可以看到該資料庫中的所有物件註解。對於資料庫而言，角色和資料表空間等共享物件，註解將以全域儲存，因此連線到叢集中任何資料庫的任何使用者都可以看到共享物件的所有註解。因此，請勿將安全關鍵訊息置於註解中。

## 範例

對資料表 mytable 加上註解：

```text
COMMENT ON TABLE mytable IS 'This is my table.';
```

再來移除它：

```text
COMMENT ON TABLE mytable IS NULL;
```

更多例子：

```text
COMMENT ON ACCESS METHOD rtree IS 'R-Tree access method';
COMMENT ON AGGREGATE my_aggregate (double precision) IS 'Computes sample variance';
COMMENT ON CAST (text AS int4) IS 'Allow casts from text to int4';
COMMENT ON COLLATION "fr_CA" IS 'Canadian French';
COMMENT ON COLUMN my_table.my_column IS 'Employee ID number';
COMMENT ON CONVERSION my_conv IS 'Conversion to UTF8';
COMMENT ON CONSTRAINT bar_col_cons ON bar IS 'Constrains column col';
COMMENT ON CONSTRAINT dom_col_constr ON DOMAIN dom IS 'Constrains col of domain';
COMMENT ON DATABASE my_database IS 'Development Database';
COMMENT ON DOMAIN my_domain IS 'Email Address Domain';
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
COMMENT ON ROLE my_role IS 'Administration group for finance tables';
COMMENT ON RULE my_rule ON my_table IS 'Logs updates of employee records';
COMMENT ON SCHEMA my_schema IS 'Departmental data';
COMMENT ON SEQUENCE my_sequence IS 'Used to generate primary keys';
COMMENT ON SERVER myserver IS 'my foreign server';
COMMENT ON STATISTICS my_statistics IS 'Improves planner row estimations';
COMMENT ON TABLE my_schema.my_table IS 'Employee Information';
COMMENT ON TABLESPACE my_tablespace IS 'Tablespace for indexes';
COMMENT ON TEXT SEARCH CONFIGURATION my_config IS 'Special word filtering';
COMMENT ON TEXT SEARCH DICTIONARY swedish IS 'Snowball stemmer for Swedish language';
COMMENT ON TEXT SEARCH PARSER my_parser IS 'Splits text into words';
COMMENT ON TEXT SEARCH TEMPLATE snowball IS 'Snowball stemmer';
COMMENT ON TRANSFORM FOR hstore LANGUAGE plpythonu IS 'Transform between hstore and Python dict';
COMMENT ON TRIGGER my_trigger ON my_table IS 'Used for RI';
COMMENT ON TYPE complex IS 'Complex number data type';
COMMENT ON VIEW my_view IS 'View of departmental costs';
```

## 相容性

SQL 標準中並沒有 COMMENT 指令。

