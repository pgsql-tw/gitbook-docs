<a id="id-1.8.12.8.10.1"></a>

## SPI_prepare_extended

SPI_prepare_extended — 預備一個陳述式，但尚未執行它

## 概要

```

SPIPlanPtr SPI_prepare_extended(const char * command,
                                const SPIPrepareOptions * options)
```

<a id="id-1.8.12.8.10.5"></a>

## 描述

`SPI_prepare_extended` 會為指定的指令建立並回傳一個預備陳述式，但不會執行該指令。這個函式等同於 `SPI_prepare`，另外還讓呼叫端可以指定選項，以控制外部參數參照的剖析方式，以及查詢剖析與規劃的其他面向。

<a id="id-1.8.12.8.10.6"></a>

## 引數

`const char * command`
:   指令字串

`const SPIPrepareOptions * options`
:   包含選擇性引數的結構

呼叫端應該一律先將整個 *`options`* 結構清為零，再填入想要設定的欄位。這可以確保程式碼的向前相容性，因為未來加入該結構的任何欄位，在其值為零時都會被定義成以向後相容的方式運作。目前可用的 *`options`* 欄位如下：

`ParserSetupHook parserSetup`
:   剖析器 hook 的設定函式

`void * parserSetupArg`
:   傳遞給 *`parserSetup`* 的引數

`RawParseMode parseMode`
:   原始剖析（raw parsing）的模式；`RAW_PARSE_DEFAULT`（零）會產生預設行為

`int cursorOptions`
:   游標選項的整數位元遮罩；零會產生預設行為

<a id="id-1.8.12.8.10.7"></a>

## 回傳值

`SPI_prepare_extended` 的回傳慣例與 `SPI_prepare` 相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-prepare-extended.html)（原文版本：18.6；核對日期：2026-09-13）
