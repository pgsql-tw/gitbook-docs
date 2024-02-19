# 21.3. Authentication Methods

PostgreSQL provides various methods for authenticating users:

* [Trust authentication](https://www.postgresql.org/docs/13/auth-trust.html), which simply trusts that users are who they say they are.
* [Password authentication](https://www.postgresql.org/docs/13/auth-password.html), which requires that users send a password.
* [GSSAPI authentication](https://www.postgresql.org/docs/13/gssapi-auth.html), which relies on a GSSAPI-compatible security library. Typically this is used to access an authentication server such as a Kerberos or Microsoft Active Directory server.
* [SSPI authentication](https://www.postgresql.org/docs/13/sspi-auth.html), which uses a Windows-specific protocol similar to GSSAPI.
* [Ident authentication](https://www.postgresql.org/docs/13/auth-ident.html), which relies on an “Identification Protocol” (RFC 1413) service on the client's machine. (On local Unix-socket connections, this is treated as peer authentication.)
* [Peer authentication](https://www.postgresql.org/docs/13/auth-peer.html), which relies on operating system facilities to identify the process at the other end of a local connection. This is not supported for remote connections.
* [LDAP authentication](https://www.postgresql.org/docs/13/auth-ldap.html), which relies on an LDAP authentication server.
* [RADIUS authentication](https://www.postgresql.org/docs/13/auth-radius.html), which relies on a RADIUS authentication server.
* [Certificate authentication](https://www.postgresql.org/docs/13/auth-cert.html), which requires an SSL connection and authenticates users by checking the SSL certificate they send.
* [PAM authentication](https://www.postgresql.org/docs/13/auth-pam.html), which relies on a PAM (Pluggable Authentication Modules) library.
* [BSD authentication](https://www.postgresql.org/docs/13/auth-bsd.html), which relies on the BSD Authentication framework (currently available only on OpenBSD).

Peer authentication is usually recommendable for local connections, though trust authentication might be sufficient in some circumstances. Password authentication is the easiest choice for remote connections. All the other options require some kind of external security infrastructure (usually an authentication server or a certificate authority for issuing SSL certificates), or are platform-specific.

The following sections describe each of these authentication methods in more detail.
