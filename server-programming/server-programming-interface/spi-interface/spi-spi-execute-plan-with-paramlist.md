<a id="SPI-SPI-EXECUTE-PLAN-WITH-PARAMLIST"></a><a id="id-1.8.12.8.17.1"></a>

# SPI_execute_plan_with_paramlist

SPI_execute_plan_with_paramlist — execute a statement prepared by `SPI_prepare`

## Synopsis

```

int SPI_execute_plan_with_paramlist(SPIPlanPtr plan,
                                    ParamListInfo params,
                                    bool read_only,
                                    long count)
```

<a id="id-1.8.12.8.17.5"></a>

## Description

`SPI_execute_plan_with_paramlist` executes a statement prepared by `SPI_prepare`. This function is equivalent to `SPI_execute_plan` except that information about the parameter values to be passed to the query is presented differently. The `ParamListInfo` representation can be convenient for passing down values that are already available in that format. It also supports use of dynamic parameter sets via hook functions specified in `ParamListInfo`.

This function is now deprecated in favor of `SPI_execute_plan_extended`.

<a id="id-1.8.12.8.17.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<code class="literal">ParamListInfo <em class="parameter"><code>params</code></em></code>

data structure containing parameter types and values; NULL if none

<code class="literal">bool <em class="parameter"><code>read&#95;only</code></em></code>

`true` for read-only execution

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to return, or `0` for no limit

<a id="id-1.8.12.8.17.7"></a>

## Return Value

The return value is the same as for `SPI_execute_plan`.

`SPI_processed` and `SPI_tuptable` are set as in `SPI_execute_plan` if successful.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-execute-plan-with-paramlist.html)（英文原文，待翻譯）
