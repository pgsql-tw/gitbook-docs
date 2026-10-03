<a id="SQL-DROPOPERATOR"></a><a id="id-1.9.3.119.1"></a>

## DROP OPERATOR

DROP OPERATOR — 移除運算子

<a id="id-1.9.3.119.4"></a>

## 語法

```

DROP OPERATOR [ IF EXISTS ] name ( { left_type | NONE } , right_type ) [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.119.5"></a>

## 說明

`DROP OPERATOR` 會從資料庫系統中移除現有的運算子。要執行此命令，您必須是該運算子的擁有者。

<a id="id-1.9.3.119.6"></a>

## 參數

`IF EXISTS`
:   運算子不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有運算子的名稱（可選擇以綱要限定）。

*`left_type`*
:   運算子左運算元的資料型別；若運算子沒有左運算元，請寫 `NONE`。

*`right_type`*
:   運算子右運算元的資料型別。

`CASCADE`
:   自動移除相依於該運算子的物件（例如使用它的檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該運算子則拒絕移除。這是預設行為。

<a id="id-1.9.3.119.7"></a>

## 範例

移除型別 `integer` 的次方運算子 `a^b`：

```

DROP OPERATOR ^ (integer, integer);
```

移除型別 `bit` 的位元補數前置運算子 `~b`：

```

DROP OPERATOR ~ (none, bit);
```

在一個命令中移除多個運算子：

```

DROP OPERATOR ~ (none, bit), ^ (integer, integer);
```

<a id="id-1.9.3.119.8"></a>

## 相容性

SQL 標準中沒有 `DROP OPERATOR` 陳述式。

<a id="id-1.9.3.119.9"></a>

## 另請參閱

[CREATE OPERATOR](sql-createoperator.md), [ALTER OPERATOR](sql-alteroperator.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropoperator.html)（原文版本：18.6；核對日期：2026-10-03）
