<a id="SQL-ALTERUSER"></a><a id="id-1.9.3.43.1"></a>

## ALTER USER

ALTER USER — 變更資料庫角色

<a id="id-1.9.3.43.4"></a>

## 語法

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

## 說明

`ALTER USER` 現在是
[`ALTER ROLE`](sql-alterrole.md) 的別名。

<a id="id-1.9.3.43.6"></a>

## 相容性

`ALTER USER` 陳述式是
PostgreSQL 的擴充語法。SQL 標準將使用者的定義交由各實作決定。

<a id="id-1.9.3.43.7"></a>

## 另請參閱

[ALTER ROLE](sql-alterrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteruser.html)（原文版本：18.6；核對日期：2026-10-04）
