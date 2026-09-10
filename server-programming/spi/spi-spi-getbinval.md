<a id="id-1.8.12.9.7.1"></a>

## SPI_getbinval

SPI_getbinval — 傳回指定欄位的二進位值

## 語法

```

Datum SPI_getbinval(HeapTuple row, TupleDesc rowdesc, int colnumber,
                    bool * isnull)
```

<a id="id-1.8.12.9.7.5"></a>

## 說明

`SPI_getbinval` 會以內部形式（即 `Datum` 型別）傳回指定欄位的值。

此函式不會為該 datum 配置新的空間。若資料型別以傳址方式傳遞，回傳值會是指向所傳入資料列的指標。

<a id="id-1.8.12.9.7.6"></a>

## 引數

`HeapTuple row`
:   要檢查的輸入資料列。

`TupleDesc rowdesc`
:   輸入資料列描述。

`int colnumber`
:   欄位編號（從 1 開始計數）。

`bool * isnull`
:   指示欄位值是否為 null 的旗標。

<a id="id-1.8.12.9.7.7"></a>

## 回傳值

傳回欄位的二進位值。若欄位為 null，*`isnull`* 所指向的變數會設為 true；否則設為 false。

發生錯誤時，`SPI_result` 會設為 `SPI_ERROR_NOATTRIBUTE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getbinval.html)（原文版本：18.6；核對日期：2026-09-10）
