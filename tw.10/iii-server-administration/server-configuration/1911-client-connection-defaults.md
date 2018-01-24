# 19.11. 用戶端連線預設參數[^1]

### 19.11.1. Statement Behavior

`search_path`\(`string`\)

這個參數表示，當一個物件（資料表、資料型別、函數等）以未指定 schema 的簡單名稱引用時，其搜尋的路徑順序。當不同 schema 中有相同名稱的物件時，將採用搜尋路徑中第一個找到的物件。不在搜尋路徑中的任何 schema 中物件，就只能透過使用限定名稱來指定其 schema 來引用。

search\_path 的內容必須是逗號分隔的 schema 名稱列表。任何非現有 schema 的名稱，或是使用者不具有 USAGE 權限的 schema，都將被忽略。

如果其中一個項目是特殊名稱 $user，則會使用 SESSION\_USER 回傳的名稱作為 schema 名稱，確認該 schema 存在且使用者具有 USAGE 權限。 （如果沒有權限，$user 將被忽略。）

系統目錄 pg\_catalog 一定會被搜尋，無論是否列在搜尋路徑中。如果列在搜尋路徑中了，那麼它將按照指定的順序被搜尋。 如果 pg\_catalog 不在搜尋路徑中，那麼它將會優先被搜尋。

同樣地，目前連線的臨時資料表的schema，pg\_temp\_nnn，如果它存在的話，就一定會被搜尋。它可以透過使用別名 pg\_temp 明確列在搜尋路徑中。如果沒有在搜尋路徑中列出的話，則優先搜尋（在 pg\_catalog 之前）。但是，臨時 schema 只是搜索關連（資料表、view，序列等）和資料型別名稱。不會搜尋函數或運算子名稱。

建立物件時沒有指定特定的 schema，那麼它們將被放置在 search\_path 中的第一個有效 schema 中。如果搜尋路徑為空，則會產生錯誤。

這個參數的預設值是 “$user”，public。此設定用來支援共享資料庫，沒有使用者具有私有 schema、所有共享使用 public、私人自有 schema ，以及以上情境的組合。其他的需求也可以透過更改預設的搜索路徑設置來達到，無論是全域或自有搜尋路徑。

搜尋路徑的目前內容可以使用 SQL 函數 current\_schemas 來檢查（詳見 [9.25 節](/ii-the-sql-language/functions-and-operators/925-system-information-functions.md)）。這與檢查 search\_path 的內容並不完全相同，因為 current\_schemas 表示 search\_path 中出現的項目是如何解析的。

有關 schema 處理的更多訊息，請參見第 [5.8 節](/ii-the-sql-language/data-definition/58-schemas.md)。

`row_security`\(`boolean`\)

此參數控制在資料列安全原則檢查時是否進行錯誤中斷。設定為 on 時，安全原則以正常方式運作。當設定為 off 時，除非查詢失敗，否則會至少符合一個原則。 預設值為 on。變更為 off 時，將會限制資料列的可視性，而可能造成不正確的結果；例如，pg\_dump 就會變更其預設值。此參數對於可以繞過每個安全原則的角色，也就是對具有 BYPASSRLS 屬性的超級使用者和角色都不會產生影響。

有關於資料列安全原則的更多訊息，請參閱 [CREATE POLICY](/vi-reference/i-sql-commands/create-policy.md)。

`default_tablespace`\(`string`\)

此參數指的是在 CREATE 指令未明確指定資料表空間（tablespace）時用於建立的資料庫物件（資料表和索引）的預設資料表空間。

該值可以是資料表空間的名稱，也可以是使用空字串表示為目前資料庫的預設資料表空間。如果該值與不符合任何現有的資料表空間名稱時，PostgreSQL 將自動使用目前資料庫的預設資料表空間。如果指定了非預設的資料表空間，則使用者必須具有 CREATE 權限，否則建立的操作將會失敗。

這個參數不用於臨時資料表；對於臨時資料表來說，會參考 temp\_tablespaces 參數。

