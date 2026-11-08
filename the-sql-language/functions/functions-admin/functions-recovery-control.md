# 9.28.4. 復原控制函式

<a id="FUNCTIONS-RECOVERY-CONTROL"></a>

## 9.28.4. 復原控制函式 [#](#functions-recovery-control) <a href="#functions-recovery-control" id="functions-recovery-control"></a>

[表 9.98](#functions-recovery-info-table) 所列的函式提供備用伺服器目前狀態的相關資訊。這些函式在復原期間與正常執行時都可以執行。

<a id="FUNCTIONS-RECOVERY-INFO-TABLE"></a>

### 表 9.98. 復原資訊函式 [#](#functions-recovery-info-table) <a href="#functions-recovery-info-table" id="functions-recovery-info-table"></a>

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

[表 9.99](#functions-recovery-control-table) 所列的函式用於控制復原的進度。這些函式只能在復原期間執行。

<a id="FUNCTIONS-RECOVERY-CONTROL-TABLE"></a>

### 表 9.99. 復原控制函式 [#](#functions-recovery-control-table) <a href="#functions-recovery-control-table" id="functions-recovery-control-table"></a>

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

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
