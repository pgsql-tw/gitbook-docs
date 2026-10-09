<a id="SQL-ALTERMATERIALIZEDVIEW"></a><a id="id-1.9.3.19.1"></a>

## ALTER MATERIALIZED VIEW

ALTER MATERIALIZED VIEW — 變更具體化檢視表的定義

<a id="id-1.9.3.19.4"></a>

## 語法

```

ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    action [, ... ]
ALTER MATERIALIZED VIEW name
    [ NO ] DEPENDS ON EXTENSION extension_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME TO new_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    SET SCHEMA new_schema
ALTER MATERIALIZED VIEW ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]

where action is one of:

    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name SET COMPRESSION compression_method
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET ACCESS METHOD new_access_method
    SET TABLESPACE new_tablespace
    SET ( storage_parameter [= value] [, ... ] )
    RESET ( storage_parameter [, ... ] )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.19.5"></a>

## 說明

`ALTER MATERIALIZED VIEW` 會變更現有具體化檢視表的各種輔助屬性。

你必須是具體化檢視表的擁有者，才能使用 `ALTER MATERIALIZED
VIEW`。若要變更具體化檢視表的綱要，你還必須在新的綱要上具有 `CREATE` 權限。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，而且該角色必須在具體化檢視表所屬的綱要上具有 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法透過移除並重新建立具體化檢視表而做到的事。不過，超級使用者無論如何都可以變更任何檢視表的擁有權。）

`ALTER MATERIALIZED VIEW` 可用的陳述式子形式與動作，是 `ALTER TABLE` 可用者的子集，用於具體化檢視表時意義相同。詳細資訊請參閱 [`ALTER TABLE`](sql-altertable.md) 的說明。

<a id="id-1.9.3.19.6"></a>

## 參數

*`name`*
:   現有具體化檢視表的名稱（可選擇以綱要限定）。

*`column_name`*
:   現有欄位的名稱。

*`extension_name`*
:   具體化檢視表要相依的擴充功能名稱（若指定 `NO`，則為不再相依的擴充功能）。被標記為相依於某個擴充功能的具體化檢視表，會在該擴充功能被移除時自動移除。

*`new_column_name`*
:   現有欄位的新名稱。

*`new_owner`*
:   具體化檢視表新擁有者的使用者名稱。

*`new_name`*
:   具體化檢視表的新名稱。

*`new_schema`*
:   具體化檢視表的新綱要。

<a id="id-1.9.3.19.7"></a>

## 範例

將具體化檢視表 `foo` 重新命名為 `bar`：

```

ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

<a id="id-1.9.3.19.8"></a>

## 相容性

`ALTER MATERIALIZED VIEW` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.19.9"></a>

## 另請參閱

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altermaterializedview.html)（原文版本：18.6；核對日期：2026-10-05）
