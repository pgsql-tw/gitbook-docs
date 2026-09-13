<a id="id-1.8.12.8.17.1"></a>

## SPI_execute_plan_with_paramlist

SPI_execute_plan_with_paramlist — 執行由 `SPI_prepare` 預備好的陳述式

## 概要

```

int SPI_execute_plan_with_paramlist(SPIPlanPtr plan,
                                    ParamListInfo params,
                                    bool read_only,
                                    long count)
```

<a id="id-1.8.12.8.17.5"></a>

## 描述

`SPI_execute_plan_with_paramlist` 會執行由 `SPI_prepare` 所預備的陳述式。這個函式等同於 `SPI_execute_plan`，差別在於要傳給查詢的參數值資訊是以不同的方式呈現。對於傳遞已經是該格式的值來說，`ParamListInfo` 這種表示法相當方便。它也支援透過在 `ParamListInfo` 中指定的 hook 函式來使用動態參數集。

這個函式現在已不建議使用，請改用 `SPI_execute_plan_extended`。

<a id="id-1.8.12.8.17.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`ParamListInfo params`
:   包含參數型別與值的資料結構；若沒有則為 NULL

`bool read_only`
:   `true` 表示唯讀執行

`long count`
:   要回傳的最大資料列數，或是以 `0` 表示不限制

<a id="id-1.8.12.8.17.7"></a>

## 回傳值

回傳值與 `SPI_execute_plan` 相同。

若執行成功，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute_plan` 相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute-plan-with-paramlist.html)（原文版本：18.6；核對日期：2026-09-12）
