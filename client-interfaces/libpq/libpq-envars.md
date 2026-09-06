## 32.15. Environment Variables [#](#LIBPQ-ENVARS)

<a id="id-1.7.3.22.2"></a>

The following environment variables can be used to select default
connection parameter values, which will be used by
[`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB), [`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN) and
[`PQsetdb`](libpq-connect.md#LIBPQ-PQSETDB) if no value is directly specified by the calling
code. These are useful to avoid hard-coding database connection
information into simple client applications, for example.

* <a id="id-1.7.3.22.3.4.1.1.1"></a>
  `PGHOST` behaves the same as the [host](libpq-connect.md#LIBPQ-CONNECT-HOST) connection parameter.
* <a id="id-1.7.3.22.3.4.2.1.1"></a>
  `PGSSLNEGOTIATION` behaves the same as the [sslnegotiation](libpq-connect.md#LIBPQ-CONNECT-SSLNEGOTIATION) connection parameter.
* <a id="id-1.7.3.22.3.4.3.1.1"></a>
  `PGHOSTADDR` behaves the same as the [hostaddr](libpq-connect.md#LIBPQ-CONNECT-HOSTADDR) connection parameter.
  This can be set instead of or in addition to `PGHOST`
  to avoid DNS lookup overhead.
* <a id="id-1.7.3.22.3.4.4.1.1"></a>
  `PGPORT` behaves the same as the [port](libpq-connect.md#LIBPQ-CONNECT-PORT) connection parameter.
* <a id="id-1.7.3.22.3.4.5.1.1"></a>
  `PGDATABASE` behaves the same as the [dbname](libpq-connect.md#LIBPQ-CONNECT-DBNAME) connection parameter.
* <a id="id-1.7.3.22.3.4.6.1.1"></a>
  `PGUSER` behaves the same as the [user](libpq-connect.md#LIBPQ-CONNECT-USER) connection parameter.
* <a id="id-1.7.3.22.3.4.7.1.1"></a>
  `PGPASSWORD` behaves the same as the [password](libpq-connect.md#LIBPQ-CONNECT-PASSWORD) connection parameter.
  Use of this environment variable
  is not recommended for security reasons, as some operating systems
  allow non-root users to see process environment variables via
  ps; instead consider using a password file
  (see [Section 32.16](libpq-pgpass.md)).
* <a id="id-1.7.3.22.3.4.8.1.1"></a>
  `PGPASSFILE` behaves the same as the [passfile](libpq-connect.md#LIBPQ-CONNECT-PASSFILE) connection parameter.
* <a id="id-1.7.3.22.3.4.9.1.1"></a>
  `PGREQUIREAUTH` behaves the same as the [require_auth](libpq-connect.md#LIBPQ-CONNECT-REQUIRE-AUTH) connection parameter.
* <a id="id-1.7.3.22.3.4.10.1.1"></a>
  `PGCHANNELBINDING` behaves the same as the [channel_binding](libpq-connect.md#LIBPQ-CONNECT-CHANNEL-BINDING) connection parameter.
* <a id="id-1.7.3.22.3.4.11.1.1"></a>
  `PGSERVICE` behaves the same as the [service](libpq-connect.md#LIBPQ-CONNECT-SERVICE) connection parameter.
* <a id="id-1.7.3.22.3.4.12.1.1"></a>
  `PGSERVICEFILE` specifies the name of the per-user
  connection service file
  (see [Section 32.17](libpq-pgservice.md)).
  Defaults to `~/.pg_service.conf`, or
  `%APPDATA%\postgresql\.pg_service.conf` on
  Microsoft Windows.
* <a id="id-1.7.3.22.3.4.13.1.1"></a>
  `PGOPTIONS` behaves the same as the [options](libpq-connect.md#LIBPQ-CONNECT-OPTIONS) connection parameter.
* <a id="id-1.7.3.22.3.4.14.1.1"></a>
  `PGAPPNAME` behaves the same as the [application_name](libpq-connect.md#LIBPQ-CONNECT-APPLICATION-NAME) connection parameter.
* <a id="id-1.7.3.22.3.4.15.1.1"></a>
  `PGSSLMODE` behaves the same as the [sslmode](libpq-connect.md#LIBPQ-CONNECT-SSLMODE) connection parameter.
* <a id="id-1.7.3.22.3.4.16.1.1"></a>
  `PGREQUIRESSL` behaves the same as the [requiressl](libpq-connect.md#LIBPQ-CONNECT-REQUIRESSL) connection parameter.
  This environment variable is deprecated in favor of the
  `PGSSLMODE` variable; setting both variables suppresses the
  effect of this one.
* <a id="id-1.7.3.22.3.4.17.1.1"></a>
  `PGSSLCOMPRESSION` behaves the same as the [sslcompression](libpq-connect.md#LIBPQ-CONNECT-SSLCOMPRESSION) connection parameter.
* <a id="id-1.7.3.22.3.4.18.1.1"></a>
  `PGSSLCERT` behaves the same as the [sslcert](libpq-connect.md#LIBPQ-CONNECT-SSLCERT) connection parameter.
* <a id="id-1.7.3.22.3.4.19.1.1"></a>
  `PGSSLKEY` behaves the same as the [sslkey](libpq-connect.md#LIBPQ-CONNECT-SSLKEY) connection parameter.
* <a id="id-1.7.3.22.3.4.20.1.1"></a>
  `PGSSLCERTMODE` behaves the same as the [sslcertmode](libpq-connect.md#LIBPQ-CONNECT-SSLCERTMODE) connection parameter.
* <a id="id-1.7.3.22.3.4.21.1.1"></a>
  `PGSSLROOTCERT` behaves the same as the [sslrootcert](libpq-connect.md#LIBPQ-CONNECT-SSLROOTCERT) connection parameter.
* <a id="id-1.7.3.22.3.4.22.1.1"></a>
  `PGSSLCRL` behaves the same as the [sslcrl](libpq-connect.md#LIBPQ-CONNECT-SSLCRL) connection parameter.
* <a id="id-1.7.3.22.3.4.23.1.1"></a>
  `PGSSLCRLDIR` behaves the same as the [sslcrldir](libpq-connect.md#LIBPQ-CONNECT-SSLCRLDIR) connection parameter.
* <a id="id-1.7.3.22.3.4.24.1.1"></a>
  `PGSSLSNI` behaves the same as the [sslsni](libpq-connect.md#LIBPQ-CONNECT-SSLSNI) connection parameter.
* <a id="id-1.7.3.22.3.4.25.1.1"></a>
  `PGREQUIREPEER` behaves the same as the [requirepeer](libpq-connect.md#LIBPQ-CONNECT-REQUIREPEER) connection parameter.
* <a id="id-1.7.3.22.3.4.26.1.1"></a>
  `PGSSLMINPROTOCOLVERSION` behaves the same as the [ssl_min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION) connection parameter.
* <a id="id-1.7.3.22.3.4.27.1.1"></a>
  `PGSSLMAXPROTOCOLVERSION` behaves the same as the [ssl_max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION) connection parameter.
* <a id="id-1.7.3.22.3.4.28.1.1"></a>
  `PGGSSENCMODE` behaves the same as the [gssencmode](libpq-connect.md#LIBPQ-CONNECT-GSSENCMODE) connection parameter.
* <a id="id-1.7.3.22.3.4.29.1.1"></a>
  `PGKRBSRVNAME` behaves the same as the [krbsrvname](libpq-connect.md#LIBPQ-CONNECT-KRBSRVNAME) connection parameter.
* <a id="id-1.7.3.22.3.4.30.1.1"></a>
  `PGGSSLIB` behaves the same as the [gsslib](libpq-connect.md#LIBPQ-CONNECT-GSSLIB) connection parameter.
* <a id="id-1.7.3.22.3.4.31.1.1"></a>
  `PGGSSDELEGATION` behaves the same as the [gssdelegation](libpq-connect.md#LIBPQ-CONNECT-GSSDELEGATION) connection parameter.
* <a id="id-1.7.3.22.3.4.32.1.1"></a>
  `PGCONNECT_TIMEOUT` behaves the same as the [connect_timeout](libpq-connect.md#LIBPQ-CONNECT-CONNECT-TIMEOUT) connection parameter.
* <a id="id-1.7.3.22.3.4.33.1.1"></a>
  `PGCLIENTENCODING` behaves the same as the [client_encoding](libpq-connect.md#LIBPQ-CONNECT-CLIENT-ENCODING) connection parameter.
* <a id="id-1.7.3.22.3.4.34.1.1"></a>
  `PGTARGETSESSIONATTRS` behaves the same as the [target_session_attrs](libpq-connect.md#LIBPQ-CONNECT-TARGET-SESSION-ATTRS) connection parameter.
* <a id="id-1.7.3.22.3.4.35.1.1"></a>
  `PGLOADBALANCEHOSTS` behaves the same as the [load_balance_hosts](libpq-connect.md#LIBPQ-CONNECT-LOAD-BALANCE-HOSTS) connection parameter.
* <a id="id-1.7.3.22.3.4.36.1.1"></a>
  `PGMINPROTOCOLVERSION` behaves the same as the [min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MIN-PROTOCOL-VERSION) connection parameter.
* <a id="id-1.7.3.22.3.4.37.1.1"></a>
  `PGMAXPROTOCOLVERSION` behaves the same as the [max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MAX-PROTOCOL-VERSION) connection parameter.

The following environment variables can be used to specify default
behavior for each PostgreSQL session. (See
also the [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md)
and [ALTER DATABASE](../../reference/sql-commands/sql-alterdatabase.md)
commands for ways to set default behavior on a per-user or per-database
basis.)

* <a id="id-1.7.3.22.4.4.1.1.1"></a>
  `PGDATESTYLE` sets the default style of date/time
  representation. (Equivalent to `SET datestyle TO
  ...`.)
* <a id="id-1.7.3.22.4.4.2.1.1"></a>
  `PGTZ` sets the default time zone. (Equivalent to
  `SET timezone TO ...`.)
* <a id="id-1.7.3.22.4.4.3.1.1"></a>
  `PGGEQO` sets the default mode for the genetic query
  optimizer. (Equivalent to `SET geqo TO ...`.)

Refer to the SQL command [SET](../../reference/sql-commands/sql-set.md)
for information on correct values for these
environment variables.

The following environment variables determine internal behavior of
libpq; they override compiled-in defaults.

* <a id="id-1.7.3.22.5.2.1.1.1"></a>
  `PGSYSCONFDIR` sets the directory containing the
  `pg_service.conf` file and in a future version
  possibly other system-wide configuration files.
* <a id="id-1.7.3.22.5.2.2.1.1"></a>
  `PGLOCALEDIR` sets the directory containing the
  `locale` files for message localization.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-envars.html)（英文原文，待翻譯）
