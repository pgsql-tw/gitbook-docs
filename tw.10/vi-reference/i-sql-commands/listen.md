# LISTEN[^1]

LISTEN — listen for a notification

## Synopsis

```
LISTEN 
channel
```

## Description

`LISTEN`registers the current session as a listener on the notification channel named_`channel`_. If the current session is already registered as a listener for this notification channel, nothing is done.

Whenever the command`NOTIFY`_`channel`_is invoked, either by this session or another one connected to the same database, all the sessions currently listening on that notification channel are notified, and each will in turn notify its connected client application.

A session can be unregistered for a given notification channel with the`UNLISTEN`command. A session's listen registrations are automatically cleared when the session ends.

The method a client application must use to detect notification events depends on whichPostgreSQLapplication programming interface it uses. With thelibpqlibrary, the application issues`LISTEN`as an ordinary SQL command, and then must periodically call the function`PQnotifies`to find out whether any notification events have been received. Other interfaces such aslibpgtclprovide higher-level methods for handling notify events; indeed, withlibpgtclthe application programmer should not even issue`LISTEN`or`UNLISTEN`directly. See the documentation for the interface you are using for more details.

[NOTIFY](https://www.postgresql.org/docs/10/static/sql-notify.html)contains a more extensive discussion of the use of`LISTEN`and`NOTIFY`.

## Parameters

_`channel`_

Name of a notification channel \(any identifier\).

## Notes

`LISTEN`takes effect at transaction commit. If`LISTEN`or`UNLISTEN`is executed within a transaction that later rolls back, the set of notification channels being listened to is unchanged.

A transaction that has executed`LISTEN`cannot be prepared for two-phase commit.

## Examples

Configure and execute a listen/notify sequence frompsql:

```
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

## Compatibility

There is no`LISTEN`statement in the SQL standard.

## See Also

[NOTIFY](https://www.postgresql.org/docs/10/static/sql-notify.html)

,

[UNLISTEN](https://www.postgresql.org/docs/10/static/sql-unlisten.html)

---



[^1]:  [PostgreSQL: Documentation: 10: LISTEN](https://www.postgresql.org/docs/10/static/sql-listen.html)

