<a id="SPI-SPI-EXECUTE-WITH-ARGS"></a><a id="id-1.8.12.8.7.1"></a>

# SPI_execute_with_args

SPI_execute_with_args — execute a command with out-of-line parameters

## Synopsis

```

int SPI_execute_with_args(const char *command,
                          int nargs, Oid *argtypes,
                          Datum *values, const char *nulls,
                          bool read_only, long count)
```

<a id="id-1.8.12.8.7.5"></a>

## Description

`SPI_execute_with_args` executes a command that might include references to externally supplied parameters. The command text refers to a parameter as <code class="literal">$<em class="replaceable"><code>n</code></em></code>, and the call specifies data types and values for each such symbol. <em class="parameter"><code>read&#95;only</code></em> and <em class="parameter"><code>count</code></em> have the same interpretation as in `SPI_execute`.

The main advantage of this routine compared to `SPI_execute` is that data values can be inserted into the command without tedious quoting/escaping, and thus with much less risk of SQL-injection attacks.

Similar results can be achieved with `SPI_prepare` followed by `SPI_execute_plan`; however, when using this function the query plan is always customized to the specific parameter values provided. For one-time query execution, this function should be preferred. If the same command is to be executed with many different parameters, either method might be faster, depending on the cost of re-planning versus the benefit of custom plans.

<a id="id-1.8.12.8.7.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

command string

<code class="literal">int <em class="parameter"><code>nargs</code></em></code>

number of input parameters (`$1`, `$2`, etc.)

<code class="literal">Oid &#42; <em class="parameter"><code>argtypes</code></em></code>

an array of length <em class="parameter"><code>nargs</code></em>, containing the OIDs of the data types of the parameters

<code class="literal">Datum &#42; <em class="parameter"><code>values</code></em></code>

an array of length <em class="parameter"><code>nargs</code></em>, containing the actual parameter values

<code class="literal">const char &#42; <em class="parameter"><code>nulls</code></em></code>

an array of length <em class="parameter"><code>nargs</code></em>, describing which parameters are null

If <em class="parameter"><code>nulls</code></em> is `NULL` then `SPI_execute_with_args` assumes that no parameters are null. Otherwise, each entry of the <em class="parameter"><code>nulls</code></em> array should be `' '` if the corresponding parameter value is non-null, or `'n'` if the corresponding parameter value is null. (In the latter case, the actual value in the corresponding <em class="parameter"><code>values</code></em> entry doesn't matter.) Note that <em class="parameter"><code>nulls</code></em> is not a text string, just an array: it does not need a `'\0'` terminator.

<code class="literal">bool <em class="parameter"><code>read&#95;only</code></em></code>

`true` for read-only execution

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to return, or `0` for no limit

<a id="id-1.8.12.8.7.7"></a>

## Return Value

The return value is the same as for `SPI_execute`.

`SPI_processed` and `SPI_tuptable` are set as in `SPI_execute` if successful.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-execute-with-args.html)（英文原文，待翻譯）
