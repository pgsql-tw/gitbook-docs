<a id="id-1.8.12.8.19.1"></a>

## SPI_cursor_open

SPI_cursor_open — 使用以 `SPI_prepare` 建立的陳述式設定一個游標

## 概要

```

Portal SPI_cursor_open(const char * name, SPIPlanPtr plan,
                       Datum * values, const char * nulls,
                       bool read_only)
```

<a id="id-1.8.12.8.19.5"></a>

## 描述

`SPI_cursor_open` 會設定一個游標（在內部其實是一個 portal），用來執行由 `SPI_prepare` 所預備的陳述式。各個參數的意義與 `SPI_execute_plan` 中對應的參數相同。

使用游標而不直接執行陳述式有兩項好處。第一，結果資料列可以一次取回少量，避免會回傳大量資料列的查詢耗盡記憶體。第二，portal 的存活時間可以超過目前的 C 函式（事實上它可以一直存活到目前交易結束）。把 portal 名稱回傳給該 C 函式的呼叫端，就提供了一種以資料列集合作為結果回傳的方式。

傳入的參數資料會被複製到該游標的 portal 中，因此即使游標仍然存在，那份資料也可以先行釋放。

<a id="id-1.8.12.8.19.6"></a>

## 引數

`const char * name`
:   portal 的名稱，或是 `NULL` 表示讓系統自行挑選一個名稱

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`Datum * values`
:   實際參數值的陣列。長度必須與該陳述式的引數個數相同。

`const char * nulls`
:   描述哪些參數為 NULL 的陣列。長度必須與該陳述式的引數個數相同。

    如果 *`nulls`* 為 `NULL`，`SPI_cursor_open` 就會假設沒有任何參數是 NULL。否則，若對應的參數值不是 NULL，*`nulls`* 陣列中的每一個項目都應該是 `' '`；若對應的參數值是 NULL，則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中實際存放的值並不重要。）請注意，*`nulls`* 並不是一個文字字串，而只是一個陣列：它不需要 `'\0'` 結尾字元。

`bool read_only`
:   `true` 表示唯讀執行

<a id="id-1.8.12.8.19.7"></a>

## 回傳值

指向含有該游標之 portal 的指標。請注意，這個函式沒有錯誤回傳慣例；任何錯誤都會透過 `elog` 回報。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-open.html)（原文版本：18.6；核對日期：2026-09-13）
