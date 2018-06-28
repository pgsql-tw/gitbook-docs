# COMMENT

COMMENT — 定義或變更物件的註解

### 語法

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

### 說明

COMMENT 儲存有關資料庫物件的註解。

每個物件僅能儲存一個註解字串，因此要修改註解，請為同一物件發出新的 COMMENT 指令。 要刪除註解，請寫入 NULL 代替文字字串。當物件被移除時，註解也會自動移除。

對於大多數類型的物件，只有物件的擁有者才能設定註解。角色本身沒有擁有者，因此 COMMENT ON ROLE 的規則是您必須是超級使用者才能對超級使用者角色註解，或具有 CREATEROLE 權限才能對非超級使用者角色註解。 同樣，存取方法也沒有擁有者；所以您必須是超級使用者才能對存取方法留下註解。 當然，超級使用者可以對任何物件註解。

可以使用psql的 \d 系列指令查看註解。其他使用者界面要檢索註解的話，可以使用 psql 相同內建函數的建置，即 obj\_description，col\_description 和 shobj\_description（請參閱[表格 9.68](../../ii.-sql-cha-xun-yu-yan/9.-han-shi-ji-yun-suan-zi/9.25.-xi-tong-zi-xun-han-shu.md#table-9-68-comment-information-functions)）。

### Parameters

_`object_name`_  
_`relation_name`_._`column_name`_  
_`aggregate_name`_  
_`constraint_name`_  
_`function_name`_  
_`operator_name`_  
_`policy_name`_  
_`rule_name`_  
_`trigger_name`_

The name of the object to be commented. Names of tables, aggregates, collations, conversions, domains, foreign tables, functions, indexes, operators, operator classes, operator families, sequences, statistics, text search objects, types, and views can be schema-qualified. When commenting on a column, _`relation_name`_ must refer to a table, view, composite type, or foreign table.

_`table_name`_  
_`domain_name`_

When creating a comment on a constraint, a trigger, a rule or a policy these parameters specify the name of the table or domain on which that object is defined.

_`source_type`_

The name of the source data type of the cast.

_`target_type`_

The name of the target data type of the cast.

_`argmode`_

The mode of a function or aggregate argument: `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`. Note that `COMMENT` does not actually pay any attention to `OUT` arguments, since only the input arguments are needed to determine the function's identity. So it is sufficient to list the `IN`, `INOUT`, and `VARIADIC` arguments.

_`argname`_

The name of a function or aggregate argument. Note that `COMMENT` does not actually pay any attention to argument names, since only the argument data types are needed to determine the function's identity.

_`argtype`_

The data type of a function or aggregate argument.

_`large_object_oid`_

The OID of the large object.

_`left_type`_  
_`right_type`_

The data type\(s\) of the operator's arguments \(optionally schema-qualified\). Write `NONE` for the missing argument of a prefix or postfix operator.

`PROCEDURAL`

This is a noise word.

_`type_name`_

The name of the data type of the transform.

_`lang_name`_

The name of the language of the transform.

_`text`_

The new comment, written as a string literal; or `NULL` to drop the comment.

### 注意

目前並沒有用於查看註解的安全機制：連線到資料庫的任何使用者可以看到該資料庫中的所有物件註解。對於資料庫而言，角色和資料表空間等共享物件，註解將以全域儲存，因此連線到叢集中任何資料庫的任何使用者都可以看到共享物件的所有註解。因此，請勿將安全關鍵訊息置於註解中。

### 範例

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

### 相容性

SQL 標準中並沒有 COMMENT 指令。

