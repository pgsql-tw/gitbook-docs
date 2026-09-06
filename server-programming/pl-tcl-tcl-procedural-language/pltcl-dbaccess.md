<a id="PLTCL-DBACCESS"></a>

# 44.5. Database Access from PL/Tcl

In this section, we follow the usual Tcl convention of using question marks, rather than brackets, to indicate an optional element in a syntax synopsis. The following commands are available to access the database from the body of a PL/Tcl function:

<code class="literal"><code class="function">spi&#95;exec</code> ?<span class="optional">-count <em class="replaceable"><code>n</code></em></span>? ?<span class="optional">-array <em class="replaceable"><code>name</code></em></span>? <em class="replaceable"><code>command</code></em> ?<span class="optional"><em class="replaceable"><code>loop-body</code></em></span>?</code>

Executes an SQL command given as a string. An error in the command causes an error to be raised. Otherwise, the return value of `spi_exec` is the number of rows processed (selected, inserted, updated, or deleted) by the command, or zero if the command is a utility statement. In addition, if the command is a `SELECT` statement, the values of the selected columns are placed in Tcl variables as described below.

The optional `-count` value tells `spi_exec` to stop once <em class="replaceable"><code>n</code></em> rows have been retrieved, much as if the query included a `LIMIT` clause. If <em class="replaceable"><code>n</code></em> is zero, the query is run to completion, the same as when `-count` is omitted.

If the command is a `SELECT` statement, the values of the result columns are placed into Tcl variables named after the columns. If the `-array` option is given, the column values are instead stored into elements of the named associative array, with the column names used as array indexes. In addition, the current row number within the result (counting from zero) is stored into the array element named “`.tupno`”, unless that name is in use as a column name in the result.

If the command is a `SELECT` statement and no <em class="replaceable"><code>loop-body</code></em> script is given, then only the first row of results are stored into Tcl variables or array elements; remaining rows, if any, are ignored. No storing occurs if the query returns no rows. (This case can be detected by checking the result of `spi_exec`.) For example:

```

spi_exec "SELECT count(*) AS cnt FROM pg_proc"
```

will set the Tcl variable `$cnt` to the number of rows in the `pg_proc` system catalog.

If the optional <em class="replaceable"><code>loop-body</code></em> argument is given, it is a piece of Tcl script that is executed once for each row in the query result. (<em class="replaceable"><code>loop-body</code></em> is ignored if the given command is not a `SELECT`.) The values of the current row's columns are stored into Tcl variables or array elements before each iteration. For example:

```

spi_exec -array C "SELECT * FROM pg_class" {
    elog DEBUG "have table $C(relname)"
}
```

will print a log message for every row of `pg_class`. This feature works similarly to other Tcl looping constructs; in particular `continue` and `break` work in the usual way inside the loop body.

If a column of a query result is null, the target variable for it is “unset” rather than being set.

`spi_prepare` <em class="replaceable"><code>query</code></em> <em class="replaceable"><code>typelist</code></em>

Prepares and saves a query plan for later execution. The saved plan will be retained for the life of the current session.<a id="id-1.8.9.9.2.1.2.2.1.1"></a>

The query can use parameters, that is, placeholders for values to be supplied whenever the plan is actually executed. In the query string, refer to parameters by the symbols `$1` ... <code class="literal">$<em class="replaceable"><code>n</code></em></code>. If the query uses parameters, the names of the parameter types must be given as a Tcl list. (Write an empty list for <em class="replaceable"><code>typelist</code></em> if no parameters are used.)

The return value from `spi_prepare` is a query ID to be used in subsequent calls to `spi_execp`. See `spi_execp` for an example.

<code class="literal"><code class="function">spi&#95;execp</code> ?<span class="optional">-count <em class="replaceable"><code>n</code></em></span>? ?<span class="optional">-array <em class="replaceable"><code>name</code></em></span>? ?<span class="optional">-nulls <em class="replaceable"><code>string</code></em></span>? <em class="replaceable"><code>queryid</code></em> ?<span class="optional"><em class="replaceable"><code>value-list</code></em></span>? ?<span class="optional"><em class="replaceable"><code>loop-body</code></em></span>?</code>

