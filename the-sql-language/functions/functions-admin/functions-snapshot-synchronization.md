# 9.28.5. 快照同步函式

<a id="FUNCTIONS-SNAPSHOT-SYNCHRONIZATION"></a>

## 9.28.5. 快照同步函式 [#](#functions-snapshot-synchronization) <a href="#functions-snapshot-synchronization" id="functions-snapshot-synchronization"></a>

PostgreSQL 允許資料庫工作階段同步它們的快照。*快照*決定了哪些資料對正在使用該快照的交易是可見的。當兩個以上的工作階段需要看到資料庫中完全相同的內容時，就需要同步快照。如果兩個工作階段只是各自獨立地開始交易，那麼總是有可能在兩個 `START TRANSACTION` 指令執行之間，有第三個交易提交，使得其中一個工作階段看得到該交易的效果，而另一個則看不到。

為了解決這個問題，PostgreSQL 允許交易*匯出*（export）它正在使用的快照。只要匯出快照的交易仍保持開啟，其他交易就可以*匯入*（import）它的快照，從而保證它們看到的資料庫狀態與第一個交易所看到的完全相同。但請注意，這些交易中任何一個所做的資料庫變更，對其他交易仍然是不可見的，這與未提交交易所做的變更一般情況相同。因此，這些交易對於既有的資料是同步的，但對於它們自己所做的變更則照常運作。

快照是以 `pg_export_snapshot` 函式匯出（如[表 9.100](#functions-snapshot-synchronization-table) 所示），並以 [SET TRANSACTION](../../../reference/sql-commands/sql-set-transaction.md) 指令匯入。

<a id="FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE"></a>

### 表 9.100. 快照同步函式 [#](#functions-snapshot-synchronization-table) <a href="#functions-snapshot-synchronization-table" id="functions-snapshot-synchronization-table"></a>

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
        如有需要，一個交易可以匯出多個快照。請注意，這樣做只在 <code class="literal">READ COMMITTED</code> 交易中才有用，因為在 <code class="literal">REPEATABLE READ</code> 及更高的隔離等級中，交易在其整個生命週期內都使用同一個快照。一旦交易匯出了任何快照，就不能再以 <a class="xref" href="../../../reference/sql-commands/sql-prepare-transaction.md"><span class="refentrytitle">PREPARE TRANSACTION</span></a> 進行準備。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.7.5.2.2.2.1.1.1"></a>
<code class="function">pg_log_standby_snapshot</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        擷取執行中交易的快照並寫入 WAL，而不必等待 bgwriter 或 checkpointer 記錄一筆。這對於在備用伺服器上進行邏輯解碼很有用，因為建立邏輯複寫槽必須等到這樣的紀錄在備用伺服器上重播之後才能進行。
       </p></td></tr></tbody></table>

<br>

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
