## 27.4. Progress Reporting [#](#PROGRESS-REPORTING)

[27.4.1. ANALYZE Progress Reporting](progress-reporting.md#ANALYZE-PROGRESS-REPORTING)

[27.4.2. CLUSTER Progress Reporting](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)

[27.4.3. COPY Progress Reporting](progress-reporting.md#COPY-PROGRESS-REPORTING)

[27.4.4. CREATE INDEX Progress Reporting](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)

[27.4.5. VACUUM Progress Reporting](progress-reporting.md#VACUUM-PROGRESS-REPORTING)

[27.4.6. Base Backup Progress Reporting](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING)

PostgreSQL has the ability to report the progress of
certain commands during command execution. Currently, the only commands
which support progress reporting are `ANALYZE`,
`CLUSTER`,
`CREATE INDEX`, `VACUUM`,
`COPY`,
and [BASE_BACKUP](../../internals/protocol/protocol-replication.md#PROTOCOL-REPLICATION-BASE-BACKUP) (i.e., replication
command that [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md) issues to take
a base backup).
This may be expanded in the future.

<a id="ANALYZE-PROGRESS-REPORTING"></a>

### 27.4.1. ANALYZE Progress Reporting [#](#ANALYZE-PROGRESS-REPORTING)

<a id="id-1.6.14.9.3.2"></a>

Whenever `ANALYZE` is running, the
`pg_stat_progress_analyze` view will contain a
row for each backend that is currently running that command. The tables
below describe the information that will be reported and provide
information about how to interpret it.

<a id="PG-STAT-PROGRESS-ANALYZE-VIEW"></a>

**Table 27.38. `pg_stat_progress_analyze` View**

<table border="1" class="table" summary="pg_stat_progress_analyze View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of backend.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table being analyzed.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       Current processing phase. See <a class="xref" href="progress-reporting.md#ANALYZE-PHASES">Table 27.39</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sample_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of heap blocks that will be sampled.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sample_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap blocks scanned.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ext_stats_total</code> <code class="type">bigint</code>
</p>
<p>
       Number of extended statistics.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ext_stats_computed</code> <code class="type">bigint</code>
</p>
<p>
       Number of extended statistics computed. This counter only advances
       when the phase is <code class="literal">computing extended statistics</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">child_tables_total</code> <code class="type">bigint</code>
</p>
<p>
       Number of child tables.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">child_tables_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of child tables scanned. This counter only advances when the
       phase is <code class="literal">acquiring inherited sample rows</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">current_child_table_relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the child table currently being scanned. This field is
       only valid when the phase is
       <code class="literal">acquiring inherited sample rows</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delay_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent sleeping due to cost-based delay (see
       <a class="xref" href="../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST">Section 19.10.2</a>), in milliseconds
       (if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a> is enabled, otherwise
       zero).
      </p></td></tr></tbody></table>

<br><a id="ANALYZE-PHASES"></a>

**Table 27.39. ANALYZE Phases**

<table border="1" class="table" summary="ANALYZE Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Phase</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       The command is preparing to begin scanning the heap.  This phase is
       expected to be very brief.
      </td></tr><tr><td><code class="literal">acquiring sample rows</code></td><td>
       The command is currently scanning the table given by
       <code class="structfield">relid</code> to obtain sample rows.
      </td></tr><tr><td><code class="literal">acquiring inherited sample rows</code></td><td>
       The command is currently scanning child tables to obtain sample rows.
       Columns <code class="structfield">child_tables_total</code>,
       <code class="structfield">child_tables_done</code>, and
       <code class="structfield">current_child_table_relid</code> contain the
       progress information for this phase.
      </td></tr><tr><td><code class="literal">computing statistics</code></td><td>
       The command is computing statistics from the sample rows obtained
       during the table scan.
      </td></tr><tr><td><code class="literal">computing extended statistics</code></td><td>
       The command is computing extended statistics from the sample rows
       obtained during the table scan.
      </td></tr><tr><td><code class="literal">finalizing analyze</code></td><td>
       The command is updating <code class="structname">pg_class</code>. When this
       phase is completed, <code class="command">ANALYZE</code> will end.
      </td></tr></tbody></table>

<br>

### Note

Note that when `ANALYZE` is run on a partitioned table
without the `ONLY` keyword, all of its partitions are
also recursively analyzed. In that case, `ANALYZE`
progress is reported first for the parent table, whereby its inheritance
statistics are collected, followed by that for each partition.

<a id="CLUSTER-PROGRESS-REPORTING"></a>

### 27.4.2. CLUSTER Progress Reporting [#](#CLUSTER-PROGRESS-REPORTING)

<a id="id-1.6.14.9.4.2"></a>

Whenever `CLUSTER` or `VACUUM FULL` is
running, the `pg_stat_progress_cluster` view will
contain a row for each backend that is currently running either command.
The tables below describe the information that will be reported and
provide information about how to interpret it.

<a id="PG-STAT-PROGRESS-CLUSTER-VIEW"></a>

**Table 27.40. `pg_stat_progress_cluster` View**

<table border="1" class="table" summary="pg_stat_progress_cluster View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of backend.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table being clustered.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       The command that is running. Either <code class="literal">CLUSTER</code> or <code class="literal">VACUUM FULL</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       Current processing phase. See <a class="xref" href="progress-reporting.md#CLUSTER-PHASES">Table 27.41</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cluster_index_relid</code> <code class="type">oid</code>
</p>
<p>
       If the table is being scanned using an index, this is the OID of the
       index being used; otherwise, it is zero.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_tuples_scanned</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap tuples scanned.
       This counter only advances when the phase is
       <code class="literal">seq scanning heap</code>,
       <code class="literal">index scanning heap</code>
       or <code class="literal">writing new heap</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_tuples_written</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap tuples written.
       This counter only advances when the phase is
       <code class="literal">seq scanning heap</code>,
       <code class="literal">index scanning heap</code>
       or <code class="literal">writing new heap</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of heap blocks in the table.  This number is reported
       as of the beginning of <code class="literal">seq scanning heap</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap blocks scanned.  This counter only advances when the
       phase is <code class="literal">seq scanning heap</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_rebuild_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of indexes rebuilt.  This counter only advances when the phase
       is <code class="literal">rebuilding index</code>.
      </p></td></tr></tbody></table>

<br><a id="CLUSTER-PHASES"></a>

**Table 27.41. CLUSTER and VACUUM FULL Phases**

<table border="1" class="table" summary="CLUSTER and VACUUM FULL Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Phase</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       The command is preparing to begin scanning the heap.  This phase is
       expected to be very brief.
     </td></tr><tr><td><code class="literal">seq scanning heap</code></td><td>
       The command is currently scanning the table using a sequential scan.
     </td></tr><tr><td><code class="literal">index scanning heap</code></td><td>
<code class="command">CLUSTER</code> is currently scanning the table using an index scan.
     </td></tr><tr><td><code class="literal">sorting tuples</code></td><td>
<code class="command">CLUSTER</code> is currently sorting tuples.
     </td></tr><tr><td><code class="literal">writing new heap</code></td><td>
<code class="command">CLUSTER</code> is currently writing the new heap.
     </td></tr><tr><td><code class="literal">swapping relation files</code></td><td>
       The command is currently swapping newly-built files into place.
     </td></tr><tr><td><code class="literal">rebuilding index</code></td><td>
       The command is currently rebuilding an index.
     </td></tr><tr><td><code class="literal">performing final cleanup</code></td><td>
       The command is performing final cleanup.  When this phase is
       completed, <code class="command">CLUSTER</code>
       or <code class="command">VACUUM FULL</code> will end.
     </td></tr></tbody></table>

<br>

<a id="COPY-PROGRESS-REPORTING"></a>

### 27.4.3. COPY Progress Reporting [#](#COPY-PROGRESS-REPORTING)

<a id="id-1.6.14.9.5.2"></a>

Whenever `COPY` is running, the
`pg_stat_progress_copy` view will contain one row
for each backend that is currently running a `COPY` command.
The table below describes the information that will be reported and provides
information about how to interpret it.

<a id="PG-STAT-PROGRESS-COPY-VIEW"></a>

**Table 27.42. `pg_stat_progress_copy` View**

<table border="1" class="table" summary="pg_stat_progress_copy View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of backend.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table on which the <code class="command">COPY</code> command is
       executed. It is set to <code class="literal">0</code> if copying from a
       <code class="command">SELECT</code> query.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       The command that is running: <code class="literal">COPY FROM</code>, or
       <code class="literal">COPY TO</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       The I/O type that the data is read from or written to:
       <code class="literal">FILE</code>, <code class="literal">PROGRAM</code>,
       <code class="literal">PIPE</code> (for <code class="command">COPY FROM STDIN</code> and
       <code class="command">COPY TO STDOUT</code>), or <code class="literal">CALLBACK</code>
       (used for example during the initial table synchronization in
       logical replication).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_processed</code> <code class="type">bigint</code>
</p>
<p>
       Number of bytes already processed by <code class="command">COPY</code> command.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_total</code> <code class="type">bigint</code>
</p>
<p>
       Size of source file for <code class="command">COPY FROM</code> command in bytes.
       It is set to <code class="literal">0</code> if not available.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_processed</code> <code class="type">bigint</code>
</p>
<p>
       Number of tuples already processed by <code class="command">COPY</code> command.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_excluded</code> <code class="type">bigint</code>
</p>
<p>
       Number of tuples not processed because they were excluded by the
       <code class="command">WHERE</code> clause of the <code class="command">COPY</code> command.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_skipped</code> <code class="type">bigint</code>
</p>
<p>
       Number of tuples skipped because they contain malformed data.
       This counter only advances when a value other than
       <code class="literal">stop</code> is specified to the <code class="literal">ON_ERROR</code>
       option.
      </p></td></tr></tbody></table>

<br>

<a id="CREATE-INDEX-PROGRESS-REPORTING"></a>

### 27.4.4. CREATE INDEX Progress Reporting [#](#CREATE-INDEX-PROGRESS-REPORTING)

<a id="id-1.6.14.9.6.2"></a>

Whenever `CREATE INDEX` or `REINDEX` is running, the
`pg_stat_progress_create_index` view will contain
one row for each backend that is currently creating indexes. The tables
below describe the information that will be reported and provide information
about how to interpret it.

<a id="PG-STAT-PROGRESS-CREATE-INDEX-VIEW"></a>

**Table 27.43. `pg_stat_progress_create_index` View**

<table border="1" class="table" summary="pg_stat_progress_create_index View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of the backend creating indexes.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table on which the index is being created.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the index being created or reindexed.  During a
       non-concurrent <code class="command">CREATE INDEX</code>, this is 0.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       Specific command type: <code class="literal">CREATE INDEX</code>,
       <code class="literal">CREATE INDEX CONCURRENTLY</code>,
       <code class="literal">REINDEX</code>, or <code class="literal">REINDEX CONCURRENTLY</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       Current processing phase of index creation.  See <a class="xref" href="progress-reporting.md#CREATE-INDEX-PHASES">Table 27.44</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lockers_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of lockers to wait for, when applicable.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lockers_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of lockers already waited for.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">current_locker_pid</code> <code class="type">bigint</code>
</p>
<p>
       Process ID of the locker currently being waited for.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blocks_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of blocks to be processed in the current phase.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blocks_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of blocks already processed in the current phase.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of tuples to be processed in the current phase.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of tuples already processed in the current phase.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partitions_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of partitions on which the index is to be created
       or attached, including both direct and indirect partitions.
       <code class="literal">0</code> during a <code class="literal">REINDEX</code>, or when
       the index is not partitioned.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partitions_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of partitions on which the index has already been created
       or attached, including both direct and indirect partitions.
       <code class="literal">0</code> during a <code class="literal">REINDEX</code>, or when
       the index is not partitioned.
      </p></td></tr></tbody></table>

<br><a id="CREATE-INDEX-PHASES"></a>

**Table 27.44. CREATE INDEX Phases**

<table border="1" class="table" summary="CREATE INDEX Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Phase</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
<code class="command">CREATE INDEX</code> or <code class="command">REINDEX</code> is preparing to create the index.  This
       phase is expected to be very brief.
      </td></tr><tr><td><code class="literal">waiting for writers before build</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> or <code class="command">REINDEX CONCURRENTLY</code> is waiting for transactions
       with write locks that can potentially see the table to finish.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">lockers_total</code>, <code class="structname">lockers_done</code>
       and <code class="structname">current_locker_pid</code> contain the progress
       information for this phase.
      </td></tr><tr><td><code class="literal">building index</code></td><td>
       The index is being built by the access method-specific code.  In this phase,
       access methods that support progress reporting fill in their own progress data,
       and the subphase is indicated in this column.  Typically,
       <code class="structname">blocks_total</code> and <code class="structname">blocks_done</code>
       will contain progress data, as well as potentially
       <code class="structname">tuples_total</code> and <code class="structname">tuples_done</code>.
      </td></tr><tr><td><code class="literal">waiting for writers before validation</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> or <code class="command">REINDEX CONCURRENTLY</code> is waiting for transactions
       with write locks that can potentially write into the table to finish.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">lockers_total</code>, <code class="structname">lockers_done</code>
       and <code class="structname">current_locker_pid</code> contain the progress
       information for this phase.
      </td></tr><tr><td><code class="literal">index validation: scanning index</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> is scanning the index searching
       for tuples that need to be validated.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">blocks_total</code> (set to the total size of the index)
       and <code class="structname">blocks_done</code> contain the progress information for this phase.
      </td></tr><tr><td><code class="literal">index validation: sorting tuples</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> is sorting the output of the
       index scanning phase.
      </td></tr><tr><td><code class="literal">index validation: scanning table</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> is scanning the table
       to validate the index tuples collected in the previous two phases.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">blocks_total</code> (set to the total size of the table)
       and <code class="structname">blocks_done</code> contain the progress information for this phase.
      </td></tr><tr><td><code class="literal">waiting for old snapshots</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> or <code class="command">REINDEX CONCURRENTLY</code> is waiting for transactions
       that can potentially see the table to release their snapshots.  This
       phase is skipped when not in concurrent mode.
       Columns <code class="structname">lockers_total</code>, <code class="structname">lockers_done</code>
       and <code class="structname">current_locker_pid</code> contain the progress
       information for this phase.
      </td></tr><tr><td><code class="literal">waiting for readers before marking dead</code></td><td>
<code class="command">REINDEX CONCURRENTLY</code> is waiting for transactions
       with read locks on the table to finish, before marking the old index dead.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">lockers_total</code>, <code class="structname">lockers_done</code>
       and <code class="structname">current_locker_pid</code> contain the progress
       information for this phase.
      </td></tr><tr><td><code class="literal">waiting for readers before dropping</code></td><td>
<code class="command">REINDEX CONCURRENTLY</code> is waiting for transactions
       with read locks on the table to finish, before dropping the old index.
       This phase is skipped when not in concurrent mode.
       Columns <code class="structname">lockers_total</code>, <code class="structname">lockers_done</code>
       and <code class="structname">current_locker_pid</code> contain the progress
       information for this phase.
      </td></tr></tbody></table>

<br>

<a id="VACUUM-PROGRESS-REPORTING"></a>

### 27.4.5. VACUUM Progress Reporting [#](#VACUUM-PROGRESS-REPORTING)

<a id="id-1.6.14.9.7.2"></a>

Whenever `VACUUM` is running, the
`pg_stat_progress_vacuum` view will contain
one row for each backend (including autovacuum worker processes) that is
currently vacuuming. The tables below describe the information
that will be reported and provide information about how to interpret it.
Progress for `VACUUM FULL` commands is reported via
`pg_stat_progress_cluster`
because both `VACUUM FULL` and `CLUSTER`
rewrite the table, while regular `VACUUM` only modifies it
in place. See [Section 27.4.2](progress-reporting.md#CLUSTER-PROGRESS-REPORTING).

<a id="PG-STAT-PROGRESS-VACUUM-VIEW"></a>

**Table 27.45. `pg_stat_progress_vacuum` View**

<table border="1" class="table" summary="pg_stat_progress_vacuum View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of backend.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database to which this backend is connected.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table being vacuumed.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       Current processing phase of vacuum.  See <a class="xref" href="progress-reporting.md#VACUUM-PHASES">Table 27.46</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of heap blocks in the table.  This number is reported
       as of the beginning of the scan; blocks added later will not be (and
       need not be) visited by this <code class="command">VACUUM</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap blocks scanned.  Because the
       <a class="link" href="../../internals/storage/storage-vm.md">visibility map</a> is used to optimize scans,
       some blocks will be skipped without inspection; skipped blocks are
       included in this total, so that this number will eventually become
       equal to <code class="structfield">heap_blks_total</code> when the vacuum is complete.
       This counter only advances when the phase is <code class="literal">scanning heap</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_vacuumed</code> <code class="type">bigint</code>
</p>
<p>
       Number of heap blocks vacuumed.  Unless the table has no indexes, this
       counter only advances when the phase is <code class="literal">vacuuming heap</code>.
       Blocks that contain no dead tuples are skipped, so the counter may
       sometimes skip forward in large increments.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_vacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of completed index vacuum cycles.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_dead_tuple_bytes</code> <code class="type">bigint</code>
</p>
<p>
       Amount of dead tuple data that we can store before needing to perform
       an index vacuum cycle, based on
       <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dead_tuple_bytes</code> <code class="type">bigint</code>
</p>
<p>
       Amount of dead tuple data collected since the last index vacuum cycle.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_dead_item_ids</code> <code class="type">bigint</code>
</p>
<p>
       Number of dead item identifiers collected since the last index vacuum cycle.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexes_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of indexes that will be vacuumed or cleaned up. This
       number is reported at the beginning of the
       <code class="literal">vacuuming indexes</code> phase or the
       <code class="literal">cleaning up indexes</code> phase.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexes_processed</code> <code class="type">bigint</code>
</p>
<p>
       Number of indexes processed. This counter only advances when the
       phase is <code class="literal">vacuuming indexes</code> or
       <code class="literal">cleaning up indexes</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delay_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent sleeping due to cost-based delay (see
       <a class="xref" href="../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST">Section 19.10.2</a>), in milliseconds
       (if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a> is enabled, otherwise
       zero).  This includes the time that any associated parallel workers have
       slept.  However, parallel workers report their sleep time no more
       frequently than once per second, so the reported value may be slightly
       stale.
      </p></td></tr></tbody></table>

<br><a id="VACUUM-PHASES"></a>

**Table 27.46. VACUUM Phases**

<table border="1" class="table" summary="VACUUM Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Phase</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
<code class="command">VACUUM</code> is preparing to begin scanning the heap.  This
       phase is expected to be very brief.
     </td></tr><tr><td><code class="literal">scanning heap</code></td><td>
<code class="command">VACUUM</code> is currently scanning the heap.  It will prune and
       defragment each page if required, and possibly perform freezing
       activity.  The <code class="structfield">heap_blks_scanned</code> column can be used
       to monitor the progress of the scan.
     </td></tr><tr><td><code class="literal">vacuuming indexes</code></td><td>
<code class="command">VACUUM</code> is currently vacuuming the indexes.  If a table has
       any indexes, this will happen at least once per vacuum, after the heap
       has been completely scanned.  It may happen multiple times per vacuum
       if <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a> (or, in the case of autovacuum,
       <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM">autovacuum_work_mem</a> if set) is insufficient to store
       the number of dead tuples found.
     </td></tr><tr><td><code class="literal">vacuuming heap</code></td><td>
<code class="command">VACUUM</code> is currently vacuuming the heap.  Vacuuming the heap
       is distinct from scanning the heap, and occurs after each instance of
       vacuuming indexes.  If <code class="structfield">heap_blks_scanned</code> is less than
       <code class="structfield">heap_blks_total</code>, the system will return to scanning
       the heap after this phase is completed; otherwise, it will begin
       cleaning up indexes after this phase is completed.
     </td></tr><tr><td><code class="literal">cleaning up indexes</code></td><td>
<code class="command">VACUUM</code> is currently cleaning up indexes.  This occurs after
       the heap has been completely scanned and all vacuuming of the indexes
       and the heap has been completed.
     </td></tr><tr><td><code class="literal">truncating heap</code></td><td>
<code class="command">VACUUM</code> is currently truncating the heap so as to return
       empty pages at the end of the relation to the operating system.  This
       occurs after cleaning up indexes.
     </td></tr><tr><td><code class="literal">performing final cleanup</code></td><td>
<code class="command">VACUUM</code> is performing final cleanup.  During this phase,
       <code class="command">VACUUM</code> will vacuum the free space map, update statistics
       in <code class="literal">pg_class</code>, and report statistics to the cumulative
       statistics system. When this phase is completed, <code class="command">VACUUM</code> will end.
     </td></tr></tbody></table>

<br>

<a id="BASEBACKUP-PROGRESS-REPORTING"></a>

### 27.4.6. Base Backup Progress Reporting [#](#BASEBACKUP-PROGRESS-REPORTING)

<a id="id-1.6.14.9.8.2"></a>

Whenever an application like pg_basebackup
is taking a base backup, the
`pg_stat_progress_basebackup`
view will contain a row for each WAL sender process that is currently
running the `BASE_BACKUP` replication command
and streaming the backup. The tables below describe the information
that will be reported and provide information about how to interpret it.

<a id="PG-STAT-PROGRESS-BASEBACKUP-VIEW"></a>

**Table 27.47. `pg_stat_progress_basebackup` View**

<table border="1" class="table" summary="pg_stat_progress_basebackup View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of a WAL sender process.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       Current processing phase. See <a class="xref" href="progress-reporting.md#BASEBACKUP-PHASES">Table 27.48</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_total</code> <code class="type">bigint</code>
</p>
<p>
       Total amount of data that will be streamed. This is estimated and
       reported as of the beginning of
       <code class="literal">streaming database files</code> phase. Note that
       this is only an approximation since the database
       may change during <code class="literal">streaming database files</code> phase
       and WAL log may be included in the backup later. This is always
       the same value as <code class="structfield">backup_streamed</code>
       once the amount of data streamed exceeds the estimated
       total size. If the estimation is disabled in
       <span class="application">pg_basebackup</span>
       (i.e., <code class="literal">--no-estimate-size</code> option is specified),
       this is <code class="literal">NULL</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_streamed</code> <code class="type">bigint</code>
</p>
<p>
       Amount of data streamed. This counter only advances
       when the phase is <code class="literal">streaming database files</code> or
       <code class="literal">transferring wal files</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_total</code> <code class="type">bigint</code>
</p>
<p>
       Total number of tablespaces that will be streamed.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_streamed</code> <code class="type">bigint</code>
</p>
<p>
       Number of tablespaces streamed. This counter only
       advances when the phase is <code class="literal">streaming database files</code>.
      </p></td></tr></tbody></table>

<br><a id="BASEBACKUP-PHASES"></a>

**Table 27.48. Base Backup Phases**

<table border="1" class="table" summary="Base Backup Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Phase</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       The WAL sender process is preparing to begin the backup.
       This phase is expected to be very brief.
      </td></tr><tr><td><code class="literal">waiting for checkpoint to finish</code></td><td>
       The WAL sender process is currently performing
       <code class="function">pg_backup_start</code> to prepare to
       take a base backup, and waiting for the start-of-backup
       checkpoint to finish.
      </td></tr><tr><td><code class="literal">estimating backup size</code></td><td>
       The WAL sender process is currently estimating the total amount
       of database files that will be streamed as a base backup.
      </td></tr><tr><td><code class="literal">streaming database files</code></td><td>
       The WAL sender process is currently streaming database files
       as a base backup.
      </td></tr><tr><td><code class="literal">waiting for wal archiving to finish</code></td><td>
       The WAL sender process is currently performing
       <code class="function">pg_backup_stop</code> to finish the backup,
       and waiting for all the WAL files required for the base backup
       to be successfully archived.
       If either <code class="literal">--wal-method=none</code> or
       <code class="literal">--wal-method=stream</code> is specified in
       <span class="application">pg_basebackup</span>, the backup will end
       when this phase is completed.
      </td></tr><tr><td><code class="literal">transferring wal files</code></td><td>
       The WAL sender process is currently transferring all WAL logs
       generated during the backup. This phase occurs after
       <code class="literal">waiting for wal archiving to finish</code> phase if
       <code class="literal">--wal-method=fetch</code> is specified in
       <span class="application">pg_basebackup</span>. The backup will end
       when this phase is completed.
      </td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（英文原文，待翻譯）
