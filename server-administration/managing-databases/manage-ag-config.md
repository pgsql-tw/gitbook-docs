## 22.4. Database Configuration [#](#MANAGE-AG-CONFIG)

Recall from [Chapter 19](../runtime-config/README.md) that the
PostgreSQL server provides a large number of
run-time configuration variables. You can set database-specific
default values for many of these settings.

For example, if for some reason you want to disable the
GEQO optimizer for a given database, you'd
ordinarily have to either disable it for all databases or make sure
that every connecting client is careful to issue `SET geqo
TO off`. To make this setting the default within a particular
database, you can execute the command:

```

ALTER DATABASE mydb SET geqo TO off;
```

This will save the setting (but not set it immediately). In
subsequent connections to this database it will appear as though
`SET geqo TO off;` had been executed just before the
session started.
Note that users can still alter this setting during their sessions; it
will only be the default. To undo any such setting, use
`ALTER DATABASE dbname RESET
varname`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-config.html)（英文原文，待翻譯）
