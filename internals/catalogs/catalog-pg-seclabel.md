<a id="CATALOG-PG-SECLABEL"></a>

## 52.46. `pg_seclabel` [#](#catalog-pg-seclabel) <a href="#catalog-pg-seclabel" id="catalog-pg-seclabel"></a>

<a id="id-1.10.4.48.2"></a>

系統目錄 `pg_seclabel` 存放資料庫物件上的安全標籤。安全標籤可以使用 [`SECURITY LABEL`](../../reference/sql-commands/sql-security-label.md) 命令操作。若要以更簡便的方式檢視安全標籤，請參閱[第 53.23 節](../views/view-pg-seclabels.md)。

另請參閱 [`pg_shseclabel`](catalog-pg-shseclabel.md)，它對在整個資料庫叢集中共享之資料庫物件的安全標籤執行類似的功能。

<a id="id-1.10.4.48.5"></a>

**表 52.46. `pg_seclabel` 欄位**

<table border="1" class="table" summary="表 52.46. pg_seclabel 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       此安全標籤所屬物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此物件所在之系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位上的安全標籤，這是欄位編號（<code class="structfield">objoid</code> 與 <code class="structfield">classoid</code> 參照資料表本身）。對於所有其他物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provider</code> <code class="type">text</code>
</p>
<p>
       與此標籤相關聯的標籤提供者。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">label</code> <code class="type">text</code>
</p>
<p>
       套用於此物件的安全標籤。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-seclabel.html)（原文版本：18.6；核對日期：2026-10-17）
