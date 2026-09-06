<a id="id-1.8.12.9.8.1"></a>

## SPI_gettype

SPI_gettype — 回傳指定欄位的資料型別名稱

## 語法

```

char * SPI_gettype(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.8.5"></a>

## 說明

`SPI_gettype` 會回傳指定欄位之資料型別名稱的副本。（不再需要此名稱副本時，可以使用 `pfree` 釋放。）

<a id="id-1.8.12.9.8.6"></a>

## 引數

`TupleDesc rowdesc`
:   輸入資料列的描述資訊

`int colnumber`
:   欄位編號（從 1 開始計算）

<a id="id-1.8.12.9.8.7"></a>

## 回傳值

指定欄位的資料型別名稱；發生錯誤時回傳 `NULL`。發生錯誤時，`SPI_result` 會設為 `SPI_ERROR_NOATTRIBUTE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-gettype.html)（原文版本：18.6；核對日期：2026-09-07）
