<a id="SQL-DROPFUNCTION"></a><a id="id-1.9.3.114.1"></a>

## DROP FUNCTION

DROP FUNCTION — 移除函式

<a id="id-1.9.3.114.4"></a>

## 語法

```

DROP FUNCTION [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.114.5"></a>

## 說明

`DROP FUNCTION` 會移除現有函式的定義。要執行此命令，使用者必須是該函式的擁有者。必須指定函式的引數型別，因為可能存在多個名稱相同但引數列表不同的函式。

<a id="id-1.9.3.114.6"></a>

## 參數

`IF EXISTS`
:   函式不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有函式的名稱（可選擇以綱要限定）。若未指定引數列表，該名稱在其綱要中必須是唯一的。

*`argmode`*
:   引數的模式：`IN`、`OUT`、
    `INOUT` 或 `VARIADIC`。
    若省略，預設為 `IN`。
    請注意，`DROP FUNCTION` 實際上並不理會 `OUT` 引數，因為只需要輸入引數就能判定函式的身分。
    因此只需列出 `IN`、`INOUT`
    與 `VARIADIC` 引數就足夠了。

*`argname`*
:   引數的名稱。
    請注意，`DROP FUNCTION` 實際上並不理會引數名稱，因為只需要引數的資料型別就能判定函式的身分。

*`argtype`*
:   函式引數（若有）的資料型別（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於函式的物件（例如運算子或觸發程序），以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於函式則拒絕移除。這是預設行為。

<a id="SQL-DROPFUNCTION-EXAMPLES"></a>

## 範例

以下命令會移除平方根函式：

```

DROP FUNCTION sqrt(integer);
```

在一個命令中移除多個函式：

```

DROP FUNCTION sqrt(integer), sqrt(bigint);
```

若函式名稱在其綱要中是唯一的，就可以不加引數列表來引用它：

```

DROP FUNCTION update_employee_salaries;
```

請注意，這與以下命令不同：

```

DROP FUNCTION update_employee_salaries();
```

後者引用的是沒有引數的函式；而前一種寫法只要名稱是唯一的，就可以引用具有任意數量引數（包括零個）的函式。

<a id="SQL-DROPFUNCTION-COMPATIBILITY"></a>

## 相容性

此命令符合 SQL 標準，但有以下 PostgreSQL 擴充功能：

* 標準只允許每個命令移除一個函式。
* `IF EXISTS` 選項
* 指定引數模式與名稱的能力

<a id="id-1.9.3.114.9"></a>

## 另請參閱

[CREATE FUNCTION](sql-createfunction.md), [ALTER FUNCTION](sql-alterfunction.md), [DROP PROCEDURE](sql-dropprocedure.md), [DROP ROUTINE](sql-droproutine.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropfunction.html)（原文版本：18.6；核對日期：2026-10-03）
