<a id="SPI-SPI-PREPARE-PARAMS"></a><a id="id-1.8.12.8.11.1"></a>

# SPI_prepare_params

SPI_prepare_params — prepare a statement, without executing it yet

## Synopsis

```

SPIPlanPtr SPI_prepare_params(const char * command,
                              ParserSetupHook parserSetup,
                              void * parserSetupArg,
                              int cursorOptions)
```

<a id="id-1.8.12.8.11.5"></a>

## Description

`SPI_prepare_params` creates and returns a prepared statement for the specified command, but doesn't execute the command. This function is equivalent to `SPI_prepare_cursor`, with the addition that the caller can specify parser hook functions to control the parsing of external parameter references.

This function is now deprecated in favor of `SPI_prepare_extended`.

<a id="id-1.8.12.8.11.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

command string

<code class="literal">ParserSetupHook <em class="parameter"><code>parserSetup</code></em></code>

Parser hook setup function

<code class="literal">void &#42; <em class="parameter"><code>parserSetupArg</code></em></code>

pass-through argument for <em class="parameter"><code>parserSetup</code></em>

<code class="literal">int <em class="parameter"><code>cursorOptions</code></em></code>

integer bit mask of cursor options; zero produces default behavior

<a id="id-1.8.12.8.11.7"></a>

## Return Value

`SPI_prepare_params` has the same return conventions as `SPI_prepare`.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-prepare-params.html)（英文原文，待翻譯）
