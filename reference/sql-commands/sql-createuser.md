<a id="id-1.9.3.95.1"></a>

## CREATE USER

CREATE USER — define a new database role

## Synopsis

```

CREATE USER name [ [ WITH ] option [ ... ] ]

where option can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ ENCRYPTED ] PASSWORD 'password' | PASSWORD NULL
    | VALID UNTIL 'timestamp'
    | IN ROLE role_name [, ...]
    | IN GROUP role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | USER role_name [, ...]
    | SYSID uid
```

<a id="id-1.9.3.95.5"></a>

## Description

`CREATE USER` is now an alias for
[`CREATE ROLE`](sql-createrole.md).
The only difference is that when the command is spelled
`CREATE USER`, `LOGIN` is assumed
by default, whereas `NOLOGIN` is assumed when
the command is spelled
`CREATE ROLE`.

<a id="id-1.9.3.95.6"></a>

## Compatibility

The `CREATE USER` statement is a
PostgreSQL extension. The SQL standard
leaves the definition of users to the implementation.

<a id="id-1.9.3.95.7"></a>

## See Also

[CREATE ROLE](sql-createrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createuser.html)（英文原文，待翻譯）
