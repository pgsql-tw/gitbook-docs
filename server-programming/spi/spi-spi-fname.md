<a id="id-1.8.12.9.4.1"></a>

## SPI_fname

SPI_fname — 取得指定欄位編號的欄位名稱

## 語法

```

char * SPI_fname(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.4.5"></a>

## 說明

`SPI_fname` 會回傳指定欄位名稱的副本。（不再需要此名稱副本時，可以使用 `pfree` 釋放。）

<a id="id-1.8.12.9.4.6"></a>

## 引數

`TupleDesc rowdesc`
:   輸入資料列的描述資訊

`int colnumber`
:   欄位編號（從 1 開始計算）

<a id="id-1.8.12.9.4.7"></a>

## 回傳值

欄位名稱；若 *`colnumber`* 超出範圍則回傳 `NULL`。發生錯誤時，`SPI_result` 會設為 `SPI_ERROR_NOATTRIBUTE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-fname.html)（原文版本：18.6；核對日期：2026-09-07）
