# DROP FUNCTION

DROP FUNCTION — 移除一個函數

## 語法

```text
DROP FUNCTION [ IF EXISTS ] name 
              [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] 
              [, ...]
              [ CASCADE | RESTRICT ]
```

## 說明

DROP FUNCTION 移除現有函數的定義。要執行此命令，使用者必須是該函數的擁有者。必須指定該函數的參數類型，因為可能存在多個具有相同名稱和不同參數列表的不同函數。

## 參數

`IF EXISTS`

如果函數不存在，不要拋出錯誤。在這種情況下發布 NOTICE。

_`name`_

現有函數的名稱（可以加上綱要）。如果未指定參數列表，則該名稱在其綱要中必須是唯一的。

_`argmode`_

參數的模式：IN、OUT、INOUT 或 VARIADIC。如果省略，則預設為 IN。請注意，DROP FUNCTION 實際上並不關注 OUT 參數，因為只需要輸入參數來確定函數的身份。所以列出 IN、INOUT 和 VARIADIC 參數就足夠了。

_`argname`_

參數的名稱。 請注意，DROP FUNCTION 實際上並不關注參數名稱，因為只需要參數資料型別來確定函數的身份。

_`argtype`_

如果有的話，函數參數的資料型別（可加上綱要）。

`CASCADE`

自動刪除依賴於該功能的物件（如運算子或觸發器），並依次移除依賴於這些物件的所有物件（請參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果任何物件依賴於它，拒絕移除該函數。這是預設的做法。

## 範例

此指令移除平方根函數：

```text
DROP FUNCTION sqrt(integer);
```

在一個指令中刪除多個函數：

```text
DROP FUNCTION sqrt(integer), sqrt(bigint);
```

如果函數名稱在其綱要中是唯一的，則可以在不帶參數列表的情況下引用它：

```text
DROP FUNCTION update_employee_salaries;
```

請注意，這不同於

```text
DROP FUNCTION update_employee_salaries();
```

它指的是一個零個參數的函數，而第一個變形可以引用具有任意數量參數的函數，包括零個，只要該名稱是唯一的。

## 相容性

這個指令符合 SQL 標準，並帶有這些 PostgreSQL 的延伸功能：

* 原標準只允許每個指令刪除一個函數。
* 具有 IF EXISTS 選項
* 能夠指定參數模式和名稱

## 參閱

[CREATE FUNCTION](create-function.md), [ALTER FUNCTION](alter-function.md)

