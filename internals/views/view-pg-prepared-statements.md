<a id="VIEW-PG-PREPARED-STATEMENTS"></a>

## 53.16. `pg_prepared_statements` [#](#view-pg-prepared-statements) <a href="#view-pg-prepared-statements" id="view-pg-prepared-statements"></a>

<a id="id-1.10.5.20.2"></a>

檢視表 `pg_prepared_statements` 顯示目前工作階段中可用的所有預備陳述式。關於預備陳述式的更多資訊，請參閱 [PREPARE](../../reference/sql-commands/sql-prepare.md)。

`pg_prepared_statements` 中每個預備陳述式各有一筆資料列。建立新的預備陳述式時，會在此檢視表中加入資料列；釋放預備陳述式時（例如透過 [`DEALLOCATE`](../../reference/sql-commands/sql-deallocate.md) 命令），則會移除資料列。

<a id="id-1.10.5.20.5"></a>

**表 53.16. `pg_prepared_statements` 欄位**

<table border="1" class="table" summary="表 53.16. pg_prepared_statements 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       預備陳述式的識別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statement</code> <code class="type">text</code>
</p>
<p>
       用戶端為建立此預備陳述式所送出的查詢字串。對於透過 SQL 建立的預備陳述式，這是用戶端送出的 <code class="command">PREPARE</code> 陳述式。對於透過前端／後端協定建立的預備陳述式，這是預備陳述式本身的文字。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prepare_time</code> <code class="type">timestamptz</code>
</p>
<p>
       建立此預備陳述式的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_types</code> <code class="type">regtype[]</code>
</p>
<p>
       此預備陳述式預期的參數型別，以 <code class="type">regtype</code> 陣列的形式呈現。將 <code class="type">regtype</code> 值轉型為 <code class="type">oid</code>，即可取得此陣列中某個元素所對應的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_types</code> <code class="type">regtype[]</code>
</p>
<p>
       此預備陳述式所傳回之欄位的型別，以 <code class="type">regtype</code> 陣列的形式呈現。將 <code class="type">regtype</code> 值轉型為 <code class="type">oid</code>，即可取得此陣列中某個元素所對應的 OID。若預備陳述式不提供結果（例如 DML 陳述式），則此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">from_sql</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> 表示此預備陳述式是透過 <code class="command">PREPARE</code> SQL 命令建立的；<code class="literal">false</code> 表示此陳述式是透過前端／後端協定預備的
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">generic_plans</code> <code class="type">int8</code>
</p>
<p>
       選用通用計畫的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">custom_plans</code> <code class="type">int8</code>
</p>
<p>
       選用客製計畫的次數
      </p></td></tr></tbody></table>

<br>

檢視表 `pg_prepared_statements` 是唯讀的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-prepared-statements.html)（原文版本：18.6；核對日期：2026-10-09）
