---
description: 版本：11
---

# 51.32. pg\_namespace

The catalog `pg_namespace` stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.

#### **Table 51.32. `pg_namespace` Columns**

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
        <p><code>nspname</code>  <code>name</code>
        </p>
        <p>Name of the namespace</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>nspowner</code>  <code>oid</code> (references <a href="pg_authid.md"><code>pg_authid</code></a>.<code>oid</code>)</p>
        <p>Owner of the namespace</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>nspacl</code>  <code>aclitem[]</code>
        </p>
        <p>&#x5B58;&#x53D6;&#x6B0A;&#x9650;&#xFF1B; &#x8A73;&#x898B; <a href="../../the-sql-language/ddl/privileges.md">5.7 &#x7BC0;</a>
        </p>
      </td>
    </tr>
  </tbody>
</table>

