<a id="CATALOG-PG-REPLICATION-ORIGIN"></a>

## 52.44. `pg_replication_origin` [#](#CATALOG-PG-REPLICATION-ORIGIN)

<a id="id-1.10.4.46.2"></a>

系統目錄 `pg_replication_origin` 包含所有已建立的複寫來源。關於複寫來源的更多資訊，請參閱[第 48 章](../../server-programming/replication-origins/README.md)。

與大多數系統目錄不同，`pg_replication_origin` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_replication_origin`，而不是每個資料庫各一份。

<a id="id-1.10.4.46.5"></a>

**表 52.44. `pg_replication_origin` 欄位**

<table border="1" class="table" summary="表 52.44. pg_replication_origin 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">roident</code> <code class="type">oid</code>
</p>
<p>
       複寫來源在整個叢集中唯一的識別碼。絕不應流出本系統。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">roname</code> <code class="type">text</code>
</p>
<p>
       複寫來源對外使用、由使用者定義的名稱。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-replication-origin.html)（原文版本：18.6；核對日期：2026-10-17）
