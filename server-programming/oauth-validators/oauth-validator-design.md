## 50.1. Safely Designing a Validator Module [#](#OAUTH-VALIDATOR-DESIGN)

[50.1.1. Validator Responsibilities](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)

[50.1.2. General Coding Guidelines](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-GUIDELINES)

[50.1.3. Authorizing Users (Usermap Delegation)](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

### Warning

Read and understand the entirety of this section before implementing a
validator module. A malfunctioning validator is potentially worse than no
authentication at all, both because of the false sense of security it
provides, and because it may contribute to attacks against other pieces of
an OAuth ecosystem.

<a id="OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES"></a>

### 50.1.1. Validator Responsibilities [#](#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)

Although different modules may take very different approaches to token
validation, implementations generally need to perform three separate
actions:

Validate the Token
:   The validator must first ensure that the presented token is in fact a
    valid Bearer token for use in client authentication. The correct way to
    do this depends on the provider, but it generally involves either
    cryptographic operations to prove that the token was created by a trusted
    party (offline validation), or the presentation of the token to that
    trusted party so that it can perform validation for you (online
    validation).

    Online validation, usually implemented via
    [OAuth Token
    Introspection](https://datatracker.ietf.org/doc/html/rfc7662), requires fewer steps of a validator module and
    allows central revocation of a token in the event that it is stolen
    or misissued. However, it does require the module to make at least one
    network call per authentication attempt (all of which must complete
    within the configured [authentication_timeout](../../server-administration/runtime-config/runtime-config-connection.md#GUC-AUTHENTICATION-TIMEOUT)).
    Additionally, your provider may not provide introspection endpoints for
    use by external resource servers.

    Offline validation is much more involved, typically requiring a validator
    to maintain a list of trusted signing keys for a provider and then
    check the token's cryptographic signature along with its contents.
    Implementations must follow the provider's instructions to the letter,
    including any verification of issuer ("where is this token from?"),
    audience ("who is this token for?"), and validity period ("when can this
    token be used?"). Since there is no communication between the module and
    the provider, tokens cannot be centrally revoked using this method;
    offline validator implementations may wish to place restrictions on the
    maximum length of a token's validity period.

    If the token cannot be validated, the module should immediately fail.
    Further authentication/authorization is pointless if the bearer token
    wasn't issued by a trusted party.

Authorize the Client
:   Next the validator must ensure that the end user has given the client
    permission to access the server on their behalf. This generally involves
    checking the scopes that have been assigned to the token, to make sure
    that they cover database access for the current HBA parameters.

    The purpose of this step is to prevent an OAuth client from obtaining a
    token under false pretenses. If the validator requires all tokens to
    carry scopes that cover database access, the provider should then loudly
    prompt the user to grant that access during the flow. This gives them the
    opportunity to reject the request if the client isn't supposed to be
    using their credentials to connect to databases.

    While it is possible to establish client authorization without explicit
    scopes by using out-of-band knowledge of the deployed architecture, doing
    so removes the user from the loop, which prevents them from catching
    deployment mistakes and allows any such mistakes to be exploited
    silently. Access to the database must be tightly restricted to only
    trusted clients
    [<a id="id-1.8.17.6.3.3.2.2.3.1"></a>[17]](#ftn.id-1.8.17.6.3.3.2.2.3.1)
    if users are not prompted for additional scopes.

    Even if authorization fails, a module may choose to continue to pull
    authentication information from the token for use in auditing and
    debugging.

Authenticate the End User
:   Finally, the validator should determine a user identifier for the token,
    either by asking the provider for this information or by extracting it
    from the token itself, and return that identifier to the server (which
    will then make a final authorization decision using the HBA
    configuration). This identifier will be available within the session via
    [`system_user`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)
    and recorded in the server logs if [log_connections](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-CONNECTIONS)
    is enabled.

    Different providers may record a variety of different authentication
    information for an end user, typically referred to as
    *claims*. Providers usually document which of these
    claims are trustworthy enough to use for authorization decisions and
    which are not. (For instance, it would probably not be wise to use an
    end user's full name as the identifier for authentication, since many
    providers allow users to change their display names arbitrarily.)
    Ultimately, the choice of which claim (or combination of claims) to use
    comes down to the provider implementation and application requirements.

    Note that anonymous/pseudonymous login is possible as well, by enabling
    usermap delegation; see
    [Section 50.1.3](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION).

<a id="OAUTH-VALIDATOR-DESIGN-GUIDELINES"></a>

### 50.1.2. General Coding Guidelines [#](#OAUTH-VALIDATOR-DESIGN-GUIDELINES)

Developers should keep the following in mind when implementing token
validation:

Token Confidentiality
:   Modules should not write tokens, or pieces of tokens, into the server
    log. This is true even if the module considers the token invalid; an
    attacker who confuses a client into communicating with the wrong provider
    should not be able to retrieve that (otherwise valid) token from the
    disk.

    Implementations that send tokens over the network (for example, to
    perform online token validation with a provider) must authenticate the
    peer and ensure that strong transport security is in use.

Logging
:   Modules may use the same [logging
    facilities](../../internals/source/error-message-reporting.md) as standard extensions; however, the rules for emitting
    log entries to the client are subtly different during the authentication
    phase of the connection. Generally speaking, modules should log
    verification problems at the `COMMERROR` level and return
    normally, instead of using `ERROR`/`FATAL`
    to unwind the stack, to avoid leaking information to unauthenticated
    clients.

Interruptibility
:   Modules must remain interruptible by signals so that the server can
    correctly handle authentication timeouts and shutdown signals from
    pg_ctl. For example, blocking calls on sockets
    should generally be replaced with code that handles both socket events
    and interrupts without races (see `WaitLatchOrSocket()`,
    `WaitEventSetWait()`, et al), and long-running loops
    should periodically call `CHECK_FOR_INTERRUPTS()`.
    Failure to follow this guidance may result in unresponsive backend
    sessions.

Testing
:   The breadth of testing an OAuth system is well beyond the scope of this
    documentation, but at minimum, negative testing should be considered
    mandatory. It's trivial to design a module that lets authorized users in;
    the whole point of the system is to keep unauthorized users out.

Documentation
:   Validator implementations should document the contents and format of the
    authenticated ID that is reported to the server for each end user, since
    DBAs may need to use this information to construct pg_ident maps. (For
    instance, is it an email address? an organizational ID number? a UUID?)
    They should also document whether or not it is safe to use the module in
    `delegate_ident_mapping=1` mode, and what additional
    configuration is required in order to do so.

<a id="OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION"></a>

### 50.1.3. Authorizing Users (Usermap Delegation) [#](#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

The standard deliverable of a validation module is the user identifier,
which the server will then compare to any configured
[`pg_ident.conf`
mappings](../../server-administration/client-authentication/auth-username-maps.md) and determine whether the end user is authorized to connect.
However, OAuth is itself an authorization framework, and tokens may carry
information about user privileges. For example, a token may be associated
with the organizational groups that a user belongs to, or list the roles
that a user may assume, and duplicating that knowledge into local usermaps
for every server may not be desirable.

To bypass username mapping entirely, and have the validator module assume
the additional responsibility of authorizing user connections, the HBA may
be configured with [delegate_ident_mapping](../../server-administration/client-authentication/auth-oauth.md#AUTH-OAUTH-DELEGATE-IDENT-MAPPING).
The module may then use token scopes or an equivalent method to decide
whether the user is allowed to connect under their desired role. The user
identifier will still be recorded by the server, but it plays no part in
determining whether to continue the connection.

Using this scheme, authentication itself is optional. As long as the module
reports that the connection is authorized, login will continue even if there
is no recorded user identifier at all. This makes it possible to implement
anonymous or pseudonymous access to the database, where the third-party
provider performs all necessary authentication but does not provide any
user-identifying information to the server. (Some providers may create an
anonymized ID number that can be recorded instead, for later auditing.)

Usermap delegation provides the most architectural flexibility, but it turns
the validator module into a single point of failure for connection
authorization. Use with caution.

<br>

---

<a id="ftn.id-1.8.17.6.3.3.2.2.3.1"></a>

[[17]](#id-1.8.17.6.3.3.2.2.3.1) 
That is, "trusted" in the sense that the OAuth client and the
PostgreSQL server are controlled by the same
entity. Notably, the Device Authorization client flow supported by
libpq does not usually meet this bar, since it's designed for use by
public/untrusted clients.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validator-design.html)（英文原文，待翻譯）
