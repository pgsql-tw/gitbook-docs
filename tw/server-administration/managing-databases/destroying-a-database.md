# 22.5. Destroying a Database

Databases are destroyed with the command [DROP DATABASE](https://www.postgresql.org/docs/13/sql-dropdatabase.html):

```
DROP DATABASE name;
```

Only the owner of the database, or a superuser, can drop a database. Dropping a database removes all objects that were contained within the database. The destruction of a database cannot be undone.

You cannot execute the `DROP DATABASE` command while connected to the victim database. You can, however, be connected to any other database, including the `template1` database. `template1` would be the only option for dropping the last user database of a given cluster.

For convenience, there is also a shell program to drop databases, [dropdb](https://www.postgresql.org/docs/13/app-dropdb.html):

```
dropdb dbname
```

(Unlike `createdb`, it is not the default action to drop the database with the current user name.)\
