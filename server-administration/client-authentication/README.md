## Chapter 20. Client Authentication

**Table of Contents**

[20.1. The `pg_hba.conf` File](auth-pg-hba-conf.md)

[20.2. User Name Maps](auth-username-maps.md)

[20.3. Authentication Methods](auth-methods.md)

[20.4. Trust Authentication](auth-trust.md)

[20.5. Password Authentication](auth-password.md)

[20.6. GSSAPI Authentication](gssapi-auth.md)

[20.7. SSPI Authentication](sspi-auth.md)

[20.8. Ident Authentication](auth-ident.md)

[20.9. Peer Authentication](auth-peer.md)

[20.10. LDAP Authentication](auth-ldap.md)

[20.11. RADIUS Authentication](auth-radius.md)

[20.12. Certificate Authentication](auth-cert.md)

[20.13. PAM Authentication](auth-pam.md)

[20.14. BSD Authentication](auth-bsd.md)

[20.15. OAuth Authorization/Authentication](auth-oauth.md)

[20.16. Authentication Problems](client-authentication-problems.md)

<a id="id-1.6.7.2"></a>

When a client application connects to the database server, it
specifies which PostgreSQL database user name it
wants to connect as, much the same way one logs into a Unix computer
as a particular user. Within the SQL environment the active database
user name determines access privileges to database objects — see
[Chapter 21](../user-manag/README.md) for more information. Therefore, it is
essential to restrict which database users can connect.

### Note

As explained in [Chapter 21](../user-manag/README.md),
PostgreSQL actually does privilege
management in terms of “roles”. In this chapter, we
consistently use *database user* to mean “role with the
`LOGIN` privilege”.

*Authentication* is the process by which the
database server establishes the identity of the client, and by
extension determines whether the client application (or the user
who runs the client application) is permitted to connect with the
database user name that was requested.

PostgreSQL offers a number of different
client authentication methods. The method used to authenticate a
particular client connection can be selected on the basis of
(client) host address, database, and user.

PostgreSQL database user names are logically
separate from user names of the operating system in which the server
runs. If all the users of a particular server also have accounts on
the server's machine, it makes sense to assign database user names
that match their operating system user names. However, a server that
accepts remote connections might have many database users who have no local
operating system
account, and in such cases there need be no connection between
database user names and OS user names.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/client-authentication.html)（英文原文，待翻譯）
