# 22.6. Tablespaces

PostgreSQL 中的資料表空間允許資料庫管理者定義檔案系統中可以儲存資料庫物件的檔案的路徑。建立完成後，在建立資料庫物件時可以透過名稱來引用資料表空間。

通過使用資料表空間，管理者可以控制 PostgreSQL 安裝的磁碟規畫。至少在兩個方面是很有用的。首先，如果初始化叢集的分割區\(partition\)或磁碟區\(volume\)的空間不足並且無法擴展時，則可以在不同的分割區上建立資料表空間，資料庫系統重新配置即可使用。

其次，資料表空間允許管理者依資料庫物件特性的知識來優化效能。例如，使用率很高的索引可以放置在非常快速、高可用的磁碟上，例如昂貴的固態磁碟。另一方面，對於很少使用或不關鍵的歸檔資料的資料表可以儲存在較便宜、速度較慢的磁碟系統上。

## Warning

Even though located outside the main PostgreSQL data directory, tablespaces are an integral part of the database cluster and\_cannot\_be treated as an autonomous collection of data files. They are dependent on metadata contained in the main data directory, and therefore cannot be attached to a different database cluster or backed up individually. Similarly, if you lose a tablespace \(file deletion, disk failure, etc\), the database cluster might become unreadable or unable to start. Placing a tablespace on a temporary file system like a RAM disk risks the reliability of the entire cluster.

To define a tablespace, use the[CREATE TABLESPACE](https://www.postgresql.org/docs/10/static/sql-createtablespace.html)command, for example::

```text
CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
```

The location must be an existing, empty directory that is owned by thePostgreSQLoperating system user. All objects subsequently created within the tablespace will be stored in files underneath this directory. The location must not be on removable or transient storage, as the cluster might fail to function if the tablespace is missing or lost.

## Note

There is usually not much point in making more than one tablespace per logical file system, since you cannot control the location of individual files within a logical file system. However,PostgreSQLdoes not enforce any such limitation, and indeed it is not directly aware of the file system boundaries on your system. It just stores files in the directories you tell it to use.

Creation of the tablespace itself must be done as a database superuser, but after that you can allow ordinary database users to use it. To do that, grant them the`CREATE`privilege on it.

Tables, indexes, and entire databases can be assigned to particular tablespaces. To do so, a user with the`CREATE`privilege on a given tablespace must pass the tablespace name as a parameter to the relevant command. For example, the following creates a table in the tablespace`space1`:

```text
CREATE TABLE foo(i int) TABLESPACE space1;
```

Alternatively, use the[default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE)parameter:

```text
SET default_tablespace = space1;
CREATE TABLE foo(i int);
```

When`default_tablespace`is set to anything but an empty string, it supplies an implicit`TABLESPACE`clause for`CREATE TABLE`and`CREATE INDEX`commands that do not have an explicit one.

There is also a[temp\_tablespaces](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TEMP-TABLESPACES)parameter, which determines the placement of temporary tables and indexes, as well as temporary files that are used for purposes such as sorting large data sets. This can be a list of tablespace names, rather than only one, so that the load associated with temporary objects can be spread over multiple tablespaces. A random member of the list is picked each time a temporary object is to be created.

The tablespace associated with a database is used to store the system catalogs of that database. Furthermore, it is the default tablespace used for tables, indexes, and temporary files created within the database, if no`TABLESPACE`clause is given and no other selection is specified by`default_tablespace`or`temp_tablespaces`\(as appropriate\). If a database is created without specifying a tablespace for it, it uses the same tablespace as the template database it is copied from.

Two tablespaces are automatically created when the database cluster is initialized. The`pg_global`tablespace is used for shared system catalogs. The`pg_default`tablespace is the default tablespace of the`template1`and`template0`databases \(and, therefore, will be the default tablespace for other databases as well, unless overridden by a`TABLESPACE`clause in`CREATE DATABASE`\).

Once created, a tablespace can be used from any database, provided the requesting user has sufficient privilege. This means that a tablespace cannot be dropped until all objects in all databases using the tablespace have been removed.

To remove an empty tablespace, use the[DROP TABLESPACE](https://www.postgresql.org/docs/10/static/sql-droptablespace.html)command.

To determine the set of existing tablespaces, examine the[`pg_tablespace`](https://www.postgresql.org/docs/10/static/catalog-pg-tablespace.html)system catalog, for example

```text
SELECT spcname FROM pg_tablespace;
```

The[psql](https://www.postgresql.org/docs/10/static/app-psql.html)program's`\db`meta-command is also useful for listing the existing tablespaces.

PostgreSQLmakes use of symbolic links to simplify the implementation of tablespaces. This means that tablespaces can be used\_only\_on systems that support symbolic links.

The directory`$PGDATA/pg_tblspc`contains symbolic links that point to each of the non-built-in tablespaces defined in the cluster. Although not recommended, it is possible to adjust the tablespace layout by hand by redefining these links. Under no circumstances perform this operation while the server is running. Note that in PostgreSQL 9.1 and earlier you will also need to update the`pg_tablespace`catalog with the new locations. \(If you do not,`pg_dump`will continue to output the old tablespace locations.\)

## 參考資料

1.  [PostgreSQL: Documentation: 10: 22.6. Tablespaces](https://www.postgresql.org/docs/10/static/manage-ag-tablespaces.html)

