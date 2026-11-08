# 9.27.8. 交易 ID 與快照資訊函式

<a id="FUNCTIONS-INFO-SNAPSHOT"></a>

## 9.27.8. 交易 ID 與快照資訊函式 [#](#functions-info-snapshot) <a href="#functions-info-snapshot" id="functions-info-snapshot"></a>

[表 9.84](#functions-pg-snapshot) 所列的函式以可匯出的形式提供伺服器的交易資訊。這些函式的主要用途是判斷在兩個快照之間有哪些交易已經提交。

<a id="FUNCTIONS-PG-SNAPSHOT"></a>

### 表 9.84. 交易 ID 與快照資訊函式 [#](#functions-pg-snapshot) <a href="#functions-pg-snapshot" id="functions-pg-snapshot"></a>

<table border="1" class="table" summary="Transaction ID and Snapshot Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.1.1.1.1"></a>
<code class="function">age</code>  ( <code class="type">xid</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳所提供的交易 ID 與目前交易計數器之間相差的交易數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.2.1.1.1"></a>
<code class="function">mxid_age</code>  ( <code class="type">xid</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳所提供的 multixact ID 與目前 multixact 計數器之間相差的 multixact ID 數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.3.1.1.1"></a>
<code class="function">pg_current_xact_id</code> ()
        → <code class="returnvalue">xid8</code>
</p>
<p>
        回傳目前交易的 ID。如果目前交易還沒有 ID（因為它尚未執行任何資料庫更新），就會為它指派一個新的 ID；詳情請參閱<a class="xref" href="../../../internals/transactions/transaction-id.md">第 67.1 節</a>。如果是在子交易中執行，則會回傳最上層的交易 ID；詳情請參閱<a class="xref" href="../../../internals/transactions/subxacts.md">第 67.3 節</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.4.1.1.1"></a>
<code class="function">pg_current_xact_id_if_assigned</code> ()
        → <code class="returnvalue">xid8</code>
</p>
<p>
        回傳目前交易的 ID；如果尚未指派 ID，則回傳 <code class="literal">NULL</code>。（如果交易原本可能是唯讀的，最好使用這個版本，以避免不必要地消耗 XID。）如果是在子交易中執行，則會回傳最上層的交易 ID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.5.1.1.1"></a>
<code class="function">pg_xact_status</code> ( <code class="type">xid8</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回報近期某個交易的提交狀態。只要該交易夠近期，使得系統仍保留該交易的提交狀態，結果就會是 <code class="literal">in progress</code>、<code class="literal">committed</code> 或 <code class="literal">aborted</code> 其中之一。如果該交易已經久遠到系統中不再留有任何對它的參照，且提交狀態資訊已被捨棄，則結果為 <code class="literal">NULL</code>。應用程式可以使用這個函式，例如在 <code class="literal">COMMIT</code> 進行中而應用程式與資料庫伺服器之間的連線中斷後，用來判斷其交易究竟是已提交還是已中止。請注意，已預備的交易會被回報為 <code class="literal">in
        progress</code>；如果應用程式需要判斷某個交易 ID 是否屬於已預備的交易，就必須檢查 <a class="link" href="../../../internals/views/view-pg-prepared-xacts.md"><code class="structname">pg_prepared_xacts</code></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.6.1.1.1"></a>
<code class="function">pg_current_snapshot</code> ()
        → <code class="returnvalue">pg_snapshot</code>
</p>
<p>
        回傳目前的<em class="firstterm">快照</em>，這是一種資料結構，顯示目前有哪些交易 ID 正在進行中。快照中只包含最上層的交易 ID，不會顯示子交易 ID；詳情請參閱<a class="xref" href="../../../internals/transactions/subxacts.md">第 67.3 節</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.7.1.1.1"></a>
<code class="function">pg_snapshot_xip</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">setof xid8</code>
</p>
<p>
        回傳快照中所包含之進行中交易 ID 的集合。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.8.1.1.1"></a>
<code class="function">pg_snapshot_xmax</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">xid8</code>
</p>
<p>
        回傳快照的 <code class="structfield">xmax</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.9.1.1.1"></a>
<code class="function">pg_snapshot_xmin</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">xid8</code>
</p>
<p>
        回傳快照的 <code class="structfield">xmin</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.10.1.1.1"></a>
<code class="function">pg_visible_in_snapshot</code> ( <code class="type">xid8</code>, <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        依據這個快照，給定的交易 ID 是否<em class="firstterm">可見</em>（也就是說，它是否在快照取得之前就已經完成）？請注意，對於子交易 ID（subxid），這個函式不會給出正確的答案；詳情請參閱<a class="xref" href="../../../internals/transactions/subxacts.md">第 67.3 節</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.11.1.1.1"></a>
<code class="function">pg_get_multixact_members</code> ( <em class="parameter"><code>multixid</code></em> <code class="type">xid</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>mode</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳指定 multixact ID 之每個成員的交易 ID 與鎖模式。鎖模式 <code class="literal">forupd</code>、<code class="literal">fornokeyupd</code>、<code class="literal">sh</code> 與 <code class="literal">keysh</code> 分別對應於資料列層級鎖 <code class="literal">FOR UPDATE</code>、<code class="literal">FOR NO KEY UPDATE</code>、<code class="literal">FOR SHARE</code> 與 <code class="literal">FOR KEY SHARE</code>，如<a class="xref" href="../../mvcc/explicit-locking.md#locking-rows">第 13.3.2 節</a>所述。另外還有兩種 multixact 專用的模式：<code class="literal">nokeyupd</code>，用於未修改鍵欄位的更新；以及 <code class="literal">upd</code>，用於會修改鍵欄位的更新或刪除。
       </p></td></tr></tbody></table>

<br>

內部的交易 ID 型別 `xid` 為 32 位元寬，每經過 40 億個交易就會迴繞（wrap around）。不過，[表 9.84](#functions-pg-snapshot) 所列的函式，除了 `age`、`mxid_age` 與 `pg_get_multixact_members` 之外，都使用 64 位元的型別 `xid8`，它在安裝環境的整個生命週期內都不會迴繞，並且在需要時可以透過型別轉換轉為 `xid`；詳情請參閱[第 67.1 節](../../../internals/transactions/transaction-id.md)。資料型別 `pg_snapshot` 儲存在某個特定時間點的交易 ID 可見性資訊。其組成部分說明於[表 9.85](#functions-pg-snapshot-parts)。`pg_snapshot` 的文字表示形式為 `xmin:xmax:xip_list`。例如 `10:20:10,14,15` 表示 `xmin=10, xmax=20, xip_list=10, 14, 15`。

<a id="FUNCTIONS-PG-SNAPSHOT-PARTS"></a>

### 表 9.85. 快照組成部分 [#](#functions-pg-snapshot-parts) <a href="#functions-pg-snapshot-parts" id="functions-pg-snapshot-parts"></a>

<table border="1" class="table" summary="Snapshot Components"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">xmin</code></td><td>
         仍在進行中的最小交易 ID。所有小於 <code class="structfield">xmin</code> 的交易 ID，不是已提交且可見，就是已回滾且無效。
       </td></tr><tr><td><code class="structfield">xmax</code></td><td>
         比已完成之最大交易 ID 大一的值。所有大於或等於 <code class="structfield">xmax</code> 的交易 ID，在取得快照時都尚未完成，因此是不可見的。
       </td></tr><tr><td><code class="structfield">xip_list</code></td><td>
        取得快照時正在進行中的交易。若某個交易 ID 符合 <code class="literal">xmin &lt;= <em class="replaceable"><code>X</code></em> &lt; xmax</code> 且不在這個清單中，表示它在取得快照時已經完成，因此依其提交狀態，不是可見就是無效。這個清單不包含子交易的交易 ID（subxid）。
       </td></tr></tbody></table>

<br>

在 PostgreSQL 13 之前的版本中沒有 `xid8` 型別，因此提供了這些函式的變體，它們使用 `bigint` 來表示 64 位元的 XID，並相對應地使用另一個獨立的快照資料型別 `txid_snapshot`。這些較舊的函式名稱中帶有 `txid`。為了向下相容，它們仍然受到支援，但可能會在未來的版本中移除。請參閱[表 9.86](#functions-txid-snapshot)。

<a id="FUNCTIONS-TXID-SNAPSHOT"></a>

### 表 9.86. 已棄用的交易 ID 與快照資訊函式 [#](#functions-txid-snapshot) <a href="#functions-txid-snapshot" id="functions-txid-snapshot"></a>

<table border="1" class="table" summary="Deprecated Transaction ID and Snapshot Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.1.1.1.1"></a>
<code class="function">txid_current</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_current_xact_id()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.2.1.1.1"></a>
<code class="function">txid_current_if_assigned</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_current_xact_id_if_assigned()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.3.1.1.1"></a>
<code class="function">txid_current_snapshot</code> ()
        → <code class="returnvalue">txid_snapshot</code>
</p>
<p>
        See <code class="function">pg_current_snapshot()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.4.1.1.1"></a>
<code class="function">txid_snapshot_xip</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">setof bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xip()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.5.1.1.1"></a>
<code class="function">txid_snapshot_xmax</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xmax()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.6.1.1.1"></a>
<code class="function">txid_snapshot_xmin</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xmin()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.7.1.1.1"></a>
<code class="function">txid_visible_in_snapshot</code> ( <code class="type">bigint</code>, <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        See <code class="function">pg_visible_in_snapshot()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.8.1.1.1"></a>
<code class="function">txid_status</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        See <code class="function">pg_xact_status()</code>.
       </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
