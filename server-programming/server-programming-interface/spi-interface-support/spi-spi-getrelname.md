<a id="SPI-SPI-GETRELNAME"></a><a id="id-1.8.12.9.10.1"></a>

# SPI_getrelname

SPI_getrelname — return the name of the specified relation

## Synopsis

```

char * SPI_getrelname(Relation rel)
```

<a id="id-1.8.12.9.10.5"></a>

## Description

`SPI_getrelname` returns a copy of the name of the specified relation. (You can use `pfree` to release the copy of the name when you don't need it anymore.)

<a id="id-1.8.12.9.10.6"></a>

## Arguments

<code class="literal">Relation <em class="parameter"><code>rel</code></em></code>

input relation

<a id="id-1.8.12.9.10.7"></a>

## Return Value

The name of the specified relation.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-getrelname.html)（英文原文，待翻譯）
