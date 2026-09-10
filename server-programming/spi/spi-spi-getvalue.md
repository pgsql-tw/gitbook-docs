<a id="id-1.8.12.9.6.1"></a>

## SPI_getvalue

SPI_getvalue — 傳回指定欄位值的字串表示形式

## 語法

```

char * SPI_getvalue(HeapTuple row, TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.6.5"></a>

## 說明

`SPI_getvalue` 會傳回指定欄位值的字串表示形式。

結果會在以 `palloc` 配置的記憶體中傳回。（不再需要時，可使用 `pfree` 釋放該記憶體。）

<a id="id-1.8.12.9.6.6"></a>

## 引數

`HeapTuple row`
:   要檢查的輸入資料列。

`TupleDesc rowdesc`
:   輸入資料列描述

`int colnumber`
:   欄位編號（從 1 開始計數）

<a id="id-1.8.12.9.6.7"></a>

## 回傳值

欄位值；若欄位為 null、*`colnumber`* 超出範圍（`SPI_result` 設為 `SPI_ERROR_NOATTRIBUTE`），或沒有可用的輸出函式（`SPI_result` 設為 `SPI_ERROR_NOOUTFUNC`），則回傳 `NULL`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getvalue.html)（原文版本：18.6；核對日期：2026-09-10）
