<a id="id-1.8.12.9.10.1"></a>

## SPI_getrelname

SPI_getrelname — 回傳指定關聯的名稱

## 語法

```

char * SPI_getrelname(Relation rel)
```

<a id="id-1.8.12.9.10.5"></a>

## 說明

`SPI_getrelname` 會回傳指定關聯名稱的副本。（不再需要此名稱副本時，可以使用 `pfree` 釋放。）

<a id="id-1.8.12.9.10.6"></a>

## 引數

`Relation rel`
:   輸入關聯

<a id="id-1.8.12.9.10.7"></a>

## 回傳值

指定關聯的名稱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getrelname.html)（原文版本：18.6；核對日期：2026-09-07）
