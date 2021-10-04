# SECURITY LABEL

SECURITY LABEL — 定義或變更套用於物件的安全標籤

### 語法

```text
SECURITY LABEL [ FOR provider ] ON
{
  TABLE object_name |
  COLUMN table_name.column_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  DATABASE object_name |
  DOMAIN object_name |
  EVENT TRIGGER object_name |
  FOREIGN TABLE object_name
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  LARGE OBJECT large_object_oid |
  MATERIALIZED VIEW object_name |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  PUBLICATION object_name |
  ROLE object_name |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  SCHEMA object_name |
  SEQUENCE object_name |
  SUBSCRIPTION object_name |
  TABLESPACE object_name |
  TYPE object_name |
  VIEW object_name
} IS 'label'

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

### 說明

SECURITY LABEL 將安全標籤套用於資料庫物件。可以將任意數量的安全標籤，每個標籤提供者各一個，與給定的資料庫物件相關聯。標籤提供程序是可動態載入的模塊，它們透過使用函數 register\_label\_provider 進行註冊。

**注意**  
register\_label\_provider 並不是 SQL 函數；只能從載入到後端的 C 程式中呼叫它。

標籤提供者決定給定的標籤是否有效以及是否可以將該標籤分配給指定的物件。標籤所賦予的含義同樣由標籤提供者決定。PostgreSQL 對標籤提供者是否必須解釋或如何解釋安全標籤沒有任何限制；它僅提供了一種儲存它們的機制。實際上，此功能旨在允許與基於標籤的強制性存取控制（Mandatory Access Control, MAC）系統（例如 SELinux）集成。 這樣的系統基於物件標籤而不是傳統的自由訪問控制（Discretionary Access Control, DAC）概念（例如使用者和群組）做出所有存取控制決策。

### Parameters

_`object_name`_  
_`table_name.column_name`_  
_`aggregate_name`_  
_`function_name`_  
_`procedure_name`_  
_`routine_name`_

The name of the object to be labeled. Names of tables, aggregates, domains, foreign tables, functions, procedures, routines, sequences, types, and views can be schema-qualified.

_`provider`_

The name of the provider with which this label is to be associated. The named provider must be loaded and must consent to the proposed labeling operation. If exactly one provider is loaded, the provider name may be omitted for brevity.

_`argmode`_

The mode of a function, procedure, or aggregate argument: `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`. Note that `SECURITY LABEL` does not actually pay any attention to `OUT` arguments, since only the input arguments are needed to determine the function's identity. So it is sufficient to list the `IN`, `INOUT`, and `VARIADIC` arguments.

_`argname`_

The name of a function, procedure, or aggregate argument. Note that `SECURITY LABEL` does not actually pay any attention to argument names, since only the argument data types are needed to determine the function's identity.

_`argtype`_

The data type of a function, procedure, or aggregate argument.

_`large_object_oid`_

The OID of the large object.

`PROCEDURAL`

This is a noise word.

_`label`_

The new security label, written as a string literal; or `NULL` to drop the security label.

### 範例

以下範例展示如何變更資料表的安全標籤。

```text
SECURITY LABEL FOR selinux ON TABLE mytable IS 'system_u:object_r:sepgsql_table_t:s0';
```

### 相容性

SQL 標準中沒有 SECURITY LABEL 指令。

### 參閱

[sepgsql](../../appendixes/additional-supplied-modules/sepgsql.md), `src/test/modules/dummy_seclabel`

