<a id="SQL-CALL"></a><a id="id-1.9.3.48.1"></a>

## CALL

CALL — 呼叫程序

<a id="id-1.9.3.48.4"></a>

## 語法

```

CALL name ( [ argument ] [, ...] )
```

<a id="id-1.9.3.48.5"></a>

## 說明

`CALL` 會執行一個程序。

若該程序有任何輸出參數，則會傳回一筆結果資料列，其中包含這些參數的值。

<a id="id-1.9.3.48.6"></a>

## 參數

*`name`*
:   程序的名稱（可選擇以綱要限定）。

*`argument`*
:   程序呼叫的引數運算式。

    引數可以包含參數名稱，使用語法
    `name => value`。
    這與一般函式呼叫的運作方式相同；詳情請參閱
    [第 4.3 節](../../the-sql-language/sql-syntax/sql-syntax-calling-funcs.md)。

    所有沒有預設值的程序參數都必須提供引數，包括 `OUT` 參數。不過，
    對應 `OUT` 參數的引數不會被求值，
    所以慣例上只要為它們寫 `NULL` 即可。
    （為 `OUT` 參數寫入其他內容，
    可能會造成與
    未來 PostgreSQL 版本的相容性問題。）

<a id="id-1.9.3.48.7"></a>

## 注意事項

使用者必須擁有該程序的 `EXECUTE` 權限，
才能呼叫它。

若要呼叫函式（而非程序），請改用 `SELECT`。

若 `CALL` 在交易區塊中執行，則
被呼叫的程序不能執行交易控制陳述式。
只有當 `CALL`
在其自己的交易中執行時，才允許使用交易控制陳述式。

PL/pgSQL 對
`CALL` 命令中輸出參數的處理方式不同；
請參閱[第 41.6.3 節](../../server-programming/plpgsql/plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)。

<a id="id-1.9.3.48.8"></a>

## 範例

```

CALL do_db_maintenance();
```

<a id="id-1.9.3.48.9"></a>

## 相容性

`CALL` 符合 SQL 標準，
但輸出參數的處理方式除外。標準規定，
使用者應該寫出變數來接收
輸出參數的值。

<a id="id-1.9.3.48.10"></a>

## 另請參閱

[CREATE PROCEDURE](sql-createprocedure.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-call.html)（原文版本：18.6；核對日期：2026-10-04）
