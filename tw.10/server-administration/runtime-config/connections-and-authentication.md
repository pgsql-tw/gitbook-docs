---
description: 版本：10
---

# 19.3. Connections and Authentication

## 19.3.1. Connection Settings

`listen_addresses` \(`string`\)

Specifies the TCP/IP address\(es\) on which the server is to listen for connections from client applications. The value takes the form of a comma-separated list of host names and/or numeric IP addresses. The special entry `*`corresponds to all available IP interfaces. The entry `0.0.0.0` allows listening for all IPv4 addresses and `::` allows listening for all IPv6 addresses. If the list is empty, the server does not listen on any IP interface at all, in which case only Unix-domain sockets can be used to connect to it. The default value is localhost, which allows only local TCP/IP “loopback” connections to be made. While client authentication \([Chapter 20](https://www.postgresql.org/docs/10/static/client-authentication.html)\) allows fine-grained control over who can access the server, `listen_addresses` controls which interfaces accept connection attempts, which can help prevent repeated malicious connection requests on insecure network interfaces. This parameter can only be set at server start.

`port` \(`integer`\)

The TCP port the server listens on; 5432 by default. Note that the same port number is used for all IP addresses the server listens on. This parameter can only be set at server start.

`max_connections` \(`integer`\)

Determines the maximum number of concurrent connections to the database server. The default is typically 100 connections, but might be less if your kernel settings will not support it \(as determined during initdb\). This parameter can only be set at server start.

When running a standby server, you must set this parameter to the same or higher value than on the master server. Otherwise, queries will not be allowed in the standby server.

`superuser_reserved_connections` \(`integer`\)

Determines the number of connection “slots” that are reserved for connections by PostgreSQL superusers. At most [max\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) connections can ever be active simultaneously. Whenever the number of active concurrent connections is at least `max_connections` minus `superuser_reserved_connections`, new connections will be accepted only for superusers, and no new replication connections will be accepted.

The default value is three connections. The value must be less than the value of `max_connections`. This parameter can only be set at server start.

`unix_socket_directories` \(`string`\)

Specifies the directory of the Unix-domain socket\(s\) on which the server is to listen for connections from client applications. Multiple sockets can be created by listing multiple directories separated by commas. Whitespace between entries is ignored; surround a directory name with double quotes if you need to include whitespace or commas in the name. An empty value specifies not listening on any Unix-domain sockets, in which case only TCP/IP sockets can be used to connect to the server. The default value is normally `/tmp`, but that can be changed at build time. This parameter can only be set at server start.

In addition to the socket file itself, which is named `.s.PGSQL.`_`nnnn`_ where _`nnnn`_ is the server's port number, an ordinary file named `.s.PGSQL.`_`nnnn`_.lock will be created in each of the `unix_socket_directories` directories. Neither file should ever be removed manually.

This parameter is irrelevant on Windows, which does not have Unix-domain sockets.

`unix_socket_group` \(`string`\)

Sets the owning group of the Unix-domain socket\(s\). \(The owning user of the sockets is always the user that starts the server.\) In combination with the parameter `unix_socket_permissions` this can be used as an additional access control mechanism for Unix-domain connections. By default this is the empty string, which uses the default group of the server user. This parameter can only be set at server start.

This parameter is irrelevant on Windows, which does not have Unix-domain sockets.

`unix_socket_permissions` \(`integer`\)

Sets the access permissions of the Unix-domain socket\(s\). Unix-domain sockets use the usual Unix file system permission set. The parameter value is expected to be a numeric mode specified in the format accepted by the `chmod` and `umask` system calls. \(To use the customary octal format the number must start with a `0` \(zero\).\)

The default permissions are `0777`, meaning anyone can connect. Reasonable alternatives are `0770` \(only user and group, see also `unix_socket_group`\) and `0700` \(only user\). \(Note that for a Unix-domain socket, only write permission matters, so there is no point in setting or revoking read or execute permissions.\)

This access control mechanism is independent of the one described in [Chapter 20](https://www.postgresql.org/docs/10/static/client-authentication.html).

This parameter can only be set at server start.

This parameter is irrelevant on systems, notably Solaris as of Solaris 10, that ignore socket permissions entirely. There, one can achieve a similar effect by pointing `unix_socket_directories` to a directory having search permission limited to the desired audience. This parameter is also irrelevant on Windows, which does not have Unix-domain sockets.

`bonjour` \(`boolean`\)

Enables advertising the server's existence via Bonjour. The default is off. This parameter can only be set at server start.

`bonjour_name` \(`string`\)

Specifies the Bonjour service name. The computer name is used if this parameter is set to the empty string `''` \(which is the default\). This parameter is ignored if the server was not compiled with Bonjour support. This parameter can only be set at server start.

`tcp_keepalives_idle` \(`integer`\)

Specifies the number of seconds of inactivity after which TCP should send a keepalive message to the client. A value of 0 uses the system default. This parameter is supported only on systems that support `TCP_KEEPIDLE` or an equivalent socket option, and on Windows; on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

#### Note

On Windows, a value of 0 will set this parameter to 2 hours, since Windows does not provide a way to read the system default value.

`tcp_keepalives_interval` \(`integer`\)

Specifies the number of seconds after which a TCP keepalive message that is not acknowledged by the client should be retransmitted. A value of 0 uses the system default. This parameter is supported only on systems that support `TCP_KEEPINTVL` or an equivalent socket option, and on Windows; on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

#### Note

On Windows, a value of 0 will set this parameter to 1 second, since Windows does not provide a way to read the system default value.

`tcp_keepalives_count` \(`integer`\)

Specifies the number of TCP keepalives that can be lost before the server's connection to the client is considered dead. A value of 0 uses the system default. This parameter is supported only on systems that support `TCP_KEEPCNT` or an equivalent socket option; on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

#### Note

This parameter is not supported on Windows, and must be zero.

## 19.3.2. Security and Authentication

`authentication_timeout` \(`integer`\)

Maximum time to complete client authentication, in seconds. If a would-be client has not completed the authentication protocol in this much time, the server closes the connection. This prevents hung clients from occupying a connection indefinitely. The default is one minute \(`1m`\). This parameter can only be set in the `postgresql.conf` file or on the server command line.

`ssl` \(`boolean`\)

Enables SSL connections. Please read [Section 18.9](https://www.postgresql.org/docs/10/static/ssl-tcp.html) before using this. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `off`.

`ssl_ca_file` \(`string`\)

Specifies the name of the file containing the SSL server certificate authority \(CA\). Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is empty, meaning no CA file is loaded, and client certificate verification is not performed.

In previous releases of PostgreSQL, the name of this file was hard-coded as `root.crt`.

`ssl_cert_file` \(`string`\)

Specifies the name of the file containing the SSL server certificate. Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `server.crt`.

`ssl_crl_file` \(`string`\)

Specifies the name of the file containing the SSL server certificate revocation list \(CRL\). Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is empty, meaning no CRL file is loaded.

In previous releases of PostgreSQL, the name of this file was hard-coded as `root.crl`.

`ssl_key_file` \(`string`\)

Specifies the name of the file containing the SSL server private key. Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `server.key`.

`ssl_ciphers` \(`string`\)

Specifies a list of SSL cipher suites that are allowed to be used on secure connections. See the ciphers manual page in the OpenSSL package for the syntax of this setting and a list of supported values. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default value is `HIGH:MEDIUM:+3DES:!aNULL`. The default is usually a reasonable choice unless you have specific security requirements.

Explanation of the default value:`HIGH`

Cipher suites that use ciphers from `HIGH` group \(e.g., AES, Camellia, 3DES\)`MEDIUM`

Cipher suites that use ciphers from `MEDIUM` group \(e.g., RC4, SEED\)`+3DES`

The OpenSSL default order for `HIGH` is problematic because it orders 3DES higher than AES128. This is wrong because 3DES offers less security than AES128, and it is also much slower. `+3DES` reorders it after all other `HIGH` and `MEDIUM` ciphers.`!aNULL`

Disables anonymous cipher suites that do no authentication. Such cipher suites are vulnerable to man-in-the-middle attacks and therefore should not be used.

Available cipher suite details will vary across OpenSSL versions. Use the command `openssl ciphers -v 'HIGH:MEDIUM:+3DES:!aNULL'` to see actual details for the currently installed OpenSSL version. Note that this list is filtered at run time based on the server key type.

`ssl_prefer_server_ciphers` \(`boolean`\)

Specifies whether to use the server's SSL cipher preferences, rather than the client's. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `true`.

Older PostgreSQL versions do not have this setting and always use the client's preferences. This setting is mainly for backward compatibility with those versions. Using the server's preferences is usually better because it is more likely that the server is appropriately configured.

`ssl_ecdh_curve` \(`string`\)

Specifies the name of the curve to use in ECDH key exchange. It needs to be supported by all clients that connect. It does not need to be the same curve used by the server's Elliptic Curve key. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `prime256v1`.

OpenSSL names for the most common curves are: `prime256v1` \(NIST P-256\), `secp384r1` \(NIST P-384\), `secp521r1` \(NIST P-521\). The full list of available curves can be shown with the command `openssl ecparam -list_curves`. Not all of them are usable in TLS though.

`password_encryption` \(`enum`\)

When a password is specified in [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html) or [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html), this parameter determines the algorithm to use to encrypt the password. The default value is `md5`, which stores the password as an MD5 hash \(`on` is also accepted, as alias for `md5`\). Setting this parameter to `scram-sha-256` will encrypt the password with SCRAM-SHA-256.

Note that older clients might lack support for the SCRAM authentication mechanism, and hence not work with passwords encrypted with SCRAM-SHA-256. See [Section 20.3.2](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PASSWORD) for more details.

`ssl_dh_params_file` \(`string`\)

Specifies the name of the file containing Diffie-Hellman parameters used for so-called ephemeral DH family of SSL ciphers. The default is empty, in which case compiled-in default DH parameters used. Using custom DH parameters reduces the exposure if an attacker manages to crack the well-known compiled-in DH parameters. You can create your own DH parameters file with the command `openssl dhparam -out dhparams.pem 2048`.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`krb_server_keyfile` \(`string`\)

Sets the location of the Kerberos server key file. See [Section 20.3.3](https://www.postgresql.org/docs/10/static/auth-methods.html#GSSAPI-AUTH) for details. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`krb_caseins_users` \(`boolean`\)

Sets whether GSSAPI user names should be treated case-insensitively. The default is `off` \(case sensitive\). This parameter can only be set in the `postgresql.conf` file or on the server command line.

`db_user_namespace` \(`boolean`\)

This parameter enables per-database user names. It is off by default. This parameter can only be set in the `postgresql.conf` file or on the server command line.

If this is on, you should create users as _`username@dbname`_. When _`username`_ is passed by a connecting client, `@` and the database name are appended to the user name and that database-specific user name is looked up by the server. Note that when you create users with names containing `@` within the SQL environment, you will need to quote the user name.

With this parameter enabled, you can still create ordinary global users. Simply append `@` when specifying the user name in the client, e.g. `joe@`. The `@` will be stripped off before the user name is looked up by the server.

`db_user_namespace` causes the client's and server's user name representation to differ. Authentication checks are always done with the server's user name so authentication methods must be configured for the server's user name, not the client's. Because `md5` uses the user name as salt on both the client and server, `md5` cannot be used with `db_user_namespace`.

#### Note

This feature is intended as a temporary measure until a complete solution is found. At that time, this option will be removed.

