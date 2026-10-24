<a id="LIBPQ-ENVARS"></a>

## 32.15. 環境變數 [#](#libpq-envars) <a href="#libpq-envars" id="libpq-envars"></a>

<a id="id-1.7.3.22.2"></a>

下列環境變數可用來選擇連線參數的預設值；若呼叫端程式碼沒有直接指定值，[`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB)、[`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN) 與 [`PQsetdb`](libpq-connect.md#LIBPQ-PQSETDB) 就會使用這些值。舉例來說，這些環境變數有助於避免把資料庫連線資訊寫死在簡單的用戶端應用程式中。

* <a id="id-1.7.3.22.3.4.1.1.1"></a>
  `PGHOST` 的行為與 [host](libpq-connect.md#LIBPQ-CONNECT-HOST) 連線參數相同。
* <a id="id-1.7.3.22.3.4.2.1.1"></a>
  `PGSSLNEGOTIATION` 的行為與 [sslnegotiation](libpq-connect.md#LIBPQ-CONNECT-SSLNEGOTIATION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.3.1.1"></a>
  `PGHOSTADDR` 的行為與 [hostaddr](libpq-connect.md#LIBPQ-CONNECT-HOSTADDR) 連線參數相同。
  可以設定此變數來取代 `PGHOST`，或與之一併設定，以避免 DNS 查詢的額外負擔。
* <a id="id-1.7.3.22.3.4.4.1.1"></a>
  `PGPORT` 的行為與 [port](libpq-connect.md#LIBPQ-CONNECT-PORT) 連線參數相同。
* <a id="id-1.7.3.22.3.4.5.1.1"></a>
  `PGDATABASE` 的行為與 [dbname](libpq-connect.md#LIBPQ-CONNECT-DBNAME) 連線參數相同。
* <a id="id-1.7.3.22.3.4.6.1.1"></a>
  `PGUSER` 的行為與 [user](libpq-connect.md#LIBPQ-CONNECT-USER) 連線參數相同。
* <a id="id-1.7.3.22.3.4.7.1.1"></a>
  `PGPASSWORD` 的行為與 [password](libpq-connect.md#LIBPQ-CONNECT-PASSWORD) 連線參數相同。
  基於安全考量，不建議使用此環境變數，因為某些作業系統允許非 root 使用者透過 ps 查看程序的環境變數；請改為考慮使用密碼檔（請參閱[第 32.16 節](libpq-pgpass.md)）。
* <a id="id-1.7.3.22.3.4.8.1.1"></a>
  `PGPASSFILE` 的行為與 [passfile](libpq-connect.md#LIBPQ-CONNECT-PASSFILE) 連線參數相同。
* <a id="id-1.7.3.22.3.4.9.1.1"></a>
  `PGREQUIREAUTH` 的行為與 [require_auth](libpq-connect.md#LIBPQ-CONNECT-REQUIRE-AUTH) 連線參數相同。
* <a id="id-1.7.3.22.3.4.10.1.1"></a>
  `PGCHANNELBINDING` 的行為與 [channel_binding](libpq-connect.md#LIBPQ-CONNECT-CHANNEL-BINDING) 連線參數相同。
* <a id="id-1.7.3.22.3.4.11.1.1"></a>
  `PGSERVICE` 的行為與 [service](libpq-connect.md#LIBPQ-CONNECT-SERVICE) 連線參數相同。
* <a id="id-1.7.3.22.3.4.12.1.1"></a>
  `PGSERVICEFILE` 指定個別使用者的連線服務檔名稱（請參閱[第 32.17 節](libpq-pgservice.md)）。預設為 `~/.pg_service.conf`，在 Microsoft Windows 上則為 `%APPDATA%\postgresql\.pg_service.conf`。
* <a id="id-1.7.3.22.3.4.13.1.1"></a>
  `PGOPTIONS` 的行為與 [options](libpq-connect.md#LIBPQ-CONNECT-OPTIONS) 連線參數相同。
* <a id="id-1.7.3.22.3.4.14.1.1"></a>
  `PGAPPNAME` 的行為與 [application_name](libpq-connect.md#LIBPQ-CONNECT-APPLICATION-NAME) 連線參數相同。
* <a id="id-1.7.3.22.3.4.15.1.1"></a>
  `PGSSLMODE` 的行為與 [sslmode](libpq-connect.md#LIBPQ-CONNECT-SSLMODE) 連線參數相同。
* <a id="id-1.7.3.22.3.4.16.1.1"></a>
  `PGREQUIRESSL` 的行為與 [requiressl](libpq-connect.md#LIBPQ-CONNECT-REQUIRESSL) 連線參數相同。
  此環境變數已棄用，請改用 `PGSSLMODE` 變數；若同時設定這兩個變數，此變數將不會生效。
* <a id="id-1.7.3.22.3.4.17.1.1"></a>
  `PGSSLCOMPRESSION` 的行為與 [sslcompression](libpq-connect.md#LIBPQ-CONNECT-SSLCOMPRESSION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.18.1.1"></a>
  `PGSSLCERT` 的行為與 [sslcert](libpq-connect.md#LIBPQ-CONNECT-SSLCERT) 連線參數相同。
* <a id="id-1.7.3.22.3.4.19.1.1"></a>
  `PGSSLKEY` 的行為與 [sslkey](libpq-connect.md#LIBPQ-CONNECT-SSLKEY) 連線參數相同。
* <a id="id-1.7.3.22.3.4.20.1.1"></a>
  `PGSSLCERTMODE` 的行為與 [sslcertmode](libpq-connect.md#LIBPQ-CONNECT-SSLCERTMODE) 連線參數相同。
* <a id="id-1.7.3.22.3.4.21.1.1"></a>
  `PGSSLROOTCERT` 的行為與 [sslrootcert](libpq-connect.md#LIBPQ-CONNECT-SSLROOTCERT) 連線參數相同。
* <a id="id-1.7.3.22.3.4.22.1.1"></a>
  `PGSSLCRL` 的行為與 [sslcrl](libpq-connect.md#LIBPQ-CONNECT-SSLCRL) 連線參數相同。
* <a id="id-1.7.3.22.3.4.23.1.1"></a>
  `PGSSLCRLDIR` 的行為與 [sslcrldir](libpq-connect.md#LIBPQ-CONNECT-SSLCRLDIR) 連線參數相同。
* <a id="id-1.7.3.22.3.4.24.1.1"></a>
  `PGSSLSNI` 的行為與 [sslsni](libpq-connect.md#LIBPQ-CONNECT-SSLSNI) 連線參數相同。
* <a id="id-1.7.3.22.3.4.25.1.1"></a>
  `PGREQUIREPEER` 的行為與 [requirepeer](libpq-connect.md#LIBPQ-CONNECT-REQUIREPEER) 連線參數相同。
* <a id="id-1.7.3.22.3.4.26.1.1"></a>
  `PGSSLMINPROTOCOLVERSION` 的行為與 [ssl_min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.27.1.1"></a>
  `PGSSLMAXPROTOCOLVERSION` 的行為與 [ssl_max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.28.1.1"></a>
  `PGGSSENCMODE` 的行為與 [gssencmode](libpq-connect.md#LIBPQ-CONNECT-GSSENCMODE) 連線參數相同。
* <a id="id-1.7.3.22.3.4.29.1.1"></a>
  `PGKRBSRVNAME` 的行為與 [krbsrvname](libpq-connect.md#LIBPQ-CONNECT-KRBSRVNAME) 連線參數相同。
* <a id="id-1.7.3.22.3.4.30.1.1"></a>
  `PGGSSLIB` 的行為與 [gsslib](libpq-connect.md#LIBPQ-CONNECT-GSSLIB) 連線參數相同。
* <a id="id-1.7.3.22.3.4.31.1.1"></a>
  `PGGSSDELEGATION` 的行為與 [gssdelegation](libpq-connect.md#LIBPQ-CONNECT-GSSDELEGATION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.32.1.1"></a>
  `PGCONNECT_TIMEOUT` 的行為與 [connect_timeout](libpq-connect.md#LIBPQ-CONNECT-CONNECT-TIMEOUT) 連線參數相同。
* <a id="id-1.7.3.22.3.4.33.1.1"></a>
  `PGCLIENTENCODING` 的行為與 [client_encoding](libpq-connect.md#LIBPQ-CONNECT-CLIENT-ENCODING) 連線參數相同。
* <a id="id-1.7.3.22.3.4.34.1.1"></a>
  `PGTARGETSESSIONATTRS` 的行為與 [target_session_attrs](libpq-connect.md#LIBPQ-CONNECT-TARGET-SESSION-ATTRS) 連線參數相同。
* <a id="id-1.7.3.22.3.4.35.1.1"></a>
  `PGLOADBALANCEHOSTS` 的行為與 [load_balance_hosts](libpq-connect.md#LIBPQ-CONNECT-LOAD-BALANCE-HOSTS) 連線參數相同。
* <a id="id-1.7.3.22.3.4.36.1.1"></a>
  `PGMINPROTOCOLVERSION` 的行為與 [min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MIN-PROTOCOL-VERSION) 連線參數相同。
* <a id="id-1.7.3.22.3.4.37.1.1"></a>
  `PGMAXPROTOCOLVERSION` 的行為與 [max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MAX-PROTOCOL-VERSION) 連線參數相同。

下列環境變數可用來指定每個 PostgreSQL 工作階段的預設行為。（關於以個別使用者或個別資料庫為單位設定預設行為的方法，另請參閱 [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 與 [ALTER DATABASE](../../reference/sql-commands/sql-alterdatabase.md) 命令。）

* <a id="id-1.7.3.22.4.4.1.1.1"></a>
  `PGDATESTYLE` 設定日期／時間表示法的預設樣式。（等同於 `SET datestyle TO
  ...`。）
* <a id="id-1.7.3.22.4.4.2.1.1"></a>
  `PGTZ` 設定預設時區。（等同於 `SET timezone TO ...`。）
* <a id="id-1.7.3.22.4.4.3.1.1"></a>
  `PGGEQO` 設定基因查詢最佳化器的預設模式。（等同於 `SET geqo TO ...`。）

關於這些環境變數的正確值，請參閱 SQL 命令 [SET](../../reference/sql-commands/sql-set.md)。

下列環境變數決定 libpq 的內部行為；它們會覆寫編譯時內建的預設值。

* <a id="id-1.7.3.22.5.2.1.1.1"></a>
  `PGSYSCONFDIR` 設定包含 `pg_service.conf` 檔案的目錄，在未來的版本中也可能包含其他全系統的設定檔。
* <a id="id-1.7.3.22.5.2.2.1.1"></a>
  `PGLOCALEDIR` 設定包含用於訊息在地化之 `locale` 檔案的目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-envars.html)（原文版本：18.6；核對日期：2026-10-18）
