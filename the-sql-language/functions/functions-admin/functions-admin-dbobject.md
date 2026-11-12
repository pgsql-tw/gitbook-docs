# 9.28.7. 資料庫物件管理函式

<a id="FUNCTIONS-ADMIN-DBOBJECT"></a>

## 9.28.7. 資料庫物件管理函式 [#](#functions-admin-dbobject) <a href="#functions-admin-dbobject" id="functions-admin-dbobject"></a>

[表 9.102](#functions-admin-dbsize) 所列的函式會計算資料庫物件的磁碟空間使用量，或協助呈現或理解使用量的結果。`bigint` 結果以位元組為單位。如果傳給這些函式的 OID 並不代表既有的物件，就會回傳 `NULL`。

<a id="FUNCTIONS-ADMIN-DBSIZE"></a>

### 表 9.102. 資料庫物件大小函式 [#](#functions-admin-dbsize) <a href="#functions-admin-dbsize" id="functions-admin-dbsize"></a>

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
        顯示存放在磁碟上之 <acronym class="acronym">TOAST</acronym> 化值的 <code class="structfield">chunk_id</code>。如果該值未經 <acronym class="acronym">TOAST</acronym> 處理或不在磁碟上，就回傳 <code class="literal">NULL</code>。關於 <acronym class="acronym">TOAST</acronym> 的更多資訊，請參閱<a class="xref" href="../../../internals/storage/storage-toast.md">第 66.2 節</a>。
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
<code class="literal">fsm</code> 回傳與該關聯相關聯之空閒空間對應表（Free Space Map，請參閱<a class="xref" href="../../../internals/storage/storage-fsm.md">第 66.3 節</a>）的大小。
          </p></li><li class="listitem"><p>
<code class="literal">vm</code> 回傳與該關聯相關聯之可見性對應表（Visibility Map，請參閱<a class="xref" href="../../../internals/storage/storage-vm.md">第 66.4 節</a>）的大小。
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

上述對資料表或索引進行操作的函式接受 `regclass` 引數，它就是該資料表或索引在 `pg_class` 系統目錄中的 OID。不過，你不必手動查詢 OID，因為 `regclass` 資料型別的輸入轉換器會替你完成這項工作。詳情請參閱[第 8.19 節](../../datatype/datatype-oid.md)。

[表 9.103](#functions-admin-dblocation) 所列的函式可協助識別與資料庫物件相關聯的特定磁碟檔案。

<a id="FUNCTIONS-ADMIN-DBLOCATION"></a>

### 表 9.103. 資料庫物件位置函式 [#](#functions-admin-dblocation) <a href="#functions-admin-dblocation" id="functions-admin-dblocation"></a>

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
        回傳目前指派給指定關聯的<span class="quote">「<span class="quote">filenode</span>」</span>（檔案節點）編號。filenode 是該關聯所使用之檔案名稱的基本組成部分（更多資訊請參閱<a class="xref" href="../../../internals/storage/storage-file-layout.md">第 66.1 節</a>）。對大多數關聯而言，結果與 <code class="structname">pg_class</code>.<code class="structfield">relfilenode</code> 相同，但對某些系統目錄而言，<code class="structfield">relfilenode</code> 為零，必須使用這個函式才能取得正確的值。如果傳入的是沒有儲存空間的關聯（例如檢視表），函式會回傳 NULL。
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

[表 9.104](#functions-admin-collation) 列出用於管理定序的函式。

<a id="FUNCTIONS-ADMIN-COLLATION"></a>

### 表 9.104. 定序管理函式 [#](#functions-admin-collation) <a href="#functions-admin-collation" id="functions-admin-collation"></a>

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
        回傳該定序物件目前安裝在作業系統中的實際版本。如果這與 <code class="structname">pg_collation</code>.<code class="structfield">collversion</code> 中的值不同，那麼相依於該定序的物件可能需要重建。另請參閱 <a class="xref" href="../../../reference/sql-commands/sql-altercollation.md"><span class="refentrytitle">ALTER COLLATION</span></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.8.2.2.2.1.1.1"></a>
<code class="function">pg_database_collation_actual_version</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳資料庫的定序目前安裝在作業系統中的實際版本。如果這與 <code class="structname">pg_database</code>.<code class="structfield">datcollversion</code> 中的值不同，那麼相依於該定序的物件可能需要重建。另請參閱 <a class="xref" href="../../../reference/sql-commands/sql-alterdatabase.md"><span class="refentrytitle">ALTER DATABASE</span></a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.9.8.2.2.3.1.1.1"></a>
<code class="function">pg_import_system_collations</code> ( <em class="parameter"><code>schema</code></em> <code class="type">regnamespace</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        依據在作業系統中找到的所有語系，將定序加入系統目錄 <code class="structname">pg_collation</code>。這就是 <code class="command">initdb</code> 所使用的方式；詳情請參閱<a class="xref" href="../../../server-administration/charset/collation.md#collation-managing">第 23.2.2 節</a>。如果之後在作業系統中安裝了其他語系，可以再次執行這個函式，為新的語系加入定序。與 <code class="structname">pg_collation</code> 中既有項目相符的語系會被略過。（但以已不再存在於作業系統中之語系為基礎的定序物件，並不會被這個函式移除。）<em class="parameter"><code>schema</code></em> 參數通常會是 <code class="literal">pg_catalog</code>，但這並非必要條件；定序也可以安裝到其他綱要中。函式會回傳它所建立的新定序物件數量。這個函式只限超級使用者使用。
       </p></td></tr></tbody></table>

<br>

[表 9.105](#functions-admin-statsmod) 列出用於操作統計資訊的函式。這些函式不能在復原期間執行。

### 警告

這些統計資訊操作函式所做的變更，很可能會被 [autovacuum](../../../server-administration/maintenance/routine-vacuuming.md#autovacuum)（或手動執行的 `VACUUM` 或 `ANALYZE`）覆寫，因此應視為暫時性的。

<a id="FUNCTIONS-ADMIN-STATSMOD"></a>

### 表 9.105. 資料庫物件統計資訊操作函式 [#](#functions-admin-statsmod) <a href="#functions-admin-statsmod" id="functions-admin-statsmod"></a>

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
         更新資料表層級的統計資訊。通常這些統計資訊會自動收集，或作為 <a class="xref" href="../../../reference/sql-commands/sql-vacuum.md"><span class="refentrytitle">VACUUM</span></a> 或 <a class="xref" href="../../../reference/sql-commands/sql-analyze.md"><span class="refentrytitle">ANALYZE</span></a> 的一部分而更新，所以不需要呼叫這個函式。不過，在還原之後如果尚未執行 <code class="command">ANALYZE</code>，這個函式可以讓最佳化器選擇較好的執行計畫。
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
         引數 <code class="literal">schemaname</code> 與 <code class="literal">relname</code> 是必要的，用來指定資料表。其他引數則是對應於 <a class="link" href="../../../internals/catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a> 中特定欄位之統計資訊的名稱與值。目前支援的關聯統計資訊有：<code class="literal">relpages</code>（值為 <code class="type">integer</code> 型別）、<code class="literal">reltuples</code>（值為 <code class="type">real</code> 型別）、<code class="literal">relallvisible</code>（值為 <code class="type">integer</code> 型別），以及 <code class="literal">relallfrozen</code>（值為 <code class="type">integer</code> 型別）。
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
         建立或更新欄位層級的統計資訊。通常這些統計資訊會自動收集，或作為 <a class="xref" href="../../../reference/sql-commands/sql-vacuum.md"><span class="refentrytitle">VACUUM</span></a> 或 <a class="xref" href="../../../reference/sql-commands/sql-analyze.md"><span class="refentrytitle">ANALYZE</span></a> 的一部分而更新，所以不需要呼叫這個函式。不過，在還原之後如果尚未執行 <code class="command">ANALYZE</code>，這個函式可以讓最佳化器選擇較好的執行計畫。
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
         必要的引數有：<code class="literal">schemaname</code> 與 <code class="literal">relname</code>（值為 <code class="type">text</code> 型別），用來指定資料表；<code class="literal">attname</code>（值為 <code class="type">text</code> 型別）或 <code class="literal">attnum</code>（值為 <code class="type">smallint</code> 型別）二者之一，用來指定欄位；以及 <code class="literal">inherited</code>，用來指定統計資訊是否包含子資料表的值。其他引數則是對應於 <a class="link" href="../../../internals/views/view-pg-stats.md"><code class="structname">pg_stats</code></a> 中欄位之統計資訊的名稱與值。
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

[表 9.106](#functions-info-partition) 列出提供分割資料表結構相關資訊的函式。

<a id="FUNCTIONS-INFO-PARTITION"></a>

### 表 9.106. 分割資訊函式 [#](#functions-info-partition) <a href="#functions-info-partition" id="functions-info-partition"></a>

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

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
