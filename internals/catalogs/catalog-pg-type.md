<a id="CATALOG-PG-TYPE"></a>

## 52.64. `pg_type` [#](#catalog-pg-type) <a href="#catalog-pg-type" id="catalog-pg-type"></a>

<a id="id-1.10.4.66.2"></a>

目錄 `pg_type` 儲存資料型別的相關資訊。基本型別與列舉型別（純量型別）是以
[`CREATE TYPE`](../../reference/sql-commands/sql-createtype.md) 建立，網域則以
[`CREATE DOMAIN`](../../reference/sql-commands/sql-createdomain.md) 建立。
資料庫中的每個資料表都會自動建立一個複合型別，用以表示該資料表的資料列結構。也可以使用 `CREATE TYPE AS` 建立複合型別。

<a id="id-1.10.4.66.4"></a>

**表 52.64. `pg_type` 欄位**

<table border="1" class="table" summary="表 52.64. pg_type 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typname</code> <code class="type">name</code>
</p>
<p>
       資料型別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此型別之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       型別的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typlen</code> <code class="type">int2</code>
</p>
<p>
       對於固定大小的型別，<code class="structfield">typlen</code> 是該型別內部表示法的位元組數。但對於可變長度型別，<code class="structfield">typlen</code> 為負值。
       -1 表示 <span class="quote">“<span class="quote">varlena</span>”</span> 型別（具有長度字組的型別），
       -2 表示以 null 結尾的 C 字串。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typbyval</code> <code class="type">bool</code>
</p>
<p>
<code class="structfield">typbyval</code> 決定內部常式以傳值或傳參照方式傳遞此型別的值。
       <code class="structfield">typbyval</code> 在
       <code class="structfield">typlen</code> 不是 1、2 或 4（在 Datum 為 8 位元組的機器上，另外也允許 8）時最好為 false。
       可變長度型別一律以傳參照方式傳遞。請注意，即使長度允許傳值，
       <code class="structfield">typbyval</code> 仍可以為 false。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typtype</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">typtype</code> 為
       <code class="literal">b</code> 表示基本型別、
       <code class="literal">c</code> 表示複合型別（例如資料表的資料列型別）、
       <code class="literal">d</code> 表示網域、
       <code class="literal">e</code> 表示列舉型別、
       <code class="literal">p</code> 表示虛擬型別、
       <code class="literal">r</code> 表示範圍型別，或
       <code class="literal">m</code> 表示多重範圍型別。
       另請參閱 <code class="structfield">typrelid</code> 與
       <code class="structfield">typbasetype</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typcategory</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">typcategory</code> 是資料型別的任意分類，
       剖析器用它來決定應<span class="quote">“<span class="quote">優先</span>”</span>採用哪些隱含型別轉換。
       請參閱<a class="xref" href="catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE">表 52.65</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typispreferred</code> <code class="type">bool</code>
</p>
<p>
       若此型別是其
       <code class="structfield">typcategory</code> 內的優先轉換目標，則為 true
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typisdefined</code> <code class="type">bool</code>
</p>
<p>
       若型別已定義則為 true；若這是尚未定義之型別的預留項目，則為 false。當
       <code class="structfield">typisdefined</code> 為 false 時，除了型別名稱、命名空間與 OID 之外，其他內容都不可依賴。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typdelim</code> <code class="type">char</code>
