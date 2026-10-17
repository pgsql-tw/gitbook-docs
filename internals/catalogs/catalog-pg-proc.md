<a id="CATALOG-PG-PROC"></a>

## 52.39. `pg_proc` [#](#CATALOG-PG-PROC)

<a id="id-1.10.4.41.2"></a>

目錄 `pg_proc` 儲存函式、程序、彙總函式與視窗函式
（也統稱為常式）的相關資訊。更多資訊請參閱 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)、[CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md) 與
[第 36.3 節](../../server-programming/extend/xfunc.md)。

若 `prokind` 指出該項目是彙總函式，則
[`pg_aggregate`](catalog-pg-aggregate.md) 中應該有一筆相符的資料列。

<a id="id-1.10.4.41.5"></a>

**表 52.39. `pg_proc` 欄位**

<table border="1" class="table" summary="表 52.39. pg_proc 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">proname</code> <code class="type">name</code>
</p>
<p>
       函式名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此函式之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此函式的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prolang</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-language.md"><code class="structname">pg_language</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此函式的實作語言或呼叫介面
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">procost</code> <code class="type">float4</code>
</p>
<p>
       估計的執行成本（以
       <a class="xref" href="../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-OPERATOR-COST">cpu_operator_cost</a> 為單位）；若為 <code class="structfield">proretset</code>，
       則為每個傳回資料列的成本
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prorows</code> <code class="type">float4</code>
</p>
<p>
       估計的結果資料列數（若非 <code class="structfield">proretset</code> 則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provariadic</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       可變參數陣列參數之元素的資料型別；
       若函式沒有可變參數，則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosupport</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此函式的規劃器支援函式
       （請參閱<a class="xref" href="../../server-programming/extend/xfunc-optimization.md">第 36.11 節</a>）；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prokind</code> <code class="type">char</code>
</p>
<p>
<code class="literal">f</code> 表示一般函式，<code class="literal">p</code>
       表示程序，<code class="literal">a</code> 表示彙總函式，或
       <code class="literal">w</code> 表示視窗函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosecdef</code> <code class="type">bool</code>
</p>
<p>
       函式是安全性定義者（security definer，即 <span class="quote">“<span class="quote">setuid</span>”</span>
       函式）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proleakproof</code> <code class="type">bool</code>
</p>
<p>
       此函式沒有副作用。除了透過傳回值之外，不會傳遞任何關於
       引數的資訊。任何可能依其引數的值而擲出錯誤的函式
       都不是 leakproof（防洩漏）的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proisstrict</code> <code class="type">bool</code>
</p>
<p>
       若任何呼叫引數為 null，函式即傳回 null。在這種情況下，
       函式實際上完全不會被呼叫。不是 <span class="quote">“<span class="quote">strict</span>”</span> 的函式
       必須能夠處理 null 輸入。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proretset</code> <code class="type">bool</code>
</p>
<p>
       函式傳回一個集合（即指定資料型別的多個值）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provolatile</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">provolatile</code> 指出函式的結果是只取決於
       其輸入引數，還是會受外部因素影響。
       <code class="literal">i</code> 表示 <span class="quote">“<span class="quote">immutable</span>”</span> 函式，
       對相同的輸入一律產生相同的結果。
       <code class="literal">s</code> 表示 <span class="quote">“<span class="quote">stable</span>”</span> 函式，
       其結果（在輸入固定時）在單次掃描內不會改變。
       <code class="literal">v</code> 表示 <span class="quote">“<span class="quote">volatile</span>”</span> 函式，
       其結果可能隨時改變。（有副作用的函式也請使用 <code class="literal">v</code>，
       使對它們的呼叫不會被最佳化掉。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proparallel</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">proparallel</code> 指出函式
       是否可以在平行模式下安全執行。
       <code class="literal">s</code> 表示可在平行模式下
       不受限制地安全執行的函式。
       <code class="literal">r</code> 表示可在平行模式下執行、
       但其執行僅限於平行群組領導程序的函式；
       平行工作程序不能呼叫這些函式。
       <code class="literal">u</code> 表示在平行模式下不安全的函式；
       只要存在這類函式，就會強制採用序列執行計畫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronargs</code> <code class="type">int2</code>
</p>
<p>
       輸入引數的數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronargdefaults</code> <code class="type">int2</code>
