---
description: 版本：10
---

# 51.15 pg\_database

目錄 pg\_database 儲存有關資料庫一些可用的訊息。資料庫是使用 [CREATE DATABASE](../../reference/sql-commands/create-database.md) 命令建立的。關於某些參數的含義的詳細訊息，請參閱[第 22 章](../../server-administration/managing-databases/)。

Unlike most system catalogs, `pg_database` is shared across all databases of a cluster: there is only one copy of `pg_database` per cluster, not one per database.

**Table 51.15. `pg_database` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `datname` | `name` |   | Database name |
| `datdba` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the database, usually the user who created it |
| `encoding` | `int4` |   | Character encoding for this database \(`pg_encoding_to_char()` can translate this number to the encoding name\) |
| `datcollate` | `name` |   | LC\_COLLATE for this database |
| `datctype` | `name` |   | LC\_CTYPE for this database |
| `datistemplate` | `bool` |   | If true, then this database can be cloned by any user with `CREATEDB` privileges; if false, then only superusers or the owner of the database can clone it. |
| `datallowconn` | `bool` |   | If false then no one can connect to this database. This is used to protect the `template0` database from being altered. |
| `datconnlimit` | `int4` |   | Sets maximum number of concurrent connections that can be made to this database. -1 means no limit. |
| `datlastsysoid` | `oid` |   | Last system OID in the database; useful particularly to pg\_dump |
| `datfrozenxid` | `xid` |   | All transaction IDs before this one have been replaced with a permanent \(“frozen”\) transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent transaction ID wraparound or to allow `pg_xact` to be shrunk. It is the minimum of the per-table `pg_class`.`relfrozenxid` values. |
| `datminmxid` | `xid` |   | All multixact IDs before this one have been replaced with a transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent multixact ID wraparound or to allow `pg_multixact` to be shrunk. It is the minimum of the per-table `pg_class`.`relminmxid` values. |
| `dattablespace` | `oid` | [`pg_tablespace`](https://www.postgresql.org/docs/10/static/catalog-pg-tablespace.html).oid | The default tablespace for the database. Within this database, all tables for which `pg_class`.`reltablespace` is zero will be stored in this tablespace; in particular, all the non-shared system catalogs will be there. |
| `datacl` | `aclitem[]` |   | Access privileges; see [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html) for details |

