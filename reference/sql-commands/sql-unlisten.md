<a id="id-1.9.3.182.1"></a>

## UNLISTEN

UNLISTEN — stop listening for a notification

## Synopsis

```

UNLISTEN { channel | * }
```

<a id="id-1.9.3.182.5"></a>

## Description

`UNLISTEN` is used to remove an existing
registration for `NOTIFY` events.
`UNLISTEN` cancels any existing registration of
the current PostgreSQL session as a
listener on the notification channel named *`channel`*. The special wildcard
`*` cancels all listener registrations for the
current session.

[NOTIFY](sql-notify.md)
contains a more extensive
discussion of the use of `LISTEN` and
`NOTIFY`.

<a id="id-1.9.3.182.6"></a>

## Parameters

*`channel`*
:   Name of a notification channel (any identifier).

`*`
:   All current listen registrations for this session are cleared.

<a id="id-1.9.3.182.7"></a>

## Notes

You can unlisten something you were not listening for; no warning or error
will appear.

At the end of each session, `UNLISTEN *` is
automatically executed.

A transaction that has executed `UNLISTEN` cannot be
prepared for two-phase commit.

<a id="id-1.9.3.182.8"></a>

## Examples

To make a registration:

```

LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

Once `UNLISTEN` has been executed, further `NOTIFY`
messages will be ignored:

```

UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

<a id="id-1.9.3.182.9"></a>

## Compatibility

There is no `UNLISTEN` command in the SQL standard.

<a id="id-1.9.3.182.10"></a>

## See Also

[LISTEN](sql-listen.md), [NOTIFY](sql-notify.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-unlisten.html)（英文原文，待翻譯）
