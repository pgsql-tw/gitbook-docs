<a id="id-1.8.12.8.16.1"></a>

## SPI_execute_plan_extended

SPI_execute_plan_extended — 執行由 `SPI_prepare` 預備好的陳述式

## 概要

```

int SPI_execute_plan_extended(SPIPlanPtr plan,
                              const SPIExecuteOptions * options)
```

<a id="id-1.8.12.8.16.5"></a>

## 描述

`SPI_execute_plan_extended` 會執行由 `SPI_prepare` 或其同類函式所預備的陳述式。這個函式等同於 `SPI_execute_plan`，差別在於要傳給查詢的參數值資訊是以不同的方式呈現，而且還可以傳入額外的執行控制選項。

查詢參數值是以 `ParamListInfo` 結構來表示，對於傳遞已經是該格式的值來說相當方便。也可以透過在 `ParamListInfo` 中指定的 hook 函式來使用動態參數集。

此外，結果 tuple 不一定要累積到 `SPI_tuptable` 結構中，也可以在執行器產生它們時傳給由呼叫端提供的 `DestReceiver` 物件。對於可能產生大量 tuple 的查詢來說，這特別有幫助，因為資料可以即時處理，而不必累積在記憶體中。

<a id="id-1.8.12.8.16.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

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
:   將接收該查詢所產生之所有 tuple 的 `DestReceiver` 物件；若為 NULL，結果 tuple 會像 `SPI_execute_plan` 那樣累積到 `SPI_tuptable` 結構中

`ResourceOwner owner`
:   在執行計畫執行期間持有其參考計數的資源擁有者。若為 NULL，則會使用 CurrentResourceOwner。對於未儲存的執行計畫則會被忽略，因為 SPI 不會對它們取得參考計數。

<a id="id-1.8.12.8.16.7"></a>

## 回傳值

回傳值與 `SPI_execute_plan` 相同。

當 *`options->dest`* 為 NULL 時，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute_plan` 相同。當 *`options->dest`* 不是 NULL 時，`SPI_processed` 會被設為零，而 `SPI_tuptable` 會被設為 NULL。如果需要 tuple 的計數，必須由呼叫端的 `DestReceiver` 物件自行計算。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute-plan-extended.html)（原文版本：18.6；核對日期：2026-09-12）
