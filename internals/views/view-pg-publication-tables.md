<a id="VIEW-PG-PUBLICATION-TABLES"></a>

## 53.18. `pg_publication_tables` [#](#VIEW-PG-PUBLICATION-TABLES)

<a id="id-1.10.5.22.2"></a>

檢視表 `pg_publication_tables` 提供發佈與其所包含之資料表的資訊之間的對應資訊。與底層系統目錄 [`pg_publication_rel`](../catalogs/catalog-pg-publication-rel.md) 不同，此檢視表會展開定義為 [`FOR ALL TABLES`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 與 [`FOR TABLES IN SCHEMA`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA) 的發佈，因此對於這類發佈，每個符合條件的資料表都會有一筆資料列。

<a id="id-1.10.5.22.4"></a>

**表 53.18. `pg_publication_tables` 欄位**

<table border="1" class="table" summary="表 53.18. pg_publication_tables 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">pubname</code>）
      </p>
<p>
       發佈名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含資料表之綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnames</code> <code class="type">name[]</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>）
      </p>
<p>
       發佈中所包含之資料表欄位的名稱。當使用者未為該資料表指定欄位清單時，此欄位包含該資料表的所有欄位。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rowfilter</code> <code class="type">text</code>
</p>
<p>
       該資料表在發佈中之限定條件的運算式
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-publication-tables.html)（原文版本：18.6；核對日期：2026-10-10）
