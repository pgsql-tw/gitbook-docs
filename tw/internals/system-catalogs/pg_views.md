# 51.95. pg\_views

檢視表 pg\_views 提供對資料庫中每個檢視表的詳細資訊。

#### **Table 51.96. `pg_views` Columns**

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
        <p><code>schemaname</code>  <code>name</code> (references <a href="pg_namespace.md"><code>pg_namespace</code></a>.<code>nspname</code>)</p>
        <p>Name of schema containing view</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>viewname</code>  <code>name</code> (references <a href="pg_class.md"><code>pg_class</code></a>.<code>relname</code>)</p>
        <p>Name of view</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>viewowner</code>  <code>name</code> (references <a href="pg_authid.md"><code>pg_authid</code></a>.<code>rolname</code>)</p>
        <p>Name of view&apos;s owner</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>definition</code>  <code>text</code>
        </p>
        <p>View definition (a reconstructed <code>SELECT</code> query)</p>
      </td>
    </tr>
  </tbody>
</table>

