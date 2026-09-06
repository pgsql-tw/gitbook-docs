## VAR

VAR — define a variable

## Synopsis

```

VAR varname IS ctype
```

<a id="id-1.7.5.20.18.3"></a>

## Description

The `VAR` command assigns a new C data type
to a host variable. The host variable must be previously
declared in a declare section.

<a id="id-1.7.5.20.18.4"></a>

## Parameters

<a id="ECPG-SQL-VAR-VARNAME"></a>

*`varname`* [#](#ECPG-SQL-VAR-VARNAME)
:   A C variable name.
<a id="ECPG-SQL-VAR-CTYPE"></a>

*`ctype`* [#](#ECPG-SQL-VAR-CTYPE)
:   A C type specification.

<a id="id-1.7.5.20.18.5"></a>

## Examples

```

Exec sql begin declare section;
short a;
exec sql end declare section;
EXEC SQL VAR a IS int;
```

<a id="id-1.7.5.20.18.6"></a>

## Compatibility

The `VAR` command is a PostgreSQL extension.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-var.html)（英文原文，待翻譯）
