<a id="CATALOG-PG-PUBLICATION-REL"></a>

## 52.42. `pg_publication_rel` [#](#CATALOG-PG-PUBLICATION-REL)

<a id="id-1.10.4.44.2"></a>

系統目錄 `pg_publication_rel` 包含資料庫中關聯與發佈之間的對應。這是多對多的對應。關於這些資訊更易於使用的檢視方式，另請參閱[第 53.18 節](../views/view-pg-publication-tables.md)。

<a id="id-1.10.4.44.4"></a>

**表 52.42. `pg_publication_rel` 欄位**

<table border="1" class="table" summary="表 52.42. pg_publication_rel 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">prpubid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對發佈的參照
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對關聯的參照
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prqual</code> <code class="type">pg_node_tree</code>
</p>
<p>關聯之發佈限定條件的運算式樹（採 <code class="function">nodeToString()</code> 表示法）。若沒有發佈限定條件，則為 null。</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prattrs</code> <code class="type">int2vector</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       這是一個值陣列，指出哪些資料表欄位屬於此發佈。例如值 <code class="literal">1 3</code> 表示發佈資料表的第一個與第三個欄位。null 值表示發佈所有欄位。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-publication-rel.html)（原文版本：18.6；核對日期：2026-10-17）
