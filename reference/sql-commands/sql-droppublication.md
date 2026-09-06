<a id="id-1.9.3.125.1"></a>

## DROP PUBLICATION

DROP PUBLICATION — 移除發佈物件

## 語法

```

DROP PUBLICATION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.125.5"></a>

## 說明

`DROP PUBLICATION` 會從資料庫移除既有的發佈物件。

只有發佈物件的擁有者或超級使用者可以刪除它。

<a id="id-1.9.3.125.6"></a>

## 參數

`IF EXISTS`
:   若發佈物件不存在，不拋出錯誤，而是發出一則提示。

*`name`*
:   既有發佈物件的名稱。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有任何作用，因為沒有物件依賴發佈物件。

<a id="id-1.9.3.125.7"></a>

## 範例

刪除發佈物件：

```

DROP PUBLICATION mypublication;
```

<a id="id-1.9.3.125.8"></a>

## 相容性

`DROP PUBLICATION` 是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.125.9"></a>

## 另請參閱

[CREATE PUBLICATION](sql-createpublication.md), [ALTER PUBLICATION](sql-alterpublication.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droppublication.html)（原文版本：18.6；核對日期：2026-09-07）
