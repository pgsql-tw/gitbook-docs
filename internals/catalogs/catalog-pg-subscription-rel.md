<a id="CATALOG-PG-SUBSCRIPTION-REL"></a>

## 52.55. `pg_subscription_rel` [#](#catalog-pg-subscription-rel) <a href="#catalog-pg-subscription-rel" id="catalog-pg-subscription-rel"></a>

<a id="id-1.10.4.57.2"></a>

目錄 `pg_subscription_rel` 包含每個訂閱中每個被複寫關聯的狀態。這是多對多的對應。

此目錄只包含在執行 [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) 或
[`ALTER SUBSCRIPTION ... REFRESH
PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md) 之後，訂閱所知道的資料表。

<a id="id-1.10.4.57.5"></a>

**表 52.55. `pg_subscription_rel` 欄位**

<table border="1" class="table" summary="表 52.55. pg_subscription_rel 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srsubid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-subscription.md"><code class="structname">pg_subscription</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對訂閱的參照
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對關聯的參照
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srsubstate</code> <code class="type">char</code>
</p>
<p>
       狀態代碼：
       <code class="literal">i</code> = 初始化，
       <code class="literal">d</code> = 正在複製資料，
       <code class="literal">f</code> = 資料表複製完成，
       <code class="literal">s</code> = 已同步，
       <code class="literal">r</code> = 就緒（正常複寫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srsublsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       處於 <code class="literal">s</code> 或 <code class="literal">r</code> 狀態時，
       用於同步協調之狀態變更的遠端 LSN；否則為 null
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-subscription-rel.html)（原文版本：18.6；核對日期：2026-10-17）
