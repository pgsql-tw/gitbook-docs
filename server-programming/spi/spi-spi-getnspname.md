<a id="id-1.8.12.9.11.1"></a>

## SPI_getnspname

SPI_getnspname — 回傳指定關聯的命名空間

## 語法

```

char * SPI_getnspname(Relation rel)
```

<a id="id-1.8.12.9.11.5"></a>

## 說明

`SPI_getnspname` 會回傳指定 `Relation` 所屬命名空間名稱的副本。這等同於該關聯的 schema。使用完此函式的回傳值後，應以 `pfree` 釋放。

<a id="id-1.8.12.9.11.6"></a>

## 引數

`Relation rel`
:   輸入關聯

<a id="id-1.8.12.9.11.7"></a>

## 回傳值

指定關聯所屬命名空間的名稱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getnspname.html)（原文版本：18.6；核對日期：2026-09-07）
