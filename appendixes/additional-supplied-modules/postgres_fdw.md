# F.33. postgres\_fdw

postgres\_fdw 模組提供了外部資料封裝器 postgres\_fdw，可用於存取儲存在外部 PostgreSQL 伺服器中的資料。

此模組提供的功能與舊版 dblink 模組的功能基本上是重疊的。但是 postgres\_fdw 提供了更直覺且符合標準的語法來存取遠端資料表，並且在許多情況下可以提供更好的效能。

要準備使用 postgres\_fdw 進行遠端存取：

1. 使用 [CREATE EXTENSION](../../reference/sql-commands/create-extension.md) 安裝 postgres\_fdw 延伸功能。
2. 使用 CREATE SERVER 建立一個外部伺服器物件，設定您要連線的每個遠端資料庫。將連線資訊（使用者名稱和密碼除外）指定為 SERVER 物件的選項。
3. 使用 [CREATE USER MAPPING](../../reference/sql-commands/create-user-mapping.md) 為要存取每個外部伺服器的每個資料庫使用者建立一個使用者對應。指定用作使用者對應的使用者和密碼選項的遠端使用者名稱和密碼。
4. 使用 [CREATE FOREIGN TABLE](../../reference/sql-commands/create-foreign-table.md) 或 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/import-foreign-schema.md) 為要存取的每個遠端資料表建立一個外部資料表。外部資料表的欄位必須與引用的遠端資料表相符。但是，如果您指定正確的遠端名稱作為外部資料表物件的選項，則可以使用與遠端資料不同的資料表名稱和欄位名稱。

現在，您只需要從外部資料表中執行 SELECT 即可存取儲存在遠端的基本資料表中的資料。您還可以使用 INSERT、UPDATE 或 DELETE 來修改遠端資料表。 （當然，您在 USER MAPPING 中所指定的遠端使用者必須具有執行這些操作的權限。）

請注意，postgres\_fdw 目前不支援帶有 ON CONFLICT DO UPDATE 子句的 INSERT 語句。但是，支援 ON CONFLICT DO NOTHING 子句，唯一性衝突處理宣告將會被忽略。還要注意，postgres\_fdw 支援在分割資料表上執行的 UPDATE 語句所呼叫的資料遷移，但是目前不能處理以下情況：選擇將插入資料的遠端分割區也剛好是後續要 UPDATE 的目標分割區。

通常建議使用與遠端資料表欄位完全相同的資料型別和排序規則來宣告外部資料表的欄位。儘管 postgres\_fdw 目前相當寬容地根據需要執行資料型別轉換，但是當型別或排序規則不符合時，由於遠端伺服器對 WHERE 子句的解釋與本機伺服器的解釋略有不同，因此可能會出現令人驚訝的語義結果。

請注意，與基本遠端資料表相比，可以用更少的欄位或不同的欄位順序宣告一個外部資料表。欄位與遠端資料表的對應是按名稱而不是位置進行的。

## F.33.1. FDW Options of postgres\_fdw

### **F.33.1.1. Connection Options**

A foreign server using the `postgres_fdw` foreign data wrapper can have the same options that libpq accepts in connection strings, as described in [Section 33.1.2](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PARAMKEYWORDS), except that these options are not allowed or have special handling:

* `user`, `password` and `sslpassword` (specify these in a user mapping, instead, or use a service file)
* `client_encoding` (this is automatically set from the local server encoding)
* `fallback_application_name` (always set to `postgres_fdw`)
* `sslkey` and `sslcert` - these may appear in _either or both_ a connection and a user mapping. If both are present, the user mapping setting overrides the connection setting.

Only superusers may create or modify user mappings with the `sslcert` or `sslkey` settings.

Only superusers may connect to foreign servers without password authentication, so always specify the `password` option for user mappings belonging to non-superusers.

A superuser may override this check on a per-user-mapping basis by setting the user mapping option `password_required 'false'`, e.g.,

```
ALTER USER MAPPING FOR some_non_superuser SERVER loopback_nopw
OPTIONS (ADD password_required 'false');
```

To prevent unprivileged users from exploiting the authentication rights of the unix user the postgres server is running as to escalate to superuser rights, only the superuser may set this option on a user mapping.

Care is required to ensure that this does not allow the mapped user the ability to connect as superuser to the mapped database per CVE-2007-3278 and CVE-2007-6601. Don't set `password_required=false` on the `public` role. Keep in mind that the mapped user can potentially use any client certificates, `.pgpass`, `.pg_service.conf` etc in the unix home directory of the system user the postgres server runs as. They can also use any trust relationship granted by authentication modes like `peer` or `ident` authentication.

