<a id="id-1.8.12.8.14.1"></a>

## SPI_is_cursor_plan

SPI_is_cursor_plan — 判定 `SPI_prepare` 準備的陳述式是否可供 `SPI_cursor_open` 使用

## 語法

```

bool SPI_is_cursor_plan(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.14.5"></a>

## 說明

若 `SPI_prepare` 準備的陳述式可作為 `SPI_cursor_open` 的引數，`SPI_is_cursor_plan` 會傳回 `true`；否則傳回 `false`。條件是 *`plan`* 代表單一命令，且該命令會向呼叫端傳回 tuple；例如，不含 `INTO` 子句的 `SELECT` 可用，而 `UPDATE` 僅在含有 `RETURNING` 子句時可用。

<a id="id-1.8.12.8.14.6"></a>

## 引數

`SPIPlanPtr plan`
:   已準備的陳述式（由 `SPI_prepare` 傳回）。

<a id="id-1.8.12.8.14.7"></a>

## 回傳值

以 `true` 或 `false` 指示 *`plan`* 是否可產生游標，且 `SPI_result` 設為零。若無法判定（例如 *`plan`* 為 `NULL` 或無效，或未連線至 SPI 時呼叫），則 `SPI_result` 設為適當錯誤碼並傳回 `false`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-is-cursor-plan.html)（原文版本：18.6；核對日期：2026-09-10）
