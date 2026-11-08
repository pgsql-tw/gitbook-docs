# 9.28.2. 伺服器訊號函式

<a id="FUNCTIONS-ADMIN-SIGNAL"></a>

## 9.28.2. 伺服器訊號函式 [#](#functions-admin-signal) <a href="#functions-admin-signal" id="functions-admin-signal"></a>

<a id="id-1.5.8.34.4.2"></a>

[表 9.96](#functions-admin-signal-table) 所列的函式會向其他伺服器程序傳送控制訊號。這些函式預設只限超級使用者使用，但可以使用 `GRANT` 將存取權授予其他使用者，另有註明的例外情形除外。

這些函式在訊號傳送成功時都會回傳 `true`，傳送失敗時則回傳 `false`。

<a id="FUNCTIONS-ADMIN-SIGNAL-TABLE"></a>

### 表 9.96. 伺服器訊號函式 [#](#functions-admin-signal-table) <a href="#functions-admin-signal-table" id="functions-admin-signal-table"></a>

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
        請求將具有指定程序 ID 之後端的記憶體內容記錄到日誌中。這個函式可以將請求傳送給 logger 以外的後端與輔助程序。這些記憶體內容會以 <code class="literal">LOG</code> 訊息層級記錄。它們會依照所設定的日誌組態出現在伺服器日誌中（更多資訊請參閱<a class="xref" href="../../../server-administration/runtime-config/runtime-config-logging.md">第 19.8 節</a>），但無論 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES">client_min_messages</a> 如何設定，都不會傳送給用戶端。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.4.5.2.2.3.1.1.1"></a>
<code class="function">pg_reload_conf</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        讓 <span class="productname">PostgreSQL</span> 伺服器的所有程序重新載入它們的組態檔案。（這是透過向 postmaster 程序傳送 <span class="systemitem">SIGHUP</span> 訊號來啟動的，postmaster 接著會向它的每個子程序傳送 <span class="systemitem">SIGHUP</span>。）在重新載入之前，你可以使用 <a class="link" href="../../../internals/views/view-pg-file-settings.md"><code class="structname">pg_file_settings</code></a>、<a class="link" href="../../../internals/views/view-pg-hba-file-rules.md"><code class="structname">pg_hba_file_rules</code></a> 與 <a class="link" href="../../../internals/views/view-pg-ident-file-mappings.md"><code class="structname">pg_ident_file_mappings</code></a> 檢視表來檢查組態檔案中可能的錯誤。
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

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
