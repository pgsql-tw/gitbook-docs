# 20.3. Authentication Methods

PostgreSQL provides various methods for authenticating users:

* [Trust authentication](trust-authentication.md), which simply trusts that users are who they say they are.
* [Password authentication](password-authentication.md), which requires that users send a password.
* [GSSAPI authentication](gssapi-authentication.md), which relies on a GSSAPI-compatible security library. Typically this is used to access an authentication server such as a Kerberos or Microsoft Active Directory server.
* [SSPI authentication](sspi-authentication.md), which uses a Windows-specific protocol similar to GSSAPI.
* [Ident authentication](ident-authentication.md), which relies on an “Identification Protocol” (RFC 1413) service on the client's machine. (On local Unix-socket connections, this is treated as peer authentication.)
* [Peer authentication](peer-authentication.md), which relies on operating system facilities to identify the process at the other end of a local connection. This is not supported for remote connections.
* [LDAP authentication](ldap-authentication.md), which relies on an LDAP authentication server.
* [RADIUS authentication](radius-authentication.md), which relies on a RADIUS authentication server.
* [Certificate authentication](certificate-authentication.md), which requires an SSL connection and authenticates users by checking the SSL certificate they send.
* [PAM authentication](pam-authentication.md), which relies on a PAM (Pluggable Authentication Modules) library.
* [BSD authentication](21.14.-bsd-authentication.md), which relies on the BSD Authentication framework (currently available only on OpenBSD).

Peer authentication is usually recommendable for local connections, though trust authentication might be sufficient in some circumstances. Password authentication is the easiest choice for remote connections. All the other options require some kind of external security infrastructure (usually an authentication server or a certificate authority for issuing SSL certificates), or are platform-specific.

The following sections describe each of these authentication methods in more detail.
