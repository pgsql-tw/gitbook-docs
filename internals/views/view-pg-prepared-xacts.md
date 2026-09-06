## 53.17. `pg_prepared_xacts` [#](#VIEW-PG-PREPARED-XACTS)

<a id="id-1.10.5.21.2"></a>

The view `pg_prepared_xacts` displays
information about transactions that are currently prepared for two-phase
commit (see [PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md) for details).

`pg_prepared_xacts` contains one row per prepared
transaction. An entry is removed when the transaction is committed or
rolled back.

<a id="id-1.10.5.21.5"></a>

**Table 53.17. `pg_prepared_xacts` Columns**

<table border="1" class="table" summary="pg_prepared_xacts Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">transaction</code> <code class="type">xid</code>
</p>
<p>
       Numeric transaction identifier of the prepared transaction
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">gid</code> <code class="type">text</code>
</p>
<p>
       Global transaction identifier that was assigned to the transaction
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prepared</code> <code class="type">timestamptz</code>
</p>
<p>
       Time at which the transaction was prepared for commit
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">owner</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of the user that executed the transaction
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">database</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">datname</code>)
      </p>
<p>
       Name of the database in which the transaction was executed
      </p></td></tr></tbody></table>

<br>

When the `pg_prepared_xacts` view is accessed, the
internal transaction manager data structures are momentarily locked, and
a copy is made for the view to display. This ensures that the
view produces a consistent set of results, while not blocking
normal operations longer than necessary. Nonetheless
there could be some impact on database performance if this view is
frequently accessed.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-prepared-xacts.html)（英文原文，待翻譯）