建立資料庫時也不會使用這個參數。預設情況下，新的資料庫將複製的樣板資料庫，並繼承其資料表空間的設定。

有關於資料表空間的更多資訊，請參閱[第 22.6 節](/iii-server-administration/226-tablespaces.md)。

`temp_tablespaces`

\(

`string`

\)

This variable specifies tablespaces in which to create temporary objects \(temp tables and indexes on temp tables\) when a`CREATE`command does not explicitly specify a tablespace. Temporary files for purposes such as sorting large data sets are also created in these tablespaces.

The value is a list of names of tablespaces. When there is more than one name in the list,PostgreSQLchooses a random member of the list each time a temporary object is to be created; except that within a transaction, successively created temporary objects are placed in successive tablespaces from the list. If the selected element of the list is an empty string,PostgreSQLwill automatically use the default tablespace of the current database instead.

When`temp_tablespaces`is set interactively, specifying a nonexistent tablespace is an error, as is specifying a tablespace for which the user does not have`CREATE`privilege. However, when using a previously set value, nonexistent tablespaces are ignored, as are tablespaces for which the user lacks`CREATE`privilege. In particular, this rule applies when using a value set in`postgresql.conf`.

The default value is an empty string, which results in all temporary objects being created in the default tablespace of the current database.

See also[default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE).

`check_function_bodies`

\(

`boolean`

\)

This parameter is normally on. When set to`off`, it disables validation of the function body string during[CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html). Disabling validation avoids side effects of the validation process and avoids false positives due to problems such as forward references. Set this parameter to`off`before loading functions on behalf of other users;pg\_dumpdoes so automatically.

`default_transaction_isolation`

\(

`enum`

\)

Each SQL transaction has an isolation level, which can be either“read uncommitted”,“read committed”,“repeatable read”, or“serializable”. This parameter controls the default isolation level of each new transaction. The default is“read committed”.

Consult[Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html)and[SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)for more information.

`default_transaction_read_only`

\(

`boolean`

\)

A read-only SQL transaction cannot alter non-temporary tables. This parameter controls the default read-only status of each new transaction. The default is`off`\(read/write\).

Consult[SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)for more information.

`default_transaction_deferrable`

\(

`boolean`

\)

When running at the`serializable`isolation level, a deferrable read-only SQL transaction may be delayed before it is allowed to proceed. However, once it begins executing it does not incur any of the overhead required to ensure serializability; so serialization code will have no reason to force it to abort because of concurrent updates, making this option suitable for long-running read-only transactions.

This parameter controls the default deferrable status of each new transaction. It currently has no effect on read-write transactions or those operating at isolation levels lower than`serializable`. The default is`off`.

Consult[SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)for more information.

`session_replication_role`

\(

`enum`

\)

Controls firing of replication-related triggers and rules for the current session. Setting this variable requires superuser privilege and results in discarding any previously cached query plans. Possible values are`origin`\(the default\),`replica`and`local`. See[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)for more information.

`statement_timeout`

\(

`integer`

\)

Abort any statement that takes more than the specified number of milliseconds, starting from the time the command arrives at the server from the client. If`log_min_error_statement`is set to`ERROR`or lower, the statement that timed out will also be logged. A value of zero \(the default\) turns this off.

Setting`statement_timeout`in`postgresql.conf`is not recommended because it would affect all sessions.

`lock_timeout`

\(

`integer`

\)

Abort any statement that waits longer than the specified number of milliseconds while attempting to acquire a lock on a table, index, row, or other database object. The time limit applies separately to each lock acquisition attempt. The limit applies both to explicit locking requests \(such as`LOCK TABLE`, or`SELECT FOR UPDATE`without`NOWAIT`\) and to implicitly-acquired locks. If`log_min_error_statement`is set to`ERROR`or lower, the statement that timed out will be logged. A value of zero \(the default\) turns this off.

Unlike`statement_timeout`, this timeout can only occur while waiting for locks. Note that if`statement_timeout`is nonzero, it is rather pointless to set`lock_timeout`to the same or larger value, since the statement timeout would always trigger first.

