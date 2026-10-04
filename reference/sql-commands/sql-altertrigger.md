<a id="SQL-ALTERTRIGGER"></a><a id="id-1.9.3.41.1"></a>

## ALTER TRIGGER

ALTER TRIGGER — 變更觸發程序的定義

<a id="id-1.9.3.41.4"></a>

## 語法

```

ALTER TRIGGER name ON table_name RENAME TO new_name
ALTER TRIGGER name ON table_name [ NO ] DEPENDS ON EXTENSION extension_name
```

<a id="id-1.9.3.41.5"></a>

## 說明

`ALTER TRIGGER` 會變更現有觸發程序的屬性。

`RENAME` 子句會變更指定觸發程序的名稱，而不會以其他方式變更觸發程序的定義。若觸發程序所在的資料表是分割資料表，則各分割區中對應的複製觸發程序也會一併重新命名。

`DEPENDS ON EXTENSION` 子句會將觸發程序標記為相依於某個擴充功能，如此一來，若該擴充功能被移除，觸發程序也會自動被移除。

你必須擁有觸發程序所作用的資料表，才可以變更觸發程序的屬性。

<a id="id-1.9.3.41.6"></a>

## 參數

*`name`*
:   要變更之現有觸發程序的名稱。

*`table_name`*
:   此觸發程序所作用之資料表的名稱。

*`new_name`*
:   觸發程序的新名稱。

*`extension_name`*
:   觸發程序要相依的擴充功能名稱（若指定 `NO`，則為不再相依的擴充功能名稱）。被標記為相依於某個擴充功能的觸發程序，會在該擴充功能被移除時自動被移除。

<a id="id-1.9.3.41.7"></a>

## 注意事項

暫時啟用或停用觸發程序的功能是由 [`ALTER TABLE`](sql-altertable.md) 提供，而不是由 `ALTER TRIGGER` 提供，因為 `ALTER TRIGGER` 沒有方便的方式可以表達「一次啟用或停用某個資料表所有觸發程序」的選項。

<a id="id-1.9.3.41.8"></a>

## 範例

若要重新命名現有的觸發程序：

```

ALTER TRIGGER emp_stamp ON emp RENAME TO emp_track_chgs;
```

若要將觸發程序標記為相依於某個擴充功能：

```

ALTER TRIGGER emp_stamp ON emp DEPENDS ON EXTENSION emplib;
```

<a id="id-1.9.3.41.9"></a>

## 相容性

`ALTER TRIGGER` 是 PostgreSQL 對 SQL 標準的擴充語法。

<a id="id-1.9.3.41.10"></a>

## 另請參閱

[ALTER TABLE](sql-altertable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertrigger.html)（原文版本：18.6；核對日期：2026-10-04）
