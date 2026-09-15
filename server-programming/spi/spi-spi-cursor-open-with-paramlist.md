<a id="id-1.8.12.8.21.1"></a>

## SPI_cursor_open_with_paramlist

SPI_cursor_open_with_paramlist — 使用參數設定一個游標

## 概要

```

Portal SPI_cursor_open_with_paramlist(const char *name,
                                      SPIPlanPtr plan,
                                      ParamListInfo params,
                                      bool read_only)
```

<a id="id-1.8.12.8.21.5"></a>

## 描述

`SPI_cursor_open_with_paramlist` 會設定一個游標（在內部其實是一個 portal），用來執行由 `SPI_prepare` 所預備的陳述式。這個函式等同於 `SPI_cursor_open`，差別在於要傳給查詢的參數值資訊是以不同的方式呈現。對於傳遞已經是該格式的值來說，`ParamListInfo` 這種表示法相當方便。它也支援透過在 `ParamListInfo` 中指定的 hook 函式來使用動態參數集。

傳入的參數資料會被複製到該游標的 portal 中，因此即使游標仍然存在，那份資料也可以先行釋放。

<a id="id-1.8.12.8.21.6"></a>

## 引數

`const char * name`
:   portal 的名稱，或是 `NULL` 表示讓系統自行挑選一個名稱

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`ParamListInfo params`
:   包含參數型別與值的資料結構；若沒有則為 NULL

`bool read_only`
:   `true` 表示唯讀執行

<a id="id-1.8.12.8.21.7"></a>

## 回傳值

指向含有該游標之 portal 的指標。請注意，這個函式沒有錯誤回傳慣例；任何錯誤都會透過 `elog` 回報。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-open-with-paramlist.html)（原文版本：18.6；核對日期：2026-09-13）
