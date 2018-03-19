# 9.25. 系統資訊函數[^1]

[Table 9.60](#table-960-session-information-functions) 列出了一些取得連線和系統資訊的函數。

除了本節中列出的功能之外，還有一些與統計系統相關的功能也提供系統訊息。有關更多訊息，請參閱[第 28.2.2 節](/iii-server-administration/monitoring-database-activity/282-the-statistics-collector.md)。

##### **Table 9.60. 連線資訊函數**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `current_catalog` | `name` | 目前資料庫的名稱（在 SQL 標準中稱為「catalog」） |
| `current_database()` | `name` | 目前資料庫的名稱 |
| `current_query()` | `text` | 正在執行的查詢的文字內容（由用戶端送出的）（可能包含多個語句） |
| `current_role` | `name` | 等同於 current\_user |
| `current_schema`\[\(\)\] | `name` | 目前 schema 的名稱 |
| `current_schemas(boolean)` | `name[]` | 搜尋路徑中的 schema 名稱，選擇性包含隱含的 schema |
| `current_user` | `name` | 目前執行查詢的使用者名稱 |
| `inet_client_addr()` | `inet` | 遠端連線的位址 |
| `inet_client_port()` | `int` | 遠端連線的連接埠 |
| `inet_server_addr()` | `inet` | 本機連線的位址 |
| `inet_server_port()` | `int` | 本機連線的連接埠 |
| `pg_backend_pid()` | `int` | 目前伺服連線服務的 Process ID |
| `pg_blocking_pids(int)` | `int[]` | 正在防止指定的伺服器 Process ID 取得鎖定權限的 Process ID |
| `pg_conf_load_time()` | `timestamp with time zone` | 載入時間的設定 |
| `pg_current_logfile([text])` | `text` | 主要日誌的檔案名稱，或者登記的日誌收集器目前正在使用的請求格式 |
| `pg_my_temp_schema()` | `oid` | 目前連線的暫時 schema 的 OID，如果沒有則為 0 |
| `pg_is_other_temp_schema(oid)` | `boolean` | 這個 schema 是另一個連線的暫時 schema 嗎？ |
| `pg_listening_channels()` | `setof text` | 連線目前正在監聽的頻道（channel）名稱 |
| `pg_notification_queue_usage()` | `double` | 目前佔用的非同步通知佇列的使用率（0-1） |
| `pg_postmaster_start_time()` | `timestamp with time zone` | 伺服器的啟動時間 |
| `pg_safe_snapshot_blocking_pids(int)` | `int[]` | 阻擋指定的伺服器 Process ID 取得安全快照的 Process ID |
|  | `pg_trigger_depth()` | `intPostgreSQL 觸發器的目前巢狀等級（如果未從觸發器內部直接或間接呼叫，則為 0）` |
| `session_user` | `name` | 連線中的使用者名稱 |
| `user` | `name` | 等同於 current\_user |
| `version()` | `text` | PostgreSQL 版本訊息。另請參閱 [server\_version\_num](/iii-server-administration/server-configuration/1915-preset-options.md) 以獲得機器可讀版本內容。 |

> ### 注意
>
> `current_catalog`,`current_role`,`current_schema`,`current_user`,`session_user`, 和`user 在 SQL 中有特殊的語法狀態：他們必須以沒有括號的方式呼叫。（在PostgreSQL中，括號可以選擇性地與 current_schema 一起使用，但不能與其他的函數一起使用。）`

session\_user 通常是發起目前資料庫連線的使用者；但超級使用者可以利用 [SET SESSION AUTHORIZATION](/vi-reference/i-sql-commands/set-session-authorization.md) 更改此設定。current\_user 是適用於權限檢查的使用者識別方式。通常它與連線中的使用者相同，但也可以使用 [SET ROLE](/vi-reference/i-sql-commands/set-role.md) 進行更改。在使用 SECURITY DEFINER 屬性執行功能期間，它也會發生變化。用 Unix 的說法，連線使用者是「real user」，而目前使用者是「effective user」。current\_role 和 user 是 current\_user 的同義詞。 （標準 SQL 區分了 current\_role 和 current\_user，但 PostgreSQL 並沒有，因為它將使用者和角色統合為一種實體。）

current\_schema 回傳搜尋路徑中的第一個 schema 名稱（如果搜尋路徑為空值，則回傳空值）。這將會用於在沒有指定 schema 的情況下建立的任何資料表或其他物件的 schema。current\_schemas（boolean）回傳目前搜尋路徑中所有 schema 名稱的陣列。 布林選項表示隱含的系統 schema（如pg\_catalog）是否包含在回傳的搜尋路徑中。

> ### 注意
>
> 搜尋路徑可以在執行中時更改。該指令是：
>
> ```
> SET search_path TO schema [, schema, ...]
> ```

inet\_client\_addr 回傳目前用戶端的 IP 位址、inet\_client\_port 回傳連接埠、inet\_server\_addr 回傳伺服器接受目前連線的 IP 位址、inet\_server\_port 回傳連接埠。 如果目前連線是透過 Unix-domain socker，那這些函數都會回傳 NULL。

pg\_blocking\_pids 會回傳連線中阻擋指定 Process ID 的 Process ID 陣列，如果沒有這樣的 Process 或未被阻擋，則回傳一個空的陣列。如果一個伺服器的 Process 阻擋了其他 Process 的鎖定請求（Hard block），或者正在與其他請求鎖定的 Process 在等待佇列之前即發生衝突（Soft block）。在使用平行查詢時，即使實際的 lock 被子程序持有或等待，結果也都會列出用戶端可見的 Process ID（即 pg\_backend\_pid 結果）。因此，結果中可能會有重複的 PID。還要注意的是，當準備好的交易事務持有衝突的鎖定時，它將在此函數的結果中以 zero process ID 表示。頻繁呼叫此函數可能會對資料庫效能產生一些影響，因為它需要短時間獨佔鎖定管理器的共享狀態。

pg\_conf\_load\_time 回傳上次載入伺服器設定檔的時間戳記，帶有時區記錄。 （如果目前的連線仍然存在的話，這將是連線本身重新讀取設定檔的時間，因此在不同的連線中讀取會有所不同，否則會是 postmaster 重新讀取設定檔的時間。）

pg\_current\_logfile 以 text 型別回傳日誌收集器目前使用的日誌檔的路徑。該路徑包括log\_directory目錄和日誌檔名稱。日誌收集必須啟用或回傳值為 NULL。當存在多個日誌檔（每個檔案格式不同）時，呼叫不帶參數的 pg\_current\_log 將回傳具有在有序列表中找到的第一個格式的檔案路徑：stderr，csvlog。 沒有任何日誌檔具有這些格式時，將回傳 NULL。 要以文字形式請求特定的檔案格式，請將 csvlog 或 stderr 作為參數。當請求的日誌格式不是設定的 [log\_destination](/iii-server-administration/server-configuration/198-error-reporting-and-logging.md) 時，回傳值為 NULL。pg\_current\_log 檔案反映了 current\_logfiles 檔案的內容。

pg\_my\_temp\_schema 回傳目前連線臨時 schema 的 OID，如果沒有的話（因為沒有建立任何臨時資料表），則回傳零。pg\_is\_other\_temp\_schema 如果給予的 OID 是另一個連線的臨時 schema OID，則回傳 true。 （舉個例子，這可以用於從列表顯示中排除其他連線的臨時資料表。）

pg\_listening\_channels 回傳目前連線正在監聽的一組非同步監聽通道的名稱。 pg\_notification\_queue\_usage 回傳目前正在等待處理的監聽佔用的總可用空間的比率，範圍為 0-1。 有關更多訊息，請參閱 [LISTEN](/vi-reference/i-sql-commands/listen.md) 和 [NOTIFY](/vi-reference/i-sql-commands/notify.md)。

pg\_postmaster\_start\_time 回傳伺服器啟動時帶有時區的時間戳記。

pg\_safe\_snapshot\_blocking\_pids 回傳阻擋具有指定 Process ID的取得安全快照的連線 Process ID 陣列，如果沒有這樣的 Process 或未有阻擋的情況，則回傳一個空陣列。執行 SERIALIZABLE 交易事務的連線會阻止另一個 SERIALIZABLE READ ONLY DEFERRABLE 交易事務取得快照，直到後者確定避免使用任何謂 predicate lock 是安全的。有關可序列化 SERIALIZABLE 和可延期 DEFERRABLE 交易的更多訊息，請參閱[第 13.2.3 節](/ii-the-sql-language/concurrency-control/132-transaction-isolation.md)。頻繁呼叫此函數可能會對資料庫效能產生一些影響，因為它需要短時間詢問 predicate lock 管理器的共享狀態。

version 回傳一個說明 PostgreSQL 伺服器版本的字串。你也可以從 [server\_version](/iii-server-administration/server-configuration/1915-preset-options.md) 或適於機器讀取的 [server\_version\_num](/iii-server-administration/server-configuration/1915-preset-options.md) 取得此信息。軟體研發人員應該使用 server\_version\_num（自8.2起可用）或 [PQserverVersion](/iv-client-interfaces/332-connection-status-functions.md)，而不用需要解析文字的版本。

[Table 9.61](#table-961-access-privilege-inquiry-functions) 列出了允許使用者以程式控制的方式查詢資料庫物件存取權限的函數。有關權限的更多訊息，請參閱[第 5.6 節](/ii-the-sql-language/data-definition/56-privileges.md)。

##### **Table 9.61. 存取權限查詢功能**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `has_any_column_privilege`\(`user`,`table`,`privilege`\) | `boolean` | 使用者是否有任何資料表欄位的權限？ |
| `has_any_column_privilege`\(`table`,`privilege`\) | `boolean` | 目前使用者是否有任何資料表欄位的權限？ |
| `has_column_privilege`\(`user`,`table`,`column`,`privilege`\) | `boolean` | 使用者是否有該欄位的權限？ |
| `has_column_privilege`\(`table`,`column`,`privilege`\) | `boolean` | 目前用戶是否具有該欄位的權限？ |
| `has_database_privilege`\(`user`,`database`,`privilege`\) | `boolean` | 使用者對該資料庫是否有權限？ |
| `has_database_privilege`\(`database`,`privilege`\) | `boolean` | 目前用戶是否具有該資料庫的權限？ |
| `has_foreign_data_wrapper_privilege`\(`user`,`fdw`,`privilege`\) | `boolean` | 使用者是否擁有該 FDW 權限？ |
| `has_foreign_data_wrapper_privilege`\(`fdw`,`privilege`\) | `boolean` | 目前使用者是否具有該 FDW 的權限？ |
| `has_function_privilege`\(`user`,`function`,`privilege`\) | `boolean` | 使用者是否具有該函數的權限？ |
| `has_function_privilege`\(`function`,`privilege`\) | `boolean` | 目前用戶是否具有該函數的權限？ |
| `has_language_privilege`\(`user`,`language`,`privilege`\) | `boolean` | 使用者是否有該程式語言的權限？ |
| `has_language_privilege`\(`language`,`privilege`\) | `boolean` | 目前使用者是否具有該程式語言的權限？ |
| `has_schema_privilege`\(`user`,`schema`,`privilege`\) | `boolean` | 使用者是否具有該 schema 的權限？ |
| `has_schema_privilege`\(`schema`,`privilege`\) | `boolean` | 目前使用者是否具有該 schema 的權限？ |
| `has_sequence_privilege`\(`user`,`sequence`,`privilege`\) | `boolean` | 使用者是否具有該序列資料的權限？ |
| `has_sequence_privilege`\(`sequence`,`privilege`\) | `boolean` | 目前使用者是否具有該序列資料的權限？ |
| `has_server_privilege`\(`user`,`server`,`privilege`\) | `boolean` | 使用者是否擁有該 foreign server 的權限？ |
| `has_server_privilege`\(`server`,`privilege`\) | `boolean` | 目前使用者是否具有該 foreign server 的權限？ |
| `has_table_privilege`\(`user`,`table`,`privilege`\) | `boolean` | 使用者是否擁有該資料表的權限？ |
| `has_table_privilege`\(`table`,`privilege`\) | `boolean` | 目前使用者是否擁有該資料表的權限？ |
| `has_tablespace_privilege`\(`user`,`tablespace`,`privilege`\) | `boolean` | 使用者是否擁有資料表空間的權限？ |
| `has_tablespace_privilege`\(`tablespace`,`privilege`\) | `boolean` | 目前用戶是否擁有資料表空間的權限？ |
| `has_type_privilege`\(`user`,`type`,`privilege`\) | `boolean` | 使用者是否有該資料型別的權限？ |
| `has_type_privilege`\(`type`,`privilege`\) | `boolean` | 目前使用者是否擁有該資料型別的權限？ |
| `pg_has_role`\(`user`,`role`,`privilege`\) | `boolean` | 使用者是否具有該角色的權限？ |
| `pg_has_role`\(`role`,`privilege`\) | `boolean` | 目前使用者是否擁有該角色的權限？ |
| `row_security_active`\(`table`\) | `boolean` | 目前使用者對於資料表的資料列級安全設定是否有效？ |

has\_table\_privilege 用於檢查使用者是否可以以特定的方式存取資料表。使用者可以透過 name、OID（pg\_authid.oid）、public 來指定 PUBLIC 的虛擬角色，如果省略參數的話，預設為 current\_user。該資料表可以使用名稱或 OID 來指定。（因此，has\_table\_privilege 實際上有六種變形，以它們的參數數量和型別加以區分。）以資料表名稱指定時，如果需要的，名稱可以加上 schema。所需的存取權限類型由文字字串指定，該文字字串必須為 SELECT、INSERT、UPDATE、DELETE、TRUNCATE、REFERENCES 或 TRIGGER 之一。或者，可以將 WITH GRANT OPTION 加到權限型別中以測試權限是否與授予的選項一起保存。此外，多個權限型別可以用逗號分隔列出，在這種情況下，如果列出的任何權限被保留，將會是 True 的結果。（權限字串的大小寫不重要，可以允許在權限名稱之間，但不在權限名稱內有額外的空白）。一些範例：

```
SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

has\_sequence\_privilege 用於檢查使用者是否能以特定方式存取序列物件。其參數類似於 has\_table\_privilege。所需的存取權限類型必須為 USAGE、SELECT 或 UPDATE 之一。

has\_any\_column\_privilege 用於檢查使用者是否能以特定方式存取資料表中的任何欄位。它的參數類似於 has\_table\_privilege，只是所需的存取權限類型必須為 SELECT、INSERT、UPDATE 或 REFERENCES 的組合。請注意，在資料表等級具有這些權限中的任何一項，都自然地授予該資料表的每一欄位。因此如果 has\_table\_privilege 對相同參數執行操作，has\_table\_privilege 始終都會回傳 true。但是，如果至少有一欄位有欄位級的欄限授予，則 has\_any\_column\_privilege 也會為 true。

has\_column\_privilege 用於檢查使用者是否能以特定方式存取欄位。它的參數類似於 has\_table\_privilege，該欄位可以透過名稱或屬性編號指定。所需的存取權限類型必須為 SELECT、INSERT、UPDATE 或 REFERENCES 的某種組合。請注意，在資料表級擁有的權限中的任何一項都會自動授予該資料表的每一個欄位。

has\_database\_privilege 用於檢查使用者是否能以特定方式存取資料庫。它的參數與 has\_table\_privilege 類似。所需的存取權限類型必須為 CREATE、CONNECT、TEMPORARY 或 TEMP（相當於 TEMPORARY）的某種組合。

has\_function\_privilege 用於檢查使用者是否可以以特定方式存取函數。它的參數類似於 has\_table\_privilege。 當透過文字字串而不是 OID 指定函數時，允許的輸入與regprocedure 資料型別相同（請參閱[第 8.18 節](/ii-the-sql-language/data-types/818-object-identifier-types.md)）。所需的存取權限類型必須為 EXECUTE。例如：

```
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
```

has\_foreign\_data\_wrapper\_privilege 用於檢查使用者是否能以特定方式存取 FDW。 它的參數類似於 has\_table\_privilege。所需的存取權限類型必須為 USAGE。

has\_language\_privilege 用於檢查使用者是否能以特定方式存 procedure 的程式語言。 它的參數類似於 has\_table\_privilege。所需的存取權限類型必須為 USAGE。

`has_schema_privilege`checks whether a user can access a schema in a particular way. Its argument possibilities are analogous to`has_table_privilege`. The desired access privilege type must evaluate to some combination of`CREATE`or`USAGE`.

`has_server_privilege`checks whether a user can access a foreign server in a particular way. Its argument possibilities are analogous to`has_table_privilege`. The desired access privilege type must evaluate to`USAGE`.

`has_tablespace_privilege`checks whether a user can access a tablespace in a particular way. Its argument possibilities are analogous to`has_table_privilege`. The desired access privilege type must evaluate to`CREATE`.

`has_type_privilege`checks whether a user can access a type in a particular way. Its argument possibilities are analogous to`has_table_privilege`. When specifying a type by a text string rather than by OID, the allowed input is the same as for the`regtype`data type \(see[Section 8.18](https://www.postgresql.org/docs/10/static/datatype-oid.html)\). The desired access privilege type must evaluate to`USAGE`.

`pg_has_role`checks whether a user can access a role in a particular way. Its argument possibilities are analogous to`has_table_privilege`, except that`public`is not allowed as a user name. The desired access privilege type must evaluate to some combination of`MEMBER`or`USAGE`.`MEMBER`denotes direct or indirect membership in the role \(that is, the right to do`SET ROLE`\), while`USAGE`denotes whether the privileges of the role are immediately available without doing`SET ROLE`.

`row_security_active`checks whether row level security is active for the specified table in the context of the`current_user`and environment. The table can be specified by name or by OID.

[Table 9.62](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-schema-table)shows functions that determine whether a certain object is\_visible\_in the current schema search path. For example, a table is said to be visible if its containing schema is in the search path and no table of the same name appears earlier in the search path. This is equivalent to the statement that the table can be referenced by name without explicit schema qualification. To list the names of all visible tables:

```
SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

**Table 9.62. Schema Visibility Inquiry Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_collation_is_visible(collation_oid`\) | `boolean` | is collation visible in search path |
| `pg_conversion_is_visible(conversion_oid`\) | `boolean` | is conversion visible in search path |
| `pg_function_is_visible(function_oid`\) | `boolean` | is function visible in search path |
| `pg_opclass_is_visible(opclass_oid`\) | `boolean` | is operator class visible in search path |
| `pg_operator_is_visible(operator_oid`\) | `boolean` | is operator visible in search path |
| `pg_opfamily_is_visible(opclass_oid`\) | `boolean` | is operator family visible in search path |
| `pg_statistics_obj_is_visible(stat_oid`\) | `boolean` | is statistics object visible in search path |
| `pg_table_is_visible(table_oid`\) | `boolean` | is table visible in search path |
| `pg_ts_config_is_visible(config_oid`\) | `boolean` | is text search configuration visible in search path |
| `pg_ts_dict_is_visible(dict_oid`\) | `boolean` | is text search dictionary visible in search path |
| `pg_ts_parser_is_visible(parser_oid`\) | `boolean` | is text search parser visible in search path |
| `pg_ts_template_is_visible(template_oid`\) | `boolean` | is text search template visible in search path |
| `pg_type_is_visible(type_oid`\) | `boolean` | is type \(or domain\) visible in search path |

Each function performs the visibility check for one type of database object. Note that`pg_table_is_visible`can also be used with views, materialized views, indexes, sequences and foreign tables;`pg_type_is_visible`can also be used with domains. For functions and operators, an object in the search path is visible if there is no object of the same name\_and argument data type\(s\)\_earlier in the path. For operator classes, both name and associated index access method are considered.

All these functions require object OIDs to identify the object to be checked. If you want to test an object by name, it is convenient to use the OID alias types \(`regclass`,`regtype`,`regprocedure`,`regoperator`,`regconfig`, or`regdictionary`\), for example:

```
SELECT pg_type_is_visible('myschema.widget'::regtype);
```

Note that it would not make much sense to test a non-schema-qualified type name in this way — if the name can be recognized at all, it must be visible.

[Table 9.63](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-catalog-table)lists functions that extract information from the system catalogs.

**Table 9.63. System Catalog Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `format_type(type_oid`,`typemod`\) | `text` | get SQL name of a data type |
| `pg_get_constraintdef(constraint_oid`\) | `text` | get definition of a constraint |
| `pg_get_constraintdef(constraint_oid`,`pretty_bool`\) | `text` | get definition of a constraint |
| `pg_get_expr(pg_node_tree`,`relation_oid`\) | `text` | decompile internal form of an expression, assuming that any Vars in it refer to the relation indicated by the second parameter |
| `pg_get_expr(pg_node_tree`,`relation_oid`,`pretty_bool`\) | `text` | decompile internal form of an expression, assuming that any Vars in it refer to the relation indicated by the second parameter |
| `pg_get_functiondef(func_oid`\) | `text` | get definition of a function |
| `pg_get_function_arguments(func_oid`\) | `text` | get argument list of function's definition \(with default values\) |
| `pg_get_function_identity_arguments(func_oid`\) | `text` | get argument list to identify a function \(without default values\) |
| `pg_get_function_result(func_oid`\) | `text` | get`RETURNS`clause for function |
| `pg_get_indexdef(index_oid`\) | `text` | get`CREATE INDEX`command for index |
| `pg_get_indexdef(index_oid`,`column_no`,`pretty_bool`\) | `text` | get`CREATE INDEX`command for index, or definition of just one index column when\_`column_no`\_is not zero |
| `pg_get_keywords()` | `setof record` | get list of SQL keywords and their categories |
| `pg_get_ruledef(rule_oid`\) | `text` | get`CREATE RULE`command for rule |
| `pg_get_ruledef(rule_oid`,`pretty_bool`\) | `text` | get`CREATE RULE`command for rule |
| `pg_get_serial_sequence(table_name`,`column_name`\) | `text` | get name of the sequence that a`serial`,`smallserial`or`bigserial`column uses |
| `pg_get_statisticsobjdef(statobj_oid`\) | `text` | get`CREATE STATISTICS`command for extended statistics object |
| `pg_get_triggerdef`\(`trigger_oid`\) | `text` | get`CREATE [ CONSTRAINT ] TRIGGER`command for trigger |
| `pg_get_triggerdef`\(`trigger_oid`,`pretty_bool`\) | `text` | get`CREATE [ CONSTRAINT ] TRIGGER`command for trigger |
| `pg_get_userbyid(role_oid`\) | `name` | get role name with given OID |
| `pg_get_viewdef(view_name`\) | `text` | get underlying`SELECT`command for view or materialized view \(_deprecated_\) |
| `pg_get_viewdef(view_name`,`pretty_bool`\) | `text` | get underlying`SELECT`command for view or materialized view \(_deprecated_\) |
| `pg_get_viewdef(view_oid`\) | `text` | get underlying`SELECT`command for view or materialized view |
| `pg_get_viewdef(view_oid`,`pretty_bool`\) | `text` | get underlying`SELECT`command for view or materialized view |
| `pg_get_viewdef(view_oid`,`wrap_column_int`\) | `text` | get underlying`SELECT`command for view or materialized view; lines with fields are wrapped to specified number of columns, pretty-printing is implied |
| `pg_index_column_has_property(index_oid`,`column_no`,`prop_name`\) | `boolean` | test whether an index column has a specified property |
| `pg_index_has_property(index_oid`,`prop_name`\) | `boolean` | test whether an index has a specified property |
| `pg_indexam_has_property(am_oid`,`prop_name`\) | `boolean` | test whether an index access method has a specified property |
| `pg_options_to_table(reloptions`\) | `setof record` | get the set of storage option name/value pairs |
| `pg_tablespace_databases(tablespace_oid`\) | `setof oid` | get the set of database OIDs that have objects in the tablespace |
| `pg_tablespace_location(tablespace_oid`\) | `text` | get the path in the file system that this tablespace is located in |
| `pg_typeof(any`\) | `regtype` | get the data type of any value |
| `collation for (any`\) | `text` | get the collation of the argument |
| `to_regclass(rel_name`\) | `regclass` | get the OID of the named relation |
| `to_regproc(func_name`\) | `regproc` | get the OID of the named function |
| `to_regprocedure(func_name`\) | `regprocedure` | get the OID of the named function |
| `to_regoper(operator_name`\) | `regoper` | get the OID of the named operator |
| `to_regoperator(operator_name`\) | `regoperator` | get the OID of the named operator |
| `to_regtype(type_name`\) | `regtype` | get the OID of the named type |
| `to_regnamespace(schema_name`\) | `regnamespace` | get the OID of the named schema |
| `to_regrole(role_name`\) | `regrole` | get the OID of the named role |

`format_type`returns the SQL name of a data type that is identified by its type OID and possibly a type modifier. Pass NULL for the type modifier if no specific modifier is known.

`pg_get_keywords`returns a set of records describing the SQL keywords recognized by the server. The`word`column contains the keyword. The`catcode`column contains a category code:`U`for unreserved,`C`for column name,`T`for type or function name, or`R`for reserved. The`catdesc`column contains a possibly-localized string describing the category.

`pg_get_constraintdef`,`pg_get_indexdef`,`pg_get_ruledef`,`pg_get_statisticsobjdef`, and`pg_get_triggerdef`, respectively reconstruct the creating command for a constraint, index, rule, extended statistics object, or trigger. \(Note that this is a decompiled reconstruction, not the original text of the command.\)`pg_get_expr`decompiles the internal form of an individual expression, such as the default value for a column. It can be useful when examining the contents of system catalogs. If the expression might contain Vars, specify the OID of the relation they refer to as the second parameter; if no Vars are expected, zero is sufficient.`pg_get_viewdef`reconstructs the`SELECT`query that defines a view. Most of these functions come in two variants, one of which can optionally“pretty-print”the result. The pretty-printed format is more readable, but the default format is more likely to be interpreted the same way by future versions ofPostgreSQL; avoid using pretty-printed output for dump purposes. Passing`false`for the pretty-print parameter yields the same result as the variant that does not have the parameter at all.

`pg_get_functiondef`returns a complete`CREATE OR REPLACE FUNCTION`statement for a function.`pg_get_function_arguments`returns the argument list of a function, in the form it would need to appear in within`CREATE FUNCTION`.`pg_get_function_result`similarly returns the appropriate`RETURNS`clause for the function.`pg_get_function_identity_arguments`returns the argument list necessary to identify a function, in the form it would need to appear in within`ALTER FUNCTION`, for instance. This form omits default values.

`pg_get_serial_sequence`returns the name of the sequence associated with a column, or NULL if no sequence is associated with the column. The first input parameter is a table name with optional schema, and the second parameter is a column name. Because the first parameter is potentially a schema and table, it is not treated as a double-quoted identifier, meaning it is lower cased by default, while the second parameter, being just a column name, is treated as double-quoted and has its case preserved. The function returns a value suitably formatted for passing to sequence functions \(see[Section 9.16](https://www.postgresql.org/docs/10/static/functions-sequence.html)\). This association can be modified or removed with`ALTER SEQUENCE OWNED BY`. \(The function probably should have been called`pg_get_owned_sequence`; its current name reflects the fact that it's typically used with`serial`or`bigserial`columns.\)

`pg_get_userbyid`extracts a role's name given its OID.

`pg_index_column_has_property`,`pg_index_has_property`, and`pg_indexam_has_property`return whether the specified index column, index, or index access method possesses the named property.`NULL`is returned if the property name is not known or does not apply to the particular object, or if the OID or column number does not identify a valid object. Refer to[Table 9.64](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-index-column-props)for column properties,[Table 9.65](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-index-props)for index properties, and[Table 9.66](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-indexam-props)for access method properties. \(Note that extension access methods can define additional property names for their indexes.\)

**Table 9.64. Index Column Properties**

| Name | Description |
| :--- | :--- |
| `asc` | Does the column sort in ascending order on a forward scan? |
| `desc` | Does the column sort in descending order on a forward scan? |
| `nulls_first` | Does the column sort with nulls first on a forward scan? |
| `nulls_last` | Does the column sort with nulls last on a forward scan? |
| `orderable` | Does the column possess any defined sort ordering? |
| `distance_orderable` | Can the column be scanned in order by a“distance”operator, for example`ORDER BY col <-> constant`? |
| `returnable` | Can the column value be returned by an index-only scan? |
| `search_array` | Does the column natively support`col = ANY(array)`searches? |
| `search_nulls` | Does the column support`IS NULL`and`IS NOT NULL`searches? |

**Table 9.65. Index Properties**

| Name | Description |
| :--- | :--- |
| `clusterable` | Can the index be used in a`CLUSTER`command? |
| `index_scan` | Does the index support plain \(non-bitmap\) scans? |
| `bitmap_scan` | Does the index support bitmap scans? |
| `backward_scan` | Can the index be scanned backwards? |

**Table 9.66. Index Access Method Properties**

| Name | Description |
| :--- | :--- |
| `can_order` | Does the access method support`ASC`,`DESC`and related keywords in`CREATE INDEX`? |
| `can_unique` | Does the access method support unique indexes? |
| `can_multi_col` | Does the access method support indexes with multiple columns? |
| `can_exclude` | Does the access method support exclusion constraints? |

`pg_options_to_table`returns the set of storage option name/value pairs \(`option_name`/`option_value`\) when passed`pg_class`.`reloptions`or`pg_attribute`.`attoptions`.

`pg_tablespace_databases`allows a tablespace to be examined. It returns the set of OIDs of databases that have objects stored in the tablespace. If this function returns any rows, the tablespace is not empty and cannot be dropped. To display the specific objects populating the tablespace, you will need to connect to the databases identified by`pg_tablespace_databases`and query their`pg_class`catalogs.

`pg_typeof`returns the OID of the data type of the value that is passed to it. This can be helpful for troubleshooting or dynamically constructing SQL queries. The function is declared as returning`regtype`, which is an OID alias type \(see[Section 8.18](https://www.postgresql.org/docs/10/static/datatype-oid.html)\); this means that it is the same as an OID for comparison purposes but displays as a type name. For example:

```
SELECT pg_typeof(33);

 pg_typeof 
-----------
 integer
(1 row)

SELECT typlen FROM pg_type WHERE oid = pg_typeof(33);
 typlen 
--------
      4
(1 row)
```

The expression`collation for`returns the collation of the value that is passed to it. Example:

```
SELECT collation for (description) FROM pg_description LIMIT 1;
 pg_collation_for 
------------------
 "default"
(1 row)

SELECT collation for ('foo' COLLATE "de_DE");
 pg_collation_for 
------------------
 "de_DE"
(1 row)
```

The value might be quoted and schema-qualified. If no collation is derived for the argument expression, then a null value is returned. If the argument is not of a collatable data type, then an error is raised.

The`to_regclass`,`to_regproc`,`to_regprocedure`,`to_regoper`,`to_regoperator`,`to_regtype`,`to_regnamespace`, and`to_regrole`functions translate relation, function, operator, type, schema, and role names \(given as`text`\) to objects of type`regclass`,`regproc`,`regprocedure`,`regoper`,`regoperator`,`regtype`,`regnamespace`, and`regrole`respectively. These functions differ from a cast from text in that they don't accept a numeric OID, and that they return null rather than throwing an error if the name is not found \(or, for`to_regproc`and`to_regoper`, if the given name matches multiple objects\).

[Table 9.67](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-object-table)lists functions related to database object identification and addressing.

**Table 9.67. Object Information and Addressing Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_describe_object(catalog_id`,`object_id`,`object_sub_id`\) | `text` | get description of a database object |
| `pg_identify_object(catalog_idoid`,`object_idoid`,`object_sub_idinteger`\) | `typetext`,`schematext`,`nametext`,`identitytext` | get identity of a database object |
| `pg_identify_object_as_address(catalog_idoid`,`object_idoid`,`object_sub_idinteger`\) | `typetext`,`nametext[]`,`argstext[]` | get external representation of a database object's address |
| `pg_get_object_address(typetext`,`nametext[]`,`argstext[]`\) | `catalog_idoid`,`object_idoid`,`object_sub_idint32` | get address of a database object, from its external representation |

`pg_describe_object`returns a textual description of a database object specified by catalog OID, object OID and a \(possibly zero\) sub-object ID. This description is intended to be human-readable, and might be translated, depending on server configuration. This is useful to determine the identity of an object as stored in the`pg_depend`catalog.

`pg_identify_object`returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and a \(possibly zero\) sub-object ID. This information is intended to be machine-readable, and is never translated.`type`_\_identifies the type of database object;_`schema`_is the schema name that the object belongs in, or_`NULL`_for object types that do not belong to schemas;_`name`_is the name of the object, quoted if necessary, only present if it can be used \(alongside schema name, if pertinent\) as a unique identifier of the object, otherwise_`NULL`_;_`identity`\_is the complete object identity, with the precise format depending on object type, and each part within the format being schema-qualified and quoted as necessary.

`pg_identify_object_as_address`returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and a \(possibly zero\) sub-object ID. The returned information is independent of the current server, that is, it could be used to identify an identically named object in another server.`type`_\_identifies the type of database object;_`name`_and_`args`\_are text arrays that together form a reference to the object. These three columns can be passed to`pg_get_object_address`to obtain the internal address of the object. This function is the inverse of`pg_get_object_address`.

`pg_get_object_address`returns a row containing enough information to uniquely identify the database object specified by its type and object name and argument arrays. The returned values are the ones that would be used in system catalogs such as`pg_depend`and can be passed to other system functions such as`pg_identify_object`or`pg_describe_object`.`catalog_id`_\_is the OID of the system catalog containing the object;_`object_id`_is the OID of the object itself, and_`object_sub_id`\_is the object sub-ID, or zero if none. This function is the inverse of`pg_identify_object_as_address`.

The functions shown in[Table 9.68](https://www.postgresql.org/docs/10/static/functions-info.html#functions-info-comment-table)extract comments previously stored with the[COMMENT](https://www.postgresql.org/docs/10/static/sql-comment.html)command. A null value is returned if no comment could be found for the specified parameters.

**Table 9.68. Comment Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `col_description(table_oid`,`column_number`\) | `text` | get comment for a table column |
| `obj_description(object_oid`,`catalog_name`\) | `text` | get comment for a database object |
| `obj_description(object_oid`\) | `text` | get comment for a database object \(_deprecated_\) |
| `shobj_description(object_oid`,`catalog_name`\) | `text` | get comment for a shared database object |

`col_description`returns the comment for a table column, which is specified by the OID of its table and its column number. \(`obj_description`cannot be used for table columns since columns do not have OIDs of their own.\)

The two-parameter form of`obj_description`returns the comment for a database object specified by its OID and the name of the containing system catalog. For example,`obj_description(123456,'pg_class')`would retrieve the comment for the table with OID 123456. The one-parameter form of`obj_description`requires only the object OID. It is deprecated since there is no guarantee that OIDs are unique across different system catalogs; therefore, the wrong comment might be returned.

`shobj_description`is used just like`obj_description`except it is used for retrieving comments on shared objects. Some system catalogs are global to all databases within each cluster, and the descriptions for objects in them are stored globally as well.

The functions shown in[Table 9.69](https://www.postgresql.org/docs/10/static/functions-info.html#functions-txid-snapshot)provide server transaction information in an exportable form. The main use of these functions is to determine which transactions were committed between two snapshots.

**Table 9.69. Transaction IDs and Snapshots**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `txid_current()` | `bigint` | get current transaction ID, assigning a new one if the current transaction does not have one |
| `txid_current_if_assigned()` | `bigint` | same as`txid_current()`but returns null instead of assigning an xid if none is already assigned |
| `txid_current_snapshot()` | `txid_snapshot` | get current snapshot |
| `txid_snapshot_xip(txid_snapshot`\) | `setof bigint` | get in-progress transaction IDs in snapshot |
| `txid_snapshot_xmax(txid_snapshot`\) | `bigint` | get`xmax`of snapshot |
| `txid_snapshot_xmin(txid_snapshot`\) | `bigint` | get`xmin`of snapshot |
| `txid_visible_in_snapshot(bigint`,`txid_snapshot`\) | `boolean` | is transaction ID visible in snapshot? \(do not use with subtransaction ids\) |
| `txid_status(bigint`\) | `txid_status` | report the status of the given xact -`committed`,`aborted`,`in progress`, or NULL if the txid is too old |

The internal transaction ID type \(`xid`\) is 32 bits wide and wraps around every 4 billion transactions. However, these functions export a 64-bit format that is extended with an“epoch”counter so it will not wrap around during the life of an installation. The data type used by these functions,`txid_snapshot`, stores information about transaction ID visibility at a particular moment in time. Its components are described in[Table 9.70](https://www.postgresql.org/docs/10/static/functions-info.html#functions-txid-snapshot-parts).

**Table 9.70. Snapshot Components**

| Name | Description |
| :--- | :--- |
| `xmin` | Earliest transaction ID \(txid\) that is still active. All earlier transactions will either be committed and visible, or rolled back and dead. |
| `xmax` | First as-yet-unassigned txid. All txids greater than or equal to this are not yet started as of the time of the snapshot, and thus invisible. |
| `xip_list` | Active txids at the time of the snapshot. The list includes only those active txids between`xmin`and`xmax`; there might be active txids higher than`xmax`. A txid that is`xmin <= txid < xmax`and not in this list was already completed at the time of the snapshot, and thus either visible or dead according to its commit status. The list does not include txids of subtransactions. |

`txid_snapshot`'s textual representation is`xmin`:`xmax`:`xip_list`. For example`10:20:10,14,15`means`xmin=10, xmax=20, xip_list=10, 14, 15`.

`txid_status(bigint)`reports the commit status of a recent transaction. Applications may use it to determine whether a transaction committed or aborted when the application and database server become disconnected while a`COMMIT`is in progress. The status of a transaction will be reported as either`in progress`,`committed`, or`aborted`, provided that the transaction is recent enough that the system retains the commit status of that transaction. If is old enough that no references to that transaction survive in the system and the commit status information has been discarded, this function will return NULL. Note that prepared transactions are reported as`in progress`; applications must check[`pg_prepared_xacts`](https://www.postgresql.org/docs/10/static/view-pg-prepared-xacts.html)if they need to determine whether the txid is a prepared transaction.

The functions shown in[Table 9.71](https://www.postgresql.org/docs/10/static/functions-info.html#functions-commit-timestamp)provide information about transactions that have been already committed. These functions mainly provide information about when the transactions were committed. They only provide useful data when[track\_commit\_timestamp](https://www.postgresql.org/docs/10/static/runtime-config-replication.html#guc-track-commit-timestamp)configuration option is enabled and only for transactions that were committed after it was enabled.

**Table 9.71. Committed transaction information**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_xact_commit_timestamp(xid`\) | `timestamp with time zone` | get commit timestamp of a transaction |
| `pg_last_committed_xact()` | `xidxid`,`timestamptimestamp with time zone` | get transaction ID and commit timestamp of latest committed transaction |

The functions shown in[Table 9.72](https://www.postgresql.org/docs/10/static/functions-info.html#functions-controldata)print information initialized during`initdb`, such as the catalog version. They also show information about write-ahead logging and checkpoint processing. This information is cluster-wide, and not specific to any one database. They provide most of the same information, from the same source, as[pg\_controldata](https://www.postgresql.org/docs/10/static/app-pgcontroldata.html), although in a form better suited toSQLfunctions.

**Table 9.72. Control Data Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_control_checkpoint()` | `record` | Returns information about current checkpoint state. |
| `pg_control_system()` | `record` | Returns information about current control file state. |
| `pg_control_init()` | `record` | Returns information about cluster initialization state. |
| `pg_control_recovery()` | `record` | Returns information about recovery state. |

`pg_control_checkpoint`returns a record, shown in[Table 9.73](https://www.postgresql.org/docs/10/static/functions-info.html#functions-pg-control-checkpoint)

**Table 9.73. **`pg_control_checkpoint`**Columns**

| Column Name | Data Type |
| :--- | :--- |
| `checkpoint_lsn` | `pg_lsn` |
| `prior_lsn` | `pg_lsn` |
| `redo_lsn` | `pg_lsn` |
| `redo_wal_file` | `text` |
| `timeline_id` | `integer` |
| `prev_timeline_id` | `integer` |
| `full_page_writes` | `boolean` |
| `next_xid` | `text` |
| `next_oid` | `oid` |
| `next_multixact_id` | `xid` |
| `next_multi_offset` | `xid` |
| `oldest_xid` | `xid` |
| `oldest_xid_dbid` | `oid` |
| `oldest_active_xid` | `xid` |
| `oldest_multi_xid` | `xid` |
| `oldest_multi_dbid` | `oid` |
| `oldest_commit_ts_xid` | `xid` |
| `newest_commit_ts_xid` | `xid` |
| `checkpoint_time` | `timestamp with time zone` |

`pg_control_system`returns a record, shown in[Table 9.74](https://www.postgresql.org/docs/10/static/functions-info.html#functions-pg-control-system)

**Table 9.74. **`pg_control_system`**Columns**

| Column Name | Data Type |
| :--- | :--- |
| `pg_control_version` | `integer` |
| `catalog_version_no` | `integer` |
| `system_identifier` | `bigint` |
| `pg_control_last_modified` | `timestamp with time zone` |

`pg_control_init`returns a record, shown in[Table 9.75](https://www.postgresql.org/docs/10/static/functions-info.html#functions-pg-control-init)

**Table 9.75. **`pg_control_init`**Columns**

| Column Name | Data Type |
| :--- | :--- |
| `max_data_alignment` | `integer` |
| `database_block_size` | `integer` |
| `blocks_per_segment` | `integer` |
| `wal_block_size` | `integer` |
| `bytes_per_wal_segment` | `integer` |
| `max_identifier_length` | `integer` |
| `max_index_columns` | `integer` |
| `max_toast_chunk_size` | `integer` |
| `large_object_chunk_size` | `integer` |
| `float4_pass_by_value` | `boolean` |
| `float8_pass_by_value` | `boolean` |
| `data_page_checksum_version` | `integer` |

`pg_control_recovery`returns a record, shown in[Table 9.76](https://www.postgresql.org/docs/10/static/functions-info.html#functions-pg-control-recovery)

**Table 9.76. **`pg_control_recovery`**Columns**

| Column Name | Data Type |
| :--- | :--- |
| `min_recovery_end_lsn` | `pg_lsn` |
| `min_recovery_end_timeline` | `integer` |
| `backup_start_lsn` | `pg_lsn` |
| `backup_end_lsn` | `pg_lsn` |
| `end_of_backup_record_required` | `boolean` |

---

[^1]:  [PostgreSQL: Documentation: 10: 9.25. System Information Functions](https://www.postgresql.org/docs/10/static/functions-info.html)

