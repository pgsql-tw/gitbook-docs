<a id="id-1.8.12.8.11.1"></a>

## SPI_prepare_params

SPI_prepare_params — 準備陳述式，但尚不執行

## 語法

```

SPIPlanPtr SPI_prepare_params(const char * command,
                              ParserSetupHook parserSetup,
                              void * parserSetupArg,
                              int cursorOptions)
```

<a id="id-1.8.12.8.11.5"></a>

## 說明

`SPI_prepare_params` 為指定命令建立並回傳已準備的陳述式，但不執行該命令。此函式等同於 `SPI_prepare_cursor`，但呼叫端還可指定剖析器掛鉤函式，以控制外部參數參照的剖析。

此函式現已棄用，請改用 `SPI_prepare_extended`。

<a id="id-1.8.12.8.11.6"></a>

## 引數

`const char * command`
:   命令字串

`ParserSetupHook parserSetup`
:   剖析器掛鉤設定函式

`void * parserSetupArg`
:   傳遞給 *`parserSetup`* 的引數

`int cursorOptions`
:   游標選項的整數位元遮罩；零代表預設行為

<a id="id-1.8.12.8.11.7"></a>

## 回傳值

`SPI_prepare_params` 使用與 `SPI_prepare` 相同的回傳慣例。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-prepare-params.html)（原文版本：18.6；核對日期：2026-09-06）
