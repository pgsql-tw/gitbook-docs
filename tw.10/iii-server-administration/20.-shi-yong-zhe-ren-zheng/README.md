# 20. 使用者認證

**Table of Contents**

[20.1. The`pg_hba.conf`File](https://www.postgresql.org/docs/10/static/auth-pg-hba-conf.html)

[20.2. User Name Maps](https://www.postgresql.org/docs/10/static/auth-username-maps.html)

[20.3. Authentication Methods](https://www.postgresql.org/docs/10/static/auth-methods.html)

[20.3.1. Trust Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-TRUST)

[20.3.2. Password Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PASSWORD)

[20.3.3. GSSAPI Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#GSSAPI-AUTH)

[20.3.4. SSPI Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#SSPI-AUTH)

[20.3.5. Ident Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-IDENT)

[20.3.6. Peer Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PEER)

[20.3.7. LDAP Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-LDAP)

[20.3.8. RADIUS Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-RADIUS)

[20.3.9. Certificate Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-CERT)

[20.3.10. PAM Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PAM)

[20.3.11. BSD Authentication](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-BSD)

[20.4. Authentication Problems](https://www.postgresql.org/docs/10/static/client-authentication-problems.html)

When a client application connects to the database server, it specifies whichPostgreSQLdatabase user name it wants to connect as, much the same way one logs into a Unix computer as a particular user. Within the SQL environment the active database user name determines access privileges to database objects — see[Chapter 21](https://www.postgresql.org/docs/10/static/user-manag.html)for more information. Therefore, it is essential to restrict which database users can connect.

## Note

As explained in[Chapter 21](https://www.postgresql.org/docs/10/static/user-manag.html),PostgreSQLactually does privilege management in terms of“roles”. In this chapter, we consistently use\_database user\_to mean“role with the`LOGIN`privilege”.

\_Authentication\_is the process by which the database server establishes the identity of the client, and by extension determines whether the client application \(or the user who runs the client application\) is permitted to connect with the database user name that was requested.

PostgreSQLoffers a number of different client authentication methods. The method used to authenticate a particular client connection can be selected on the basis of \(client\) host address, database, and user.

PostgreSQLdatabase user names are logically separate from user names of the operating system in which the server runs. If all the users of a particular server also have accounts on the server's machine, it makes sense to assign database user names that match their operating system user names. However, a server that accepts remote connections might have many database users who have no local operating system account, and in such cases there need be no connection between database user names and OS user names.

