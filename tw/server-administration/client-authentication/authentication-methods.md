# 20.3. Authentication Methods

The following subsections describe the authentication methods in more detail.

#### 20.3.1. Trust Authentication

When `trust` authentication is specified, PostgreSQL assumes that anyone who can connect to the server is authorized to access the database with whatever database user name they specify \(even superuser names\). Of course, restrictions made in the `database` and `user` columns still apply. This method should only be used when there is adequate operating-system-level protection on connections to the server.

`trust` authentication is appropriate and very convenient for local connections on a single-user workstation. It is usually _not_ appropriate by itself on a multiuser machine. However, you might be able to use `trust` even on a multiuser machine, if you restrict access to the server's Unix-domain socket file using file-system permissions. To do this, set the `unix_socket_permissions` \(and possibly `unix_socket_group`\) configuration parameters as described in [Section 19.3](https://www.postgresql.org/docs/10/static/runtime-config-connection.html). Or you could set the `unix_socket_directories` configuration parameter to place the socket file in a suitably restricted directory.

Setting file-system permissions only helps for Unix-socket connections. Local TCP/IP connections are not restricted by file-system permissions. Therefore, if you want to use file-system permissions for local security, remove the `host ... 127.0.0.1 ...` line from `pg_hba.conf`, or change it to a non-`trust` authentication method.

`trust` authentication is only suitable for TCP/IP connections if you trust every user on every machine that is allowed to connect to the server by the `pg_hba.conf` lines that specify `trust`. It is seldom reasonable to use `trust` for any TCP/IP connections other than those from localhost \(127.0.0.1\).

#### 20.3.2. Password Authentication

There are several password-based authentication methods. These methods operate similarly but differ in how the users' passwords are stored on the server and how the password provided by a client is sent across the connection.`scram-sha-256`

