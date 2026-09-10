<a id="id-1.9.3.132.1"></a>

## DROP STATISTICS

DROP STATISTICS — 移除擴充統計資訊

## 語法

```

DROP STATISTICS [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.132.5"></a>

## 說明

`DROP STATISTICS` 會從資料庫移除統計資訊物件。只有統計資訊物件擁有者、schema 擁有者或超級使用者可以移除統計資訊物件。

<a id="id-1.9.3.132.6"></a>

## 參數

`IF EXISTS`
:   統計資訊物件不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除統計資訊物件的名稱（可選擇以 schema 限定）。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有作用，因為統計資訊沒有相依性。

<a id="id-1.9.3.132.7"></a>

## 範例

若要銷毀兩個不同 schema 中的統計資訊物件，且在物件不存在時不失敗：

```

DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

<a id="id-1.9.3.132.8"></a>

## 相容性

SQL 標準中沒有 `DROP STATISTICS` 命令。

<a id="id-1.9.3.132.9"></a>

## 另請參閱

[ALTER STATISTICS](sql-alterstatistics.md), [CREATE STATISTICS](sql-createstatistics.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropstatistics.html)（原文版本：18.6；核對日期：2026-09-10）
