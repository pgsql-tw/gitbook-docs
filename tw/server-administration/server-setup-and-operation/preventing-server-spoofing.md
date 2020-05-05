# 18.7. Preventing Server Spoofing

While the server is running, it is not possible for a malicious user to take the place of the normal database server. However, when the server is down, it is possible for a local user to spoof the normal server by starting their own server. The spoof server could read passwords and queries sent by clients, but could not return any data because the `PGDATA` directory would still be secure because of directory permissions. Spoofing is possible because any user can start a database server; a client cannot identify an invalid server unless it is specially configured.

One way to prevent spoofing of `local` connections is to use a Unix domain socket directory \([unix\_socket\_directories](https://www.postgresql.org/docs/12/runtime-config-connection.html#GUC-UNIX-SOCKET-DIRECTORIES)\) that has write permission only for a trusted local user. This prevents a malicious user from creating their own socket file in that directory. If you are concerned that some applications might still reference `/tmp` for the socket file and hence be vulnerable to spoofing, during operating system startup create a symbolic link `/tmp/.s.PGSQL.5432` that points to the relocated socket file. You also might need to modify your `/tmp` cleanup script to prevent removal of the symbolic link.

Another option for `local` connections is for clients to use [`requirepeer`](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNECT-REQUIREPEER) to specify the required owner of the server process connected to the socket.

To prevent spoofing on TCP connections, either use SSL certificates and make sure that clients check the server's certificate, or use GSSAPI encryption \(or both, if they're on separate connections\).

To prevent spoofing with SSL, the server must be configured to accept only `hostssl` connections \([Section 20.1](https://www.postgresql.org/docs/12/auth-pg-hba-conf.html)\) and have SSL key and certificate files \([Section 18.9](https://www.postgresql.org/docs/12/ssl-tcp.html)\). The TCP client must connect using `sslmode=verify-ca` or `verify-full` and have the appropriate root certificate file installed \([Section 33.18.1](https://www.postgresql.org/docs/12/libpq-ssl.html#LIBQ-SSL-CERTIFICATES)\).

To prevent spoofing with GSSAPI, the server must be configured to accept only `hostgssenc` connections \([Section 20.1](https://www.postgresql.org/docs/12/auth-pg-hba-conf.html)\) and use `gss` authentication with them. The TCP client must connect using `gssencmode=require`.

