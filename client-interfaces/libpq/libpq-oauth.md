## 32.20. OAuth Support [#](#LIBPQ-OAUTH)

[32.20.1. Authdata Hooks](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)

[32.20.2. Debugging and Developer Settings](libpq-oauth.md#LIBPQ-OAUTH-DEBUGGING)

libpq implements support for the OAuth v2 Device Authorization client flow,
documented in
[RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628),
as an optional module. See the [installation documentation](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL) for information on how to enable support
for Device Authorization as a builtin flow.

When support is enabled and the optional module installed, libpq
will use the builtin flow by default if the server
[requests a bearer token](../../server-administration/client-authentication/auth-oauth.md) during
authentication. This flow can be utilized even if the system running the
client application does not have a usable web browser, for example when
running a client via SSH.

The builtin flow will, by default, print a URL to visit and a user code to
enter there:

```

$ psql 'dbname=postgres oauth_issuer=https://example.com oauth_client_id=...'
Visit https://example.com/device and enter the code: ABCD-EFGH
```

(This prompt may be
[customized](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE).)
The user will then log into their OAuth provider, which will ask whether
to allow libpq and the server to perform actions on their behalf. It is always
a good idea to carefully review the URL and permissions displayed, to ensure
they match expectations, before continuing. Permissions should not be given
to untrusted third parties.

Client applications may implement their own flows to customize interaction
and integration with applications. See [Section 32.20.1](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)
for more information on how add a custom flow to libpq.

For an OAuth client flow to be usable, the connection string must at minimum
contain [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) and
[oauth_client_id](libpq-connect.md#LIBPQ-CONNECT-OAUTH-CLIENT-ID). (These settings are
determined by your organization's OAuth provider.) The builtin flow
additionally requires the OAuth authorization server to publish a device
authorization endpoint.

### Note

The builtin Device Authorization flow is not currently supported on Windows.
Custom client flows may still be implemented.

<a id="LIBPQ-OAUTH-AUTHDATA-HOOKS"></a>

### 32.20.1. Authdata Hooks [#](#LIBPQ-OAUTH-AUTHDATA-HOOKS)

The behavior of the OAuth flow may be modified or replaced by a client using
the following hook API:

<a id="LIBPQ-PQSETAUTHDATAHOOK"></a>

`PQsetAuthDataHook`<a id="id-1.7.3.27.8.2.1.1.1.2"></a> [#](#LIBPQ-PQSETAUTHDATAHOOK)
:   Sets the `PGauthDataHook`, overriding
    libpq's handling of one or more aspects of
    its OAuth client flow.

    ```

    void PQsetAuthDataHook(PQauthDataHook_type hook);
    ```

    If *`hook`* is `NULL`, the
    default handler will be reinstalled. Otherwise, the application passes
    a pointer to a callback function with the signature:

    ```

    int hook_fn(PGauthData type, PGconn *conn, void *data);
    ```

    which libpq will call when an action is
    required of the application. *`type`* describes
    the request being made, *`conn`* is the
    connection handle being authenticated, and *`data`*
    points to request-specific metadata. The contents of this pointer are
    determined by *`type`*; see
    [Section 32.20.1.1](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES) for the supported
    list.

    Hooks can be chained together to allow cooperative and/or fallback
    behavior. In general, a hook implementation should examine the incoming
    *`type`* (and, potentially, the request metadata
    and/or the settings for the particular *`conn`*
    in use) to decide whether or not to handle a specific piece of authdata.
    If not, it should delegate to the previous hook in the chain
    (retrievable via `PQgetAuthDataHook`).

    Success is indicated by returning an integer greater than zero.
    Returning a negative integer signals an error condition and abandons the
    connection attempt. (A zero value is reserved for the default
    implementation.)
<a id="LIBPQ-PQGETAUTHDATAHOOK"></a>

`PQgetAuthDataHook`<a id="id-1.7.3.27.8.2.1.2.1.2"></a> [#](#LIBPQ-PQGETAUTHDATAHOOK)
:   Retrieves the current value of `PGauthDataHook`.

    ```

    PQauthDataHook_type PQgetAuthDataHook(void);
    ```

    At initialization time (before the first call to
    `PQsetAuthDataHook`), this function will return
    `PQdefaultAuthDataHook`.

<a id="LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES"></a>

#### 32.20.1.1. Hook Types [#](#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES)

The following `PGauthData` types and their corresponding
*`data`* structures are defined:

<a id="LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE"></a>

`PQAUTHDATA_PROMPT_OAUTH_DEVICE` <a id="id-1.7.3.27.8.3.2.3.1.1.2"></a> [#](#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE)
:   Replaces the default user prompt during the builtin device
    authorization client flow. *`data`* points to
    an instance of `PGpromptOAuthDevice`:

    ```

    typedef struct _PGpromptOAuthDevice
    {
        const char *verification_uri;   /* verification URI to visit */
        const char *user_code;          /* user code to enter */
        const char *verification_uri_complete;  /* optional combination of URI and
                                                 * code, or NULL */
        int         expires_in;         /* seconds until user code expires */
    } PGpromptOAuthDevice;
    ```

    The OAuth Device Authorization flow which
    [can be included](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)
    in libpq
    requires the end user to visit a URL with a browser, then enter a code
    which permits libpq to connect to the server
    on their behalf. The default prompt simply prints the
    `verification_uri` and `user_code`
    on standard error. Replacement implementations may display this
    information using any preferred method, for example with a GUI.

    This callback is only invoked during the builtin device
    authorization flow. If the application installs a
    [custom OAuth
    flow](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN), or libpq was not built with
    support for the builtin flow, this authdata type will not be used.

    If a non-NULL `verification_uri_complete` is
    provided, it may optionally be used for non-textual verification (for
    example, by displaying a QR code). The URL and user code should still
    be displayed to the end user in this case, because the code will be
    manually confirmed by the provider, and the URL lets users continue
    even if they can't use the non-textual method. For more information,
    see section 3.3.1 in
    [RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628#section-3.3.1).
<a id="LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN"></a>

`PQAUTHDATA_OAUTH_BEARER_TOKEN` <a id="id-1.7.3.27.8.3.2.3.2.1.2"></a> [#](#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN)
:   Adds a custom implementation of a flow, replacing the builtin flow if
    it is [installed](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL).
    The hook should either directly return a Bearer token for the current
    user/issuer/scope combination, if one is available without blocking, or
    else set up an asynchronous callback to retrieve one.

    *`data`* points to an instance
    of `PGoauthBearerRequest`, which should be filled in
    by the implementation:

    ```

    typedef struct PGoauthBearerRequest
    {
        /* Hook inputs (constant across all calls) */
        const char *openid_configuration; /* OIDC discovery URL */
        const char *scope;                /* required scope(s), or NULL */

        /* Hook outputs */

        /*
         * Callback implementing a custom asynchronous OAuth flow. The signature is
         * platform-dependent: PQ_SOCKTYPE is SOCKET on Windows, and int everywhere
         * else.
         */
        PostgresPollingStatusType (*async) (PGconn *conn,
                                            struct PGoauthBearerRequest *request,
                                            PQ_SOCKTYPE *altsock);

        /* Callback to clean up custom allocations. */
        void        (*cleanup) (PGconn *conn, struct PGoauthBearerRequest *request);

        char       *token;   /* acquired Bearer token */
        void       *user;    /* hook-defined allocated data */
    } PGoauthBearerRequest;
    ```

    Two pieces of information are provided to the hook by
    libpq:
    *`openid_configuration`* contains the URL of an
    OAuth discovery document describing the authorization server's
    supported flows, and *`scope`* contains a
    (possibly empty) space-separated list of OAuth scopes which are
    required to access the server. Either or both may be
    `NULL` to indicate that the information was not
    discoverable. (In this case, implementations may be able to establish
    the requirements using some other preconfigured knowledge, or they may
    choose to fail.)

    The final output of the hook is *`token`*, which
    must point to a valid Bearer token for use on the connection. (This
    token should be issued by the
    [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) and hold the requested
    scopes, or the connection will be rejected by the server's validator
    module.) The allocated token string must remain valid until
    libpq is finished connecting; the hook
    should set a *`cleanup`* callback which will be
    called when libpq no longer requires it.

    If an implementation cannot immediately produce a
    *`token`* during the initial call to the hook,
    it should set the *`async`* callback to handle
    nonblocking communication with the authorization server.
    [<a id="id-1.7.3.27.8.3.2.3.2.2.5.3"></a>[16]](#ftn.id-1.7.3.27.8.3.2.3.2.2.5.3)
    This will be called to begin the flow immediately upon return from the
    hook. When the callback cannot make further progress without blocking,
    it should return either `PGRES_POLLING_READING` or
    `PGRES_POLLING_WRITING` after setting
    `*altsock` to the file descriptor that will be marked
    ready to read/write when progress can be made again. (This descriptor
    is then provided to the top-level polling loop via
    `PQsocket()`.) Return `PGRES_POLLING_OK`
    after setting *`token`* when the flow is
    complete, or `PGRES_POLLING_FAILED` to indicate failure.

    Implementations may wish to store additional data for bookkeeping
    across calls to the *`async`* and
    *`cleanup`* callbacks. The
    *`user`* pointer is provided for this purpose;
    libpq will not touch its contents and the
    application may use it at its convenience. (Remember to free any
    allocations during token cleanup.)

<a id="LIBPQ-OAUTH-DEBUGGING"></a>

### 32.20.2. Debugging and Developer Settings [#](#LIBPQ-OAUTH-DEBUGGING)

A "dangerous debugging mode" may be enabled by setting the environment
variable `PGOAUTHDEBUG=UNSAFE`. This functionality is provided
for ease of local development and testing only. It does several things that
you will not want a production system to do:

* permits the use of unencrypted HTTP during the OAuth provider exchange
* allows the system's trusted CA list to be completely replaced using the
  `PGOAUTHCAFILE` environment variable
* prints HTTP traffic (containing several critical secrets) to standard
  error during the OAuth flow
* permits the use of zero-second retry intervals, which can cause the
  client to busy-loop and pointlessly consume CPU

### Warning

Do not share the output of the OAuth flow traffic with third parties. It
contains secrets that can be used to attack your clients and servers.

<br>

---

<a id="ftn.id-1.7.3.27.8.3.2.3.2.2.5.3"></a>

[[16]](#id-1.7.3.27.8.3.2.3.2.2.5.3) 
Performing blocking operations during the
`PQAUTHDATA_OAUTH_BEARER_TOKEN` hook callback will
interfere with nonblocking connection APIs such as
`PQconnectPoll` and prevent concurrent connections
from making progress. Applications which only ever use the
synchronous connection primitives, such as
`PQconnectdb`, may synchronously retrieve a token
during the hook instead of implementing the
*`async`* callback, but they will necessarily
be limited to one connection at a time.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-oauth.html)（英文原文，待翻譯）
