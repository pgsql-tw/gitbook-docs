## 22.2. Creating a Database [#](#MANAGE-AG-CREATEDB)

<a id="id-1.6.9.5.2"></a>

In order to create a database, the PostgreSQL
server must be up and running (see [Section 18.3](../runtime/server-start.md)).

Databases are created with the SQL command
[CREATE DATABASE](../../reference/sql-commands/sql-createdatabase.md):

```

CREATE DATABASE name;
```

where *`name`* follows the usual rules for
SQL identifiers. The current role automatically
becomes the owner of the new database. It is the privilege of the
owner of a database to remove it later (which also removes all
the objects in it, even if they have a different owner).

The creation of databases is a restricted operation. See [Section 21.2](../user-manag/role-attributes.md) for how to grant permission.

Since you need to be connected to the database server in order to
execute the `CREATE DATABASE` command, the
question remains how the *first* database at any given
site can be created. The first database is always created by the
`initdb` command when the data storage area is
initialized. (See [Section 18.2](../runtime/creating-cluster.md).) This
database is called
`postgres`.<a id="id-1.6.9.5.6.6"></a> So to
create the first “ordinary” database you can connect to
`postgres`.

Two additional databases,
`template1`<a id="id-1.6.9.5.7.2"></a>
and
`template0`,<a id="id-1.6.9.5.7.4"></a>
are also created during database cluster initialization. Whenever a
new database is created within the
cluster, `template1` is essentially cloned.
This means that any changes you make in `template1` are
propagated to all subsequently created databases. Because of this,
avoid creating objects in `template1` unless you want them
propagated to every newly created database.
`template0` is meant as a pristine copy of the original
contents of `template1`. It can be cloned instead
of `template1` when it is important to make a database
without any such site-local additions. More details
appear in [Section 22.3](manage-ag-templatedbs.md).

As a convenience, there is a program you can
execute from the shell to create new databases,
`createdb`.<a id="id-1.6.9.5.8.2"></a>

```

createdb dbname
```

`createdb` does no magic. It connects to the `postgres`
database and issues the `CREATE DATABASE` command,
exactly as described above.
The [createdb](../../reference/reference-client/app-createdb.md) reference page contains the invocation
details. Note that `createdb` without any arguments will create
a database with the current user name.

### Note

[Chapter 20](../client-authentication/README.md) contains information about
how to restrict who can connect to a given database.

Sometimes you want to create a database for someone else, and have them
become the owner of the new database, so they can
configure and manage it themselves. To achieve that, use one of the
following commands:

```

CREATE DATABASE dbname OWNER rolename;
```

from the SQL environment, or:

```

createdb -O rolename dbname
```

from the shell.
Only the superuser is allowed to create a database for
someone else (that is, for a role you are not a member of).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-createdb.html)（英文原文，待翻譯）
