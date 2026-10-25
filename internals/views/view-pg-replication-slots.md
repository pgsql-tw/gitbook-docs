<a id="VIEW-PG-REPLICATION-SLOTS"></a>

## 53.20. `pg_replication_slots` [#](#view-pg-replication-slots) <a href="#view-pg-replication-slots" id="view-pg-replication-slots"></a>

<a id="id-1.10.5.24.2"></a>

檢視表 `pg_replication_slots` 列出資料庫叢集中目前存在的所有複寫插槽，以及它們目前的狀態。

關於複寫插槽的更多資訊，請參閱[第 26.2.6 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)與[第 47 章](../../server-programming/logicaldecoding/README.md)。

<a id="id-1.10.5.24.5"></a>

**表 53.20. `pg_replication_slots` 欄位**

<table border="1" class="table" summary="表 53.20. pg_replication_slots 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">name</code>
</p>
<p>
       此複寫插槽在整個叢集中唯一的識別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">plugin</code> <code class="type">name</code>
</p>
<p>
       此邏輯插槽所使用之輸出外掛所在的共享物件的基本名稱；實體插槽則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_type</code> <code class="type">text</code>
</p>
<p>
       插槽類型：<code class="literal">physical</code> 或 <code class="literal">logical</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此插槽所關聯之資料庫的 OID，或為 null。只有邏輯插槽才有關聯的資料庫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">datname</code>）
      </p>
<p>
       此插槽所關聯之資料庫的名稱，或為 null。只有邏輯插槽才有關聯的資料庫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temporary</code> <code class="type">bool</code>
</p>
<p>
       若這是暫時複寫插槽則為 true。暫時插槽不會儲存到磁碟，並會在發生錯誤時或工作階段結束時自動移除。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active</code> <code class="type">bool</code>
</p>
<p>
       若此插槽目前正在進行串流則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active_pid</code> <code class="type">int4</code>
</p>
<p>
       為此插槽串流資料之工作階段的程序 ID。非使用中時為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xmin</code> <code class="type">xid</code>
</p>
<p>
       此插槽需要資料庫保留的最舊交易。<code class="literal">VACUUM</code> 無法移除由任何較晚的交易所刪除的資料列。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">catalog_xmin</code> <code class="type">xid</code>
</p>
<p>
       此插槽需要資料庫保留、且會影響系統目錄的最舊交易。<code class="literal">VACUUM</code> 無法移除由任何較晚的交易所刪除的系統目錄資料列。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restart_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       此插槽的取用端可能仍需要的最舊 WAL 的位址（<code class="literal">LSN</code>），因此這些 WAL 在檢查點期間不會被自動移除，除非此 LSN 落後目前的 LSN 超過 <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">max_slot_wal_keep_size</a>。以下情況為 <code class="literal">NULL</code>：此插槽的 <code class="literal">LSN</code> 從未被保留。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confirmed_flush_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       邏輯插槽的取用端已確認收到資料所到達的位址（<code class="literal">LSN</code>）。在此 <code class="literal">LSN</code> 之前已提交之交易所對應的資料已不再可用。實體插槽則為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_status</code> <code class="type">text</code>
</p>
<p>
       此插槽所要求保留之 WAL 檔案的可用狀態。可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p><code class="literal">reserved</code> 表示所要求保留的檔案仍在 <code class="varname">max_wal_size</code> 的範圍內。</p></li><li class="listitem"><p><code class="literal">extended</code> 表示已超過 <code class="varname">max_wal_size</code>，但這些檔案仍由複寫插槽或 <code class="varname">wal_keep_size</code> 保留著。
         </p></li><li class="listitem"><p>
<code class="literal">unreserved</code> 表示此插槽已不再保留所需的 WAL 檔案，其中部分檔案將在下一次檢查點時被移除。這通常發生在 <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">max_slot_wal_keep_size</a> 設為非負值時。此狀態可以回到 <code class="literal">reserved</code> 或 <code class="literal">extended</code>。
         </p></li><li class="listitem"><p>
<code class="literal">lost</code> 表示此插槽已無法再使用。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">safe_wal_size</code> <code class="type">int8</code>
</p>
<p>
       在不使此插槽陷入「lost」狀態之危險的前提下，仍可寫入 WAL 的位元組數。對於處於 lost 狀態的插槽，以及 <code class="varname">max_slot_wal_keep_size</code> 為 <code class="literal">-1</code> 時，此值為 NULL。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">two_phase</code> <code class="type">bool</code>
</p>
<p>
       若此插槽已啟用已準備交易的解碼則為 true。實體插槽一律為 false。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">two_phase_at</code> <code class="type">pg_lsn</code>
</p>
<p>
       開始啟用已準備交易解碼的位址（<code class="literal">LSN</code>）。以下情況為 <code class="literal">NULL</code>：<code class="structfield">two_phase</code> 為 false 的邏輯插槽，以及實體插槽。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inactive_since</code> <code class="type">timestamptz</code>
</p>
<p>
        插槽變為非使用中的時間。若插槽目前正在串流，則為 <code class="literal">NULL</code>。若插槽變為無效，此值將永遠不會再更新。對於正從主要伺服器同步過來的待命伺服器插槽（其 <code class="structfield">synced</code> 欄位為 <code class="literal">true</code>），<code class="structfield">inactive_since</code> 表示插槽同步（請參閱 <a class="xref" href="../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION">第 47.2.3 節</a>）最近一次停止的時間。若插槽一直保持同步，則為 <code class="literal">NULL</code>。這有助於待命伺服器插槽追蹤同步是在何時中斷的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conflicting</code> <code class="type">bool</code>
</p>
<p>
       若此邏輯插槽與復原發生衝突（因而現已失效）則為 true。此欄位為 true 時，請查看 <code class="structfield">invalidation_reason</code> 欄位以了解衝突原因。實體插槽一律為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">invalidation_reason</code> <code class="type">text</code>
</p>
<p>
       插槽失效的原因。邏輯插槽與實體插槽都會設定此欄位。若插槽未失效，則為 <code class="literal">NULL</code>。可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">wal_removed</code> 表示所需的 WAL 已被移除。
         </p></li><li class="listitem"><p>
<code class="literal">rows_removed</code> 表示所需的資料列已被移除。只有邏輯插槽會設定此值。
         </p></li><li class="listitem"><p>
<code class="literal">wal_level_insufficient</code> 表示主要伺服器的 <a class="xref" href="../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL">wal_level</a> 不足以執行邏輯解碼。只有邏輯插槽會設定此值。
         </p></li><li class="listitem"><p>
<code class="literal">idle_timeout</code> 表示插槽維持非使用中的時間已超過所設定的
          <a class="xref" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT">idle_replication_slot_timeout</a> 時間長度。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">failover</code> <code class="type">bool</code>
</p>
<p>
       若這是已啟用同步至待命伺服器的邏輯插槽則為 true，如此在容錯移轉後，邏輯複寫便可從新的主要伺服器繼續進行。實體插槽一律為 false。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">synced</code> <code class="type">bool</code>
</p>
<p>
       若這是從主要伺服器同步而來的邏輯插槽則為 true。在熱備援伺服器上，synced 欄位標記為 true 的插槽既不能用於邏輯解碼，也不能手動移除。此欄位的值在主要伺服器上沒有意義；主要伺服器上所有插槽的此欄位值預設為 false，但也可能為 true（若該插槽是從已提升為主要伺服器的待命伺服器遺留下來的）。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-replication-slots.html)（原文版本：18.6；核對日期：2026-10-10）
