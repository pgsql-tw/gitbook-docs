# 9.27.1. 工作階段資訊函式

<a id="FUNCTIONS-INFO-SESSION"></a>

## 9.27.1. 工作階段資訊函式 [#](#functions-info-session) <a href="#functions-info-session" id="functions-info-session"></a>

[表 9.71](#functions-info-session-table) 列出了幾個擷取工作階段與系統資訊的函式。

除了本節所列的函式之外，還有一些與統計系統相關的函式也會提供系統資訊。詳情請參閱[第 27.2.26 節](../../../server-administration/monitoring/monitoring-stats.md#monitoring-stats-functions)。

<a id="FUNCTIONS-INFO-SESSION-TABLE"></a>

### 表 9.71. 工作階段資訊函式 [#](#functions-info-session-table) <a href="#functions-info-session-table" id="functions-info-session-table"></a>

<table border="1" class="table" summary="Session Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.1.1.1.1"></a>
<code class="function">current_catalog</code>
        → <code class="returnvalue">name</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.1.1.2.1"></a>
<code class="function">current_database</code> ()
        → <code class="returnvalue">name</code>
</p>
<p>
        回傳目前資料庫的名稱。（在 SQL 標準中，資料庫稱為<span class="quote">「<span class="quote">catalog</span>」</span>，因此 <code class="function">current_catalog</code> 是標準的寫法。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.2.1.1.1"></a>
<code class="function">current_query</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳目前正在執行之查詢的文字，也就是用戶端所送出的內容（其中可能包含不只一個陳述句）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.3.1.1.1"></a>
<code class="function">current_role</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        這等同於 <code class="function">current_user</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.4.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.4.1.1.2"></a>
<code class="function">current_schema</code>
        → <code class="returnvalue">name</code>
</p>
<p class="func_signature">
<code class="function">current_schema</code> ()
        → <code class="returnvalue">name</code>
</p>
<p>
        回傳搜尋路徑中第一個綱要的名稱（如果搜尋路徑為空，則回傳 NULL 值）。這個綱要就是在未指定目標綱要的情況下，建立任何資料表或其他具名物件時所使用的綱要。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.5.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.5.1.1.2"></a>
<code class="function">current_schemas</code> ( <em class="parameter"><code>include_implicit</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">name[]</code>
</p>
<p>
        依優先順序回傳目前有效搜尋路徑中所有綱要名稱所組成的陣列。（目前 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH">search_path</a> 設定中，不對應於現存且可搜尋之綱要的項目會被省略。）如果布林引數為 <code class="literal">true</code>，則像 <code class="literal">pg_catalog</code> 這類會被隱含搜尋的系統綱要也會包含在結果中。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.6.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.6.1.1.2"></a>
<code class="function">current_user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        回傳目前執行情境的使用者名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.7.1.1.1"></a>
<code class="function">inet_client_addr</code> ()
        → <code class="returnvalue">inet</code>
</p>
<p>
        回傳目前用戶端的 IP 位址；如果目前的連線是透過 Unix-domain socket，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.8.1.1.1"></a>
<code class="function">inet_client_port</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳目前用戶端的 IP 連接埠號碼；如果目前的連線是透過 Unix-domain socket，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.9.1.1.1"></a>
<code class="function">inet_server_addr</code> ()
        → <code class="returnvalue">inet</code>
</p>
<p>
        回傳伺服器接受目前連線時所使用的 IP 位址；如果目前的連線是透過 Unix-domain socket，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.10.1.1.1"></a>
<code class="function">inet_server_port</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳伺服器接受目前連線時所使用的 IP 連接埠號碼；如果目前的連線是透過 Unix-domain socket，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.11.1.1.1"></a>
<code class="function">pg_backend_pid</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳附屬於目前工作階段之伺服器程序的程序 ID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.12.1.1.1"></a>
<code class="function">pg_blocking_pids</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        回傳一個陣列，內容為阻擋指定程序 ID 之伺服器程序取得鎖的那些工作階段的程序 ID；如果沒有這樣的伺服器程序，或者它並未被阻擋，則回傳空陣列。
       </p>
<p>
        一個伺服器程序會阻擋另一個伺服器程序的情形有兩種：它持有與被阻擋程序的鎖請求相衝突的鎖（硬性阻擋），或者它正在等待一個會與被阻擋程序的鎖請求相衝突的鎖，且在等待佇列中排在被阻擋程序之前（軟性阻擋）。使用平行查詢時，即使實際的鎖是由子工作程序持有或等待，結果中列出的一律是用戶端可見的程序 ID（也就是 <code class="function">pg_backend_pid</code> 的結果）。因此，結果中可能會有重複的 PID。另請注意，當一個已預備的交易持有相衝突的鎖時，會以程序 ID 零來表示。
       </p>
<p>
        頻繁呼叫這個函式可能會對資料庫效能造成一些影響，因為它需要短暫地獨占存取鎖管理器的共享狀態。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.13.1.1.1"></a>
<code class="function">pg_conf_load_time</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳伺服器組態檔最後一次載入的時間。如果目前的工作階段在那時已經存在，這會是該工作階段本身重新讀取組態檔的時間（因此在不同的工作階段中，讀到的值會稍有不同）。否則，就是 postmaster 程序重新讀取組態檔的時間。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.2"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.3"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.4"></a>
<code class="function">pg_current_logfile</code> ( [<span class="optional"> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳日誌收集器目前正在使用之日誌檔的路徑名稱。此路徑包含 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DIRECTORY">log_directory</a> 目錄以及個別的日誌檔名稱。如果日誌收集器已停用，結果為 <code class="literal">NULL</code>。當存在多個各自採用不同格式的日誌檔時，不帶引數的 <code class="function">pg_current_logfile</code> 會依照 <code class="literal">stderr</code>、<code class="literal">csvlog</code>、<code class="literal">jsonlog</code> 的順序，回傳第一個找到之格式的檔案路徑。如果沒有任何日誌檔採用這些格式，則回傳 <code class="literal">NULL</code>。若要取得特定日誌檔格式的資訊，請以 <code class="literal">csvlog</code>、<code class="literal">jsonlog</code> 或 <code class="literal">stderr</code> 作為選用參數的值。如果所要求的日誌格式未設定於 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DESTINATION">log_destination</a> 中，結果為 <code class="literal">NULL</code>。結果反映的是 <code class="filename">current_logfiles</code> 檔案的內容。
       </p>
<p>
        這個函式預設僅限超級使用者以及具有 <code class="literal">pg_monitor</code> 角色權限的角色使用，但也可以授予其他使用者 EXECUTE 權限來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.15.1.1.1"></a>
<code class="function">pg_get_loaded_modules</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>module_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>version</code></em> <code class="type">text</code>,
        <em class="parameter"><code>file_name</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳已載入目前伺服器工作階段的可載入模組清單。<em class="parameter"><code>module_name</code></em> 與 <em class="parameter"><code>version</code></em> 欄位的值為 NULL，除非模組作者已使用 <code class="literal">PG_MODULE_MAGIC_EXT</code> 巨集為它們提供值。<em class="parameter"><code>file_name</code></em> 欄位提供模組（共享函式庫）的檔案名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.16.1.1.1"></a>
<code class="function">pg_my_temp_schema</code> ()
        → <code class="returnvalue">oid</code>
</p>
<p>
        回傳目前工作階段之暫存綱要的 OID；如果沒有暫存綱要（因為它尚未建立任何暫存資料表），則回傳零。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.17.1.1.1"></a>
<code class="function">pg_is_other_temp_schema</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果給定的 OID 是其他工作階段之暫存綱要的 OID，就回傳 true。（這很有用，例如可用來在顯示系統目錄內容時排除其他工作階段的暫存資料表。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.18.1.1.1"></a>
<code class="function">pg_jit_available</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果有可用的 <acronym class="acronym">JIT</acronym> 編譯器擴充功能（請參閱<a class="xref" href="../../../server-administration/jit/README.md">第 30 章</a>），並且 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-query.md#GUC-JIT">jit</a> 組態參數設定為 <code class="literal">on</code>，就回傳 true。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.19.1.1.1"></a>
<code class="function">pg_numa_available</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果伺服器編譯時加入了 <acronym class="acronym">NUMA</acronym> 支援，就回傳 true。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.20.1.1.1"></a>
<code class="function">pg_listening_channels</code> ()
        → <code class="returnvalue">setof text</code>
</p>
<p>
        回傳目前工作階段正在監聽的非同步通知頻道名稱集合。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.21.1.1.1"></a>
<code class="function">pg_notification_queue_usage</code> ()
        → <code class="returnvalue">double precision</code>
</p>
<p>
        回傳非同步通知佇列目前被等待處理之通知所占用的比例（0–1），以佇列最大容量為基準。詳情請參閱 <a class="xref" href="../../../reference/sql-commands/sql-listen.md"><span class="refentrytitle">LISTEN</span></a> 與 <a class="xref" href="../../../reference/sql-commands/sql-notify.md"><span class="refentrytitle">NOTIFY</span></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.22.1.1.1"></a>
<code class="function">pg_postmaster_start_time</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳伺服器啟動的時間。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.23.1.1.1"></a>
<code class="function">pg_safe_snapshot_blocking_pids</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        回傳一個陣列，內容為阻擋指定程序 ID 之伺服器程序取得安全快照的那些工作階段的程序 ID；如果沒有這樣的伺服器程序，或者它並未被阻擋，則回傳空陣列。
       </p>
<p>
        執行 <code class="literal">SERIALIZABLE</code> 交易的工作階段，會阻擋 <code class="literal">SERIALIZABLE READ ONLY DEFERRABLE</code> 交易取得快照，直到後者判定可以安全地避免取得任何述詞鎖為止。關於可序列化與可延後交易的更多資訊，請參閱<a class="xref" href="../../mvcc/transaction-iso.md#xact-serializable">第 13.2.3 節</a>。
       </p>
<p>
        頻繁呼叫這個函式可能會對資料庫效能造成一些影響，因為它需要短暫地存取述詞鎖管理器的共享狀態。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.24.1.1.1"></a>
<code class="function">pg_trigger_depth</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 <span class="productname">PostgreSQL</span> 觸發程序目前的巢狀層級（如果不是直接或間接從觸發程序內部呼叫，則為 0）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.25.1.1.1"></a>
<code class="function">session_user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        回傳工作階段使用者的名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.26.1.1.1"></a>
<code class="function">system_user</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳使用者在被指派資料庫角色之前，於認證過程中所提出的認證方法與身分（如果有的話）。其表示形式為 <code class="literal">auth_method:identity</code>；如果使用者未經認證（例如使用了 <a class="link" href="../../../server-administration/client-authentication/auth-trust.md">Trust 認證</a>），則為 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.27.1.1.1"></a>
<code class="function">user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        這等同於 <code class="function">current_user</code>。
       </p></td></tr></tbody></table>

<br>

### 注意

`current_catalog`、`current_role`、`current_schema`、`current_user`、`session_user` 與 `user` 在 SQL 中具有特殊的語法地位：呼叫它們時不能加上尾端的括號。在 PostgreSQL 中，`current_schema` 可以選擇性地加上括號，但其他幾個則不行。

`session_user` 通常是發起目前資料庫連線的使用者；但超級使用者可以使用 [SET SESSION AUTHORIZATION](../../../reference/sql-commands/sql-set-session-authorization.md) 變更這項設定。`current_user` 是用於權限檢查的使用者識別。通常它與工作階段使用者相同，但可以使用 [SET ROLE](../../../reference/sql-commands/sql-set-role.md) 加以變更。在執行具有 `SECURITY DEFINER` 屬性的函式期間，它也會改變。以 Unix 的說法，工作階段使用者是「真實使用者」（real user），而目前使用者是「有效使用者」（effective user）。`current_role` 與 `user` 是 `current_user` 的同義詞。（SQL 標準區分了 `current_role` 與 `current_user`，但 PostgreSQL 並不區分，因為它將使用者與角色統一為單一種類的實體。）

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
