# 52.29. pg\_language

The catalog `pg_language` registers languages in which you can write functions or stored procedures. See [CREATE LANGUAGE](https://www.postgresql.org/docs/10/static/sql-createlanguage.html) and [Chapter 41](https://www.postgresql.org/docs/10/static/xplang.html) for more information about language handlers.

**Table 51.29. `pg_language` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `lanname` | `name` |   | Name of the language |
| `lanowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the language |
| `lanispl` | `bool` |   | This is false for internal languages \(such as SQL\) and true for user-defined languages. Currently, pg\_dump still uses this to determine which languages need to be dumped, but this might be replaced by a different mechanism in the future. |
| `lanpltrusted` | `bool` |   | True if this is a trusted language, which means that it is believed not to grant access to anything outside the normal SQL execution environment. Only superusers can create functions in untrusted languages. |
| `lanplcallfoid` | `oid` | [`pg_proc`](https://www.postgresql.org/docs/10/static/catalog-pg-proc.html).oid | For noninternal languages this references the language handler, which is a special function that is responsible for executing all functions that are written in the particular language |
| `laninline` | `oid` | [`pg_proc`](https://www.postgresql.org/docs/10/static/catalog-pg-proc.html).oid | This references a function that is responsible for executing “inline” anonymous code blocks \([DO](https://www.postgresql.org/docs/10/static/sql-do.html) blocks\). Zero if inline blocks are not supported. |
| `lanvalidator` | `oid` | [`pg_proc`](https://www.postgresql.org/docs/10/static/catalog-pg-proc.html).oid | This references a language validator function that is responsible for checking the syntax and validity of new functions when they are created. Zero if no validator is provided. |
| `lanacl` | `aclitem[]` |   | Access privileges; see [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html) for details |

