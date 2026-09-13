<a id="id-1.8.12.8.7.1"></a>

## SPI_execute_with_args

SPI_execute_with_args — 以外部（out-of-line）參數執行指令

## 概要

```

int SPI_execute_with_args(const char *command,
                          int nargs, Oid *argtypes,
                          Datum *values, const char *nulls,
                          bool read_only, long count)
```

<a id="id-1.8.12.8.7.5"></a>

## 描述

`SPI_execute_with_args` 會執行可能包含外部提供之參數參照的指令。指令文字以 `$n` 的形式參照參數，而呼叫時則為每個這樣的符號指定資料型別與值。*`read_only`* 與 *`count`* 的意義和 `SPI_execute` 中的相同。

相較於 `SPI_execute`，這個常式的主要優點是資料值可以插入指令中，而不必進行繁瑣的引號處理／跳脫，因此遭受 SQL 注入攻擊的風險也小得多。

使用 `SPI_prepare` 再接著 `SPI_execute_plan` 也可以達到類似的結果；不過使用本函式時，查詢計畫一律會針對所提供的特定參數值來客製化。對於只執行一次的查詢，應該優先採用本函式。如果同一個指令要用許多不同的參數來執行，兩種做法哪一種比較快，則要看重新規劃的成本與客製化計畫所帶來的好處孰輕孰重。

<a id="id-1.8.12.8.7.6"></a>

## 引數

`const char * command`
:   指令字串

`int nargs`
:   輸入參數的個數（`$1`、`$2` 等等）

`Oid * argtypes`
:   長度為 *`nargs`* 的陣列，內含各參數資料型別的 OID

`Datum * values`
:   長度為 *`nargs`* 的陣列，內含實際的參數值

`const char * nulls`
:   長度為 *`nargs`* 的陣列，描述哪些參數為 NULL

    如果 *`nulls`* 是 `NULL`，則 `SPI_execute_with_args` 會假設沒有任何參數是 NULL。否則，*`nulls`* 陣列的每個項目在對應的參數值不為 NULL 時應該是 `' '`，在對應的參數值為 NULL 時則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中的實際值並不重要。）請注意，*`nulls`* 並不是文字字串，而只是一個陣列：它不需要 `'\0'` 結束符號。

`bool read_only`
:   `true` 表示唯讀執行

`long count`
:   要回傳的最大資料列數，或是以 `0` 表示不限制

<a id="id-1.8.12.8.7.7"></a>

## 回傳值

回傳值與 `SPI_execute` 相同。

若執行成功，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute` 相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute-with-args.html)（原文版本：18.6；核對日期：2026-09-12）
