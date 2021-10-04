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
        <p>&#x6AA2;&#x8996;&#x8868;&#x7684;&#x7DB1;&#x8981;&#x540D;&#x7A31;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>viewname</code>  <code>name</code> (references <a href="pg_class.md"><code>pg_class</code></a>.<code>relname</code>)</p>
        <p>&#x6AA2;&#x8996;&#x8868;&#x540D;&#x7A31;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>viewowner</code>  <code>name</code> (references <a href="pg_authid.md"><code>pg_authid</code></a>.<code>rolname</code>)</p>
        <p>&#x6AA2;&#x8996;&#x5716;&#x7684;&#x64C1;&#x6709;&#x8005;&#x540D;&#x7A31;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>definition</code>  <code>text</code>
        </p>
        <p>&#x6AA2;&#x8996;&#x8868;&#x7684;&#x5B9A;&#x7FA9;&#xFF08;&#x91CD;&#x65B0;&#x5EFA;&#x69CB;&#x7684;
          SELECT &#x67E5;&#x8A62;&#xFF09;</p>
      </td>
    </tr>
  </tbody>
</table>

