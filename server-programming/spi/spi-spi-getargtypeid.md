<a id="id-1.8.12.8.13.1"></a>

## SPI_getargtypeid

SPI_getargtypeid — 回傳由 `SPI_prepare` 準備之陳述式中某個引數的資料型別 OID

## 語法

```

Oid SPI_getargtypeid(SPIPlanPtr plan, int argIndex)
```

<a id="id-1.8.12.8.13.5"></a>

## 說明

`SPI_getargtypeid` 會回傳由 `SPI_prepare` 準備之陳述式中，索引為 *`argIndex`* 的引數型別 OID。第一個引數的索引為零。

<a id="id-1.8.12.8.13.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`int argIndex`
:   從零開始的引數索引

<a id="id-1.8.12.8.13.7"></a>

## 回傳值

指定索引處引數的型別 OID。若 *`plan`* 為 `NULL` 或無效，或 *`argIndex`* 小於 0，或不小於 *`plan`* 所宣告的引數數量，則將 `SPI_result` 設為 `SPI_ERROR_ARGUMENT`，並回傳 `InvalidOid`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getargtypeid.html)（原文版本：18.6；核對日期：2026-09-07）
