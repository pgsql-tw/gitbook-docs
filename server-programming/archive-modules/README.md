## Chapter 49. Archive Modules

**Table of Contents**

[49.1. Initialization Functions](archive-module-init.md)

[49.2. Archive Module Callbacks](archive-module-callbacks.md)
:   [49.2.1. Startup Callback](archive-module-callbacks.md#ARCHIVE-MODULE-STARTUP)

    [49.2.2. Check Callback](archive-module-callbacks.md#ARCHIVE-MODULE-CHECK)

    [49.2.3. Archive Callback](archive-module-callbacks.md#ARCHIVE-MODULE-ARCHIVE)

    [49.2.4. Shutdown Callback](archive-module-callbacks.md#ARCHIVE-MODULE-SHUTDOWN)

<a id="id-1.8.16.2"></a>

PostgreSQL provides infrastructure to create custom modules for continuous
archiving (see [Section 25.3](../../server-administration/backup/continuous-archiving.md)). While archiving via
a shell command (i.e., [archive_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND)) is much
simpler, a custom archive module will often be considerably more robust and
performant.

When a custom [archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) is configured, PostgreSQL
will submit completed WAL files to the module, and the server will avoid
recycling or removing these WAL files until the module indicates that the files
were successfully archived. It is ultimately up to the module to decide what
to do with each WAL file, but many recommendations are listed at
[Section 25.3.1](../../server-administration/backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL).

Archiving modules must at least consist of an initialization function (see
[Section 49.1](archive-module-init.md)) and the required callbacks (see
[Section 49.2](archive-module-callbacks.md)). However, archive modules are
also permitted to do much more (e.g., declare GUCs and register background
workers).

The `contrib/basic_archive` module contains a working
example, which demonstrates some useful techniques.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/archive-modules.html)（英文原文，待翻譯）
