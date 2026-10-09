<a id="SQL-ALTEROPCLASS"></a><a id="id-1.9.3.21.1"></a>

## ALTER OPERATOR CLASS

ALTER OPERATOR CLASS — 變更運算子類別的定義

<a id="id-1.9.3.21.4"></a>

## 語法

```

ALTER OPERATOR CLASS name USING index_method
    RENAME TO new_name

ALTER OPERATOR CLASS name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS name USING index_method
    SET SCHEMA new_schema
```

<a id="id-1.9.3.21.5"></a>

## 說明

`ALTER OPERATOR CLASS` 會變更運算子類別的定義。

你必須是運算子類別的擁有者，才能使用 `ALTER OPERATOR CLASS`。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，而且該角色必須在運算子類別所屬的綱要上具有 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法透過移除並重新建立運算子類別而做到的事。不過，超級使用者無論如何都可以變更任何運算子類別的擁有權。）

<a id="id-1.9.3.21.6"></a>

## 參數

*`name`*
:   現有運算子類別的名稱（可選擇以綱要限定）。

*`index_method`*
:   此運算子類別所適用之索引方法的名稱。

*`new_name`*
:   運算子類別的新名稱。

*`new_owner`*
:   運算子類別的新擁有者。

*`new_schema`*
:   運算子類別的新綱要。

<a id="id-1.9.3.21.7"></a>

## 相容性

SQL 標準中沒有 `ALTER OPERATOR CLASS` 陳述式。

<a id="id-1.9.3.21.8"></a>

## 另請參閱

[CREATE OPERATOR CLASS](sql-createopclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md), [ALTER OPERATOR FAMILY](sql-alteropfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteropclass.html)（原文版本：18.6；核對日期：2026-10-05）
