# vacuumdb

vacuumdb — 資源回收並重新分析 PostgreSQL 資料庫

## 語法

`vacuumdb` \[_`connection-option`_...] \[_`option`_...] \[ `-t` | `--table` _`table`_ \[( _`column`_ \[,...] )] ] ... \[_`dbname`_]

`vacuumdb` \[_`connection-option`_...] \[_`option`_...] `-a` | `--all`

## 說明

vacuumdb 是一個用於清理 PostgreSQL 資料庫的工具程式。vacuumdb 也會產生 PostgreSQL 查詢最佳化程式所使用的內部統計資訊。

vacuumdb 只是一個將 SQL 指令 [VACUUM ](../sql-commands/vacuum.md)封裝起來的工具。透過此工具與透過其他方法存取伺服器之間，對資料庫進行清理和分析的工作並沒有任何區別。

## 選項參數

vacuumdb 接受以下的命令列參數：

`-a`\
`--all`

清理所有資料庫。

`[-d]` _`dbname`_\
`[--dbname=]`_`dbname`_

指定要清理或分析的資料庫名稱。如果未指定，也未使用 -a（或--all），則從環境變數 PGDATABASE 中取得資料庫名稱。如果都未設定，則使用此連線所使用的使用者名稱。

`--disable-page-skipping`

Disable skipping pages based on the contents of the visibility map.

#### Note

This option is only available for servers running PostgreSQL 9.6 and later.

`-e`\
`--echo`

顯示 vacuumdb 產生並發送到伺服器的指令。

`-f`\
`--full`

執行「完全」清理。

`-F`\
`--freeze`

積極地「凍結」資料 tuple。

`--force-index-cleanup`

Always remove index entries pointing to dead tuples.

#### Note

This option is only available for servers running PostgreSQL 12 and later.

`-j` _`njobs`_\
`--jobs=`_`njobs`_

透過同時執行 njobs 指令平行執行 vacuum 或 analyze 指令。此選項可以縮短處理時間，但也會增加資料庫伺服器的負載。

vacuumdb 將打開與資料庫的 njobs 連線，因此請確保您的 max\_connections 設定夠高以容納所有連線。

請注意，如果平行處理某些系統目錄，則此選項與 -f（FULL）選項一起使用可能會導致鎖死而失敗。

`--min-mxid-age`` `_`mxid_age`_

Only execute the vacuum or analyze commands on tables with a multixact ID age of at least _`mxid_age`_. This setting is useful for prioritizing tables to process to prevent multixact ID wraparound (see [Section 25.1.5.1](https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND)).

For the purposes of this option, the multixact ID age of a relation is the greatest of the ages of the main relation and its associated TOAST table, if one exists. Since the commands issued by vacuumdb will also process the TOAST table for the relation if necessary, it does not need to be considered separately.

#### Note

This option is only available for servers running PostgreSQL 9.6 and later.

`--min-xid-age`` `_`xid_age`_

Only execute the vacuum or analyze commands on tables with a transaction ID age of at least _`xid_age`_. This setting is useful for prioritizing tables to process to prevent transaction ID wraparound (see [Section 25.1.5](https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND)).

For the purposes of this option, the transaction ID age of a relation is the greatest of the ages of the main relation and its associated TOAST table, if one exists. Since the commands issued by vacuumdb will also process the TOAST table for the relation if necessary, it does not need to be considered separately.

#### Note

This option is only available for servers running PostgreSQL 9.6 and later.

`--no-index-cleanup`

Do not remove index entries pointing to dead tuples.

#### Note

This option is only available for servers running PostgreSQL 12 and later.

`--no-process-toast`

Skip the TOAST table associated with the table to vacuum, if any.

#### Note

This option is only available for servers running PostgreSQL 14 and later.

`--no-truncate`

Do not truncate empty pages at the end of the table.

#### Note

This option is only available for servers running PostgreSQL 12 and later.

`-P`` `_`parallel_workers`_\
`--parallel=`_`parallel_workers`_

