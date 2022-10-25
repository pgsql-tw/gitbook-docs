# pg\_basebackup

pg\_basebackup — 對 PostgreSQL 叢集進行基礎備份

### 語法

`pg_basebackup` \[_`option`_...]

### 說明

pg\_basebackup 用於對正在執行的 PostgreSQL 資料庫叢集進行基礎備份。採取這些措施不會影響資料庫的其他用戶端，並且可以用於時間點隨選還原（請參閱[第 25.3 節](../../server-administration/backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md)），也可以用於日誌傳送或串流複寫備用伺服器的起點（請參閱[第 26.2 節](../../server-administration/high-availability-load-balancing-and-replication/log-shipping-standby-servers.md)）。

pg\_basebackup 製作資料庫叢集檔案的二進位副本，同時確保系統自動進入和退出備份模式。只能對整個資料庫叢集進行備份；無法備份單個資料庫或資料庫物件。對於單一資料庫的備份，必須使用如 [pg\_dump](pg\_dump.md) 之類的工具。

此備份是透過一般 PostgreSQL 連線所進行的，並使用複寫協定。必須由超級使用者或具有 REPLICATION 權限的使用者建立連線（請參閱 [21.2](../../server-administration/database-roles/role-attributes.md)），並且 pg\_hba.conf 必須明確允許複寫連線。必須讓伺服器設定的 [max\_wal\_senders](../../server-administration/server-configuration/replication.md#max\_wal\_senders-integer) 設定得夠多，以使至少一個連線可用於備份，而至少一個連線可用於 WAL 串流傳輸（如果有使用的話）。

可以同時執行多個 pg\_basebackup，但是從效能的角度來看，最好只執行一個備份並且複製其結果。

pg\_basebackup 不僅可以從主要資料庫備份，也可以從備用資料庫進行基礎備份。要從備用資料庫中取得備份，請設定該備用資料庫，使其可以接受複寫連線（即設定 max\_wal\_senders 和 [hot\_standby](../../server-administration/server-configuration/replication.md#hot\_standby-boolean)，並配置基於主機的身份驗證）。您還需要在主要伺服器上啟用 [full\_page\_writes](../../server-administration/server-configuration/write-ahead-log.md#full\_page\_writes-boolean)。

請注意，從備用資料庫的備份會有一些限制：

* The backup history file is not created in the database cluster backed up.
* If you are using `-X none`, there is no guarantee that all WAL files required for the backup are archived at the end of backup.
* If the standby is promoted to the master during online backup, the backup fails.
* All WAL records required for the backup must contain sufficient full-page writes, which requires you to enable `full_page_writes` on the master and not to use a tool like pg\_compresslog as `archive_command` to remove full-page writes from WAL files.

### Options

The following command-line options control the location and format of the output.

`-D`` `_`directory`_\
`--pgdata=`_`directory`_

Directory to write the output to. pg\_basebackup will create the directory and any parent directories if necessary. The directory may already exist, but it is an error if the directory already exists and is not empty.

When the backup is in tar mode, and the directory is specified as `-` (dash), the tar file will be written to `stdout`.

This option is required.

`-F`` `_`format`_\
`--format=`_`format`_

Selects the format for the output. _`format`_ can be one of the following:

`p`\
`plain`

Write the output as plain files, with the same layout as the current data directory and tablespaces. When the cluster has no additional tablespaces, the whole database will be placed in the target directory. If the cluster contains additional tablespaces, the main data directory will be placed in the target directory, but all other tablespaces will be placed in the same absolute path as they have on the server.

This is the default format.

`t`\
`tar`

Write the output as tar files in the target directory. The main data directory will be written to a file named `base.tar`, and all other tablespaces will be named after the tablespace OID.

If the value `-` (dash) is specified as target directory, the tar contents will be written to standard output, suitable for piping to for example gzip. This is only possible if the cluster has no additional tablespaces and WAL streaming is not used.

`-r`` `_`rate`_\
`--max-rate=`_`rate`_

The maximum transfer rate of data transferred from the server. Values are in kilobytes per second. Use a suffix of `M` to indicate megabytes per second. A suffix of `k` is also accepted, and has no effect. Valid values are between 32 kilobytes per second and 1024 megabytes per second.

The purpose is to limit the impact of pg\_basebackup on the running server.

This option always affects transfer of the data directory. Transfer of WAL files is only affected if the collection method is `fetch`.

`-R`\
`--write-recovery-conf`

Create `standby.signal` and append connection settings to `postgresql.auto.conf` in the output directory (or into the base archive file when using tar format) to ease setting up a standby server. The `postgresql.auto.conf` file will record the connection settings and, if specified, the replication slot that pg\_basebackup is using, so that the streaming replication will use the same settings later on.

`-T`` `_`olddir`_=_`newdir`_\
`--tablespace-mapping=`_`olddir`_=_`newdir`_

Relocate the tablespace in directory _`olddir`_ to _`newdir`_ during the backup. To be effective, _`olddir`_ must exactly match the path specification of the tablespace as it is currently defined. (But it is not an error if there is no tablespace in _`olddir`_ contained in the backup.) Both _`olddir`_ and _`newdir`_ must be absolute paths. If a path happens to contain a `=` sign, escape it with a backslash. This option can be specified multiple times for multiple tablespaces. See examples below.

If a tablespace is relocated in this way, the symbolic links inside the main data directory are updated to point to the new location. So the new data directory is ready to be used for a new server instance with all tablespaces in the updated locations.

`--waldir=`_`waldir`_

Specifies the location for the write-ahead log directory. _`waldir`_ must be an absolute path. The write-ahead log directory can only be specified when the backup is in plain mode.

`-X`` `_`method`_\
`--wal-method=`_`method`_

Includes the required write-ahead log files (WAL files) in the backup. This will include all write-ahead logs generated during the backup. Unless the method `none` is specified, it is possible to start a postmaster directly in the extracted directory without the need to consult the log archive, thus making this a completely standalone backup.

The following methods for collecting the write-ahead logs are supported:

`n`\
`none`

Don't include write-ahead log in the backup.

`f`\
`fetch`

The write-ahead log files are collected at the end of the backup. Therefore, it is necessary for the [wal\_keep\_segments](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-WAL-KEEP-SEGMENTS) parameter to be set high enough that the log is not removed before the end of the backup. If the log has been rotated when it's time to transfer it, the backup will fail and be unusable.

When tar format mode is used, the write-ahead log files will be written to the `base.tar` file.

`s`\
`stream`

Stream the write-ahead log while the backup is created. This will open a second connection to the server and start streaming the write-ahead log in parallel while running the backup. Therefore, it will use up two connections configured by the [max\_wal\_senders](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-MAX-WAL-SENDERS) parameter. As long as the client can keep up with write-ahead log received, using this mode requires no extra write-ahead logs to be saved on the master.

When tar format mode is used, the write-ahead log files will be written to a separate file named `pg_wal.tar` (if the server is a version earlier than 10, the file will be named `pg_xlog.tar`).

This value is the default.

`-z`\
`--gzip`

Enables gzip compression of tar file output, with the default compression level. Compression is only available when using the tar format, and the suffix `.gz` will automatically be added to all tar filenames.

`-Z`` `_`level`_\
`--compress=`_`level`_

Enables gzip compression of tar file output, and specifies the compression level (0 through 9, 0 being no compression and 9 being best compression). Compression is only available when using the tar format, and the suffix `.gz` will automatically be added to all tar filenames.

The following command-line options control the generation of the backup and the running of the program.

`-c`` `_`fast|spread`_\
`--checkpoint=`_`fast|spread`_

Sets checkpoint mode to fast (immediate) or spread (default) (see [Section 25.3.3](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP)).

`-C`\
`--create-slot`

This option causes creation of a replication slot named by the `--slot` option before starting the backup. An error is raised if the slot already exists.

`-l`` `_`label`_\
`--label=`_`label`_

Sets the label for the backup. If none is specified, a default value of “`pg_basebackup base backup`” will be used.

`-n`\
`--no-clean`

By default, when `pg_basebackup` aborts with an error, it removes any directories it might have created before discovering that it cannot finish the job (for example, data directory and write-ahead log directory). This option inhibits tidying-up and is thus useful for debugging.

Note that tablespace directories are not cleaned up either way.

`-N`\
`--no-sync`

By default, `pg_basebackup` will wait for all files to be written safely to disk. This option causes `pg_basebackup` to return without waiting, which is faster, but means that a subsequent operating system crash can leave the base backup corrupt. Generally, this option is useful for testing but should not be used when creating a production installation.

`-P`\
`--progress`

Enables progress reporting. Turning this on will deliver an approximate progress report during the backup. Since the database may change during the backup, this is only an approximation and may not end at exactly `100%`. In particular, when WAL log is included in the backup, the total amount of data cannot be estimated in advance, and in this case the estimated target size will increase once it passes the total estimate without WAL.

When this is enabled, the backup will start by enumerating the size of the entire database, and then go back and send the actual contents. This may make the backup take slightly longer, and in particular it will take longer before the first data is sent.

`-S`` `_`slotname`_\
`--slot=`_`slotname`_

This option can only be used together with `-X stream`. It causes the WAL streaming to use the specified replication slot. If the base backup is intended to be used as a streaming replication standby using replication slots, it should then use the same replication slot name in [primary\_slot\_name](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-PRIMARY-SLOT-NAME). That way, it is ensured that the server does not remove any necessary WAL data in the time between the end of the base backup and the start of streaming replication.

The specified replication slot has to exist unless the option `-C` is also used.

If this option is not specified and the server supports temporary replication slots (version 10 and later), then a temporary replication slot is automatically used for WAL streaming.

`-v`\
`--verbose`

Enables verbose mode. Will output some extra steps during startup and shutdown, as well as show the exact file name that is currently being processed if progress reporting is also enabled.

`--no-slot`

This option prevents the creation of a temporary replication slot during the backup even if it's supported by the server.

Temporary replication slots are created by default if no slot name is given with the option `-S` when using log streaming.

The main purpose of this option is to allow taking a base backup when the server is out of free replication slots. Using replication slots is almost always preferred, because it prevents needed WAL from being removed by the server during the backup.

`--no-verify-checksums`

Disables verification of checksums, if they are enabled on the server the base backup is taken from.

By default, checksums are verified and checksum failures will result in a non-zero exit status. However, the base backup will not be removed in such a case, as if the `--no-clean` option had been used. Checksum verifications failures will also be reported in the [pg\_stat\_database](https://www.postgresql.org/docs/12/monitoring-stats.html#PG-STAT-DATABASE-VIEW) view.

The following command-line options control the database connection parameters.

`-d`` `_`connstr`_\
`--dbname=`_`connstr`_

Specifies parameters used to connect to the server, as a connection string. See [Section 33.1.1](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING) for more information.

The option is called `--dbname` for consistency with other client applications, but because pg\_basebackup doesn't connect to any particular database in the cluster, database name in the connection string will be ignored.

`-h`` `_`host`_\
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket. The default is taken from the `PGHOST` environment variable, if set, else a Unix domain socket connection is attempted.

`-p`` `_`port`_\
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections. Defaults to the `PGPORT` environment variable, if set, or a compiled-in default.

`-s`` `_`interval`_\
`--status-interval=`_`interval`_

Specifies the number of seconds between status packets sent back to the server. This allows for easier monitoring of the progress from server. A value of zero disables the periodic status updates completely, although an update will still be sent when requested by the server, to avoid timeout disconnect. The default value is 10 seconds.

`-U`` `_`username`_\
`--username=`_`username`_

User name to connect as.

`-w`\
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`\
`--password`

Force pg\_basebackup to prompt for a password before connecting to a database.

This option is never essential, since pg\_basebackup will automatically prompt for a password if the server demands password authentication. However, pg\_basebackup will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

Other options are also available:

`-V`\
`--version`

Print the pg\_basebackup version and exit.

`-?`\
`--help`

Show help about pg\_basebackup command line arguments, and exit.

### 環境變數

與大多數其他 PostgreSQL 工具程式一樣，此工具使用 libpq 所支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

環境變數 PG\_COLOR 指定是否在診斷資訊中使用彩色。可能的值為 always，auto 和 never。

### 注意

在備份開始時，需要在備份目標的伺服器上寫入一個檢查點。特別是如果不使用 --checkpoint = fast 選項的話，這可能會花費一些時間，在此期間 pg\_basebackup 會顯示為 idle。

備份將包括資料目錄和資料表空間中的所有檔案，包括組態檔案以及由第三方套件放置在目錄中的任何其他檔案，但由 PostgreSQL 管理的某些臨時檔案會排除在外。只會複製一般檔案和目錄，除了保留用於資料表空間的 symbolic links。指向 PostgreSQL 已知的某些目錄的 symbolic links 會被複製為空目錄。其他 symbolic links 和特殊裝置檔案將被跳過。有關詳細資訊，請參閱[第 52.4 節](../../internals/52.-frontend-backend-protocol/streaming-replication-protocol.md)。

Tablespaces will in plain format by default be backed up to the same path they have on the server, unless the option `--tablespace-mapping` is used. Without this option, running a plain format base backup on the same host as the server will not work if tablespaces are in use, because the backup would have to be written to the same directory locations as the original tablespaces.

When tar format mode is used, it is the user's responsibility to unpack each tar file before starting the PostgreSQL server. If there are additional tablespaces, the tar files for them need to be unpacked in the correct locations. In this case the symbolic links for those tablespaces will be created by the server according to the contents of the `tablespace_map` file that is included in the `base.tar` file.

pg\_basebackup works with servers of the same or an older major version, down to 9.1. However, WAL streaming mode (`-X stream`) only works with server version 9.3 and later, and tar format mode (`--format=tar`) of the current version only works with server version 9.5 or later.

pg\_basebackup will preserve group permissions in both the `plain` and `tar` formats if group permissions are enabled on the source cluster.

### 範例

要在 mydbserver 上建立伺服器的基礎備份並將其儲存在本機路徑 /usr/local/pgsql/data 下：

```
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
```

要為每個資料表空間使用一個壓縮的 tar 檔案建立本機伺服器的備份，並將其儲存在目錄備份中，且在執行時顯示進度報告：

```
$ pg_basebackup -D backup -Ft -z -P
```

要建立單個資料表空間本機資料庫的備份並使用 bzip2 來壓縮它：

```
$ pg_basebackup -D - -Ft -X fetch | bzip2 > backup.tar.bz2
```

（如果資料庫中有多個資料表空間，則此命令將會失敗。）

要建立本機資料庫的備份，其中 /opt/ts 中的資料表空間要重新定位到 ./backup/ts：

```
$ pg_basebackup -D backup/data -T /opt/ts=$(pwd)/backup/ts
```

### 參閱

[pg\_dump](pg\_dump.md)
