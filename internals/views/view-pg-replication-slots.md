## 53.20. `pg_replication_slots` [#](#VIEW-PG-REPLICATION-SLOTS)

<a id="id-1.10.5.24.2"></a>

The `pg_replication_slots` view provides a listing
of all replication slots that currently exist on the database cluster,
along with their current state.

For more on replication slots,
see [Section 26.2.6](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS) and [Chapter 47](../../server-programming/logicaldecoding/README.md).

<a id="id-1.10.5.24.5"></a>

**Table 53.20. `pg_replication_slots` Columns**

<table border="1" class="table" summary="pg_replication_slots Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">name</code>
</p>
<p>
       A unique, cluster-wide identifier for the replication slot
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">plugin</code> <code class="type">name</code>
</p>
<p>
       The base name of the shared object containing the output plugin this logical slot is using, or null for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_type</code> <code class="type">text</code>
</p>
<p>
       The slot type: <code class="literal">physical</code> or <code class="literal">logical</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datoid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the database this slot is associated with, or
       null. Only logical slots have an associated database.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">datname</code>)
      </p>
<p>
       The name of the database this slot is associated with, or
       null. Only logical slots have an associated database.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temporary</code> <code class="type">bool</code>
</p>
<p>
       True if this is a temporary replication slot. Temporary slots are
       not saved to disk and are automatically dropped on error or when
       the session has finished.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active</code> <code class="type">bool</code>
</p>
<p>
       True if this slot is currently being streamed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active_pid</code> <code class="type">int4</code>
</p>
<p>
       The process ID of the session streaming data for this slot.
       <code class="literal">NULL</code> if inactive.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xmin</code> <code class="type">xid</code>
</p>
<p>
       The oldest transaction that this slot needs the database to
       retain.  <code class="literal">VACUUM</code> cannot remove tuples deleted
       by any later transaction.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">catalog_xmin</code> <code class="type">xid</code>
</p>
<p>
       The oldest transaction affecting the system catalogs that this
       slot needs the database to retain.  <code class="literal">VACUUM</code> cannot
       remove catalog tuples deleted by any later transaction.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restart_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       The address (<code class="literal">LSN</code>) of oldest WAL which still
       might be required by the consumer of this slot and thus won't be
       automatically removed during checkpoints unless this LSN
       gets behind more than <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">max_slot_wal_keep_size</a>
       from the current LSN.  <code class="literal">NULL</code>
       if the <code class="literal">LSN</code> of this slot has never been reserved.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confirmed_flush_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       The address (<code class="literal">LSN</code>) up to which the logical
       slot's consumer has confirmed receiving data. Data corresponding to the
       transactions committed before this <code class="literal">LSN</code> is not
       available anymore. <code class="literal">NULL</code> for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_status</code> <code class="type">text</code>
</p>
<p>
       Availability of WAL files claimed by this slot.
       Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p><code class="literal">reserved</code> means that the claimed files
          are within <code class="varname">max_wal_size</code>.</p></li><li class="listitem"><p><code class="literal">extended</code> means
          that <code class="varname">max_wal_size</code> is exceeded but the files are
          still retained, either by the replication slot or
          by <code class="varname">wal_keep_size</code>.
         </p></li><li class="listitem"><p>
<code class="literal">unreserved</code> means that the slot no longer
          retains the required WAL files and some of them are to be removed at
          the next checkpoint.  This typically occurs when
          <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">max_slot_wal_keep_size</a> is set to
          a non-negative value.  This state can return
          to <code class="literal">reserved</code> or <code class="literal">extended</code>.
         </p></li><li class="listitem"><p>
<code class="literal">lost</code> means that this slot is no longer usable.
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">safe_wal_size</code> <code class="type">int8</code>
</p>
<p>
       The number of bytes that can be written to WAL such that this slot
       is not in danger of getting in state "lost".  It is NULL for lost
       slots, as well as if <code class="varname">max_slot_wal_keep_size</code>
       is <code class="literal">-1</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">two_phase</code> <code class="type">bool</code>
</p>
<p>
       True if the slot is enabled for decoding prepared transactions.  Always
       false for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">two_phase_at</code> <code class="type">pg_lsn</code>
</p>
<p>
       The address (<code class="literal">LSN</code>) from which the decoding of prepared
       transactions is enabled. <code class="literal">NULL</code> for logical slots
       where <code class="structfield">two_phase</code> is false and for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inactive_since</code> <code class="type">timestamptz</code>
</p>
<p>
        The time when the slot became inactive. <code class="literal">NULL</code> if the
        slot is currently being streamed. If the slot becomes invalid,
        this value will never be updated.
        For standby slots that are being synced from a
        primary server (whose <code class="structfield">synced</code> field is
        <code class="literal">true</code>), the <code class="structfield">inactive_since</code>
        indicates the time when slot synchronization (see <a class="xref" href="../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION">Section 47.2.3</a>)
        was most recently stopped.  <code class="literal">NULL</code> if the slot
        has always been synchronized. This helps standby slots track when
        synchronization was interrupted.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conflicting</code> <code class="type">bool</code>
</p>
<p>
       True if this logical slot conflicted with recovery (and so is now
       invalidated). When this column is true, check
       <code class="structfield">invalidation_reason</code> column for the conflict
       reason. Always <code class="literal">NULL</code> for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">invalidation_reason</code> <code class="type">text</code>
</p>
<p>
       The reason for the slot's invalidation. It is set for both logical and
       physical slots. <code class="literal">NULL</code> if the slot is not invalidated.
       Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">wal_removed</code> means that the required WAL has been
          removed.
         </p></li><li class="listitem"><p>
<code class="literal">rows_removed</code> means that the required rows have
          been removed. It is set only for logical slots.
         </p></li><li class="listitem"><p>
<code class="literal">wal_level_insufficient</code> means that the
          primary doesn't have a <a class="xref" href="../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL">wal_level</a> sufficient to
          perform logical decoding.  It is set only for logical slots.
         </p></li><li class="listitem"><p>
<code class="literal">idle_timeout</code> means that the slot has remained
          inactive longer than the configured
          <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT">idle_replication_slot_timeout</a> duration.
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">failover</code> <code class="type">bool</code>
</p>
<p>
       True if this is a logical slot enabled to be synced to the standbys
       so that logical replication can be resumed from the new primary
       after failover. Always false for physical slots.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">synced</code> <code class="type">bool</code>
</p>
<p>
       True if this is a logical slot that was synced from a primary server.
       On a hot standby, the slots with the synced column marked as true can
       neither be used for logical decoding nor dropped manually. The value
       of this column has no meaning on the primary server; the column value on
       the primary is default false for all slots but may (if leftover from a
       promoted standby) also be true.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-replication-slots.html)（英文原文，待翻譯）
