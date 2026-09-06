<a id="id-1.8.12.9.9.1"></a>

## SPI_gettypeid

SPI_gettypeid — 回傳指定欄位的資料型別 OID

## 語法

```

Oid SPI_gettypeid(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.9.5"></a>

## 說明

`SPI_gettypeid` 會回傳指定欄位之資料型別的 OID。

<a id="id-1.8.12.9.9.6"></a>

## 引數

`TupleDesc rowdesc`
:   輸入資料列的描述資訊

`int colnumber`
:   欄位編號（從 1 開始計算）

<a id="id-1.8.12.9.9.7"></a>

## 回傳值

指定欄位之資料型別的 OID；發生錯誤時回傳 `InvalidOid`。發生錯誤時，`SPI_result` 會設為 `SPI_ERROR_NOATTRIBUTE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-gettypeid.html)（原文版本：18.6；核對日期：2026-09-07）
