---
description: 版本：11
---

# 51.50. pg\_statistic\_ext

The catalog `pg_statistic_ext` holds definitions of extended planner statistics. Each row in this catalog corresponds to a _statistics object_ created with [CREATE STATISTICS](https://www.postgresql.org/docs/13/sql-createstatistics.html).

#### **Table 51.50. `pg_statistic_ext` Columns**

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
        <p><code>oid</code>  <code>oid</code>
        </p>
        <p>Row identifier</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxrelid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>Table containing the columns described by this object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxname</code>  <code>name</code>
        </p>
        <p>Name of the statistics object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxnamespace</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-namespace.html"><code>pg_namespace</code></a>.<code>oid</code>)</p>
        <p>The OID of the namespace that contains this statistics object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxowner</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>oid</code>)</p>
        <p>Owner of the statistics object</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxstattarget</code>  <code>int4</code>
        </p>
        <p><code>stxstattarget</code> controls the level of detail of statistics accumulated
          for this statistics object by <a href="https://www.postgresql.org/docs/13/sql-analyze.html">ANALYZE</a>.
          A zero value indicates that no statistics should be collected. A negative
          value says to use the maximum of the statistics targets of the referenced
          columns, if set, or the system default statistics target. Positive values
          of <code>stxstattarget</code> determine the target number of &#x201C;most
          common values&#x201D; to collect.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxkeys</code>  <code>int2vector</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-attribute.html"><code>pg_attribute</code></a>.<code>attnum</code>)</p>
        <p>An array of attribute numbers, indicating which table columns are covered
          by this statistics object; for example a value of <code>1 3</code> would
          mean that the first and the third table columns are covered</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stxkind</code>  <code>char[]</code>
        </p>
        <p>An array containing codes for the enabled statistic kinds; valid values
          are: <code>d</code> for n-distinct statistics, <code>f</code> for functional
          dependency statistics, and <code>m</code> for most common values (MCV) list
          statistics</p>
      </td>
    </tr>
  </tbody>
</table>

The `pg_statistic_ext` entry is filled in completely during `CREATE STATISTICS`, but the actual statistical values are not computed then. Subsequent `ANALYZE` commands compute the desired values and populate an entry in the [`pg_statistic_ext_data`](https://www.postgresql.org/docs/13/catalog-pg-statistic-ext-data.html) catalog.

