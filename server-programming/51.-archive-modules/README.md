# 51. Archive Modules

PostgreSQL provides infrastructure to create custom modules for continuous archiving (see [Section 26.3](https://www.postgresql.org/docs/15/continuous-archiving.html)). While archiving via a shell command (i.e., [archive\_command](https://www.postgresql.org/docs/15/runtime-config-wal.html#GUC-ARCHIVE-COMMAND)) is much simpler, a custom archive module will often be considerably more robust and performant.

When a custom [archive\_library](https://www.postgresql.org/docs/15/runtime-config-wal.html#GUC-ARCHIVE-LIBRARY) is configured, PostgreSQL will submit completed WAL files to the module, and the server will avoid recycling or removing these WAL files until the module indicates that the files were successfully archived. It is ultimately up to the module to decide what to do with each WAL file, but many recommendations are listed at [Section 26.3.1](https://www.postgresql.org/docs/15/continuous-archiving.html#BACKUP-ARCHIVING-WAL).

Archiving modules must at least consist of an initialization function (see [Section 51.1](https://www.postgresql.org/docs/15/archive-module-init.html)) and the required callbacks (see [Section 51.2](https://www.postgresql.org/docs/15/archive-module-callbacks.html)). However, archive modules are also permitted to do much more (e.g., declare GUCs and register background workers).

The `contrib/basic_archive` module contains a working example, which demonstrates some useful techniques.
