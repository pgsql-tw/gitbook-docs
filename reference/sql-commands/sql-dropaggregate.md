<a id="SQL-DROPAGGREGATE"></a><a id="id-1.9.3.104.1"></a>

## DROP AGGREGATE

DROP AGGREGATE — 移除彙總函式

<a id="id-1.9.3.104.4"></a>

## 語法

```

DROP AGGREGATE [ IF EXISTS ] name ( aggregate_signature ) [, ...] [ CASCADE | RESTRICT ]

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

<a id="id-1.9.3.104.5"></a>

## 說明

`DROP AGGREGATE` 會移除現有的彙總函式。要執行此命令，目前使用者必須是該彙總函式的擁有者。

<a id="id-1.9.3.104.6"></a>

## 參數

`IF EXISTS`
:   彙總函式不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有彙總函式的名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN` 或 `VARIADIC`。若省略，預設為 `IN`。

*`argname`*
:   引數的名稱。請注意，`DROP AGGREGATE` 實際上並不會理會引數名稱，因為只需要引數的資料型別就能確定彙總函式的身分。

*`argtype`*
:   彙總函式所處理的輸入資料型別。若要引用零引數的彙總函式，請以 `*` 代替引數規格列表。若要引用有序集合彙總函式，請在直接引數與彙總引數的規格之間寫上 `ORDER BY`。

`CASCADE`
:   自動移除相依於彙總函式的物件（例如使用它的檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於彙總函式則拒絕移除。這是預設行為。

<a id="id-1.9.3.104.7"></a>

## 注意事項

引用有序集合彙總函式的替代語法，說明於 [ALTER AGGREGATE](sql-alteraggregate.md)。

<a id="id-1.9.3.104.8"></a>

## 範例

若要移除型別 `integer` 的彙總函式 `myavg`：

```

DROP AGGREGATE myavg(integer);
```

若要移除假設集合彙總函式 `myrank`，它接受任意的排序欄位列表，以及相對應的直接引數列表：

```

DROP AGGREGATE myrank(VARIADIC "any" ORDER BY VARIADIC "any");
```

若要在一個命令中移除多個彙總函式：

```

DROP AGGREGATE myavg(integer), myavg(bigint);
```

<a id="id-1.9.3.104.9"></a>

## 相容性

SQL 標準中沒有 `DROP AGGREGATE` 陳述式。

<a id="id-1.9.3.104.10"></a>

## 另請參閱

[ALTER AGGREGATE](sql-alteraggregate.md), [CREATE AGGREGATE](sql-createaggregate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropaggregate.html)（原文版本：18.6；核對日期：2026-10-03）
