<a id="CATALOG-PG-DESCRIPTION"></a>

## 52.19. `pg_description` [#](#catalog-pg-description) <a href="#catalog-pg-description" id="catalog-pg-description"></a>

<a id="id-1.10.4.21.2"></a>

系統目錄 `pg_description` 存放每個資料庫物件的選擇性描述（註解）。描述可以使用 [`COMMENT`](../../reference/sql-commands/sql-comment.md) 命令操作，並以 psql 的 `\d` 命令檢視。`pg_description` 的初始內容中已提供許多內建系統物件的描述。

另請參閱 [`pg_shdescription`](catalog-pg-shdescription.md)，它對涉及在整個資料庫叢集中共享之物件的描述執行類似的功能。

<a id="id-1.10.4.21.5"></a>

**表 52.19. `pg_description` 欄位**

<table border="1" class="table" summary="表 52.19. pg_description 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       此描述所屬物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此物件所在系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位上的註解，這是欄位編號（<code class="structfield">objoid</code> 與 <code class="structfield">classoid</code> 參照資料表本身）。對於所有其他物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">description</code> <code class="type">text</code>
</p>
<p>
       作為此物件描述的任意文字
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-description.html)（原文版本：18.6；核對日期：2026-10-17）
