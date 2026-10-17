<a id="CATALOG-PG-SHSECLABEL"></a>

## 52.50. `pg_shseclabel` [#](#CATALOG-PG-SHSECLABEL)

<a id="id-1.10.4.52.2"></a>

系統目錄 `pg_shseclabel` 存放共享資料庫物件上的安全標籤。安全標籤可以使用 [`SECURITY LABEL`](../../reference/sql-commands/sql-security-label.md) 命令操作。若要以更簡便的方式檢視安全標籤，請參閱[第 53.23 節](../views/view-pg-seclabels.md)。

另請參閱 [`pg_seclabel`](catalog-pg-seclabel.md)，它對涉及單一資料庫內物件的安全標籤執行類似的功能。

與大多數系統目錄不同，`pg_shseclabel` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_shseclabel`，而不是每個資料庫各一份。

<a id="id-1.10.4.52.6"></a>

**表 52.50. `pg_shseclabel` 欄位**

<table border="1" class="table" summary="表 52.50. pg_shseclabel 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-shseclabel.html)（原文版本：18.6；核對日期：2026-10-17）
