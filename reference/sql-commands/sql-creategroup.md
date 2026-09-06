<a id="id-1.9.3.68.1"></a>

## CREATE GROUP

CREATE GROUP — 定義新的資料庫角色

## 語法

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

## 說明

`CREATE GROUP` 現在是 [CREATE ROLE](sql-createrole.md) 的別名。

<a id="id-1.9.3.68.6"></a>

## 相容性

SQL 標準中沒有 `CREATE GROUP` 陳述式。

<a id="id-1.9.3.68.7"></a>

## 另請參閱

[CREATE ROLE](sql-createrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-creategroup.html)（原文版本：18.6；核對日期：2026-09-07）
