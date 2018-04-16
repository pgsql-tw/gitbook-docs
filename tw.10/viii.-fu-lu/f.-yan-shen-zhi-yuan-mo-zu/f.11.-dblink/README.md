# F.11. dblink

[dblink\_connect](https://www.postgresql.org/docs/10/static/contrib-dblink-connect.html)

— opens a persistent connection to a remote database

[dblink\_connect\_u](https://www.postgresql.org/docs/10/static/contrib-dblink-connect-u.html)

— opens a persistent connection to a remote database, insecurely

[dblink\_disconnect](https://www.postgresql.org/docs/10/static/contrib-dblink-disconnect.html)

— closes a persistent connection to a remote database

[dblink](https://www.postgresql.org/docs/10/static/contrib-dblink-function.html)

— executes a query in a remote database

[dblink\_exec](https://www.postgresql.org/docs/10/static/contrib-dblink-exec.html)

— executes a command in a remote database

[dblink\_open](https://www.postgresql.org/docs/10/static/contrib-dblink-open.html)

— opens a cursor in a remote database

[dblink\_fetch](https://www.postgresql.org/docs/10/static/contrib-dblink-fetch.html)

— returns rows from an open cursor in a remote database

[dblink\_close](https://www.postgresql.org/docs/10/static/contrib-dblink-close.html)

— closes a cursor in a remote database

[dblink\_get\_connections](https://www.postgresql.org/docs/10/static/contrib-dblink-get-connections.html)

— returns the names of all open named dblink connections

[dblink\_error\_message](https://www.postgresql.org/docs/10/static/contrib-dblink-error-message.html)

— gets last error message on the named connection

[dblink\_send\_query](https://www.postgresql.org/docs/10/static/contrib-dblink-send-query.html)

— sends an async query to a remote database

[dblink\_is\_busy](https://www.postgresql.org/docs/10/static/contrib-dblink-is-busy.html)

— checks if connection is busy with an async query

[dblink\_get\_notify](https://www.postgresql.org/docs/10/static/contrib-dblink-get-notify.html)

— retrieve async notifications on a connection

[dblink\_get\_result](https://www.postgresql.org/docs/10/static/contrib-dblink-get-result.html)

— gets an async query result

[dblink\_cancel\_query](https://www.postgresql.org/docs/10/static/contrib-dblink-cancel-query.html)

— cancels any active query on the named connection

[dblink\_get\_pkey](https://www.postgresql.org/docs/10/static/contrib-dblink-get-pkey.html)

— returns the positions and field names of a relation's primary key fields

[dblink\_build\_sql\_insert](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-insert.html)

— builds an INSERT statement using a local tuple, replacing the primary key field values with alternative supplied values

[dblink\_build\_sql\_delete](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-delete.html)

— builds a DELETE statement using supplied values for primary key field values

[dblink\_build\_sql\_update](https://www.postgresql.org/docs/10/static/contrib-dblink-build-sql-update.html)

— builds an UPDATE statement using a local tuple, replacing the primary key field values with alternative supplied values

`dblink`is a module that supports connections to otherPostgreSQLdatabases from within a database session.

See also[postgres\_fdw](https://www.postgresql.org/docs/10/static/postgres-fdw.html), which provides roughly the same functionality using a more modern and standards-compliant infrastructure.