</p>
<p>
       剖析陣列輸入時，用來分隔此型別兩個值的字元。請注意，分隔字元是與陣列元素的資料型別相關聯，而不是與陣列資料型別相關聯。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若這是複合型別（請參閱
       <code class="structfield">typtype</code>），此欄位會指向定義對應資料表的
       <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 項目。（對於獨立的複合型別，該
       <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 項目並不真正代表一個資料表，但仍然需要它，以供該型別的
       <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a> 項目連結。）
       非複合型別則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typsubscript</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       下標處理函式的 OID；若此型別不支援下標，則為零。屬於<span class="quote">“<span class="quote">真正</span>”</span>陣列型別的型別，其 <code class="structfield">typsubscript</code>
       = <code class="function">array_subscript_handler</code>，但其他型別可能有其他處理函式，以實作特殊的下標行為。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typelem</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若 <code class="structfield">typelem</code> 不為零，它會識別
       <code class="structname">pg_type</code> 中的另一個資料列，該資料列定義下標運算所產生的型別。若
       <code class="structfield">typsubscript</code> 為零，此欄位應該為零。不過，當
       <code class="structfield">typsubscript</code> 不為零時，若處理函式不需要
       <code class="structfield">typelem</code> 來決定下標結果的型別，此欄位也可以為零。
       請注意，<code class="structfield">typelem</code> 相依關係被視為意味著元素型別在實體上包含於此型別之中；因此，此型別的存在可能會限制對元素型別所做的 DDL 變更。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typarray</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若 <code class="structfield">typarray</code> 不為零，它會識別
       <code class="structname">pg_type</code> 中的另一個資料列，即以此型別為元素的<span class="quote">“<span class="quote">真正</span>”</span>陣列型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typinput</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       輸入轉換函式（文字格式）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typoutput</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       輸出轉換函式（文字格式）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typreceive</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       輸入轉換函式（二進位格式）；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typsend</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       輸出轉換函式（二進位格式）；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typmodin</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       型別修飾詞輸入函式；若型別不支援修飾詞，則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typmodout</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       型別修飾詞輸出函式；若為零則使用標準格式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typanalyze</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       自訂的 <a class="xref" href="../../reference/sql-commands/sql-analyze.md"><span class="refentrytitle">ANALYZE</span></a> 函式；
       若為零則使用標準函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typalign</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">typalign</code> 是儲存此型別的值時所需的對齊方式。它適用於磁碟上的儲存，也適用於該值在
       <span class="productname">PostgreSQL</span> 內部的大多數表示形式。
       當多個值連續儲存時（例如在磁碟上表示一整個資料列時），會在此型別的資料項（datum）之前插入填補，使其從指定的邊界開始。對齊的基準點是序列中第一個資料項的起點。
       可能的值為：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p><code class="literal">c</code> = <code class="type">char</code> 對齊，亦即不需要對齊。</p></li><li class="listitem"><p><code class="literal">s</code> = <code class="type">short</code> 對齊（在大多數機器上為 2 位元組）。</p></li><li class="listitem"><p><code class="literal">i</code> = <code class="type">int</code> 對齊（在大多數機器上為 4 位元組）。</p></li><li class="listitem"><p><code class="literal">d</code> = <code class="type">double</code> 對齊（在許多機器上為 8 位元組，但絕非全部）。</p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typstorage</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">typstorage</code> 針對 varlena
       型別（即 <code class="structfield">typlen</code> = -1 的型別）指出
       該型別是否已準備好進行 TOAST 處理，以及此型別之屬性的預設策略應為何。
       可能的值為：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">p</code>（plain）：值必須一律以一般方式儲存
          （非 varlena 型別一律使用此值）。
         </p></li><li class="listitem"><p>
<code class="literal">e</code>（external）：值可以儲存在次要的
          <span class="quote">“<span class="quote">TOAST</span>”</span> 關聯中（若該關聯有的話，請參閱
          <code class="literal">pg_class.reltoastrelid</code>）。
         </p></li><li class="listitem"><p>
<code class="literal">m</code>（main）：值可以被壓縮並以內嵌（inline）方式儲存。
         </p></li><li class="listitem"><p>
<code class="literal">x</code>（extended）：值可以被壓縮和／或移至次要關聯。
         </p></li></ul></div><p>
對於可 TOAST 的型別，<code class="literal">x</code> 是常見的選擇。
       請注意，<code class="literal">m</code> 的值也可以被移出至次要儲存空間，但僅作為最後手段（<code class="literal">e</code>
       與 <code class="literal">x</code> 的值會先被移出）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typnotnull</code> <code class="type">bool</code>
</p>
<p>
<code class="structfield">typnotnull</code> 表示型別上的非 NULL 限制條件。僅用於網域。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typbasetype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若這是網域（請參閱 <code class="structfield">typtype</code>），
       <code class="structfield">typbasetype</code> 會識別此型別所依據的型別。若此型別不是網域，則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typtypmod</code> <code class="type">int4</code>
