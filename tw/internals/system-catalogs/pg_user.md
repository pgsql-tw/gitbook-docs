# 51.93. pg\_user

The view `pg_user` provides access to information about database users. This is simply a publicly readable view of [`pg_shadow`](https://www.postgresql.org/docs/13/view-pg-shadow.html) that blanks out the password field.

#### **Table 51.94. `pg_user` Columns**

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
        <p><code>usename</code>  <code>name</code>
        </p>
        <p>User name</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usesysid</code>  <code>oid</code>
        </p>
        <p>ID of this user</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usecreatedb</code>  <code>bool</code>
        </p>
        <p>User can create databases</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usesuper</code>  <code>bool</code>
        </p>
        <p>User is a superuser</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>userepl</code>  <code>bool</code>
        </p>
        <p>User can initiate streaming replication and put the system in and out
          of backup mode.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usebypassrls</code>  <code>bool</code>
        </p>
        <p>User bypasses every row level security policy, see <a href="https://www.postgresql.org/docs/13/ddl-rowsecurity.html">Section 5.8</a> for
          more information.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>passwd</code>  <code>text</code>
        </p>
        <p>Not the password (always reads as <code>********</code>)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>valuntil</code>  <code>timestamptz</code>
        </p>
        <p>Password expiry time (only used for password authentication)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>useconfig</code>  <code>text[]</code>
        </p>
        <p>Session defaults for run-time configuration variables</p>
      </td>
    </tr>
  </tbody>
</table>

