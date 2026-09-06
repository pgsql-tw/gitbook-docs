<a id="id-1.8.12.9.11.1"></a>

## SPI_getnspname

SPI_getnspname — return the namespace of the specified relation

## Synopsis

```

char * SPI_getnspname(Relation rel)
```

<a id="id-1.8.12.9.11.5"></a>

## Description

`SPI_getnspname` returns a copy of the name of
the namespace that the specified `Relation`
belongs to. This is equivalent to the relation's schema. You should
`pfree` the return value of this function when
you are finished with it.

<a id="id-1.8.12.9.11.6"></a>

## Arguments

`Relation rel`
:   input relation

<a id="id-1.8.12.9.11.7"></a>

## Return Value

The name of the specified relation's namespace.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getnspname.html)（英文原文，待翻譯）
