<a id="id-1.8.12.8.6.1"></a>

## SPI_execute_extended

SPI_execute_extended — 以外部（out-of-line）參數執行指令

## 概要

```

int SPI_execute_extended(const char *command,
                         const SPIExecuteOptions * options)
```

<a id="id-1.8.12.8.6.5"></a>

## 描述

`SPI_execute_extended` 會執行可能包含外部提供之參數參照的指令。指令文字以 `$n` 的形式參照參數，而 *`options->params`* 物件（若有提供）則為每個這樣的符號提供值與型別資訊。各種執行選項也可以在 *`options`* 結構中指定。

*`options->params`* 物件通常應該將每個參數都標上 `PARAM_FLAG_CONST` 旗標，因為這個查詢一律使用一次性的執行計畫。

如果 *`options->dest`* 不是 NULL，那麼結果 tuple 會在執行器產生時直接傳給該物件，而不會累積在 `SPI_tuptable` 中。對於可能產生大量 tuple 的查詢來說，使用由呼叫端提供的 `DestReceiver` 物件特別有幫助，因為資料可以即時處理，而不必累積在記憶體中。

<a id="id-1.8.12.8.6.6"></a>

## 引數

`const char * command`
:   指令字串

`const SPIExecuteOptions * options`
:   包含選擇性引數的結構

呼叫端應該一律先將整個 *`options`* 結構清為零，再填入想要設定的欄位。這可以確保程式碼的向前相容性，因為未來加入該結構的任何欄位，在其值為零時都會被定義成以向後相容的方式運作。目前可用的 *`options`* 欄位如下：

`ParamListInfo params`
:   包含查詢參數型別與值的資料結構；若沒有則為 NULL

`bool read_only`
:   `true` 表示唯讀執行

`bool allow_nonatomic`
:   `true` 允許以非原子方式執行 CALL 與 DO 陳述式（但除非有將 `SPI_OPT_NONATOMIC` 旗標傳給 `SPI_connect_ext`，否則這個欄位會被忽略）

`bool must_return_tuples`
:   若為 `true`，當查詢不屬於會回傳 tuple 的種類時就引發錯誤（這並不禁止查詢剛好回傳零個 tuple 的情況）

`uint64 tcount`
:   要回傳的最大資料列數，或是以 `0` 表示不限制

`DestReceiver * dest`
:   將接收該查詢所產生之所有 tuple 的 `DestReceiver` 物件；若為 NULL，結果 tuple 會像 `SPI_execute` 那樣累積到 `SPI_tuptable` 結構中

`ResourceOwner owner`
:   這個欄位是為了與 `SPI_execute_plan_extended` 保持一致而存在，但它會被忽略，因為 `SPI_execute_extended` 所使用的執行計畫從不會被儲存。

<a id="id-1.8.12.8.6.7"></a>

## 回傳值

回傳值與 `SPI_execute` 相同。

當 *`options->dest`* 為 NULL 時，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute` 相同。當 *`options->dest`* 不是 NULL 時，`SPI_processed` 會被設為零，而 `SPI_tuptable` 會被設為 NULL。如果需要 tuple 的計數，必須由呼叫端的 `DestReceiver` 物件自行計算。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute-extended.html)（原文版本：18.6；核對日期：2026-09-13）
