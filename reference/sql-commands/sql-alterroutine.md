<a id="SQL-ALTERROUTINE"></a><a id="id-1.9.3.27.1"></a>

## ALTER ROUTINE

ALTER ROUTINE — 變更常式的定義

<a id="id-1.9.3.27.4"></a>

## 語法

```

ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    IMMUTABLE | STABLE | VOLATILE
    [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

<a id="id-1.9.3.27.5"></a>

## 說明

`ALTER ROUTINE` 會變更常式的定義；常式可以是彙總函式、一般函式或程序。參數說明、更多範例與進一步的細節，請參閱 [ALTER AGGREGATE](sql-alteraggregate.md)、[ALTER FUNCTION](sql-alterfunction.md) 與 [ALTER PROCEDURE](sql-alterprocedure.md)。

<a id="id-1.9.3.27.6"></a>

## 範例

將引數型別為 `integer` 的常式 `foo` 重新命名為 `foobar`：

```

ALTER ROUTINE foo(integer) RENAME TO foobar;
```

無論 `foo` 是彙總函式、函式還是程序，此命令都能運作。

<a id="id-1.9.3.27.7"></a>

## 相容性

此陳述式與 SQL 標準中的 `ALTER
ROUTINE` 陳述式部分相容。更多細節請參閱 [ALTER FUNCTION](sql-alterfunction.md) 與 [ALTER PROCEDURE](sql-alterprocedure.md)。允許常式名稱指向彙總函式是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.27.8"></a>

## 另請參閱

[ALTER AGGREGATE](sql-alteraggregate.md), [ALTER FUNCTION](sql-alterfunction.md), [ALTER PROCEDURE](sql-alterprocedure.md), [DROP ROUTINE](sql-droproutine.md)

請注意，沒有 `CREATE ROUTINE` 命令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterroutine.html)（原文版本：18.6；核對日期：2026-10-05）
