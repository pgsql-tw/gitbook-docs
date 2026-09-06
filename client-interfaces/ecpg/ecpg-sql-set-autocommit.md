## SET AUTOCOMMIT

SET AUTOCOMMIT — set the autocommit behavior of the current session

## Synopsis

```

SET AUTOCOMMIT { = | TO } { ON | OFF }
```

<a id="id-1.7.5.20.14.3"></a>

## Description

`SET AUTOCOMMIT` sets the autocommit behavior of
the current database session. By default, embedded SQL programs
are *not* in autocommit mode,
so `COMMIT` needs to be issued explicitly when
desired. This command can change the session to autocommit mode,
where each individual statement is committed implicitly.

<a id="id-1.7.5.20.14.4"></a>

## Compatibility

`SET AUTOCOMMIT` is an extension of PostgreSQL ECPG.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-set-autocommit.html)（英文原文，待翻譯）
