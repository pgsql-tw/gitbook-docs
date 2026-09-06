<a id="id-1.9.3.154.1"></a>

## LOAD

LOAD — load a shared library file

## Synopsis

```

LOAD 'filename'
```

<a id="SQL-LOAD-DESCRIPTION"></a>

## Description

This command loads a shared library file into the PostgreSQL
server's address space. If the file has been loaded already,
the command does nothing. Shared library files that contain C functions
are automatically loaded whenever one of their functions is called.
Therefore, an explicit `LOAD` is usually only needed to
load a library that modifies the server's behavior through “hooks”
rather than providing a set of functions.

The library file name is typically given as just a bare file name,
which is sought in the server's library search path (set
by [dynamic_library_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH)). Alternatively it can be
given as a full path name. In either case the platform's standard shared
library file name extension may be omitted.
See [Section 36.10.1](../../server-programming/extend/xfunc-c.md#XFUNC-C-DYNLOAD) for more information on this topic.

<a id="id-1.9.3.154.5.4"></a>

Non-superusers can only apply `LOAD` to library files
located in `$libdir/plugins/` — the specified
*`filename`* must begin
with exactly that string. (It is the database administrator's
responsibility to ensure that only “safe” libraries
are installed there.)

<a id="SQL-LOAD-COMPAT"></a>

## Compatibility

`LOAD` is a PostgreSQL
extension.

<a id="id-1.9.3.154.7"></a>

## See Also

[CREATE FUNCTION](sql-createfunction.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-load.html)（英文原文，待翻譯）
