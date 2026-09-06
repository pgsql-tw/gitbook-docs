## 19.13. Version and Platform Compatibility [#](#RUNTIME-CONFIG-COMPATIBLE)

[19.13.1. Previous PostgreSQL Versions](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)

[19.13.2. Platform and Client Compatibility](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

<a id="RUNTIME-CONFIG-COMPATIBLE-VERSION"></a>

### 19.13.1. Previous PostgreSQL Versions [#](#RUNTIME-CONFIG-COMPATIBLE-VERSION)

<a id="GUC-ARRAY-NULLS"></a>

`array_nulls` (`boolean`) <a id="id-1.6.6.16.2.2.1.1.3"></a> [#](#GUC-ARRAY-NULLS)
:   This controls whether the array input parser recognizes
    unquoted `NULL` as specifying a null array element.
    By default, this is `on`, allowing array values containing
    null values to be entered. However, PostgreSQL versions
    before 8.2 did not support null values in arrays, and therefore would
    treat `NULL` as specifying a normal array element with
    the string value “NULL”. For backward compatibility with
    applications that require the old behavior, this variable can be
    turned `off`.

    Note that it is possible to create array values containing null values
    even when this variable is `off`.
<a id="GUC-BACKSLASH-QUOTE"></a>

`backslash_quote` (`enum`) <a id="id-1.6.6.16.2.2.2.1.3"></a> <a id="id-1.6.6.16.2.2.2.1.4"></a> [#](#GUC-BACKSLASH-QUOTE)
:   This controls whether a quote mark can be represented by
    `\'` in a string literal. The preferred, SQL-standard way
    to represent a quote mark is by doubling it (`''`) but
    PostgreSQL has historically also accepted
    `\'`. However, use of `\'` creates security risks
    because in some client character set encodings, there are multibyte
    characters in which the last byte is numerically equivalent to ASCII
    `\`. If client-side code does escaping incorrectly then an
    SQL-injection attack is possible. This risk can be prevented by
    making the server reject queries in which a quote mark appears to be
    escaped by a backslash.
    The allowed values of `backslash_quote` are
    `on` (allow `\'` always),
    `off` (reject always), and
    `safe_encoding` (allow only if client encoding does not
    allow ASCII `\` within a multibyte character).
    `safe_encoding` is the default setting.

    Note that in a standard-conforming string literal, `\` just
    means `\` anyway. This parameter only affects the handling of
    non-standard-conforming literals, including
    escape string syntax (`E'...'`).
<a id="GUC-ESCAPE-STRING-WARNING"></a>

`escape_string_warning` (`boolean`) <a id="id-1.6.6.16.2.2.3.1.3"></a> <a id="id-1.6.6.16.2.2.3.1.4"></a> [#](#GUC-ESCAPE-STRING-WARNING)
:   When on, a warning is issued if a backslash (`\`)
    appears in an ordinary string literal (`'...'`
    syntax) and `standard_conforming_strings` is off.
    The default is `on`.

    Applications that wish to use backslash as escape should be
    modified to use escape string syntax (`E'...'`),
    because the default behavior of ordinary strings is now to treat
    backslash as an ordinary character, per SQL standard. This variable
    can be enabled to help locate code that needs to be changed.
<a id="GUC-LO-COMPAT-PRIVILEGES"></a>

`lo_compat_privileges` (`boolean`) <a id="id-1.6.6.16.2.2.4.1.3"></a> [#](#GUC-LO-COMPAT-PRIVILEGES)
:   In PostgreSQL releases prior to 9.0, large objects
    did not have access privileges and were, therefore, always readable
    and writable by all users. Setting this variable to `on`
    disables the new privilege checks, for compatibility with prior
    releases. The default is `off`.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    Setting this variable does not disable all security checks related to
    large objects — only those for which the default behavior has
    changed in PostgreSQL 9.0.
<a id="GUC-QUOTE-ALL-IDENTIFIERS"></a>

`quote_all_identifiers` (`boolean`) <a id="id-1.6.6.16.2.2.5.1.3"></a> [#](#GUC-QUOTE-ALL-IDENTIFIERS)
:   When the database generates SQL, force all identifiers to be quoted,
    even if they are not (currently) keywords. This will affect the
    output of `EXPLAIN` as well as the results of functions
    like `pg_get_viewdef`. See also the
    `--quote-all-identifiers` option of
    [pg_dump](../../reference/reference-client/app-pgdump.md) and [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md).
<a id="GUC-STANDARD-CONFORMING-STRINGS"></a>

`standard_conforming_strings` (`boolean`) <a id="id-1.6.6.16.2.2.6.1.3"></a> <a id="id-1.6.6.16.2.2.6.1.4"></a> [#](#GUC-STANDARD-CONFORMING-STRINGS)
:   This controls whether ordinary string literals
    (`'...'`) treat backslashes literally, as specified in
    the SQL standard.
    Beginning in PostgreSQL 9.1, the default is
    `on` (prior releases defaulted to `off`).
    Applications can check this
    parameter to determine how string literals will be processed.
    The presence of this parameter can also be taken as an indication
    that the escape string syntax (`E'...'`) is supported.
    Escape string syntax ([Section 4.1.2.2](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE))
    should be used if an application desires
    backslashes to be treated as escape characters.
<a id="GUC-SYNCHRONIZE-SEQSCANS"></a>

`synchronize_seqscans` (`boolean`) <a id="id-1.6.6.16.2.2.7.1.3"></a> [#](#GUC-SYNCHRONIZE-SEQSCANS)
:   This allows sequential scans of large tables to synchronize with each
    other, so that concurrent scans read the same block at about the
    same time and hence share the I/O workload. When this is enabled,
    a scan might start in the middle of the table and then “wrap
    around” the end to cover all rows, so as to synchronize with the
    activity of scans already in progress. This can result in
    unpredictable changes in the row ordering returned by queries that
    have no `ORDER BY` clause. Setting this parameter to
    `off` ensures the pre-8.3 behavior in which a sequential
    scan always starts from the beginning of the table. The default
    is `on`.

<a id="RUNTIME-CONFIG-COMPATIBLE-CLIENTS"></a>

### 19.13.2. Platform and Client Compatibility [#](#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

<a id="GUC-TRANSFORM-NULL-EQUALS"></a>

`transform_null_equals` (`boolean`) <a id="id-1.6.6.16.3.2.1.1.3"></a> <a id="id-1.6.6.16.3.2.1.1.4"></a> [#](#GUC-TRANSFORM-NULL-EQUALS)
:   When on, expressions of the form `expr =
    NULL` (or `NULL =
    expr`) are treated as
    `expr IS NULL`, that is, they
    return true if *`expr`* evaluates to the null value,
    and false otherwise. The correct SQL-spec-compliant behavior of
    `expr = NULL` is to always
    return null (unknown). Therefore this parameter defaults to
    `off`.

    However, filtered forms in Microsoft
    Access generate queries that appear to use
    `expr = NULL` to test for
    null values, so if you use that interface to access the database you
    might want to turn this option on. Since expressions of the
    form `expr = NULL` always
    return the null value (using the SQL standard interpretation), they are not
    very useful and do not appear often in normal applications so
    this option does little harm in practice. But new users are
    frequently confused about the semantics of expressions
    involving null values, so this option is off by default.

    Note that this option only affects the exact form `= NULL`,
    not other comparison operators or other expressions
    that are computationally equivalent to some expression
    involving the equals operator (such as `IN`).
    Thus, this option is not a general fix for bad programming.

    Refer to [Section 9.2](../../the-sql-language/functions/functions-comparison.md) for related information.
<a id="GUC-ALLOW-ALTER-SYSTEM"></a>

`allow_alter_system` (`boolean`) <a id="id-1.6.6.16.3.2.2.1.3"></a> [#](#GUC-ALLOW-ALTER-SYSTEM)
:   When `allow_alter_system` is set to
    `off`, an error is returned if the `ALTER
    SYSTEM` command is executed. This parameter can only be set in
    the `postgresql.conf` file or on the server command
    line. The default value is `on`.

    Note that this setting must not be regarded as a security feature. It
    only disables the `ALTER SYSTEM` command. It does not
    prevent a superuser from changing the configuration using other SQL
    commands. A superuser has many ways of executing shell commands at
    the operating system level, and can therefore modify
    `postgresql.auto.conf` regardless of the value of
    this setting.

    Turning this setting off is intended for environments where the
    configuration of PostgreSQL is managed by
    some external tool.
    In such environments, a well-intentioned superuser might
    *mistakenly* use `ALTER SYSTEM`
    to change the configuration instead of using the external tool.
    This might result in unintended behavior, such as the external tool
    overwriting the change at some later point in time when it updates the
    configuration.
    Setting this parameter to `off` can
    help avoid such mistakes.

    This parameter only controls the use of `ALTER SYSTEM`.
    The settings stored in `postgresql.auto.conf`
    take effect even if `allow_alter_system` is set to
    `off`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-compatible.html)（英文原文，待翻譯）
