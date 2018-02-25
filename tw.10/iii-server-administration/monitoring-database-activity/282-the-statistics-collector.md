# 28.2. 統計資訊收集器

[28.2.1. Statistics Collection Configuration](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-SETUP)

[28.2.2. Viewing Statistics](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-VIEWS)

[28.2.3. Statistics Functions](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-FUNCTIONS)



PostgreSQL's_statistics collector_is a subsystem that supports collection and reporting of information about server activity. Presently, the collector can count accesses to tables and indexes in both disk-block and individual-row terms. It also tracks the total number of rows in each table, and information about vacuum and analyze actions for each table. It can also count calls to user-defined functions and the total time spent in each one.

PostgreSQLalso supports reporting dynamic information about exactly what is going on in the system right now, such as the exact command currently being executed by other server processes, and which other connections exist in the system. This facility is independent of the collector process.

### 28.2.1. Statistics Collection Configuration

Since collection of statistics adds some overhead to query execution, the system can be configured to collect or not collect information. This is controlled by configuration parameters that are normally set in`postgresql.conf`. \(See[Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html)for details about setting configuration parameters.\)

The parameter[track\_activities](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-ACTIVITIES)enables monitoring of the current command being executed by any server process.

The parameter[track\_counts](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-COUNTS)controls whether statistics are collected about table and index accesses.

The parameter[track\_functions](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-FUNCTIONS)enables tracking of usage of user-defined functions.

The parameter[track\_io\_timing](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-IO-TIMING)enables monitoring of block read and write times.

Normally these parameters are set in`postgresql.conf`so that they apply to all server processes, but it is possible to turn them on or off in individual sessions using the[SET](https://www.postgresql.org/docs/10/static/sql-set.html)command. \(To prevent ordinary users from hiding their activity from the administrator, only superusers are allowed to change these parameters with`SET`.\)

The statistics collector transmits the collected information to otherPostgreSQLprocesses through temporary files. These files are stored in the directory named by the[stats\_temp\_directory](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-STATS-TEMP-DIRECTORY)parameter,`pg_stat_tmp`by default. For better performance,`stats_temp_directory`can be pointed at a RAM-based file system, decreasing physical I/O requirements. When the server shuts down cleanly, a permanent copy of the statistics data is stored in the`pg_stat`subdirectory, so that statistics can be retained across server restarts. When recovery is performed at server start \(e.g. after immediate shutdown, server crash, and point-in-time recovery\), all statistics counters are reset.

