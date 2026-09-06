## 54.3. SASL Authentication [#](#SASL-AUTHENTICATION)

[54.3.1. SCRAM-SHA-256 Authentication](sasl-authentication.md#SASL-SCRAM-SHA-256)

[54.3.2. OAUTHBEARER Authentication](sasl-authentication.md#SASL-OAUTHBEARER)

*SASL* is a framework for authentication in connection-oriented
protocols. At the moment, PostgreSQL implements three
SASL authentication mechanisms: SCRAM-SHA-256, SCRAM-SHA-256-PLUS, and
OAUTHBEARER. More might be added in the future. The below steps illustrate how SASL
authentication is performed in general, while the next subsections give
more details on particular mechanisms.

<a id="id-1.10.6.8.3"></a>

**SASL Authentication Message Flow**

<a id="SASL-AUTH-BEGIN"></a>1. To begin a SASL authentication exchange, the server sends an
   AuthenticationSASL message. It includes a list of SASL authentication
   mechanisms that the server can accept, in the server's preferred order.
<a id="SASL-AUTH-INITIAL-RESPONSE"></a>2. The client selects one of the supported mechanisms from the list, and sends
   a SASLInitialResponse message to the server. The message includes the name
   of the selected mechanism, and an optional Initial Client Response, if the
   selected mechanism uses that.
<a id="SASL-AUTH-CONTINUE"></a>3. One or more server-challenge and client-response message will follow. Each
   server-challenge is sent in an AuthenticationSASLContinue message, followed
   by a response from client in a SASLResponse message. The particulars of
   the messages are mechanism specific.
<a id="SASL-AUTH-END"></a>4. Finally, when the authentication exchange is completed successfully, the
   server sends an optional AuthenticationSASLFinal message, followed
   immediately by an AuthenticationOk message. The AuthenticationSASLFinal
   contains additional server-to-client data, whose content is particular to the
   selected authentication mechanism. If the authentication mechanism doesn't
   use additional data that's sent at completion, the AuthenticationSASLFinal
   message is not sent.

On error, the server can abort the authentication at any stage, and send an
ErrorMessage.

<a id="SASL-SCRAM-SHA-256"></a>

### 54.3.1. SCRAM-SHA-256 Authentication [#](#SASL-SCRAM-SHA-256)

`SCRAM-SHA-256`, and its variant with channel
binding `SCRAM-SHA-256-PLUS`, are password-based
authentication mechanisms. They are described in
detail in [RFC 7677](https://datatracker.ietf.org/doc/html/rfc7677)
and [RFC 5802](https://datatracker.ietf.org/doc/html/rfc5802).

When SCRAM-SHA-256 is used in PostgreSQL, the server will ignore the user name
that the client sends in the `client-first-message`. The user name
that was already sent in the startup message is used instead.
PostgreSQL supports multiple character encodings, while SCRAM
dictates UTF-8 to be used for the user name, so it might be impossible to
represent the PostgreSQL user name in UTF-8.

The SCRAM specification dictates that the password is also in UTF-8, and is
processed with the *SASLprep* algorithm.
PostgreSQL, however, does not require UTF-8 to be used for
the password. When a user's password is set, it is processed with SASLprep
as if it was in UTF-8, regardless of the actual encoding used. However, if
it is not a legal UTF-8 byte sequence, or it contains UTF-8 byte sequences
that are prohibited by the SASLprep algorithm, the raw password will be used
without SASLprep processing, instead of throwing an error. This allows the
password to be normalized when it is in UTF-8, but still allows a non-UTF-8
password to be used, and doesn't require the system to know which encoding
the password is in.

*Channel binding* is supported in PostgreSQL builds with
SSL support. The SASL mechanism name for SCRAM with channel binding is
`SCRAM-SHA-256-PLUS`. The channel binding type used by
PostgreSQL is `tls-server-end-point`.

In SCRAM without channel binding, the server chooses
a random number that is transmitted to the client to be mixed with the
user-supplied password in the transmitted password hash. While this
prevents the password hash from being successfully retransmitted in
a later session, it does not prevent a fake server between the real
server and client from passing through the server's random value
and successfully authenticating.

SCRAM with channel binding prevents such
man-in-the-middle attacks by mixing the signature of the server's
certificate into the transmitted password hash. While a fake server can
retransmit the real server's certificate, it doesn't have access to the
private key matching that certificate, and therefore cannot prove it is
the owner, causing SSL connection failure.

<a id="id-1.10.6.8.5.8"></a>

**Example**

<a id="SCRAM-BEGIN"></a>1. The server sends an AuthenticationSASL message. It includes a list of
   SASL authentication mechanisms that the server can accept.
   This will be `SCRAM-SHA-256-PLUS`
   and `SCRAM-SHA-256` if the server is built with SSL
   support, or else just the latter.
<a id="SCRAM-CLIENT-FIRST"></a>2. The client responds by sending a SASLInitialResponse message, which
   indicates the chosen mechanism, `SCRAM-SHA-256` or
   `SCRAM-SHA-256-PLUS`. (A client is free to choose either
   mechanism, but for better security it should choose the channel-binding
   variant if it can support it.) In the Initial Client response field, the
   message contains the SCRAM `client-first-message`.
   The `client-first-message` also contains the channel
   binding type chosen by the client.
<a id="SCRAM-SERVER-FIRST"></a>3. Server sends an AuthenticationSASLContinue message, with a SCRAM
   `server-first-message` as the content.
<a id="SCRAM-CLIENT-FINAL"></a>4. Client sends a SASLResponse message, with SCRAM
   `client-final-message` as the content.
<a id="SCRAM-SERVER-FINAL"></a>5. Server sends an AuthenticationSASLFinal message, with the SCRAM
   `server-final-message`, followed immediately by
   an AuthenticationOk message.

<a id="SASL-OAUTHBEARER"></a>

### 54.3.2. OAUTHBEARER Authentication [#](#SASL-OAUTHBEARER)

`OAUTHBEARER` is a token-based mechanism for federated
authentication. It is described in detail in
[RFC 7628](https://datatracker.ietf.org/doc/html/rfc7628).

A typical exchange differs depending on whether or not the client already
has a bearer token cached for the current user. If it does not, the exchange
will take place over two connections: the first "discovery" connection to
obtain OAuth metadata from the server, and the second connection to send
the token after the client has obtained it. (libpq does not currently
implement a caching method as part of its builtin flow, so it uses the
two-connection exchange.)

This mechanism is client-initiated, like SCRAM. The client initial response
consists of the standard "GS2" header used by SCRAM, followed by a list of
`key=value` pairs. The only key currently supported by
the server is `auth`, which contains the bearer token.
`OAUTHBEARER` additionally specifies three optional
components of the client initial response (the `authzid` of
the GS2 header, and the `host` and
`port` keys) which are currently ignored by the
server.

`OAUTHBEARER` does not support channel binding, and there
is no "OAUTHBEARER-PLUS" mechanism. This mechanism does not make use of
server data during a successful authentication, so the
AuthenticationSASLFinal message is not used in the exchange.

<a id="id-1.10.6.8.6.6"></a>

**Example**

1. During the first exchange, the server sends an AuthenticationSASL message
   with the `OAUTHBEARER` mechanism advertised.
2. The client responds by sending a SASLInitialResponse message which
   indicates the `OAUTHBEARER` mechanism. Assuming the
   client does not already have a valid bearer token for the current user,
   the `auth` field is empty, indicating a discovery
   connection.
3. Server sends an AuthenticationSASLContinue message containing an error
   `status` alongside a well-known URI and scopes that the
   client should use to conduct an OAuth flow.
4. Client sends a SASLResponse message containing the empty set (a single
   `0x01` byte) to finish its half of the discovery
   exchange.
5. Server sends an ErrorMessage to fail the first exchange.

   At this point, the client conducts one of many possible OAuth flows to
   obtain a bearer token, using any metadata that it has been configured with
   in addition to that provided by the server. (This description is left
   deliberately vague; `OAUTHBEARER` does not specify or
   mandate any particular method for obtaining a token.)

   Once it has a token, the client reconnects to the server for the final
   exchange:
6. The server once again sends an AuthenticationSASL message with the
   `OAUTHBEARER` mechanism advertised.
7. The client responds by sending a SASLInitialResponse message, but this
   time the `auth` field in the message contains the
   bearer token that was obtained during the client flow.
8. The server validates the token according to the instructions of the
   token provider. If the client is authorized to connect, it sends an
   AuthenticationOk message to end the SASL exchange.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sasl-authentication.html)（英文原文，待翻譯）
