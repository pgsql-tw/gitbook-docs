## F.15. file_fdw — 存取伺服器檔案系統中的資料檔案 [#](#FILE-FDW)

<a id="id-1.11.7.25.2"></a>

`file_fdw` 模組提供外部資料包裝器
`file_fdw`，可用來存取伺服器檔案系統中的資料檔案，或在伺服器上執行程式並讀取其輸出。資料檔案或程式輸出必須採用
`COPY FROM` 可讀取的格式；詳細資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。目前對資料檔案的存取僅限讀取。

使用此包裝器建立的外部資料表可設定下列選項：

`filename`
:   指定要讀取的檔案。相對路徑是相對於資料目錄。
    必須指定 `filename` 或 `program` 其中之一，但不可同時指定兩者。

`program`
:   指定要執行的命令。系統會如同使用 `COPY FROM PROGRAM` 一般讀取此命令的標準輸出。
    必須指定 `program` 或 `filename` 其中之一，但不可同時指定兩者。

`format`
:   指定資料格式，等同於 `COPY` 的 `FORMAT` 選項。

`header`
:   指定資料是否含有標頭列，等同於 `COPY` 的 `HEADER` 選項。

`delimiter`
:   指定資料的分隔字元，等同於 `COPY` 的 `DELIMITER` 選項。

`quote`
:   指定資料的引號字元，等同於 `COPY` 的 `QUOTE` 選項。

`escape`
:   指定資料的逸出字元，等同於 `COPY` 的 `ESCAPE` 選項。

`null`
:   指定資料的 NULL 字串，等同於 `COPY` 的 `NULL` 選項。

`default`
:   指定代表預設值的字串，等同於 `COPY` 的 `DEFAULT` 選項。

`encoding`
:   指定資料編碼，等同於 `COPY` 的 `ENCODING` 選項。

`on_error`
:   指定將欄位輸入值轉換為其資料型別時遇到錯誤的處理方式，等同於 `COPY` 的 `ON_ERROR` 選項。

`reject_limit`
:   指定將欄位輸入值轉換為其資料型別時可容許的最大錯誤數，等同於 `COPY` 的
    `REJECT_LIMIT` 選項。

`log_verbosity`
:   指定 `file_fdw` 發出的訊息量，等同於 `COPY` 的 `LOG_VERBOSITY` 選項。

請注意，雖然 `COPY` 允許指定如 `HEADER` 這類沒有對應值的選項，外部資料表的選項語法在所有情況下都必須提供值。若要啟用通常不寫值的
`COPY` 選項，可傳入值 TRUE，因為所有這類選項都是布林值。

使用此包裝器建立的外部資料表之欄位可設定下列選項：

`force_not_null`
:   這是布林選項。若為 true，表示不應將該欄位的值與 NULL 字串（亦即資料表層級的
    `null` 選項）比對。這與在 `COPY` 的 `FORCE_NOT_NULL` 選項中列出該欄位具有相同效果。

`force_null`
:   這是布林選項。若為 true，與 NULL 字串相符的欄位值即使被加上引號，也會傳回為 `NULL`。
    沒有此選項時，只有未加引號且與 NULL 字串相符的值會傳回為 `NULL`。
    這與在 `COPY` 的 `FORCE_NULL` 選項中列出該欄位具有相同效果。

`file_fdw` 目前不支援 `COPY` 的 `FORCE_QUOTE` 選項。

這些選項只能為外部資料表或其欄位指定，不可在 `file_fdw` 外部資料包裝器的選項中指定，也不可在使用此包裝器的伺服器或使用者對應選項中指定。

基於安全理由，變更資料表層級的選項需要是超級使用者，或具有角色
`pg_read_server_files`（使用檔名時）或角色 `pg_execute_server_program`（使用程式時）的權限：只有特定使用者應能控制讀取哪個檔案或執行哪個程式。原則上可以允許一般使用者變更其他選項，但目前尚未支援。

指定 `program` 選項時，請記得選項字串會由 shell 執行。若需將來自不受信任來源的任何引數傳給命令，必須謹慎移除或逸出可能對 shell 具有特殊意義的字元。基於安全理由，最好使用固定的命令字串，或至少避免在其中傳入任何使用者輸入。

對使用 `file_fdw` 的外部資料表，`EXPLAIN` 會顯示要讀取的檔案名稱或要執行的程式。對檔案而言，除非指定
`COSTS OFF`，也會顯示檔案大小（位元組）。

<a id="id-1.11.7.25.14"></a>

**範例 F.1. 為 PostgreSQL CSV 日誌建立外部資料表**

`file_fdw` 的一個明顯用途，是將 PostgreSQL 活動日誌以可查詢的資料表形式提供。為此，您必須先[記錄至 CSV 檔案](../../server-administration/runtime-config/runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)，此處將其稱為 `pglog.csv`。首先，將 `file_fdw` 安裝為擴充功能：

```

CREATE EXTENSION file_fdw;
```

接著建立外部伺服器：

```

CREATE SERVER pglog FOREIGN DATA WRAPPER file_fdw;
```

現在可以建立外部資料表。使用 `CREATE FOREIGN TABLE` 命令時，必須定義資料表欄位、CSV 檔案名稱及其格式：

```

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
  application_name text,
  backend_type text,
  leader_pid integer,
  query_id bigint
) SERVER pglog
OPTIONS ( filename 'log/pglog.csv', format 'csv' );
```

至此即可直接查詢日誌。當然，在正式環境中，還必須定義處理日誌輪替的方式。

<br><a id="id-1.11.7.25.15"></a>

**範例 F.2. 建立在欄位上設定選項的外部資料表**

若要為欄位設定 `force_null` 選項，請使用 `OPTIONS` 關鍵字。

```

CREATE FOREIGN TABLE films (
 code char(5) NOT NULL,
 title text NOT NULL,
 rating text OPTIONS (force_null 'true')
) SERVER film_server
OPTIONS ( filename 'films/db.csv', format 'csv' );
```

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/file-fdw.html)
