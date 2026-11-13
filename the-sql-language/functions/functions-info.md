<a id="FUNCTIONS-INFO"></a>

## 9.27. 系統資訊函式與運算子 [#](#functions-info) <a href="#functions-info" id="functions-info"></a>

[9.27.1. 工作階段資訊函式](functions-info/functions-info-session.md#functions-info-session)

[9.27.2. 存取權限查詢函式](functions-info/functions-info-access.md#functions-info-access)

[9.27.3. 綱要可見性查詢函式](functions-info/functions-info-schema.md#functions-info-schema)

[9.27.4. 系統目錄資訊函式](functions-info.md#functions-info-catalog)

[9.27.5. 物件資訊與定址函式](functions-info/functions-info-object.md#functions-info-object)

[9.27.6. 註解資訊函式](functions-info/functions-info-comment.md#functions-info-comment)

[9.27.7. 資料有效性檢查函式](functions-info/functions-info-validity.md#functions-info-validity)

[9.27.8. 交易 ID 與快照資訊函式](functions-info/functions-info-snapshot.md#functions-info-snapshot)

[9.27.9. 已提交交易資訊函式](functions-info/functions-info-commit-timestamp.md#functions-info-commit-timestamp)

[9.27.10. 控制資料函式](functions-info/functions-info-controldata.md#functions-info-controldata)

[9.27.11. 版本資訊函式](functions-info/functions-info-version.md#functions-info-version)

[9.27.12. WAL 摘要資訊函式](functions-info/functions-info-wal-summary.md#functions-info-wal-summary)

本節所描述的函式用於取得 PostgreSQL 安裝環境的各種資訊。

### 9.27.1. 工作階段資訊函式 [#](#functions-info-session) <a href="#functions-info-session" id="functions-info-session"></a>

完整內容請見 [9.27.1. 工作階段資訊函式](functions-info/functions-info-session.md#functions-info-session)。

### 9.27.2. 存取權限查詢函式 [#](#functions-info-access) <a href="#functions-info-access" id="functions-info-access"></a>

完整內容請見 [9.27.2. 存取權限查詢函式](functions-info/functions-info-access.md#functions-info-access)。

### 9.27.3. 綱要可見性查詢函式 [#](#functions-info-schema) <a href="#functions-info-schema" id="functions-info-schema"></a>

完整內容請見 [9.27.3. 綱要可見性查詢函式](functions-info/functions-info-schema.md#functions-info-schema)。

<a id="FUNCTIONS-INFO-CATALOG"></a>

### 9.27.4. 系統目錄資訊函式 [#](#functions-info-catalog) <a href="#functions-info-catalog" id="functions-info-catalog"></a>

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

### 9.27.5. 物件資訊與定址函式 [#](#functions-info-object) <a href="#functions-info-object" id="functions-info-object"></a>

完整內容請見 [9.27.5. 物件資訊與定址函式](functions-info/functions-info-object.md#functions-info-object)。

### 9.27.6. 註解資訊函式 [#](#functions-info-comment) <a href="#functions-info-comment" id="functions-info-comment"></a>

完整內容請見 [9.27.6. 註解資訊函式](functions-info/functions-info-comment.md#functions-info-comment)。

### 9.27.7. 資料有效性檢查函式 [#](#functions-info-validity) <a href="#functions-info-validity" id="functions-info-validity"></a>

完整內容請見 [9.27.7. 資料有效性檢查函式](functions-info/functions-info-validity.md#functions-info-validity)。

### 9.27.8. 交易 ID 與快照資訊函式 [#](#functions-info-snapshot) <a href="#functions-info-snapshot" id="functions-info-snapshot"></a>

完整內容請見 [9.27.8. 交易 ID 與快照資訊函式](functions-info/functions-info-snapshot.md#functions-info-snapshot)。

### 9.27.9. 已提交交易資訊函式 [#](#functions-info-commit-timestamp) <a href="#functions-info-commit-timestamp" id="functions-info-commit-timestamp"></a>

完整內容請見 [9.27.9. 已提交交易資訊函式](functions-info/functions-info-commit-timestamp.md#functions-info-commit-timestamp)。

### 9.27.10. 控制資料函式 [#](#functions-info-controldata) <a href="#functions-info-controldata" id="functions-info-controldata"></a>

完整內容請見 [9.27.10. 控制資料函式](functions-info/functions-info-controldata.md#functions-info-controldata)。

### 9.27.11. 版本資訊函式 [#](#functions-info-version) <a href="#functions-info-version" id="functions-info-version"></a>

完整內容請見 [9.27.11. 版本資訊函式](functions-info/functions-info-version.md#functions-info-version)。

### 9.27.12. WAL 摘要資訊函式 [#](#functions-info-wal-summary) <a href="#functions-info-wal-summary" id="functions-info-wal-summary"></a>

完整內容請見 [9.27.12. WAL 摘要資訊函式](functions-info/functions-info-wal-summary.md#functions-info-wal-summary)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
