# 19.13. 版本與平台的相容性[^1]

[19.13.1. Previous PostgreSQL Versions](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#runtime-config-compatible-version)

[19.13.2. Platform and Client Compatibility](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#runtime-config-compatible-clients)

### 19.13.1. Previous PostgreSQL Versions

`array_nulls`

\(

`boolean`

\)



This controls whether the array input parser recognizes unquoted`NULL`as specifying a null array element. By default, this is`on`, allowing array values containing null values to be entered. However,PostgreSQLversions before 8.2 did not support null values in arrays, and therefore would treat`NULL`as specifying a normal array element with the string value“NULL”. For backward compatibility with applications that require the old behavior, this variable can be turned`off`.

Note that it is possible to create array values containing null values even when this variable is`off`.

`backslash_quote`

\(

`enum`

\)





This controls whether a quote mark can be represented by`\'`in a string literal. The preferred, SQL-standard way to represent a quote mark is by doubling it \(`''`\) butPostgreSQLhas historically also accepted`\'`. However, use of`\'`creates security risks because in some client character set encodings, there are multibyte characters in which the last byte is numerically equivalent to ASCII`\`. If client-side code does escaping incorrectly then a SQL-injection attack is possible. This risk can be prevented by making the server reject queries in which a quote mark appears to be escaped by a backslash. The allowed values of`backslash_quote`are`on`\(allow`\'`always\),`off`\(reject always\), and`safe_encoding`\(allow only if client encoding does not allow ASCII`\`within a multibyte character\).`safe_encoding`is the default setting.

Note that in a standard-conforming string literal,`\`just means`\`anyway. This parameter only affects the handling of non-standard-conforming literals, including escape string syntax \(`E'...'`\).

`default_with_oids`

\(

`boolean`

\)



This controls whether`CREATE TABLE`and`CREATE TABLE AS`include an OID column in newly-created tables, if neither`WITH OIDS`nor`WITHOUT OIDS`is specified. It also determines whether OIDs will be included in tables created by`SELECT INTO`. The parameter is`off`by default; inPostgreSQL8.0 and earlier, it was`on`by default.

The use of OIDs in user tables is considered deprecated, so most installations should leave this variable disabled. Applications that require OIDs for a particular table should specify`WITH OIDS`when creating the table. This variable can be enabled for compatibility with old applications that do not follow this behavior.

`escape_string_warning`

\(

`boolean`

\)





When on, a warning is issued if a backslash \(`\`\) appears in an ordinary string literal \(`'...'`syntax\) and`standard_conforming_strings`is off. The default is`on`.

Applications that wish to use backslash as escape should be modified to use escape string syntax \(`E'...'`\), because the default behavior of ordinary strings is now to treat backslash as an ordinary character, per SQL standard. This variable can be enabled to help locate code that needs to be changed.

`lo_compat_privileges`

\(

`boolean`

\)



InPostgreSQLreleases prior to 9.0, large objects did not have access privileges and were, therefore, always readable and writable by all users. Setting this variable to`on`disables the new privilege checks, for compatibility with prior releases. The default is`off`. Only superusers can change this setting.

Setting this variable does not disable all security checks related to large objects — only those for which the default behavior has changed inPostgreSQL9.0. For example,`lo_import()`and`lo_export()`need superuser privileges regardless of this setting.

`operator_precedence_warning`

\(

`boolean`

\)



When on, the parser will emit a warning for any construct that might have changed meanings sincePostgreSQL9.4 as a result of changes in operator precedence. This is useful for auditing applications to see if precedence changes have broken anything; but it is not meant to be kept turned on in production, since it will warn about some perfectly valid, standard-compliant SQL code. The default is`off`.

See[Section 4.1.6](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-precedence)for more information.

`quote_all_identifiers`

\(

`boolean`

\)



When the database generates SQL, force all identifiers to be quoted, even if they are not \(currently\) keywords. This will affect the output of`EXPLAIN`as well as the results of functions like`pg_get_viewdef`. See also the`--quote-all-identifiers`option of[pg\_dump](https://www.postgresql.org/docs/10/static/app-pgdump.html)and[pg\_dumpall](https://www.postgresql.org/docs/10/static/app-pg-dumpall.html).

`standard_conforming_strings`

\(

`boolean`

\)





This controls whether ordinary string literals \(`'...'`\) treat backslashes literally, as specified in the SQL standard. Beginning inPostgreSQL9.1, the default is`on`\(prior releases defaulted to`off`\). Applications can check this parameter to determine how string literals will be processed. The presence of this parameter can also be taken as an indication that the escape string syntax \(`E'...'`\) is supported. Escape string syntax \([Section 4.1.2.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-strings-escape)\) should be used if an application desires backslashes to be treated as escape characters.

`synchronize_seqscans`

\(

`boolean`

\)



This allows sequential scans of large tables to synchronize with each other, so that concurrent scans read the same block at about the same time and hence share the I/O workload. When this is enabled, a scan might start in the middle of the table and then“wrap around”the end to cover all rows, so as to synchronize with the activity of scans already in progress. This can result in unpredictable changes in the row ordering returned by queries that have no`ORDER BY`clause. Setting this parameter to`off`ensures the pre-8.3 behavior in which a sequential scan always starts from the beginning of the table. The default is`on`.

### 19.13.2. Platform and Client Compatibility

`transform_null_equals`

\(

`boolean`

\)





When on, expressions of the form_`expr`_= NULL\(or`NULL =`_`expr`_\) are treated as_`expr`_IS NULL, that is, they return true if_`expr`_evaluates to the null value, and false otherwise. The correct SQL-spec-compliant behavior of_`expr`_= NULLis to always return null \(unknown\). Therefore this parameter defaults to`off`.

However, filtered forms inMicrosoft Accessgenerate queries that appear to use_`expr`_= NULLto test for null values, so if you use that interface to access the database you might want to turn this option on. Since expressions of the form_`expr`_= NULLalways return the null value \(using the SQL standard interpretation\), they are not very useful and do not appear often in normal applications so this option does little harm in practice. But new users are frequently confused about the semantics of expressions involving null values, so this option is off by default.

Note that this option only affects the exact form`= NULL`, not other comparison operators or other expressions that are computationally equivalent to some expression involving the equals operator \(such as`IN`\). Thus, this option is not a general fix for bad programming.

Refer to[Section 9.2](https://www.postgresql.org/docs/10/static/functions-comparison.html)for related information.

---



[^1]:  [PostgreSQL: Documentation: 10: 19.13. Version and Platform Compatibility](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html)

