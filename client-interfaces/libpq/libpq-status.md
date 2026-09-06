## 32.2. Connection Status Functions [#](#LIBPQ-STATUS)

These functions can be used to interrogate the status
of an existing database connection object.

### Tip

<a id="id-1.7.3.9.3.1.1"></a>
<a id="id-1.7.3.9.3.1.2"></a>
libpq application programmers should be careful to
maintain the `PGconn` abstraction. Use the accessor
functions described below to get at the contents of `PGconn`.
Reference to internal `PGconn` fields using
`libpq-int.h` is not recommended because they are subject to change
in the future.

The following functions return parameter values established at connection.
These values are fixed for the life of the connection. If a multi-host
connection string is used, the values of [`PQhost`](libpq-status.md#LIBPQ-PQHOST),
[`PQport`](libpq-status.md#LIBPQ-PQPORT), and [`PQpass`](libpq-status.md#LIBPQ-PQPASS) can change if a new connection
is established using the same `PGconn` object. Other values
are fixed for the lifetime of the `PGconn` object.

<a id="LIBPQ-PQDB"></a>

`PQdb`<a id="id-1.7.3.9.4.6.1.1.2"></a> [#](#LIBPQ-PQDB)
:   Returns the database name of the connection.

    ```

    char *PQdb(const PGconn *conn);
    ```
<a id="LIBPQ-PQUSER"></a>

`PQuser`<a id="id-1.7.3.9.4.6.2.1.2"></a> [#](#LIBPQ-PQUSER)
:   Returns the user name of the connection.

    ```

    char *PQuser(const PGconn *conn);
    ```
<a id="LIBPQ-PQPASS"></a>

`PQpass`<a id="id-1.7.3.9.4.6.3.1.2"></a> [#](#LIBPQ-PQPASS)
:   Returns the password of the connection.

    ```

    char *PQpass(const PGconn *conn);
    ```

    [`PQpass`](libpq-status.md#LIBPQ-PQPASS) will return either the password specified
    in the connection parameters, or if there was none and the password
    was obtained from the [password
    file](libpq-pgpass.md), it will return that. In the latter case,
    if multiple hosts were specified in the connection parameters, it is
    not possible to rely on the result of [`PQpass`](libpq-status.md#LIBPQ-PQPASS) until
    the connection is established. The status of the connection can be
    checked using the function [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS).
<a id="LIBPQ-PQHOST"></a>

`PQhost`<a id="id-1.7.3.9.4.6.4.1.2"></a> [#](#LIBPQ-PQHOST)
:   Returns the server host name of the active connection.
    This can be a host name, an IP address, or a directory path if the
    connection is via Unix socket. (The path case can be distinguished
    because it will always be an absolute path, beginning
    with `/`.)

    ```

    char *PQhost(const PGconn *conn);
    ```

    If the connection parameters specified both `host` and
    `hostaddr`, then [`PQhost`](libpq-status.md#LIBPQ-PQHOST) will
    return the `host` information. If only
    `hostaddr` was specified, then that is returned.
    If multiple hosts were specified in the connection parameters,
    [`PQhost`](libpq-status.md#LIBPQ-PQHOST) returns the host actually connected to.

    [`PQhost`](libpq-status.md#LIBPQ-PQHOST) returns `NULL` if the
    *`conn`* argument is `NULL`.
    Otherwise, if there is an error producing the host information (perhaps
    if the connection has not been fully established or there was an
    error), it returns an empty string.

    If multiple hosts were specified in the connection parameters, it is
    not possible to rely on the result of [`PQhost`](libpq-status.md#LIBPQ-PQHOST) until
    the connection is established. The status of the connection can be
    checked using the function [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS).
<a id="LIBPQ-PQHOSTADDR"></a>

`PQhostaddr`<a id="id-1.7.3.9.4.6.5.1.2"></a> [#](#LIBPQ-PQHOSTADDR)
:   Returns the server IP address of the active connection.
    This can be the address that a host name resolved to,
    or an IP address provided through the `hostaddr`
    parameter.

    ```

    char *PQhostaddr(const PGconn *conn);
    ```

    [`PQhostaddr`](libpq-status.md#LIBPQ-PQHOSTADDR) returns `NULL` if the
    *`conn`* argument is `NULL`.
    Otherwise, if there is an error producing the host information
    (perhaps if the connection has not been fully established or
    there was an error), it returns an empty string.
<a id="LIBPQ-PQPORT"></a>

`PQport`<a id="id-1.7.3.9.4.6.6.1.2"></a> [#](#LIBPQ-PQPORT)
:   Returns the port of the active connection.

    ```

    char *PQport(const PGconn *conn);
    ```

    If multiple ports were specified in the connection parameters,
    [`PQport`](libpq-status.md#LIBPQ-PQPORT) returns the port actually connected to.

    [`PQport`](libpq-status.md#LIBPQ-PQPORT) returns `NULL` if the
    *`conn`* argument is `NULL`.
    Otherwise, if there is an error producing the port information (perhaps
    if the connection has not been fully established or there was an
    error), it returns an empty string.

    If multiple ports were specified in the connection parameters, it is
    not possible to rely on the result of [`PQport`](libpq-status.md#LIBPQ-PQPORT) until
    the connection is established. The status of the connection can be
    checked using the function [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS).
<a id="LIBPQ-PQTTY"></a>

`PQtty`<a id="id-1.7.3.9.4.6.7.1.2"></a> [#](#LIBPQ-PQTTY)
:   This function no longer does anything, but it remains for backwards
    compatibility. The function always return an empty string, or
    `NULL` if the *`conn`* argument is
    `NULL`.

    ```

    char *PQtty(const PGconn *conn);
    ```
<a id="LIBPQ-PQOPTIONS"></a>

`PQoptions`<a id="id-1.7.3.9.4.6.8.1.2"></a> [#](#LIBPQ-PQOPTIONS)
:   Returns the command-line options passed in the connection request.

    ```

    char *PQoptions(const PGconn *conn);
    ```

The following functions return status data that can change as operations
are executed on the `PGconn` object.

<a id="LIBPQ-PQSTATUS"></a>

`PQstatus`<a id="id-1.7.3.9.5.2.1.1.2"></a> [#](#LIBPQ-PQSTATUS)
:   Returns the status of the connection.

    ```

    ConnStatusType PQstatus(const PGconn *conn);
    ```

    The status can be one of a number of values. However, only two of
    these are seen outside of an asynchronous connection procedure:
    `CONNECTION_OK` and
    `CONNECTION_BAD`. A good connection to the database
    has the status `CONNECTION_OK`. A failed
    connection attempt is signaled by status
    `CONNECTION_BAD`. Ordinarily, an OK status will
    remain so until [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH), but a communications
    failure might result in the status changing to
    `CONNECTION_BAD` prematurely. In that case the
    application could try to recover by calling
    [`PQreset`](libpq-connect.md#LIBPQ-PQRESET).

    See the entry for [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS), `PQconnectStart`
    and `PQconnectPoll` with regards to other status codes that
    might be returned.
<a id="LIBPQ-PQTRANSACTIONSTATUS"></a>

`PQtransactionStatus`<a id="id-1.7.3.9.5.2.2.1.2"></a> [#](#LIBPQ-PQTRANSACTIONSTATUS)
:   Returns the current in-transaction status of the server.

    ```

    PGTransactionStatusType PQtransactionStatus(const PGconn *conn);
    ```

    The status can be `PQTRANS_IDLE` (currently idle),
    `PQTRANS_ACTIVE` (a command is in progress),
    `PQTRANS_INTRANS` (idle, in a valid transaction block),
    or `PQTRANS_INERROR` (idle, in a failed transaction block).
    `PQTRANS_UNKNOWN` is reported if the connection is bad.
    `PQTRANS_ACTIVE` is reported only when a query
    has been sent to the server and not yet completed.
<a id="LIBPQ-PQPARAMETERSTATUS"></a>

`PQparameterStatus`<a id="id-1.7.3.9.5.2.3.1.2"></a> [#](#LIBPQ-PQPARAMETERSTATUS)
:   Looks up a current parameter setting of the server.

    ```

    const char *PQparameterStatus(const PGconn *conn, const char *paramName);
    ```

    Certain parameter values are reported by the server automatically at
    connection startup or whenever their values change.
    [`PQparameterStatus`](libpq-status.md#LIBPQ-PQPARAMETERSTATUS) can be used to interrogate these settings.
    It returns the current value of a parameter if known, or `NULL`
    if the parameter is not known.

    Parameters reported as of the current release include:

    <table border="0" class="simplelist" summary="Simple list"><tr><td><code class="varname">application_name</code></td><td><code class="varname">scram_iterations</code></td></tr><tr><td><code class="varname">client_encoding</code></td><td><code class="varname">search_path</code></td></tr><tr><td><code class="varname">DateStyle</code></td><td><code class="varname">server_encoding</code></td></tr><tr><td><code class="varname">default_transaction_read_only</code></td><td><code class="varname">server_version</code></td></tr><tr><td><code class="varname">in_hot_standby</code></td><td><code class="varname">session_authorization</code></td></tr><tr><td><code class="varname">integer_datetimes</code></td><td><code class="varname">standard_conforming_strings</code></td></tr><tr><td><code class="varname">IntervalStyle</code></td><td><code class="varname">TimeZone</code></td></tr><tr><td><code class="varname">is_superuser</code></td><td> </td></tr></table>

    (`default_transaction_read_only` and
    `in_hot_standby` were not reported by releases before
    14; `scram_iterations` was not reported by releases
    before 16; `search_path` was not reported by releases
    before 18.)
    Note that
    `server_version`,
    `server_encoding` and
    `integer_datetimes`
    cannot change after startup.

    If no value for `standard_conforming_strings` is reported,
    applications can assume it is `off`, that is, backslashes
    are treated as escapes in string literals. Also, the presence of
    this parameter can be taken as an indication that the escape string
    syntax (`E'...'`) is accepted.

    Although the returned pointer is declared `const`, it in fact
    points to mutable storage associated with the `PGconn` structure.
    It is unwise to assume the pointer will remain valid across queries.
<a id="LIBPQ-PQFULLPROTOCOLVERSION"></a>

`PQfullProtocolVersion`<a id="id-1.7.3.9.5.2.4.1.2"></a> [#](#LIBPQ-PQFULLPROTOCOLVERSION)
:   Interrogates the frontend/backend protocol being used.

    ```

    int PQfullProtocolVersion(const PGconn *conn);
    ```

    Applications might wish to use this function to determine whether certain
    features are supported. The result is formed by multiplying the server's
    major version number by 10000 and adding the minor version number. For
    example, version 3.2 would be returned as 30002, and version 4.0 would
    be returned as 40000. Zero is returned if the connection is bad. The 3.0
    protocol is supported by PostgreSQL server
    versions 7.4 and above.

    The protocol version will not change after connection startup is
    complete, but it could theoretically change during a connection reset.
<a id="LIBPQ-PQPROTOCOLVERSION"></a>

`PQprotocolVersion`<a id="id-1.7.3.9.5.2.5.1.2"></a> [#](#LIBPQ-PQPROTOCOLVERSION)
:   Interrogates the frontend/backend protocol major version.

    ```

    int PQprotocolVersion(const PGconn *conn);
    ```

    Unlike [`PQfullProtocolVersion`](libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION), this returns only
    the major protocol version in use, but it is supported by a wider range
    of libpq releases back to version 7.4. Currently, the possible values are
    3 (3.0 protocol), or zero (connection bad). Prior to release version
    14.0, libpq could additionally return 2 (2.0 protocol).
<a id="LIBPQ-PQSERVERVERSION"></a>

`PQserverVersion`<a id="id-1.7.3.9.5.2.6.1.2"></a> [#](#LIBPQ-PQSERVERVERSION)
:   Returns an integer representing the server version.

    ```

    int PQserverVersion(const PGconn *conn);
    ```

    Applications might use this function to determine the version of the
    database server they are connected to. The result is formed by
    multiplying the server's major version number by 10000 and adding
    the minor version number. For example, version 10.1 will be
    returned as 100001, and version 11.0 will be returned as 110000.
    Zero is returned if the connection is bad.

    Prior to major version 10, PostgreSQL used
    three-part version numbers in which the first two parts together
    represented the major version. For those
    versions, [`PQserverVersion`](libpq-status.md#LIBPQ-PQSERVERVERSION) uses two digits for each
    part; for example version 9.1.5 will be returned as 90105, and
    version 9.2.0 will be returned as 90200.

    Therefore, for purposes of determining feature compatibility,
    applications should divide the result of [`PQserverVersion`](libpq-status.md#LIBPQ-PQSERVERVERSION)
    by 100 not 10000 to determine a logical major version number.
    In all release series, only the last two digits differ between
    minor releases (bug-fix releases).
<a id="LIBPQ-PQERRORMESSAGE"></a>

`PQerrorMessage`<a id="id-1.7.3.9.5.2.7.1.2"></a> <a id="id-1.7.3.9.5.2.7.1.3"></a> [#](#LIBPQ-PQERRORMESSAGE)
:   Returns the error message most recently generated by
    an operation on the connection.

    ```

    char *PQerrorMessage(const PGconn *conn);
    ```

    Nearly all libpq functions will set a message for
    [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) if they fail. Note that by
    libpq convention, a nonempty
    [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) result can consist of multiple lines,
    and will include a trailing newline. The caller should not free
    the result directly. It will be freed when the associated
    `PGconn` handle is passed to
    [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH). The result string should not be
    expected to remain the same across operations on the
    `PGconn` structure.
<a id="LIBPQ-PQSOCKET"></a>

`PQsocket`<a id="id-1.7.3.9.5.2.8.1.2"></a> [#](#LIBPQ-PQSOCKET)
:   Obtains the file descriptor number of the connection socket to
    the server. A valid descriptor will be greater than or equal
    to 0; a result of -1 indicates that no server connection is
    currently open. (This will not change during normal operation,
    but could change during connection setup or reset.)

    ```

    int PQsocket(const PGconn *conn);
    ```
<a id="LIBPQ-PQBACKENDPID"></a>

`PQbackendPID`<a id="id-1.7.3.9.5.2.9.1.2"></a> [#](#LIBPQ-PQBACKENDPID)
:   Returns the process ID (PID)<a id="id-1.7.3.9.5.2.9.2.1.2"></a>
    of the backend process handling this connection.

    ```

    int PQbackendPID(const PGconn *conn);
    ```

    The backend PID is useful for debugging
    purposes and for comparison to `NOTIFY`
    messages (which include the PID of the
    notifying backend process). Note that the
    PID belongs to a process executing on the
    database server host, not the local host!
<a id="LIBPQ-PQCONNECTIONNEEDSPASSWORD"></a>

`PQconnectionNeedsPassword`<a id="id-1.7.3.9.5.2.10.1.2"></a> [#](#LIBPQ-PQCONNECTIONNEEDSPASSWORD)
:   Returns true (1) if the connection authentication method
    required a password, but none was available.
    Returns false (0) if not.

    ```

    int PQconnectionNeedsPassword(const PGconn *conn);
    ```

    This function can be applied after a failed connection attempt
    to decide whether to prompt the user for a password.
<a id="LIBPQ-PQCONNECTIONUSEDPASSWORD"></a>

`PQconnectionUsedPassword`<a id="id-1.7.3.9.5.2.11.1.2"></a> [#](#LIBPQ-PQCONNECTIONUSEDPASSWORD)
:   Returns true (1) if the connection authentication method
    used a password. Returns false (0) if not.

    ```

    int PQconnectionUsedPassword(const PGconn *conn);
    ```

    This function can be applied after either a failed or successful
    connection attempt to detect whether the server demanded a password.
<a id="LIBPQ-PQCONNECTIONUSEDGSSAPI"></a>

`PQconnectionUsedGSSAPI`<a id="id-1.7.3.9.5.2.12.1.2"></a> [#](#LIBPQ-PQCONNECTIONUSEDGSSAPI)
:   Returns true (1) if the connection authentication method
    used GSSAPI. Returns false (0) if not.

    ```

    int PQconnectionUsedGSSAPI(const PGconn *conn);
    ```

    This function can be applied to detect whether the connection was
    authenticated with GSSAPI.

The following functions return information related to SSL. This information
usually doesn't change after a connection is established.

<a id="LIBPQ-PQSSLINUSE"></a>

`PQsslInUse`<a id="id-1.7.3.9.6.1.1.1.2"></a> [#](#LIBPQ-PQSSLINUSE)
:   Returns true (1) if the connection uses SSL, false (0) if not.

    ```

    int PQsslInUse(const PGconn *conn);
    ```
<a id="LIBPQ-PQSSLATTRIBUTE"></a>

`PQsslAttribute`<a id="id-1.7.3.9.6.1.2.1.2"></a> [#](#LIBPQ-PQSSLATTRIBUTE)
:   Returns SSL-related information about the connection.

    ```

    const char *PQsslAttribute(const PGconn *conn, const char *attribute_name);
    ```

    The list of available attributes varies depending on the SSL library
    being used and the type of connection. Returns NULL if the connection
    does not use SSL or the specified attribute name is not defined for the
    library in use.

    The following attributes are commonly available:

    `library`
    :   Name of the SSL implementation in use. (Currently, only
        `"OpenSSL"` is implemented)

    `protocol`
    :   SSL/TLS version in use. Common values
        are `"TLSv1"`, `"TLSv1.1"`
        and `"TLSv1.2"`, but an implementation may
        return other strings if some other protocol is used.

    `key_bits`
    :   Number of key bits used by the encryption algorithm.

    `cipher`
    :   A short name of the ciphersuite used, e.g.,
        `"DHE-RSA-DES-CBC3-SHA"`. The names are specific
        to each SSL implementation.

    `compression`
    :   Returns "on" if SSL compression is in use, else it returns "off".

    `alpn`
    :   Application protocol selected by the TLS Application-Layer
        Protocol Negotiation (ALPN) extension. The only protocol
        supported by libpq is `postgresql`, so this is
        mainly useful for checking whether the server supported ALPN or
        not. Empty string if ALPN was not used.

    As a special case, the `library` attribute may be
    queried without a connection by passing NULL as
    the `conn` argument. The result will be the default
    SSL library name, or NULL if libpq was
    compiled without any SSL support. (Prior
    to PostgreSQL version 15, passing NULL as
    the `conn` argument always resulted in NULL.
    Client programs needing to differentiate between the newer and older
    implementations of this case may check the
    `LIBPQ_HAS_SSL_LIBRARY_DETECTION` feature macro.)
<a id="LIBPQ-PQSSLATTRIBUTENAMES"></a>

`PQsslAttributeNames`<a id="id-1.7.3.9.6.1.3.1.2"></a> [#](#LIBPQ-PQSSLATTRIBUTENAMES)
:   Returns an array of SSL attribute names that can be used
    in `PQsslAttribute()`.
    The array is terminated by a NULL pointer.

    ```

    const char * const * PQsslAttributeNames(const PGconn *conn);
    ```

    If `conn` is NULL, the attributes available for the
    default SSL library are returned, or an empty list
    if libpq was compiled without any SSL
    support. If `conn` is not NULL, the attributes
    available for the SSL library in use for the connection are returned,
    or an empty list if the connection is not encrypted.
<a id="LIBPQ-PQSSLSTRUCT"></a>

`PQsslStruct`<a id="id-1.7.3.9.6.1.4.1.2"></a> [#](#LIBPQ-PQSSLSTRUCT)
:   Returns a pointer to an SSL-implementation-specific object describing
    the connection. Returns NULL if the connection is not encrypted
    or the requested type of object is not available from the connection's
    SSL implementation.

    ```

    void *PQsslStruct(const PGconn *conn, const char *struct_name);
    ```

    The struct(s) available depend on the SSL implementation in use.
    For OpenSSL, there is one struct,
    available under the name `OpenSSL`,
    and it returns a pointer to
    OpenSSL's `SSL` struct.
    To use this function, code along the following lines could be used:

    ```

    #include <libpq-fe.h>
    #include <openssl/ssl.h>

    ...

        SSL *ssl;

        dbconn = PQconnectdb(...);
        ...

        ssl = PQsslStruct(dbconn, "OpenSSL");
        if (ssl)
        {
            /* use OpenSSL functions to access ssl */
        }
    ```

    This structure can be used to verify encryption levels, check server
    certificates, and more. Refer to the OpenSSL
    documentation for information about this structure.
<a id="LIBPQ-PQGETSSL"></a>

`PQgetssl`<a id="id-1.7.3.9.6.1.5.1.2"></a> [#](#LIBPQ-PQGETSSL)
:   <a id="id-1.7.3.9.6.1.5.2.1.1"></a>
    Returns the SSL structure used in the connection, or NULL
    if SSL is not in use.

    ```

    void *PQgetssl(const PGconn *conn);
    ```

    This function is equivalent to `PQsslStruct(conn, "OpenSSL")`. It should
    not be used in new applications, because the returned struct is
    specific to OpenSSL and will not be
    available if another SSL implementation is used.
    To check if a connection uses SSL, call
    [`PQsslInUse`](libpq-status.md#LIBPQ-PQSSLINUSE) instead, and for more details about the
    connection, use [`PQsslAttribute`](libpq-status.md#LIBPQ-PQSSLATTRIBUTE).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-status.html)（英文原文，待翻譯）
