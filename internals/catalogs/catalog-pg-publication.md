<a id="CATALOG-PG-PUBLICATION"></a>

## 52.40. `pg_publication` [#](#CATALOG-PG-PUBLICATION)

<a id="id-1.10.4.42.2"></a>

系統目錄 `pg_publication` 包含資料庫中建立的所有發佈。關於發佈的更多資訊，請參閱[第 29.1 節](../../server-administration/logical-replication/logical-replication-publication.md)。

<a id="id-1.10.4.42.4"></a>

**表 52.40. `pg_publication` 欄位**

<table border="1" class="table" summary="表 52.40. pg_publication 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">pubname</code> <code class="type">name</code>
</p>
<p>
       發佈的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       發佈的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">puballtables</code> <code class="type">bool</code>
</p>
<p>
       若為真，此發佈會自動包含資料庫中的所有資料表，包括未來將建立的任何資料表。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubinsert</code> <code class="type">bool</code>
</p>
<p>
       若為真，發佈中資料表的 <a class="xref" href="../../reference/sql-commands/sql-insert.md"><span class="refentrytitle">INSERT</span></a> 操作會被複寫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubupdate</code> <code class="type">bool</code>
</p>
<p>
       若為真，發佈中資料表的 <a class="xref" href="../../reference/sql-commands/sql-update.md"><span class="refentrytitle">UPDATE</span></a> 操作會被複寫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubdelete</code> <code class="type">bool</code>
</p>
<p>
       若為真，發佈中資料表的 <a class="xref" href="../../reference/sql-commands/sql-delete.md"><span class="refentrytitle">DELETE</span></a> 操作會被複寫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubtruncate</code> <code class="type">bool</code>
</p>
<p>
       若為真，發佈中資料表的 <a class="xref" href="../../reference/sql-commands/sql-truncate.md"><span class="refentrytitle">TRUNCATE</span></a> 操作會被複寫。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubviaroot</code> <code class="type">bool</code>
</p>
<p>
       若為真，對葉分割區的操作會以發佈中所提及、其最上層分割資料表祖先的識別與綱要進行複寫，而不是使用葉分割區自身的識別與綱要。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pubgencols</code> <code class="type">char</code>
</p>
<p>
       控制在沒有發佈欄位清單時，如何處理產生欄位的複寫：<code class="literal">n</code> = 不應複寫與此發佈相關聯之資料表中的產生欄位，<code class="literal">s</code> = 應複寫與此發佈相關聯之資料表中的儲存式產生欄位。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-publication.html)（原文版本：18.6；核對日期：2026-10-17）
