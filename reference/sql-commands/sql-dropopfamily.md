<a id="SQL-DROPOPFAMILY"></a><a id="id-1.9.3.121.1"></a>

## DROP OPERATOR FAMILY

DROP OPERATOR FAMILY — 移除運算子家族

<a id="id-1.9.3.121.4"></a>

## 語法

```

DROP OPERATOR FAMILY [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.121.5"></a>

## 說明

`DROP OPERATOR FAMILY` 會移除現有的運算子家族。若要執行此命令，你必須是該運算子家族的擁有者。

`DROP OPERATOR FAMILY` 會一併移除該家族中包含的所有運算子類別，但不會移除該家族所參照的任何運算子或函式。若有任何索引相依於該家族中的運算子類別，你需要指定 `CASCADE` 才能完成移除。

<a id="id-1.9.3.121.6"></a>

## 參數

`IF EXISTS`
:   運算子家族不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有運算子家族的名稱（可選擇以綱要限定）。

*`index_method`*
:   該運算子家族所適用之索引存取方法的名稱。

`CASCADE`
:   自動移除相依於該運算子家族的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該運算子家族則拒絕移除。這是預設行為。

<a id="id-1.9.3.121.7"></a>

## 範例

移除 B-tree 運算子家族 `float_ops`：

```

DROP OPERATOR FAMILY float_ops USING btree;
```

若有任何現有索引使用該家族中的運算子類別，此命令將不會成功。加上 `CASCADE` 可將這些索引連同運算子家族一併移除。

<a id="id-1.9.3.121.8"></a>

## 相容性

SQL 標準中沒有 `DROP OPERATOR FAMILY` 陳述式。

<a id="id-1.9.3.121.9"></a>

## 另請參閱

[ALTER OPERATOR FAMILY](sql-alteropfamily.md), [CREATE OPERATOR FAMILY](sql-createopfamily.md), [ALTER OPERATOR CLASS](sql-alteropclass.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropopfamily.html)（原文版本：18.6；核對日期：2026-10-03）
