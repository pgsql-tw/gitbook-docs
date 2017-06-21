# 5.11. 外部資料[^1]

PostgreSQLimplements portions of the SQL/MED specification, allowing you to access data that resides outside PostgreSQL using regular SQL queries. Such data is referred to as_foreign data_. \(Note that this usage is not to be confused with foreign keys, which are a type of constraint within the database.\)

Foreign data is accessed with help from a_foreign data wrapper_. A foreign data wrapper is a library that can communicate with an external data source, hiding the details of connecting to the data source and obtaining data from it. There are some foreign data wrappers available as`contrib`modules; see[Appendix F](https://www.postgresql.org/docs/10/static/contrib.html). Other kinds of foreign data wrappers might be found as third party products. If none of the existing foreign data wrappers suit your needs, you can write your own; see[Chapter 56](https://www.postgresql.org/docs/10/static/fdwhandler.html).

To access foreign data, you need to create a_foreign server_object, which defines how to connect to a particular external data source according to the set of options used by its supporting foreign data wrapper. Then you need to create one or more_foreign tables_, which define the structure of the remote data. A foreign table can be used in queries just like a normal table, but a foreign table has no storage in the PostgreSQL server. Whenever it is used,PostgreSQLasks the foreign data wrapper to fetch data from the external source, or transmit data to the external source in the case of update commands.

Accessing remote data may require authenticating to the external data source. This information can be provided by a_user mapping_, which can provide additional data such as user names and passwords based on the currentPostgreSQLrole.

For additional information, see[CREATE FOREIGN DATA WRAPPER](https://www.postgresql.org/docs/10/static/sql-createforeigndatawrapper.html),[CREATE SERVER](https://www.postgresql.org/docs/10/static/sql-createserver.html),[CREATE USER MAPPING](https://www.postgresql.org/docs/10/static/sql-createusermapping.html),[CREATE FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-createforeigntable.html), and[IMPORT FOREIGN SCHEMA](https://www.postgresql.org/docs/10/static/sql-importforeignschema.html).

---



[^1]: [PostgreSQL: Documentation: 10: 5.11. Foreign Data](https://www.postgresql.org/docs/10/static/ddl-foreign-data.html)

