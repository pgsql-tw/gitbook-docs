# 51.53. pg\_subscription\_rel

目錄 pg\_subscription\_rel 包含每個訂閱中每個複寫關係的狀態。這是多對多的關連情況。

在執行 CREATE SUBSCRIPTION 或 ALTER SUBSCRIPTION ... REFRESH PUBLICATION 之後才會更新，此目錄僅會包含已知的訂閱資料表。

#### **Table 51.53. `pg_subscription_rel` Columns**

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
        <p><code>srsubid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-subscription.html"><code>pg_subscription</code></a>.<code>oid</code>)</p>
        <p>Reference to subscription</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>srrelid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>oid</code>)</p>
        <p>Reference to relation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>srsubstate</code>  <code>char</code>
        </p>
        <p>State code: <code>i</code> = initialize, <code>d</code> = data is being copied, <code>s</code> =
          synchronized, <code>r</code> = ready (normal replication)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>srsublsn</code>  <code>pg_lsn</code>
        </p>
        <p>Remote LSN of the state change used for synchronization coordination when
          in <code>s</code> or <code>r</code> states, otherwise null</p>
      </td>
    </tr>
  </tbody>
</table>

