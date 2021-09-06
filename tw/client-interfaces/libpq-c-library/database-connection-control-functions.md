---
description: 版本：11
---

# 33.1. 資料庫連線控制函數

The following functions deal with making a connection to a PostgreSQL backend server. An application program can have several backend connections open at one time. \(One reason to do that is to access more than one database.\) Each connection is represented by a `PGconn` object, which is obtained from the function [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB), [`PQconnectdbParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS), or [`PQsetdbLogin`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQSETDBLOGIN). Note that these functions will always return a non-null object pointer, unless perhaps there is too little memory even to allocate the `PGconn` object. The [`PQstatus`](https://www.postgresql.org/docs/13/libpq-status.html#LIBPQ-PQSTATUS) function should be called to check the return value for a successful connection before queries are sent via the connection object.

#### Warning

If untrusted users have access to a database that has not adopted a [secure schema usage pattern](https://www.postgresql.org/docs/13/ddl-schemas.html#DDL-SCHEMAS-PATTERNS), begin each session by removing publicly-writable schemas from `search_path`. One can set parameter key word `options` to value `-csearch_path=`. Alternately, one can issue `PQexec(`_`conn`_, "SELECT pg\_catalog.set\_config\('search\_path', '', false\)"\) after connecting. This consideration is not specific to libpq; it applies to every interface for executing arbitrary SQL commands.

#### Warning

On Unix, forking a process with open libpq connections can lead to unpredictable results because the parent and child processes share the same sockets and operating system resources. For this reason, such usage is not recommended, though doing an `exec` from the child process to load a new executable is safe.

`PQconnectdbParams`

Makes a new connection to the database server.

```text
PGconn *PQconnectdbParams(const char * const *keywords,
                          const char * const *values,
                          int expand_dbname);
```

This function opens a new database connection using the parameters taken from two `NULL`-terminated arrays. The first, `keywords`, is defined as an array of strings, each one being a key word. The second, `values`, gives the value for each key word. Unlike [`PQsetdbLogin`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQSETDBLOGIN) below, the parameter set can be extended without changing the function signature, so use of this function \(or its nonblocking analogs [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS) and `PQconnectPoll`\) is preferred for new application programming.

The currently recognized parameter key words are listed in [Section 33.1.2](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

The passed arrays can be empty to use all default parameters, or can contain one or more parameter settings. They must be matched in length. Processing will stop at the first `NULL` entry in the `keywords` array. Also, if the `values` entry associated with a non-`NULL` `keywords` entry is `NULL` or an empty string, that entry is ignored and processing continues with the next pair of array entries.

When `expand_dbname` is non-zero, the value for the first _`dbname`_ key word is checked to see if it is a _connection string_. If so, it is “expanded” into the individual connection parameters extracted from the string. The value is considered to be a connection string, rather than just a database name, if it contains an equal sign \(`=`\) or it begins with a URI scheme designator. \(More details on connection string formats appear in [Section 33.1.1](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING).\) Only the first occurrence of _`dbname`_ is treated in this way; any subsequent _`dbname`_ parameter is processed as a plain database name.

In general the parameter arrays are processed from start to end. If any key word is repeated, the last value \(that is not `NULL` or empty\) is used. This rule applies in particular when a key word found in a connection string conflicts with one appearing in the `keywords` array. Thus, the programmer may determine whether array entries can override or be overridden by values taken from a connection string. Array entries appearing before an expanded _`dbname`_ entry can be overridden by fields of the connection string, and in turn those fields are overridden by array entries appearing after _`dbname`_ \(but, again, only if those entries supply non-empty values\).

After processing all the array entries and any expanded connection string, any connection parameters that remain unset are filled with default values. If an unset parameter's corresponding environment variable \(see [Section 33.14](https://www.postgresql.org/docs/13/libpq-envars.html)\) is set, its value is used. If the environment variable is not set either, then the parameter's built-in default value is used.

`PQconnectdb`

Makes a new connection to the database server.

```text
PGconn *PQconnectdb(const char *conninfo);
```

This function opens a new database connection using the parameters taken from the string `conninfo`.

The passed string can be empty to use all default parameters, or it can contain one or more parameter settings separated by whitespace, or it can contain a URI. See [Section 33.1.1](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING) for details.

`PQsetdbLogin`

Makes a new connection to the database server.

```text
PGconn *PQsetdbLogin(const char *pghost,
                     const char *pgport,
                     const char *pgoptions,
                     const char *pgtty,
                     const char *dbName,
                     const char *login,
                     const char *pwd);
```

This is the predecessor of [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB) with a fixed set of parameters. It has the same functionality except that the missing parameters will always take on default values. Write `NULL` or an empty string for any one of the fixed parameters that is to be defaulted.

If the _`dbName`_ contains an `=` sign or has a valid connection URI prefix, it is taken as a _`conninfo`_ string in exactly the same way as if it had been passed to [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB), and the remaining parameters are then applied as specified for [`PQconnectdbParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS).

`PQsetdb`

Makes a new connection to the database server.

```text
PGconn *PQsetdb(char *pghost,
                char *pgport,
                char *pgoptions,
                char *pgtty,
                char *dbName);
```

This is a macro that calls [`PQsetdbLogin`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQSETDBLOGIN) with null pointers for the _`login`_ and _`pwd`_ parameters. It is provided for backward compatibility with very old programs.`PQconnectStartParams`  
`PQconnectStart`  
`PQconnectPoll`

Make a connection to the database server in a nonblocking manner.

```text
PGconn *PQconnectStartParams(const char * const *keywords,
                             const char * const *values,
                             int expand_dbname);

PGconn *PQconnectStart(const char *conninfo);

PostgresPollingStatusType PQconnectPoll(PGconn *conn);
```

These three functions are used to open a connection to a database server such that your application's thread of execution is not blocked on remote I/O whilst doing so. The point of this approach is that the waits for I/O to complete can occur in the application's main loop, rather than down inside [`PQconnectdbParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS) or [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB), and so the application can manage this operation in parallel with other activities.

With [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS), the database connection is made using the parameters taken from the `keywords` and `values` arrays, and controlled by `expand_dbname`, as described above for [`PQconnectdbParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS).

With `PQconnectStart`, the database connection is made using the parameters taken from the string `conninfo` as described above for [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB).

Neither [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS) nor `PQconnectStart` nor `PQconnectPoll` will block, so long as a number of restrictions are met:

* The `hostaddr` parameter must be used appropriately to prevent DNS queries from being made. See the documentation of this parameter in [Section 33.1.2](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PARAMKEYWORDS) for details.
* If you call [`PQtrace`](https://www.postgresql.org/docs/13/libpq-control.html#LIBPQ-PQTRACE), ensure that the stream object into which you trace will not block.
* You must ensure that the socket is in the appropriate state before calling `PQconnectPoll`, as described below.

To begin a nonblocking connection request, call `PQconnectStart` or [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS). If the result is null, then libpq has been unable to allocate a new `PGconn` structure. Otherwise, a valid `PGconn` pointer is returned \(though not yet representing a valid connection to the database\). Next call `PQstatus(conn)`. If the result is `CONNECTION_BAD`, the connection attempt has already failed, typically because of invalid connection parameters.

If `PQconnectStart` or [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS) succeeds, the next stage is to poll libpq so that it can proceed with the connection sequence. Use `PQsocket(conn)` to obtain the descriptor of the socket underlying the database connection. \(Caution: do not assume that the socket remains the same across `PQconnectPoll` calls.\) Loop thus: If `PQconnectPoll(conn)` last returned `PGRES_POLLING_READING`, wait until the socket is ready to read \(as indicated by `select()`, `poll()`, or similar system function\). Then call `PQconnectPoll(conn)` again. Conversely, if `PQconnectPoll(conn)` last returned `PGRES_POLLING_WRITING`, wait until the socket is ready to write, then call `PQconnectPoll(conn)` again. On the first iteration, i.e., if you have yet to call `PQconnectPoll`, behave as if it last returned `PGRES_POLLING_WRITING`. Continue this loop until `PQconnectPoll(conn)` returns `PGRES_POLLING_FAILED`, indicating the connection procedure has failed, or `PGRES_POLLING_OK`, indicating the connection has been successfully made.

At any time during connection, the status of the connection can be checked by calling [`PQstatus`](https://www.postgresql.org/docs/13/libpq-status.html#LIBPQ-PQSTATUS). If this call returns `CONNECTION_BAD`, then the connection procedure has failed; if the call returns `CONNECTION_OK`, then the connection is ready. Both of these states are equally detectable from the return value of `PQconnectPoll`, described above. Other states might also occur during \(and only during\) an asynchronous connection procedure. These indicate the current stage of the connection procedure and might be useful to provide feedback to the user for example. These statuses are:

`CONNECTION_STARTED`

Waiting for connection to be made.

`CONNECTION_MADE`

Connection OK; waiting to send.

`CONNECTION_AWAITING_RESPONSE`

Waiting for a response from the server.

`CONNECTION_AUTH_OK`

Received authentication; waiting for backend start-up to finish.

`CONNECTION_SSL_STARTUP`

Negotiating SSL encryption.

`CONNECTION_SETENV`

Negotiating environment-driven parameter settings.

`CONNECTION_CHECK_WRITABLE`

Checking if connection is able to handle write transactions.

`CONNECTION_CONSUME`

Consuming any remaining response messages on connection.

Note that, although these constants will remain \(in order to maintain compatibility\), an application should never rely upon these occurring in a particular order, or at all, or on the status always being one of these documented values. An application might do something like this:

```text
switch(PQstatus(conn))
{
        case CONNECTION_STARTED:
            feedback = "Connecting...";
            break;

        case CONNECTION_MADE:
            feedback = "Connected to server...";
            break;
.
.
.
        default:
            feedback = "Connecting...";
}
```

The `connect_timeout` connection parameter is ignored when using `PQconnectPoll`; it is the application's responsibility to decide whether an excessive amount of time has elapsed. Otherwise, `PQconnectStart` followed by a `PQconnectPoll` loop is equivalent to [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB).

Note that when `PQconnectStart` or [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS) returns a non-null pointer, you must call [`PQfinish`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQFINISH) when you are finished with it, in order to dispose of the structure and any associated memory blocks. This must be done even if the connection attempt fails or is abandoned.

`PQconndefaults`

Returns the default connection options.

```text
PQconninfoOption *PQconndefaults(void);

typedef struct
{
    char   *keyword;   /* The keyword of the option */
    char   *envvar;    /* Fallback environment variable name */
    char   *compiled;  /* Fallback compiled in default value */
    char   *val;       /* Option's current value, or NULL */
    char   *label;     /* Label for field in connect dialog */
    char   *dispchar;  /* Indicates how to display this field
                          in a connect dialog. Values are:
                          ""        Display entered value as is
                          "*"       Password field - hide value
                          "D"       Debug option - don't show by default */
    int     dispsize;  /* Field size in characters for dialog */
} PQconninfoOption;
```

Returns a connection options array. This can be used to determine all possible [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB) options and their current default values. The return value points to an array of `PQconninfoOption` structures, which ends with an entry having a null `keyword` pointer. The null pointer is returned if memory could not be allocated. Note that the current default values \(`val` fields\) will depend on environment variables and other context. A missing or invalid service file will be silently ignored. Callers must treat the connection options data as read-only.

After processing the options array, free it by passing it to [`PQconninfoFree`](https://www.postgresql.org/docs/13/libpq-misc.html#LIBPQ-PQCONNINFOFREE). If this is not done, a small amount of memory is leaked for each call to [`PQconndefaults`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNDEFAULTS).`PQconninfo`

Returns the connection options used by a live connection.

```text
PQconninfoOption *PQconninfo(PGconn *conn);
```

Returns a connection options array. This can be used to determine all possible [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB) options and the values that were used to connect to the server. The return value points to an array of `PQconninfoOption` structures, which ends with an entry having a null `keyword` pointer. All notes above for [`PQconndefaults`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNDEFAULTS) also apply to the result of [`PQconninfo`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNINFO).

`PQconninfoParse`

Returns parsed connection options from the provided connection string.

```text
PQconninfoOption *PQconninfoParse(const char *conninfo, char **errmsg);
```

Parses a connection string and returns the resulting options as an array; or returns `NULL` if there is a problem with the connection string. This function can be used to extract the [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB) options in the provided connection string. The return value points to an array of `PQconninfoOption` structures, which ends with an entry having a null `keyword` pointer.

All legal options will be present in the result array, but the `PQconninfoOption` for any option not present in the connection string will have `val` set to `NULL`; default values are not inserted.

If `errmsg` is not `NULL`, then `*errmsg` is set to `NULL` on success, else to a `malloc`'d error string explaining the problem. \(It is also possible for `*errmsg` to be set to `NULL` and the function to return `NULL`; this indicates an out-of-memory condition.\)

After processing the options array, free it by passing it to [`PQconninfoFree`](https://www.postgresql.org/docs/13/libpq-misc.html#LIBPQ-PQCONNINFOFREE). If this is not done, some memory is leaked for each call to [`PQconninfoParse`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNINFOPARSE). Conversely, if an error occurs and `errmsg` is not `NULL`, be sure to free the error string using [`PQfreemem`](https://www.postgresql.org/docs/13/libpq-misc.html#LIBPQ-PQFREEMEM).

`PQfinish`

Closes the connection to the server. Also frees memory used by the `PGconn` object.

```text
void PQfinish(PGconn *conn);
```

Note that even if the server connection attempt fails \(as indicated by [`PQstatus`](https://www.postgresql.org/docs/13/libpq-status.html#LIBPQ-PQSTATUS)\), the application should call [`PQfinish`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQFINISH) to free the memory used by the `PGconn` object. The `PGconn` pointer must not be used again after [`PQfinish`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQFINISH) has been called.

`PQreset`

Resets the communication channel to the server.

```text
void PQreset(PGconn *conn);
```

This function will close the connection to the server and attempt to establish a new connection, using all the same parameters previously used. This might be useful for error recovery if a working connection is lost.

`PQresetStart`  
`PQresetPoll`

Reset the communication channel to the server, in a nonblocking manner.

```text
int PQresetStart(PGconn *conn);

PostgresPollingStatusType PQresetPoll(PGconn *conn);
```

These functions will close the connection to the server and attempt to establish a new connection, using all the same parameters previously used. This can be useful for error recovery if a working connection is lost. They differ from [`PQreset`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQRESET) \(above\) in that they act in a nonblocking manner. These functions suffer from the same restrictions as [`PQconnectStartParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTSTARTPARAMS), `PQconnectStart` and `PQconnectPoll`.

To initiate a connection reset, call [`PQresetStart`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQRESETSTART). If it returns 0, the reset has failed. If it returns 1, poll the reset using `PQresetPoll` in exactly the same way as you would create the connection using `PQconnectPoll`.

`PQpingParams`

[`PQpingParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQPINGPARAMS) reports the status of the server. It accepts connection parameters identical to those of [`PQconnectdbParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS), described above. It is not necessary to supply correct user name, password, or database name values to obtain the server status; however, if incorrect values are provided, the server will log a failed connection attempt.

```text
PGPing PQpingParams(const char * const *keywords,
                    const char * const *values,
                    int expand_dbname);
```

The function returns one of the following values:

`PQPING_OK`

The server is running and appears to be accepting connections.

`PQPING_REJECT`

The server is running but is in a state that disallows connections \(startup, shutdown, or crash recovery\).

`PQPING_NO_RESPONSE`

The server could not be contacted. This might indicate that the server is not running, or that there is something wrong with the given connection parameters \(for example, wrong port number\), or that there is a network connectivity problem \(for example, a firewall blocking the connection request\).

`PQPING_NO_ATTEMPT`

No attempt was made to contact the server, because the supplied parameters were obviously incorrect or there was some client-side problem \(for example, out of memory\).

`PQping`

[`PQping`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQPING) reports the status of the server. It accepts connection parameters identical to those of [`PQconnectdb`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQCONNECTDB), described above. It is not necessary to supply correct user name, password, or database name values to obtain the server status; however, if incorrect values are provided, the server will log a failed connection attempt.

```text
PGPing PQping(const char *conninfo);
```

The return values are the same as for [`PQpingParams`](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PQPINGPARAMS).

`PQsetSSLKeyPassHook_OpenSSL`

`PQsetSSLKeyPassHook_OpenSSL` lets an application override libpq's [default handling of encrypted client certificate key files](https://www.postgresql.org/docs/13/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT) using [sslpassword](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD) or interactive prompting.

```text
void PQsetSSLKeyPassHook_OpenSSL(PQsslKeyPassHook_OpenSSL_type hook);
```

The application passes a pointer to a callback function with signature:

```text
int callback_fn(char *buf, int size, PGconn *conn);
```

which libpq will then call _instead of_ its default `PQdefaultSSLKeyPassHook_OpenSSL` handler. The callback should determine the password for the key and copy it to result-buffer _`buf`_ of size _`size`_. The string in _`buf`_ must be null-terminated. The callback must return the length of the password stored in _`buf`_ excluding the null terminator. On failure, the callback should set `buf[0] = '\0'` and return 0. See `PQdefaultSSLKeyPassHook_OpenSSL` in libpq's source code for an example.

If the user specified an explicit key location, its path will be in `conn->sslkey` when the callback is invoked. This will be empty if the default key path is being used. For keys that are engine specifiers, it is up to engine implementations whether they use the OpenSSL password callback or define their own handling.

The app callback may choose to delegate unhandled cases to `PQdefaultSSLKeyPassHook_OpenSSL`, or call it first and try something else if it returns 0, or completely override it.

The callback _must not_ escape normal flow control with exceptions, `longjmp(...)`, etc. It must return normally.

`PQgetSSLKeyPassHook_OpenSSL`

`PQgetSSLKeyPassHook_OpenSSL` returns the current client certificate key password hook, or `NULL` if none has been set.

```text
PQsslKeyPassHook_OpenSSL_type PQgetSSLKeyPassHook_OpenSSL(void);
```

## 33.1.1. Connection Strings

Several libpq functions parse a user-specified string to obtain connection parameters. There are two accepted formats for these strings: plain keyword/value strings and URIs. URIs generally follow [RFC 3986](https://tools.ietf.org/html/rfc3986), except that multi-host connection strings are allowed as further described below.

### **33.1.1.1. Keyword/Value Connection Strings**

In the keyword/value format, each parameter setting is in the form _`keyword`_ `=` _`value`_, with space\(s\) between settings. Spaces around a setting's equal sign are optional. To write an empty value, or a value containing spaces, surround it with single quotes, for example `keyword = 'a value'`. Single quotes and backslashes within a value must be escaped with a backslash, i.e., `\'` and `\\`.

Example:

```text
host=localhost port=5432 dbname=mydb connect_timeout=10
```

The recognized parameter key words are listed in [Section 33.1.2](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

### **33.1.1.2. Connection URIs**

The general form for a connection URI is:

```text
postgresql://[userspec@][hostspec][/dbname][?paramspec]

where userspec is:

user[:password]

and hostspec is:

[host][:port][,...]

and paramspec is:

name=value[&...]
```

The URI scheme designator can be either `postgresql://` or `postgres://`. Each of the remaining URI parts is optional. The following examples illustrate valid URI syntax:

```text
postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
```

Values that would normally appear in the hierarchical part of the URI can alternatively be given as named parameters. For example:

```text
postgresql:///mydb?host=localhost&port=5433
```

All named parameters must match key words listed in [Section 33.1.2](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-PARAMKEYWORDS), except that for compatibility with JDBC connection URIs, instances of `ssl=true` are translated into `sslmode=require`.

The connection URI needs to be encoded with [percent-encoding](https://tools.ietf.org/html/rfc3986#section-2.1) if it includes symbols with special meaning in any of its parts. Here is an example where the equal sign \(`=`\) is replaced with `%3D` and the space character with `%20`:

```text
postgresql://user@localhost:5433/mydb?options=-c%20synchronous_commit%3Doff
```

The host part may be either a host name or an IP address. To specify an IPv6 address, enclose it in square brackets:

```text
postgresql://[2001:db8::1234]/database
```

The host part is interpreted as described for the parameter [host](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNECT-HOST). In particular, a Unix-domain socket connection is chosen if the host part is either empty or looks like an absolute path name, otherwise a TCP/IP connection is initiated. Note, however, that the slash is a reserved character in the hierarchical part of the URI. So, to specify a non-standard Unix-domain socket directory, either omit the host part of the URI and specify the host as a named parameter, or percent-encode the path in the host part of the URI:

```text
postgresql:///dbname?host=/var/lib/postgresql
postgresql://%2Fvar%2Flib%2Fpostgresql/dbname
```

It is possible to specify multiple host components, each with an optional port component, in a single URI. A URI of the form `postgresql://host1:port1,host2:port2,host3:port3/` is equivalent to a connection string of the form `host=host1,host2,host3 port=port1,port2,port3`. As further described below, each host will be tried in turn until a connection is successfully established.

### **33.1.1.3. Specifying Multiple Hosts**

可以指定多個連線主機，以便按次序嘗試連線。在 Keyword/Value 格式中，host、hostaddr 和 port 選項可以接受以逗號分隔的列表。在指定的每個選項中必須設定相同數量的元素。例如，第一個 hostaddr 對應於第一個主機名稱，第二個 hostaddr 對應於第二個主機名稱，依此類推。作為例外，如果只指定了一個連接埠，則它適用於所有主機。

在連線的 URI 格式中，您可以在 URI 的主機部份中列出多個以逗號分隔的 host:port。

無論採用哪種格式，單個主機名稱都可以轉換為多個網路位址。這方面的一個常見情況是同時具有 IPv4 和 IPv6 位址的主機。

當指定多個主機時，或者當單個主機名稱轉換為多個位址時，將依次嘗試所有主機和位址，直到成功為止。如果無法連線任何主機，才會連線失敗。但如果連線成功建立，但身份驗證失敗，則不會嘗試列表中的其餘主機。

如果使用密碼檔，您可以為不同的主機設定不同的密碼。對於列表中的每個主機，所有其他連線選項都相同；例如，不可能為不同的主機指定不同的使用者名稱。

## 33.1.2. Parameter Key Words

The currently recognized parameter key words are:

`host`

Name of host to connect to. If a host name looks like an absolute path name, it specifies Unix-domain communication rather than TCP/IP communication; the value is the name of the directory in which the socket file is stored. \(On Unix, an absolute path name begins with a slash. On Windows, paths starting with drive letters are also recognized.\) The default behavior when `host` is not specified, or is empty, is to connect to a Unix-domain socket in `/tmp` \(or whatever socket directory was specified when PostgreSQL was built\). On Windows and on machines without Unix-domain sockets, the default is to connect to `localhost`.

A comma-separated list of host names is also accepted, in which case each host name in the list is tried in order; an empty item in the list selects the default behavior as explained above. See [Section 33.1.1.3](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-MULTIPLE-HOSTS) for details.

`hostaddr`

Numeric IP address of host to connect to. This should be in the standard IPv4 address format, e.g., `172.28.40.9`. If your machine supports IPv6, you can also use those addresses. TCP/IP communication is always used when a nonempty string is specified for this parameter. If this parameter is not specified, the value of `host` will be looked up to find the corresponding IP address — or, if `host` specifies an IP address, that value will be used directly.

Using `hostaddr` allows the application to avoid a host name look-up, which might be important in applications with time constraints. However, a host name is required for GSSAPI or SSPI authentication methods, as well as for `verify-full` SSL certificate verification. The following rules are used:

* If `host` is specified without `hostaddr`, a host name lookup occurs. \(When using `PQconnectPoll`, the lookup occurs when `PQconnectPoll` first considers this host name, and it may cause `PQconnectPoll` to block for a significant amount of time.\)
* If `hostaddr` is specified without `host`, the value for `hostaddr` gives the server network address. The connection attempt will fail if the authentication method requires a host name.
* If both `host` and `hostaddr` are specified, the value for `hostaddr` gives the server network address. The value for `host` is ignored unless the authentication method requires it, in which case it will be used as the host name.

Note that authentication is likely to fail if `host` is not the name of the server at network address `hostaddr`. Also, when both `host` and `hostaddr` are specified, `host` is used to identify the connection in a password file \(see [Section 33.15](https://www.postgresql.org/docs/13/libpq-pgpass.html)\).

A comma-separated list of `hostaddr` values is also accepted, in which case each host in the list is tried in order. An empty item in the list causes the corresponding host name to be used, or the default host name if that is empty as well. See [Section 33.1.1.3](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-MULTIPLE-HOSTS) for details.

Without either a host name or host address, libpq will connect using a local Unix-domain socket; or on Windows and on machines without Unix-domain sockets, it will attempt to connect to `localhost`.

`port`

Port number to connect to at the server host, or socket file name extension for Unix-domain connections. If multiple hosts were given in the `host` or `hostaddr` parameters, this parameter may specify a comma-separated list of ports of the same length as the host list, or it may specify a single port number to be used for all hosts. An empty string, or an empty item in a comma-separated list, specifies the default port number established when PostgreSQL was built.

`dbname`

The database name. Defaults to be the same as the user name. In certain contexts, the value is checked for extended formats; see [Section 33.1.1](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING) for more details on those.

`user`

PostgreSQL user name to connect as. Defaults to be the same as the operating system name of the user running the application.

`password`

Password to be used if the server demands password authentication.

`passfile`

Specifies the name of the file used to store passwords \(see [Section 33.15](https://www.postgresql.org/docs/13/libpq-pgpass.html)\). Defaults to `~/.pgpass`, or `%APPDATA%\postgresql\pgpass.conf` on Microsoft Windows. \(No error is reported if this file does not exist.\)

`channel_binding`

This option controls the client's use of channel binding. A setting of `require` means that the connection must employ channel binding, `prefer` means that the client will choose channel binding if available, and `disable` prevents the use of channel binding. The default is `prefer` if PostgreSQL is compiled with SSL support; otherwise the default is `disable`.

Channel binding is a method for the server to authenticate itself to the client. It is only supported over SSL connections with PostgreSQL 11 or later servers using the `SCRAM` authentication method.

`connect_timeout`

Maximum time to wait while connecting, in seconds \(write as a decimal integer, e.g., `10`\). Zero, negative, or not specified means wait indefinitely. The minimum allowed timeout is 2 seconds, therefore a value of `1` is interpreted as `2`. This timeout applies separately to each host name or IP address. For example, if you specify two hosts and `connect_timeout` is 5, each host will time out if no connection is made within 5 seconds, so the total time spent waiting for a connection might be up to 10 seconds.

`client_encoding`

This sets the `client_encoding` configuration parameter for this connection. In addition to the values accepted by the corresponding server option, you can use `auto` to determine the right encoding from the current locale in the client \(`LC_CTYPE` environment variable on Unix systems\).

`options`

Specifies command-line options to send to the server at connection start. For example, setting this to `-c geqo=off` sets the session's value of the `geqo` parameter to `off`. Spaces within this string are considered to separate command-line arguments, unless escaped with a backslash \(`\`\); write `\\` to represent a literal backslash. For a detailed discussion of the available options, consult [Chapter 19](https://www.postgresql.org/docs/13/runtime-config.html).

`application_name`

Specifies a value for the [application\_name](https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-APPLICATION-NAME) configuration parameter.

`fallback_application_name`

Specifies a fallback value for the [application\_name](https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-APPLICATION-NAME) configuration parameter. This value will be used if no value has been given for `application_name` via a connection parameter or the `PGAPPNAME` environment variable. Specifying a fallback name is useful in generic utility programs that wish to set a default application name but allow it to be overridden by the user.

`keepalives`

Controls whether client-side TCP keepalives are used. The default value is 1, meaning on, but you can change this to 0, meaning off, if keepalives are not wanted. This parameter is ignored for connections made via a Unix-domain socket.

`keepalives_idle`

Controls the number of seconds of inactivity after which TCP should send a keepalive message to the server. A value of zero uses the system default. This parameter is ignored for connections made via a Unix-domain socket, or if keepalives are disabled. It is only supported on systems where `TCP_KEEPIDLE` or an equivalent socket option is available, and on Windows; on other systems, it has no effect.

`keepalives_interval`

Controls the number of seconds after which a TCP keepalive message that is not acknowledged by the server should be retransmitted. A value of zero uses the system default. This parameter is ignored for connections made via a Unix-domain socket, or if keepalives are disabled. It is only supported on systems where `TCP_KEEPINTVL` or an equivalent socket option is available, and on Windows; on other systems, it has no effect.

`keepalives_count`

Controls the number of TCP keepalives that can be lost before the client's connection to the server is considered dead. A value of zero uses the system default. This parameter is ignored for connections made via a Unix-domain socket, or if keepalives are disabled. It is only supported on systems where `TCP_KEEPCNT` or an equivalent socket option is available; on other systems, it has no effect.

`tcp_user_timeout`

Controls the number of milliseconds that transmitted data may remain unacknowledged before a connection is forcibly closed. A value of zero uses the system default. This parameter is ignored for connections made via a Unix-domain socket. It is only supported on systems where `TCP_USER_TIMEOUT` is available; on other systems, it has no effect.

`tty`

Ignored \(formerly, this specified where to send server debug output\).

`replication`

This option determines whether the connection should use the replication protocol instead of the normal protocol. This is what PostgreSQL replication connections as well as tools such as pg\_basebackup use internally, but it can also be used by third-party applications. For a description of the replication protocol, consult [Section 52.4](https://www.postgresql.org/docs/13/protocol-replication.html).

The following values, which are case-insensitive, are supported:

`true`, `on`, `yes`, `1`

The connection goes into physical replication mode.

`database`

The connection goes into logical replication mode, connecting to the database specified in the `dbname` parameter.

`false`, `off`, `no`, `0`

The connection is a regular one, which is the default behavior.

In physical or logical replication mode, only the simple query protocol can be used.

`gssencmode`

This option determines whether or with what priority a secure GSS TCP/IP connection will be negotiated with the server. There are three modes:

`disable`

only try a non-GSSAPI-encrypted connection

`prefer` \(default\)

if there are GSSAPI credentials present \(i.e., in a credentials cache\), first try a GSSAPI-encrypted connection; if that fails or there are no credentials, try a non-GSSAPI-encrypted connection. This is the default when PostgreSQL has been compiled with GSSAPI support.

`require`

only try a GSSAPI-encrypted connection

`gssencmode` is ignored for Unix domain socket communication. If PostgreSQL is compiled without GSSAPI support, using the `require` option will cause an error, while `prefer` will be accepted but libpq will not actually attempt a GSSAPI-encrypted connection.

`sslmode`

This option determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the server. There are six modes:

`disable`

only try a non-SSL connection

`allow`

first try a non-SSL connection; if that fails, try an SSL connection

`prefer` \(default\)

first try an SSL connection; if that fails, try a non-SSL connection

`require`

only try an SSL connection. If a root CA file is present, verify the certificate in the same way as if `verify-ca` was specified`verify-ca`

only try an SSL connection, and verify that the server certificate is issued by a trusted certificate authority \(CA\)

`verify-full`

only try an SSL connection, verify that the server certificate is issued by a trusted CA and that the requested server host name matches that in the certificate

See [Section 33.18](https://www.postgresql.org/docs/13/libpq-ssl.html) for a detailed description of how these options work.

`sslmode` is ignored for Unix domain socket communication. If PostgreSQL is compiled without SSL support, using options `require`, `verify-ca`, or `verify-full` will cause an error, while options `allow` and `prefer` will be accepted but libpq will not actually attempt an SSL connection.

Note that if GSSAPI encryption is possible, that will be used in preference to SSL encryption, regardless of the value of `sslmode`. To force use of SSL encryption in an environment that has working GSSAPI infrastructure \(such as a Kerberos server\), also set `gssencmode` to `disable`.

`requiressl`

This option is deprecated in favor of the `sslmode` setting.

If set to 1, an SSL connection to the server is required \(this is equivalent to `sslmode` `require`\). libpq will then refuse to connect if the server does not accept an SSL connection. If set to 0 \(default\), libpq will negotiate the connection type with the server \(equivalent to `sslmode` `prefer`\). This option is only available if PostgreSQL is compiled with SSL support.

`sslcompression`

If set to 1, data sent over SSL connections will be compressed. If set to 0, compression will be disabled. The default is 0. This parameter is ignored if a connection without SSL is made.

SSL compression is nowadays considered insecure and its use is no longer recommended. OpenSSL 1.1.0 disables compression by default, and many operating system distributions disable it in prior versions as well, so setting this parameter to on will not have any effect if the server does not accept compression.

If security is not a primary concern, compression can improve throughput if the network is the bottleneck. Disabling compression can improve response time and throughput if CPU performance is the limiting factor.

`sslcert`

This parameter specifies the file name of the client SSL certificate, replacing the default `~/.postgresql/postgresql.crt`. This parameter is ignored if an SSL connection is not made.`sslkey`

This parameter specifies the location for the secret key used for the client certificate. It can either specify a file name that will be used instead of the default `~/.postgresql/postgresql.key`, or it can specify a key obtained from an external “engine” \(engines are OpenSSL loadable modules\). An external engine specification should consist of a colon-separated engine name and an engine-specific key identifier. This parameter is ignored if an SSL connection is not made.`sslpassword`

This parameter specifies the password for the secret key specified in `sslkey`, allowing client certificate private keys to be stored in encrypted form on disk even when interactive passphrase input is not practical.

Specifying this parameter with any non-empty value suppresses the `Enter PEM pass phrase:` prompt that OpenSSL will emit by default when an encrypted client certificate key is provided to `libpq`.

If the key is not encrypted this parameter is ignored. The parameter has no effect on keys specified by OpenSSL engines unless the engine uses the OpenSSL password callback mechanism for prompts.

There is no environment variable equivalent to this option, and no facility for looking it up in `.pgpass`. It can be used in a service file connection definition. Users with more sophisticated uses should consider using openssl engines and tools like PKCS\#11 or USB crypto offload devices.

`sslrootcert`

This parameter specifies the name of a file containing SSL certificate authority \(CA\) certificate\(s\). If the file exists, the server's certificate will be verified to be signed by one of these authorities. The default is `~/.postgresql/root.crt`.

`sslcrl`

This parameter specifies the file name of the SSL certificate revocation list \(CRL\). Certificates listed in this file, if it exists, will be rejected while attempting to authenticate the server's certificate. The default is `~/.postgresql/root.crl`.

`requirepeer`

This parameter specifies the operating-system user name of the server, for example `requirepeer=postgres`. When making a Unix-domain socket connection, if this parameter is set, the client checks at the beginning of the connection that the server process is running under the specified user name; if it is not, the connection is aborted with an error. This parameter can be used to provide server authentication similar to that available with SSL certificates on TCP/IP connections. \(Note that if the Unix-domain socket is in `/tmp` or another publicly writable location, any user could start a server listening there. Use this parameter to ensure that you are connected to a server run by a trusted user.\) This option is only supported on platforms for which the `peer` authentication method is implemented; see [Section 20.9](https://www.postgresql.org/docs/13/auth-peer.html).

`ssl_min_protocol_version`

This parameter specifies the minimum SSL/TLS protocol version to allow for the connection. Valid values are `TLSv1`, `TLSv1.1`, `TLSv1.2` and `TLSv1.3`. The supported protocols depend on the version of OpenSSL used, older versions not supporting the most modern protocol versions. If not specified, the default is `TLSv1.2`, which satisfies industry best practices as of this writing.

`ssl_max_protocol_version`

This parameter specifies the maximum SSL/TLS protocol version to allow for the connection. Valid values are `TLSv1`, `TLSv1.1`, `TLSv1.2` and `TLSv1.3`. The supported protocols depend on the version of OpenSSL used, older versions not supporting the most modern protocol versions. If not set, this parameter is ignored and the connection will use the maximum bound defined by the backend, if set. Setting the maximum protocol version is mainly useful for testing or if some component has issues working with a newer protocol.

`krbsrvname`

Kerberos service name to use when authenticating with GSSAPI. This must match the service name specified in the server configuration for Kerberos authentication to succeed. \(See also [Section 20.6](https://www.postgresql.org/docs/13/gssapi-auth.html).\) The default value is normally `postgres`, but that can be changed when building PostgreSQL via the `--with-krb-srvnam` option of configure. In most environments, this parameter never needs to be changed. Some Kerberos implementations might require a different service name, such as Microsoft Active Directory which requires the service name to be in upper case \(`POSTGRES`\).`gsslib`

GSS library to use for GSSAPI authentication. Currently this is disregarded except on Windows builds that include both GSSAPI and SSPI support. In that case, set this to `gssapi` to cause libpq to use the GSSAPI library for authentication instead of the default SSPI.

`service`

Service name to use for additional parameters. It specifies a service name in `pg_service.conf` that holds additional connection parameters. This allows applications to specify only a service name so connection parameters can be centrally maintained. See [Section 33.16](https://www.postgresql.org/docs/13/libpq-pgservice.html).

`target_session_attrs`

If this parameter is set to `read-write`, only a connection in which read-write transactions are accepted by default is considered acceptable. The query `SHOW transaction_read_only` will be sent upon any successful connection; if it returns `on`, the connection will be closed. If multiple hosts were specified in the connection string, any remaining servers will be tried just as if the connection attempt had failed. The default value of this parameter, `any`, regards all connections as acceptable.

