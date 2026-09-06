# ALTER EXTENSION

ALTER EXTENSION — 變更延伸功能的宣告內容

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

## 說明

ALTER EXTENSION 用來變更已安裝的延伸功能的定義。包括有幾個子形態：

`UPDATE`

此形態將該延伸功能更新為新的版本。該延伸功能必須提供合適的更新腳本（或一系列的腳本），可以將目前安裝的版本升級到要求更新的版本。

`SET SCHEMA`

這種形態將延伸功能的物件移動到另一個綱要中。該延伸功能必須是可以重新定位的，此命令才能成功。

`ADD` _`member_object`_

此形態將現有物件新增至延伸功能之中。這主要在延伸功能更新腳本時有用處。該物件隨後將被視為延伸功能的成員之一；值得注意的是，接下來也只能透過移除延伸功能來移除它。

`DROP` _`member_object`_

此形態從延伸功能中移除成員物件。這主要用於延伸功能的更新腳本之中。該物件並不會被實體移除，僅與該延伸功能脫離關連。

有關這些操作的更多資訊，請參閱[第 37.17 節](../../server-programming/extending-sql/packaging-related-objects-into-an-extension.md)。

您必須擁有該延伸功能才能使用 ALTER EXTENSION。ADD/DROP 形態還需要所要新增/移除物件的所有權。

## Parameters

_`name`_

The name of an installed extension.

_`new_version`_

The desired new version of the extension. This can be written as either an identifier or a string literal. If not specified, `ALTER EXTENSION UPDATE` attempts to update to whatever is shown as the default version in the extension's control file.

_`new_schema`_

The new schema for the extension.

_`object_name`_\
_`aggregate_name`_\
_`function_name`_\
_`operator_name`_\
_`procedure_name`_\
_`routine_name`_

The name of an object to be added to or removed from the extension. Names of tables, aggregates, domains, foreign tables, functions, operators, operator classes, operator families, procedures, routines, sequences, text search objects, types, and views can be schema-qualified.

_`source_type`_

The name of the source data type of the cast.

_`target_type`_

The name of the target data type of the cast.

_`argmode`_

The mode of a function, procedure, or aggregate argument: `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`. Note that `ALTER EXTENSION` does not actually pay any attention to `OUT`arguments, since only the input arguments are needed to determine the function's identity. So it is sufficient to list the `IN`, `INOUT`, and `VARIADIC` arguments.

_`argname`_

The name of a function, procedure, or aggregate argument. Note that `ALTER EXTENSION` does not actually pay any attention to argument names, since only the argument data types are needed to determine the function's identity.

_`argtype`_

The data type of a function, procedure, or aggregate argument.

_`left_type`_\
_`right_type`_

The data type(s) of the operator's arguments (optionally schema-qualified). Write `NONE` for the missing argument of a prefix or postfix operator.

`PROCEDURAL`

This is a noise word.

_`type_name`_

The name of the data type of the transform.

_`lang_name`_

The name of the language of the transform.

## 範例

要將 hstore 延伸功能更新到版本 2.0：

```
ALTER EXTENSION hstore UPDATE TO '2.0';
```

要將 hstore 延伸功能的綱要變更為 utils：

```
ALTER EXTENSION hstore SET SCHEMA utils;
```

要將現有函數新增到 hstore 延伸功能之中：

```
ALTER EXTENSION hstore ADD FUNCTION populate_record(anyelement, hstore);
```

## 相容性

ALTER EXTENSION 是 PostgreSQL 的延伸功能。

## 參閱

[CREATE EXTENSION](create-extension.md), [DROP EXTENSION](drop-extension.md)
