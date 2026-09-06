<a id="SPI-SPI-CURSOR-FIND"></a><a id="id-1.8.12.8.23.1"></a>

# SPI_cursor_find

SPI_cursor_find — find an existing cursor by name

## Synopsis

```

Portal SPI_cursor_find(const char * name)
```

<a id="id-1.8.12.8.23.5"></a>

## Description

`SPI_cursor_find` finds an existing portal by name. This is primarily useful to resolve a cursor name returned as text by some other function.

<a id="id-1.8.12.8.23.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>name</code></em></code>

name of the portal

<a id="id-1.8.12.8.23.7"></a>

## Return Value

pointer to the portal with the specified name, or `NULL` if none was found

<a id="id-1.8.12.8.23.8"></a>

## Notes

Beware that this function can return a `Portal` object that does not have cursor-like properties; for example it might not return tuples. If you simply pass the `Portal` pointer to other SPI functions, they can defend themselves against such cases, but caution is appropriate when directly inspecting the `Portal`.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-cursor-find.md)（英文原文，待翻譯）
