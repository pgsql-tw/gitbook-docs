## 32.12. Miscellaneous Functions [#](#LIBPQ-MISC)

As always, there are some functions that just don't fit anywhere.

<a id="LIBPQ-PQFREEMEM"></a>

`PQfreemem`<a id="id-1.7.3.19.3.1.1.2"></a> [#](#LIBPQ-PQFREEMEM)
:   Frees memory allocated by libpq.

    ```

    void PQfreemem(void *ptr);
    ```

    Frees memory allocated by libpq, particularly
    [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN),
    [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA),
    [`PQunescapeBytea`](libpq-exec.md#LIBPQ-PQUNESCAPEBYTEA),
    and `PQnotifies`.
    It is particularly important that this function, rather than
    `free()`, be used on Microsoft Windows. This is because
    allocating memory in a DLL and releasing it in the application works
    only if multithreaded/single-threaded, release/debug, and static/dynamic
    flags are the same for the DLL and the application. On non-Microsoft
    Windows platforms, this function is the same as the standard library
    function `free()`.
<a id="LIBPQ-PQCONNINFOFREE"></a>

`PQconninfoFree`<a id="id-1.7.3.19.3.2.1.2"></a> [#](#LIBPQ-PQCONNINFOFREE)
:   Frees the data structures allocated by
    [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS) or [`PQconninfoParse`](libpq-connect.md#LIBPQ-PQCONNINFOPARSE).

    ```

    void PQconninfoFree(PQconninfoOption *connOptions);
    ```

    If the argument is a `NULL` pointer, no operation is
    performed.

    A simple [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) will not do for this, since
    the array contains references to subsidiary strings.
<a id="LIBPQ-PQENCRYPTPASSWORDCONN"></a>

`PQencryptPasswordConn`<a id="id-1.7.3.19.3.3.1.2"></a> [#](#LIBPQ-PQENCRYPTPASSWORDCONN)
:   Prepares the encrypted form of a PostgreSQL password.

    ```

    char *PQencryptPasswordConn(PGconn *conn, const char *passwd, const char *user, const char *algorithm);
    ```

    This function is intended to be used by client applications that
    wish to send commands like `ALTER USER joe PASSWORD
    'pwd'`. It is good practice not to send the original cleartext
    password in such a command, because it might be exposed in command
    logs, activity displays, and so on. Instead, use this function to
    convert the password to encrypted form before it is sent.

    The *`passwd`* and *`user`* arguments
    are the cleartext password, and the SQL name of the user it is for.
    *`algorithm`* specifies the encryption algorithm
    to use to encrypt the password. Currently supported algorithms are
    `md5` and `scram-sha-256` (`on` and
    `off` are also accepted as aliases for `md5`, for
    compatibility with older server versions). Note that support for
    `scram-sha-256` was introduced in PostgreSQL
    version 10, and will not work correctly with older server versions. If
    *`algorithm`* is `NULL`, this function will query
    the server for the current value of the
    [password_encryption](../../server-administration/runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION) setting. That can block, and
    will fail if the current transaction is aborted, or if the connection
    is busy executing another query. If you wish to use the default
    algorithm for the server but want to avoid blocking, query
    `password_encryption` yourself before calling
    [`PQencryptPasswordConn`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORDCONN), and pass that value as the
    *`algorithm`*.

    The return value is a string allocated by `malloc`.
    The caller can assume the string doesn't contain any special characters
    that would require escaping. Use [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) to free the
    result when done with it. On error, returns `NULL`, and
    a suitable message is stored in the connection object.
<a id="LIBPQ-PQCHANGEPASSWORD"></a>

`PQchangePassword`<a id="id-1.7.3.19.3.4.1.2"></a> [#](#LIBPQ-PQCHANGEPASSWORD)
:   Changes a PostgreSQL password.

    ```

    PGresult *PQchangePassword(PGconn *conn, const char *user, const char *passwd);
    ```

    This function uses `PQencryptPasswordConn`
    to build and execute the command `ALTER USER ... PASSWORD
    '...'`, thereby changing the user's password. It exists for
    the same reason as `PQencryptPasswordConn`, but
    is more convenient as it both builds and runs the command for you.
    [`PQencryptPasswordConn`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORDCONN) is passed a
    `NULL` for the algorithm argument, hence encryption is
    done according to the server's [password_encryption](../../server-administration/runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION)
    setting.

    The *`user`* and *`passwd`* arguments
    are the SQL name of the target user, and the new cleartext password.

    Returns a `PGresult` pointer representing
    the result of the `ALTER USER` command, or
    a null pointer if the routine failed before issuing any command.
    The [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) function should be called
    to check the return value for any errors (including the value of a null
    pointer, in which case it will return
    `PGRES_FATAL_ERROR`). Use
    [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) to get more information about
    such errors.
<a id="LIBPQ-PQENCRYPTPASSWORD"></a>

`PQencryptPassword`<a id="id-1.7.3.19.3.5.1.2"></a> [#](#LIBPQ-PQENCRYPTPASSWORD)
:   Prepares the md5-encrypted form of a PostgreSQL password.

    ```

    char *PQencryptPassword(const char *passwd, const char *user);
    ```

    [`PQencryptPassword`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORD) is an older, deprecated version of
    [`PQencryptPasswordConn`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORDCONN). The difference is that
    [`PQencryptPassword`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORD) does not
    require a connection object, and `md5` is always used as the
    encryption algorithm.
<a id="LIBPQ-PQMAKEEMPTYPGRESULT"></a>

`PQmakeEmptyPGresult`<a id="id-1.7.3.19.3.6.1.2"></a> [#](#LIBPQ-PQMAKEEMPTYPGRESULT)
:   Constructs an empty `PGresult` object with the given status.

    ```

    PGresult *PQmakeEmptyPGresult(PGconn *conn, ExecStatusType status);
    ```

    This is libpq's internal function to allocate and
    initialize an empty `PGresult` object. This
    function returns `NULL` if memory could not be allocated. It is
    exported because some applications find it useful to generate result
    objects (particularly objects with error status) themselves. If
    *`conn`* is not null and *`status`*
    indicates an error, the current error message of the specified
    connection is copied into the `PGresult`.
    Also, if *`conn`* is not null, any event procedures
    registered in the connection are copied into the
    `PGresult`. (They do not get
    `PGEVT_RESULTCREATE` calls, but see
    [`PQfireResultCreateEvents`](libpq-misc.md#LIBPQ-PQFIRERESULTCREATEEVENTS).)
    Note that [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) should eventually be called
    on the object, just as with a `PGresult`
    returned by libpq itself.
<a id="LIBPQ-PQFIRERESULTCREATEEVENTS"></a>

`PQfireResultCreateEvents`<a id="id-1.7.3.19.3.7.1.2"></a> [#](#LIBPQ-PQFIRERESULTCREATEEVENTS)
:   Fires a `PGEVT_RESULTCREATE` event (see [Section 32.14](libpq-events.md)) for each event procedure registered in the
    `PGresult` object. Returns non-zero for success,
    zero if any event procedure fails.

    ```

    int PQfireResultCreateEvents(PGconn *conn, PGresult *res);
    ```

    The `conn` argument is passed through to event procedures
    but not used directly. It can be `NULL` if the event
    procedures won't use it.

    Event procedures that have already received a
    `PGEVT_RESULTCREATE` or `PGEVT_RESULTCOPY` event
    for this object are not fired again.

    The main reason that this function is separate from
    [`PQmakeEmptyPGresult`](libpq-misc.md#LIBPQ-PQMAKEEMPTYPGRESULT) is that it is often appropriate
    to create a `PGresult` and fill it with data
    before invoking the event procedures.
<a id="LIBPQ-PQCOPYRESULT"></a>

`PQcopyResult`<a id="id-1.7.3.19.3.8.1.2"></a> [#](#LIBPQ-PQCOPYRESULT)
:   Makes a copy of a `PGresult` object. The copy is
    not linked to the source result in any way and
    [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) must be called when the copy is no longer
    needed. If the function fails, `NULL` is returned.

    ```

    PGresult *PQcopyResult(const PGresult *src, int flags);
    ```

    This is not intended to make an exact copy. The returned result is
    always put into `PGRES_TUPLES_OK` status, and does not
    copy any error message in the source. (It does copy the command status
    string, however.) The *`flags`* argument determines
    what else is copied. It is a bitwise OR of several flags.
    `PG_COPYRES_ATTRS` specifies copying the source
    result's attributes (column definitions).
    `PG_COPYRES_TUPLES` specifies copying the source
    result's tuples. (This implies copying the attributes, too.)
    `PG_COPYRES_NOTICEHOOKS` specifies
    copying the source result's notify hooks.
    `PG_COPYRES_EVENTS` specifies copying the source
    result's events. (But any instance data associated with the source
    is not copied.)
    The event procedures receive `PGEVT_RESULTCOPY` events.
<a id="LIBPQ-PQSETRESULTATTRS"></a>

`PQsetResultAttrs`<a id="id-1.7.3.19.3.9.1.2"></a> [#](#LIBPQ-PQSETRESULTATTRS)
:   Sets the attributes of a `PGresult` object.

    ```

    int PQsetResultAttrs(PGresult *res, int numAttributes, PGresAttDesc *attDescs);
    ```

    The provided *`attDescs`* are copied into the result.
    If the *`attDescs`* pointer is `NULL` or
    *`numAttributes`* is less than one, the request is
    ignored and the function succeeds. If *`res`*
    already contains attributes, the function will fail. If the function
    fails, the return value is zero. If the function succeeds, the return
    value is non-zero.
<a id="LIBPQ-PQSETVALUE"></a>

`PQsetvalue`<a id="id-1.7.3.19.3.10.1.2"></a> [#](#LIBPQ-PQSETVALUE)
:   Sets a tuple field value of a `PGresult` object.

    ```

    int PQsetvalue(PGresult *res, int tup_num, int field_num, char *value, int len);
    ```

    The function will automatically grow the result's internal tuples array
    as needed. However, the *`tup_num`* argument must be
    less than or equal to [`PQntuples`](libpq-exec.md#LIBPQ-PQNTUPLES), meaning this
    function can only grow the tuples array one tuple at a time. But any
    field of any existing tuple can be modified in any order. If a value at
    *`field_num`* already exists, it will be overwritten.
    If *`len`* is -1 or
    *`value`* is `NULL`, the field value
    will be set to an SQL null value. The
    *`value`* is copied into the result's private storage,
    thus is no longer needed after the function
    returns. If the function fails, the return value is zero. If the
    function succeeds, the return value is non-zero.
<a id="LIBPQ-PQRESULTALLOC"></a>

`PQresultAlloc`<a id="id-1.7.3.19.3.11.1.2"></a> [#](#LIBPQ-PQRESULTALLOC)
:   Allocate subsidiary storage for a `PGresult` object.

    ```

    void *PQresultAlloc(PGresult *res, size_t nBytes);
    ```

    Any memory allocated with this function will be freed when
    *`res`* is cleared. If the function fails,
    the return value is `NULL`. The result is
    guaranteed to be adequately aligned for any type of data,
    just as for `malloc`.
<a id="LIBPQ-PQRESULTMEMORYSIZE"></a>

`PQresultMemorySize`<a id="id-1.7.3.19.3.12.1.2"></a> [#](#LIBPQ-PQRESULTMEMORYSIZE)
:   Retrieves the number of bytes allocated for
    a `PGresult` object.

    ```

    size_t PQresultMemorySize(const PGresult *res);
    ```

    This value is the sum of all `malloc` requests
    associated with the `PGresult` object, that is,
    all the memory that will be freed by [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR).
    This information can be useful for managing memory consumption.
<a id="LIBPQ-PQLIBVERSION"></a>

`PQlibVersion`<a id="id-1.7.3.19.3.13.1.2"></a> [#](#LIBPQ-PQLIBVERSION)
:   Return the version of libpq that is being used.

    ```

    int PQlibVersion(void);
    ```

    The result of this function can be used to determine, at
    run time, whether specific functionality is available in the currently
    loaded version of libpq. The function can be used, for example,
    to determine which connection options are available in
    [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB).

    The result is formed by multiplying the library's major version
    number by 10000 and adding the minor version number. For example,
    version 10.1 will be returned as 100001, and version 11.0 will be
    returned as 110000.

    Prior to major version 10, PostgreSQL used
    three-part version numbers in which the first two parts together
    represented the major version. For those
    versions, [`PQlibVersion`](libpq-misc.md#LIBPQ-PQLIBVERSION) uses two digits for each
    part; for example version 9.1.5 will be returned as 90105, and
    version 9.2.0 will be returned as 90200.

    Therefore, for purposes of determining feature compatibility,
    applications should divide the result of [`PQlibVersion`](libpq-misc.md#LIBPQ-PQLIBVERSION)
    by 100 not 10000 to determine a logical major version number.
    In all release series, only the last two digits differ between
    minor releases (bug-fix releases).

    ### Note

    This function appeared in PostgreSQL version 9.1, so
    it cannot be used to detect required functionality in earlier
    versions, since calling it will create a link dependency
    on version 9.1 or later.
<a id="LIBPQ-PQGETCURRENTTIMEUSEC"></a>

`PQgetCurrentTimeUSec`<a id="id-1.7.3.19.3.14.1.2"></a> [#](#LIBPQ-PQGETCURRENTTIMEUSEC)
:   Retrieves the current time, expressed as the number of microseconds
    since the Unix epoch (that is, `time_t` times 1 million).

    ```

    pg_usec_time_t PQgetCurrentTimeUSec(void);
    ```

    This is primarily useful for calculating timeout values to use with
    [`PQsocketPoll`](libpq-connect.md#LIBPQ-PQSOCKETPOLL).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-misc.html)（英文原文，待翻譯）
