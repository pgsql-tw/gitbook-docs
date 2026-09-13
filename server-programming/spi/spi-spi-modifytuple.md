<a id="id-1.8.12.10.11.1"></a>

## SPI_modifytuple

SPI_modifytuple — 以取代指定資料列中某些欄位的方式建立一個資料列

## 概要

```

HeapTuple SPI_modifytuple(Relation rel, HeapTuple row, int ncols,
                          int * colnum, Datum * values, const char * nulls)
```

<a id="id-1.8.12.10.11.5"></a>

## 描述

`SPI_modifytuple` 會以新值取代選定欄位的方式建立一個新的資料列，其他位置的欄位則從原本的資料列複製過來。輸入的資料列不會被修改。新的資料列會在上層執行器的記憶體上下文中回傳。

這個函式只能在連接到 SPI 的狀態下使用。否則它會回傳 NULL，並將 `SPI_result` 設為 `SPI_ERROR_UNCONNECTED`。

<a id="id-1.8.12.10.11.6"></a>

## 引數

`Relation rel`
:   只用來作為該資料列之資料列描述子的來源。（傳入關聯而非資料列描述子是一項設計缺失。）

`HeapTuple row`
:   要被修改的資料列

`int ncols`
:   要變更的欄位數

`int * colnum`
:   長度為 *`ncols`* 的陣列，內含要變更之欄位的編號（欄位編號從 1 開始）

`Datum * values`
:   長度為 *`ncols`* 的陣列，內含指定欄位的新值

`const char * nulls`
:   長度為 *`ncols`* 的陣列，描述哪些新值為 NULL

    如果 *`nulls`* 是 `NULL`，則 `SPI_modifytuple` 會假設沒有任何新值是 NULL。否則，*`nulls`* 陣列的每個項目在對應的新值不為 NULL 時應該是 `' '`，在對應的新值為 NULL 時則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中的實際值並不重要。）請注意，*`nulls`* 並不是文字字串，而只是一個陣列：它不需要 `'\0'` 結束符號。

<a id="id-1.8.12.10.11.7"></a>

## 回傳值

修改後的新資料列，配置於上層執行器的記憶體上下文中；發生錯誤時則為 `NULL`（錯誤指示請參閱 `SPI_result`）

發生錯誤時，`SPI_result` 會被設定如下：

`SPI_ERROR_ARGUMENT`
:   如果 *`rel`* 是 `NULL`，或 *`row`* 是 `NULL`，或 *`ncols`* 小於或等於 0，或 *`colnum`* 是 `NULL`，或 *`values`* 是 `NULL`。

`SPI_ERROR_NOATTRIBUTE`
:   如果 *`colnum`* 中含有無效的欄位編號（小於或等於 0，或大於 *`row`* 中的欄位數）

`SPI_ERROR_UNCONNECTED`
:   如果 SPI 未在作用中

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-modifytuple.html)（原文版本：18.6；核對日期：2026-09-13）
