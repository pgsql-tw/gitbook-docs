<a id="SQL-DROPOPCLASS"></a><a id="id-1.9.3.120.1"></a>

## DROP OPERATOR CLASS

DROP OPERATOR CLASS — 移除運算子類別

<a id="id-1.9.3.120.4"></a>

## 語法

```

DROP OPERATOR CLASS [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.120.5"></a>

## 說明

`DROP OPERATOR CLASS` 會移除現有的運算子類別。
要執行此命令，您必須是該運算子類別的擁有者。

`DROP OPERATOR CLASS` 不會移除該類別所引用的任何運算子或函式。若有任何索引相依於該運算子類別，您需要指定
`CASCADE` 才能完成移除。

<a id="id-1.9.3.120.6"></a>

## 參數

`IF EXISTS`
:   運算子類別不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有運算子類別的名稱（可選擇以綱要限定）。

*`index_method`*
:   該運算子類別所適用之索引存取方法的名稱。

`CASCADE`
:   自動移除相依於運算子類別的物件（例如索引），以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於運算子類別則拒絕移除。這是預設行為。

<a id="id-1.9.3.120.7"></a>

## 注意事項

`DROP OPERATOR CLASS` 不會移除包含該類別的運算子家族，即使該家族中已沒有其他任何成員也一樣（特別是在該家族是由 `CREATE OPERATOR CLASS` 隱含建立的情況下）。空的運算子家族並無害處，但為了整潔起見，您可能會想用 `DROP OPERATOR FAMILY` 移除該家族；或者更好的做法是，一開始就使用 `DROP OPERATOR FAMILY`。

<a id="id-1.9.3.120.8"></a>

## 範例

移除 B-tree 運算子類別 `widget_ops`：

```

DROP OPERATOR CLASS widget_ops USING btree;
```

若有任何現有索引使用該運算子類別，此命令將不會成功。加上 `CASCADE` 即可將這些索引連同運算子類別一併移除。

<a id="id-1.9.3.120.9"></a>

## 相容性

SQL 標準中沒有 `DROP OPERATOR CLASS` 陳述式。

<a id="id-1.9.3.120.10"></a>

## 另請參閱

[ALTER OPERATOR CLASS](sql-alteropclass.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [DROP OPERATOR FAMILY](sql-dropopfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropopclass.html)（原文版本：18.6；核對日期：2026-10-03）
