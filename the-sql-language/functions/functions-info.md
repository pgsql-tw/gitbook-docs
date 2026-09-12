<a id="FUNCTIONS-INFO"></a>

## 9.27. 系統資訊函式與運算子 [#](#FUNCTIONS-INFO)

[9.27.1. 工作階段資訊函式](functions-info.md#FUNCTIONS-INFO-SESSION)

[9.27.2. 存取權限查詢函式](functions-info.md#FUNCTIONS-INFO-ACCESS)

[9.27.3. 綱要可見性查詢函式](functions-info.md#FUNCTIONS-INFO-SCHEMA)

[9.27.4. 系統目錄資訊函式](functions-info.md#FUNCTIONS-INFO-CATALOG)

[9.27.5. 物件資訊與定址函式](functions-info.md#FUNCTIONS-INFO-OBJECT)

[9.27.6. 註解資訊函式](functions-info.md#FUNCTIONS-INFO-COMMENT)

[9.27.7. 資料有效性檢查函式](functions-info.md#FUNCTIONS-INFO-VALIDITY)

[9.27.8. 交易 ID 與快照資訊函式](functions-info.md#FUNCTIONS-INFO-SNAPSHOT)

[9.27.9. 已提交交易資訊函式](functions-info.md#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

[9.27.10. 控制資料函式](functions-info.md#FUNCTIONS-INFO-CONTROLDATA)

[9.27.11. 版本資訊函式](functions-info.md#FUNCTIONS-INFO-VERSION)

[9.27.12. WAL 摘要資訊函式](functions-info.md#FUNCTIONS-INFO-WAL-SUMMARY)

本節所描述的函式用於取得 PostgreSQL 安裝環境的各種資訊。

<a id="FUNCTIONS-INFO-SESSION"></a>

### 9.27.1. 工作階段資訊函式 [#](#FUNCTIONS-INFO-SESSION)

[表 9.71](functions-info.md#FUNCTIONS-INFO-SESSION-TABLE) 列出了幾個擷取工作階段與系統資訊的函式。

除了本節所列的函式之外，還有一些與統計系統相關的函式也會提供系統資訊。詳情請參閱[第 27.2.26 節](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCTIONS)。

<a id="FUNCTIONS-INFO-SESSION-TABLE"></a>

**表 9.71. 工作階段資訊函式**

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
        依優先順序回傳目前有效搜尋路徑中所有綱要名稱所組成的陣列。（目前 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH">search_path</a> 設定中，不對應於現存且可搜尋之綱要的項目會被省略。）如果布林引數為 <code class="literal">true</code>，則像 <code class="literal">pg_catalog</code> 這類會被隱含搜尋的系統綱要也會包含在結果中。
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
        回傳日誌收集器目前正在使用之日誌檔的路徑名稱。此路徑包含 <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DIRECTORY">log_directory</a> 目錄以及個別的日誌檔名稱。如果日誌收集器已停用，結果為 <code class="literal">NULL</code>。當存在多個各自採用不同格式的日誌檔時，不帶引數的 <code class="function">pg_current_logfile</code> 會依照 <code class="literal">stderr</code>、<code class="literal">csvlog</code>、<code class="literal">jsonlog</code> 的順序，回傳第一個找到之格式的檔案路徑。如果沒有任何日誌檔採用這些格式，則回傳 <code class="literal">NULL</code>。若要取得特定日誌檔格式的資訊，請以 <code class="literal">csvlog</code>、<code class="literal">jsonlog</code> 或 <code class="literal">stderr</code> 作為選用參數的值。如果所要求的日誌格式未設定於 <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DESTINATION">log_destination</a> 中，結果為 <code class="literal">NULL</code>。結果反映的是 <code class="filename">current_logfiles</code> 檔案的內容。
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
        如果有可用的 <acronym class="acronym">JIT</acronym> 編譯器擴充功能（請參閱<a class="xref" href="../../server-administration/jit/README.md">第 30 章</a>），並且 <a class="xref" href="../../server-administration/runtime-config/runtime-config-query.md#GUC-JIT">jit</a> 組態參數設定為 <code class="literal">on</code>，就回傳 true。
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
        回傳非同步通知佇列目前被等待處理之通知所占用的比例（0–1），以佇列最大容量為基準。詳情請參閱 <a class="xref" href="../../reference/sql-commands/sql-listen.md"><span class="refentrytitle">LISTEN</span></a> 與 <a class="xref" href="../../reference/sql-commands/sql-notify.md"><span class="refentrytitle">NOTIFY</span></a>。
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
        執行 <code class="literal">SERIALIZABLE</code> 交易的工作階段，會阻擋 <code class="literal">SERIALIZABLE READ ONLY DEFERRABLE</code> 交易取得快照，直到後者判定可以安全地避免取得任何述詞鎖為止。關於可序列化與可延後交易的更多資訊，請參閱<a class="xref" href="../mvcc/transaction-iso.md#XACT-SERIALIZABLE">第 13.2.3 節</a>。
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
        回傳使用者在被指派資料庫角色之前，於認證過程中所提出的認證方法與身分（如果有的話）。其表示形式為 <code class="literal">auth_method:identity</code>；如果使用者未經認證（例如使用了 <a class="link" href="../../server-administration/client-authentication/auth-trust.md">Trust 認證</a>），則為 <code class="literal">NULL</code>。
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

`session_user` 通常是發起目前資料庫連線的使用者；但超級使用者可以使用 [SET SESSION AUTHORIZATION](../../reference/sql-commands/sql-set-session-authorization.md) 變更這項設定。`current_user` 是用於權限檢查的使用者識別。通常它與工作階段使用者相同，但可以使用 [SET ROLE](../../reference/sql-commands/sql-set-role.md) 加以變更。在執行具有 `SECURITY DEFINER` 屬性的函式期間，它也會改變。以 Unix 的說法，工作階段使用者是「真實使用者」（real user），而目前使用者是「有效使用者」（effective user）。`current_role` 與 `user` 是 `current_user` 的同義詞。（SQL 標準區分了 `current_role` 與 `current_user`，但 PostgreSQL 並不區分，因為它將使用者與角色統一為單一種類的實體。）

<a id="FUNCTIONS-INFO-ACCESS"></a>

### 9.27.2. 存取權限查詢函式 [#](#FUNCTIONS-INFO-ACCESS)

<a id="id-1.5.8.33.4.2"></a>

[表 9.72](functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE) 列出了能以程式方式查詢物件存取權限的函式。（關於權限的更多資訊，請參閱[第 5.8 節](../ddl/ddl-priv.md)。）在這些函式中，要查詢其權限的使用者可以用名稱或 OID（`pg_authid`.`oid`）指定；如果名稱指定為 `public`，則會檢查 PUBLIC 虛擬角色的權限。此外，*`user`* 引數也可以完全省略，此時會假定為 `current_user`。要查詢的物件同樣可以用名稱或 OID 指定。以名稱指定時，若有需要可以包含綱要名稱。所要查詢的存取權限以文字字串指定，其值必須是該物件型別適用的權限關鍵字之一（例如 `SELECT`）。也可以選擇在權限類型後面加上 `WITH GRANT OPTION`，以測試該權限是否帶有授權選項（grant option）。此外，也可以列出以逗號分隔的多個權限類型，此時只要擁有所列權限中的任何一個，結果就為 true。（權限字串不區分大小寫，並且權限名稱之間可以有多餘的空白，但權限名稱內部不可以。）以下是一些範例：

```

SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

<a id="FUNCTIONS-INFO-ACCESS-TABLE"></a>

**表 9.72. 存取權限查詢函式**

<table border="1" class="table" summary="Access Privilege Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.1.1.1.1"></a>
<code class="function">has_any_column_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表的任一欄位擁有權限？只要對整個資料表擁有該權限，或者至少有一個欄位被授予了該權限的欄位層級授權，就會成立。允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code> 與 <code class="literal">REFERENCES</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.2.1.1.1"></a> <code class="function">has_column_privilege</code> ( [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> 或 <code class="type">oid</code>, </span>] <em class="parameter"><code>table</code></em> <code class="type">text</code> 或 <code class="type">oid</code>, <em class="parameter"><code>column</code></em> <code class="type">text</code> 或 <code class="type">smallint</code>, <em class="parameter"><code>privilege</code></em> <code class="type">text</code> ) → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對指定的資料表欄位擁有權限？只要對整個資料表擁有該權限，或者該欄位被授予了該權限的欄位層級授權，就會成立。欄位可以用名稱或屬性編號（<code class="structname">pg_attribute</code>.<code class="structfield">attnum</code>）指定。允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code> 與 <code class="literal">REFERENCES</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.3.1.1.1"></a>
<code class="function">has_database_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>database</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料庫擁有權限？允許的權限類型為 <code class="literal">CREATE</code>、<code class="literal">CONNECT</code>、<code class="literal">TEMPORARY</code> 與 <code class="literal">TEMP</code>（等同於 <code class="literal">TEMPORARY</code>）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.4.1.1.1"></a>
<code class="function">has_foreign_data_wrapper_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>fdw</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對外部資料包裝器（foreign-data wrapper）擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.5.1.1.1"></a>
<code class="function">has_function_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>function</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對函式擁有權限？唯一允許的權限類型為 <code class="literal">EXECUTE</code>。
       </p>
<p>
        以名稱而非 OID 指定函式時，允許的輸入與 <code class="type">regprocedure</code> 資料型別相同（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）。範例如下：
</p><pre class="programlisting">
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.6.1.1.1"></a>
<code class="function">has_language_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>language</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對程序語言擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.7.1.1.1"></a>
<code class="function">has_largeobject_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>largeobject</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對大型物件擁有權限？允許的權限類型為 <code class="literal">SELECT</code> 與 <code class="literal">UPDATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.8.1.1.1"></a>
<code class="function">has_parameter_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>parameter</code></em> <code class="type">text</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對組態參數擁有權限？參數名稱不區分大小寫。允許的權限類型為 <code class="literal">SET</code> 與 <code class="literal">ALTER SYSTEM</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.9.1.1.1"></a>
<code class="function">has_schema_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>schema</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對綱要擁有權限？允許的權限類型為 <code class="literal">CREATE</code> 與 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.10.1.1.1"></a>
<code class="function">has_sequence_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>sequence</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對序列擁有權限？允許的權限類型為 <code class="literal">USAGE</code>、<code class="literal">SELECT</code> 與 <code class="literal">UPDATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.11.1.1.1"></a>
<code class="function">has_server_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>server</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對外部伺服器擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.12.1.1.1"></a>
<code class="function">has_table_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表擁有權限？允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code>、<code class="literal">DELETE</code>、<code class="literal">TRUNCATE</code>、<code class="literal">REFERENCES</code>、<code class="literal">TRIGGER</code> 與 <code class="literal">MAINTAIN</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.13.1.1.1"></a>
<code class="function">has_tablespace_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>tablespace</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表空間擁有權限？唯一允許的權限類型為 <code class="literal">CREATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.14.1.1.1"></a>
<code class="function">has_type_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>type</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料型別擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。以名稱而非 OID 指定型別時，允許的輸入與 <code class="type">regtype</code> 資料型別相同（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.15.1.1.1"></a>
<code class="function">pg_has_role</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>role</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對角色擁有權限？允許的權限類型為 <code class="literal">MEMBER</code>、<code class="literal">USAGE</code> 與 <code class="literal">SET</code>。<code class="literal">MEMBER</code> 表示直接或間接身為該角色的成員，而不考慮可能被賦予了哪些具體權限。<code class="literal">USAGE</code> 表示是否不必執行 <code class="command">SET ROLE</code> 就能立即使用該角色的權限，而 <code class="literal">SET</code> 表示是否可以使用 <code class="literal">SET ROLE</code> 指令切換為該角色。可以在上述任何一種權限類型後面加上 <code class="literal">WITH ADMIN OPTION</code> 或 <code class="literal">WITH GRANT
        OPTION</code>，以測試是否持有 <code class="literal">ADMIN</code> 權限（這六種寫法測試的都是同一件事）。這個函式不允許將 <em class="parameter"><code>user</code></em> 設為 <code class="literal">public</code> 的特殊情況，因為 PUBLIC 虛擬角色永遠不可能是實際角色的成員。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.16.1.1.1"></a>
<code class="function">row_security_active</code> (
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        在目前使用者與目前環境的情境下，指定的資料表是否啟用了資料列層級安全性？
       </p></td></tr></tbody></table>

<br>

[表 9.73](functions-info.md#FUNCTIONS-ACLITEM-OP-TABLE) 列出了 `aclitem` 型別可用的運算子，該型別是存取權限在系統目錄中的表示方式。關於如何解讀存取權限值，請參閱[第 5.8 節](../ddl/ddl-priv.md)。

<a id="FUNCTIONS-ACLITEM-OP-TABLE"></a>

**表 9.73. `aclitem` 運算子**

<table border="1" class="table" summary="aclitem Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         運算子
        </p>
<p>
         說明
        </p>
<p>
         範例
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.1.1.1.1"></a>
<code class="type">aclitem</code> <code class="literal">=</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         兩個 <code class="type">aclitem</code> 是否相等？（請注意，<code class="type">aclitem</code> 型別沒有一般的一整組比較運算子，只有相等比較。因此，<code class="type">aclitem</code> 陣列也只能比較是否相等。）
        </p>
<p>
<code class="literal">'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::aclitem</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.2.1.1.1"></a>
<code class="type">aclitem[]</code> <code class="literal">@&gt;</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         陣列是否包含指定的權限？（如果陣列中有一個項目，其被授權者與授權者都與該 <code class="type">aclitem</code> 相符，並且至少擁有所指定的權限集合，結果即為 true。）
        </p>
<p>
<code class="literal">'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @&gt; 'calvin=r*/hobbes'::aclitem</code>
         → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

[表 9.74](functions-info.md#FUNCTIONS-ACLITEM-FN-TABLE) 列出了一些用於管理 `aclitem` 型別的其他函式。

<a id="FUNCTIONS-ACLITEM-FN-TABLE"></a>

**表 9.74. `aclitem` 函式**

<table border="1" class="table" summary="aclitem Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.1.1.1.1"></a>
<code class="function">acldefault</code> (
          <em class="parameter"><code>type</code></em> <code class="type">"char"</code>,
          <em class="parameter"><code>ownerId</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        建構一個 <code class="type">aclitem</code> 陣列，內容為某個型別為 <em class="parameter"><code>type</code></em> 之物件的預設存取權限，該物件屬於 OID 為 <em class="parameter"><code>ownerId</code></em> 的角色。這代表了當物件的 <acronym class="acronym">ACL</acronym> 項目為 NULL 時所假定的存取權限。（預設存取權限說明於<a class="xref" href="../ddl/ddl-priv.md">第 5.8 節</a>。）<em class="parameter"><code>type</code></em> 參數必須是下列之一：'c' 代表 <code class="literal">COLUMN</code>，'r' 代表 <code class="literal">TABLE</code> 及類似資料表的物件，'s' 代表 <code class="literal">SEQUENCE</code>，'d' 代表 <code class="literal">DATABASE</code>，'f' 代表 <code class="literal">FUNCTION</code> 或 <code class="literal">PROCEDURE</code>，'l' 代表 <code class="literal">LANGUAGE</code>，'L' 代表 <code class="literal">LARGE OBJECT</code>，'n' 代表 <code class="literal">SCHEMA</code>，'p' 代表 <code class="literal">PARAMETER</code>，'t' 代表 <code class="literal">TABLESPACE</code>，'F' 代表 <code class="literal">FOREIGN DATA WRAPPER</code>，'S' 代表 <code class="literal">FOREIGN SERVER</code>，或 'T' 代表 <code class="literal">TYPE</code> 或 <code class="literal">DOMAIN</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.2.1.1.1"></a>
<code class="function">aclexplode</code> ( <code class="type">aclitem[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>privilege_type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
       </p>
<p>
        將 <code class="type">aclitem</code> 陣列以一組資料列的形式回傳。如果被授權者是虛擬角色 PUBLIC，則在 <em class="parameter"><code>grantee</code></em> 欄位中以零表示。每一項授予的權限都以 <code class="literal">SELECT</code>、<code class="literal">INSERT</code> 等表示（完整清單請參閱<a class="xref" href="../ddl/ddl-priv.md#PRIVILEGE-ABBREVS-TABLE">表 5.1</a>）。請注意，每一項權限都會拆成獨立的一筆資料列，因此 <em class="parameter"><code>privilege_type</code></em> 欄位中只會出現一個關鍵字。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.3.1.1.1"></a>
<code class="function">makeaclitem</code> (
          <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privileges</code></em> <code class="type">text</code>,
          <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">aclitem</code>
</p>
<p>
        以給定的屬性建構一個 <code class="type">aclitem</code>。<em class="parameter"><code>privileges</code></em> 是以逗號分隔的權限名稱清單，例如 <code class="literal">SELECT</code>、<code class="literal">INSERT</code> 等，這些權限都會設定在結果中。（權限字串不區分大小寫，並且權限名稱之間可以有多餘的空白，但權限名稱內部不可以。）
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-SCHEMA"></a>

### 9.27.3. 綱要可見性查詢函式 [#](#FUNCTIONS-INFO-SCHEMA)

[表 9.75](functions-info.md#FUNCTIONS-INFO-SCHEMA-TABLE) 列出了用來判斷某個物件在目前的綱要搜尋路徑中是否*可見*的函式。舉例來說，如果一個資料表所屬的綱要位於搜尋路徑中，並且搜尋路徑中較前面的位置沒有同名的資料表，就稱該資料表是可見的。這等同於說，該資料表可以只用名稱來引用，而不需明確的綱要限定。因此，要列出所有可見資料表的名稱：

```

SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

對於函式與運算子而言，如果搜尋路徑中較前面的位置沒有名稱*與引數資料型別*都相同的物件，就稱搜尋路徑中的該物件是可見的。對於運算子類別與運算子家族，則會同時考慮名稱與相關聯的索引存取方法。

<a id="id-1.5.8.33.5.3"></a><a id="FUNCTIONS-INFO-SCHEMA-TABLE"></a>

**表 9.75. 綱要可見性查詢函式**

<table border="1" class="table" summary="Schema Visibility Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.1.1.1.1"></a>
<code class="function">pg_collation_is_visible</code> ( <em class="parameter"><code>collation</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        定序在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.2.1.1.1"></a>
<code class="function">pg_conversion_is_visible</code> ( <em class="parameter"><code>conversion</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        編碼轉換（conversion）在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.3.1.1.1"></a>
<code class="function">pg_function_is_visible</code> ( <em class="parameter"><code>function</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        函式在搜尋路徑中是否可見？（這也適用於程序與彙總函式。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.4.1.1.1"></a>
<code class="function">pg_opclass_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子類別在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.5.1.1.1"></a>
<code class="function">pg_operator_is_visible</code> ( <em class="parameter"><code>operator</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.6.1.1.1"></a>
<code class="function">pg_opfamily_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子家族在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.7.1.1.1"></a>
<code class="function">pg_statistics_obj_is_visible</code> ( <em class="parameter"><code>stat</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        統計資訊物件在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.8.1.1.1"></a>
<code class="function">pg_table_is_visible</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        資料表在搜尋路徑中是否可見？（這適用於所有種類的關聯，包括檢視表、具體化檢視表、索引、序列與外部資料表。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.9.1.1.1"></a>
<code class="function">pg_ts_config_is_visible</code> ( <em class="parameter"><code>config</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索設定在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.10.1.1.1"></a>
<code class="function">pg_ts_dict_is_visible</code> ( <em class="parameter"><code>dict</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索字典在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.11.1.1.1"></a>
<code class="function">pg_ts_parser_is_visible</code> ( <em class="parameter"><code>parser</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索剖析器在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.12.1.1.1"></a>
<code class="function">pg_ts_template_is_visible</code> ( <em class="parameter"><code>template</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索範本在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.13.1.1.1"></a>
<code class="function">pg_type_is_visible</code> ( <em class="parameter"><code>type</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        型別（或值域）在搜尋路徑中是否可見？
       </p></td></tr></tbody></table>

<br>

這些函式全都需要以物件 OID 來識別要檢查的物件。如果你想以名稱來測試物件，使用 OID 別名型別（`regclass`、`regtype`、`regprocedure`、`regoperator`、`regconfig` 或 `regdictionary`）會很方便，例如：

```

SELECT pg_type_is_visible('myschema.widget'::regtype);
```

請注意，以這種方式測試未經綱要限定的型別名稱並沒有太大意義——如果這個名稱能夠被辨識，它就必定是可見的。

<a id="FUNCTIONS-INFO-CATALOG"></a>

### 9.27.4. 系統目錄資訊函式 [#](#FUNCTIONS-INFO-CATALOG)

[表 9.76](functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE) 列出了從系統目錄擷取資訊的函式。

<a id="FUNCTIONS-INFO-CATALOG-TABLE"></a>

**表 9.76. 系統目錄資訊函式**

<table border="1" class="table" summary="System Catalog Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry" id="FORMAT-TYPE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.1.1.1.1"></a>
<code class="function">format_type</code> ( <em class="parameter"><code>type</code></em> <code class="type">oid</code>, <em class="parameter"><code>typemod</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以型別 OID 以及可能的型別修飾詞所識別之資料型別的 SQL 名稱。如果不知道具體的修飾詞，請為型別修飾詞傳入 NULL。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.2.1.1.1"></a>
<code class="function">pg_basetype</code> ( <code class="type">regtype</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        回傳以型別 OID 所識別之值域的基礎型別 OID。如果引數是非值域型別的 OID，則原樣回傳該引數。如果引數不是有效的型別 OID，則回傳 NULL。如果存在一連串的值域相依關係，它會遞迴下去，直到找到基礎型別為止。
       </p>
<p>
        假設已執行 <code class="literal">CREATE DOMAIN mytext AS text</code>：
       </p>
<p>
<code class="literal">pg_basetype('mytext'::regtype)</code>
        → <code class="returnvalue">text</code>
</p></td></tr><tr><td class="func_table_entry" id="PG-CHAR-TO-ENCODING"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.3.1.1.1"></a>
<code class="function">pg_char_to_encoding</code> ( <em class="parameter"><code>encoding</code></em> <code class="type">name</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        將所提供的編碼名稱轉換為整數，該整數即為某些系統目錄資料表中所使用的內部識別碼。如果提供了未知的編碼名稱，則回傳 <code class="literal">-1</code>。
       </p></td></tr><tr><td class="func_table_entry" id="PG-ENCODING-TO-CHAR"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.4.1.1.1"></a>
<code class="function">pg_encoding_to_char</code> ( <em class="parameter"><code>encoding</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">name</code>
</p>
<p>
        將某些系統目錄資料表中作為編碼內部識別碼的整數，轉換為人類可讀的字串。如果提供了無效的編碼編號，則回傳空字串。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_catalog_foreign_keys</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>fktable</code></em> <code class="type">regclass</code>,
          <em class="parameter"><code>fkcols</code></em> <code class="type">text[]</code>,
          <em class="parameter"><code>pktable</code></em> <code class="type">regclass</code>,
          <em class="parameter"><code>pkcols</code></em> <code class="type">text[]</code>,
          <em class="parameter"><code>is_array</code></em> <code class="type">boolean</code>,
          <em class="parameter"><code>is_opt</code></em> <code class="type">boolean</code> )
       </p>
<p>
        回傳一組紀錄，描述 <span class="productname">PostgreSQL</span> 系統目錄內部存在的外部鍵關係。<em class="parameter"><code>fktable</code></em> 欄位包含參照端系統目錄的名稱，<em class="parameter"><code>fkcols</code></em> 欄位包含參照端欄位的名稱。同樣地，<em class="parameter"><code>pktable</code></em> 欄位包含被參照之系統目錄的名稱，<em class="parameter"><code>pkcols</code></em> 欄位包含被參照之欄位的名稱。如果 <em class="parameter"><code>is_array</code></em> 為 true，則最後一個參照端欄位是陣列，其每個元素都應該與被參照系統目錄中的某個項目相符。如果 <em class="parameter"><code>is_opt</code></em> 為 true，則參照端欄位允許包含零，而不是有效的參照。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.6.1.1.1"></a>
<code class="function">pg_get_constraintdef</code> ( <em class="parameter"><code>constraint</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建約束條件的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.7.1.1.1"></a>
<code class="function">pg_get_expr</code> ( <em class="parameter"><code>expr</code></em> <code class="type">pg_node_tree</code>, <em class="parameter"><code>relation</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        反編譯儲存在系統目錄中之運算式的內部形式，例如欄位的預設值。如果運算式可能包含 Var，請以第二個參數指定它們所參照之關聯的 OID；如果預期不會有 Var，傳入零即可。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.8.1.1.1"></a>
<code class="function">pg_get_functiondef</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建函式或程序的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）結果是一個完整的 <code class="command">CREATE OR REPLACE FUNCTION</code> 或 <code class="command">CREATE OR REPLACE PROCEDURE</code> 陳述句。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.9.1.1.1"></a>
<code class="function">pg_get_function_arguments</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建函式或程序的引數清單，其形式與在 <code class="command">CREATE FUNCTION</code> 中所需出現的形式相同（包含預設值）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.10.1.1.1"></a>
<code class="function">pg_get_function_identity_arguments</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建用來識別函式或程序所需的引數清單，其形式與在 <code class="command">ALTER FUNCTION</code> 等指令中所需出現的形式相同。這種形式會省略預設值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.11.1.1.1"></a>
<code class="function">pg_get_function_result</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建函式的 <code class="literal">RETURNS</code> 子句，其形式與在 <code class="command">CREATE
        FUNCTION</code> 中所需出現的形式相同。對於程序則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.12.1.1.1"></a>
<code class="function">pg_get_indexdef</code> ( <em class="parameter"><code>index</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>column</code></em> <code class="type">integer</code>, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建索引的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）如果有提供 <em class="parameter"><code>column</code></em> 且其值不為零，則只會重建該欄位的定義。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.13.1.1.1"></a>
<code class="function">pg_get_keywords</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>word</code></em> <code class="type">text</code>,
        <em class="parameter"><code>catcode</code></em> <code class="type">"char"</code>,
        <em class="parameter"><code>barelabel</code></em> <code class="type">boolean</code>,
        <em class="parameter"><code>catdesc</code></em> <code class="type">text</code>,
        <em class="parameter"><code>baredesc</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳一組紀錄，描述伺服器所認得的 SQL 關鍵字。<em class="parameter"><code>word</code></em> 欄位包含關鍵字。<em class="parameter"><code>catcode</code></em> 欄位包含類別代碼：<code class="literal">U</code> 表示非保留關鍵字，<code class="literal">C</code> 表示可以作為欄位名稱的關鍵字，<code class="literal">T</code> 表示可以作為型別或函式名稱的關鍵字，<code class="literal">R</code> 則表示完全保留的關鍵字。<em class="parameter"><code>barelabel</code></em> 欄位的值為 <code class="literal">true</code> 表示該關鍵字可以在 <code class="command">SELECT</code> 列表中作為<span class="quote">「<span class="quote">單獨</span>」</span>（bare）的欄位標籤使用，為 <code class="literal">false</code> 則表示只能在 <code class="literal">AS</code> 之後使用。<em class="parameter"><code>catdesc</code></em> 欄位包含一個描述關鍵字類別的字串（可能經過在地化）。<em class="parameter"><code>baredesc</code></em> 欄位包含一個描述關鍵字欄位標籤狀態的字串（可能經過在地化）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.14.1.1.1"></a>
<code class="function">pg_get_partition_constraintdef</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建分割區約束條件的定義。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.15.1.1.1"></a>
<code class="function">pg_get_partkeydef</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建已分割資料表之分割鍵的定義，其形式與寫在 <code class="literal">PARTITION
        BY</code> 子句中的形式相同，也就是 <code class="command">CREATE TABLE</code> 中的該子句。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.16.1.1.1"></a>
<code class="function">pg_get_ruledef</code> ( <em class="parameter"><code>rule</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建規則的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.17.1.1.1"></a>
<code class="function">pg_get_serial_sequence</code> ( <em class="parameter"><code>table</code></em> <code class="type">text</code>, <em class="parameter"><code>column</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳與某個欄位相關聯之序列的名稱；如果沒有序列與該欄位相關聯，則回傳 NULL。如果該欄位是識別欄位（identity column），相關聯的序列就是在內部為該欄位建立的序列。對於使用 serial 型別之一（<code class="type">serial</code>、<code class="type">smallserial</code>、<code class="type">bigserial</code>）建立的欄位，則是為該 serial 欄位定義所建立的序列。在後者的情況下，可以使用 <code class="command">ALTER SEQUENCE OWNED BY</code> 修改或移除這個關聯。（這個函式或許應該命名為 <code class="function">pg_get_owned_sequence</code>；它目前的名稱反映了它在歷史上一直用於 serial 型別欄位這個事實。）第一個參數是資料表名稱，可選擇性地加上綱要；第二個參數是欄位名稱。由於第一個參數可能同時包含綱要名稱與資料表名稱，它會依照一般的 SQL 規則進行剖析，也就是預設會轉換為小寫。第二個參數只是欄位名稱，會照字面處理，因此會保留其大小寫。結果的格式適合傳給序列函式使用（請參閱<a class="xref" href="functions-sequence.md">第 9.17 節</a>）。
       </p>
<p>
        典型的用法是讀取識別欄位或 serial 欄位之序列的目前值，例如：
</p><pre class="programlisting">
SELECT currval(pg_get_serial_sequence('sometable', 'id'));
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.18.1.1.1"></a>
<code class="function">pg_get_statisticsobjdef</code> ( <em class="parameter"><code>statobj</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建延伸統計資訊物件的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.19.1.1.1"></a>
<code class="function">pg_get_triggerdef</code> ( <em class="parameter"><code>trigger</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建觸發程序的建立指令。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.20.1.1.1"></a>
<code class="function">pg_get_userbyid</code> ( <em class="parameter"><code>role</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">name</code>
</p>
<p>
        以角色的 OID 回傳該角色的名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.21.1.1.1"></a>
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建檢視表或具體化檢視表底層的 <code class="command">SELECT</code> 指令。（這是反編譯後重建的結果，而非該指令的原始文字。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">oid</code>, <em class="parameter"><code>wrap_column</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建檢視表或具體化檢視表底層的 <code class="command">SELECT</code> 指令。（這是反編譯後重建的結果，而非該指令的原始文字。）在這個形式的函式中，一律會啟用美化輸出，並且會將較長的行換行，盡量使其短於指定的欄數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        重建檢視表或具體化檢視表底層的 <code class="command">SELECT</code> 指令，但是以檢視表的文字名稱而非其 OID 為依據。（這種用法已棄用；請改用 OID 的版本。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.24.1.1.1"></a>
<code class="function">pg_index_column_has_property</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>column</code></em> <code class="type">integer</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試索引欄位是否具有指定名稱的屬性。常見的索引欄位屬性列於<a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-COLUMN-PROPS">表 9.77</a>。（請注意，擴充的存取方法可以為其索引定義額外的屬性名稱。）如果屬性名稱未知或不適用於該特定物件，或者 OID 或欄位編號無法識別出有效的物件，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.25.1.1.1"></a>
<code class="function">pg_index_has_property</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試索引是否具有指定名稱的屬性。常見的索引屬性列於<a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-PROPS">表 9.78</a>。（請注意，擴充的存取方法可以為其索引定義額外的屬性名稱。）如果屬性名稱未知或不適用於該特定物件，或者 OID 無法識別出有效的物件，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.26.1.1.1"></a>
<code class="function">pg_indexam_has_property</code> ( <em class="parameter"><code>am</code></em> <code class="type">oid</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試索引存取方法是否具有指定名稱的屬性。存取方法的屬性列於<a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEXAM-PROPS">表 9.79</a>。如果屬性名稱未知或不適用於該特定物件，或者 OID 無法識別出有效的物件，則回傳 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.27.1.1.1"></a>
<code class="function">pg_options_to_table</code> ( <em class="parameter"><code>options_array</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>option_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>option_value</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳由 <code class="structname">pg_class</code>.<code class="structfield">reloptions</code> 或 <code class="structname">pg_attribute</code>.<code class="structfield">attoptions</code> 中的值所代表的儲存選項集合。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.28.1.1.1"></a>
<code class="function">pg_settings_get_flags</code> ( <em class="parameter"><code>guc</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        回傳與給定 GUC 相關聯之旗標所組成的陣列；如果該 GUC 不存在，則回傳 <code class="literal">NULL</code>。如果該 GUC 存在但沒有要顯示的旗標，結果為空陣列。只有<a class="xref" href="functions-info.md#FUNCTIONS-PG-SETTINGS-FLAGS">表 9.80</a> 所列最有用的旗標才會被顯示出來。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.29.1.1.1"></a>
<code class="function">pg_tablespace_databases</code> ( <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">setof oid</code>
</p>
<p>
        回傳在指定資料表空間中存有物件之資料庫的 OID 集合。如果這個函式回傳了任何資料列，就表示該資料表空間不是空的，因此無法刪除。若要找出占用該資料表空間的具體物件，你需要連線到 <code class="function">pg_tablespace_databases</code> 所識別出的資料庫，並查詢它們的 <code class="structname">pg_class</code> 系統目錄。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.30.1.1.1"></a>
<code class="function">pg_tablespace_location</code> ( <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳這個資料表空間所在的檔案系統路徑。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.31.1.1.1"></a>
<code class="function">pg_typeof</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        回傳傳入值之資料型別的 OID。這有助於疑難排解或動態建構 SQL 查詢。這個函式宣告為回傳 <code class="type">regtype</code>，這是一種 OID 別名型別（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；這表示在進行比較時它與 OID 相同，但顯示時會呈現為型別名稱。
       </p>
<p>
<code class="literal">pg_typeof(33)</code>
        → <code class="returnvalue">integer</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.32.1.1.1"></a>
<code class="function">COLLATION FOR</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳傳入值之定序的名稱。必要時，該值會加上引號並加上綱要限定。如果引數運算式沒有推導出任何定序，則回傳 <code class="literal">NULL</code>。如果引數不是可定序的資料型別，則會引發錯誤。
       </p>
<p>
<code class="literal">collation for ('foo'::text)</code>
        → <code class="returnvalue">"default"</code>
</p>
<p>
<code class="literal">collation for ('foo' COLLATE "de_DE")</code>
        → <code class="returnvalue">"de_DE"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.33.1.1.1"></a>
<code class="function">to_regclass</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regclass</code>
</p>
<p>
        將文字形式的關聯名稱轉換為其 OID。將字串轉型為 <code class="type">regclass</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.34.1.1.1"></a>
<code class="function">to_regcollation</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regcollation</code>
</p>
<p>
        將文字形式的定序名稱轉換為其 OID。將字串轉型為 <code class="type">regcollation</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.35.1.1.1"></a>
<code class="function">to_regnamespace</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regnamespace</code>
</p>
<p>
        將文字形式的綱要名稱轉換為其 OID。將字串轉型為 <code class="type">regnamespace</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.36.1.1.1"></a>
<code class="function">to_regoper</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regoper</code>
</p>
<p>
        將文字形式的運算子名稱轉換為其 OID。將字串轉型為 <code class="type">regoper</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱或該名稱有歧義，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.37.1.1.1"></a>
<code class="function">to_regoperator</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regoperator</code>
</p>
<p>
        將文字形式的運算子名稱（含參數型別）轉換為其 OID。將字串轉型為 <code class="type">regoperator</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.38.1.1.1"></a>
<code class="function">to_regproc</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regproc</code>
</p>
<p>
        將文字形式的函式或程序名稱轉換為其 OID。將字串轉型為 <code class="type">regproc</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱或該名稱有歧義，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.39.1.1.1"></a>
<code class="function">to_regprocedure</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regprocedure</code>
</p>
<p>
        將文字形式的函式或程序名稱（含引數型別）轉換為其 OID。將字串轉型為 <code class="type">regprocedure</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.40.1.1.1"></a>
<code class="function">to_regrole</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regrole</code>
</p>
<p>
        將文字形式的角色名稱轉換為其 OID。將字串轉型為 <code class="type">regrole</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>）；不過，如果找不到該名稱，這個函式會回傳 <code class="literal">NULL</code>，而不是拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry" id="TO-REGTYPE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.41.1.1.1"></a>
<code class="function">to_regtype</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        剖析一段文字字串，從中擷取可能的型別名稱，並將該名稱轉換為型別 OID。字串中的語法錯誤會導致錯誤；但如果該字串是語法上有效的型別名稱，只是剛好在系統目錄中找不到，則結果為 <code class="literal">NULL</code>。將字串轉型為 <code class="type">regtype</code> 型別也可以得到類似的結果（請參閱<a class="xref" href="../datatype/datatype-oid.md">第 8.19 節</a>），差別在於後者在找不到名稱時會拋出錯誤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.42.1.1.1"></a>
<code class="function">to_regtypemod</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        剖析一段文字字串，從中擷取可能的型別名稱，並轉換其型別修飾詞（如果有的話）。字串中的語法錯誤會導致錯誤；但如果該字串是語法上有效的型別名稱，只是剛好在系統目錄中找不到，則結果為 <code class="literal">NULL</code>。如果沒有型別修飾詞，結果為 <code class="literal">-1</code>。
       </p>
<p>
<code class="function">to_regtypemod</code> 可以與 <a class="xref" href="functions-info.md#TO-REGTYPE">to_regtype</a> 搭配使用，為 <a class="xref" href="functions-info.md#FORMAT-TYPE">format_type</a> 產生適當的輸入，從而將代表型別名稱的字串正規化。
       </p>
<p>
<code class="literal">format_type(to_regtype('varchar(32)'), to_regtypemod('varchar(32)'))</code>
        → <code class="returnvalue">character varying(32)</code>
</p></td></tr></tbody></table>

<br>

大多數重建（反編譯）資料庫物件的函式都有一個選用的 *`pretty`* 旗標，若為 `true`，會使結果以「美化輸出」（pretty-printed）的形式呈現。美化輸出會省略不必要的括號，並加入空白以提高可讀性。美化輸出的格式較易於閱讀，但預設格式較有可能被未來版本的 PostgreSQL 以相同的方式解讀；因此請避免將美化輸出用於傾印（dump）用途。為 *`pretty`* 參數傳入 `false`，會得到與省略該參數相同的結果。

<a id="FUNCTIONS-INFO-INDEX-COLUMN-PROPS"></a>

**表 9.77. 索引欄位屬性**

<table border="1" class="table" summary="Index Column Properties"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">asc</code></td><td>在正向掃描時，該欄位是否以遞增順序排序？
      </td></tr><tr><td><code class="literal">desc</code></td><td>在正向掃描時，該欄位是否以遞減順序排序？
      </td></tr><tr><td><code class="literal">nulls_first</code></td><td>在正向掃描時，該欄位是否以 NULL 值在前的方式排序？
      </td></tr><tr><td><code class="literal">nulls_last</code></td><td>在正向掃描時，該欄位是否以 NULL 值在後的方式排序？
      </td></tr><tr><td><code class="literal">orderable</code></td><td>該欄位是否具有任何已定義的排序順序？
      </td></tr><tr><td><code class="literal">distance_orderable</code></td><td>該欄位是否可以依<span class="quote">「<span class="quote">距離</span>」</span>運算子依序掃描，例如 <code class="literal">ORDER BY col &lt;-&gt; constant</code>？
      </td></tr><tr><td><code class="literal">returnable</code></td><td>該欄位的值是否可以由僅索引掃描（index-only scan）回傳？
      </td></tr><tr><td><code class="literal">search_array</code></td><td>該欄位是否原生支援 <code class="literal">col = ANY(array)</code> 搜尋？
      </td></tr><tr><td><code class="literal">search_nulls</code></td><td>該欄位是否支援 <code class="literal">IS NULL</code> 與 <code class="literal">IS NOT NULL</code> 搜尋？
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-INFO-INDEX-PROPS"></a>

**表 9.78. 索引屬性**

<table border="1" class="table" summary="Index Properties"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">clusterable</code></td><td>該索引是否可以用於 <code class="literal">CLUSTER</code> 指令？
      </td></tr><tr><td><code class="literal">index_scan</code></td><td>該索引是否支援一般（非點陣圖）掃描？
      </td></tr><tr><td><code class="literal">bitmap_scan</code></td><td>該索引是否支援點陣圖掃描？
      </td></tr><tr><td><code class="literal">backward_scan</code></td><td>是否可以在掃描途中變更掃描方向（以便在不需要實體化的情況下，支援對游標執行 <code class="literal">FETCH BACKWARD</code>）？
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-INFO-INDEXAM-PROPS"></a>

**表 9.79. 索引存取方法屬性**

<table border="1" class="table" summary="Index Access Method Properties"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">can_order</code></td><td>該存取方法是否支援將 <code class="literal">ASC</code>、<code class="literal">DESC</code> 及相關的關鍵字用於 <code class="literal">CREATE INDEX</code> 中？
      </td></tr><tr><td><code class="literal">can_unique</code></td><td>該存取方法是否支援唯一索引？
      </td></tr><tr><td><code class="literal">can_multi_col</code></td><td>該存取方法是否支援多欄位索引？
      </td></tr><tr><td><code class="literal">can_exclude</code></td><td>該存取方法是否支援排除約束條件？
      </td></tr><tr><td><code class="literal">can_include</code></td><td>該存取方法是否支援將 <code class="literal">INCLUDE</code> 子句用於 <code class="literal">CREATE INDEX</code> 中？
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-SETTINGS-FLAGS"></a>

**表 9.80. GUC 旗標**

<table border="1" class="table" summary="GUC Flags"><colgroup><col/><col/></colgroup><thead><tr><th>旗標</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">EXPLAIN</code></td><td>帶有此旗標的參數會包含在 <code class="command">EXPLAIN (SETTINGS)</code> 指令的輸出中。
      </td></tr><tr><td><code class="literal">NO_SHOW_ALL</code></td><td>帶有此旗標的參數會被排除在 <code class="command">SHOW ALL</code> 指令的輸出之外。
      </td></tr><tr><td><code class="literal">NO_RESET</code></td><td>帶有此旗標的參數不支援 <code class="command">RESET</code> 指令。
      </td></tr><tr><td><code class="literal">NO_RESET_ALL</code></td><td>帶有此旗標的參數會被排除在 <code class="command">RESET ALL</code> 指令的作用範圍之外。
      </td></tr><tr><td><code class="literal">NOT_IN_SAMPLE</code></td><td>帶有此旗標的參數預設不會包含在 <code class="filename">postgresql.conf</code> 中。
      </td></tr><tr><td><code class="literal">RUNTIME_COMPUTED</code></td><td>帶有此旗標的參數是在執行時期計算得出的參數。
      </td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-OBJECT"></a>

### 9.27.5. 物件資訊與定址函式 [#](#FUNCTIONS-INFO-OBJECT)

[表 9.81](functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE) 列出了與資料庫物件識別及定址相關的函式。

<a id="FUNCTIONS-INFO-OBJECT-TABLE"></a>

**表 9.81. 物件資訊與定址函式**

<table border="1" class="table" summary="Object Information and Addressing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.1.1.1.1"></a>
<code class="function">pg_get_acl</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        回傳以系統目錄 OID、物件 OID 與子物件 ID 指定之資料庫物件的 <acronym class="acronym">ACL</acronym>。對於未定義的物件，這個函式會回傳 <code class="literal">NULL</code> 值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.2.1.1.1"></a>
<code class="function">pg_describe_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以系統目錄 OID、物件 OID 與子物件 ID（例如資料表中的欄位編號；指的是整個物件時，子物件 ID 為零）所識別之資料庫物件的文字描述。這個描述旨在供人閱讀，並且可能會依伺服器的設定而經過翻譯。這特別有助於確認 <code class="structname">pg_depend</code> 系統目錄中所參照之物件的身分。對於未定義的物件，這個函式會回傳 <code class="literal">NULL</code> 值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.3.1.1.1"></a>
<code class="function">pg_identify_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>schema</code></em> <code class="type">text</code>,
        <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>identity</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以系統目錄 OID、物件 OID 與子物件 ID 所指定之資料庫物件的資訊。這些資訊是供機器讀取的，永遠不會被翻譯。<em class="parameter"><code>type</code></em> 識別資料庫物件的類型；<em class="parameter"><code>schema</code></em> 是該物件所屬的綱要名稱，對於不屬於綱要的物件類型則為 <code class="literal">NULL</code>；<em class="parameter"><code>name</code></em> 是物件的名稱（必要時會加上引號），前提是該名稱（在適用時連同綱要名稱）足以唯一識別該物件，否則為 <code class="literal">NULL</code>；<em class="parameter"><code>identity</code></em> 是完整的物件識別，其精確格式取決於物件類型，且格式中的每個名稱都會視需要加上綱要限定與引號。未定義的物件會以 <code class="literal">NULL</code> 值識別。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.4.1.1.1"></a>
<code class="function">pg_identify_object_as_address</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>,
        <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以系統目錄 OID、物件 OID 與子物件 ID 所指定之資料庫物件的資訊。所回傳的資訊與目前的伺服器無關，也就是說，它可以用來識別另一台伺服器中同名的物件。<em class="parameter"><code>type</code></em> 識別資料庫物件的類型；<em class="parameter"><code>object_names</code></em> 與 <em class="parameter"><code>object_args</code></em> 是文字陣列，兩者共同構成對該物件的參照。這三個值可以傳給 <code class="function">pg_get_object_address</code>，以取得該物件的內部位址。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_object_address</code> ( <em class="parameter"><code>type</code></em> <code class="type">text</code>, <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>, <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以類型代碼、物件名稱與引數陣列所指定之資料庫物件的資訊。所回傳的值就是像 <code class="structname">pg_depend</code> 這類系統目錄中會使用的值；它們可以傳給其他系統函式，例如 <code class="function">pg_describe_object</code> 或 <code class="function">pg_identify_object</code>。<em class="parameter"><code>classid</code></em> 是包含該物件之系統目錄的 OID；<em class="parameter"><code>objid</code></em> 是物件本身的 OID，而 <em class="parameter"><code>objsubid</code></em> 是子物件 ID，若無則為零。這個函式是 <code class="function">pg_identify_object_as_address</code> 的反函式。未定義的物件會以 <code class="literal">NULL</code> 值識別。
       </p></td></tr></tbody></table>

<br>

`pg_get_acl` 可用於擷取並檢視與資料庫物件相關聯的權限，而不必去查看特定的系統目錄。例如，要擷取目前資料庫中所有物件上已授予的權限：

```

postgres=# SELECT
    (pg_identify_object(s.classid,s.objid,s.objsubid)).*,
    pg_catalog.pg_get_acl(s.classid,s.objid,s.objsubid) AS acl
FROM pg_catalog.pg_shdepend AS s
JOIN pg_catalog.pg_database AS d
    ON d.datname = current_database() AND
       d.oid = s.dbid
JOIN pg_catalog.pg_authid AS a
    ON a.oid = s.refobjid AND
       s.refclassid = 'pg_authid'::regclass
WHERE s.deptype = 'a';
-[ RECORD 1 ]-----------------------------------------
type     | table
schema   | public
name     | testtab
identity | public.testtab
acl      | {postgres=arwdDxtm/postgres,foo=r/postgres}
```

<a id="FUNCTIONS-INFO-COMMENT"></a>

### 9.27.6. 註解資訊函式 [#](#FUNCTIONS-INFO-COMMENT)

<a id="id-1.5.8.33.8.2"></a>

[表 9.82](functions-info.md#FUNCTIONS-INFO-COMMENT-TABLE) 所列的函式會擷取先前以 [COMMENT](../../reference/sql-commands/sql-comment.md) 指令儲存的註解。如果找不到符合指定參數的註解，則回傳 NULL 值。

<a id="FUNCTIONS-INFO-COMMENT-TABLE"></a>

**表 9.82. 註解資訊函式**

<table border="1" class="table" summary="Comment Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.1.1.1.1"></a>
<code class="function">col_description</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code>, <em class="parameter"><code>column</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳資料表欄位的註解，該欄位以其所屬資料表的 OID 與欄位編號指定。（<code class="function">obj_description</code> 無法用於資料表欄位，因為欄位沒有自己的 OID。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.2.1.1.1"></a>
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以 OID 與所在系統目錄名稱指定之資料庫物件的註解。例如，<code class="literal">obj_description(123456, 'pg_class')</code> 會擷取 OID 為 123456 之資料表的註解。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳僅以 OID 指定之資料庫物件的註解。這種用法<span class="emphasis"><em>已棄用</em></span>，因為無法保證 OID 在不同的系統目錄之間是唯一的；因此，可能會回傳錯誤的註解。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.4.1.1.1"></a>
<code class="function">shobj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以 OID 與所在系統目錄名稱指定之共享資料庫物件的註解。這與 <code class="function">obj_description</code> 相同，只不過它是用來擷取共享物件（也就是資料庫、角色與資料表空間）的註解。有些系統目錄對每個叢集中的所有資料庫而言是全域的，而其中物件的描述也同樣以全域方式儲存。
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-VALIDITY"></a>

### 9.27.7. 資料有效性檢查函式 [#](#FUNCTIONS-INFO-VALIDITY)

[表 9.83](functions-info.md#FUNCTIONS-INFO-VALIDITY-TABLE) 所列的函式有助於檢查擬輸入資料的有效性。

<a id="FUNCTIONS-INFO-VALIDITY-TABLE"></a>

**表 9.83. 資料有效性檢查函式**

<table border="1" class="table" summary="Data Validity Checking Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.1.1.1.1"></a>
<code class="function">pg_input_is_valid</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試給定的 <em class="parameter"><code>string</code></em> 對於指定的資料型別而言是否為有效的輸入，並回傳 true 或 false。
       </p>
<p>
        只有在該資料型別的輸入函式已經更新為將無效輸入以<span class="quote">「<span class="quote">軟性</span>」</span>錯誤回報時，這個函式才能如預期般運作。否則，無效的輸入會中止交易，就如同直接將字串轉型為該型別一樣。
        </p>
<p>
<code class="literal">pg_input_is_valid('42', 'integer')</code>
         → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">pg_input_is_valid('42000000000', 'integer')</code>
         → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">pg_input_is_valid('1234.567', 'numeric(7,4)')</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.2.1.1.1"></a>
<code class="function">pg_input_error_info</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>message</code></em> <code class="type">text</code>,
        <em class="parameter"><code>detail</code></em> <code class="type">text</code>,
        <em class="parameter"><code>hint</code></em> <code class="type">text</code>,
        <em class="parameter"><code>sql_error_code</code></em> <code class="type">text</code> )
       </p>
<p>
        測試給定的 <em class="parameter"><code>string</code></em> 對於指定的資料型別而言是否為有效的輸入；如果不是，則回傳原本會拋出之錯誤的詳細資訊。如果輸入有效，結果為 NULL。其輸入與 <code class="function">pg_input_is_valid</code> 相同。
       </p>
<p>
        只有在該資料型別的輸入函式已經更新為將無效輸入以<span class="quote">「<span class="quote">軟性</span>」</span>錯誤回報時，這個函式才能如預期般運作。否則，無效的輸入會中止交易，就如同直接將字串轉型為該型別一樣。
       </p>
<p>
<code class="literal">SELECT * FROM pg_input_error_info('42000000000', 'integer')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
                       message                        | detail | hint | sql_error_code
------------------------------------------------------+--------+------+----------------
 value "42000000000" is out of range for type integer |        |      | 22003
</pre><p>
</p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-SNAPSHOT"></a>

### 9.27.8. 交易 ID 與快照資訊函式 [#](#FUNCTIONS-INFO-SNAPSHOT)

[表 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT) 所列的函式以可匯出的形式提供伺服器的交易資訊。這些函式的主要用途是判斷在兩個快照之間有哪些交易已經提交。

<a id="FUNCTIONS-PG-SNAPSHOT"></a>

**表 9.84. 交易 ID 與快照資訊函式**

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
        回傳目前交易的 ID。如果目前交易還沒有 ID（因為它尚未執行任何資料庫更新），就會為它指派一個新的 ID；詳情請參閱<a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a>。如果是在子交易中執行，則會回傳最上層的交易 ID；詳情請參閱<a class="xref" href="../../internals/transactions/subxacts.md">第 67.3 節</a>。
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
        progress</code>；如果應用程式需要判斷某個交易 ID 是否屬於已預備的交易，就必須檢查 <a class="link" href="../../internals/views/view-pg-prepared-xacts.md"><code class="structname">pg_prepared_xacts</code></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.6.1.1.1"></a>
<code class="function">pg_current_snapshot</code> ()
        → <code class="returnvalue">pg_snapshot</code>
</p>
<p>
        回傳目前的<em class="firstterm">快照</em>，這是一種資料結構，顯示目前有哪些交易 ID 正在進行中。快照中只包含最上層的交易 ID，不會顯示子交易 ID；詳情請參閱<a class="xref" href="../../internals/transactions/subxacts.md">第 67.3 節</a>。
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
        依據這個快照，給定的交易 ID 是否<em class="firstterm">可見</em>（也就是說，它是否在快照取得之前就已經完成）？請注意，對於子交易 ID（subxid），這個函式不會給出正確的答案；詳情請參閱<a class="xref" href="../../internals/transactions/subxacts.md">第 67.3 節</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.11.1.1.1"></a>
<code class="function">pg_get_multixact_members</code> ( <em class="parameter"><code>multixid</code></em> <code class="type">xid</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>mode</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳指定 multixact ID 之每個成員的交易 ID 與鎖模式。鎖模式 <code class="literal">forupd</code>、<code class="literal">fornokeyupd</code>、<code class="literal">sh</code> 與 <code class="literal">keysh</code> 分別對應於資料列層級鎖 <code class="literal">FOR UPDATE</code>、<code class="literal">FOR NO KEY UPDATE</code>、<code class="literal">FOR SHARE</code> 與 <code class="literal">FOR KEY SHARE</code>，如<a class="xref" href="../mvcc/explicit-locking.md#LOCKING-ROWS">第 13.3.2 節</a>所述。另外還有兩種 multixact 專用的模式：<code class="literal">nokeyupd</code>，用於未修改鍵欄位的更新；以及 <code class="literal">upd</code>，用於會修改鍵欄位的更新或刪除。
       </p></td></tr></tbody></table>

<br>

內部的交易 ID 型別 `xid` 為 32 位元寬，每經過 40 億個交易就會迴繞（wrap around）。不過，[表 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT) 所列的函式，除了 `age`、`mxid_age` 與 `pg_get_multixact_members` 之外，都使用 64 位元的型別 `xid8`，它在安裝環境的整個生命週期內都不會迴繞，並且在需要時可以透過型別轉換轉為 `xid`；詳情請參閱[第 67.1 節](../../internals/transactions/transaction-id.md)。資料型別 `pg_snapshot` 儲存在某個特定時間點的交易 ID 可見性資訊。其組成部分說明於[表 9.85](functions-info.md#FUNCTIONS-PG-SNAPSHOT-PARTS)。`pg_snapshot` 的文字表示形式為 `xmin:xmax:xip_list`。例如 `10:20:10,14,15` 表示 `xmin=10, xmax=20, xip_list=10, 14, 15`。

<a id="FUNCTIONS-PG-SNAPSHOT-PARTS"></a>

**表 9.85. 快照組成部分**

<table border="1" class="table" summary="Snapshot Components"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">xmin</code></td><td>
         仍在進行中的最小交易 ID。所有小於 <code class="structfield">xmin</code> 的交易 ID，不是已提交且可見，就是已回滾且無效。
       </td></tr><tr><td><code class="structfield">xmax</code></td><td>
         比已完成之最大交易 ID 大一的值。所有大於或等於 <code class="structfield">xmax</code> 的交易 ID，在取得快照時都尚未完成，因此是不可見的。
       </td></tr><tr><td><code class="structfield">xip_list</code></td><td>
        取得快照時正在進行中的交易。若某個交易 ID 符合 <code class="literal">xmin &lt;= <em class="replaceable"><code>X</code></em> &lt; xmax</code> 且不在這個清單中，表示它在取得快照時已經完成，因此依其提交狀態，不是可見就是無效。這個清單不包含子交易的交易 ID（subxid）。
       </td></tr></tbody></table>

<br>

在 PostgreSQL 13 之前的版本中沒有 `xid8` 型別，因此提供了這些函式的變體，它們使用 `bigint` 來表示 64 位元的 XID，並相對應地使用另一個獨立的快照資料型別 `txid_snapshot`。這些較舊的函式名稱中帶有 `txid`。為了向下相容，它們仍然受到支援，但可能會在未來的版本中移除。請參閱[表 9.86](functions-info.md#FUNCTIONS-TXID-SNAPSHOT)。

<a id="FUNCTIONS-TXID-SNAPSHOT"></a>

**表 9.86. 已棄用的交易 ID 與快照資訊函式**

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

<a id="FUNCTIONS-INFO-COMMIT-TIMESTAMP"></a>

### 9.27.9. 已提交交易資訊函式 [#](#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

[表 9.87](functions-info.md#FUNCTIONS-COMMIT-TIMESTAMP) 所列的函式提供過去的交易是在何時提交的資訊。只有在啟用了 [track_commit_timestamp](../../server-administration/runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) 組態選項時，它們才會提供有用的資料，而且只適用於啟用該選項之後才提交的交易。提交時間戳記資訊會在 vacuum 期間例行性地移除。

<a id="FUNCTIONS-COMMIT-TIMESTAMP"></a>

**表 9.87. 已提交交易資訊函式**

<table border="1" class="table" summary="Committed Transaction Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.1.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳交易的提交時間戳記。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.2.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp_origin</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
         <em class="parameter"><code>roident</code></em> <code class="type">oid</code>)
       </p>
<p>
         回傳交易的提交時間戳記與複寫來源（replication origin）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.3.1.1.1"></a>
<code class="function">pg_last_committed_xact</code> ()
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>roident</code></em> <code class="type">oid</code> )
       </p>
<p>
        回傳最近一個已提交交易的交易 ID、提交時間戳記與複寫來源。
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-CONTROLDATA"></a>

### 9.27.10. 控制資料函式 [#](#FUNCTIONS-INFO-CONTROLDATA)

[表 9.88](functions-info.md#FUNCTIONS-CONTROLDATA) 所列的函式會輸出在 `initdb` 期間初始化的資訊，例如系統目錄版本。它們也會顯示關於預寫式日誌（write-ahead logging）與檢查點處理的資訊。這些資訊是整個叢集共通的，並非專屬於任何一個資料庫。這些函式所提供的資訊，大多與 [pg_controldata](../../reference/reference-server/app-pgcontroldata.md) 應用程式相同，且來源也相同。

<a id="FUNCTIONS-CONTROLDATA"></a>

**表 9.88. 控制資料函式**

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
        回傳目前檢查點狀態的資訊，如<a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-CHECKPOINT">表 9.89</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.2.1.1.1"></a>
<code class="function">pg_control_system</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳目前控制檔狀態的資訊，如<a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-SYSTEM">表 9.90</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.3.1.1.1"></a>
<code class="function">pg_control_init</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳叢集初始化狀態的資訊，如<a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-INIT">表 9.91</a> 所示。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.4.1.1.1"></a>
<code class="function">pg_control_recovery</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳復原狀態的資訊，如<a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-RECOVERY">表 9.92</a> 所示。
       </p></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-CHECKPOINT"></a>

**表 9.89. `pg_control_checkpoint` 輸出欄位**

<table border="1" class="table" summary="pg_control_checkpoint Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">checkpoint_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_wal_file</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">prev_timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">full_page_writes</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">next_xid</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">next_oid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">next_multixact_id</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">next_multi_offset</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_active_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">newest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">checkpoint_time</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-SYSTEM"></a>

**表 9.90. `pg_control_system` 輸出欄位**

<table border="1" class="table" summary="pg_control_system Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">pg_control_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">catalog_version_no</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">system_identifier</code></td><td><code class="type">bigint</code></td></tr><tr><td><code class="structfield">pg_control_last_modified</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-INIT"></a>

**表 9.91. `pg_control_init` 輸出欄位**

<table border="1" class="table" summary="pg_control_init Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">max_data_alignment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">database_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">blocks_per_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">wal_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">bytes_per_wal_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_identifier_length</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_index_columns</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_toast_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">large_object_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">float8_pass_by_value</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">data_page_checksum_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">default_char_signedness</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-RECOVERY"></a>

**表 9.92. `pg_control_recovery` 輸出欄位**

<table border="1" class="table" summary="pg_control_recovery Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>欄位名稱</th><th>資料型別</th></tr></thead><tbody><tr><td><code class="structfield">min_recovery_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">min_recovery_end_timeline</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">backup_start_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">backup_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">end_of_backup_record_required</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-VERSION"></a>

### 9.27.11. 版本資訊函式 [#](#FUNCTIONS-INFO-VERSION)

[表 9.93](functions-info.md#FUNCTIONS-VERSION) 所列的函式會輸出版本資訊。

<a id="FUNCTIONS-VERSION"></a>

**表 9.93. 版本資訊函式**

<table border="1" class="table" summary="Version Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.1.1.1.1"></a>
<code class="function">version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳描述 <span class="productname">PostgreSQL</span> 伺服器版本的字串。你也可以從 <a class="xref" href="../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION">server_version</a> 取得這項資訊；若需要機器可讀的版本，則可以使用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION-NUM">server_version_num</a>。軟體開發人員應該使用 <code class="varname">server_version_num</code>（自 8.2 版起提供）或 <a class="xref" href="../../client-interfaces/libpq/libpq-status.md#LIBPQ-PQSERVERVERSION"><code class="function">PQserverVersion</code></a>，而不是剖析文字形式的版本。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.2.1.1.1"></a>
<code class="function">unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳代表 <span class="productname">PostgreSQL</span> 所使用之 Unicode 版本的字串。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.3.1.1.1"></a>
<code class="function">icu_unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        如果伺服器建置時加入了 ICU 支援，則回傳代表 ICU 所使用之 Unicode 版本的字串；否則回傳 <code class="literal">NULL</code> </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-WAL-SUMMARY"></a>

### 9.27.12. WAL 摘要資訊函式 [#](#FUNCTIONS-INFO-WAL-SUMMARY)

[表 9.94](functions-info.md#FUNCTIONS-WAL-SUMMARY) 所列的函式會輸出 WAL 摘要的狀態資訊。請參閱 [summarize_wal](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SUMMARIZE-WAL)。

<a id="FUNCTIONS-WAL-SUMMARY"></a>

**表 9.94. WAL 摘要資訊函式**

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

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