### **F.33.1.2. Object Name Options**

These options can be used to control the names used in SQL statements sent to the remote PostgreSQL server. These options are needed when a foreign table is created with names different from the underlying remote table's names.

`schema_name`

This option, which can be specified for a foreign table, gives the schema name to use for the foreign table on the remote server. If this option is omitted, the name of the foreign table's schema is used.

`table_name`

This option, which can be specified for a foreign table, gives the table name to use for the foreign table on the remote server. If this option is omitted, the foreign table's name is used.

`column_name`

This option, which can be specified for a column of a foreign table, gives the column name to use for the column on the remote server. If this option is omitted, the column's name is used.

### **F.33.1.3. Cost Estimation Options**

`postgres_fdw` retrieves remote data by executing queries against remote servers, so ideally the estimated cost of scanning a foreign table should be whatever it costs to be done on the remote server, plus some overhead for communication. The most reliable way to get such an estimate is to ask the remote server and then add something for overhead — but for simple queries, it may not be worth the cost of an additional remote query to get a cost estimate. So `postgres_fdw` provides the following options to control how cost estimation is done:

`use_remote_estimate`

This option, which can be specified for a foreign table or a foreign server, controls whether `postgres_fdw` issues remote `EXPLAIN` commands to obtain cost estimates. A setting for a foreign table overrides any setting for its server, but only for that table. The default is `false`.

`fdw_startup_cost`

This option, which can be specified for a foreign server, is a numeric value that is added to the estimated startup cost of any foreign-table scan on that server. This represents the additional overhead of establishing a connection, parsing and planning the query on the remote side, etc. The default value is `100`.

`fdw_tuple_cost`

This option, which can be specified for a foreign server, is a numeric value that is used as extra cost per-tuple for foreign-table scans on that server. This represents the additional overhead of data transfer between servers. You might increase or decrease this number to reflect higher or lower network delay to the remote server. The default value is `0.01`.

When `use_remote_estimate` is true, `postgres_fdw` obtains row count and cost estimates from the remote server and then adds `fdw_startup_cost` and `fdw_tuple_cost` to the cost estimates. When `use_remote_estimate` is false, `postgres_fdw` performs local row count and cost estimation and then adds `fdw_startup_cost` and `fdw_tuple_cost` to the cost estimates. This local estimation is unlikely to be very accurate unless local copies of the remote table's statistics are available. Running [ANALYZE](https://www.postgresql.org/docs/13/sql-analyze.html) on the foreign table is the way to update the local statistics; this will perform a scan of the remote table and then calculate and store statistics just as though the table were local. Keeping local statistics can be a useful way to reduce per-query planning overhead for a remote table — but if the remote table is frequently updated, the local statistics will soon be obsolete.

### **F.33.1.4. Remote Execution Options**

By default, only `WHERE` clauses using built-in operators and functions will be considered for execution on the remote server. Clauses involving non-built-in functions are checked locally after rows are fetched. If such functions are available on the remote server and can be relied on to produce the same results as they do locally, performance can be improved by sending such `WHERE` clauses for remote execution. This behavior can be controlled using the following option:

`extensions`

This option is a comma-separated list of names of PostgreSQL extensions that are installed, in compatible versions, on both the local and remote servers. Functions and operators that are immutable and belong to a listed extension will be considered shippable to the remote server. This option can only be specified for foreign servers, not per-table.

When using the `extensions` option, _it is the user's responsibility_ that the listed extensions exist and behave identically on both the local and remote servers. Otherwise, remote queries may fail or behave unexpectedly.

`fetch_size`

This option specifies the number of rows `postgres_fdw` should get in each fetch operation. It can be specified for a foreign table or a foreign server. The option specified on a table overrides an option specified for the server. The default is `100`.

### **F.33.1.5. Updatability Options**

By default all foreign tables using `postgres_fdw` are assumed to be updatable. This may be overridden using the following option:`updatable`

This option controls whether `postgres_fdw` allows foreign tables to be modified using `INSERT`, `UPDATE` and `DELETE` commands. It can be specified for a foreign table or a foreign server. A table-level option overrides a server-level option. The default is `true`.

Of course, if the remote table is not in fact updatable, an error would occur anyway. Use of this option primarily allows the error to be thrown locally without querying the remote server. Note however that the `information_schema` views will report a `postgres_fdw` foreign table to be updatable (or not) according to the setting of this option, without any check of the remote server.

