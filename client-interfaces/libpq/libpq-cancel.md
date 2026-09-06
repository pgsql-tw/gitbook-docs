## 32.7. Canceling Queries in Progress [#](#LIBPQ-CANCEL)

[32.7.1. Functions for Sending Cancel Requests](libpq-cancel.md#LIBPQ-CANCEL-FUNCTIONS)

[32.7.2. Obsolete Functions for Sending Cancel Requests](libpq-cancel.md#LIBPQ-CANCEL-DEPRECATED)

<a id="id-1.7.3.14.2"></a><a id="id-1.7.3.14.3"></a><a id="LIBPQ-CANCEL-FUNCTIONS"></a>

### 32.7.1. Functions for Sending Cancel Requests [#](#LIBPQ-CANCEL-FUNCTIONS)

<a id="LIBPQ-PQCANCELCREATE"></a>

`PQcancelCreate`<a id="id-1.7.3.14.4.2.1.1.2"></a> [#](#LIBPQ-PQCANCELCREATE)
:   Prepares a connection over which a cancel request can be sent.

    ```

    PGcancelConn *PQcancelCreate(PGconn *conn);
    ```

    [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) creates a
    `PGcancelConn`<a id="id-1.7.3.14.4.2.1.2.2.3"></a>
    object, but it won't instantly start sending a cancel request over this
    connection. A cancel request can be sent over this connection in a
    blocking manner using [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) and in a
    non-blocking manner using [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART).
    The return value can be passed to [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS)
    to check if the `PGcancelConn` object was
    created successfully. The `PGcancelConn` object
    is an opaque structure that is not meant to be accessed directly by the
    application. This `PGcancelConn` object can be
    used to cancel the query that's running on the original connection in a
    thread-safe way.

    Many connection parameters of the original client will be reused when
    setting up the connection for the cancel request. Importantly, if the
    original connection requires encryption of the connection and/or
    verification of the target host (using `sslmode` or
    `gssencmode`), then the connection for the cancel
    request is made with these same requirements. Any connection options
    that are only used during authentication or after authentication of the
    client are ignored though, because cancellation requests do not require
    authentication and the connection is closed right after the cancellation
    request is submitted.

    Note that when `PQcancelCreate` returns a non-null
    pointer, you must call [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) when you
    are finished with it, in order to dispose of the structure and any
    associated memory blocks. This must be done even if the cancel request
    failed or was abandoned.
<a id="LIBPQ-PQCANCELBLOCKING"></a>

`PQcancelBlocking`<a id="id-1.7.3.14.4.2.2.1.2"></a> [#](#LIBPQ-PQCANCELBLOCKING)
:   Requests that the server abandons processing of the current command
    in a blocking manner.

    ```

    int PQcancelBlocking(PGcancelConn *cancelConn);
    ```

    The request is made over the given `PGcancelConn`,
    which needs to be created with [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE).
    The return value of [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)
    is 1 if the cancel request was successfully
    dispatched and 0 if not. If it was unsuccessful, the error message can be
    retrieved using [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE).

    Successful dispatch of the cancellation is no guarantee that the request
    will have any effect, however. If the cancellation is effective, the
    command being canceled will terminate early and return an error result.
    If the cancellation fails (say, because the server was already done
    processing the command), then there will be no visible result at all.
<a id="LIBPQ-PQCANCELSTART"></a>

`PQcancelStart`<a id="id-1.7.3.14.4.2.3.1.2"></a><br>`PQcancelPoll`<a id="id-1.7.3.14.4.2.3.2.2"></a> [#](#LIBPQ-PQCANCELSTART)
:   Requests that the server abandons processing of the current command
    in a non-blocking manner.

    ```

    int PQcancelStart(PGcancelConn *cancelConn);

    PostgresPollingStatusType PQcancelPoll(PGcancelConn *cancelConn);
    ```

    The request is made over the given `PGcancelConn`,
    which needs to be created with [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE).
    The return value of [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART)
    is 1 if the cancellation request could be started and 0 if not.
    If it was unsuccessful, the error message can be
    retrieved using [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE).

    If `PQcancelStart` succeeds, the next stage
    is to poll libpq so that it can proceed with
    the cancel connection sequence.
    Use [`PQcancelSocket`](libpq-cancel.md#LIBPQ-PQCANCELSOCKET) to obtain the descriptor of the
    socket underlying the database connection.
    (Caution: do not assume that the socket remains the same
    across `PQcancelPoll` calls.)
    Loop thus: If `PQcancelPoll(cancelConn)` last returned
    `PGRES_POLLING_READING`, wait until the socket is ready to
    read (as indicated by `select()`,
    `poll()`, or similar system function).
    Then call `PQcancelPoll(cancelConn)` again.
    Conversely, if `PQcancelPoll(cancelConn)` last returned
    `PGRES_POLLING_WRITING`, wait until the socket is ready
    to write, then call `PQcancelPoll(cancelConn)` again.
    On the first iteration, i.e., if you have yet to call
    `PQcancelPoll(cancelConn)`, behave as if it last returned
    `PGRES_POLLING_WRITING`. Continue this loop until
    `PQcancelPoll(cancelConn)` returns
    `PGRES_POLLING_FAILED`, indicating the connection procedure
    has failed, or `PGRES_POLLING_OK`, indicating cancel
    request was successfully dispatched.

    Successful dispatch of the cancellation is no guarantee that the request
    will have any effect, however. If the cancellation is effective, the
    command being canceled will terminate early and return an error result.
    If the cancellation fails (say, because the server was already done
    processing the command), then there will be no visible result at all.

    At any time during connection, the status of the connection can be
    checked by calling [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS).
    If this call returns `CONNECTION_BAD`, then
    the cancel procedure has failed; if the call returns
    `CONNECTION_OK`, then cancel request was
    successfully dispatched.
    Both of these states are equally detectable from the return value of
    `PQcancelPoll`, described above.
    Other states might also occur during (and only during) an asynchronous
    connection procedure.
    These indicate the current stage of the connection procedure and might
    be useful to provide feedback to the user for example.
    These statuses are:

    <a id="LIBPQ-CANCEL-CONNECTION-ALLOCATED"></a>

    `CONNECTION_ALLOCATED` [#](#LIBPQ-CANCEL-CONNECTION-ALLOCATED)
    :   Waiting for a call to [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) or
        [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING), to actually open the
        socket. This is the connection state right after
        calling [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE)
        or [`PQcancelReset`](libpq-cancel.md#LIBPQ-PQCANCELRESET). No connection to the
        server has been initiated yet at this point. To actually start
        sending the cancel request use [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) or
        [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).
    <a id="LIBPQ-CANCEL-CONNECTION-STARTED"></a>

    `CONNECTION_STARTED` [#](#LIBPQ-CANCEL-CONNECTION-STARTED)
    :   Waiting for connection to be made.
    <a id="LIBPQ-CANCEL-CONNECTION-MADE"></a>

    `CONNECTION_MADE` [#](#LIBPQ-CANCEL-CONNECTION-MADE)
    :   Connection OK; waiting to send.
    <a id="LIBPQ-CANCEL-CONNECTION-AWAITING-RESPONSE"></a>

    `CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CANCEL-CONNECTION-AWAITING-RESPONSE)
    :   Waiting for a response from the server.
    <a id="LIBPQ-CANCEL-CONNECTION-SSL-STARTUP"></a>

    `CONNECTION_SSL_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-SSL-STARTUP)
    :   Negotiating SSL encryption.
    <a id="LIBPQ-CANCEL-CONNECTION-GSS-STARTUP"></a>

    `CONNECTION_GSS_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-GSS-STARTUP)
    :   Negotiating GSS encryption.

    Note that, although these constants will remain (in order to maintain
    compatibility), an application should never rely upon these occurring in a
    particular order, or at all, or on the status always being one of these
    documented values. An application might do something like this:

    ```

    switch(PQcancelStatus(conn))
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

    The `connect_timeout` connection parameter is ignored
    when using `PQcancelPoll`; it is the application's
    responsibility to decide whether an excessive amount of time has elapsed.
    Otherwise, `PQcancelStart` followed by a
    `PQcancelPoll` loop is equivalent to
    [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).
<a id="LIBPQ-PQCANCELSTATUS"></a>

`PQcancelStatus`<a id="id-1.7.3.14.4.2.4.1.2"></a> [#](#LIBPQ-PQCANCELSTATUS)
:   Returns the status of the cancel connection.

    ```

    ConnStatusType PQcancelStatus(const PGcancelConn *cancelConn);
    ```

    The status can be one of a number of values. However, only three of
    these are seen outside of an asynchronous cancel procedure:
    `CONNECTION_ALLOCATED`,
    `CONNECTION_OK` and
    `CONNECTION_BAD`. The initial state of a
    `PGcancelConn` that's successfully created using
    [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) is `CONNECTION_ALLOCATED`.
    A cancel request that was successfully dispatched
    has the status `CONNECTION_OK`. A failed
    cancel attempt is signaled by status
    `CONNECTION_BAD`. An OK status will
    remain so until [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) or
    [`PQcancelReset`](libpq-cancel.md#LIBPQ-PQCANCELRESET) is called.

    See the entry for [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) with regards
    to other status codes that might be returned.

    Successful dispatch of the cancellation is no guarantee that the request
    will have any effect, however. If the cancellation is effective, the
    command being canceled will terminate early and return an error result.
    If the cancellation fails (say, because the server was already done
    processing the command), then there will be no visible result at all.
<a id="LIBPQ-PQCANCELSOCKET"></a>

`PQcancelSocket`<a id="id-1.7.3.14.4.2.5.1.2"></a> [#](#LIBPQ-PQCANCELSOCKET)
:   Obtains the file descriptor number of the cancel connection socket to
    the server.

    ```

    int PQcancelSocket(const PGcancelConn *cancelConn);
    ```

    A valid descriptor will be greater than or equal to 0;
    a result of -1 indicates that no server connection is currently open.
    This might change as a result of calling any of the functions
    in this section on the `PGcancelConn`
    (except for [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) and
    `PQcancelSocket` itself).
<a id="LIBPQ-PQCANCELERRORMESSAGE"></a>

`PQcancelErrorMessage`<a id="id-1.7.3.14.4.2.6.1.2"></a> <a id="id-1.7.3.14.4.2.6.1.3"></a> [#](#LIBPQ-PQCANCELERRORMESSAGE)
:   Returns the error message most recently generated by an
    operation on the cancel connection.

    ```

    char *PQcancelErrorMessage(const PGcancelConn *cancelconn);
    ```

    Nearly all libpq functions that take a
    `PGcancelConn` will set a message for
    [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) if they fail.
    Note that by libpq convention,
    a nonempty [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) result
    can consist of multiple lines, and will include a trailing newline.
    The caller should not free the result directly.
    It will be freed when the associated
    `PGcancelConn` handle is passed to
    [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH). The result string should not be
    expected to remain the same across operations on the
    `PGcancelConn` structure.
<a id="LIBPQ-PQCANCELFINISH"></a>

`PQcancelFinish`<a id="id-1.7.3.14.4.2.7.1.2"></a> [#](#LIBPQ-PQCANCELFINISH)
:   Closes the cancel connection (if it did not finish sending the
    cancel request yet). Also frees memory used by the
    `PGcancelConn` object.

    ```

    void PQcancelFinish(PGcancelConn *cancelConn);
    ```

    Note that even if the cancel attempt fails (as
    indicated by [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS)), the
    application should call [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH)
    to free the memory used by the `PGcancelConn`
    object.
    The `PGcancelConn` pointer must not be used
    again after [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) has been called.
<a id="LIBPQ-PQCANCELRESET"></a>

`PQcancelReset`<a id="id-1.7.3.14.4.2.8.1.2"></a> [#](#LIBPQ-PQCANCELRESET)
:   Resets the `PGcancelConn` so it can be reused for a new
    cancel connection.

    ```

    void PQcancelReset(PGcancelConn *cancelConn);
    ```

    If the `PGcancelConn` is currently used to send a cancel
    request, then this connection is closed. It will then prepare the
    `PGcancelConn` object such that it can be used to send a
    new cancel request.

    This can be used to create one `PGcancelConn`
    for a `PGconn` and reuse it multiple times
    throughout the lifetime of the original `PGconn`.

<a id="LIBPQ-CANCEL-DEPRECATED"></a>

### 32.7.2. Obsolete Functions for Sending Cancel Requests [#](#LIBPQ-CANCEL-DEPRECATED)

These functions represent older methods of sending cancel requests.
Although they still work, they are deprecated due to not sending the cancel
requests in an encrypted manner, even when the original connection
specified `sslmode` or `gssencmode` to
require encryption. Thus these older methods are heavily discouraged from
being used in new code, and it is recommended to change existing code to
use the new functions instead.

<a id="LIBPQ-PQGETCANCEL"></a>

`PQgetCancel`<a id="id-1.7.3.14.5.3.1.1.2"></a> [#](#LIBPQ-PQGETCANCEL)
:   Creates a data structure containing the information needed to cancel
    a command using [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL).

    ```

    PGcancel *PQgetCancel(PGconn *conn);
    ```

    [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL) creates a
    `PGcancel`<a id="id-1.7.3.14.5.3.1.2.2.3"></a>
    object given a `PGconn` connection object.
    It will return `NULL` if the given *`conn`*
    is `NULL` or an invalid connection.
    The `PGcancel` object is an opaque
    structure that is not meant to be accessed directly by the
    application; it can only be passed to [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL)
    or [`PQfreeCancel`](libpq-cancel.md#LIBPQ-PQFREECANCEL).
<a id="LIBPQ-PQFREECANCEL"></a>

`PQfreeCancel`<a id="id-1.7.3.14.5.3.2.1.2"></a> [#](#LIBPQ-PQFREECANCEL)
:   Frees a data structure created by [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL).

    ```

    void PQfreeCancel(PGcancel *cancel);
    ```

    [`PQfreeCancel`](libpq-cancel.md#LIBPQ-PQFREECANCEL) frees a data object previously created
    by [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL).
<a id="LIBPQ-PQCANCEL"></a>

`PQcancel`<a id="id-1.7.3.14.5.3.3.1.2"></a> [#](#LIBPQ-PQCANCEL)
:   [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) is a deprecated and insecure
    variant of [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING), but one that can be
    used safely from within a signal handler.

    ```

    int PQcancel(PGcancel *cancel, char *errbuf, int errbufsize);
    ```

    [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) only exists because of backwards
    compatibility reasons. [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) should be
    used instead. The only benefit that [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) has
    is that it can be safely invoked from a signal handler, if the
    *`errbuf`* is a local variable in the signal handler.
    However, this is generally not considered a big enough benefit to be
    worth the security issues that this function has.

    The `PGcancel` object is read-only as far as
    [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) is concerned, so it can also be invoked
    from a thread that is separate from the one manipulating the
    `PGconn` object.

    The return value of [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) is 1 if the
    cancel request was successfully dispatched and 0 if not.
    If not, *`errbuf`* is filled with an explanatory
    error message.
    *`errbuf`* must be a char array of size
    *`errbufsize`* (the recommended size is 256 bytes).

<a id="LIBPQ-PQREQUESTCANCEL"></a>

`PQrequestCancel`<a id="id-1.7.3.14.5.4.1.1.2"></a> [#](#LIBPQ-PQREQUESTCANCEL)
:   [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) is a deprecated and insecure
    variant of [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).

    ```

    int PQrequestCancel(PGconn *conn);
    ```

    [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) only exists because of backwards
    compatibility reasons. [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) should be
    used instead. There is no benefit to using
    [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) over
    [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).

    Requests that the server abandon processing of the current
    command. It operates directly on the
    `PGconn` object, and in case of failure stores the
    error message in the `PGconn` object (whence it can
    be retrieved by [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE)). Although
    the functionality is the same, this approach is not safe within
    multiple-thread programs or signal handlers, since it is possible
    that overwriting the `PGconn`'s error message will
    mess up the operation currently in progress on the connection.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-cancel.html)（英文原文，待翻譯）
