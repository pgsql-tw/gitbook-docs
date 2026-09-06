<a id="id-1.9.3.43.1"></a>

## ALTER USER

ALTER USER — change a database role

## Synopsis

```

ALTER USER role_specification [ WITH ] option [ ... ]

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

ALTER USER name RENAME TO new_name

ALTER USER { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter { TO | = } { value | DEFAULT }
ALTER USER { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter FROM CURRENT
ALTER USER { role_specification | ALL } [ IN DATABASE database_name ] RESET configuration_parameter
ALTER USER { role_specification | ALL } [ IN DATABASE database_name ] RESET ALL

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

<a id="id-1.9.3.43.5"></a>

## Description

`ALTER USER` is now an alias for
[`ALTER ROLE`](sql-alterrole.md).

<a id="id-1.9.3.43.6"></a>

## Compatibility

The `ALTER USER` statement is a
PostgreSQL extension. The SQL standard
leaves the definition of users to the implementation.

<a id="id-1.9.3.43.7"></a>

## See Also

[ALTER ROLE](sql-alterrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteruser.html)（英文原文，待翻譯）
