# 33.14. Environment Variables

The following environment variables can be used to select default connection parameter values, which will be used by `PQconnectdb`, `PQsetdbLogin` and `PQsetdb` if no value is directly specified by the calling code. These are useful to avoid hard-coding database connection information into simple client applications, for example.

* `PGHOST` behaves the same as the [host](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-HOST) connection parameter.
* `PGHOSTADDR` behaves the same as the [hostaddr](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-HOSTADDR) connection parameter. This can be set instead of or in addition to `PGHOST` to avoid DNS lookup overhead.
* `PGPORT` behaves the same as the [port](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-PORT) connection parameter.
* `PGDATABASE` behaves the same as the [dbname](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-DBNAME) connection parameter.
* `PGUSER` behaves the same as the [user](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-USER) connection parameter.
* `PGPASSWORD` behaves the same as the [password](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-PASSWORD) connection parameter. Use of this environment variable is not recommended for security reasons, as some operating systems allow non-root users to see process environment variables via ps; instead consider using a password file \(see [Section 33.15](https://www.postgresql.org/docs/10/static/libpq-pgpass.html)\).
* `PGPASSFILE` behaves the same as the [passfile](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNECT-PASSFILE) connection parameter.
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

The following environment variables can be used to specify default behavior for each PostgreSQL session. \(See also the [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html) and [ALTER DATABASE](https://www.postgresql.org/docs/10/static/sql-alterdatabase.html) commands for ways to set default behavior on a per-user or per-database basis.\)

* `PGDATESTYLE` sets the default style of date/time representation. \(Equivalent to `SET datestyle TO ...`.\)
* `PGTZ` sets the default time zone. \(Equivalent to `SET timezone TO ...`.\)
* `PGGEQO` sets the default mode for the genetic query optimizer. \(Equivalent to `SET geqo TO ...`.\)

Refer to the SQL command [SET](https://www.postgresql.org/docs/10/static/sql-set.html) for information on correct values for these environment variables.

The following environment variables determine internal behavior of libpq; they override compiled-in defaults.

* `PGSYSCONFDIR` sets the directory containing the `pg_service.conf` file and in a future version possibly other system-wide configuration files.
* `PGLOCALEDIR` sets the directory containing the `locale` files for message localization.

