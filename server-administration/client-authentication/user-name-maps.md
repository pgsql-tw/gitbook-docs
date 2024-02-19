# 21.2. User Name Maps

When using an external authentication system such as Ident or GSSAPI, the name of the operating system user that initiated the connection might not be the same as the database user (role) that is to be used. In this case, a user name map can be applied to map the operating system user name to a database user. To use user name mapping, specify `map`=_`map-name`_ in the options field in `pg_hba.conf`. This option is supported for all authentication methods that receive external user names. Since different mappings might be needed for different connections, the name of the map to be used is specified in the _`map-name`_ parameter in `pg_hba.conf` to indicate which map to use for each individual connection.

使用者名映射在標識映射檔中定義，預設情況下名為 pg\_ident.conf，存儲在群集的數據目錄中。（但是，可以將映射檔放置在其他位置;請參閱 [ident\_file](../server-configuration/file-locations.md#ident\_file-string) 配置參數。識別對應檔包含一般形式的行：

```
map-name system-username database-username
```

Comments, whitespace and line continuations are handled in the same way as in `pg_hba.conf`. The _`map-name`_ is an arbitrary name that will be used to refer to this mapping in `pg_hba.conf`. The other two fields specify an operating system user name and a matching database user name. The same _`map-name`_ can be used repeatedly to specify multiple user-mappings within a single map.

There is no restriction regarding how many database users a given operating system user can correspond to, nor vice versa. Thus, entries in a map should be thought of as meaning “this operating system user is allowed to connect as this database user”, rather than implying that they are equivalent. The connection will be allowed if there is any map entry that pairs the user name obtained from the external authentication system with the database user name that the user has requested to connect as.

If the _`system-username`_ field starts with a slash (`/`), the remainder of the field is treated as a regular expression. (See [Section 9.7.3.1](https://www.postgresql.org/docs/current/functions-matching.html#POSIX-SYNTAX-DETAILS) for details of PostgreSQL's regular expression syntax.) The regular expression can include a single capture, or parenthesized subexpression, which can then be referenced in the _`database-username`_ field as `\1` (backslash-one). This allows the mapping of multiple user names in a single line, which is particularly useful for simple syntax substitutions. For example, these entries

```
mymap   /^(.*)@mydomain\.com$      \1
mymap   /^(.*)@otherdomain\.com$   guest
```

will remove the domain part for users with system user names that end with `@mydomain.com`, and allow any user whose system name ends with `@otherdomain.com` to log in as `guest`.

{% hint style="info" %}
#### Tip

請記住，預設情況下，正規表示式只能匹配字串的一部分。通常明智的做法是使用 ^ 和 $（如上面的範例所示）強制匹配到完整的系統使用者名稱。
{% endhint %}

The `pg_ident.conf` file is read on start-up and when the main server process receives a SIGHUP signal. If you edit the file on an active system, you will need to signal the postmaster (using `pg_ctl reload`, calling the SQL function `pg_reload_conf()`, or using `kill -HUP`) to make it re-read the file.

The system view [`pg_ident_file_mappings`](https://www.postgresql.org/docs/current/view-pg-ident-file-mappings.html) can be helpful for pre-testing changes to the `pg_ident.conf` file, or for diagnosing problems if loading of the file did not have the desired effects. Rows in the view with non-null `error` fields indicate problems in the corresponding lines of the file.

A `pg_ident.conf` file that could be used in conjunction with the `pg_hba.conf` file in [Example 21.1](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html#EXAMPLE-PG-HBA.CONF) is shown in [Example 21.2](https://www.postgresql.org/docs/current/auth-username-maps.html#EXAMPLE-PG-IDENT.CONF). In this example, anyone logged in to a machine on the 192.168 network that does not have the operating system user name `bryanh`, `ann`, or `robert` would not be granted access. Unix user `robert` would only be allowed access when he tries to connect as PostgreSQL user `bob`, not as `robert` or anyone else. `ann` would only be allowed to connect as `ann`. User `bryanh` would be allowed to connect as either `bryanh` or as `guest1`.

#### **Example 21.2. An Example `pg_ident.conf` File**

```
# MAPNAME       SYSTEM-USERNAME         PG-USERNAME

omicron         bryanh                  bryanh
omicron         ann                     ann
# bob has user name robert on these machines
omicron         robert                  bob
# bryanh can also connect as guest1
omicron         bryanh                  guest1
```
