<a id="id-1.11.7.21.8.1"></a>

## dblink_connect_u

dblink_connect_u — opens a persistent connection to a remote database, insecurely

## Synopsis

```

dblink_connect_u(text connstr) returns text
dblink_connect_u(text connname, text connstr) returns text
```

<a id="id-1.11.7.21.8.5"></a>

## Description

`dblink_connect_u()` is identical to
`dblink_connect()`, except that it will allow non-superusers
to connect using any authentication method.

If the remote server selects an authentication method that does not
involve a password, then impersonation and subsequent escalation of
privileges can occur, because the session will appear to have
originated from the user as which the local PostgreSQL
server runs. Also, even if the remote server does demand a password,
it is possible for the password to be supplied from the server
environment, such as a `~/.pgpass` file belonging to the
server's user. This opens not only a risk of impersonation, but the
possibility of exposing a password to an untrustworthy remote server.
Therefore, `dblink_connect_u()` is initially
installed with all privileges revoked from `PUBLIC`,
making it un-callable except by superusers. In some situations
it may be appropriate to grant `EXECUTE` permission for
`dblink_connect_u()` to specific users who are considered
trustworthy, but this should be done with care. It is also recommended
that any `~/.pgpass` file belonging to the server's user
*not* contain any records specifying a wildcard host name.

For further details see `dblink_connect()`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-connect-u.html)（英文原文，待翻譯）