Specify the number of parallel workers for _parallel vacuum_. This allows the vacuum to leverage multiple CPUs to process indexes. See [VACUUM](https://www.postgresql.org/docs/current/sql-vacuum.html).

#### Note

This option is only available for servers running PostgreSQL 13 and later.

`-q`\
`--quiet`

不顯示進度訊息。

`--skip-locked`

Skip relations that cannot be immediately locked for processing.

#### Note

This option is only available for servers running PostgreSQL 12 and later.

`-t` _`table`_ \[ (_`column`_ \[,...]) ]\
`--table=`_`table`_ \[ (_`column`_ \[,...]) ]

僅清理或分析資料表。欄位名稱只能與 --analyze 或 --analyze-only 選項一起指定。以多個選項開關可以對多個資料表進行清理。

### 小技巧

如果指定欄位，則可能必須從 shell 中跳脫括號。 （請參閱下面的例子。）

`-v`\
`--verbose`

處理期間輸出詳細訊息。

`V`\
`--version`

輸出 vacuumdb 版本後結束。

`-z`\
`--analyze`

同時計算最佳化程序所使用的統計資訊。

`-Z`\
`--analyze-only`

僅計算最佳化程序所使用的統計資訊（不做清理）。

`--analyze-in-stages`

僅計算最佳化程序所使用的統計資訊（不做清理），如同 --analyze-only。使用不同的設定執行幾個（目前是三個）分析階段，以更快地產可用的統計資訊。

此選項對於分析從還原備份或 pg\_upgrade 新加入的資料庫非常有用。此選項將嘗試盡可能更快地建立一些統計資訊，使資料庫可用，然後在後續階段產生更完整的統計資訊。

`-?`\
`--help`

顯示有關 vacuumdb 命令列參數的說明，然後結束。

vacuumdb 也在命令列中接受以下連線參數：

`-h` _`host`_\
`--host=`_`host`_

指定執行伺服器的主機名稱。如果以斜線開頭，則將其用作 Unix domain socket 的目錄。

`-p` _`port`_\
`--port=`_`port`_

指定伺服器正在監聽連線的 TCP 連接埠或本地 Unix domain socket 檔案的延伸名稱。

`-U` _`username`_\
`--username=`_`username`_

要連線的使用者名稱。

`-w`\
`--no-password`

不要發出密碼提示。如果伺服器需要密碼身份驗證，而其他方式（例如 .pgpass 檔案）無法使用密碼，則連線嘗試將會失敗。此選項在沒有使用者輸入密碼的批次處理作業腳本中非常有用。

`-W`\
`--password`

強制 vacuumdb 在連線到資料庫之前提示輸入密碼。

此選項並不是必要的，因為如果伺服器需要密碼驗證，vacuumdb 將自動提示輸入密碼。只是，vacuumdb 會浪費連線嘗試，才能發現伺服器需要密碼。在某些情況下，值得輸入 -W 以避免額外的連線嘗試。

`--maintenance-db=`_`dbname`_

指定要連線的資料庫名稱，以發現應該清理哪些其他資料庫。如果未指定，將使用 postgres 資料庫，如果 postgres 不存在的話，將使用 template1。

## 執行環境

`PGDATABASE`\
`PGHOST`\
`PGPORT`\
`PGUSER`

預設連線參數

與大多數其他 PostgreSQL 工具程式一樣，此工具也使用 libpq 所支援的環境變數（請參閱[第 34.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

## 問題分析

如果遇到困難，請參閱 [VACUUM](../sql-commands/vacuum.md) 和 [psql](psql.md) 以了解潛在問題和錯誤訊息。資料庫伺服器必須在目標主機上執行。此外，將套用 libpq 前端函式庫使用的所有預設連線設定和環境變數。

## 注意

vacuumdb 可能需要多次連線到 PostgreSQL 伺服器，而每次都會要求輸入密碼。在這種情況下，有一個 \~/.pgpass 檔案的話會很方便。有關更多訊息，請參閱[第 34.16 節](../../client-interfaces/libpq-c-library/libpq-pgpass.md)。

## `範例`

要清理資料庫 test：

```
$ vacuumdb test
```

為最佳化程序清理並分析名為 bigdb 的資料庫：

```
$ vacuumdb --analyze bigdb
```

要清理 xyzzy 資料庫中的資料表 foo，並為最佳化程序分析資料表的單個欄位：

```
$ vacuumdb --analyze --verbose --table='foo(bar)' xyzzy
```

## 參閱

[VACUUM](../sql-commands/vacuum.md)
