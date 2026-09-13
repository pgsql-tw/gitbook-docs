<a id="id-1.8.12.8.20.1"></a>

## SPI_cursor_open_with_args

SPI_cursor_open_with_args — 使用一個查詢與參數設定一個 cursor

## 概要

```

Portal SPI_cursor_open_with_args(const char *name,
                                 const char *command,
                                 int nargs, Oid *argtypes,
                                 Datum *values, const char *nulls,
                                 bool read_only, int cursorOptions)
```

<a id="id-1.8.12.8.20.5"></a>

## 描述

`SPI_cursor_open_with_args` 會設定一個 cursor（在內部其實是一個 portal），用來執行所指定的查詢。大多數參數的意義與 `SPI_prepare_cursor` 及 `SPI_cursor_open` 中對應的參數相同。

如果查詢只執行一次，應優先使用這個函式，而不是先呼叫 `SPI_prepare_cursor` 再呼叫 `SPI_cursor_open`。如果同一個指令要以許多不同的參數執行，兩種做法都有可能比較快，取決於重新規劃的成本與客製計畫所帶來的效益孰輕孰重。

傳入的參數資料會被複製到該 cursor 的 portal 中，因此即使 cursor 仍然存在，那份資料也可以先行釋放。

這個函式現在已不建議使用，請改用 `SPI_cursor_parse_open`，它以更現代的 API 處理查詢參數，並提供相同的功能。

<a id="id-1.8.12.8.20.6"></a>

## 引數

`const char * name`
:   portal 的名稱，或是 `NULL` 表示讓系統自行挑選一個名稱

`const char * command`
:   指令字串

`int nargs`
:   輸入參數的個數（`$1`、`$2` 等等）

`Oid * argtypes`
:   長度為 *`nargs`* 的陣列，內含各參數資料型別的 OID

`Datum * values`
:   長度為 *`nargs`* 的陣列，內含實際的參數值

`const char * nulls`
:   長度為 *`nargs`* 的陣列，用來描述哪些參數為 NULL

    如果 *`nulls`* 為 `NULL`，`SPI_cursor_open_with_args` 就會假設沒有任何參數是 NULL。否則，若對應的參數值不是 NULL，*`nulls`* 陣列中的每一個項目都應該是 `' '`；若對應的參數值是 NULL，則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中實際存放的值並不重要。）請注意，*`nulls`* 並不是一個文字字串，而只是一個陣列：它不需要 `'\0'` 結尾字元。

`bool read_only`
:   `true` 表示唯讀執行

`int cursorOptions`
:   cursor 選項的整數位元遮罩；零代表預設行為

<a id="id-1.8.12.8.20.7"></a>

## 回傳值

指向含有該 cursor 之 portal 的指標。請注意，這個函式沒有錯誤回傳慣例；任何錯誤都會透過 `elog` 回報。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-open-with-args.html)（原文版本：18.6；核對日期：2026-09-12）
