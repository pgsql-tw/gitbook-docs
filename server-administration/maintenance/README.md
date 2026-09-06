## Chapter 24. Routine Database Maintenance Tasks

**Table of Contents**

[24.1. Routine Vacuuming](routine-vacuuming.md)
:   [24.1.1. Vacuuming Basics](routine-vacuuming.md#VACUUM-BASICS)

    [24.1.2. Recovering Disk Space](routine-vacuuming.md#VACUUM-FOR-SPACE-RECOVERY)

    [24.1.3. Updating Planner Statistics](routine-vacuuming.md#VACUUM-FOR-STATISTICS)

    [24.1.4. Updating the Visibility Map](routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)

    [24.1.5. Preventing Transaction ID Wraparound Failures](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)

    [24.1.6. The Autovacuum Daemon](routine-vacuuming.md#AUTOVACUUM)

[24.2. Routine Reindexing](routine-reindex.md)

[24.3. Log File Maintenance](logfile-maintenance.md)

<a id="id-1.6.11.2"></a><a id="id-1.6.11.3"></a>

PostgreSQL, like any database software, requires that certain tasks
be performed regularly to achieve optimum performance. The tasks
discussed here are *required*, but they
are repetitive in nature and can easily be automated using standard
tools such as cron scripts or
Windows' Task Scheduler. It is the database
administrator's responsibility to set up appropriate scripts, and to
check that they execute successfully.

One obvious maintenance task is the creation of backup copies of the data on a
regular schedule. Without a recent backup, you have no chance of recovery
after a catastrophe (disk failure, fire, mistakenly dropping a critical
table, etc.). The backup and recovery mechanisms available in
PostgreSQL are discussed at length in
[Chapter 25](../backup/README.md).

The other main category of maintenance task is periodic “vacuuming”
of the database. This activity is discussed in
[Section 24.1](routine-vacuuming.md). Closely related to this is updating
the statistics that will be used by the query planner, as discussed in
[Section 24.1.3](routine-vacuuming.md#VACUUM-FOR-STATISTICS).

Another task that might need periodic attention is log file management.
This is discussed in [Section 24.3](logfile-maintenance.md).

[check_postgres](https://bucardo.org/check_postgres/)
is available for monitoring database health and reporting unusual
conditions. check_postgres integrates with
Nagios and MRTG, but can be run standalone too.

PostgreSQL is low-maintenance compared
to some other database management systems. Nonetheless,
appropriate attention to these tasks will go far towards ensuring a
pleasant and productive experience with the system.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/maintenance.html)（英文原文，待翻譯）
