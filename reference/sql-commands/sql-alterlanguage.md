<a id="id-1.9.3.17.1"></a>

## ALTER LANGUAGE

ALTER LANGUAGE — 變更程序語言的定義

## 語法

```

ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.17.5"></a>

## 說明

`ALTER LANGUAGE` 會變更程序語言的定義。其功能僅限於重新命名語言或指定新的擁有者。你必須是超級使用者或該語言的擁有者，才能使用 `ALTER LANGUAGE`。

<a id="id-1.9.3.17.6"></a>

## 參數

*`name`*
:   語言名稱

*`new_name`*
:   語言的新名稱

*`new_owner`*
:   語言的新擁有者

<a id="id-1.9.3.17.7"></a>

## 相容性

SQL 標準中沒有 `ALTER LANGUAGE` 陳述式。

<a id="id-1.9.3.17.8"></a>

## 另請參閱

[CREATE LANGUAGE](sql-createlanguage.md), [DROP LANGUAGE](sql-droplanguage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterlanguage.html)（原文版本：18.6；核對日期：2026-09-07）
