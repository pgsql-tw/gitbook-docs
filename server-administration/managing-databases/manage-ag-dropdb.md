## 22.5. Destroying a Database [#](#MANAGE-AG-DROPDB)

Databases are destroyed with the command
[DROP DATABASE](../../reference/sql-commands/sql-dropdatabase.md):<a id="id-1.6.9.8.2.2"></a>

```

DROP DATABASE name;
```

Only the owner of the database, or
a superuser, can drop a database. Dropping a database removes all objects
that were
contained within the database. The destruction of a database cannot
be undone.

You cannot execute the `DROP DATABASE` command
while connected to the victim database. You can, however, be
connected to any other database, including the `template1`
database.
`template1` would be the only option for dropping the last user database of a
given cluster.

For convenience, there is also a shell program to drop
databases, [dropdb](../../reference/reference-client/app-dropdb.md):<a id="id-1.6.9.8.4.2"></a>

```

dropdb dbname
```

(Unlike `createdb`, it is not the default action to drop
the database with the current user name.)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-dropdb.html)（英文原文，待翻譯）
