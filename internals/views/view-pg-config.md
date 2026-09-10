## 53.6. `pg_config` [#](#VIEW-PG-CONFIG)

<a id="id-1.10.5.10.2"></a>

檢視表 `pg_config` 說明目前已安裝 PostgreSQL 版本的編譯時期設定參數。舉例來說，需要與 PostgreSQL 介接的軟體套件可使用它，以利尋找所需的標頭檔與程式庫。它提供與 [pg_config](../../reference/reference-client/app-pgconfig.md) PostgreSQL 用戶端應用程式相同的基本資訊。

預設情況下，只有超級使用者可讀取 `pg_config` 檢視表。

<a id="id-1.10.5.10.5"></a>

**表 53.6. `pg_config` 欄位**

<table border="1" class="table" summary="pg_config Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       參數名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setting</code> <code class="type">text</code>
</p>
<p>
       參數值
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-config.html)（原文版本：18.6；核對日期：2026-09-11）
