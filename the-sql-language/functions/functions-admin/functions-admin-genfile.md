# 9.28.9. 通用檔案存取函式

<a id="FUNCTIONS-ADMIN-GENFILE"></a>

## 9.28.9. 通用檔案存取函式 [#](#functions-admin-genfile) <a href="#functions-admin-genfile" id="functions-admin-genfile"></a>

[表 9.108](#functions-admin-genfile-table) 所列的函式提供對伺服器所在主機上檔案的原生存取。除非使用者是超級使用者或被授予 `pg_read_server_files` 角色，否則只能存取資料庫叢集目錄與 `log_directory` 之內的檔案。對於叢集目錄中的檔案，請使用相對路徑；對於日誌檔案，請使用與 `log_directory` 組態設定相符的路徑。

請注意，授予使用者對 `pg_read_file()` 或相關函式的 EXECUTE 權限，會讓他們能夠讀取伺服器上任何資料庫伺服器程序可讀取的檔案；這些函式會略過所有資料庫內的權限檢查。這表示，舉例來說，具有這種存取權的使用者能夠讀取存放認證資訊的 `pg_authid` 資料表內容，也能讀取資料庫中的任何資料表資料。因此，授予這些函式的存取權時應審慎考慮。

授予這些函式的權限時，請注意，資料表中顯示選用參數的項目，大多是實作為數個具有不同參數列表的實體函式。如果要使用這類函式，就必須個別對每個函式授予權限。psql 的 `\df` 指令可以用來檢查實際的函式簽章為何。

其中部分函式接受選用的 *`missing_ok`* 參數，用來指定檔案或目錄不存在時的行為。如果為 `true`，函式會視情況回傳 `NULL` 或空的結果集合。如果為 `false`，則會引發錯誤。（除了「找不到檔案」之外的失敗情況，在任何情況下都會以錯誤回報。）預設值為 `false`。

<a id="FUNCTIONS-ADMIN-GENFILE-TABLE"></a>

### 表 9.108. 通用檔案存取函式 [#](#functions-admin-genfile-table) <a href="#functions-admin-genfile-table" id="functions-admin-genfile-table"></a>

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

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
