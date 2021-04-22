# CREATE USER

CREATE USER — 定義一個新的資料庫角色

## 語法

```text
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
    | [ ENCRYPTED ] PASSWORD 'password'
    | VALID UNTIL 'timestamp'
    | IN ROLE role_name [, ...]
    | IN GROUP role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | USER role_name [, ...]
    | SYSID uid
```

## 說明

`CREATE USER 現在是 CREATE ROLE 的別名指令。唯一的區別是當命令為 CREATE USER 時，預設情況下是具有 LOGIN 權限的，而當命令為 CREATE ROLE 時則預設為 NOLOGIN。`

## 相容性

CREATE USER 語句是 PostgreSQL 延伸功能。SQL 標準將使用者的定義留給各資料庫系統自行實作。

## 參閱

[CREATE ROLE](create-role.md)

