<a id="id-1.9.3.29.1"></a>

## ALTER SCHEMA

ALTER SCHEMA — 變更 schema 的定義

## 語法

```

ALTER SCHEMA name RENAME TO new_name
ALTER SCHEMA name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.29.5"></a>

## 說明

`ALTER SCHEMA` 會變更 schema 的定義。

你必須擁有該 schema 才能使用 `ALTER SCHEMA`。若要重新命名 schema，你也必須擁有資料庫的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有資料庫的 `CREATE` 權限。（超級使用者自動擁有所有這些權限。）

<a id="id-1.9.3.29.6"></a>

## 參數

*`name`*
:   現有 schema 的名稱。

*`new_name`*
:   schema 的新名稱。新名稱不能以 `pg_` 開頭，因為此類名稱保留給系統 schema。

*`new_owner`*
:   schema 的新擁有者。

<a id="id-1.9.3.29.7"></a>

## 相容性

SQL 標準中沒有 `ALTER SCHEMA` 陳述式。

<a id="id-1.9.3.29.8"></a>

## 另請參閱

[CREATE SCHEMA](sql-createschema.md), [DROP SCHEMA](sql-dropschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterschema.html)（原文版本：18.6；核對日期：2026-09-10）
