<a id="id-1.9.3.95.1"></a>

## CREATE USER

CREATE USER — 定義新的資料庫角色

## 語法

```

CREATE USER name [ [ WITH ] option [ ... ] ]

其中 option 可以是：

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

## 說明

`CREATE USER` 現在是 [`CREATE ROLE`](sql-createrole.md) 的別名。唯一差異是命令寫為 `CREATE USER` 時預設採用 `LOGIN`；寫為 `CREATE ROLE` 時預設採用 `NOLOGIN`。

<a id="id-1.9.3.95.6"></a>

## 相容性

`CREATE USER` 陳述式是 PostgreSQL 擴充功能。SQL 標準將使用者的定義交由實作決定。

<a id="id-1.9.3.95.7"></a>

## 另請參閱

[CREATE ROLE](sql-createrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createuser.html)（原文版本：18.6；核對日期：2026-09-10）