Setting`lock_timeout`in`postgresql.conf`is not recommended because it would affect all sessions.

`idle_in_transaction_session_timeout`

\(

`integer`

\)

Terminate any session with an open transaction that has been idle for longer than the specified duration in milliseconds. This allows any locks held by that session to be released and the connection slot to be reused; it also allows tuples visible only to this transaction to be vacuumed. See[Section 24.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html)for more details about this.

The default value of 0 disables this feature.

`vacuum_freeze_table_age`

\(

`integer`

\)

`VACUUM`performs an aggressive scan if the table's`pg_class`.`relfrozenxid`field has reached the age specified by this setting. An aggressive scan differs from a regular`VACUUM`in that it visits every page that might contain unfrozen XIDs or MXIDs, not just those that might contain dead tuples. The default is 150 million transactions. Although users can set this value anywhere from zero to two billions,`VACUUM`will silently limit the effective value to 95% of[autovacuum\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE), so that a periodical manual`VACUUM`has a chance to run before an anti-wraparound autovacuum is launched for the table. For more information see[Section 24.1.5](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND).

`vacuum_freeze_min_age`

\(

`integer`

\)

Specifies the cutoff age \(in transactions\) that`VACUUM`should use to decide whether to freeze row versions while scanning a table. The default is 50 million transactions. Although users can set this value anywhere from zero to one billion,`VACUUM`will silently limit the effective value to half the value of[autovacuum\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE), so that there is not an unreasonably short time between forced autovacuums. For more information see[Section 24.1.5](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND).

`vacuum_multixact_freeze_table_age`

\(

`integer`

\)

`VACUUM`performs an aggressive scan if the table's`pg_class`.`relminmxid`field has reached the age specified by this setting. An aggressive scan differs from a regular`VACUUM`in that it visits every page that might contain unfrozen XIDs or MXIDs, not just those that might contain dead tuples. The default is 150 million multixacts. Although users can set this value anywhere from zero to two billions,`VACUUM`will silently limit the effective value to 95% of[autovacuum\_multixact\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE), so that a periodical manual`VACUUM`has a chance to run before an anti-wraparound is launched for the table. For more information see[Section 24.1.5.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND).

`vacuum_multixact_freeze_min_age`

\(

`integer`

\)

