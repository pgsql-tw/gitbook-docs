---
description: 版本：11
---

# 33.14. 環境變數

以下環境變數可用於選擇預設連線參數值，如果呼叫變數沒有直接指定值， PQconnectdb，PQsetdbLogin 和 PQsetdb 將使用這些值。例如，這些有助於避免將資料庫連線訊息硬寫到簡單的用戶端應用程序中。

* `PGHOST` 的行為與 [host](database-connection-control-functions.md#host) 參數相同。
* `PGHOSTADDR` 的行為與 [hostaddr](database-connection-control-functions.md#hostaddr) 連線參數相同。這可以代替 PGHOST 或者除了 PGHOST 之外設定，以避免 DNS 查詢的開銷。
* `PGPORT` 的行為與 [port](database-connection-control-functions.md#port) 連線參數相同。
* `PGDATABASE` 的行為與 [dbname](database-connection-control-functions.md#dbname) 連線參數相同。
* `PGUSER` 的行為與 [user](database-connection-control-functions.md#user) 連線參數相同。
* `PGPASSWORD` 的行為與 [password](database-connection-control-functions.md#password) 連線參數相同。但由於安全因素，不建議使用此環境變數，因為某些作業系統允許非 root 使用者透過 ps 查看程序環境變數；而是考慮使用密碼檔案（參閱[第 33.15 節](33.15.-mi-ma-dang.md)）。
* `PGPASSFILE` 行為與 [passfile ](database-connection-control-functions.md#34-1-2-parameter-key-words)連線參數相同。
* `PGSERVICE` behaves the same as the [service](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SERVICE) connection parameter.
* `PGSERVICEFILE` specifies the name of the per-user connection service file. If not set, it defaults to `~/.pg_service.conf` \(see [Section 33.16](https://www.postgresql.org/docs/10/static/libpq-pgservice.html)\).
* `PGOPTIONS` behaves the same as the [options](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-OPTIONS) connection parameter.
* `PGAPPNAME` behaves the same as the [application\_name](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-APPLICATION-NAME) connection parameter.
* `PGSSLMODE` behaves the same as the [sslmode](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLMODE) connection parameter.
* `PGREQUIRESSL` behaves the same as the [requiressl](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-REQUIRESSL) connection parameter. This environment variable is deprecated in favor of the `PGSSLMODE` variable; setting both variables suppresses the effect of this one.
* `PGSSLCOMPRESSION` behaves the same as the [sslcompression](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLCOMPRESSION) connection parameter.
* `PGSSLCERT` behaves the same as the [sslcert](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLCERT) connection parameter.
* `PGSSLKEY` behaves the same as the [sslkey](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLKEY) connection parameter.
* `PGSSLROOTCERT` behaves the same as the [sslrootcert](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT) connection parameter.
* `PGSSLCRL` behaves the same as the [sslcrl](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) connection parameter.
* `PGREQUIREPEER` behaves the same as the [requirepeer](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-REQUIREPEER) connection parameter.
* `PGKRBSRVNAME` behaves the same as the [krbsrvname](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-KRBSRVNAME) connection parameter.
* `PGGSSLIB` behaves the same as the [gsslib](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-GSSLIB) connection parameter.
* `PGCONNECT_TIMEOUT` behaves the same as the [connect\_timeout](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-CONNECT-TIMEOUT) connection parameter.
* `PGCLIENTENCODING` behaves the same as the [client\_encoding](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-CLIENT-ENCODING) connection parameter.
* `PGTARGETSESSIONATTRS` behaves the same as the [target\_session\_attrs](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-TARGET-SESSION-ATTRS) connection parameter.

以下環境變數可用於指定每個 PostgreSQL 連線的預設行為。（有關基於每個使用者或每個資料庫設定預設行為的方法，另請參閱 [ALTER ROLE](../../reference/sql-commands/alter-role.md) 和 [ALTER DATABASE](../../reference/sql-commands/alter-database.md) 指令。）

* `PGDATESTYLE` 設定日期/時間表示的預設樣式。 （相當於 SET datestyle TO ....）
* `PGTZ`設定預設時區。 （相當於 `SET timezone TO ....`）
* `PGGEQO` 設定 genetic 查詢最佳化程序的預設模式。（相當於 `SET geqo TO ....`）

有關這些環境變數的正確值的資訊，請參閱 SQL 指令 [SET](../../reference/sql-commands/set.md)。

以下環境變數決定了 libpq 的內部行為；它們會覆寫編譯時的預設值。

* `PGSYSCONFDIR` 設定包含 pg\_service.conf 檔案的目錄，在未來版本中可能用於設定其他系統範圍的組態檔案。
* `PGLOCALEDIR` 設定包含用於訊息本地化的區域設定檔案的目錄。

