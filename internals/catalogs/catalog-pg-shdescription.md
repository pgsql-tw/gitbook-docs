<a id="CATALOG-PG-SHDESCRIPTION"></a>

## 52.49. `pg_shdescription` [#](#CATALOG-PG-SHDESCRIPTION)

<a id="id-1.10.4.51.2"></a>

系統目錄 `pg_shdescription` 存放共享資料庫物件的選擇性描述（註解）。描述可以使用 [`COMMENT`](../../reference/sql-commands/sql-comment.md) 命令操作，並以 psql 的 `\d` 命令檢視。

另請參閱 [`pg_description`](catalog-pg-description.md)，它對涉及單一資料庫內物件的描述執行類似的功能。

與大多數系統目錄不同，`pg_shdescription` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_shdescription`，而不是每個資料庫各一份。

<a id="id-1.10.4.51.6"></a>

**表 52.49. `pg_shdescription` 欄位**

<table border="1" class="table" summary="表 52.49. pg_shdescription 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       此物件所在之系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">description</code> <code class="type">text</code>
</p>
<p>
       作為此物件描述的任意文字
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-shdescription.html)（原文版本：18.6；核對日期：2026-10-17）
