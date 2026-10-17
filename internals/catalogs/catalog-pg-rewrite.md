<a id="CATALOG-PG-REWRITE"></a>

## 52.45. `pg_rewrite` [#](#CATALOG-PG-REWRITE)

<a id="id-1.10.4.47.2"></a>

系統目錄 `pg_rewrite` 存放資料表與檢視表的重寫規則。

<a id="id-1.10.4.47.4"></a>

**表 52.45. `pg_rewrite` 欄位**

<table border="1" class="table" summary="表 52.45. pg_rewrite 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">rulename</code> <code class="type">name</code>
</p>
<p>
       規則名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_class</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此規則所屬的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_type</code> <code class="type">char</code>
</p>
<p>
       此規則所適用的事件類型：1 = <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a>、2 = <a class="xref" href="../../reference/sql-commands/sql-update.md"><span class="refentrytitle">UPDATE</span></a>、3 = <a class="xref" href="../../reference/sql-commands/sql-insert.md"><span class="refentrytitle">INSERT</span></a>、4 = <a class="xref" href="../../reference/sql-commands/sql-delete.md"><span class="refentrytitle">DELETE</span></a>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_enabled</code> <code class="type">char</code>
</p>
<p>
       控制規則在哪些 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> 模式下觸發。<code class="literal">O</code> = 規則在 <span class="quote">“<span class="quote">origin</span>”</span> 與 <span class="quote">“<span class="quote">local</span>”</span> 模式下觸發，<code class="literal">D</code> = 規則已停用，<code class="literal">R</code> = 規則在 <span class="quote">“<span class="quote">replica</span>”</span> 模式下觸發，<code class="literal">A</code> = 規則一律觸發。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_instead</code> <code class="type">bool</code>
</p>
<p>
       若此規則為 <code class="literal">INSTEAD</code> 規則，則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_qual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       規則限定條件的運算式樹（以 <code class="function">nodeToString()</code> 表示法的形式）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ev_action</code> <code class="type">pg_node_tree</code>
</p>
<p>
       規則動作的查詢樹（以 <code class="function">nodeToString()</code> 表示法的形式）
      </p></td></tr></tbody></table>

<br>

### 注意

若資料表在此系統目錄中有任何規則，`pg_class.relhasrules` 必須為真。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-rewrite.html)（原文版本：18.6；核對日期：2026-10-17）
