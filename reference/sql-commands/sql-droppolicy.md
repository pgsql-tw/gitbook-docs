<a id="SQL-DROPPOLICY"></a><a id="id-1.9.3.123.1"></a>

## DROP POLICY

DROP POLICY — 從資料表移除資料列層級安全性政策

<a id="id-1.9.3.123.4"></a>

## 語法

```

DROP POLICY [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.123.5"></a>

## 說明

`DROP POLICY` 會從資料表移除指定的政策。
請注意，若某個資料表的最後一個政策被移除，而該資料表仍透過 `ALTER TABLE` 啟用資料列層級安全性，則會使用預設拒絕政策。無論該資料表是否存在政策，都可以使用 `ALTER TABLE ... DISABLE ROW
LEVEL SECURITY` 停用該資料表的資料列層級安全性。

<a id="id-1.9.3.123.6"></a>

## 參數

`IF EXISTS`
:   政策不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除的政策名稱。

*`table_name`*
:   該政策所在資料表的名稱（可選擇以綱要限定）。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有任何作用，因為沒有任何東西相依於政策。

<a id="id-1.9.3.123.7"></a>

## 範例

若要移除資料表 `my_table` 上名為 `p1` 的政策：

```

DROP POLICY p1 ON my_table;
```

<a id="id-1.9.3.123.8"></a>

## 相容性

`DROP POLICY` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.123.9"></a>

## 另請參閱

[CREATE POLICY](sql-createpolicy.md), [ALTER POLICY](sql-alterpolicy.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droppolicy.html)（原文版本：18.6；核對日期：2026-10-03）
