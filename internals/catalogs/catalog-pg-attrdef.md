<a id="CATALOG-PG-ATTRDEF"></a>

## 52.6. `pg_attrdef` [#](#CATALOG-PG-ATTRDEF)

<a id="id-1.10.4.8.2"></a>

系統目錄 `pg_attrdef` 存放欄位的預設值運算式與產生運算式。欄位的主要資訊
存放在 [`pg_attribute`](catalog-pg-attribute.md) 中。
只有明確設定了預設值運算式或產生運算式的欄位，才會在這裡有項目。

<a id="id-1.10.4.8.4"></a>

**表 52.6. `pg_attrdef` 欄位**

<table border="1" class="table" summary="表 52.6. pg_attrdef 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">adrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位所屬的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">adnum</code> <code class="type">int2</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       欄位的編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">adbin</code> <code class="type">pg_node_tree</code>
</p>
<p>
       欄位的預設值運算式或產生運算式，以 <code class="function">nodeToString()</code>
       表示法呈現。使用 <code class="literal">pg_get_expr(adbin, adrelid)</code>
       可將其轉換為 SQL 運算式。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-attrdef.html)（原文版本：18.6；核對日期：2026-10-17）