### **F.33.1.6. Importing Options**

`postgres_fdw` is able to import foreign table definitions using [IMPORT FOREIGN SCHEMA](https://www.postgresql.org/docs/13/sql-importforeignschema.html). This command creates foreign table definitions on the local server that match tables or views present on the remote server. If the remote tables to be imported have columns of user-defined data types, the local server must have compatible types of the same names.

Importing behavior can be customized with the following options (given in the `IMPORT FOREIGN SCHEMA` command):

`import_collate`

This option controls whether column `COLLATE` options are included in the definitions of foreign tables imported from a foreign server. The default is `true`. You might need to turn this off if the remote server has a different set of collation names than the local server does, which is likely to be the case if it's running on a different operating system.

`import_default`

This option controls whether column `DEFAULT` expressions are included in the definitions of foreign tables imported from a foreign server. The default is `false`. If you enable this option, be wary of defaults that might get computed differently on the local server than they would be on the remote server; `nextval()` is a common source of problems. The `IMPORT` will fail altogether if an imported default expression uses a function or operator that does not exist locally.

`import_not_null`

This option controls whether column `NOT NULL` constraints are included in the definitions of foreign tables imported from a foreign server. The default is `true`.

Note that constraints other than `NOT NULL` will never be imported from the remote tables. Although PostgreSQL does support `CHECK` constraints on foreign tables, there is no provision for importing them automatically, because of the risk that a constraint expression could evaluate differently on the local and remote servers. Any such inconsistency in the behavior of a `CHECK` constraint could lead to hard-to-detect errors in query optimization. So if you wish to import `CHECK` constraints, you must do so manually, and you should verify the semantics of each one carefully. For more detail about the treatment of `CHECK` constraints on foreign tables, see [CREATE FOREIGN TABLE](https://www.postgresql.org/docs/13/sql-createforeigntable.html).

Tables or foreign tables which are partitions of some other table are automatically excluded. Partitioned tables are imported, unless they are a partition of some other table. Since all data can be accessed through the partitioned table which is the root of the partitioning hierarchy, this approach should allow access to all the data without creating extra objects.

## F.33.2. Connection Management

`postgres_fdw` establishes a connection to a foreign server during the first query that uses a foreign table associated with the foreign server. This connection is kept and re-used for subsequent queries in the same session. However, if multiple user identities (user mappings) are used to access the foreign server, a connection is established for each user mapping.

## F.33.3. Transaction Management

During a query that references any remote tables on a foreign server, `postgres_fdw` opens a transaction on the remote server if one is not already open corresponding to the current local transaction. The remote transaction is committed or aborted when the local transaction commits or aborts. Savepoints are similarly managed by creating corresponding remote savepoints.

The remote transaction uses `SERIALIZABLE` isolation level when the local transaction has `SERIALIZABLE` isolation level; otherwise it uses `REPEATABLE READ` isolation level. This choice ensures that if a query performs multiple table scans on the remote server, it will get snapshot-consistent results for all the scans. A consequence is that successive queries within a single transaction will see the same data from the remote server, even if concurrent updates are occurring on the remote server due to other activities. That behavior would be expected anyway if the local transaction uses `SERIALIZABLE` or `REPEATABLE READ` isolation level, but it might be surprising for a `READ COMMITTED` local transaction. A future PostgreSQL release might modify these rules.

Note that it is currently not supported by `postgres_fdw` to prepare the remote transaction for two-phase commit.

## F.33.4. Remote Query Optimization

`postgres_fdw` attempts to optimize remote queries to reduce the amount of data transferred from foreign servers. This is done by sending query `WHERE` clauses to the remote server for execution, and by not retrieving table columns that are not needed for the current query. To reduce the risk of misexecution of queries, `WHERE` clauses are not sent to the remote server unless they use only data types, operators, and functions that are built-in or belong to an extension that's listed in the foreign server's `extensions` option. Operators and functions in such clauses must be `IMMUTABLE` as well. For an `UPDATE` or `DELETE` query, `postgres_fdw` attempts to optimize the query execution by sending the whole query to the remote server if there are no query `WHERE` clauses that cannot be sent to the remote server, no local joins for the query, no row-level local `BEFORE` or `AFTER` triggers or stored generated columns on the target table, and no `CHECK OPTION` constraints from parent views. In `UPDATE`, expressions to assign to target columns must use only built-in data types, `IMMUTABLE` operators, or `IMMUTABLE` functions, to reduce the risk of misexecution of the query.

When `postgres_fdw` encounters a join between foreign tables on the same foreign server, it sends the entire join to the foreign server, unless for some reason it believes that it will be more efficient to fetch rows from each table individually, or unless the table references involved are subject to different user mappings. While sending the `JOIN` clauses, it takes the same precautions as mentioned above for the `WHERE` clauses.

The query that is actually sent to the remote server for execution can be examined using `EXPLAIN VERBOSE`.

## F.33.5. Remote Query Execution Environment

In the remote sessions opened by `postgres_fdw`, the [search\_path](https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-SEARCH-PATH) parameter is set to just `pg_catalog`, so that only built-in objects are visible without schema qualification. This is not an issue for queries generated by `postgres_fdw` itself, because it always supplies such qualification. However, this can pose a hazard for functions that are executed on the remote server via triggers or rules on remote tables. For example, if a remote table is actually a view, any functions used in that view will be executed with the restricted search path. It is recommended to schema-qualify all names in such functions, or else attach `SET search_path` options (see [CREATE FUNCTION](https://www.postgresql.org/docs/13/sql-createfunction.html)) to such functions to establish their expected search path environment.

`postgres_fdw` likewise establishes remote session settings for various parameters:

* [TimeZone](https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-TIMEZONE) is set to `UTC`
* [DateStyle](https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-DATESTYLE) is set to `ISO`
* [IntervalStyle](https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-INTERVALSTYLE) is set to `postgres`
* [extra\_float\_digits](https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-EXTRA-FLOAT-DIGITS) is set to `3` for remote servers 9.0 and newer and is set to `2` for older versions

These are less likely to be problematic than `search_path`, but can be handled with function `SET` options if the need arises.

It is _not_ recommended that you override this behavior by changing the session-level settings of these parameters; that is likely to cause `postgres_fdw` to malfunction.

## F.33.6. Cross-Version Compatibility

`postgres_fdw` can be used with remote servers dating back to PostgreSQL 8.3. Read-only capability is available back to 8.1. A limitation however is that `postgres_fdw` generally assumes that immutable built-in functions and operators are safe to send to the remote server for execution, if they appear in a `WHERE` clause for a foreign table. Thus, a built-in function that was added since the remote server's release might be sent to it for execution, resulting in “function does not exist” or a similar error. This type of failure can be worked around by rewriting the query, for example by embedding the foreign table reference in a sub-`SELECT` with `OFFSET 0` as an optimization fence, and placing the problematic function or operator outside the sub-`SELECT`.

## F.33.7. 範例

這是使用 postgres\_fdw 建立一個外部資料表的範例。 首先安裝延伸功能：

```
CREATE EXTENSION postgres_fdw;
```

然後使用 [CREATE SERVER](../../reference/sql-commands/create-server.md) 建立一個外部伺服器。在此範例中，我們希望連線到主機 192.83.123.89 上連接埠為 5432 的 PostgreSQL 伺服器。該伺服器建立連線的資料庫，在遠端伺服器上的名稱為 foreign\_db：

```
CREATE SERVER foreign_server
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host '192.83.123.89', port '5432', dbname 'foreign_db');
```

還需要使用 [CREATE USER MAPPING](../../reference/sql-commands/create-user-mapping.md) 定義的使用者對應，以標示將在遠端伺服器上所使用的角色：

```
CREATE USER MAPPING FOR local_user
        SERVER foreign_server
        OPTIONS (user 'foreign_user', password 'password');
```

現在可以用 [CREATE FOREIGN TABLE](../../reference/sql-commands/create-foreign-table.md) 建立一個外部資料表。在此範例中，我們希望存取遠端伺服器上名為 some\_schema.some\_table 的資料表。它在本機的名稱將為 foreign\_table：

```
CREATE FOREIGN TABLE foreign_table (
        id integer NOT NULL,
        data text
)
        SERVER foreign_server
        OPTIONS (schema_name 'some_schema', table_name 'some_table');
```

在 CREATE FOREIGN TABLE 中宣告的欄位資料型別和其他屬性必須與實際遠端的資料表相符。欄位名稱也必須相符，除非您將 column\_name 選項附加到各個欄位以表示它們在遠端資料表中的命名方式。在許多情況下，使用 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/import-foreign-schema.md) 優於手動建構外部資料表定義。

## F.33.8. 作者

Shigeru Hanada `<`[`shigeru.hanada@gmail.com`](mailto:shigeru.hanada@gmail.com)`>`
