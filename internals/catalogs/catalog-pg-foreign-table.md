<a id="CATALOG-PG-FOREIGN-TABLE"></a>

## 52.25. `pg_foreign_table` [#](#CATALOG-PG-FOREIGN-TABLE)

<a id="id-1.10.4.27.2"></a>

目錄 `pg_foreign_table` 存放外部資料表的輔助資訊。外部資料表主要以 [`pg_class`](catalog-pg-class.md) 項目表示，就像一般資料表一樣。它在 `pg_foreign_table` 中的項目，則存放只與外部資料表相關、而與其他任何種類的關聯無關的資訊。

<a id="id-1.10.4.27.4"></a>

**表 52.25. `pg_foreign_table` 欄位**

<table border="1" class="table" summary="表 52.25. pg_foreign_table 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此外部資料表之 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftserver</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-foreign-server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此外部資料表之外部伺服器的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftoptions</code> <code class="type">text[]</code>
</p>
<p>
       外部資料表選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串形式呈現
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-foreign-table.html)（原文版本：18.6；核對日期：2026-10-17）
