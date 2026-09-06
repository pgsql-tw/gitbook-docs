<a id="SQL-CREATEGROUP"></a><a id="id-1.9.3.68.1"></a>

# CREATE GROUP

CREATE GROUP — define a new database role

## Synopsis

```

CREATE GROUP name [ [ WITH ] option [ ... ] ]

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

<a id="id-1.9.3.68.5"></a>

## Description

`CREATE GROUP` is now an alias for [CREATE ROLE](create-role.md).

<a id="id-1.9.3.68.6"></a>

## Compatibility

There is no `CREATE GROUP` statement in the SQL standard.

<a id="id-1.9.3.68.7"></a>

## See Also

[CREATE ROLE](create-role.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-creategroup.html)（英文原文，待翻譯）