</p>
<p>
       網域使用 <code class="structfield">typtypmod</code> 記錄要套用至其基礎型別的 <code class="literal">typmod</code>
       （若基礎型別不使用
       <code class="literal">typmod</code>，則為 -1）。若此型別不是網域，則為 -1。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typndims</code> <code class="type">int4</code>
</p>
<p>
<code class="structfield">typndims</code> 是建立在陣列上的網域（也就是 <code class="structfield">typbasetype</code> 為陣列型別）的陣列維度數。
       對於建立在陣列型別上的網域以外的型別，此值為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typcollation</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
<code class="structfield">typcollation</code> 指定型別的定序。若型別不支援定序，此值將為零。支援定序的基本型別在此會有非零值，通常是 <code class="symbol">DEFAULT_COLLATION_OID</code>。
       建立在可定序型別上的網域，若為該網域指定了定序，其定序 OID 可以與其基礎型別的不同。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typdefaultbin</code> <code class="type">pg_node_tree</code>
</p>
<p>
       若 <code class="structfield">typdefaultbin</code> 不為 null，它是此型別預設表示式的
       <code class="function">nodeToString()</code>
       表示形式。這只用於網域。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typdefault</code> <code class="type">text</code>
</p>
<p>
若型別沒有相關聯的預設值，
       <code class="structfield">typdefault</code> 為 null。若 <code class="structfield">typdefaultbin</code> 不為 null，
       <code class="structfield">typdefault</code> 必須包含
       <code class="structfield">typdefaultbin</code> 所表示之預設表示式的人類可讀版本。若
       <code class="structfield">typdefaultbin</code> 為 null 而 <code class="structfield">typdefault</code> 不為 null，
       則 <code class="structfield">typdefault</code> 是該型別預設值的外部表示形式，可以將它交給該型別的輸入轉換器以產生常數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">typacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳情請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

### 注意

對於系統資料表中使用的固定寬度型別，`pg_type` 中定義的大小與對齊方式，必須與編譯器在表示資料表資料列的結構中配置該欄位的方式一致，這一點至關重要。

[表 52.65](catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE) 列出 `typcategory` 的系統定義值。未來新增至此清單的任何值也都會是大寫 ASCII 字母。其他所有 ASCII 字元都保留給使用者定義的類別。

<a id="CATALOG-TYPCATEGORY-TABLE"></a>

**表 52.65. `typcategory` 代碼**

<table border="1" class="table" summary="表 52.65. typcategory 代碼"><colgroup><col/><col/></colgroup><thead><tr><th>代碼</th><th>類別</th></tr></thead><tbody><tr><td><code class="literal">A</code></td><td>陣列型別</td></tr><tr><td><code class="literal">B</code></td><td>布林型別</td></tr><tr><td><code class="literal">C</code></td><td>複合型別</td></tr><tr><td><code class="literal">D</code></td><td>日期／時間型別</td></tr><tr><td><code class="literal">E</code></td><td>列舉型別</td></tr><tr><td><code class="literal">G</code></td><td>幾何型別</td></tr><tr><td><code class="literal">I</code></td><td>網路位址型別</td></tr><tr><td><code class="literal">N</code></td><td>數值型別</td></tr><tr><td><code class="literal">P</code></td><td>虛擬型別</td></tr><tr><td><code class="literal">R</code></td><td>範圍型別</td></tr><tr><td><code class="literal">S</code></td><td>字串型別</td></tr><tr><td><code class="literal">T</code></td><td>時間間隔型別</td></tr><tr><td><code class="literal">U</code></td><td>使用者定義型別</td></tr><tr><td><code class="literal">V</code></td><td>位元字串型別</td></tr><tr><td><code class="literal">X</code></td><td><code class="type">unknown</code> 型別</td></tr><tr><td><code class="literal">Z</code></td><td>內部使用型別</td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-type.html)（原文版本：18.6；核對日期：2026-10-17）
