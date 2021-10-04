# 51.71. pg\_hba\_file\_rules

The view `pg_hba_file_rules` provides a summary of the contents of the client authentication configuration file, `pg_hba.conf`. A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the rule could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure. Note that this view reports on the _current_ contents of the file, not on what was last loaded by the server.

By default, the `pg_hba_file_rules` view can be read only by superusers.

#### **Table 51.72. `pg_hba_file_rules` Columns**

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
        <p><code>line_number</code>  <code>int4</code>
        </p>
        <p>Line number of this rule in <code>pg_hba.conf</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>type</code>  <code>text</code>
        </p>
        <p>Type of connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>database</code>  <code>text[]</code>
        </p>
        <p>List of database name(s) to which this rule applies</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>user_name</code>  <code>text[]</code>
        </p>
        <p>List of user and group name(s) to which this rule applies</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>address</code>  <code>text</code>
        </p>
        <p>Host name or IP address, or one of <code>all</code>, <code>samehost</code>,
          or <code>samenet</code>, or null for local connections</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>netmask</code>  <code>text</code>
        </p>
        <p>IP address mask, or null if not applicable</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>auth_method</code>  <code>text</code>
        </p>
        <p>Authentication method</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>options</code>  <code>text[]</code>
        </p>
        <p>Options specified for authentication method, if any</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>error</code>  <code>text</code>
        </p>
        <p>If not null, an error message indicating why this line could not be processed</p>
      </td>
    </tr>
  </tbody>
</table>

Usually, a row reflecting an incorrect entry will have values for only the `line_number` and `error` fields.

使用者身份驗證設定的相關資訊，請參閱[第 20 章](../../server-administration/client-authentication/)。

