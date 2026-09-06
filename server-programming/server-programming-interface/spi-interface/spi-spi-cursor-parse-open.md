<a id="SPI-SPI-CURSOR-PARSE-OPEN"></a><a id="id-1.8.12.8.22.1"></a>

# SPI_cursor_parse_open

SPI_cursor_parse_open — set up a cursor using a query string and parameters

## Synopsis

```

Portal SPI_cursor_parse_open(const char *name,
                             const char *command,
                             const SPIParseOpenOptions * options)
```

<a id="id-1.8.12.8.22.5"></a>

## Description

`SPI_cursor_parse_open` sets up a cursor (internally, a portal) that will execute the specified query string. This is comparable to `SPI_prepare_cursor` followed by `SPI_cursor_open_with_paramlist`, except that parameter references within the query string are handled entirely by supplying a `ParamListInfo` object.

For one-time query execution, this function should be preferred over `SPI_prepare_cursor` followed by `SPI_cursor_open_with_paramlist`. If the same command is to be executed with many different parameters, either method might be faster, depending on the cost of re-planning versus the benefit of custom plans.

The <em class="parameter"><code>options-&gt;params</code></em> object should normally mark each parameter with the `PARAM_FLAG_CONST` flag, since a one-shot plan is always used for the query.

The passed-in parameter data will be copied into the cursor's portal, so it can be freed while the cursor still exists.

<a id="id-1.8.12.8.22.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>name</code></em></code>

name for portal, or `NULL` to let the system select a name

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

command string

<code class="literal">const SPIParseOpenOptions &#42; <em class="parameter"><code>options</code></em></code>

struct containing optional arguments

Callers should always zero out the entire <em class="parameter"><code>options</code></em> struct, then fill whichever fields they want to set. This ensures forward compatibility of code, since any fields that are added to the struct in future will be defined to behave backwards-compatibly if they are zero. The currently available <em class="parameter"><code>options</code></em> fields are:

<code class="literal">ParamListInfo <em class="parameter"><code>params</code></em></code>

data structure containing query parameter types and values; NULL if none

<code class="literal">int <em class="parameter"><code>cursorOptions</code></em></code>

integer bit mask of cursor options; zero produces default behavior

<code class="literal">bool <em class="parameter"><code>read&#95;only</code></em></code>

`true` for read-only execution

<a id="id-1.8.12.8.22.7"></a>

## Return Value

Pointer to portal containing the cursor. Note there is no error return convention; any error will be reported via `elog`.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-cursor-parse-open.html)（英文原文，待翻譯）
