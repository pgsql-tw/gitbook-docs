<a id="SPI-SPI-UNREGISTER-RELATION"></a><a id="id-1.8.12.8.32.1"></a><a id="id-1.8.12.8.32.2"></a>

# SPI_unregister_relation

SPI_unregister_relation — remove an ephemeral named relation from the registry

## Synopsis

```

int SPI_unregister_relation(const char * name)
```

<a id="id-1.8.12.8.32.6"></a>

## Description

`SPI_unregister_relation` removes an ephemeral named relation from the registry for the current connection.

<a id="id-1.8.12.8.32.7"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>name</code></em></code>

the relation registry entry name

<a id="id-1.8.12.8.32.8"></a>

## Return Value

If the execution of the command was successful then the following (nonnegative) value will be returned:

`SPI_OK_REL_UNREGISTER`

if the tuplestore has been successfully removed from the registry

On error, one of the following negative values is returned:

`SPI_ERROR_ARGUMENT`

if <em class="parameter"><code>name</code></em> is `NULL`

`SPI_ERROR_UNCONNECTED`

if called from an unconnected C function

`SPI_ERROR_REL_NOT_FOUND`

if <em class="parameter"><code>name</code></em> is not found in the registry for the current connection

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-unregister-relation.html)（英文原文，待翻譯）
