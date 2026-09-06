## 53.7. `pg_cursors` [#](#VIEW-PG-CURSORS)

<a id="id-1.10.5.11.2"></a>

The `pg_cursors` view lists the cursors that
are currently available. Cursors can be defined in several ways:

* via the [`DECLARE`](../../reference/sql-commands/sql-declare.md)
  statement in SQL
* via the Bind message in the frontend/backend protocol, as
  described in [Section 54.2.3](../protocol/protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)
* via the Server Programming Interface (SPI), as described in
  [Section 45.1](../../server-programming/spi/spi-interface.md)

The `pg_cursors` view displays cursors
created by any of these means. Cursors only exist for the duration
of the transaction that defines them, unless they have been
declared `WITH HOLD`. Therefore non-holdable
cursors are only present in the view until the end of their
creating transaction.

### Note

Cursors are used internally to implement some of the components
of PostgreSQL, such as procedural languages.
Therefore, the `pg_cursors` view might include cursors
that have not been explicitly created by the user.

<a id="id-1.10.5.11.4"></a>

**Table 53.7. `pg_cursors` Columns**

<table border="1" class="table" summary="pg_cursors Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       The name of the cursor
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statement</code> <code class="type">text</code>
</p>
<p>
       The verbatim query string submitted to declare this cursor
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_holdable</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> if the cursor is holdable (that is, it
       can be accessed after the transaction that declared the cursor
       has committed); <code class="literal">false</code> otherwise
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_binary</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> if the cursor was declared
       <code class="literal">BINARY</code>; <code class="literal">false</code>
       otherwise
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_scrollable</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> if the cursor is scrollable (that is, it
       allows rows to be retrieved in a nonsequential manner);
       <code class="literal">false</code> otherwise
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">creation_time</code> <code class="type">timestamptz</code>
</p>
<p>
       The time at which the cursor was declared
      </p></td></tr></tbody></table>

<br>

The `pg_cursors` view is read-only.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-cursors.html)（英文原文，待翻譯）
