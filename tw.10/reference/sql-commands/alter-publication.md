---
description: 版本：10
---

# ALTER PUBLICATION

ALTER PUBLICATION — change the definition of a publication

### Synopsis

```text
ALTER PUBLICATION name ADD TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name SET TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name DROP TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name SET ( publication_parameter [= value] [, ... ] )
ALTER PUBLICATION name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER PUBLICATION name RENAME TO new_name
```

### Description

The command `ALTER PUBLICATION` can change the attributes of a publication.

The first three variants change which tables are part of the publication. The `SET TABLE` clause will replace the list of tables in the publication with the specified one. The `ADD TABLE` and `DROP TABLE` clauses will add and remove one or more tables from the publication. Note that adding tables to a publication that is already subscribed to will require a `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` action on the subscribing side in order to become effective.

The fourth variant of this command listed in the synopsis can change all of the publication properties specified in [CREATE PUBLICATION](https://www.postgresql.org/docs/10/static/sql-createpublication.html). Properties not mentioned in the command retain their previous settings.

The remaining variants change the owner and the name of the publication.

You must own the publication to use `ALTER PUBLICATION`. To alter the owner, you must also be a direct or indirect member of the new owning role. The new owner must have `CREATE` privilege on the database. Also, the new owner of a `FOR ALL TABLES` publication must be a superuser. However, a superuser can change the ownership of a publication while circumventing these restrictions.

### Parameters

_`name`_

The name of an existing publication whose definition is to be altered._`table_name`_

Name of an existing table. If `ONLY` is specified before the table name, only that table is affected. If `ONLY` is not specified, the table and all its descendant tables \(if any\) are affected. Optionally, `*` can be specified after the table name to explicitly indicate that descendant tables are included.`SET (` _`publication_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause alters publication parameters originally set by [CREATE PUBLICATION](https://www.postgresql.org/docs/10/static/sql-createpublication.html). See there for more information._`new_owner`_

The user name of the new owner of the publication._`new_name`_

The new name for the publication.

### Examples

Change the publication to publish only deletes and updates:

```text
ALTER PUBLICATION noinsert SET (publish = 'update, delete');
```

Add some tables to the publication:

```text
ALTER PUBLICATION mypublication ADD TABLE users, departments;
```

### Compatibility

`ALTER PUBLICATION` is a PostgreSQL extension.

### See Also

[CREATE PUBLICATION](https://www.postgresql.org/docs/10/static/sql-createpublication.html), [DROP PUBLICATION](https://www.postgresql.org/docs/10/static/sql-droppublication.html), [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html), [ALTER SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-altersubscription.html)

