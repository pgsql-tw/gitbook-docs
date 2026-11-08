# 9.27.10. 控制資料函式

<a id="FUNCTIONS-INFO-CONTROLDATA"></a>

## 9.27.10. 控制資料函式 [#](#functions-info-controldata) <a href="#functions-info-controldata" id="functions-info-controldata"></a>

[表 9.88](#functions-controldata) 所列的函式會輸出在 `initdb` 期間初始化的資訊，例如系統目錄版本。它們也會顯示關於預寫式日誌（write-ahead logging）與檢查點處理的資訊。這些資訊是整個叢集共通的，並非專屬於任何一個資料庫。這些函式所提供的資訊，大多與 [pg_controldata](../../../reference/reference-server/app-pgcontroldata.md) 應用程式相同，且來源也相同。

<a id="FUNCTIONS-CONTROLDATA"></a>

### 表 9.88. 控制資料函式 [#](#functions-controldata) <a href="#functions-controldata" id="functions-controldata"></a>

<table border="1" class="table" summary="Control Data Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.1.1.1.1"></a>
<code class="function">pg_control_checkpoint</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳目前檢查點狀態的資訊，如<a class="xref" href="#functions-pg-control-checkpoint">表 9.89</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.2.1.1.1"></a>
<code class="function">pg_control_system</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳目前控制檔狀態的資訊，如<a class="xref" href="#functions-pg-control-system">表 9.90</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.3.1.1.1"></a>
<code class="function">pg_control_init</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳叢集初始化狀態的資訊，如<a class="xref" href="#functions-pg-control-init">表 9.91</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.4.1.1.1"></a>
<code class="function">pg_control_recovery</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳復原狀態的資訊，如<a class="xref" href="#functions-pg-control-recovery">表 9.92</a> 所示。
       </p></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-CHECKPOINT"></a>

### 表 9.89. `pg_control_checkpoint` 輸出欄位 [#](#functions-pg-control-checkpoint) <a href="#functions-pg-control-checkpoint" id="functions-pg-control-checkpoint"></a>

<table border="1" class="table" summary="pg_control_checkpoint Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">checkpoint_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_wal_file</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">prev_timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">full_page_writes</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">next_xid</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">next_oid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">next_multixact_id</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">next_multi_offset</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_active_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">newest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">checkpoint_time</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-SYSTEM"></a>

### 表 9.90. `pg_control_system` 輸出欄位 [#](#functions-pg-control-system) <a href="#functions-pg-control-system" id="functions-pg-control-system"></a>

<table border="1" class="table" summary="pg_control_system Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">pg_control_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">catalog_version_no</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">system_identifier</code></td><td><code class="type">bigint</code></td></tr><tr><td><code class="structfield">pg_control_last_modified</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-INIT"></a>

### 表 9.91. `pg_control_init` 輸出欄位 [#](#functions-pg-control-init) <a href="#functions-pg-control-init" id="functions-pg-control-init"></a>

<table border="1" class="table" summary="pg_control_init Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">max_data_alignment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">database_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">blocks_per_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">wal_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">bytes_per_wal_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_identifier_length</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_index_columns</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_toast_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">large_object_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">float8_pass_by_value</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">data_page_checksum_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">default_char_signedness</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-RECOVERY"></a>

### 表 9.92. `pg_control_recovery` 輸出欄位 [#](#functions-pg-control-recovery) <a href="#functions-pg-control-recovery" id="functions-pg-control-recovery"></a>

<table border="1" class="table" summary="pg_control_recovery Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">min_recovery_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">min_recovery_end_timeline</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">backup_start_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">backup_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">end_of_backup_record_required</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
