<a id="id-1.8.12.8.22.1"></a>

## SPI_cursor_parse_open

SPI_cursor_parse_open — 使用一個查詢字串與參數設定一個游標

## 概要

```

Portal SPI_cursor_parse_open(const char *name,
                             const char *command,
                             const SPIParseOpenOptions * options)
```

<a id="id-1.8.12.8.22.5"></a>

## 描述

`SPI_cursor_parse_open` 會設定一個游標（在內部其實是一個 portal），用來執行所指定的查詢字串。這相當於先呼叫 `SPI_prepare_cursor` 再呼叫 `SPI_cursor_open_with_paramlist`，差別在於查詢字串中的參數參照完全是靠提供一個 `ParamListInfo` 物件來處理的。

如果查詢只執行一次，應優先使用這個函式，而不是先呼叫 `SPI_prepare_cursor` 再呼叫 `SPI_cursor_open_with_paramlist`。如果同一個指令要以許多不同的參數執行，兩種做法都有可能比較快，取決於重新規劃的成本與客製計畫所帶來的效益孰輕孰重。

*`options->params`* 物件通常應該把每一個參數都標上 `PARAM_FLAG_CONST` 旗標，因為該查詢一律會使用一次性的執行計畫。

傳入的參數資料會被複製到該游標的 portal 中，因此即使游標仍然存在，那份資料也可以先行釋放。

<a id="id-1.8.12.8.22.6"></a>

## 引數

`const char * name`
:   portal 的名稱，或是 `NULL` 表示讓系統自行挑選一個名稱

`const char * command`
:   指令字串

`const SPIParseOpenOptions * options`
:   含有選用引數的結構

呼叫端應該一律先把整個 *`options`* 結構清為零，再填入想要設定的欄位。這可確保程式碼的向前相容性，因為未來若在該結構中新增任何欄位，其定義都會讓欄位為零時保持向後相容的行為。目前可用的 *`options`* 欄位如下：

`ParamListInfo params`
:   包含查詢參數型別與值的資料結構；若沒有則為 NULL

`int cursorOptions`
:   游標選項的整數位元遮罩；零代表預設行為

`bool read_only`
:   `true` 表示唯讀執行

<a id="id-1.8.12.8.22.7"></a>

## 回傳值

指向含有該游標之 portal 的指標。請注意，這個函式沒有錯誤回傳慣例；任何錯誤都會透過 `elog` 回報。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-parse-open.html)（原文版本：18.6；核對日期：2026-09-13）