The method `scram-sha-256` performs SCRAM-SHA-256 authentication, as described in [RFC 7677](https://tools.ietf.org/html/rfc7677). It is a challenge-response scheme that prevents password sniffing on untrusted connections and supports storing passwords on the server in a cryptographically hashed form that is thought to be secure.

This is the most secure of the currently provided methods, but it is not supported by older client libraries.`md5`

The method `md5` uses a custom less secure challenge-response mechanism. It prevents password sniffing and avoids storing passwords on the server in plain text but provides no protection if an attacker manages to steal the password hash from the server. Also, the MD5 hash algorithm is nowadays no longer considered secure against determined attacks.

The `md5` method cannot be used with the [db\_user\_namespace](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-DB-USER-NAMESPACE) feature.

To ease transition from the `md5` method to the newer SCRAM method, if `md5` is specified as a method in `pg_hba.conf` but the user's password on the server is encrypted for SCRAM \(see below\), then SCRAM-based authentication will automatically be chosen instead.`password`

The method `password` sends the password in clear-text and is therefore vulnerable to password “sniffing” attacks. It should always be avoided if possible. If the connection is protected by SSL encryption then `password` can be used safely, though. \(Though SSL certificate authentication might be a better choice if one is depending on using SSL\).

PostgreSQL database passwords are separate from operating system user passwords. The password for each database user is stored in the `pg_authid` system catalog. Passwords can be managed with the SQL commands [CREATE USER](https://www.postgresql.org/docs/10/static/sql-createuser.html) and [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html), e.g., **`CREATE USER foo WITH PASSWORD 'secret'`**, or the psql command `\password`. If no password has been set up for a user, the stored password is null and password authentication will always fail for that user.

The availability of the different password-based authentication methods depends on how a user's password on the server is encrypted \(or hashed, more accurately\). This is controlled by the configuration parameter [password\_encryption](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) at the time the password is set. If a password was encrypted using the `scram-sha-256` setting, then it can be used for the authentication methods `scram-sha-256` and `password` \(but password transmission will be in plain text in the latter case\). The authentication method specification `md5` will automatically switch to using the `scram-sha-256` method in this case, as explained above, so it will also work. If a password was encrypted using the `md5` setting, then it can be used only for the `md5`and `password` authentication method specifications \(again, with the password transmitted in plain text in the latter case\). \(Previous PostgreSQL releases supported storing the password on the server in plain text. This is no longer possible.\) To check the currently stored password hashes, see the system catalog `pg_authid`.

To upgrade an existing installation from `md5` to `scram-sha-256`, after having ensured that all client libraries in use are new enough to support SCRAM, set `password_encryption = 'scram-sha-256'` in `postgresql.conf`, make all users set new passwords, and change the authentication method specifications in `pg_hba.conf` to `scram-sha-256`.

#### 20.3.3. GSSAPI Authentication

GSSAPI is an industry-standard protocol for secure authentication defined in RFC 2743. PostgreSQL supports GSSAPI with Kerberos authentication according to RFC 1964. GSSAPIprovides automatic authentication \(single sign-on\) for systems that support it. The authentication itself is secure, but the data sent over the database connection will be sent unencrypted unless SSL is used.

GSSAPI support has to be enabled when PostgreSQL is built; see [Chapter 16](https://www.postgresql.org/docs/10/static/installation.html) for more information.

When GSSAPI uses Kerberos, it uses a standard principal in the format _`servicename`_/_`hostname`_@_`realm`_. The PostgreSQL server will accept any principal that is included in the keytab used by the server, but care needs to be taken to specify the correct principal details when making the connection from the client using the `krbsrvname` connection parameter. \(See also [Section 33.1.2](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS).\) The installation default can be changed from the default `postgres` at build time using `./configure --with-krb-srvnam=`_`whatever`_. In most environments, this parameter never needs to be changed. Some Kerberos implementations might require a different service name, such as Microsoft Active Directory which requires the service name to be in upper case \(`POSTGRES`\).

_`hostname`_ is the fully qualified host name of the server machine. The service principal's realm is the preferred realm of the server machine.

Client principals can be mapped to different PostgreSQL database user names with `pg_ident.conf`. For example, `pgusername@realm` could be mapped to just `pgusername`. Alternatively, you can use the full `username@realm` principal as the role name in PostgreSQL without any mapping.

PostgreSQL also supports a parameter to strip the realm from the principal. This method is supported for backwards compatibility and is strongly discouraged as it is then impossible to distinguish different users with the same user name but coming from different realms. To enable this, set `include_realm` to 0. For simple single-realm installations, doing that combined with setting the `krb_realm` parameter \(which checks that the principal's realm matches exactly what is in the `krb_realm` parameter\) is still secure; but this is a less capable approach compared to specifying an explicit mapping in `pg_ident.conf`.

Make sure that your server keytab file is readable \(and preferably only readable, not writable\) by the PostgreSQL server account. \(See also [Section 18.1](https://www.postgresql.org/docs/10/static/postgres-user.html).\) The location of the key file is specified by the [krb\_server\_keyfile](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-KRB-SERVER-KEYFILE) configuration parameter. The default is `/usr/local/pgsql/etc/krb5.keytab` \(or whatever directory was specified as `sysconfdir` at build time\). For security reasons, it is recommended to use a separate keytab just for the PostgreSQL server rather than opening up permissions on the system keytab file.

The keytab file is generated by the Kerberos software; see the Kerberos documentation for details. The following example is for MIT-compatible Kerberos 5 implementations:

```text
kadmin% ank -randkey postgres/server.my.domain.org
kadmin% ktadd -k krb5.keytab postgres/server.my.domain.org
```

When connecting to the database make sure you have a ticket for a principal matching the requested database user name. For example, for database user name `fred`, principal`fred@EXAMPLE.COM` would be able to connect. To also allow principal `fred/users.example.com@EXAMPLE.COM`, use a user name map, as described in [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html).

The following configuration options are supported for GSSAPI:`include_realm`

If set to 0, the realm name from the authenticated user principal is stripped off before being passed through the user name mapping \([Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html)\). This is discouraged and is primarily available for backwards compatibility, as it is not secure in multi-realm environments unless `krb_realm` is also used. It is recommended to leave `include_realm` set to the default \(1\) and to provide an explicit mapping in `pg_ident.conf` to convert principal names to PostgreSQL user names.`map`

Allows for mapping between system and database user names. See [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html) for details. For a GSSAPI/Kerberos principal, such as `username@EXAMPLE.COM` \(or, less commonly,`username/hostbased@EXAMPLE.COM`\), the user name used for mapping is `username@EXAMPLE.COM` \(or `username/hostbased@EXAMPLE.COM`, respectively\), unless `include_realm` has been set to 0, in which case `username` \(or `username/hostbased`\) is what is seen as the system user name when mapping.`krb_realm`

Sets the realm to match user principal names against. If this parameter is set, only users of that realm will be accepted. If it is not set, users of any realm can connect, subject to whatever user name mapping is done.

#### 20.3.4. SSPI Authentication

SSPI is a Windows technology for secure authentication with single sign-on. PostgreSQL will use SSPI in `negotiate` mode, which will use Kerberos when possible and automatically fall back to NTLM in other cases. SSPI authentication only works when both server and client are running Windows, or, on non-Windows platforms, when GSSAPI is available.

When using Kerberos authentication, SSPI works the same way GSSAPI does; see [Section 20.3.3](https://www.postgresql.org/docs/10/static/auth-methods.html#GSSAPI-AUTH) for details.

The following configuration options are supported for SSPI:`include_realm`

If set to 0, the realm name from the authenticated user principal is stripped off before being passed through the user name mapping \([Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html)\). This is discouraged and is primarily available for backwards compatibility, as it is not secure in multi-realm environments unless `krb_realm` is also used. It is recommended to leave `include_realm` set to the default \(1\) and to provide an explicit mapping in `pg_ident.conf` to convert principal names to PostgreSQL user names.`compat_realm`

If set to 1, the domain's SAM-compatible name \(also known as the NetBIOS name\) is used for the `include_realm` option. This is the default. If set to 0, the true realm name from the Kerberos user principal name is used.

Do not disable this option unless your server runs under a domain account \(this includes virtual service accounts on a domain member system\) and all clients authenticating through SSPI are also using domain accounts, or authentication will fail.`upn_username`

If this option is enabled along with `compat_realm`, the user name from the Kerberos UPN is used for authentication. If it is disabled \(the default\), the SAM-compatible user name is used. By default, these two names are identical for new user accounts.

Note that libpq uses the SAM-compatible name if no explicit user name is specified. If you use libpq or a driver based on it, you should leave this option disabled or explicitly specify user name in the connection string.`map`

Allows for mapping between system and database user names. See [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html) for details. For a SSPI/Kerberos principal, such as `username@EXAMPLE.COM` \(or, less commonly,`username/hostbased@EXAMPLE.COM`\), the user name used for mapping is `username@EXAMPLE.COM` \(or `username/hostbased@EXAMPLE.COM`, respectively\), unless `include_realm` has been set to 0, in which case `username` \(or `username/hostbased`\) is what is seen as the system user name when mapping.`krb_realm`

Sets the realm to match user principal names against. If this parameter is set, only users of that realm will be accepted. If it is not set, users of any realm can connect, subject to whatever user name mapping is done.

#### 20.3.5. Ident Authentication

The ident authentication method works by obtaining the client's operating system user name from an ident server and using it as the allowed database user name \(with an optional user name mapping\). This is only supported on TCP/IP connections.

#### Note

When ident is specified for a local \(non-TCP/IP\) connection, peer authentication \(see [Section 20.3.6](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PEER)\) will be used instead.

The following configuration options are supported for ident:`map`

Allows for mapping between system and database user names. See [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html) for details.

The “Identification Protocol” is described in RFC 1413. Virtually every Unix-like operating system ships with an ident server that listens on TCP port 113 by default. The basic functionality of an ident server is to answer questions like “What user initiated the connection that goes out of your port _`X`_ and connects to my port _`Y`_?”. Since PostgreSQL knows both _`X`_and _`Y`_ when a physical connection is established, it can interrogate the ident server on the host of the connecting client and can theoretically determine the operating system user for any given connection.

The drawback of this procedure is that it depends on the integrity of the client: if the client machine is untrusted or compromised, an attacker could run just about any program on port 113 and return any user name they choose. This authentication method is therefore only appropriate for closed networks where each client machine is under tight control and where the database and system administrators operate in close contact. In other words, you must trust the machine running the ident server. Heed the warning:

|   | The Identification Protocol is not intended as an authorization or access control protocol. |   |
| :--- | :--- | :--- |
|   | --RFC 1413 |  |

Some ident servers have a nonstandard option that causes the returned user name to be encrypted, using a key that only the originating machine's administrator knows. This option _must not_ be used when using the ident server with PostgreSQL, since PostgreSQL does not have any way to decrypt the returned string to determine the actual user name.

#### 20.3.6. Peer Authentication

The peer authentication method works by obtaining the client's operating system user name from the kernel and using it as the allowed database user name \(with optional user name mapping\). This method is only supported on local connections.

The following configuration options are supported for peer:`map`

Allows for mapping between system and database user names. See [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html) for details.

Peer authentication is only available on operating systems providing the `getpeereid()` function, the `SO_PEERCRED` socket parameter, or similar mechanisms. Currently that includes Linux, most flavors of BSD including macOS, and Solaris.

#### 20.3.7. LDAP Authentication

This authentication method operates similarly to `password` except that it uses LDAP as the password verification method. LDAP is used only to validate the user name/password pairs. Therefore the user must already exist in the database before LDAP can be used for authentication.

LDAP authentication can operate in two modes. In the first mode, which we will call the simple bind mode, the server will bind to the distinguished name constructed as _`prefix`_ _`usernamesuffix`_. Typically, the _`prefix`_ parameter is used to specify `cn=`, or _`DOMAIN`_`\` in an Active Directory environment. _`suffix`_ is used to specify the remaining part of the DN in a non-Active Directory environment.

In the second mode, which we will call the search+bind mode, the server first binds to the LDAP directory with a fixed user name and password, specified with _`ldapbinddn`_ and _`ldapbindpasswd`_, and performs a search for the user trying to log in to the database. If no user and password is configured, an anonymous bind will be attempted to the directory. The search will be performed over the subtree at _`ldapbasedn`_, and will try to do an exact match of the attribute specified in _`ldapsearchattribute`_. Once the user has been found in this search, the server disconnects and re-binds to the directory as this user, using the password specified by the client, to verify that the login is correct. This mode is the same as that used by LDAP authentication schemes in other software, such as Apache `mod_authnz_ldap` and `pam_ldap`. This method allows for significantly more flexibility in where the user objects are located in the directory, but will cause two separate connections to the LDAP server to be made.

The following configuration options are used in both modes:`ldapserver`

Names or IP addresses of LDAP servers to connect to. Multiple servers may be specified, separated by spaces.`ldapport`

Port number on LDAP server to connect to. If no port is specified, the LDAP library's default port setting will be used.`ldaptls`

Set to 1 to make the connection between PostgreSQL and the LDAP server use TLS encryption. Note that this only encrypts the traffic to the LDAP server — the connection to the client will still be unencrypted unless SSL is used.

The following options are used in simple bind mode only:`ldapprefix`

String to prepend to the user name when forming the DN to bind as, when doing simple bind authentication.`ldapsuffix`

String to append to the user name when forming the DN to bind as, when doing simple bind authentication.

The following options are used in search+bind mode only:`ldapbasedn`

Root DN to begin the search for the user in, when doing search+bind authentication.`ldapbinddn`

DN of user to bind to the directory with to perform the search when doing search+bind authentication.`ldapbindpasswd`

Password for user to bind to the directory with to perform the search when doing search+bind authentication.`ldapsearchattribute`

Attribute to match against the user name in the search when doing search+bind authentication. If no attribute is specified, the `uid` attribute will be used.`ldapurl`

An RFC 4516 LDAP URL. This is an alternative way to write some of the other LDAP options in a more compact and standard form. The format is

```text
ldap://host[:port]/basedn[?[attribute][?[scope]]]
```

_`scope`_ must be one of `base`, `one`, `sub`, typically the latter. Only one attribute is used, and some other components of standard LDAP URLs such as filters and extensions are not supported.

For non-anonymous binds, `ldapbinddn` and `ldapbindpasswd` must be specified as separate options.

To use encrypted LDAP connections, the `ldaptls` option has to be used in addition to `ldapurl`. The `ldaps` URL scheme \(direct SSL connection\) is not supported.

LDAP URLs are currently only supported with OpenLDAP, not on Windows.

It is an error to mix configuration options for simple bind with options for search+bind.

Here is an example for a simple-bind LDAP configuration:

```text
host ... ldap ldapserver=ldap.example.net ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

When a connection to the database server as database user `someuser` is requested, PostgreSQL will attempt to bind to the LDAP server using the DN `cn=someuser, dc=example, dc=net`and the password provided by the client. If that connection succeeds, the database access is granted.

Here is an example for a search+bind configuration:

```text
host ... ldap ldapserver=ldap.example.net ldapbasedn="dc=example, dc=net" ldapsearchattribute=uid
```

When a connection to the database server as database user `someuser` is requested, PostgreSQL will attempt to bind anonymously \(since `ldapbinddn` was not specified\) to the LDAP server, perform a search for `(uid=someuser)` under the specified base DN. If an entry is found, it will then attempt to bind using that found information and the password supplied by the client. If that second connection succeeds, the database access is granted.

Here is the same search+bind configuration written as a URL:

```text
host ... ldap ldapurl="ldap://ldap.example.net/dc=example,dc=net?uid?sub"
```

Some other software that supports authentication against LDAP uses the same URL format, so it will be easier to share the configuration.

#### Tip

Since LDAP often uses commas and spaces to separate the different parts of a DN, it is often necessary to use double-quoted parameter values when configuring LDAP options, as shown in the examples.

#### 20.3.8. RADIUS Authentication

This authentication method operates similarly to `password` except that it uses RADIUS as the password verification method. RADIUS is used only to validate the user name/password pairs. Therefore the user must already exist in the database before RADIUS can be used for authentication.

When using RADIUS authentication, an Access Request message will be sent to the configured RADIUS server. This request will be of type `Authenticate Only`, and include parameters for `user name`, `password` \(encrypted\) and `NAS Identifier`. The request will be encrypted using a secret shared with the server. The RADIUS server will respond to this server with either `Access Accept` or `Access Reject`. There is no support for RADIUS accounting.

Multiple RADIUS servers can be specified, in which case they will be tried sequentially. If a negative response is received from a server, the authentication will fail. If no response is received, the next server in the list will be tried. To specify multiple servers, put the names within quotes and separate the server names with a comma. If multiple servers are specified, all other RADIUS options can also be given as a comma separate list, to apply individual values to each server. They can also be specified as a single value, in which case this value will apply to all servers.

The following configuration options are supported for RADIUS:`radiusservers`

The name or IP addresses of the RADIUS servers to connect to. This parameter is required.`radiussecrets`

The shared secrets used when talking securely to the RADIUS server. This must have exactly the same value on the PostgreSQL and RADIUS servers. It is recommended that this be a string of at least 16 characters. This parameter is required.

#### Note

The encryption vector used will only be cryptographically strong if PostgreSQL is built with support for OpenSSL. In other cases, the transmission to the RADIUS server should only be considered obfuscated, not secured, and external security measures should be applied if necessary.`radiusports`

The port number on the RADIUS servers to connect to. If no port is specified, the default port `1812` will be used.`radiusidentifiers`

The string used as `NAS Identifier` in the RADIUS requests. This parameter can be used as a second parameter identifying for example which database user the user is attempting to authenticate as, which can be used for policy matching on the RADIUS server. If no identifier is specified, the default `postgresql` will be used.

#### 20.3.9. Certificate Authentication

This authentication method uses SSL client certificates to perform authentication. It is therefore only available for SSL connections. When using this authentication method, the server will require that the client provide a valid, trusted certificate. No password prompt will be sent to the client. The `cn` \(Common Name\) attribute of the certificate will be compared to the requested database user name, and if they match the login will be allowed. User name mapping can be used to allow `cn` to be different from the database user name.

The following configuration options are supported for SSL certificate authentication:`map`

Allows for mapping between system and database user names. See [Section 20.2](https://www.postgresql.org/docs/10/static/auth-username-maps.html) for details.

In a `pg_hba.conf` record specifying certificate authentication, the authentication option `clientcert` is assumed to be `1`, and it cannot be turned off since a client certificate is necessary for this method. What the `cert` method adds to the basic `clientcert` certificate validity test is a check that the `cn` attribute matches the database user name.

#### 20.3.10. PAM Authentication

This authentication method operates similarly to `password` except that it uses PAM \(Pluggable Authentication Modules\) as the authentication mechanism. The default PAM service name is `postgresql`. PAM is used only to validate user name/password pairs and optionally the connected remote host name or IP address. Therefore the user must already exist in the database before PAM can be used for authentication. For more information about PAM, please read the [Linux-PAM Page](http://www.kernel.org/pub/linux/libs/pam/).

The following configuration options are supported for PAM:`pamservice`

PAM service name.`pam_use_hostname`

Determines whether the remote IP address or the host name is provided to PAM modules through the `PAM_RHOST` item. By default, the IP address is used. Set this option to 1 to use the resolved host name instead. Host name resolution can lead to login delays. \(Most PAM configurations don't use this information, so it is only necessary to consider this setting if a PAM configuration was specifically created to make use of it.\)

#### Note

If PAM is set up to read `/etc/shadow`, authentication will fail because the PostgreSQL server is started by a non-root user. However, this is not an issue when PAM is configured to use LDAP or other authentication methods.

#### 20.3.11. BSD Authentication

This authentication method operates similarly to `password` except that it uses BSD Authentication to verify the password. BSD Authentication is used only to validate user name/password pairs. Therefore the user's role must already exist in the database before BSD Authentication can be used for authentication. The BSD Authentication framework is currently only available on OpenBSD.

BSD Authentication in PostgreSQL uses the `auth-postgresql` login type and authenticates with the `postgresql` login class if that's defined in `login.conf`. By default that login class does not exist, and PostgreSQL will use the default login class.

#### Note

To use BSD Authentication, the PostgreSQL user account \(that is, the operating system user running the server\) must first be added to the `auth` group. The `auth` group exists by default on OpenBSD systems.