</p>
<p>
       具有預設值的引數數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prorettype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       傳回值的資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargtypes</code> <code class="type">oidvector</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       函式引數資料型別的陣列。此陣列只包含
       輸入引數（包括 <code class="literal">INOUT</code> 與
       <code class="literal">VARIADIC</code> 引數），因此代表
       函式的呼叫簽章。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proallargtypes</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       函式引數資料型別的陣列。此陣列包含
       所有引數（包括 <code class="literal">OUT</code> 與
       <code class="literal">INOUT</code> 引數）；不過，若所有
       引數都是 <code class="literal">IN</code> 引數，此欄位為 null。
       請注意，此陣列的下標從 1 起算，而因歷史因素，
       <code class="structfield">proargtypes</code> 的下標從 0 起算。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargmodes</code> <code class="type">char[]</code>
</p>
<p>
       函式引數模式的陣列，編碼方式為：
       <code class="literal">i</code> 表示 <code class="literal">IN</code> 引數、
       <code class="literal">o</code> 表示 <code class="literal">OUT</code> 引數、
       <code class="literal">b</code> 表示 <code class="literal">INOUT</code> 引數、
       <code class="literal">v</code> 表示 <code class="literal">VARIADIC</code> 引數、
       <code class="literal">t</code> 表示 <code class="literal">TABLE</code> 引數。
       若所有引數都是 <code class="literal">IN</code> 引數，
       此欄位為 null。
       請注意，下標對應的是
       <code class="structfield">proallargtypes</code> 的位置，而不是 <code class="structfield">proargtypes</code> 的位置。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargnames</code> <code class="type">text[]</code>
</p>
<p>
       函式引數名稱的陣列。
       沒有名稱的引數在陣列中設為空字串。
       若所有引數都沒有名稱，此欄位為 null。
       請注意，下標對應的是
       <code class="structfield">proallargtypes</code> 的位置，而不是 <code class="structfield">proargtypes</code> 的位置。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargdefaults</code> <code class="type">pg_node_tree</code>
</p>
<p>
       預設值的運算式樹（以 <code class="function">nodeToString()</code> 表示法呈現）。
       這是一個含有
       <code class="structfield">pronargdefaults</code> 個元素的串列，對應最後
       <em class="replaceable"><code>N</code></em> 個<span class="emphasis"><em>輸入</em></span>引數（即最後
       <em class="replaceable"><code>N</code></em> 個 <code class="structfield">proargtypes</code> 位置）。
       若所有引數都沒有預設值，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">protrftypes</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       要套用轉換（transform）的引數／結果資料型別陣列
       （取自函式的 <code class="literal">TRANSFORM</code>
       子句）。若無則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosrc</code> <code class="type">text</code>
</p>
<p>
       此欄位告訴函式處理器如何呼叫該函式。依實作語言／呼叫慣例而定，
       它可能是直譯式語言中函式的實際原始碼、連結符號、檔案名稱，
       或幾乎任何其他內容。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">probin</code> <code class="type">text</code>
</p>
<p>
       關於如何呼叫該函式的附加資訊。
       同樣地，其解讀方式取決於語言。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosqlbody</code> <code class="type">pg_node_tree</code>
</p>
<p>
       預先剖析的 SQL 函式主體。當 SQL 語言函式的主體
       以 SQL 標準寫法提供、而不是以字串常值提供時，
       會使用此欄位。其他情況下為 null。
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proconfig</code> <code class="type">text[]</code>
</p>
<p>
       函式針對執行期設定變數的區域設定值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

對於編譯式函式（包括內建與動態載入的函式），
`prosrc` 包含函式的 C 語言
名稱（連結符號）。
對於 SQL 語言函式，若原始碼是以字串常值指定，`prosrc` 包含
函式的原始碼文字；
但若函式主體是以 SQL 標準風格指定，則不使用
`prosrc`（通常為空字串），而由 `prosqlbody` 包含
預先剖析的定義。
對於其他所有目前已知的語言類型，
`prosrc` 包含函式的原始碼
文字。除了動態載入的 C 函式之外，`probin` 都是 null；
對於動態載入的 C 函式，它提供包含該函式的
共享程式庫檔案名稱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-proc.html)（原文版本：18.6；核對日期：2026-10-17）
