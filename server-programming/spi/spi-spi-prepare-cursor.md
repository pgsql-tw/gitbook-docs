<a id="id-1.8.12.8.9.1"></a>

## SPI_prepare_cursor

SPI_prepare_cursor — 準備陳述式，但尚不執行

## 語法

```

SPIPlanPtr SPI_prepare_cursor(const char * command, int nargs,
                              Oid * argtypes, int cursorOptions)
```

<a id="id-1.8.12.8.9.5"></a>

## 說明

`SPI_prepare_cursor` 與 `SPI_prepare` 相同，但還允許指定規劃器的「游標選項」參數。它是位元遮罩，其值列於 `nodes/parsenodes.h` 的 `DeclareCursorStmt` `options` 欄位。`SPI_prepare` 一律將游標選項設為零。

此函式現已棄用，請改用 `SPI_prepare_extended`。

<a id="id-1.8.12.8.9.6"></a>

## 引數

`const char * command`
:   命令字串

`int nargs`
:   輸入參數數目（`$1`、`$2` 等）

`Oid * argtypes`
:   指向含有參數資料型別 OID 之陣列的指標

`int cursorOptions`
:   游標選項的整數位元遮罩；零代表預設行為

<a id="id-1.8.12.8.9.7"></a>

## 回傳值

`SPI_prepare_cursor` 使用與 `SPI_prepare` 相同的回傳慣例。

<a id="id-1.8.12.8.9.8"></a>

## 注意事項

可在 *`cursorOptions`* 設定的有用位元包括 `CURSOR_OPT_SCROLL`、`CURSOR_OPT_NO_SCROLL`、`CURSOR_OPT_FAST_PLAN`、`CURSOR_OPT_GENERIC_PLAN` 與 `CURSOR_OPT_CUSTOM_PLAN`。請特別注意，`CURSOR_OPT_HOLD` 會被忽略。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-prepare-cursor.html)（原文版本：18.6；核對日期：2026-09-06）
