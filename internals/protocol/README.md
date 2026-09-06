## Chapter 54. Frontend/Backend Protocol

**Table of Contents**

[54.1. Overview](protocol-overview.md)
:   [54.1.1. Messaging Overview](protocol-overview.md#PROTOCOL-MESSAGE-CONCEPTS)

    [54.1.2. Extended Query Overview](protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)

    [54.1.3. Formats and Format Codes](protocol-overview.md#PROTOCOL-FORMAT-CODES)

    [54.1.4. Protocol Versions](protocol-overview.md#PROTOCOL-VERSIONS)

[54.2. Message Flow](protocol-flow.md)
:   [54.2.1. Start-up](protocol-flow.md#PROTOCOL-FLOW-START-UP)

    [54.2.2. Simple Query](protocol-flow.md#PROTOCOL-FLOW-SIMPLE-QUERY)

    [54.2.3. Extended Query](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)

    [54.2.4. Pipelining](protocol-flow.md#PROTOCOL-FLOW-PIPELINING)

    [54.2.5. Function Call](protocol-flow.md#PROTOCOL-FLOW-FUNCTION-CALL)

    [54.2.6. COPY Operations](protocol-flow.md#PROTOCOL-COPY)

    [54.2.7. Asynchronous Operations](protocol-flow.md#PROTOCOL-ASYNC)

    [54.2.8. Canceling Requests in Progress](protocol-flow.md#PROTOCOL-FLOW-CANCELING-REQUESTS)

    [54.2.9. Termination](protocol-flow.md#PROTOCOL-FLOW-TERMINATION)

    [54.2.10. SSL Session Encryption](protocol-flow.md#PROTOCOL-FLOW-SSL)

    [54.2.11. GSSAPI Session Encryption](protocol-flow.md#PROTOCOL-FLOW-GSSAPI)

[54.3. SASL Authentication](sasl-authentication.md)
:   [54.3.1. SCRAM-SHA-256 Authentication](sasl-authentication.md#SASL-SCRAM-SHA-256)

    [54.3.2. OAUTHBEARER Authentication](sasl-authentication.md#SASL-OAUTHBEARER)

[54.4. Streaming Replication Protocol](protocol-replication.md)

[54.5. Logical Streaming Replication Protocol](protocol-logical-replication.md)
:   [54.5.1. Logical Streaming Replication Parameters](protocol-logical-replication.md#PROTOCOL-LOGICAL-REPLICATION-PARAMS)

    [54.5.2. Logical Replication Protocol Messages](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES)

    [54.5.3. Logical Replication Protocol Message Flow](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES-FLOW)

[54.6. Message Data Types](protocol-message-types.md)

[54.7. Message Formats](protocol-message-formats.md)

[54.8. Error and Notice Message Fields](protocol-error-fields.md)

[54.9. Logical Replication Message Formats](protocol-logicalrep-message-formats.md)

[54.10. Summary of Changes since Protocol 2.0](protocol-changes.md)

<a id="id-1.10.6.2"></a>

PostgreSQL uses a message-based protocol
for communication between frontends and backends (clients and servers).
The protocol is supported over TCP/IP and also over
Unix-domain sockets. Port number 5432 has been registered with IANA as
the customary TCP port number for servers supporting this protocol, but
in practice any non-privileged port number can be used.

This document describes version 3.2 of the protocol, introduced in
PostgreSQL version 18. The server and the libpq
client library are backwards compatible with protocol version 3.0,
implemented in PostgreSQL 7.4 and later.

In order to serve multiple clients efficiently, the server launches
a new “backend” process for each client.
In the current implementation, a new child
process is created immediately after an incoming connection is detected.
This is transparent to the protocol, however. For purposes of the
protocol, the terms “backend” and “server” are
interchangeable; likewise “frontend” and “client”
are interchangeable.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol.html)（英文原文，待翻譯）
