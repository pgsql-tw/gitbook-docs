## 18.10. Secure TCP/IP Connections with GSSAPI Encryption [#](#GSSAPI-ENC)

[18.10.1. Basic Setup](gssapi-enc.md#GSSAPI-SETUP)

<a id="id-1.6.5.13.2"></a>

PostgreSQL also has native support for
using GSSAPI to encrypt client/server communications for
increased security. Support requires that a GSSAPI
implementation (such as MIT Kerberos) is installed on both client and server
systems, and that support in PostgreSQL is
enabled at build time (see [Chapter 17](../installation/README.md)).

<a id="GSSAPI-SETUP"></a>

### 18.10.1. Basic Setup [#](#GSSAPI-SETUP)

The PostgreSQL server will listen for both
normal and GSSAPI-encrypted connections on the same TCP
port, and will negotiate with any connecting client whether to
use GSSAPI for encryption (and for authentication). By
default, this decision is up to the client (which means it can be
downgraded by an attacker); see [Section 20.1](../client-authentication/auth-pg-hba-conf.md) about
setting up the server to require the use of GSSAPI for
some or all connections.

When using GSSAPI for encryption, it is common to
use GSSAPI for authentication as well, since the
underlying mechanism will determine both client and server identities
(according to the GSSAPI implementation) in any
case. But this is not required;
another PostgreSQL authentication method
can be chosen to perform additional verification.

Other than configuration of the negotiation
behavior, GSSAPI encryption requires no setup beyond
that which is necessary for GSSAPI authentication. (For more information
on configuring that, see [Section 20.6](../client-authentication/gssapi-auth.md).)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gssapi-enc.html)（英文原文，待翻譯）
