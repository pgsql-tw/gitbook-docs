<a id="id-1.9.3.153.1"></a>

## LISTEN

LISTEN — listen for a notification

## Synopsis

```

LISTEN channel
```

<a id="id-1.9.3.153.5"></a>

## Description

`LISTEN` registers the current session as a
listener on the notification channel named *`channel`*.
If the current session is already registered as a listener for
this notification channel, nothing is done.

Whenever the command `NOTIFY channel` is invoked, either
by this session or another one connected to the same database, all
the sessions currently listening on that notification channel are
notified, and each will in turn notify its connected client
application.

A session can be unregistered for a given notification channel with the
`UNLISTEN` command. A session's listen
registrations are automatically cleared when the session ends.

The method a client application must use to detect notification events depends on
which PostgreSQL application programming interface it
uses. With the libpq library, the application issues
`LISTEN` as an ordinary SQL command, and then must
periodically call the function `PQnotifies` to find out
whether any notification events have been received. Other interfaces such as
libpgtcl provide higher-level methods for handling notify events; indeed,
with libpgtcl the application programmer should not even issue
`LISTEN` or `UNLISTEN` directly. See the
documentation for the interface you are using for more details.

<a id="id-1.9.3.153.6"></a>

## Parameters

*`channel`*
:   Name of a notification channel (any identifier).

<a id="id-1.9.3.153.7"></a>

## Notes

`LISTEN` takes effect at transaction commit.
If `LISTEN` or `UNLISTEN` is executed
within a transaction that later rolls back, the set of notification
channels being listened to is unchanged.

A transaction that has executed `LISTEN` cannot be
prepared for two-phase commit.

There is a race condition when first setting up a listening session:
if concurrently-committing transactions are sending notify events,
exactly which of those will the newly listening session receive?
The answer is that the session will receive all events committed after
an instant during the transaction's commit step. But that is slightly
later than any database state that the transaction could have observed
in queries. This leads to the following rule for
using `LISTEN`: first execute (and commit!) that
command, then in a new transaction inspect the database state as needed
by the application logic, then rely on notifications to find out about
subsequent changes to the database state. The first few received
notifications might refer to updates already observed in the initial
database inspection, but this is usually harmless.

[NOTIFY](sql-notify.md)
contains a more extensive
discussion of the use of `LISTEN` and
`NOTIFY`.

<a id="id-1.9.3.153.8"></a>

## Examples

Configure and execute a listen/notify sequence from
psql:

```

LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

<a id="id-1.9.3.153.9"></a>

## Compatibility

There is no `LISTEN` statement in the SQL
standard.

<a id="id-1.9.3.153.10"></a>

## See Also

[NOTIFY](sql-notify.md), [UNLISTEN](sql-unlisten.md), [max_notify_queue_pages](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-NOTIFY-QUEUE-PAGES)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-listen.html)（英文原文，待翻譯）
