## Chapter 25. Backup and Restore

**Table of Contents**

[25.1. SQL Dump](backup-dump.md)
:   [25.1.1. Restoring the Dump](backup-dump.md#BACKUP-DUMP-RESTORE)

    [25.1.2. Using pg_dumpall](backup-dump.md#BACKUP-DUMP-ALL)

    [25.1.3. Handling Large Databases](backup-dump.md#BACKUP-DUMP-LARGE)

[25.2. File System Level Backup](backup-file.md)

[25.3. Continuous Archiving and Point-in-Time Recovery (PITR)](continuous-archiving.md)
:   [25.3.1. Setting Up WAL Archiving](continuous-archiving.md#BACKUP-ARCHIVING-WAL)

    [25.3.2. Making a Base Backup](continuous-archiving.md#BACKUP-BASE-BACKUP)

    [25.3.3. Making an Incremental Backup](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)

    [25.3.4. Making a Base Backup Using the Low Level API](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)

    [25.3.5. Recovering Using a Continuous Archive Backup](continuous-archiving.md#BACKUP-PITR-RECOVERY)

    [25.3.6. Timelines](continuous-archiving.md#BACKUP-TIMELINES)

    [25.3.7. Tips and Examples](continuous-archiving.md#BACKUP-TIPS)

    [25.3.8. Caveats](continuous-archiving.md#CONTINUOUS-ARCHIVING-CAVEATS)

<a id="id-1.6.12.2"></a>

As with everything that contains valuable data, PostgreSQL
databases should be backed up regularly. While the procedure is
essentially simple, it is important to have a clear understanding of
the underlying techniques and assumptions.

There are three fundamentally different approaches to backing up
PostgreSQL data:

* SQL dump
* File system level backup
* Continuous archiving

Each has its own strengths and weaknesses; each is discussed in turn
in the following sections.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup.html)（英文原文，待翻譯）
