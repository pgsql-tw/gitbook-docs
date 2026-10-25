<a id="VIEW-PG-SEQUENCES"></a>

## 53.24. `pg_sequences` [#](#view-pg-sequences) <a href="#view-pg-sequences" id="view-pg-sequences"></a>

<a id="id-1.10.5.28.2"></a>

檢視表 `pg_sequences` 提供對資料庫中每個序列之實用資訊的存取。

<a id="id-1.10.5.28.4"></a>

**表 53.24. `pg_sequences` 欄位**

<table border="1" class="table" summary="表 53.24. pg_sequences 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含序列之綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequencename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       序列名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequenceowner</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       序列擁有者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">regtype</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       序列的資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">start_value</code> <code class="type">int8</code>
</p>
<p>
       序列的起始值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_value</code> <code class="type">int8</code>
</p>
<p>
       序列的最小值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_value</code> <code class="type">int8</code>
</p>
<p>
       序列的最大值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">increment_by</code> <code class="type">int8</code>
</p>
<p>
       序列的遞增值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cycle</code> <code class="type">bool</code>
</p>
<p>
       序列是否循環
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cache_size</code> <code class="type">int8</code>
</p>
<p>
       序列的快取大小
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_value</code> <code class="type">int8</code>
</p>
<p>
       最後寫入磁碟的序列值。若使用了快取，此值可能大於序列最後一次發出的值。
      </p></td></tr></tbody></table>

<br>

若下列任一條件成立，`last_value` 欄位讀出的值將為 null：

* 此序列尚未被讀取過。
* 目前使用者對此序列既沒有 `USAGE` 權限，也沒有 `SELECT` 權限。
* 此序列為無日誌序列，且伺服器為待命伺服器。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-sequences.html)（原文版本：18.6；核對日期：2026-10-10）
