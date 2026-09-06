<a id="id-1.9.3.28.1"></a>

## ALTER RULE

ALTER RULE — 變更規則的定義

## 語法

```

ALTER RULE name ON table_name RENAME TO new_name
```

<a id="id-1.9.3.28.5"></a>

## 說明

`ALTER RULE` 會變更既有規則的屬性。目前唯一可用的動作是變更規則名稱。

若要使用 `ALTER RULE`，你必須擁有該規則所套用的資料表或檢視表。

<a id="id-1.9.3.28.6"></a>

## 參數

*`name`*
:   要修改的既有規則名稱。

*`table_name`*
:   規則所套用的資料表或檢視表名稱（可加上 schema 名稱限定）。

*`new_name`*
:   規則的新名稱。

<a id="id-1.9.3.28.7"></a>

## 範例

重新命名既有規則：

```

ALTER RULE notify_all ON emp RENAME TO notify_me;
```

<a id="id-1.9.3.28.8"></a>

## 相容性

`ALTER RULE` 與整個查詢重寫系統一樣，都是 PostgreSQL 的語言擴充功能。

<a id="id-1.9.3.28.9"></a>

## 另請參閱

[CREATE RULE](sql-createrule.md), [DROP RULE](sql-droprule.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterrule.html)（原文版本：18.6；核對日期：2026-09-07）
