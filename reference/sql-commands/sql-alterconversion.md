<a id="SQL-ALTERCONVERSION"></a><a id="id-1.9.3.6.1"></a>

## ALTER CONVERSION

ALTER CONVERSION — 變更轉換的定義

<a id="id-1.9.3.6.4"></a>

## 語法

```

ALTER CONVERSION name RENAME TO new_name
ALTER CONVERSION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER CONVERSION name SET SCHEMA new_schema
```

<a id="id-1.9.3.6.5"></a>

## 說明

`ALTER CONVERSION` 會變更轉換的定義。

你必須擁有該轉換才能使用 `ALTER CONVERSION`。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有角色，而且該角色必須擁有該轉換所屬綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立轉換而做到的事。不過，超級使用者無論如何都可以變更任何轉換的擁有權。）

<a id="id-1.9.3.6.6"></a>

## 參數

*`name`*
:   現有轉換的名稱（可選擇以綱要限定）。

*`new_name`*
:   轉換的新名稱。

*`new_owner`*
:   轉換的新擁有者。

*`new_schema`*
:   轉換的新綱要。

<a id="id-1.9.3.6.7"></a>

## 範例

若要將轉換 `iso_8859_1_to_utf8` 重新命名為 `latin1_to_unicode`：

```

ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

若要將轉換 `iso_8859_1_to_utf8` 的擁有者變更為 `joe`：

```

ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

<a id="id-1.9.3.6.8"></a>

## 相容性

SQL 標準中沒有 `ALTER CONVERSION` 陳述式。

<a id="id-1.9.3.6.9"></a>

## 另請參閱

[CREATE CONVERSION](sql-createconversion.md), [DROP CONVERSION](sql-dropconversion.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterconversion.html)（原文版本：18.6；核對日期：2026-10-09）
