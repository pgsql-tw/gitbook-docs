# 25.3. Log 檔案維護

It is a good idea to save the database server's log output somewhere, rather than just discarding it via `/dev/null`. The log output is invaluable when diagnosing problems. However, the log output tends to be voluminous \(especially at higher debug levels\) so you won't want to save it indefinitely. You need to _rotate_ the log files so that new log files are started and old ones removed after a reasonable period of time.

If you simply direct the stderr of `postgres` into a file, you will have log output, but the only way to truncate the log file is to stop and restart the server. This might be acceptable if you are using PostgreSQL in a development environment, but few production servers would find this behavior acceptable.

更好的方法是將伺服器的 stderr 輸出發送到某種日誌輪轉程序。有一個內建的日誌輪轉工具，您可以透過在 postgresql.conf 中將組態參數 logging\_collector 設定為 true 來使用。該程序的控制參數在 [19.8.1 節](../server-configuration/error-reporting-and-logging.md#19-8-1-ji-lu-zai-na-li)中介紹。您還可以使用這種方法以機器可讀的 CSV（逗號分隔內容）格式取得日誌內容。

Alternatively, you might prefer to use an external log rotation program if you have one that you are already using with other server software. For example, the rotatelogs tool included in the Apache distribution can be used with PostgreSQL. One way to do this is to pipe the server's stderr output to the desired program. If you start the server with `pg_ctl`, then stderr is already redirected to stdout, so you just need a pipe command, for example:

```text
pg_ctl start | rotatelogs /var/log/pgsql_log 86400
```

您可以透過設定 logrotate 來收集 PostgreSQL 內建日誌收集器所產生的日誌檔案，從而結合使用這些方法。在這種情況下，日誌收集器會定義日誌檔案的名稱和位置，而 logrotate 會定期封存這些檔案。啟動日誌輪轉時，logrotate 必須確保應用程序會進一步的輸出發送到新檔案。 通常會使用 postrotate 腳本來完成此操作，該腳本將 SIGHUP 信號發送到應用程序，然後重新打開日誌檔案。在 PostgreSQL 中，您可以使用 logrotate 選項執行 pg\_ctl。伺服器收到此命令後，將切轉到新的日誌檔案或重新打開現有檔案，具體取決於日誌記錄設定（請參閱[第 19.8.1 節](../server-configuration/error-reporting-and-logging.md#19-8-1-ji-lu-zai-na-li)）。

{% hint style="info" %}
使用靜態日誌檔案名稱時，如果達到最大開啓檔案數量限制或超過最大檔案大小，伺服器可能會無法重新開啓日誌檔案。在這種情況下，日誌訊息將發送到舊的日誌檔案，直到成功進行日誌輪轉為止。如果將 logrotate 設定為壓縮日誌檔案並將其刪除，則伺服器可能會失去此時間範圍內記錄的訊息。為避免此問題，可以將日誌收集器設定為動態分配日誌檔案名稱，並使用 prerotate 的腳本以避免開啓日誌檔案。
{% endhint %}

Another production-grade approach to managing log output is to send it to syslog and let syslog deal with file rotation. To do this, set the configuration parameter `log_destination` to `syslog` \(to log to syslog only\) in `postgresql.conf`. Then you can send a `SIGHUP` signal to the syslog daemon whenever you want to force it to start writing a new log file. If you want to automate log rotation, the logrotate program can be configured to work with log files from syslog.

On many systems, however, syslog is not very reliable, particularly with large log messages; it might truncate or drop messages just when you need them the most. Also, on Linux, syslog will flush each message to disk, yielding poor performance. \(You can use a “`-`” at the start of the file name in the syslog configuration file to disable syncing.\)

Note that all the solutions described above take care of starting new log files at configurable intervals, but they do not handle deletion of old, no-longer-useful log files. You will probably want to set up a batch job to periodically delete old log files. Another possibility is to configure the rotation program so that old log files are overwritten cyclically.

[pgBadger](https://pgbadger.darold.net/) is an external project that does sophisticated log file analysis. [check\_postgres](https://bucardo.org/check_postgres/) provides Nagios alerts when important messages appear in the log files, as well as detection of many other extraordinary conditions.

