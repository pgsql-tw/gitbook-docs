<a id="CATALOG-PG-ATTRIBUTE"></a>

## 52.7. `pg_attribute` [#](#catalog-pg-attribute) <a href="#catalog-pg-attribute" id="catalog-pg-attribute"></a>

<a id="id-1.10.4.9.2"></a>

系統目錄 `pg_attribute` 存放資料表欄位的相關資訊。資料庫中每個資料表的
每個欄位，在 `pg_attribute` 中都恰好有一筆資料列。
（索引也會有屬性項目，事實上所有在
[`pg_class`](catalog-pg-class.md)
中有項目的物件都會有。）

「屬性」（attribute）一詞等同於欄位，是基於歷史因素而沿用的。

<a id="id-1.10.4.9.5"></a>

**表 52.7. `pg_attribute` 欄位**

<table border="1" class="table" summary="表 52.7. pg_attribute 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位所屬的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attname</code> <code class="type">name</code>
</p>
<p>
       欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atttypid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位的資料型別（已移除的欄位為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attlen</code> <code class="type">int2</code>
</p>
<p>
       此欄位型別之 <code class="literal">pg_type.typlen</code> 的副本
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnum</code> <code class="type">int2</code>
</p>
<p>
       欄位的編號。一般欄位從 1 開始
       往上編號。系統欄位（例如 <code class="structfield">ctid</code>）
       具有（任意的）負數編號。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atttypmod</code> <code class="type">int4</code>
</p>
<p>
<code class="structfield">atttypmod</code> 記錄在建立資料表時提供的型別專屬資料（例如
       <code class="type">varchar</code> 欄位的最大長度）。它會被傳遞給
       型別專屬的輸入函式與長度強制轉換函式。
       對於不需要 <code class="structfield">atttypmod</code> 的型別，其值通常為 -1。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attndims</code> <code class="type">int2</code>
</p>
<p>
       若此欄位是陣列型別，則為維度數；否則為 0。
       （目前並不強制檢查陣列的維度數，
       因此任何非零值實際上都表示<span class="quote">“<span class="quote">這是陣列</span>”</span>。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attbyval</code> <code class="type">bool</code>
</p>
<p>
       此欄位型別之 <code class="literal">pg_type.typbyval</code> 的副本
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attalign</code> <code class="type">char</code>
</p>
<p>
       此欄位型別之 <code class="literal">pg_type.typalign</code> 的副本
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attstorage</code> <code class="type">char</code>
</p>
<p>
       通常是此欄位型別之 <code class="literal">pg_type.typstorage</code> 的副本。
       對於可 TOAST 的資料型別，可以在建立欄位之後變更此值，
       以控制儲存策略。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attcompression</code> <code class="type">char</code>
</p>
<p>
       此欄位目前的壓縮方法。通常為
       <code class="literal">'\0'</code>，表示使用目前的預設設定
       （請參閱 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION">default_toast_compression</a>）。否則，
       <code class="literal">'p'</code> 選擇 pglz 壓縮，而
       <code class="literal">'l'</code> 選擇 <span class="productname">LZ4</span>
       壓縮。不過，只要 <code class="structfield">attstorage</code> 不允許
       壓縮，此欄位就會被忽略。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnotnull</code> <code class="type">bool</code>
</p>
<p>
       此欄位具有（可能無效的）非空值限制條件。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atthasdef</code> <code class="type">bool</code>
</p>
<p>
       此欄位具有預設值運算式或產生運算式；在這種情況下，
       <a class="link" href="catalog-pg-attrdef.md"><code class="structname">pg_attrdef</code></a> 系統目錄中會有一筆對應的項目，
       實際定義該運算式。（請檢查 <code class="structfield">attgenerated</code>，
       以判斷這是預設值運算式還是產生運算式。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">atthasmissing</code> <code class="type">bool</code>
</p>
<p>
       此欄位有一個值，用於資料列中完全缺少該欄位的情況；
       在資料列建立之後，以非揮發性的 <code class="literal">DEFAULT</code> 值新增欄位時，就會發生這種情況。
       實際使用的值存放在
       <code class="structfield">attmissingval</code> 欄位中。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attidentity</code> <code class="type">char</code>
</p>
<p>
       若為零位元組（<code class="literal">''</code>），則不是識別欄位。
       否則，<code class="literal">a</code> = 一律產生（GENERATED ALWAYS），
       <code class="literal">d</code> = 預設產生（GENERATED BY DEFAULT）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attgenerated</code> <code class="type">char</code>
</p>
<p>
       若為零位元組（<code class="literal">''</code>），則不是產生欄位。
       否則，<code class="literal">s</code> = 儲存式（stored），<code class="literal">v</code> =
       虛擬（virtual）。儲存式產生欄位會像一般欄位一樣實體存放。
       虛擬產生欄位在實體上存放為 null 值，
       實際值則在執行時期計算。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attisdropped</code> <code class="type">bool</code>
</p>
<p>
       此欄位已被移除，不再有效。已移除的欄位
       在實體上仍存在於資料表中，但會被剖析器忽略，
       因此無法透過 SQL 存取。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attislocal</code> <code class="type">bool</code>
</p>
<p>
       此欄位是在該關聯中本地定義的。請注意，一個欄位可以
       同時是本地定義的與繼承而來的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attinhcount</code> <code class="type">int2</code>
</p>
<p>
       此欄位擁有的直接祖先數量。祖先數量不為零的欄位
       既不能被移除，也不能被重新命名。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attcollation</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位所定義的定序；若此欄位
       不是可定序的資料型別，則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attstattarget</code> <code class="type">int2</code>
</p>
<p>
<code class="structfield">attstattarget</code> 控制
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>
       為此欄位所累積之統計資訊的詳細程度。
       零值表示不應收集任何統計資訊。
       null 值表示使用系統預設的統計目標。
       正值的確切意義取決於資料型別。
       對於純量資料型別，<code class="structfield">attstattarget</code>
       既是要收集的<span class="quote">“<span class="quote">最常見值</span>”</span>的目標數量，也是要建立的直方圖區間的目標數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       欄位層級的存取權限（若有專門針對此欄位授予的權限）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attoptions</code> <code class="type">text[]</code>
</p>
<p>
       屬性層級選項，以<span class="quote">“<span class="quote">keyword=value</span>”</span>字串表示
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attfdwoptions</code> <code class="type">text[]</code>
</p>
<p>
       屬性層級的外部資料包裝器選項，以<span class="quote">“<span class="quote">keyword=value</span>”</span>字串表示
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attmissingval</code> <code class="type">anyarray</code>
</p>
<p>
       此欄位含有一個單元素陣列，其中包含資料列中完全缺少該欄位時所使用的值；
       在資料列建立之後，以非揮發性的 <code class="literal">DEFAULT</code> 值新增該欄位時，
       就會發生這種情況。只有在
       <code class="structfield">atthasmissing</code> 為 true 時才會使用此值。
       若沒有值，此欄位為 null。
      </p></td></tr></tbody></table>

<br>

在已移除欄位的 `pg_attribute` 項目中，
`atttypid` 會被重設為零，但
`attlen` 以及其他從
[`pg_type`](catalog-pg-type.md) 複製而來的欄位仍然有效。之所以需要這樣的安排，
是為了應付已移除欄位的資料型別後來也被移除、因而 `pg_type` 中已不再有對應資料列的情況。
`attlen` 與其他欄位可用來解讀資料表中資料列的內容。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-attribute.html)（原文版本：18.6；核對日期：2026-10-17）
