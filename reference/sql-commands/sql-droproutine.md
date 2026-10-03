<a id="SQL-DROPROUTINE"></a><a id="id-1.9.3.127.1"></a>

## DROP ROUTINE

DROP ROUTINE — 移除常式

<a id="id-1.9.3.127.4"></a>

## 語法

```

DROP ROUTINE [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.127.5"></a>

## 說明

`DROP ROUTINE` 會移除一個或多個現有常式的定義。「常式」一詞涵蓋彙總函式、一般函式與程序。參數說明、更多範例與進一步細節，請參閱 [DROP AGGREGATE](sql-dropaggregate.md)、[DROP FUNCTION](sql-dropfunction.md) 與 [DROP PROCEDURE](sql-dropprocedure.md)。

<a id="SQL-DROPROUTINE-NOTES"></a>

## 注意事項

`DROP ROUTINE` 所使用的查找規則基本上與 `DROP PROCEDURE` 相同；特別是，`DROP ROUTINE` 也具有該命令的這項行為：對於沒有任何 *`argmode`* 標記的引數列表，會考慮它可能採用 SQL 標準的定義，也就是 `OUT` 引數也包含在列表中。（`DROP AGGREGATE` 與 `DROP FUNCTION` 不會這樣做。）

在某些同一名稱由不同種類的常式共用的情況下，`DROP ROUTINE` 可能會因歧義錯誤而失敗，而較具體的命令（`DROP
FUNCTION` 等）則可以正常運作。更仔細地指定引數型別列表，也同樣能解決此類問題。

這些查找規則也用於其他作用於現有常式的命令，例如 `ALTER ROUTINE` 與 `COMMENT ON ROUTINE`。

<a id="SQL-DROPROUTINE-EXAMPLES"></a>

## 範例

若要移除型別 `integer` 的常式 `foo`：

```

DROP ROUTINE foo(integer);
```

無論 `foo` 是彙總函式、函式還是程序，此命令都能運作。

<a id="SQL-DROPROUTINE-COMPATIBILITY"></a>

## 相容性

此命令符合 SQL 標準，但有以下 PostgreSQL 擴充功能：

* 標準只允許每個命令移除一個常式。
* `IF EXISTS` 選項是擴充功能。
* 可以指定引數模式與名稱是擴充功能，而且在指定了模式時，查找規則會有所不同。
* 使用者可自行定義的彙總函式是擴充功能。

<a id="id-1.9.3.127.9"></a>

## 另請參閱

[DROP AGGREGATE](sql-dropaggregate.md), [DROP FUNCTION](sql-dropfunction.md), [DROP PROCEDURE](sql-dropprocedure.md), [ALTER ROUTINE](sql-alterroutine.md)

請注意，並沒有 `CREATE ROUTINE` 命令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droproutine.html)（原文版本：18.6；核對日期：2026-10-03）