Specifies the cutoff age \(in multixacts\) that`VACUUM`should use to decide whether to replace multixact IDs with a newer transaction ID or multixact ID while scanning a table. The default is 5 million multixacts. Although users can set this value anywhere from zero to one billion,`VACUUM`will silently limit the effective value to half the value of[autovacuum\_multixact\_freeze\_max\_age](https://www.postgresql.org/docs/10/static/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE), so that there is not an unreasonably short time between forced autovacuums. For more information see[Section 24.1.5.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND).

`bytea_output`

\(

`enum`

\)

Sets the output format for values of type`bytea`. Valid values are`hex`\(the default\) and`escape`\(the traditional PostgreSQL format\). See[Section 8.4](https://www.postgresql.org/docs/10/static/datatype-binary.html)for more information. The`bytea`type always accepts both formats on input, regardless of this setting.

`xmlbinary`

\(

`enum`

\)

Sets how binary values are to be encoded in XML. This applies for example when`bytea`values are converted to XML by the functions`xmlelement`or`xmlforest`. Possible values are`base64`and`hex`, which are both defined in the XML Schema standard. The default is`base64`. For further information about XML-related functions, see[Section 9.14](https://www.postgresql.org/docs/10/static/functions-xml.html).

The actual choice here is mostly a matter of taste, constrained only by possible restrictions in client applications. Both methods support all possible values, although the hex encoding will be somewhat larger than the base64 encoding.

`xmloption`

\(

`enum`

\)

Sets whether`DOCUMENT`or`CONTENT`is implicit when converting between XML and character string values. See[Section 8.13](https://www.postgresql.org/docs/10/static/datatype-xml.html)for a description of this. Valid values are`DOCUMENT`and`CONTENT`. The default is`CONTENT`.

According to the SQL standard, the command to set this option is

```
SET XML OPTION { DOCUMENT | CONTENT };
```

This syntax is also available in PostgreSQL.

`gin_pending_list_limit`

\(

`integer`

\)

Sets the maximum size of the GIN pending list which is used when`fastupdate`is enabled. If the list grows larger than this maximum size, it is cleaned up by moving the entries in it to the main GIN data structure in bulk. The default is four megabytes \(`4MB`\). This setting can be overridden for individual GIN indexes by changing index storage parameters. See[Section 64.4.1](https://www.postgresql.org/docs/10/static/gin-implementation.html#GIN-FAST-UPDATE)and[Section 64.5](https://www.postgresql.org/docs/10/static/gin-tips.html)for more information.

### 19.11.2. Locale and Formatting

`DateStyle`

\(

`string`

\)

Sets the display format for date and time values, as well as the rules for interpreting ambiguous date input values. For historical reasons, this variable contains two independent components: the output format specification \(`ISO`,`Postgres`,`SQL`, or`German`\) and the input/output specification for year/month/day ordering \(`DMY`,`MDY`, or`YMD`\). These can be set separately or together. The keywords`Euro`and`European`are synonyms for`DMY`; the keywords`US`,`NonEuro`, and`NonEuropean`are synonyms for`MDY`. See[Section 8.5](https://www.postgresql.org/docs/10/static/datatype-datetime.html)for more information. The built-in default is`ISO, MDY`, butinitdbwill initialize the configuration file with a setting that corresponds to the behavior of the chosen`lc_time`locale.

`IntervalStyle`

\(

`enum`

\)

Sets the display format for interval values. The value`sql_standard`will produce output matchingSQLstandard interval literals. The value`postgres`\(which is the default\) will produce output matchingPostgreSQLreleases prior to 8.4 when the[DateStyle](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DATESTYLE)parameter was set to`ISO`. The value`postgres_verbose`will produce output matchingPostgreSQLreleases prior to 8.4 when the`DateStyle`parameter was set to non-`ISO`output. The value`iso_8601`will produce output matching the time interval“format with designators”defined in section 4.4.3.2 of ISO 8601.

The`IntervalStyle`parameter also affects the interpretation of ambiguous interval input. See[Section 8.5.4](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-INTERVAL-INPUT)for more information.

`TimeZone`

\(

`string`

\)

Sets the time zone for displaying and interpreting time stamps. The built-in default is`GMT`, but that is typically overridden in`postgresql.conf`;initdbwill install a setting there corresponding to its system environment. See[Section 8.5.3](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-TIMEZONES)for more information.

`timezone_abbreviations`

\(

`string`

\)

Sets the collection of time zone abbreviations that will be accepted by the server for datetime input. The default is`'Default'`, which is a collection that works in most of the world; there are also`'Australia'`and`'India'`, and other collections can be defined for a particular installation. See[Section B.3](https://www.postgresql.org/docs/10/static/datetime-config-files.html)for more information.

`extra_float_digits`

\(

`integer`

\)

This parameter adjusts the number of digits displayed for floating-point values, including`float4`,`float8`, and geometric data types. The parameter value is added to the standard number of digits \(`FLT_DIG`or`DBL_DIG`as appropriate\). The value can be set as high as 3, to include partially-significant digits; this is especially useful for dumping float data that needs to be restored exactly. Or it can be set negative to suppress unwanted digits. See also[Section 8.1.3](https://www.postgresql.org/docs/10/static/datatype-numeric.html#DATATYPE-FLOAT).

`client_encoding`

\(

`string`

\)

Sets the client-side encoding \(character set\). The default is to use the database encoding. The character sets supported by thePostgreSQLserver are described in[Section 23.3.1](https://www.postgresql.org/docs/10/static/multibyte.html#MULTIBYTE-CHARSET-SUPPORTED).

`lc_messages`

\(

`string`

\)

Sets the language in which messages are displayed. Acceptable values are system-dependent; see[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. If this variable is set to the empty string \(which is the default\) then the value is inherited from the execution environment of the server in a system-dependent way.

On some systems, this locale category does not exist. Setting this variable will still work, but there will be no effect. Also, there is a chance that no translated messages for the desired language exist. In that case you will continue to see the English messages.

Only superusers can change this setting, because it affects the messages sent to the server log as well as to the client, and an improper value might obscure the readability of the server logs.

`lc_monetary`

\(

`string`

\)

Sets the locale to use for formatting monetary amounts, for example with the`to_char`family of functions. Acceptable values are system-dependent; see[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. If this variable is set to the empty string \(which is the default\) then the value is inherited from the execution environment of the server in a system-dependent way.

`lc_numeric`

\(

`string`

\)

Sets the locale to use for formatting numbers, for example with the`to_char`family of functions. Acceptable values are system-dependent; see[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. If this variable is set to the empty string \(which is the default\) then the value is inherited from the execution environment of the server in a system-dependent way.

`lc_time`

\(

`string`

\)

Sets the locale to use for formatting dates and times, for example with the`to_char`family of functions. Acceptable values are system-dependent; see[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. If this variable is set to the empty string \(which is the default\) then the value is inherited from the execution environment of the server in a system-dependent way.

`default_text_search_config`

\(

`string`

\)

Selects the text search configuration that is used by those variants of the text search functions that do not have an explicit argument specifying the configuration. See[Chapter 12](https://www.postgresql.org/docs/10/static/textsearch.html)for further information. The built-in default is`pg_catalog.simple`, butinitdbwill initialize the configuration file with a setting that corresponds to the chosen`lc_ctype`locale, if a configuration matching that locale can be identified.

### 19.11.3. Shared Library Preloading

Several settings are available for preloading shared libraries into the server, in order to load additional functionality or achieve performance benefits. For example, a setting of`'$libdir/mylib'`would cause`mylib.so`\(or on some platforms,`mylib.sl`\) to be preloaded from the installation's standard library directory. The differences between the settings are when they take effect and what privileges are required to change them.

PostgreSQLprocedural language libraries can be preloaded in this way, typically by using the syntax`'$libdir/plXXX'`where`XXX`is`pgsql`,`perl`,`tcl`, or`python`.

Only shared libraries specifically intended to be used with PostgreSQL can be loaded this way. Every PostgreSQL-supported library has a“magic block”that is checked to guarantee compatibility. For this reason, non-PostgreSQL libraries cannot be loaded in this way. You might be able to use operating-system facilities such as`LD_PRELOAD`for that.

In general, refer to the documentation of a specific module for the recommended way to load that module.

`local_preload_libraries`

\(

`string`

\)

This variable specifies one or more shared libraries that are to be preloaded at connection start. It contains a comma-separated list of library names, where each name is interpreted as for the[LOAD](https://www.postgresql.org/docs/10/static/sql-load.html)command. Whitespace between entries is ignored; surround a library name with double quotes if you need to include whitespace or commas in the name. The parameter value only takes effect at the start of the connection. Subsequent changes have no effect. If a specified library is not found, the connection attempt will fail.

This option can be set by any user. Because of that, the libraries that can be loaded are restricted to those appearing in the`plugins`subdirectory of the installation's standard library directory. \(It is the database administrator's responsibility to ensure that only“safe”libraries are installed there.\) Entries in`local_preload_libraries`can specify this directory explicitly, for example`$libdir/plugins/mylib`, or just specify the library name —`mylib`would have the same effect as`$libdir/plugins/mylib`.

The intent of this feature is to allow unprivileged users to load debugging or performance-measurement libraries into specific sessions without requiring an explicit`LOAD`command. To that end, it would be typical to set this parameter using the`PGOPTIONS`environment variable on the client or by using`ALTER ROLE SET`.

However, unless a module is specifically designed to be used in this way by non-superusers, this is usually not the right setting to use. Look at[session\_preload\_libraries](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SESSION-PRELOAD-LIBRARIES)instead.

`session_preload_libraries`

\(

`string`

\)

This variable specifies one or more shared libraries that are to be preloaded at connection start. It contains a comma-separated list of library names, where each name is interpreted as for the[LOAD](https://www.postgresql.org/docs/10/static/sql-load.html)command. Whitespace between entries is ignored; surround a library name with double quotes if you need to include whitespace or commas in the name. The parameter value only takes effect at the start of the connection. Subsequent changes have no effect. If a specified library is not found, the connection attempt will fail. Only superusers can change this setting.

The intent of this feature is to allow debugging or performance-measurement libraries to be loaded into specific sessions without an explicit`LOAD`command being given. For example,[auto\_explain](https://www.postgresql.org/docs/10/static/auto-explain.html)could be enabled for all sessions under a given user name by setting this parameter with`ALTER ROLE SET`. Also, this parameter can be changed without restarting the server \(but changes only take effect when a new session is started\), so it is easier to add new modules this way, even if they should apply to all sessions.

Unlike[shared\_preload\_libraries](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES), there is no large performance advantage to loading a library at session start rather than when it is first used. There is some advantage, however, when connection pooling is used.

`shared_preload_libraries`

\(

`string`

\)

This variable specifies one or more shared libraries to be preloaded at server start. It contains a comma-separated list of library names, where each name is interpreted as for the[LOAD](https://www.postgresql.org/docs/10/static/sql-load.html)command. Whitespace between entries is ignored; surround a library name with double quotes if you need to include whitespace or commas in the name. This parameter can only be set at server start. If a specified library is not found, the server will fail to start.

Some libraries need to perform certain operations that can only take place at postmaster start, such as allocating shared memory, reserving light-weight locks, or starting background workers. Those libraries must be loaded at server start through this parameter. See the documentation of each library for details.

Other libraries can also be preloaded. By preloading a shared library, the library startup time is avoided when the library is first used. However, the time to start each new server process might increase slightly, even if that process never uses the library. So this parameter is recommended only for libraries that will be used in most sessions. Also, changing this parameter requires a server restart, so this is not the right setting to use for short-term debugging tasks, say. Use[session\_preload\_libraries](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SESSION-PRELOAD-LIBRARIES)for that instead.

### Note

On Windows hosts, preloading a library at server start will not reduce the time required to start each new server process; each server process will re-load all preload libraries. However,`shared_preload_libraries`is still useful on Windows hosts for libraries that need to perform operations at postmaster start time.

### 19.11.4. Other Defaults

`dynamic_library_path`

\(

`string`

\)

If a dynamically loadable module needs to be opened and the file name specified in the`CREATE FUNCTION`or`LOAD`command does not have a directory component \(i.e., the name does not contain a slash\), the system will search this path for the required file.

The value for`dynamic_library_path`must be a list of absolute directory paths separated by colons \(or semi-colons on Windows\). If a list element starts with the special string`$libdir`, the compiled-inPostgreSQLpackage library directory is substituted for`$libdir`; this is where the modules provided by the standardPostgreSQLdistribution are installed. \(Use`pg_config --pkglibdir`to find out the name of this directory.\) For example:

```
dynamic_library_path = '/usr/local/lib/postgresql:/home/my_project/lib:$libdir'
```

or, in a Windows environment:

```
dynamic_library_path = 'C:\tools\postgresql;H:\my_project\lib;$libdir'
```

The default value for this parameter is`'$libdir'`. If the value is set to an empty string, the automatic path search is turned off.

This parameter can be changed at run time by superusers, but a setting done that way will only persist until the end of the client connection, so this method should be reserved for development purposes. The recommended way to set this parameter is in the`postgresql.conf`configuration file.

`gin_fuzzy_search_limit`

\(

`integer`

\)

Soft upper limit of the size of the set returned by GIN index scans. For more information see[Section 64.5](https://www.postgresql.org/docs/10/static/gin-tips.html).

---

[^1]:  [PostgreSQL: Documentation: 10: 19.11. Client Connection Defaults](https://www.postgresql.org/docs/10/static/runtime-config-client.html)

