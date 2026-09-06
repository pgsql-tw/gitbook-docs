<a id="id-1.9.3.49.1"></a>

## CHECKPOINT

CHECKPOINT — force a write-ahead log checkpoint

## Synopsis

```

CHECKPOINT
```

<a id="id-1.9.3.49.5"></a>

## Description

A checkpoint is a point in the write-ahead log sequence at which
all data files have been updated to reflect the information in the
log. All data files will be flushed to disk. Refer to
[Section 28.5](../../server-administration/wal/wal-configuration.md) for more details about what happens
during a checkpoint.

The `CHECKPOINT` command forces an immediate
checkpoint when the command is issued, without waiting for a
regular checkpoint scheduled by the system (controlled by the settings in
[Section 19.5.2](../../server-administration/runtime-config/runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)).
`CHECKPOINT` is not intended for use during normal
operation.

If executed during recovery, the `CHECKPOINT` command
will force a restartpoint (see [Section 28.5](../../server-administration/wal/wal-configuration.md))
rather than writing a new checkpoint.

Only superusers or users with the privileges of
the [pg_checkpoint](../../server-administration/user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-CHECKPOINT)
role can call `CHECKPOINT`.

<a id="id-1.9.3.49.6"></a>

## Compatibility

The `CHECKPOINT` command is a
PostgreSQL language extension.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-checkpoint.html)（英文原文，待翻譯）
