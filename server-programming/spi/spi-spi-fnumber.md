<a id="id-1.8.12.9.5.1"></a>

## SPI_fnumber

SPI_fnumber — 取得指定欄位名稱的欄位編號

## 語法

```

int SPI_fnumber(TupleDesc rowdesc, const char * colname)
```

<a id="id-1.8.12.9.5.5"></a>

## 說明

`SPI_fnumber` 會回傳指定名稱之欄位的欄位編號。

若 *`colname`* 指向系統欄位（例如 `ctid`），則會回傳對應的負數欄位編號。呼叫端應仔細檢查回傳值是否恰好等於 `SPI_ERROR_NOATTRIBUTE`，以偵測錯誤；除非要拒絕系統欄位，否則檢查結果是否小於或等於 0 並不正確。

<a id="id-1.8.12.9.5.6"></a>

## 引數

`TupleDesc rowdesc`
:   輸入資料列的描述資訊

`const char * colname`
:   欄位名稱

<a id="id-1.8.12.9.5.7"></a>

## 回傳值

欄位編號（使用者定義的欄位從 1 開始計算）；若找不到指定名稱的欄位，則回傳 `SPI_ERROR_NOATTRIBUTE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-fnumber.html)（原文版本：18.6；核對日期：2026-09-07）
