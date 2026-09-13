<a id="id-1.8.12.8.8.1"></a>

## SPI_prepare

SPI_prepare — 預備一個陳述式，但尚未執行它

## 概要

```

SPIPlanPtr SPI_prepare(const char * command, int nargs, Oid * argtypes)
```

<a id="id-1.8.12.8.8.5"></a>

## 描述

`SPI_prepare` 會為所指定的指令建立並回傳一個預備陳述式，但不會執行該指令。這個預備陳述式之後可以用 `SPI_execute_plan` 反覆執行。

當同一個或類似的指令要被反覆執行時，通常只進行一次剖析分析會比較有利，而且重複使用該指令的執行計畫可能也更有利。`SPI_prepare` 會把指令字串轉換成一個封裝了剖析分析結果的預備陳述式。若後來發現為每次執行都產生客製化計畫並沒有幫助，該預備陳述式也提供了一個快取執行計畫的地方。

預備好的指令可以透過在一般指令中原本應是常數的位置寫上參數（`$1`、`$2` 等）來加以通用化。參數的實際值則在呼叫 `SPI_execute_plan` 時才指定。這讓預備好的指令能用在比沒有參數時更廣泛的情境中。

`SPI_prepare` 所回傳的陳述式只能在目前這次 C 函式的呼叫中使用，因為 `SPI_finish` 會釋放為這類陳述式所配置的記憶體。不過，可以使用 `SPI_keepplan` 或 `SPI_saveplan` 函式把該陳述式保留得更久。

<a id="id-1.8.12.8.8.6"></a>

## 引數

`const char * command`
:   指令字串

`int nargs`
:   輸入參數的個數（`$1`、`$2` 等）

`Oid * argtypes`
:   指向一個陣列的指標，該陣列含有各參數之資料型別的 OID

<a id="id-1.8.12.8.8.7"></a>

## 回傳值

`SPI_prepare` 會回傳一個非 null 的指標，指向代表預備陳述式的不透明結構 `SPIPlan`。發生錯誤時會回傳 `NULL`，而且 `SPI_result` 會被設為與 `SPI_execute` 所使用的相同錯誤碼之一；例外的是，若 *`command`* 為 `NULL`、或 *`nargs`* 小於 0、或 *`nargs`* 大於 0 但 *`argtypes`* 為 `NULL`，則會被設為 `SPI_ERROR_ARGUMENT`。

<a id="id-1.8.12.8.8.8"></a>

## 註記

如果沒有定義任何參數，就會在第一次使用 `SPI_execute_plan` 時建立一個通用計畫，之後的所有執行也都會沿用它。如果有參數，前幾次使用 `SPI_execute_plan` 時會產生針對所提供之參數值的客製化計畫。在同一個預備陳述式被使用足夠多次之後，`SPI_execute_plan` 會建立一個通用計畫；如果該計畫不會比客製化計畫昂貴太多，它就會開始改用通用計畫，而不再每次都重新規劃。如果這個預設行為不合適，你可以把 `CURSOR_OPT_GENERIC_PLAN` 或 `CURSOR_OPT_CUSTOM_PLAN` 旗標傳給 `SPI_prepare_cursor` 來加以改變，分別強制使用通用計畫或客製化計畫。

雖然預備陳述式的主要目的是避免對陳述式反覆進行剖析分析與規劃，但只要陳述式中所使用的資料庫物件自上次使用該預備陳述式以來發生過定義（DDL）上的變更，PostgreSQL 就會在使用它之前強制重新分析並重新規劃該陳述式。此外，如果 [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 的值在前後兩次使用之間有所改變，該陳述式也會用新的 `search_path` 重新剖析。（後面這項行為是從 PostgreSQL 9.3 起才有的。）關於預備陳述式行為的更多資訊，請參閱 [PREPARE](../../reference/sql-commands/sql-prepare.md)。

這個函式只應該從已連線的 C 函式中呼叫。

`SPIPlanPtr` 在 `spi.h` 中宣告為指向某個不透明結構型別的指標。直接嘗試存取它的內容並不明智，因為那會讓你的程式碼在 PostgreSQL 未來的版本中更容易失效。

`SPIPlanPtr` 這個名稱帶有一些歷史因素，因為該資料結構如今並不一定含有執行計畫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-prepare.html)（原文版本：18.6；核對日期：2026-09-13）
