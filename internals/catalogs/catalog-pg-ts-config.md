<a id="CATALOG-PG-TS-CONFIG"></a>

## 52.59. `pg_ts_config` [#](#CATALOG-PG-TS-CONFIG)

<a id="id-1.10.4.61.2"></a>

目錄 `pg_ts_config` 包含代表文字搜尋設定的項目。一個設定指定了特定的文字搜尋剖析器，以及剖析器每一種輸出語彙單元類型所要使用的字典清單。剖析器記錄在 `pg_ts_config` 項目中，但語彙單元到字典的對應則由 [`pg_ts_config_map`](catalog-pg-ts-config-map.md) 中的附屬項目定義。

PostgreSQL 的文字搜尋功能在[第 12 章](../../the-sql-language/textsearch/README.md)中有詳細說明。

<a id="id-1.10.4.61.5"></a>

**表 52.59. `pg_ts_config` 欄位**

<table border="1" class="table" summary="表 52.59. pg_ts_config 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">cfgname</code> <code class="type">name</code>
</p>
<p>
       文字搜尋設定名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cfgnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此設定之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cfgowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       設定的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cfgparser</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-ts-parser.md"><code class="structname">pg_ts_parser</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此設定所用文字搜尋剖析器的 OID
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-config.html)（原文版本：18.6；核對日期：2026-10-17）
