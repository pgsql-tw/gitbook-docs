<a id="CATALOG-PG-LARGEOBJECT"></a>

## 52.30. `pg_largeobject` [#](#CATALOG-PG-LARGEOBJECT)

<a id="id-1.10.4.32.2"></a>

目錄 `pg_largeobject` 存放構成「大型物件」的資料。大型物件以建立時所指派的 OID 識別。每個大型物件都會被拆分成多個區段，或稱「頁面」，其大小足以方便地以資料列的形式存放在 `pg_largeobject` 中。每頁的資料量定義為 `LOBLKSIZE`（目前為 `BLCKSZ/4`，通常是 2 kB）。

在 PostgreSQL 9.0 之前，大型物件沒有相關聯的權限結構。因此，`pg_largeobject` 可供公開讀取，並可用來取得系統中所有大型物件的 OID（及內容）。現在已不再如此；請使用 [`pg_largeobject_metadata`](catalog-pg-largeobject-metadata.md) 取得大型物件 OID 的清單。

<a id="id-1.10.4.32.5"></a>

**表 52.30. `pg_largeobject` 欄位**

<table border="1" class="table" summary="表 52.30. pg_largeobject 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">loid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-largeobject-metadata.md"><code class="structname">pg_largeobject_metadata</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此頁面之大型物件的識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pageno</code> <code class="type">int4</code>
</p>
<p>
       此頁面在其大型物件中的頁碼（從零起算）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data</code> <code class="type">bytea</code>
</p>
<p>
       存放在大型物件中的實際資料。其長度絕不會超過 <code class="symbol">LOBLKSIZE</code> 位元組，也可能較少。
      </p></td></tr></tbody></table>

<br>

`pg_largeobject` 的每個資料列存放大型物件中一個頁面的資料，從該物件內的位元組偏移量（`pageno * LOBLKSIZE`）開始。此實作允許稀疏儲存：頁面可能不存在，而且即使不是物件的最後一頁，也可能短於 `LOBLKSIZE` 位元組。大型物件內不存在的區域讀取時為零。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-largeobject.html)（原文版本：18.6；核對日期：2026-10-17）