Executes a query previously prepared with `spi_prepare`. <em class="replaceable"><code>queryid</code></em> is the ID returned by `spi_prepare`. If the query references parameters, a <em class="replaceable"><code>value-list</code></em> must be supplied. This is a Tcl list of actual values for the parameters. The list must be the same length as the parameter type list previously given to `spi_prepare`. Omit <em class="replaceable"><code>value-list</code></em> if the query has no parameters.

The optional value for `-nulls` is a string of spaces and `'n'` characters telling `spi_execp` which of the parameters are null values. If given, it must have exactly the same length as the <em class="replaceable"><code>value-list</code></em>. If it is not given, all the parameter values are nonnull.

Except for the way in which the query and its parameters are specified, `spi_execp` works just like `spi_exec`. The `-count`, `-array`, and <em class="replaceable"><code>loop-body</code></em> options are the same, and so is the result value.

Here's an example of a PL/Tcl function using a prepared plan:

```

CREATE FUNCTION t1_count(integer, integer) RETURNS integer AS $$
    if {![ info exists GD(plan) ]} {
        # prepare the saved plan on the first call
        set GD(plan) [ spi_prepare \
                "SELECT count(*) AS cnt FROM t1 WHERE num >= \$1 AND num <= \$2" \
                [ list int4 int4 ] ]
    }
    spi_execp -count 1 $GD(plan) [ list $1 $2 ]
    return $cnt
$$ LANGUAGE pltcl;
```

We need backslashes inside the query string given to `spi_prepare` to ensure that the <code class="literal">$<em class="replaceable"><code>n</code></em></code> markers will be passed through to `spi_prepare` as-is, and not replaced by Tcl variable substitution.

`subtransaction` <em class="replaceable"><code>command</code></em>

The Tcl script contained in <em class="replaceable"><code>command</code></em> is executed within an SQL subtransaction. If the script returns an error, that entire subtransaction is rolled back before returning the error out to the surrounding Tcl code. See [Section 44.9](pltcl-subtransactions.md) for more details and an example.

`quote` <em class="replaceable"><code>string</code></em>

Doubles all occurrences of single quote and backslash characters in the given string. This can be used to safely quote strings that are to be inserted into SQL commands given to `spi_exec` or `spi_prepare`. For example, think about an SQL command string like:

```

"SELECT '$val' AS ret"
```

where the Tcl variable `val` actually contains `doesn't`. This would result in the final command string:

```

SELECT 'doesn't' AS ret
```

which would cause a parse error during `spi_exec` or `spi_prepare`. To work properly, the submitted command should contain:

```

SELECT 'doesn''t' AS ret
```

which can be formed in PL/Tcl using:

```

"SELECT '[ quote $val ]' AS ret"
```

One advantage of `spi_execp` is that you don't have to quote parameter values like this, since the parameters are never parsed as part of an SQL command string.

`elog` <em class="replaceable"><code>level</code></em> <em class="replaceable"><code>msg</code></em> <a id="id-1.8.9.9.2.1.6.1.4"></a>

Emits a log or error message. Possible levels are `DEBUG`, `LOG`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, and `FATAL`. `ERROR` raises an error condition; if this is not trapped by the surrounding Tcl code, the error propagates out to the calling query, causing the current transaction or subtransaction to be aborted. This is effectively the same as the Tcl `error` command. `FATAL` aborts the transaction and causes the current session to shut down. (There is probably no good reason to use this error level in PL/Tcl functions, but it's provided for completeness.) The other levels only generate messages of different priority levels. Whether messages of a particular priority are reported to the client, written to the server log, or both is controlled by the [log_min_messages](../../server-administration/server-configuration/error-reporting-and-logging.md#GUC-LOG-MIN-MESSAGES) and [client_min_messages](../../server-administration/server-configuration/client-connection-defaults.md#GUC-CLIENT-MIN-MESSAGES) configuration variables. See [Chapter 20](../../server-administration/server-configuration/README.md) and [Section 44.8](pltcl-error-handling.md) for more information.

---

原文：[PostgreSQL 15.19 Documentation](pltcl-dbaccess.md)（英文原文，待翻譯）
