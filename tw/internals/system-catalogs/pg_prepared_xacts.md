# 51.77. pg\_prepared\_xacts

The view `pg_prepared_xacts` displays information about transactions that are currently prepared for two-phase commit \(see [PREPARE TRANSACTION](https://www.postgresql.org/docs/13/sql-prepare-transaction.html) for details\).

`pg_prepared_xacts` contains one row per prepared transaction. An entry is removed when the transaction is committed or rolled back.

#### **Table 51.78. `pg_prepared_xacts` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>transaction</code>  <code>xid</code>
        </p>
        <p>Numeric transaction identifier of the prepared transaction</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>gid</code>  <code>text</code>
        </p>
        <p>Global transaction identifier that was assigned to the transaction</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>prepared</code>  <code>timestamptz</code>
        </p>
        <p>Time at which the transaction was prepared for commit</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>owner</code>  <code>name</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>rolname</code>)</p>
        <p>Name of the user that executed the transaction</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>database</code>  <code>name</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-database.html"><code>pg_database</code></a>.<code>datname</code>)</p>
        <p>Name of the database in which the transaction was executed</p>
      </td>
    </tr>
  </tbody>
</table>

When the `pg_prepared_xacts` view is accessed, the internal transaction manager data structures are momentarily locked, and a copy is made for the view to display. This ensures that the view produces a consistent set of results, while not blocking normal operations longer than necessary. Nonetheless there could be some impact on database performance if this view is frequently accessed.

