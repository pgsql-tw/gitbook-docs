<a id="CATALOG-PG-INDEX"></a>

## 52.26. `pg_index` [#](#catalog-pg-index) <a href="#catalog-pg-index" id="catalog-pg-index"></a>

<a id="id-1.10.4.28.2"></a>

目錄 `pg_index` 存放索引的部分資訊，其餘資訊大多位於 [`pg_class`](catalog-pg-class.md) 中。

<a id="id-1.10.4.28.4"></a>

**表 52.26. `pg_index` 欄位**

<table border="1" class="table" summary="表 52.26. pg_index 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此索引之 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此索引所屬資料表之 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnatts</code> <code class="type">int2</code>
</p>
<p>
       索引中的欄位總數（與 <code class="literal">pg_class.relnatts</code> 重複）；此數目同時包含鍵屬性與包含屬性
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnkeyatts</code> <code class="type">int2</code>
</p>
<p>
       索引中<em class="firstterm">鍵欄位</em>的數目，不計入任何<em class="firstterm">包含欄位</em>；包含欄位僅被儲存，不參與索引語意
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisunique</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此索引為唯一值索引
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indnullsnotdistinct</code> <code class="type">bool</code>
</p>
<p>
       此值只用於唯一值索引。若為 false，此唯一值索引會將 null 值視為相異（因此索引的一個欄位中可以包含多個 null 值，這是 PostgreSQL 的預設行為）。若為 true，則會將 null 值視為相等（因此索引的一個欄位中只能包含一個 null 值）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisprimary</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此索引代表資料表的主鍵（此值為 true 時，<code class="structfield">indisunique</code> 應該一律為 true）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisexclusion</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此索引支援排除限制條件
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indimmediate</code> <code class="type">bool</code>
</p>
<p>
       若為 true，唯一性檢查會在插入時立即強制執行（若 <code class="structfield">indisunique</code> 不為 true，則此欄位無關緊要）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisclustered</code> <code class="type">bool</code>
</p>
<p>
       若為 true，表示資料表上一次是依此索引進行叢集
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisvalid</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此索引目前可有效用於查詢。false 表示此索引可能不完整：它仍必須由 <a class="link" href="../../reference/sql-commands/sql-insert.md"><code class="command">INSERT</code></a>/<a class="link" href="../../reference/sql-commands/sql-update.md"><code class="command">UPDATE</code></a> 作業修改，但無法安全地用於查詢。若它是唯一值索引，其唯一性也不保證成立。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indcheckxmin</code> <code class="type">bool</code>
</p>
<p>
       若為 true，則查詢不得使用此索引，直到 <code class="structfield">xmin</code>（屬於此 <code class="structname">pg_index</code> 資料列）低於查詢的 <code class="symbol">TransactionXmin</code> 事件視界（event horizon）為止，因為資料表可能包含損壞的 <a class="link" href="../storage/storage-hot.md">HOT 鏈</a>，其中有查詢看得到、但與索引不相容的資料列
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisready</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此索引目前已可接受插入。false 表示 <a class="link" href="../../reference/sql-commands/sql-insert.md"><code class="command">INSERT</code></a>/<a class="link" href="../../reference/sql-commands/sql-update.md"><code class="command">UPDATE</code></a> 作業必須忽略此索引。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indislive</code> <code class="type">bool</code>
</p>
<p>
       若為 false，此索引正在移除過程中，在所有用途上都應該忽略它（包括 HOT 安全性的判斷）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indisreplident</code> <code class="type">bool</code>
</p>
<p>
       若為 true，表示此索引已透過 <a class="link" href="../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY"><code class="command">ALTER TABLE ...
       REPLICA IDENTITY USING INDEX ...</code></a> 被選為<span class="quote">“<span class="quote">複寫識別（replica identity）</span>”</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indkey</code> <code class="type">int2vector</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       這是由 <code class="structfield">indnatts</code> 個值組成的陣列，指出此索引所索引的是哪些資料表欄位。例如，值 <code class="literal">1 3</code> 表示索引項目由資料表的第一個與第三個欄位構成。鍵欄位排在非鍵（包含）欄位之前。此陣列中的零表示對應的索引屬性是以資料表欄位構成的運算式，而非單純的欄位參照。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indcollation</code> <code class="type">oidvector</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對於索引鍵中的每個欄位（共 <code class="structfield">indnkeyatts</code> 個值），此欄位存放該索引所使用之定序的 OID；若該欄位不是可定序的資料型別則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indclass</code> <code class="type">oidvector</code>
       （參照 <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對於索引鍵中的每個欄位（共 <code class="structfield">indnkeyatts</code> 個值），此欄位存放所使用之運算子類別的 OID。詳細資訊請參閱 <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indoption</code> <code class="type">int2vector</code>
</p>
<p>
       這是由 <code class="structfield">indnkeyatts</code> 個值組成的陣列，存放每個欄位的旗標位元。這些位元的意義由索引的存取方法定義。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexprs</code> <code class="type">pg_node_tree</code>
</p>
<p>
       非單純欄位參照之索引屬性的運算式樹（以 <code class="function">nodeToString()</code> 表示法呈現）。這是一個清單，<code class="structfield">indkey</code> 中每個為零的項目各對應一個元素。若所有索引屬性都是單純參照則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indpred</code> <code class="type">pg_node_tree</code>
</p>
<p>
       部分索引述詞的運算式樹（以 <code class="function">nodeToString()</code> 表示法呈現）。若不是部分索引則為 null。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-index.html)（原文版本：18.6；核對日期：2026-10-17）
