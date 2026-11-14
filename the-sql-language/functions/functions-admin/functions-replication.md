# 9.28.6. 複寫管理函式

<a id="FUNCTIONS-REPLICATION"></a>

## 9.28.6. 複寫管理函式 [#](#functions-replication) <a href="#functions-replication" id="functions-replication"></a>

[表 9.101](#functions-replication-table) 所列的函式用於控制複寫功能並與之互動。關於底層功能的資訊，請參閱[第 26.2.5 節](../../../server-administration/high-availability/warm-standby.md#streaming-replication)、[第 26.2.6 節](../../../server-administration/high-availability/warm-standby.md#streaming-replication-slots)與[第 48 章](../../../server-programming/replication-origins/README.md)。複寫來源相關函式預設只允許超級使用者使用，但可以使用 `GRANT` 指令允許其他使用者使用。複寫槽相關函式則只限超級使用者與具有 `REPLICATION` 權限的使用者使用。

這些函式中有許多在複寫協定中都有對應的指令；請參閱[第 54.4 節](../../../internals/protocol/protocol-replication.md)。

[第 9.28.3 節](functions-admin-backup.md#functions-admin-backup)、[第 9.28.4 節](functions-recovery-control.md#functions-recovery-control)與[第 9.28.5 節](functions-snapshot-synchronization.md#functions-snapshot-synchronization)所說明的函式也與複寫相關。

<a id="FUNCTIONS-REPLICATION-TABLE"></a>

### 表 9.101. 複寫管理函式 [#](#functions-replication-table) <a href="#functions-replication-table" id="functions-replication-table"></a>

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
        建立一個名為 <em class="parameter"><code>slot_name</code></em> 的新實體複寫槽。選用的第二個參數為 <code class="literal">true</code> 時，表示要立即為這個複寫槽保留 <acronym class="acronym">LSN</acronym>；否則會在串流複寫用戶端第一次連線時才保留 <acronym class="acronym">LSN</acronym>。只有透過串流複寫協定，才能從實體複寫槽串流傳送變更——請參閱<a class="xref" href="../../../internals/protocol/protocol-replication.md">第 54.4 節</a>。選用的第三個參數 <em class="parameter"><code>temporary</code></em> 設為 true 時，表示這個複寫槽不應永久儲存到磁碟，且只供目前的工作階段使用。暫時複寫槽在發生任何錯誤時也會被釋放。這個函式對應於複寫協定指令 <code class="literal">CREATE_REPLICATION_SLOT
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
        回傳複寫槽 <em class="parameter"><code>slot_name</code></em> 中的變更，從上次取用變更之處開始。如果 <em class="parameter"><code>upto_lsn</code></em> 與 <em class="parameter"><code>upto_nchanges</code></em> 皆為 NULL，邏輯解碼會一直進行到 WAL 的結尾。如果 <em class="parameter"><code>upto_lsn</code></em> 不為 NULL，解碼只會包含在指定 LSN 之前提交的交易。如果 <em class="parameter"><code>upto_nchanges</code></em> 不為 NULL，當解碼產生的資料列數超過指定值時，解碼就會停止。不過請注意，實際回傳的資料列數可能會更多，因為這個限制只會在加入解碼每個新交易提交時所產生的資料列之後才檢查。如果指定的複寫槽是邏輯容錯移轉複寫槽，函式要等到 <a class="link" href="../../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS"><code class="varname">synchronized_standby_slots</code></a> 中指定的所有實體複寫槽都已確認收到 WAL 之後才會回傳。
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
        推進名為 <em class="parameter"><code>slot_name</code></em> 之複寫槽目前已確認的位置。複寫槽不會向後移動，也不會移動到超過目前插入位置之處。回傳複寫槽的名稱，以及它實際推進到的位置。如果有進行任何推進，更新後的複寫槽位置資訊會在下一個檢查點時寫出。因此在當機的情況下，複寫槽可能會回到較早的位置。如果指定的複寫槽是邏輯容錯移轉複寫槽，函式要等到 <a class="link" href="../../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS"><code class="varname">synchronized_standby_slots</code></a> 中指定的所有實體複寫槽都已確認收到 WAL 之後才會回傳。
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
        將邏輯容錯移轉複寫槽從主要伺服器同步到備用伺服器。這個函式只能在備用伺服器上執行。暫時的已同步複寫槽（如果有的話）不能用於邏輯解碼，且必須在提升之後刪除。詳情請參閱<a class="xref" href="../../../server-programming/logicaldecoding/logicaldecoding-explanation.md#logicaldecoding-replication-slots-synchronization">第 47.2.3 節</a>。請注意，這個函式主要是供測試與除錯之用，應謹慎使用。此外，如果已啟用 <a class="link" href="../../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS"><code class="varname">
        sync_replication_slots</code></a>，且 slotsync 工作程序已在執行複寫槽的同步，就無法執行這個函式。
       </p>
<div class="caution"><h3 class="title">Caution</h3><p>
          如果在執行此函式之後，備用伺服器上的 <a class="link" href="../../../server-administration/runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK"><code class="varname">hot_standby_feedback</code></a> 被停用，或是 <a class="link" href="../../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME"><code class="varname">primary_slot_name</code></a> 中設定的實體複寫槽被移除，那麼已同步複寫槽所需的資料列就有可能被主要伺服器上的 VACUUM 程序移除，導致已同步複寫槽失效。
        </p></div>
</td></tr></tbody></table>

<br>

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
