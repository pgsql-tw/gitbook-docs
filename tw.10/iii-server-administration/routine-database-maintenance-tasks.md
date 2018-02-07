# 24. 例行性資料庫維護工作[^1]

**Table of Contents**

[24.1. Routine Vacuuming](https://www.postgresql.org/docs/10/static/routine-vacuuming.html)

[24.1.1. Vacuuming Basics](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-BASICS)

[24.1.2. Recovering Disk Space](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-SPACE-RECOVERY)

[24.1.3. Updating Planner Statistics](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-STATISTICS)

[24.1.4. Updating The Visibility Map](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-VISIBILITY-MAP)

[24.1.5. Preventing Transaction ID Wraparound Failures](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND)

[24.1.6. The Autovacuum Daemon](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#AUTOVACUUM)

[24.2. Routine Reindexing](https://www.postgresql.org/docs/10/static/routine-reindex.html)

[24.3. Log File Maintenance](https://www.postgresql.org/docs/10/static/logfile-maintenance.html)





PostgreSQL, like any database software, requires that certain tasks be performed regularly to achieve optimum performance. The tasks discussed here are_required_, but they are repetitive in nature and can easily be automated using standard tools such ascronscripts or Windows'Task Scheduler. It is the database administrator's responsibility to set up appropriate scripts, and to check that they execute successfully.

One obvious maintenance task is the creation of backup copies of the data on a regular schedule. Without a recent backup, you have no chance of recovery after a catastrophe \(disk failure, fire, mistakenly dropping a critical table, etc.\). The backup and recovery mechanisms available inPostgreSQLare discussed at length in[Chapter 25](https://www.postgresql.org/docs/10/static/backup.html).

The other main category of maintenance task is periodic“vacuuming”of the database. This activity is discussed in[Section 24.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html). Closely related to this is updating the statistics that will be used by the query planner, as discussed in[Section 24.1.3](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-STATISTICS).

Another task that might need periodic attention is log file management. This is discussed in[Section 24.3](https://www.postgresql.org/docs/10/static/logfile-maintenance.html).

[check\_postgres](https://bucardo.org/check_postgres/)is available for monitoring database health and reporting unusual conditions.check\_postgresintegrates with Nagios and MRTG, but can be run standalone too.

PostgreSQLis low-maintenance compared to some other database management systems. Nonetheless, appropriate attention to these tasks will go far towards ensuring a pleasant and productive experience with the system.

  


---



[^1]: [PostgreSQL: Documentation: 10: Chapter 24. Routine Database Maintenance Tasks](https://www.postgresql.org/docs/10/static/maintenance.html)

