<a id="CATALOG-PG-PARTITIONED-TABLE"></a>

## 52.37. `pg_partitioned_table` [#](#CATALOG-PG-PARTITIONED-TABLE)

<a id="id-1.10.4.39.2"></a>

目錄 `pg_partitioned_table` 儲存資料表如何分割的相關資訊。

<a id="id-1.10.4.39.4"></a>

**表 52.37. `pg_partitioned_table` 欄位**

<table border="1" class="table" summary="表 52.37. pg_partitioned_table 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此分割資料表在 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 中之項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partstrat</code> <code class="type">char</code>
</p>
<p>
       分割策略；<code class="literal">h</code> = 雜湊分割資料表，
       <code class="literal">l</code> = 清單分割資料表，<code class="literal">r</code> = 範圍分割資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partnatts</code> <code class="type">int2</code>
</p>
<p>
       分割鍵中的欄位數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partdefid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此分割資料表之預設分割區在 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 中之項目的 OID；
       若此分割資料表沒有預設分割區，則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partattrs</code> <code class="type">int2vector</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       這是一個含有 <code class="structfield">partnatts</code> 個值的陣列，
       指出哪些資料表欄位屬於分割鍵。例如，值 <code class="literal">1 3</code> 表示由資料表的第一個
       與第三個欄位構成分割鍵。此陣列中的零表示對應的分割鍵欄位是
       運算式，而不是單純的欄位參照。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partclass</code> <code class="type">oidvector</code>
       （參照 <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對分割鍵中的每個欄位，此欄位記錄要使用之運算子類別的 OID。詳細資訊請參閱
       <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partcollation</code> <code class="type">oidvector</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對分割鍵中的每個欄位，此欄位記錄分割時要使用之定序的 OID；
       若該欄位不是可定序的資料型別，則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partexprs</code> <code class="type">pg_node_tree</code>
</p>
<p>
       非單純欄位參照之分割鍵欄位的運算式樹（以 <code class="function">nodeToString()</code>
       表示法呈現）。這是一個串列，
       <code class="structfield">partattrs</code> 中的每個零項目各對應一個元素。若所有分割鍵欄位
       都是單純參照，則為 null。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-partitioned-table.html)（原文版本：18.6；核對日期：2026-10-17）
