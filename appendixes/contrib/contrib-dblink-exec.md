<a id="id-1.11.7.21.11.1"></a>

## dblink_exec

dblink_exec — executes a command in a remote database

## Synopsis

```

dblink_exec(text connname, text sql [, bool fail_on_error]) returns text
dblink_exec(text connstr, text sql [, bool fail_on_error]) returns text
dblink_exec(text sql [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.11.5"></a>

## Description

`dblink_exec` executes a command (that is, any SQL statement
that doesn't return rows) in a remote database.

When two `text` arguments are given, the first one is first
looked up as a persistent connection's name; if found, the command
is executed on that connection. If not found, the first argument
is treated as a connection info string as for `dblink_connect`,
and the indicated connection is made just for the duration of this command.

<a id="id-1.11.7.21.11.6"></a>

## Arguments

*`connname`*
:   Name of the connection to use; omit this parameter to use the
    unnamed connection.

*`connstr`*
:   A connection info string, as previously described for
    `dblink_connect`.

*`sql`*
:   The SQL command that you wish to execute in the remote database,
    for example
    `insert into foo values(0, 'a', '{"a0","b0","c0"}')`.

*`fail_on_error`*
:   If true (the default when omitted) then an error thrown on the
    remote side of the connection causes an error to also be thrown
    locally. If false, the remote error is locally reported as a NOTICE,
    and the function's return value is set to `ERROR`.

<a id="id-1.11.7.21.11.7"></a>

## Return Value

Returns status, either the command's status string or `ERROR`.

<a id="id-1.11.7.21.11.8"></a>

## Examples

```

SELECT dblink_connect('dbname=dblink_test_standby');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
-----------------
 INSERT 943366 1
(1 row)

SELECT dblink_connect('myconn', 'dbname=regression');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('myconn', 'insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
------------------
 INSERT 6432584 1
(1 row)

SELECT dblink_exec('myconn', 'insert into pg_class values (''foo'')',false);
NOTICE:  sql error
DETAIL:  ERROR:  null value in column "relnamespace" violates not-null constraint

 dblink_exec
-------------
 ERROR
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-exec.html)（英文原文，待翻譯）
