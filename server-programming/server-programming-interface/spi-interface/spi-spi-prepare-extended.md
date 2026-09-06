<a id="SPI-SPI-PREPARE-EXTENDED"></a><a id="id-1.8.12.8.10.1"></a>

# SPI_prepare_extended

SPI_prepare_extended — prepare a statement, without executing it yet

## Synopsis

```

SPIPlanPtr SPI_prepare_extended(const char * command,
                                const SPIPrepareOptions * options)
```

<a id="id-1.8.12.8.10.5"></a>

## Description

`SPI_prepare_extended` creates and returns a prepared statement for the specified command, but doesn't execute the command. This function is equivalent to `SPI_prepare`, with the addition that the caller can specify options to control the parsing of external parameter references, as well as other facets of query parsing and planning.

<a id="id-1.8.12.8.10.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

command string

<code class="literal">const SPIPrepareOptions &#42; <em class="parameter"><code>options</code></em></code>

struct containing optional arguments

Callers should always zero out the entire <em class="parameter"><code>options</code></em> struct, then fill whichever fields they want to set. This ensures forward compatibility of code, since any fields that are added to the struct in future will be defined to behave backwards-compatibly if they are zero. The currently available <em class="parameter"><code>options</code></em> fields are:

<code class="literal">ParserSetupHook <em class="parameter"><code>parserSetup</code></em></code>

Parser hook setup function

<code class="literal">void &#42; <em class="parameter"><code>parserSetupArg</code></em></code>

pass-through argument for <em class="parameter"><code>parserSetup</code></em>

<code class="literal">RawParseMode <em class="parameter"><code>parseMode</code></em></code>

mode for raw parsing; `RAW_PARSE_DEFAULT` (zero) produces default behavior

<code class="literal">int <em class="parameter"><code>cursorOptions</code></em></code>

integer bit mask of cursor options; zero produces default behavior

<a id="id-1.8.12.8.10.7"></a>

## Return Value

`SPI_prepare_extended` has the same return conventions as `SPI_prepare`.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-prepare-extended.md)（英文原文，待翻譯）
