<a id="id-1.8.12.8.31.1"></a><a id="id-1.8.12.8.31.2"></a>

## SPI_register_relation

SPI_register_relation — make an ephemeral named relation available by name in SPI queries

## Synopsis

```

int SPI_register_relation(EphemeralNamedRelation enr)
```

<a id="id-1.8.12.8.31.6"></a>

## Description

`SPI_register_relation` makes an ephemeral named
relation, with associated information, available to queries planned and
executed through the current SPI connection.

<a id="id-1.8.12.8.31.7"></a>

## Arguments

`EphemeralNamedRelation enr`
:   the ephemeral named relation registry entry

<a id="id-1.8.12.8.31.8"></a>

## Return Value

If the execution of the command was successful then the following
(nonnegative) value will be returned:

`SPI_OK_REL_REGISTER`
:   if the relation has been successfully registered by name

On error, one of the following negative values is returned:

`SPI_ERROR_ARGUMENT`
:   if *`enr`* is `NULL` or its
    `name` field is `NULL`

`SPI_ERROR_UNCONNECTED`
:   if called from an unconnected C function

`SPI_ERROR_REL_DUPLICATE`
:   if the name specified in the `name` field of
    *`enr`* is already registered for this connection

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-register-relation.html)（英文原文，待翻譯）
