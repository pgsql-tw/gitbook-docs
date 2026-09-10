<a id="id-1.8.12.10.10.1"></a>

## SPI_returntuple

SPI_returntuple — 準備將 tuple 作為 Datum 傳回

## 語法

```

HeapTupleHeader SPI_returntuple(HeapTuple row, TupleDesc rowdesc)
```

<a id="id-1.8.12.10.10.5"></a>

## 說明

`SPI_returntuple` 會將資料列複製到上層執行器環境，然後以資料列型別 `Datum` 傳回。
回傳前只需透過 `PointerGetDatum` 將回傳的指標轉換為 `Datum`。

此函式只能在連線至 SPI 時使用。否則會傳回 NULL，並將 `SPI_result` 設為
`SPI_ERROR_UNCONNECTED`。

請注意，此函式應用於宣告為傳回複合型別的函式。它不適用於觸發器；如要在觸發器中
傳回已修改的資料列，請使用 `SPI_copytuple`。

<a id="id-1.8.12.10.10.6"></a>

## 引數

`HeapTuple row`
:   要複製的資料列。

`TupleDesc rowdesc`
:   資料列描述（每次傳入相同描述可獲得最有效的快取）。

<a id="id-1.8.12.10.10.7"></a>

## 回傳值

指向已複製資料列的 `HeapTupleHeader`；發生錯誤時傳回 `NULL`
（錯誤指示請參閱 `SPI_result`）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-returntuple.html)（原文版本：18.6；核對日期：2026-09-10）
