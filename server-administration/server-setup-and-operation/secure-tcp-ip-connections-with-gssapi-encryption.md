# 18.10. Secure TCP/IP Connections with GSSAPI Encryption

PostgreSQL also has native support for using GSSAPI to encrypt client/server communications for increased security. Support requires that a GSSAPI implementation (such as MIT krb5) is installed on both client and server systems, and that support in PostgreSQL is enabled at build time (see [Chapter 16](../installation-from-source-code/README.md)).

## 18.10.1. Basic Setup

The PostgreSQL server will listen for both normal and GSSAPI-encrypted connections on the same TCP port, and will negotiate with any connecting client on whether to use GSSAPI for encryption (and for authentication). By default, this decision is up to the client (which means it can be downgraded by an attacker); see [Section 20.1](../client-authentication/the-pg_hba.conf-file.md) about setting up the server to require the use of GSSAPI for some or all connections.

Other than configuration of the negotiation behavior, GSSAPI encryption requires no setup beyond that which is necessary for GSSAPI authentication. (For more information on configuring that, see [Section 20.6](../client-authentication/gssapi-authentication.md).)\\
