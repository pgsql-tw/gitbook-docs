<a id="CATALOG-PG-CONVERSION"></a>

## 52.14. `pg_conversion` [#](#CATALOG-PG-CONVERSION)

<a id="id-1.10.4.16.2"></a>

系統目錄 `pg_conversion` 描述編碼轉換函式。詳細資訊請參閱 [CREATE CONVERSION](../../reference/sql-commands/sql-createconversion.md)。

<a id="id-1.10.4.16.4"></a>

**表 52.14. `pg_conversion` 欄位**

<table border="1" class="table" summary="表 52.14. pg_conversion 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">conname</code> <code class="type">name</code>
</p>
<p>
       轉換的名稱（在命名空間內唯一）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">connamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此轉換之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       轉換的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conforencoding</code> <code class="type">int4</code>
</p>
<p>
       來源編碼 ID（<a class="link" href="../../the-sql-language/functions/functions-info.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a>
       可以將此數字轉換為編碼名稱）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">contoencoding</code> <code class="type">int4</code>
</p>
<p>
       目的編碼 ID（<a class="link" href="../../the-sql-language/functions/functions-info.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a>
       可以將此數字轉換為編碼名稱）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conproc</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       轉換函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">condefault</code> <code class="type">bool</code>
</p>
<p>
       若此為預設轉換則為真
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-conversion.html)（原文版本：18.6；核對日期：2026-10-17）
