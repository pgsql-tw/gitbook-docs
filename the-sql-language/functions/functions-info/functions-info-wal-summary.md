# 9.27.12. WAL 摘要資訊函式

<a id="FUNCTIONS-INFO-WAL-SUMMARY"></a>

## 9.27.12. WAL 摘要資訊函式 [#](#functions-info-wal-summary) <a href="#functions-info-wal-summary" id="functions-info-wal-summary"></a>

[表 9.94](#functions-wal-summary) 所列的函式會輸出 WAL 摘要的狀態資訊。請參閱 [summarize_wal](../../../server-administration/runtime-config/runtime-config-wal.md#GUC-SUMMARIZE-WAL)。

<a id="FUNCTIONS-WAL-SUMMARY"></a>

### 表 9.94. WAL 摘要資訊函式 [#](#functions-wal-summary) <a href="#functions-wal-summary" id="functions-wal-summary"></a>

<table border="1" class="table" summary="WAL Summarization Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.1.1.1.1"></a>
<code class="function">pg_available_wal_summaries</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tli</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>start_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>end_lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        回傳資料目錄中 <code class="literal">pg_wal/summaries</code> 底下現有 WAL 摘要檔的資訊。每個 WAL 摘要檔會回傳一筆資料列。每個檔案摘要了指定 TLI 上、指定 LSN 範圍內的 WAL。這個函式可用來判斷伺服器上是否存在足夠的 WAL 摘要，以便根據某個起始 LSN 已知的先前備份來進行增量備份。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.2.1.1.1"></a>
<code class="function">pg_wal_summary_contents</code> ( <em class="parameter"><code>tli</code></em> <code class="type">bigint</code>, <em class="parameter"><code>start_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>end_lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>relfilenode</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>reltablespace</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>reldatabase</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>relforknumber</code></em> <code class="type">smallint</code>,
        <em class="parameter"><code>relblocknumber</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>is_limit_block</code></em> <code class="type">boolean</code> )
       </p>
<p>
        回傳由 TLI 以及起始與結束 LSN 所識別之單一 WAL 摘要檔的內容資訊。<code class="literal">is_limit_block</code> 為 false 的每一筆資料列，表示由其餘輸出欄位所識別的區塊，在這個檔案所摘要的紀錄範圍內至少被一筆 WAL 紀錄修改過。<code class="literal">is_limit_block</code> 為 true 的每一筆資料列，則表示：(a) 該關聯的 fork 在相關的 WAL 紀錄範圍內被截斷為 <code class="literal">relblocknumber</code> 所給定的長度，或者 (b) 該關聯的 fork 在相關的 WAL 紀錄範圍內被建立或刪除；在後者的情況下，<code class="literal">relblocknumber</code> 會是零。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.3.1.1.1"></a>
<code class="function">pg_get_wal_summarizer_state</code> ()
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>summarized_tli</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>summarized_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>pending_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>summarizer_pid</code></em> <code class="type">int</code> )
       </p>
<p>
        回傳 WAL 摘要程序（WAL summarizer）進度的資訊。如果自執行個體啟動以來 WAL 摘要程序從未執行過，則 <code class="literal">summarized_tli</code> 與 <code class="literal">summarized_lsn</code> 分別為 <code class="literal">0</code> 與 <code class="literal">0/0</code>；否則，它們會是最後一個寫入磁碟之 WAL 摘要檔的 TLI 與結束 LSN。如果 WAL 摘要程序目前正在執行，<code class="literal">pending_lsn</code> 會是它最後處理完之紀錄的結束 LSN，其值必定大於或等於 <code class="literal">summarized_lsn</code>；如果 WAL 摘要程序沒有在執行，它會等於 <code class="literal">summarized_lsn</code>。<code class="literal">summarizer_pid</code> 是 WAL 摘要程序的 PID（如果它正在執行），否則為 NULL。
       </p>
<p>
        作為特殊的例外，如果 WAL 是在 <code class="literal">wal_level=minimal</code> 設定下產生的，WAL 摘要程序會拒絕為其產生 WAL 摘要檔，因為這樣的摘要若作為增量備份的基礎並不安全。在這種情況下，上述欄位仍會像正在產生摘要一樣持續推進，但不會有任何內容寫入磁碟。一旦摘要程序處理到 <code class="literal">wal_level</code> 設定為 <code class="literal">replica</code> 或更高層級時所產生的 WAL，它就會恢復將摘要寫入磁碟。
       </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
