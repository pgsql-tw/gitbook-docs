<a id="id-1.9.3.40.1"></a>

## ALTER TEXT SEARCH TEMPLATE

ALTER TEXT SEARCH TEMPLATE — 變更文本搜尋模板的定義

## 語法

```

ALTER TEXT SEARCH TEMPLATE name RENAME TO new_name
ALTER TEXT SEARCH TEMPLATE name SET SCHEMA new_schema
```

<a id="id-1.9.3.40.5"></a>

## 說明

`ALTER TEXT SEARCH TEMPLATE` 會變更文本搜尋模板的定義。目前唯一支援的功能
是變更模板名稱。

你必須是超級使用者才能使用 `ALTER TEXT SEARCH TEMPLATE`。

<a id="id-1.9.3.40.6"></a>

## 參數

*`name`*
:   現有文本搜尋模板的名稱（可選擇以 schema 限定）。

*`new_name`*
:   文本搜尋模板的新名稱。

*`new_schema`*
:   文本搜尋模板的新 schema。

<a id="id-1.9.3.40.7"></a>

## 相容性

SQL 標準中沒有 `ALTER TEXT SEARCH TEMPLATE` 陳述式。

<a id="id-1.9.3.40.8"></a>

## 另請參閱

[CREATE TEXT SEARCH TEMPLATE](sql-createtstemplate.md), [DROP TEXT SEARCH TEMPLATE](sql-droptstemplate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertstemplate.html)（原文版本：18.6；核對日期：2026-09-10）
