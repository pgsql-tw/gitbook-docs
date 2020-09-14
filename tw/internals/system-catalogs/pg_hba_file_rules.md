# 51.72. pg\_hba\_file\_rules

The view `pg_hba_file_rules` provides a summary of the contents of the client authentication configuration file, `pg_hba.conf`. A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the rule could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure. Note that this view reports on the _current_ contents of the file, not on what was last loaded by the server.

By default, the `pg_hba_file_rules` view can be read only by superusers.

#### **Table 51.73. `pg_hba_file_rules` Columns**

| Name | Type | Description |
| :--- | :--- | :--- |
| `line_number` | `integer` | Line number of this rule in `pg_hba.conf` |
| `type` | `text` | Type of connection |
| `database` | `text[]` | List of database name\(s\) to which this rule applies |
| `user_name` | `text[]` | List of user and group name\(s\) to which this rule applies |
| `address` | `text` | Host name or IP address, or one of `all`, `samehost`, or `samenet`, or null for local connections |
| `netmask` | `text` | IP address mask, or null if not applicable |
| `auth_method` | `text` | Authentication method |
| `options` | `text[]` | Options specified for authentication method, if any |
| `error` | `text` | If not null, an error message indicating why this line could not be processed |

Usually, a row reflecting an incorrect entry will have values for only the `line_number` and `error` fields.

有關用戶端身份驗證設定的更多資訊，請參閱[第 20 章](../../server-administration/client-authentication/)。

