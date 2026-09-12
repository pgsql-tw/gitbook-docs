<a id="FUNCTIONS-ADMIN"></a>

## 9.28. 系統管理函式 [#](#FUNCTIONS-ADMIN)

[9.28.1. 組態設定函式](functions-admin.md#FUNCTIONS-ADMIN-SET)

[9.28.2. 伺服器訊號函式](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)

[9.28.3. 備份控制函式](functions-admin.md#FUNCTIONS-ADMIN-BACKUP)

[9.28.4. 復原控制函式](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL)

[9.28.5. 快照同步函式](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)

[9.28.6. 複寫管理函式](functions-admin.md#FUNCTIONS-REPLICATION)

[9.28.7. 資料庫物件管理函式](functions-admin.md#FUNCTIONS-ADMIN-DBOBJECT)

[9.28.8. 索引維護函式](functions-admin.md#FUNCTIONS-ADMIN-INDEX)

[9.28.9. 通用檔案存取函式](functions-admin.md#FUNCTIONS-ADMIN-GENFILE)

[9.28.10. 諮詢鎖函式](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS)

本節所說明的函式用於控制與監控 PostgreSQL 的安裝。

<a id="FUNCTIONS-ADMIN-SET"></a>

### 9.28.1. 組態設定函式 [#](#FUNCTIONS-ADMIN-SET)

<a id="id-1.5.8.34.3.2"></a><a id="id-1.5.8.34.3.3"></a><a id="id-1.5.8.34.3.4"></a>

[表 9.95](functions-admin.md#FUNCTIONS-ADMIN-SET-TABLE) 列出可用來查詢與修改執行時期組態參數的函式。

<a id="FUNCTIONS-ADMIN-SET-TABLE"></a>

**表 9.95. 組態設定函式**

<table border="1" class="table" summary="Configuration Settings Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.3.6.2.2.1.1.1.1"></a>
<code class="function">current_setting</code> ( <em class="parameter"><code>setting_name</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳設定 <em class="parameter"><code>setting_name</code></em> 目前的值。如果沒有這個設定，<code class="function">current_setting</code> 會拋出錯誤，除非有提供 <em class="parameter"><code>missing_ok</code></em> 且其值為 <code class="literal">true</code>（此時會回傳 NULL）。這個函式對應於 <acronym class="acronym">SQL</acronym> 指令 <a class="xref" href="../../reference/sql-commands/sql-show.md"><span class="refentrytitle">SHOW</span></a>。
       </p>
<p>
<code class="literal">current_setting('datestyle')</code>
        → <code class="returnvalue">ISO, MDY</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.3.6.2.2.2.1.1.1"></a>
<code class="function">set_config</code> (
          <em class="parameter"><code>setting_name</code></em> <code class="type">text</code>,
          <em class="parameter"><code>new_value</code></em> <code class="type">text</code>,
          <em class="parameter"><code>is_local</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將參數 <em class="parameter"><code>setting_name</code></em> 設定為 <em class="parameter"><code>new_value</code></em>，並回傳該值。如果 <em class="parameter"><code>is_local</code></em> 為 <code class="literal">true</code>，新值只會在目前的交易期間生效。如果你希望新值在目前工作階段的其餘時間都生效，請改用 <code class="literal">false</code>。這個函式對應於 SQL 指令 <a class="xref" href="../../reference/sql-commands/sql-set.md"><span class="refentrytitle">SET</span></a>。
       </p>
<p>
<code class="function">set_config</code> 接受以 NULL 值作為 <em class="parameter"><code>new_value</code></em>，但由於設定不能為 NULL，這會被解讀為將該設定重設為預設值的請求。
       </p>
<p>
<code class="literal">set_config('log_statement_stats', 'off', false)</code>
        → <code class="returnvalue">off</code>
</p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-ADMIN-SIGNAL"></a>

### 9.28.2. 伺服器訊號函式 [#](#FUNCTIONS-ADMIN-SIGNAL)

<a id="id-1.5.8.34.4.2"></a>

[表 9.96](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE) 所列的函式會向其他伺服器程序傳送控制訊號。這些函式預設只限超級使用者使用，但可以使用 `GRANT` 將存取權授予其他使用者，另有註明的例外情形除外。

這些函式在訊號傳送成功時都會回傳 `true`，傳送失敗時則回傳 `false`。

<a id="FUNCTIONS-ADMIN-SIGNAL-TABLE"></a>

**表 9.96. 伺服器訊號函式**

<table border="1" class="table" summary="Server Signaling Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.1.1.1.1"></a>
<code class="function">pg_cancel_backend</code> ( <em class="parameter"><code>pid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        取消其後端程序具有指定程序 ID 之工作階段目前的查詢。如果呼叫的角色是被取消之後端所屬角色的成員，或呼叫的角色具有 <code class="literal">pg_signal_backend</code> 的權限，也可以執行此操作，但只有超級使用者可以取消超級使用者的後端。例外的是，具有 <code class="literal">pg_signal_autovacuum_worker</code> 權限的角色可以取消 autovacuum 工作程序，這些程序在其他情況下會被視為超級使用者的後端。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.2.1.1.1"></a>
<code class="function">pg_log_backend_memory_contexts</code> ( <em class="parameter"><code>pid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        請求將具有指定程序 ID 之後端的記憶體內容記錄到日誌中。這個函式可以將請求傳送給 logger 以外的後端與輔助程序。這些記憶體內容會以 <code class="literal">LOG</code> 訊息層級記錄。它們會依照所設定的日誌組態出現在伺服器日誌中（更多資訊請參閱<a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md">第 19.8 節</a>），但無論 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES">client_min_messages</a> 如何設定，都不會傳送給用戶端。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.3.1.1.1"></a>
<code class="function">pg_reload_conf</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        讓 <span class="productname">PostgreSQL</span> 伺服器的所有程序重新載入它們的組態檔案。（這是透過向 postmaster 程序傳送 <span class="systemitem">SIGHUP</span> 訊號來啟動的，postmaster 接著會向它的每個子程序傳送 <span class="systemitem">SIGHUP</span>。）在重新載入之前，你可以使用 <a class="link" href="../../internals/views/view-pg-file-settings.md"><code class="structname">pg_file_settings</code></a>、<a class="link" href="../../internals/views/view-pg-hba-file-rules.md"><code class="structname">pg_hba_file_rules</code></a> 與 <a class="link" href="../../internals/views/view-pg-ident-file-mappings.md"><code class="structname">pg_ident_file_mappings</code></a> 檢視表來檢查組態檔案中可能的錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.4.1.1.1"></a>
<code class="function">pg_rotate_logfile</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        向日誌檔案管理程序發出訊號，要求它立即切換到新的輸出檔案。這只有在內建的日誌收集器正在執行時才有作用，因為否則就不會有日誌檔案管理子程序。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.5.1.1.1"></a>
<code class="function">pg_terminate_backend</code> ( <em class="parameter"><code>pid</code></em> <code class="type">integer</code>, <em class="parameter"><code>timeout</code></em> <code class="type">bigint</code> <code class="literal">DEFAULT</code> <code class="literal">0</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        終止其後端程序具有指定程序 ID 的工作階段。如果呼叫的角色是被終止之後端所屬角色的成員，或呼叫的角色具有 <code class="literal">pg_signal_backend</code> 的權限，也可以執行此操作，但只有超級使用者可以終止超級使用者的後端。例外的是，具有 <code class="literal">pg_signal_autovacuum_worker</code> 權限的角色可以終止 autovacuum 工作程序，這些程序在其他情況下會被視為超級使用者的後端。
       </p>
<p>
        如果未指定 <em class="parameter"><code>timeout</code></em> 或其值為零，無論程序是否真的終止，這個函式都會回傳 <code class="literal">true</code>，這只表示訊號已成功傳送。如果有指定 <em class="parameter"><code>timeout</code></em>（以毫秒為單位）且大於零，函式會等到程序真正終止或經過指定的時間為止。如果程序已終止，函式會回傳 <code class="literal">true</code>。逾時的話，會發出警告並回傳 <code class="literal">false</code>。
       </p></td></tr></tbody></table>

<br>

`pg_cancel_backend` 與 `pg_terminate_backend` 會向以程序 ID 指定的後端程序傳送訊號（分別是 SIGINT 或 SIGTERM）。作用中後端的程序 ID 可以從 `pg_stat_activity` 檢視表的 `pid` 欄位查得，或是列出伺服器上的 `postgres` 程序（在 Unix 上使用 ps，在 Windows 上使用工作管理員）。作用中後端的角色可以從 `pg_stat_activity` 檢視表的 `usename` 欄位查得。

`pg_log_backend_memory_contexts` 可用來將某個後端程序的記憶體內容（memory context）記錄到日誌中。例如：

```

postgres=# SELECT pg_log_backend_memory_contexts(pg_backend_pid());
 pg_log_backend_memory_contexts
--------------------------------
 t
(1 row)
```

每個記憶體內容會記錄一則訊息。例如：

```

LOG:  logging memory contexts of PID 10377
STATEMENT:  SELECT pg_log_backend_memory_contexts(pg_backend_pid());
LOG:  level: 1; TopMemoryContext: 80800 total in 6 blocks; 14432 free (5 chunks); 66368 used
LOG:  level: 2; pgstat TabStatusArray lookup hash table: 8192 total in 1 blocks; 1408 free (0 chunks); 6784 used
LOG:  level: 2; TopTransactionContext: 8192 total in 1 blocks; 7720 free (1 chunks); 472 used
LOG:  level: 2; RowDescriptionContext: 8192 total in 1 blocks; 6880 free (0 chunks); 1312 used
LOG:  level: 2; MessageContext: 16384 total in 2 blocks; 5152 free (0 chunks); 11232 used
LOG:  level: 2; Operator class cache: 8192 total in 1 blocks; 512 free (0 chunks); 7680 used
LOG:  level: 2; smgr relation table: 16384 total in 2 blocks; 4544 free (3 chunks); 11840 used
LOG:  level: 2; TransactionAbortContext: 32768 total in 1 blocks; 32504 free (0 chunks); 264 used
...
LOG:  level: 2; ErrorContext: 8192 total in 1 blocks; 7928 free (3 chunks); 264 used
LOG:  Grand total: 1651920 bytes in 201 blocks; 622360 free (88 chunks); 1029560 used
```

如果同一個父內容之下有超過 100 個子內容，就會記錄前 100 個子內容，並附上其餘內容的摘要。請注意，頻繁呼叫這個函式可能會造成顯著的額外負擔，因為它可能產生大量的日誌訊息。

<a id="FUNCTIONS-ADMIN-BACKUP"></a>

### 9.28.3. 備份控制函式 [#](#FUNCTIONS-ADMIN-BACKUP)

<a id="id-1.5.8.34.5.2"></a>

[表 9.97](functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE) 所列的函式可協助進行線上備份。這些函式不能在復原期間執行（`pg_backup_start`、`pg_backup_stop` 與 `pg_wal_lsn_diff` 除外）。

關於這些函式的正確用法，詳情請參閱[第 25.3 節](../../server-administration/backup/continuous-archiving.md)。

<a id="FUNCTIONS-ADMIN-BACKUP-TABLE"></a>

**表 9.97. 備份控制函式**

<table border="1" class="table" summary="Backup Control Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.1.1.1.1"></a>
<code class="function">pg_create_restore_point</code> ( <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        在預寫式日誌中建立一個具名的標記紀錄，之後可以用來作為復原目標，並回傳對應的預寫式日誌位置。接著可以將所給的名稱與 <a class="xref" href="../../server-administration/runtime-config/runtime-config-wal.md#GUC-RECOVERY-TARGET-NAME">recovery_target_name</a> 搭配使用，以指定復原要進行到哪一個時間點。請避免建立多個名稱相同的還原點，因為復原會在第一個名稱符合復原目標的還原點停止。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.2.1.1.1"></a>
<code class="function">pg_current_wal_flush_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的排清位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.3.1.1.1"></a>
<code class="function">pg_current_wal_insert_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的插入位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.4.1.1.1"></a>
<code class="function">pg_current_wal_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的寫入位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.5.1.1.1"></a>
<code class="function">pg_backup_start</code> (
          <em class="parameter"><code>label</code></em> <code class="type">text</code>
          [<span class="optional">, <em class="parameter"><code>fast</code></em> <code class="type">boolean</code>
</span>] )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        讓伺服器準備開始進行線上備份。唯一必要的參數是使用者自訂的任意備份標籤。（通常這會是備份傾印檔案存放時所用的名稱。）如果選用的第二個參數指定為 <code class="literal">true</code>，就表示要盡快執行 <code class="function">pg_backup_start</code>。這會強制立即進行檢查點，因而造成 I/O 操作的尖峰，拖慢任何同時執行中的查詢。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.6.1.1.1"></a>
<code class="function">pg_backup_stop</code> (
          [<span class="optional"><em class="parameter"><code>wait_for_archive</code></em> <code class="type">boolean</code>
</span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>labelfile</code></em> <code class="type">text</code>,
        <em class="parameter"><code>spcmapfile</code></em> <code class="type">text</code> )
       </p>
<p>
        完成線上備份的執行。備份標籤檔案與資料表空間對應檔案應有的內容，會作為函式結果的一部分回傳，且必須寫入備份區域中的檔案。這些檔案不可寫入運作中的資料目錄（這樣做會導致 PostgreSQL 在當機時無法重新啟動）。
       </p>
<p>
        有一個 <code class="type">boolean</code> 型別的選用參數。如果為 false，函式會在備份完成後立即回傳，而不等待 WAL 封存。這種行為只有在搭配會獨立監控 WAL 封存的備份軟體時才有用。否則，讓備份保持一致所需的 WAL 可能會遺失，使得備份毫無用處。在預設情況下或此參數為 true 時，如果已啟用封存，<code class="function">pg_backup_stop</code> 會等待 WAL 封存完成。（在備用伺服器上，這表示只有在 <code class="varname">archive_mode</code> = <code class="literal">always</code> 時才會等待。如果主要伺服器上的寫入活動很少，在主要伺服器上執行 <code class="function">pg_switch_wal</code> 以觸發立即的區段切換可能會有幫助。）
       </p>
<p>
        在主要伺服器上執行時，這個函式還會在預寫式日誌封存區域中建立一個備份歷程檔案。歷程檔案包含傳給 <code class="function">pg_backup_start</code> 的標籤、備份的起始與結束預寫式日誌位置，以及備份的起始與結束時間。在記錄結束位置之後，目前的預寫式日誌插入點會自動推進到下一個預寫式日誌檔案，讓結束的預寫式日誌檔案可以立即封存，以完成備份。
       </p>
<p>
        這個函式的結果是單一筆紀錄。<em class="parameter"><code>lsn</code></em> 欄位存放備份的結束預寫式日誌位置（同樣可以忽略）。第二個欄位回傳備份標籤檔案的內容，第三個欄位則回傳資料表空間對應檔案的內容。這些內容必須作為備份的一部分儲存，並且是還原程序中所必需的。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.7.1.1.1"></a>
<code class="function">pg_switch_wal</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        強制伺服器切換到新的預寫式日誌檔案，讓目前的檔案可以被封存（假設你正在使用連續封存）。結果是剛完成的預寫式日誌檔案中的結束預寫式日誌位置加 1。如果自上次預寫式日誌切換以來沒有任何預寫式日誌活動，<code class="function">pg_switch_wal</code> 不會做任何事，並回傳目前使用中之預寫式日誌檔案的起始位置。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.8.1.1.1"></a>
<code class="function">pg_walfile_name</code> ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將預寫式日誌位置轉換為存放該位置的 WAL 檔案名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.9.1.1.1"></a>
<code class="function">pg_walfile_name_offset</code> ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>file_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>file_offset</code></em> <code class="type">integer</code> )
       </p>
<p>
        將預寫式日誌位置轉換為 WAL 檔案名稱，以及在該檔案內的位元組偏移量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.10.1.1.1"></a>
<code class="function">pg_split_walfile_name</code> ( <em class="parameter"><code>file_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>segment_number</code></em> <code class="type">numeric</code>,
        <em class="parameter"><code>timeline_id</code></em> <code class="type">bigint</code> )
       </p>
<p>
        從 WAL 檔案名稱中取出序號與時間軸 ID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.11.1.1.1"></a>
<code class="function">pg_wal_lsn_diff</code> ( <em class="parameter"><code>lsn1</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>lsn2</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        計算兩個預寫式日誌位置之間以位元組為單位的差值（<em class="parameter"><code>lsn1</code></em> - <em class="parameter"><code>lsn2</code></em>）。這可以與 <code class="structname">pg_stat_replication</code> 或<a class="xref" href="functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE">表 9.97</a> 中所列的部分函式搭配使用，以取得複寫延遲。
       </p></td></tr></tbody></table>

<br>

`pg_current_wal_lsn` 會以上述函式所使用的相同格式，顯示目前預寫式日誌（write-ahead log）的寫入位置。同樣地，`pg_current_wal_insert_lsn` 會顯示目前預寫式日誌的插入位置，而 `pg_current_wal_flush_lsn` 則顯示目前預寫式日誌的排清（flush）位置。插入位置是任一時刻預寫式日誌的「邏輯」結尾，而寫入位置是實際已從伺服器內部緩衝區寫出之內容的結尾，排清位置則是已知已寫入持久性儲存裝置的最後位置。寫入位置是從伺服器外部所能檢視之內容的結尾；如果你想要封存僅部分完成的預寫式日誌檔案，通常需要的就是這個位置。插入位置與排清位置主要是提供給伺服器除錯之用。這些都是唯讀操作，不需要超級使用者權限。

你可以使用 `pg_walfile_name_offset`，從 `pg_lsn` 值中取出對應的預寫式日誌檔名與位元組偏移量。例如：

```

postgres=# SELECT * FROM pg_walfile_name_offset((pg_backup_stop()).lsn);
        file_name         | file_offset
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

同樣地，`pg_walfile_name` 只會取出預寫式日誌的檔名。

`pg_split_walfile_name` 可用於從檔案偏移量與 WAL 檔名計算出 LSN，例如：

```

postgres=# \set file_name '000000010000000100C000AB'
postgres=# \set offset 256
postgres=# SELECT '0/0'::pg_lsn + pd.segment_number * ps.setting::int + :offset AS lsn
  FROM pg_split_walfile_name(:'file_name') pd,
       pg_show_all_settings() ps
  WHERE ps.name = 'wal_segment_size';
      lsn
---------------
 C001/AB000100
(1 row)
```

<a id="FUNCTIONS-RECOVERY-CONTROL"></a>

### 9.28.4. 復原控制函式 [#](#FUNCTIONS-RECOVERY-CONTROL)

[表 9.98](functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE) 所列的函式提供備用伺服器目前狀態的相關資訊。這些函式在復原期間與正常執行時都可以執行。

<a id="FUNCTIONS-RECOVERY-INFO-TABLE"></a>

**表 9.98. 復原資訊函式**

<table border="1" class="table" summary="Recovery Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.3.2.2.1.1.1.1"></a>
<code class="function">pg_is_in_recovery</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果復原仍在進行中，就回傳 true。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.3.2.2.2.1.1.1"></a>
<code class="function">pg_last_wal_receive_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳串流複寫已接收並同步到磁碟的最後一個預寫式日誌位置。在串流複寫進行期間，這個值會單調遞增。如果復原已經完成，這個值會停留在復原期間最後接收並同步到磁碟之 WAL 紀錄的位置。如果停用了串流複寫，或串流複寫尚未開始，函式會回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.3.2.2.3.1.1.1"></a>
<code class="function">pg_last_wal_replay_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳復原期間已重播的最後一個預寫式日誌位置。如果復原仍在進行中，這個值會單調遞增。如果復原已經完成，這個值會停留在復原期間最後套用之 WAL 紀錄的位置。如果伺服器是在沒有復原的情況下正常啟動，函式會回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.3.2.2.4.1.1.1"></a>
<code class="function">pg_last_xact_replay_timestamp</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳復原期間最後重播之交易的時間戳記。這是該交易的提交或中止 WAL 紀錄在主要伺服器上產生的時間。如果復原期間沒有重播任何交易，函式會回傳 <code class="literal">NULL</code>。否則，如果復原仍在進行中，這個值會單調遞增。如果復原已經完成，這個值會停留在復原期間最後套用之交易的時間。如果伺服器是在沒有復原的情況下正常啟動，函式會回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_wal_resource_managers</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>rm_id</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>rm_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>rm_builtin</code></em> <code class="type">boolean</code> )
       </p>
<p>
        回傳系統中目前已載入的 WAL 資源管理器。<em class="parameter"><code>rm_builtin</code></em> 欄位表示它是內建的資源管理器，還是由擴充套件載入的自訂資源管理器。
       </p></td></tr></tbody></table>

<br>

[表 9.99](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL-TABLE) 所列的函式用於控制復原的進度。這些函式只能在復原期間執行。

<a id="FUNCTIONS-RECOVERY-CONTROL-TABLE"></a>

**表 9.99. 復原控制函式**

<table border="1" class="table" summary="Recovery Control Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.5.2.2.1.1.1.1"></a>
<code class="function">pg_is_wal_replay_paused</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果已請求暫停復原，就回傳 true。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.5.2.2.2.1.1.1"></a>
<code class="function">pg_get_wal_replay_pause_state</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳復原暫停的狀態。回傳值為：未請求暫停時為 <code class="literal">
        not paused</code>；已請求暫停但復原尚未暫停時為 <code class="literal">
        pause requested</code>；復原實際已暫停時為 <code class="literal">paused</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.5.2.2.3.1.1.1"></a>
<code class="function">pg_promote</code> ( <em class="parameter"><code>wait</code></em> <code class="type">boolean</code> <code class="literal">DEFAULT</code> <code class="literal">true</code>, <em class="parameter"><code>wait_seconds</code></em> <code class="type">integer</code> <code class="literal">DEFAULT</code> <code class="literal">60</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        將備用伺服器提升為主要伺服器。當 <em class="parameter"><code>wait</code></em> 設為 <code class="literal">true</code>（預設值）時，函式會等到提升完成或經過 <em class="parameter"><code>wait_seconds</code></em> 秒為止，提升成功時回傳 <code class="literal">true</code>，否則回傳 <code class="literal">false</code>。如果 <em class="parameter"><code>wait</code></em> 設為 <code class="literal">false</code>，函式會回傳 <code class="literal">true</code>，而且是在向 postmaster 傳送 <code class="literal">SIGUSR1</code> 訊號以觸發提升之後立即回傳。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.5.2.2.4.1.1.1"></a>
<code class="function">pg_wal_replay_pause</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        請求暫停復原。提出請求並不代表復原會立即停止。如果你想確保復原確實已暫停，就需要檢查 <code class="function">pg_get_wal_replay_pause_state()</code> 所回傳的復原暫停狀態。請注意，<code class="function">pg_is_wal_replay_paused()</code> 回傳的是是否已提出請求。在復原暫停期間，不會再套用任何資料庫變更。如果熱備用（hot standby）處於作用中，所有新的查詢都會看到相同且一致的資料庫快照，而且在復原恢復之前不會再產生任何查詢衝突。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.6.5.2.2.5.1.1.1"></a>
<code class="function">pg_wal_replay_resume</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        如果復原已暫停，就重新開始復原。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr></tbody></table>

<br>

在提升（promotion）進行中時，不能執行 `pg_wal_replay_pause` 與 `pg_wal_replay_resume`。如果在復原暫停時觸發了提升，暫停狀態就會結束，並繼續進行提升。

如果停用了串流複寫，暫停狀態可以無限期持續而不會有問題。如果正在進行串流複寫，就會持續接收 WAL 紀錄，最終會填滿可用的磁碟空間，這取決於暫停的時間長短、WAL 的產生速率以及可用的磁碟空間。

<a id="FUNCTIONS-SNAPSHOT-SYNCHRONIZATION"></a>

### 9.28.5. 快照同步函式 [#](#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)

PostgreSQL 允許資料庫工作階段同步它們的快照。*快照*決定了哪些資料對正在使用該快照的交易是可見的。當兩個以上的工作階段需要看到資料庫中完全相同的內容時，就需要同步快照。如果兩個工作階段只是各自獨立地開始交易，那麼總是有可能在兩個 `START TRANSACTION` 指令執行之間，有第三個交易提交，使得其中一個工作階段看得到該交易的效果，而另一個則看不到。

為了解決這個問題，PostgreSQL 允許交易*匯出*（export）它正在使用的快照。只要匯出快照的交易仍保持開啟，其他交易就可以*匯入*（import）它的快照，從而保證它們看到的資料庫狀態與第一個交易所看到的完全相同。但請注意，這些交易中任何一個所做的資料庫變更，對其他交易仍然是不可見的，這與未提交交易所做的變更一般情況相同。因此，這些交易對於既有的資料是同步的，但對於它們自己所做的變更則照常運作。

快照是以 `pg_export_snapshot` 函式匯出（如[表 9.100](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE) 所示），並以 [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) 指令匯入。

<a id="FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE"></a>

**表 9.100. 快照同步函式**

<table border="1" class="table" summary="Snapshot Synchronization Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.7.5.2.2.1.1.1.1"></a>
<code class="function">pg_export_snapshot</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        儲存交易目前的快照，並回傳一個識別該快照的 <code class="type">text</code> 字串。這個字串必須（在資料庫之外）傳給想要匯入該快照的用戶端。這個快照只在匯出它的交易結束之前可供匯入。
       </p>
<p>
        如有需要，一個交易可以匯出多個快照。請注意，這樣做只在 <code class="literal">READ COMMITTED</code> 交易中才有用，因為在 <code class="literal">REPEATABLE READ</code> 及更高的隔離等級中，交易在其整個生命週期內都使用同一個快照。一旦交易匯出了任何快照，就不能再以 <a class="xref" href="../../reference/sql-commands/sql-prepare-transaction.md"><span class="refentrytitle">PREPARE TRANSACTION</span></a> 進行準備。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.7.5.2.2.2.1.1.1"></a>
<code class="function">pg_log_standby_snapshot</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        擷取執行中交易的快照並寫入 WAL，而不必等待 bgwriter 或 checkpointer 記錄一筆。這對於在備用伺服器上進行邏輯解碼很有用，因為建立邏輯複寫槽必須等到這樣的紀錄在備用伺服器上重播之後才能進行。
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-REPLICATION"></a>

### 9.28.6. 複寫管理函式 [#](#FUNCTIONS-REPLICATION)

[表 9.101](functions-admin.md#FUNCTIONS-REPLICATION-TABLE) 所列的函式用於控制複寫功能並與之互動。關於底層功能的資訊，請參閱[第 26.2.5 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)、[第 26.2.6 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)與[第 48 章](../../server-programming/replication-origins/README.md)。複寫來源相關函式預設只允許超級使用者使用，但可以使用 `GRANT` 指令允許其他使用者使用。複寫槽相關函式則只限超級使用者與具有 `REPLICATION` 權限的使用者使用。

這些函式中有許多在複寫協定中都有對應的指令；請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)。

[第 9.28.3 節](functions-admin.md#FUNCTIONS-ADMIN-BACKUP)、[第 9.28.4 節](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL)與[第 9.28.5 節](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)所說明的函式也與複寫相關。

<a id="FUNCTIONS-REPLICATION-TABLE"></a>

**表 9.101. 複寫管理函式**

<table border="1" class="table" summary="Replication Management Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.1.1.1.1"></a>
<code class="function">pg_create_physical_replication_slot</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code> [<span class="optional">, <em class="parameter"><code>immediately_reserve</code></em> <code class="type">boolean</code>, <em class="parameter"><code>temporary</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>,
        <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        建立一個名為 <em class="parameter"><code>slot_name</code></em> 的新實體複寫槽。選用的第二個參數為 <code class="literal">true</code> 時，表示要立即為這個複寫槽保留 <acronym class="acronym">LSN</acronym>；否則會在串流複寫用戶端第一次連線時才保留 <acronym class="acronym">LSN</acronym>。只有透過串流複寫協定，才能從實體複寫槽串流傳送變更——請參閱<a class="xref" href="../../internals/protocol/protocol-replication.md">第 54.4 節</a>。選用的第三個參數 <em class="parameter"><code>temporary</code></em> 設為 true 時，表示這個複寫槽不應永久儲存到磁碟，且只供目前的工作階段使用。暫時複寫槽在發生任何錯誤時也會被釋放。這個函式對應於複寫協定指令 <code class="literal">CREATE_REPLICATION_SLOT
        ... PHYSICAL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.2.1.1.1"></a>
<code class="function">pg_drop_replication_slot</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        刪除名為 <em class="parameter"><code>slot_name</code></em> 的實體或邏輯複寫槽。與複寫協定指令 <code class="literal">DROP_REPLICATION_SLOT</code> 相同。
       </p></td></tr><tr><td class="func_table_entry" id="PG-CREATE-LOGICAL-REPLICATION-SLOT"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.3.1.1.1"></a>
<code class="function">pg_create_logical_replication_slot</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>plugin</code></em> <code class="type">name</code> [<span class="optional">, <em class="parameter"><code>temporary</code></em> <code class="type">boolean</code>, <em class="parameter"><code>twophase</code></em> <code class="type">boolean</code>, <em class="parameter"><code>failover</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>,
        <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        建立一個名為 <em class="parameter"><code>slot_name</code></em> 的新邏輯（解碼）複寫槽，並使用輸出外掛 <em class="parameter"><code>plugin</code></em>。選用的第三個參數 <em class="parameter"><code>temporary</code></em> 設為 true 時，表示這個複寫槽不應永久儲存到磁碟，且只供目前的工作階段使用。暫時複寫槽在發生任何錯誤時也會被釋放。選用的第四個參數 <em class="parameter"><code>twophase</code></em> 設為 true 時，表示這個複寫槽啟用已準備交易（prepared transaction）的解碼。選用的第五個參數 <em class="parameter"><code>failover</code></em> 設為 true 時，表示這個複寫槽啟用同步到備用伺服器的功能，讓邏輯複寫能在容錯移轉之後繼續進行。呼叫這個函式的效果與複寫協定指令 <code class="literal">CREATE_REPLICATION_SLOT ... LOGICAL</code> 相同。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.4.1.1.1"></a>
<code class="function">pg_copy_physical_replication_slot</code> ( <em class="parameter"><code>src_slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>dst_slot_name</code></em> <code class="type">name</code> [<span class="optional">, <em class="parameter"><code>temporary</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>,
        <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        將名為 <em class="parameter"><code>src_slot_name</code></em> 的既有實體複寫槽，複製到名為 <em class="parameter"><code>dst_slot_name</code></em> 的實體複寫槽。複製出來的實體複寫槽會從與來源複寫槽相同的 <acronym class="acronym">LSN</acronym> 開始保留 WAL。<em class="parameter"><code>temporary</code></em> 是選用的。如果省略 <em class="parameter"><code>temporary</code></em>，就會使用與來源複寫槽相同的值。不允許複製已失效的複寫槽。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.5.1.1.1"></a>
<code class="function">pg_copy_logical_replication_slot</code> ( <em class="parameter"><code>src_slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>dst_slot_name</code></em> <code class="type">name</code> [<span class="optional">, <em class="parameter"><code>temporary</code></em> <code class="type">boolean</code> [<span class="optional">, <em class="parameter"><code>plugin</code></em> <code class="type">name</code> </span>]</span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>,
        <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        將名為 <em class="parameter"><code>src_slot_name</code></em> 的既有邏輯複寫槽，複製到名為 <em class="parameter"><code>dst_slot_name</code></em> 的邏輯複寫槽，並可選擇性地變更輸出外掛與持久性。複製出來的邏輯複寫槽會從與來源邏輯複寫槽相同的 <acronym class="acronym">LSN</acronym> 開始。<em class="parameter"><code>temporary</code></em> 與 <em class="parameter"><code>plugin</code></em> 都是選用的；如果省略，就會使用來源複寫槽的值。來源邏輯複寫槽的 <code class="literal">failover</code> 選項不會被複製，預設會設為 <code class="literal">false</code>。這是為了避免在容錯移轉到正在同步該複寫槽的備用伺服器之後，無法繼續進行邏輯複寫的風險。不允許複製已失效的複寫槽。
       </p></td></tr><tr><td class="func_table_entry" id="PG-LOGICAL-SLOT-GET-CHANGES"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.6.1.1.1"></a>
<code class="function">pg_logical_slot_get_changes</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>upto_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>upto_nchanges</code></em> <code class="type">integer</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>options</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>data</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳複寫槽 <em class="parameter"><code>slot_name</code></em> 中的變更，從上次取用變更之處開始。如果 <em class="parameter"><code>upto_lsn</code></em> 與 <em class="parameter"><code>upto_nchanges</code></em> 皆為 NULL，邏輯解碼會一直進行到 WAL 的結尾。如果 <em class="parameter"><code>upto_lsn</code></em> 不為 NULL，解碼只會包含在指定 LSN 之前提交的交易。如果 <em class="parameter"><code>upto_nchanges</code></em> 不為 NULL，當解碼產生的資料列數超過指定值時，解碼就會停止。不過請注意，實際回傳的資料列數可能會更多，因為這個限制只會在加入解碼每個新交易提交時所產生的資料列之後才檢查。如果指定的複寫槽是邏輯容錯移轉複寫槽，函式要等到 <a class="link" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS"><code class="varname">synchronized_standby_slots</code></a> 中指定的所有實體複寫槽都已確認收到 WAL 之後才會回傳。
       </p></td></tr><tr><td class="func_table_entry" id="PG-LOGICAL-SLOT-PEEK-CHANGES"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.7.1.1.1"></a>
<code class="function">pg_logical_slot_peek_changes</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>upto_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>upto_nchanges</code></em> <code class="type">integer</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>options</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
         <em class="parameter"><code>data</code></em> <code class="type">text</code> )
       </p>
<p>
        行為與 <code class="function">pg_logical_slot_get_changes()</code> 函式完全相同，差別在於變更不會被取用；也就是說，在之後的呼叫中還會再次回傳這些變更。
       </p></td></tr><tr><td class="func_table_entry" id="PG-LOGICAL-SLOT-GET-BINARY-CHANGES"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.8.1.1.1"></a>
<code class="function">pg_logical_slot_get_binary_changes</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>upto_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>upto_nchanges</code></em> <code class="type">integer</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>options</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
       </p>
<p>
        行為與 <code class="function">pg_logical_slot_get_changes()</code> 函式完全相同，差別在於變更會以 <code class="type">bytea</code> 回傳。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.9.1.1.1"></a>
<code class="function">pg_logical_slot_peek_binary_changes</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>upto_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>upto_nchanges</code></em> <code class="type">integer</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>options</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
       </p>
<p>
        行為與 <code class="function">pg_logical_slot_peek_changes()</code> 函式完全相同，差別在於變更會以 <code class="type">bytea</code> 回傳。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-SLOT-ADVANCE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.10.1.1.1"></a>
<code class="function">pg_replication_slot_advance</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>, <em class="parameter"><code>upto_lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>slot_name</code></em> <code class="type">name</code>,
        <em class="parameter"><code>end_lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        推進名為 <em class="parameter"><code>slot_name</code></em> 之複寫槽目前已確認的位置。複寫槽不會向後移動，也不會移動到超過目前插入位置之處。回傳複寫槽的名稱，以及它實際推進到的位置。如果有進行任何推進，更新後的複寫槽位置資訊會在下一個檢查點時寫出。因此在當機的情況下，複寫槽可能會回到較早的位置。如果指定的複寫槽是邏輯容錯移轉複寫槽，函式要等到 <a class="link" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS"><code class="varname">synchronized_standby_slots</code></a> 中指定的所有實體複寫槽都已確認收到 WAL 之後才會回傳。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-CREATE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.11.1.1.1"></a>
<code class="function">pg_replication_origin_create</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        以指定的外部名稱建立一個複寫來源，並回傳指派給它的內部 ID。名稱長度不得超過 512 個位元組。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-DROP"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.12.1.1.1"></a>
<code class="function">pg_replication_origin_drop</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        刪除先前建立的複寫來源，包括任何相關聯的重播進度。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.13.1.1.1"></a>
<code class="function">pg_replication_origin_oid</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        依名稱查詢複寫來源，並回傳其內部 ID。如果找不到這樣的複寫來源，就回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-SESSION-SETUP"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.14.1.1.1"></a>
<code class="function">pg_replication_origin_session_setup</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將目前的工作階段標記為正在從指定的來源進行重播，以便追蹤重播進度。只有在目前未選取任何來源時才能使用。請使用 <code class="function">pg_replication_origin_session_reset</code> 來還原此設定。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.15.1.1.1"></a>
<code class="function">pg_replication_origin_session_reset</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        取消 <code class="function">pg_replication_origin_session_setup()</code> 的效果。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.16.1.1.1"></a>
<code class="function">pg_replication_origin_session_is_setup</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果目前的工作階段已選取複寫來源，就回傳 true。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-SESSION-PROGRESS"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.17.1.1.1"></a>
<code class="function">pg_replication_origin_session_progress</code> ( <em class="parameter"><code>flush</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前工作階段中所選取之複寫來源的重播位置。參數 <em class="parameter"><code>flush</code></em> 決定是否要保證對應的本地交易已排清到磁碟。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-XACT-SETUP"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.18.1.1.1"></a>
<code class="function">pg_replication_origin_xact_setup</code> ( <em class="parameter"><code>origin_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>origin_timestamp</code></em> <code class="type">timestamp with time zone</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將目前的交易標記為正在重播一個已在指定 <acronym class="acronym">LSN</acronym> 與時間戳記提交的交易。只有在已使用 <code class="function">pg_replication_origin_session_setup</code> 選取複寫來源時才能呼叫。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-XACT-RESET"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.19.1.1.1"></a>
<code class="function">pg_replication_origin_xact_reset</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        取消 <code class="function">pg_replication_origin_xact_setup()</code> 的效果。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-ADVANCE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.20.1.1.1"></a>
<code class="function">pg_replication_origin_advance</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code>, <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將指定節點的複寫進度設定為指定的位置。這主要用於設定初始位置，或在組態變更之類的情況之後設定新的位置。請注意，不慎使用這個函式可能會導致複寫的資料不一致。
       </p></td></tr><tr><td class="func_table_entry" id="PG-REPLICATION-ORIGIN-PROGRESS"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.21.1.1.1"></a>
<code class="function">pg_replication_origin_progress</code> ( <em class="parameter"><code>node_name</code></em> <code class="type">text</code>, <em class="parameter"><code>flush</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳指定複寫來源的重播位置。參數 <em class="parameter"><code>flush</code></em> 決定是否要保證對應的本地交易已排清到磁碟。
       </p></td></tr><tr><td class="func_table_entry" id="PG-LOGICAL-EMIT-MESSAGE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.22.1.1.1"></a>
<code class="function">pg_logical_emit_message</code> ( <em class="parameter"><code>transactional</code></em> <code class="type">boolean</code>, <em class="parameter"><code>prefix</code></em> <code class="type">text</code>, <em class="parameter"><code>content</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>flush</code></em> <code class="type">boolean</code> <code class="literal">DEFAULT</code> <code class="literal">false</code></span>] )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p class="func_signature">
<code class="function">pg_logical_emit_message</code> ( <em class="parameter"><code>transactional</code></em> <code class="type">boolean</code>, <em class="parameter"><code>prefix</code></em> <code class="type">text</code>, <em class="parameter"><code>content</code></em> <code class="type">bytea</code> [<span class="optional">, <em class="parameter"><code>flush</code></em> <code class="type">boolean</code> <code class="literal">DEFAULT</code> <code class="literal">false</code></span>] )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        發出一則邏輯解碼訊息。這可以用來透過 WAL 將通用訊息傳遞給邏輯解碼外掛。<em class="parameter"><code>transactional</code></em> 參數指定該訊息應該是目前交易的一部分，還是應該立即寫入，並在邏輯解碼器讀取該紀錄時立即解碼。<em class="parameter"><code>prefix</code></em> 參數是一個文字前綴，邏輯解碼外掛可以用它來輕易辨識出它們感興趣的訊息。<em class="parameter"><code>content</code></em> 參數是訊息的內容，可以用文字或二進位形式提供。<em class="parameter"><code>flush</code></em> 參數（預設為 <code class="literal">false</code>）控制是否要立即將訊息排清到 WAL。<em class="parameter"><code>flush</code></em> 在搭配 <em class="parameter"><code>transactional</code></em> 時沒有作用，因為訊息的 WAL 紀錄會與其交易一起排清。
       </p></td></tr><tr><td class="func_table_entry" id="PG-SYNC-REPLICATION-SLOTS"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.8.5.2.2.23.1.1.1"></a>
<code class="function">pg_sync_replication_slots</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        將邏輯容錯移轉複寫槽從主要伺服器同步到備用伺服器。這個函式只能在備用伺服器上執行。暫時的已同步複寫槽（如果有的話）不能用於邏輯解碼，且必須在提升之後刪除。詳情請參閱<a class="xref" href="../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION">第 47.2.3 節</a>。請注意，這個函式主要是供測試與除錯之用，應謹慎使用。此外，如果已啟用 <a class="link" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS"><code class="varname">
        sync_replication_slots</code></a>，且 slotsync 工作程序已在執行複寫槽的同步，就無法執行這個函式。
       </p>
<div class="caution"><h3 class="title">Caution</h3><p>
          如果在執行此函式之後，備用伺服器上的 <a class="link" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK"><code class="varname">hot_standby_feedback</code></a> 被停用，或是 <a class="link" href="../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME"><code class="varname">primary_slot_name</code></a> 中設定的實體複寫槽被移除，那麼已同步複寫槽所需的資料列就有可能被主要伺服器上的 VACUUM 程序移除，導致已同步複寫槽失效。
        </p></div>
</td></tr></tbody></table>

<br>

<a id="FUNCTIONS-ADMIN-DBOBJECT"></a>

### 9.28.7. 資料庫物件管理函式 [#](#FUNCTIONS-ADMIN-DBOBJECT)

[表 9.102](functions-admin.md#FUNCTIONS-ADMIN-DBSIZE) 所列的函式會計算資料庫物件的磁碟空間使用量，或協助呈現或理解使用量的結果。`bigint` 結果以位元組為單位。如果傳給這些函式的 OID 並不代表既有的物件，就會回傳 `NULL`。

<a id="FUNCTIONS-ADMIN-DBSIZE"></a>

**表 9.102. 資料庫物件大小函式**

<table border="1" class="table" summary="Database Object Size Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.1.1.1.1"></a>
<code class="function">pg_column_size</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        顯示儲存任一個別資料值所使用的位元組數。如果直接套用在資料表欄位值上，這會反映出所做的任何壓縮。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.2.1.1.1"></a>
<code class="function">pg_column_compression</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        顯示用來壓縮個別變動長度值的壓縮演算法。如果該值未經壓縮，就回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.3.1.1.1"></a>
<code class="function">pg_column_toast_chunk_id</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        顯示存放在磁碟上之 <acronym class="acronym">TOAST</acronym> 化值的 <code class="structfield">chunk_id</code>。如果該值未經 <acronym class="acronym">TOAST</acronym> 處理或不在磁碟上，就回傳 <code class="literal">NULL</code>。關於 <acronym class="acronym">TOAST</acronym> 的更多資訊，請參閱<a class="xref" href="../../internals/storage/storage-toast.md">第 66.2 節</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.4.1.1.1"></a>
<code class="function">pg_database_size</code> ( <code class="type">name</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">pg_database_size</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算具有指定名稱或 OID 之資料庫所使用的磁碟空間總量。要使用這個函式，你必須擁有指定資料庫的 <code class="literal">CONNECT</code> 權限（預設即授予），或具有 <code class="literal">pg_read_all_stats</code> 角色的權限。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.5.1.1.1"></a>
<code class="function">pg_indexes_size</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算附屬於指定資料表之索引所使用的磁碟空間總量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.6.1.1.1"></a>
<code class="function">pg_relation_size</code> ( <em class="parameter"><code>relation</code></em> <code class="type">regclass</code> [<span class="optional">, <em class="parameter"><code>fork</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算指定關聯的一個<span class="quote">「<span class="quote">fork</span>」</span>所使用的磁碟空間。（請注意，在大多數情況下，使用較高階的函式 <code class="function">pg_total_relation_size</code> 或 <code class="function">pg_table_size</code> 會更方便，它們會加總所有 fork 的大小。）只有一個引數時，這會回傳該關聯主要資料 fork 的大小。可以提供第二個引數來指定要檢查哪一個 fork：
        </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">main</code> 回傳該關聯主要資料 fork 的大小。
          </p></li><li class="listitem"><p>
<code class="literal">fsm</code> 回傳與該關聯相關聯之空閒空間對應表（Free Space Map，請參閱<a class="xref" href="../../internals/storage/storage-fsm.md">第 66.3 節</a>）的大小。
          </p></li><li class="listitem"><p>
<code class="literal">vm</code> 回傳與該關聯相關聯之可見性對應表（Visibility Map，請參閱<a class="xref" href="../../internals/storage/storage-vm.md">第 66.4 節</a>）的大小。
          </p></li><li class="listitem"><p>
<code class="literal">init</code> 回傳與該關聯相關聯之初始化 fork（如果有的話）的大小。
          </p></li></ul></div><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.7.1.1.1"></a>
<code class="function">pg_size_bytes</code> ( <code class="type">text</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        將人類易讀格式的大小（如 <code class="function">pg_size_pretty</code> 所回傳的）轉換為位元組數。有效的單位為 <code class="literal">bytes</code>、<code class="literal">B</code>、<code class="literal">kB</code>、<code class="literal">MB</code>、<code class="literal">GB</code>、<code class="literal">TB</code> 與 <code class="literal">PB</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.8.1.1.1"></a>
<code class="function">pg_size_pretty</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">pg_size_pretty</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將以位元組表示的大小，轉換為附帶大小單位（視情況使用 bytes、kB、MB、GB、TB 或 PB）、較容易讓人閱讀的格式。請注意，這些單位是 2 的次方而不是 10 的次方，所以 1kB 是 1024 個位元組，1MB 是 1024<sup>2</sup> = 1048576 個位元組，依此類推。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.9.1.1.1"></a>
<code class="function">pg_table_size</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算指定資料表所使用的磁碟空間，不包括索引（但包括其 TOAST 資料表（如果有的話）、空閒空間對應表與可見性對應表）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.10.1.1.1"></a>
<code class="function">pg_tablespace_size</code> ( <code class="type">name</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">pg_tablespace_size</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算具有指定名稱或 OID 之資料表空間所使用的磁碟空間總量。要使用這個函式，你必須擁有指定資料表空間的 <code class="literal">CREATE</code> 權限，或具有 <code class="literal">pg_read_all_stats</code> 角色的權限，除非它是目前資料庫的預設資料表空間。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.3.2.2.11.1.1.1"></a>
<code class="function">pg_total_relation_size</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算指定資料表所使用的磁碟空間總量，包括所有索引與 <acronym class="acronym">TOAST</acronym> 資料。結果等同於 <code class="function">pg_table_size</code> <code class="literal">+</code> <code class="function">pg_indexes_size</code>。
       </p></td></tr></tbody></table>

<br>

上述對資料表或索引進行操作的函式接受 `regclass` 引數，它就是該資料表或索引在 `pg_class` 系統目錄中的 OID。不過，你不必手動查詢 OID，因為 `regclass` 資料型別的輸入轉換器會替你完成這項工作。詳情請參閱[第 8.19 節](../datatype/datatype-oid.md)。

[表 9.103](functions-admin.md#FUNCTIONS-ADMIN-DBLOCATION) 所列的函式可協助識別與資料庫物件相關聯的特定磁碟檔案。

<a id="FUNCTIONS-ADMIN-DBLOCATION"></a>

**表 9.103. 資料庫物件位置函式**

<table border="1" class="table" summary="Database Object Location Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.6.2.2.1.1.1.1"></a>
<code class="function">pg_relation_filenode</code> ( <em class="parameter"><code>relation</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        回傳目前指派給指定關聯的<span class="quote">「<span class="quote">filenode</span>」</span>（檔案節點）編號。filenode 是該關聯所使用之檔案名稱的基本組成部分（更多資訊請參閱<a class="xref" href="../../internals/storage/storage-file-layout.md">第 66.1 節</a>）。對大多數關聯而言，結果與 <code class="structname">pg_class</code>.<code class="structfield">relfilenode</code> 相同，但對某些系統目錄而言，<code class="structfield">relfilenode</code> 為零，必須使用這個函式才能取得正確的值。如果傳入的是沒有儲存空間的關聯（例如檢視表），函式會回傳 NULL。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.6.2.2.2.1.1.1"></a>
<code class="function">pg_relation_filepath</code> ( <em class="parameter"><code>relation</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳該關聯完整的檔案路徑名稱（相對於資料庫叢集的資料目錄 <code class="varname">PGDATA</code>）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.6.2.2.3.1.1.1"></a>
<code class="function">pg_filenode_relation</code> ( <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code>, <em class="parameter"><code>filenode</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">regclass</code>
</p>
<p>
        依據資料表空間 OID 與關聯所存放的 filenode，回傳該關聯的 OID。這基本上是 <code class="function">pg_relation_filepath</code> 的反向對應。對於位於資料庫預設資料表空間中的關聯，資料表空間可以指定為零。如果目前資料庫中沒有任何關聯與指定的值相關聯，或處理的是暫時關聯，就回傳 <code class="literal">NULL</code>。
       </p></td></tr></tbody></table>

<br>

[表 9.104](functions-admin.md#FUNCTIONS-ADMIN-COLLATION) 列出用於管理定序的函式。

<a id="FUNCTIONS-ADMIN-COLLATION"></a>

**表 9.104. 定序管理函式**

<table border="1" class="table" summary="Collation Management Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.8.2.2.1.1.1.1"></a>
<code class="function">pg_collation_actual_version</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳該定序物件目前安裝在作業系統中的實際版本。如果這與 <code class="structname">pg_collation</code>.<code class="structfield">collversion</code> 中的值不同，那麼相依於該定序的物件可能需要重建。另請參閱 <a class="xref" href="../../reference/sql-commands/sql-altercollation.md"><span class="refentrytitle">ALTER COLLATION</span></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.8.2.2.2.1.1.1"></a>
<code class="function">pg_database_collation_actual_version</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳資料庫的定序目前安裝在作業系統中的實際版本。如果這與 <code class="structname">pg_database</code>.<code class="structfield">datcollversion</code> 中的值不同，那麼相依於該定序的物件可能需要重建。另請參閱 <a class="xref" href="../../reference/sql-commands/sql-alterdatabase.md"><span class="refentrytitle">ALTER DATABASE</span></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.8.2.2.3.1.1.1"></a>
<code class="function">pg_import_system_collations</code> ( <em class="parameter"><code>schema</code></em> <code class="type">regnamespace</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        依據在作業系統中找到的所有語系，將定序加入系統目錄 <code class="structname">pg_collation</code>。這就是 <code class="command">initdb</code> 所使用的方式；詳情請參閱<a class="xref" href="../../server-administration/charset/collation.md#COLLATION-MANAGING">第 23.2.2 節</a>。如果之後在作業系統中安裝了其他語系，可以再次執行這個函式，為新的語系加入定序。與 <code class="structname">pg_collation</code> 中既有項目相符的語系會被略過。（但以已不再存在於作業系統中之語系為基礎的定序物件，並不會被這個函式移除。）<em class="parameter"><code>schema</code></em> 參數通常會是 <code class="literal">pg_catalog</code>，但這並非必要條件；定序也可以安裝到其他綱要中。函式會回傳它所建立的新定序物件數量。這個函式只限超級使用者使用。
       </p></td></tr></tbody></table>

<br>

[表 9.105](functions-admin.md#FUNCTIONS-ADMIN-STATSMOD) 列出用於操作統計資訊的函式。這些函式不能在復原期間執行。

### 警告

這些統計資訊操作函式所做的變更，很可能會被 [autovacuum](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)（或手動執行的 `VACUUM` 或 `ANALYZE`）覆寫，因此應視為暫時性的。

<a id="FUNCTIONS-ADMIN-STATSMOD"></a>

**表 9.105. 資料庫物件統計資訊操作函式**

<table border="1" class="table" summary="Database Object Statistics Manipulation Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.10.2.2.1.1.1.1"></a>
<code class="function">pg_restore_relation_stats</code> (
        <code class="literal">VARIADIC</code> <em class="parameter"><code>kwargs</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
         更新資料表層級的統計資訊。通常這些統計資訊會自動收集，或作為 <a class="xref" href="../../reference/sql-commands/sql-vacuum.md"><span class="refentrytitle">VACUUM</span></a> 或 <a class="xref" href="../../reference/sql-commands/sql-analyze.md"><span class="refentrytitle">ANALYZE</span></a> 的一部分而更新，所以不需要呼叫這個函式。不過，在還原之後如果尚未執行 <code class="command">ANALYZE</code>，這個函式可以讓最佳化器選擇較好的執行計畫。
        </p>
<p>
         所追蹤的統計資訊可能會隨版本而改變，因此引數是以 <em class="replaceable"><code>argname</code></em> 與 <em class="replaceable"><code>argvalue</code></em> 成對的方式傳入，形式如下：
</p><pre class="programlisting">
SELECT pg_restore_relation_stats(
    '<em class="replaceable"><code>arg1name</code></em>', '<em class="replaceable"><code>arg1value</code></em>'::<em class="replaceable"><code>arg1type</code></em>,
    '<em class="replaceable"><code>arg2name</code></em>', '<em class="replaceable"><code>arg2value</code></em>'::<em class="replaceable"><code>arg2type</code></em>,
    '<em class="replaceable"><code>arg3name</code></em>', '<em class="replaceable"><code>arg3value</code></em>'::<em class="replaceable"><code>arg3type</code></em>);
</pre><p>
</p>
<p>
         例如，要設定 <code class="structfield">relpages</code> 與 <code class="structfield">reltuples</code> 在資料表 <code class="structname">mytable</code> 上的值：
</p><pre class="programlisting">
SELECT pg_restore_relation_stats(
    'schemaname', 'myschema',
    'relname',    'mytable',
    'relpages',   173::integer,
    'reltuples',  10000::real);
</pre><p>
</p>
<p>
         引數 <code class="literal">schemaname</code> 與 <code class="literal">relname</code> 是必要的，用來指定資料表。其他引數則是對應於 <a class="link" href="../../internals/catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a> 中特定欄位之統計資訊的名稱與值。目前支援的關聯統計資訊有：<code class="literal">relpages</code>（值為 <code class="type">integer</code> 型別）、<code class="literal">reltuples</code>（值為 <code class="type">real</code> 型別）、<code class="literal">relallvisible</code>（值為 <code class="type">integer</code> 型別），以及 <code class="literal">relallfrozen</code>（值為 <code class="type">integer</code> 型別）。
        </p>
<p>
         此外，這個函式還接受名為 <code class="literal">version</code>、型別為 <code class="type">integer</code> 的引數，用來指定統計資訊來源的伺服器版本。這預期有助於從較舊版本的 <span class="productname">PostgreSQL</span> 移植統計資訊。
        </p>
<p>
         輕微的錯誤會以 <code class="literal">WARNING</code> 回報並予以忽略，其餘的統計資訊仍會被還原。如果所有指定的統計資訊都成功還原，就回傳 <code class="literal">true</code>，否則回傳 <code class="literal">false</code>。
        </p>
<p>
         呼叫者必須擁有該資料表的 <code class="literal">MAINTAIN</code> 權限，或是資料庫的擁有者。
        </p>
</td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.10.2.2.2.1.1.1"></a>
<code class="function">pg_clear_relation_stats</code> ( <em class="parameter"><code>schemaname</code></em> <code class="type">text</code>, <em class="parameter"><code>relname</code></em> <code class="type">text</code> )
         → <code class="returnvalue">void</code>
</p>
<p>
         清除指定關聯的資料表層級統計資訊，就如同該資料表是新建立的一樣。
        </p>
<p>
         呼叫者必須擁有該資料表的 <code class="literal">MAINTAIN</code> 權限，或是資料庫的擁有者。
        </p>
</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.10.2.2.3.1.1.1"></a>
<code class="function">pg_restore_attribute_stats</code> (
        <code class="literal">VARIADIC</code> <em class="parameter"><code>kwargs</code></em> <code class="type">"any"</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
         建立或更新欄位層級的統計資訊。通常這些統計資訊會自動收集，或作為 <a class="xref" href="../../reference/sql-commands/sql-vacuum.md"><span class="refentrytitle">VACUUM</span></a> 或 <a class="xref" href="../../reference/sql-commands/sql-analyze.md"><span class="refentrytitle">ANALYZE</span></a> 的一部分而更新，所以不需要呼叫這個函式。不過，在還原之後如果尚未執行 <code class="command">ANALYZE</code>，這個函式可以讓最佳化器選擇較好的執行計畫。
        </p>
<p>
         所追蹤的統計資訊可能會隨版本而改變，因此引數是以 <em class="replaceable"><code>argname</code></em> 與 <em class="replaceable"><code>argvalue</code></em> 成對的方式傳入，形式如下：
</p><pre class="programlisting">
SELECT pg_restore_attribute_stats(
    '<em class="replaceable"><code>arg1name</code></em>', '<em class="replaceable"><code>arg1value</code></em>'::<em class="replaceable"><code>arg1type</code></em>,
    '<em class="replaceable"><code>arg2name</code></em>', '<em class="replaceable"><code>arg2value</code></em>'::<em class="replaceable"><code>arg2type</code></em>,
    '<em class="replaceable"><code>arg3name</code></em>', '<em class="replaceable"><code>arg3value</code></em>'::<em class="replaceable"><code>arg3type</code></em>);
</pre><p>
</p>
<p>
         例如，要設定 <code class="structfield">avg_width</code> 與 <code class="structfield">null_frac</code> 在屬性 <code class="structfield">col1</code> 上的值，該屬性屬於資料表 <code class="structname">mytable</code>：
</p><pre class="programlisting">
SELECT pg_restore_attribute_stats(
    'schemaname', 'myschema',
    'relname',    'mytable',
    'attname',    'col1',
    'inherited',  false,
    'avg_width',  125::integer,
    'null_frac',  0.5::real);
</pre><p>
</p>
<p>
         必要的引數有：<code class="literal">schemaname</code> 與 <code class="literal">relname</code>（值為 <code class="type">text</code> 型別），用來指定資料表；<code class="literal">attname</code>（值為 <code class="type">text</code> 型別）或 <code class="literal">attnum</code>（值為 <code class="type">smallint</code> 型別）二者之一，用來指定欄位；以及 <code class="literal">inherited</code>，用來指定統計資訊是否包含子資料表的值。其他引數則是對應於 <a class="link" href="../../internals/views/view-pg-stats.md"><code class="structname">pg_stats</code></a> 中欄位之統計資訊的名稱與值。
        </p>
<p>
         此外，這個函式還接受名為 <code class="literal">version</code>、型別為 <code class="type">integer</code> 的引數，用來指定統計資訊來源的伺服器版本。這預期有助於從較舊版本的 <span class="productname">PostgreSQL</span> 移植統計資訊。
        </p>
<p>
         輕微的錯誤會以 <code class="literal">WARNING</code> 回報並予以忽略，其餘的統計資訊仍會被還原。如果所有指定的統計資訊都成功還原，就回傳 <code class="literal">true</code>，否則回傳 <code class="literal">false</code>。
        </p>
<p>
         呼叫者必須擁有該資料表的 <code class="literal">MAINTAIN</code> 權限，或是資料庫的擁有者。
        </p>
</td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.10.2.2.4.1.1.1"></a>
<code class="function">pg_clear_attribute_stats</code> (
         <em class="parameter"><code>schemaname</code></em> <code class="type">text</code>,
         <em class="parameter"><code>relname</code></em> <code class="type">text</code>,
         <em class="parameter"><code>attname</code></em> <code class="type">text</code>,
         <em class="parameter"><code>inherited</code></em> <code class="type">boolean</code> )
         → <code class="returnvalue">void</code>
</p>
<p>
         清除指定關聯與屬性的欄位層級統計資訊，就如同該資料表是新建立的一樣。
        </p>
<p>
         呼叫者必須擁有該資料表的 <code class="literal">MAINTAIN</code> 權限，或是資料庫的擁有者。
        </p>
</td></tr></tbody></table>

<br>

[表 9.106](functions-admin.md#FUNCTIONS-INFO-PARTITION) 列出提供分割資料表結構相關資訊的函式。

<a id="FUNCTIONS-INFO-PARTITION"></a>

**表 9.106. 分割資訊函式**

<table border="1" class="table" summary="Partitioning Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.12.2.2.1.1.1.1"></a>
<code class="function">pg_partition_tree</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>relid</code></em> <code class="type">regclass</code>,
        <em class="parameter"><code>parentrelid</code></em> <code class="type">regclass</code>,
        <em class="parameter"><code>isleaf</code></em> <code class="type">boolean</code>,
        <em class="parameter"><code>level</code></em> <code class="type">integer</code> )
       </p>
<p>
        列出指定的分割資料表或分割索引之分割樹中的資料表或索引，每個分割區一筆資料列。所提供的資訊包括分割區的 OID、其直接父層的 OID、表示該分割區是否為葉節點的布林值，以及表示其在階層中所在層級的整數。輸入的資料表或索引的層級值為 0，其直接子分割區為 1，再下一層的分割區為 2，依此類推。如果該關聯不存在，或者既不是分割區也不是分割資料表，就不回傳任何資料列。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.12.2.2.2.1.1.1"></a>
<code class="function">pg_partition_ancestors</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">setof regclass</code>
</p>
<p>
        列出指定分割區的上層祖先關聯，包括該關聯本身。如果該關聯不存在，或者既不是分割區也不是分割資料表，就不回傳任何資料列。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.12.2.2.3.1.1.1"></a>
<code class="function">pg_partition_root</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">regclass</code>
</p>
<p>
        回傳指定關聯所屬之分割樹最頂層的父層。如果該關聯不存在，或者既不是分割區也不是分割資料表，就回傳 <code class="literal">NULL</code>。
       </p></td></tr></tbody></table>

<br>

例如，要檢查分割資料表 `measurement` 所含資料的總大小，可以使用下列查詢：

```

SELECT pg_size_pretty(sum(pg_relation_size(relid))) AS total_size
  FROM pg_partition_tree('measurement');
```

<a id="FUNCTIONS-ADMIN-INDEX"></a>

### 9.28.8. 索引維護函式 [#](#FUNCTIONS-ADMIN-INDEX)

[表 9.107](functions-admin.md#FUNCTIONS-ADMIN-INDEX-TABLE) 列出可用於索引維護工作的函式。（請注意，這些維護工作通常由 autovacuum 自動完成；只有在特殊情況下才需要使用這些函式。）這些函式不能在復原期間執行。這些函式只限超級使用者與該索引的擁有者使用。

<a id="FUNCTIONS-ADMIN-INDEX-TABLE"></a>

**表 9.107. 索引維護函式**

<table border="1" class="table" summary="Index Maintenance Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.1.1.1.1"></a>
<code class="function">brin_summarize_new_values</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        掃描指定的 BRIN 索引，找出基礎資料表中目前尚未被該索引摘要的頁面範圍；對於每個這樣的範圍，會掃描那些資料表頁面來建立新的摘要索引 tuple（值組）。回傳插入索引中的新頁面範圍摘要數量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.2.1.1.1"></a>
<code class="function">brin_summarize_range</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>blockNumber</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        如果涵蓋指定區塊的頁面範圍尚未被摘要，就對它進行摘要。這與 <code class="function">brin_summarize_new_values</code> 類似，差別在於它只處理涵蓋指定資料表區塊編號的頁面範圍。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.3.1.1.1"></a>
<code class="function">brin_desummarize_range</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>blockNumber</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        移除摘要涵蓋指定資料表區塊之頁面範圍的 BRIN 索引 tuple（值組），如果有的話。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.4.1.1.1"></a>
<code class="function">gin_clean_pending_list</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        將指定 GIN 索引之<span class="quote">「<span class="quote">pending</span>」</span>清單中的項目批次移入主要的 GIN 資料結構，藉此清理該清單。回傳從 pending 清單中移除的頁面數。如果引數是在停用 <code class="literal">fastupdate</code> 選項的情況下建立的 GIN 索引，就不會進行任何清理，結果為零，因為該索引沒有 pending 清單。關於 pending 清單與 <code class="literal">fastupdate</code> 選項的詳細資訊，請參閱<a class="xref" href="../../internals/indextypes/gin.md#GIN-FAST-UPDATE">第 65.4.4.1 節</a>與<a class="xref" href="../../internals/indextypes/gin.md#GIN-TIPS">第 65.4.5 節</a>。
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-ADMIN-GENFILE"></a>

### 9.28.9. 通用檔案存取函式 [#](#FUNCTIONS-ADMIN-GENFILE)

[表 9.108](functions-admin.md#FUNCTIONS-ADMIN-GENFILE-TABLE) 所列的函式提供對伺服器所在主機上檔案的原生存取。除非使用者是超級使用者或被授予 `pg_read_server_files` 角色，否則只能存取資料庫叢集目錄與 `log_directory` 之內的檔案。對於叢集目錄中的檔案，請使用相對路徑；對於日誌檔案，請使用與 `log_directory` 組態設定相符的路徑。

請注意，授予使用者對 `pg_read_file()` 或相關函式的 EXECUTE 權限，會讓他們能夠讀取伺服器上任何資料庫伺服器程序可讀取的檔案；這些函式會略過所有資料庫內的權限檢查。這表示，舉例來說，具有這種存取權的使用者能夠讀取存放認證資訊的 `pg_authid` 資料表內容，也能讀取資料庫中的任何資料表資料。因此，授予這些函式的存取權時應審慎考慮。

授予這些函式的權限時，請注意，資料表中顯示選用參數的項目，大多是實作為數個具有不同參數列表的實體函式。如果要使用這類函式，就必須個別對每個函式授予權限。psql 的 `\df` 指令可以用來檢查實際的函式簽章為何。

其中部分函式接受選用的 *`missing_ok`* 參數，用來指定檔案或目錄不存在時的行為。如果為 `true`，函式會視情況回傳 `NULL` 或空的結果集合。如果為 `false`，則會引發錯誤。（除了「找不到檔案」之外的失敗情況，在任何情況下都會以錯誤回報。）預設值為 `false`。

<a id="FUNCTIONS-ADMIN-GENFILE-TABLE"></a>

**表 9.108. 通用檔案存取函式**

<table border="1" class="table" summary="Generic File Access Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.1.1.1.1"></a>
<code class="function">pg_ls_dir</code> ( <em class="parameter"><code>dirname</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code>, <em class="parameter"><code>include_dot_dirs</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        回傳指定目錄中所有檔案（以及目錄與其他特殊檔案）的名稱。<em class="parameter"><code>include_dot_dirs</code></em> 參數表示是否要在結果集合中包含<span class="quote">「<span class="quote">.</span>」</span>與<span class="quote">「<span class="quote">..</span>」</span>；預設是排除它們。當 <em class="parameter"><code>missing_ok</code></em> 為 <code class="literal">true</code> 時，包含它們可以用來區分空目錄與不存在的目錄。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.2.1.1.1"></a>
<code class="function">pg_ls_logdir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器日誌目錄中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與具有 <code class="literal">pg_monitor</code> 角色權限的角色使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.3.1.1.1"></a>
<code class="function">pg_ls_waldir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器預寫式日誌（WAL）目錄中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與具有 <code class="literal">pg_monitor</code> 角色權限的角色使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.4.1.1.1"></a>
<code class="function">pg_ls_logicalmapdir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器 <code class="filename">pg_logical/mappings</code> 目錄中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.5.1.1.1"></a>
<code class="function">pg_ls_logicalsnapdir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器 <code class="filename">pg_logical/snapshots</code> 目錄中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.6.1.1.1"></a>
<code class="function">pg_ls_replslotdir</code> ( <em class="parameter"><code>slot_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器 <code class="filename">pg_replslot/slot_name</code> 目錄中每個一般檔案的名稱、大小與最後修改時間（mtime），其中 <em class="parameter"><code>slot_name</code></em> 是作為函式輸入所提供的複寫槽名稱。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.7.1.1.1"></a>
<code class="function">pg_ls_summariesdir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器 WAL 摘要目錄（<code class="filename">pg_wal/summaries</code>）中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.8.1.1.1"></a>
<code class="function">pg_ls_archive_statusdir</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳伺服器 WAL 封存狀態目錄（<code class="filename">pg_wal/archive_status</code>）中每個一般檔案的名稱、大小與最後修改時間（mtime）。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.9.1.1.1"></a>
<code class="function">pg_ls_tmpdir</code> ( [<span class="optional"> <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code> </span>] )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code> )
       </p>
<p>
        回傳指定 <em class="parameter"><code>tablespace</code></em> 之暫存檔案目錄中每個一般檔案的名稱、大小與最後修改時間（mtime）。如果未提供 <em class="parameter"><code>tablespace</code></em>，就會檢查 <code class="literal">pg_default</code> 資料表空間。以點開頭的檔名、目錄以及其他特殊檔案會被排除。
       </p>
<p>
        這個函式預設只限超級使用者與 <code class="literal">pg_monitor</code> 角色的成員使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.10.1.1.1"></a>
<code class="function">pg_read_file</code> ( <em class="parameter"><code>filename</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>length</code></em> <code class="type">bigint</code> </span>] [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳文字檔案的全部或一部分，從指定的位元組 <em class="parameter"><code>offset</code></em> 開始，最多回傳 <em class="parameter"><code>length</code></em> 個位元組（如果先到達檔案結尾則會較少）。如果 <em class="parameter"><code>offset</code></em> 為負值，則是相對於檔案結尾的位置。如果省略 <em class="parameter"><code>offset</code></em> 與 <em class="parameter"><code>length</code></em>，就會回傳整個檔案。從檔案讀取的位元組會以資料庫的編碼解讀為字串；如果它們在該編碼中無效，就會拋出錯誤。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.11.1.1.1"></a>
<code class="function">pg_read_binary_file</code> ( <em class="parameter"><code>filename</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>length</code></em> <code class="type">bigint</code> </span>] [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        回傳檔案的全部或一部分。這個函式與 <code class="function">pg_read_file</code> 相同，差別在於它可以讀取任意的二進位資料，並將結果以 <code class="type">bytea</code> 而非 <code class="type">text</code> 回傳；因此不會進行任何編碼檢查。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p>
<p>
        搭配 <code class="function">convert_from</code> 函式，這個函式可以用來讀取以指定編碼儲存的文字檔案，並將其轉換為資料庫的編碼：
</p><pre class="programlisting">
SELECT convert_from(pg_read_binary_file('file_in_utf8.txt'), 'UTF8');
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.11.6.2.2.12.1.1.1"></a>
<code class="function">pg_stat_file</code> ( <em class="parameter"><code>filename</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>size</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>access</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>modification</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>change</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>creation</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>isdir</code></em> <code class="type">boolean</code> )
       </p>
<p>
        回傳一筆紀錄，其中包含檔案的大小、最後存取時間戳記、最後修改時間戳記、最後檔案狀態變更時間戳記（僅限 Unix 平台）、檔案建立時間戳記（僅限 Windows），以及表示它是否為目錄的旗標。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-ADVISORY-LOCKS"></a>

### 9.28.10. 諮詢鎖函式 [#](#FUNCTIONS-ADVISORY-LOCKS)

[表 9.109](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS-TABLE) 所列的函式用於管理諮詢鎖。關於這些函式的正確用法，詳情請參閱[第 13.3.5 節](../mvcc/explicit-locking.md#ADVISORY-LOCKS)。

這些函式全都是用來鎖定由應用程式定義的資源，資源可以用單一個 64 位元的鍵值，或兩個 32 位元的鍵值來識別（請注意，這兩種鍵空間不會重疊）。如果另一個工作階段已經在相同的資源識別符號上持有衝突的鎖，這些函式會視函式的性質，等待資源變為可用，或是回傳 `false` 結果。鎖可以是共享鎖或排他鎖：共享鎖不會與同一資源上的其他共享鎖衝突，只會與排他鎖衝突。鎖可以在工作階段層級取得（會一直持有，直到被釋放或工作階段結束），或在交易層級取得（會一直持有，直到目前的交易結束；無法手動釋放）。多次的工作階段層級鎖請求會堆疊，因此如果同一個資源識別符號被鎖定了三次，就必須發出三次解鎖請求，才能在工作階段結束前釋放該資源。

<a id="FUNCTIONS-ADVISORY-LOCKS-TABLE"></a>

**表 9.109. 諮詢鎖函式**

<table border="1" class="table" summary="Advisory Lock Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.1.1.1.1"></a>
<code class="function">pg_advisory_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個排他的工作階段層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.2.1.1.1"></a>
<code class="function">pg_advisory_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個共享的工作階段層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.3.1.1.1"></a>
<code class="function">pg_advisory_unlock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_unlock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        釋放先前取得的排他工作階段層級諮詢鎖。如果成功釋放該鎖，就回傳 <code class="literal">true</code>。如果並未持有該鎖，就回傳 <code class="literal">false</code>，此外伺服器還會回報一則 SQL 警告。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.4.1.1.1"></a>
<code class="function">pg_advisory_unlock_all</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        釋放目前工作階段所持有的所有工作階段層級諮詢鎖。（這個函式會在工作階段結束時自動隱含地呼叫，即使用戶端並未正常中斷連線也是如此。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.5.1.1.1"></a>
<code class="function">pg_advisory_unlock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_unlock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        釋放先前取得的共享工作階段層級諮詢鎖。如果成功釋放該鎖，就回傳 <code class="literal">true</code>。如果並未持有該鎖，就回傳 <code class="literal">false</code>，此外伺服器還會回報一則 SQL 警告。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.6.1.1.1"></a>
<code class="function">pg_advisory_xact_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_xact_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個排他的交易層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.7.1.1.1"></a>
<code class="function">pg_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個共享的交易層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.8.1.1.1"></a>
<code class="function">pg_try_advisory_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個排他的工作階段層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.9.1.1.1"></a>
<code class="function">pg_try_advisory_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個共享的工作階段層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.10.1.1.1"></a>
<code class="function">pg_try_advisory_xact_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_xact_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個排他的交易層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.11.1.1.1"></a>
<code class="function">pg_try_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個共享的交易層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
