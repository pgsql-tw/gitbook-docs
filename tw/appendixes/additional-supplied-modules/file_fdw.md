# F.14. file\_fdw

file\_fdw 模組提供了外部資料封裝器 file\_fdw，可用於存取伺服器檔案系統中的資料檔案，或在伺服器上執行某個程序並取得其輸出。資料檔案或程序輸出必須採用可由 COPY FROM 讀取的格式；有關詳細資訊，請參閱 [COPY](../../reference/sql-commands/copy.md)。目前對資料檔案的存取只有讀取的功能。

A foreign table created using this wrapper can have the following options:

`filename`

Specifies the file to be read. Must be an absolute path name. Either `filename` or `program` must be specified, but not both.

`program`

Specifies the command to be executed. The standard output of this command will be read as though `COPY FROM PROGRAM` were used. Either `program` or `filename` must be specified, but not both.

`format`

Specifies the data format, the same as `COPY`'s `FORMAT` option.`header`

Specifies whether the data has a header line, the same as `COPY`'s `HEADER` option.

`delimiter`

Specifies the data delimiter character, the same as `COPY`'s `DELIMITER` option.

`quote`

Specifies the data quote character, the same as `COPY`'s `QUOTE` option.

`escape`

Specifies the data escape character, the same as `COPY`'s `ESCAPE` option.

`null`

Specifies the data null string, the same as `COPY`'s `NULL` option.

`encoding`

Specifies the data encoding, the same as `COPY`'s `ENCODING` option.

Note that while `COPY` allows options such as `HEADER` to be specified without a corresponding value, the foreign table option syntax requires a value to be present in all cases. To activate `COPY` options typically written without a value, you can pass the value TRUE, since all such options are Booleans.

A column of a foreign table created using this wrapper can have the following options:

`force_not_null`

This is a Boolean option. If true, it specifies that values of the column should not be matched against the null string \(that is, the table-level `null` option\). This has the same effect as listing the column in `COPY`'s `FORCE_NOT_NULL` option.

`force_null`

This is a Boolean option. If true, it specifies that values of the column which match the null string are returned as `NULL` even if the value is quoted. Without this option, only unquoted values matching the null string are returned as `NULL`. This has the same effect as listing the column in `COPY`'s `FORCE_NULL` option.

`COPY`'s `FORCE_QUOTE` option is currently not supported by `file_fdw`.

These options can only be specified for a foreign table or its columns, not in the options of the `file_fdw` foreign-data wrapper, nor in the options of a server or user mapping using the wrapper.

Changing table-level options requires being a superuser or having the privileges of the default role `pg_read_server_files` \(to use a filename\) or the default role `pg_execute_server_program` \(to use a program\), for security reasons: only certain users should be able to control which file is read or which program is run. In principle regular users could be allowed to change the other options, but that's not supported at present.

When specifying the `program` option, keep in mind that the option string is executed by the shell. If you need to pass any arguments to the command that come from an untrusted source, you must be careful to strip or escape any characters that might have special meaning to the shell. For security reasons, it is best to use a fixed command string, or at least avoid passing any user input in it.

For a foreign table using `file_fdw`, `EXPLAIN` shows the name of the file to be read or program to be run. For a file, unless `COSTS OFF` is specified, the file size \(in bytes\) is shown as well.

## **Example F.1. Create a Foreign Table for PostgreSQL CSV Logs**

file\_fdw 其中一個明顯的用途是使 PostgreSQL 活動日誌形成查詢方便的資料表。為此，首先必須先產生記錄為 CSV 檔案，在這裡我們將其稱為 pglog.csv。首先，安裝 file\_fdw 延伸套件：

```text
CREATE EXTENSION file_fdw;
```

然後建立一個外部伺服器：

```text
CREATE SERVER pglog FOREIGN DATA WRAPPER file_fdw;
```

現在您可以建外部資料表了。使用 CREATE FOREIGN TABLE 命令，您將需要定義資料表的欄位、CSV 檔案名稱及其格式：

```text
CREATE FOREIGN TABLE pglog (
  log_time timestamp(3) with time zone,
  user_name text,
  database_name text,
  process_id integer,
  connection_from text,
  session_id text,
  session_line_num bigint,
  command_tag text,
  session_start_time timestamp with time zone,
  virtual_transaction_id text,
  transaction_id bigint,
  error_severity text,
  sql_state_code text,
  message text,
  detail text,
  hint text,
  internal_query text,
  internal_query_pos integer,
  context text,
  query text,
  query_pos integer,
  location text,
  application_name text
) SERVER pglog
OPTIONS ( filename '/home/josh/data/log/pglog.csv', format 'csv' );
```

就是這樣-現在您可以直接查詢日誌了。當然，在正式的運作環境中，您需要定義某種方式來處理日誌檔案的輪轉。

