## F.11. dblink — connect to other PostgreSQL databases [#](#DBLINK)

[dblink_connect](contrib-dblink-connect.md) — opens a persistent connection to a remote database

[dblink_connect_u](contrib-dblink-connect-u.md) — opens a persistent connection to a remote database, insecurely

[dblink_disconnect](contrib-dblink-disconnect.md) — closes a persistent connection to a remote database

[dblink](contrib-dblink-function.md) — executes a query in a remote database

[dblink_exec](contrib-dblink-exec.md) — executes a command in a remote database

[dblink_open](contrib-dblink-open.md) — opens a cursor in a remote database

[dblink_fetch](contrib-dblink-fetch.md) — returns rows from an open cursor in a remote database

[dblink_close](contrib-dblink-close.md) — closes a cursor in a remote database

[dblink_get_connections](contrib-dblink-get-connections.md) — returns the names of all open named dblink connections

[dblink_error_message](contrib-dblink-error-message.md) — gets last error message on the named connection

[dblink_send_query](contrib-dblink-send-query.md) — sends an async query to a remote database

[dblink_is_busy](contrib-dblink-is-busy.md) — checks if connection is busy with an async query

[dblink_get_notify](contrib-dblink-get-notify.md) — retrieve async notifications on a connection

[dblink_get_result](contrib-dblink-get-result.md) — gets an async query result

[dblink_cancel_query](contrib-dblink-cancel-query.md) — cancels any active query on the named connection

[dblink_get_pkey](contrib-dblink-get-pkey.md) — returns the positions and field names of a relation's primary key fields

[dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — builds an INSERT statement using a local tuple, replacing the primary key field values with alternative supplied values

[dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — builds a DELETE statement using supplied values for primary key field values

[dblink_build_sql_update](contrib-dblink-build-sql-update.md) — builds an UPDATE statement using a local tuple, replacing the primary key field values with alternative supplied values

<a id="id-1.11.7.21.2"></a>

`dblink` is a module that supports connections to
other PostgreSQL databases from within a database
session.

`dblink` can report the following wait events under the wait
event type `Extension`.

`DblinkConnect`
:   Waiting to establish a connection to a remote server.

`DblinkGetConnect`
:   Waiting to establish a connection to a remote server when it could not
    be found in the list of already-opened connections.

`DblinkGetResult`
:   Waiting to receive the results of a query from a remote server.

See also [postgres_fdw](postgres-fdw.md), which provides roughly the same
functionality using a more modern and standards-compliant infrastructure.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dblink.html)（英文原文，待翻譯）
