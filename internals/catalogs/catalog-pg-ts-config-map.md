<a id="CATALOG-PG-TS-CONFIG-MAP"></a>

## 52.60. `pg_ts_config_map` [#](#catalog-pg-ts-config-map) <a href="#catalog-pg-ts-config-map" id="catalog-pg-ts-config-map"></a>

<a id="id-1.10.4.62.2"></a>

目錄 `pg_ts_config_map` 包含的項目指出：對於每個文字搜尋設定之剖析器的每一種輸出語彙單元類型，應該查詢哪些文字搜尋字典，以及查詢的順序。

PostgreSQL 的文字搜尋功能在[第 12 章](../../the-sql-language/textsearch/README.md)中有詳細說明。

<a id="id-1.10.4.62.5"></a>

**表 52.60. `pg_ts_config_map` 欄位**

<table border="1" class="table" summary="表 52.60. pg_ts_config_map 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mapcfg</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-ts-config.md"><code class="structname">pg_ts_config</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       擁有此對應項目之 <a class="link" href="catalog-pg-ts-config.md"><code class="structname">pg_ts_config</code></a> 項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maptokentype</code> <code class="type">int4</code>
</p>
<p>
       該設定之剖析器所產生的語彙單元類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mapseqno</code> <code class="type">int4</code>
</p>
<p>
       查詢此項目的順序（<code class="structfield">mapseqno</code> 較小者優先）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mapdict</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-ts-dict.md"><code class="structname">pg_ts_dict</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       要查詢之文字搜尋字典的 OID
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-config-map.html)（原文版本：18.6；核對日期：2026-10-17）
