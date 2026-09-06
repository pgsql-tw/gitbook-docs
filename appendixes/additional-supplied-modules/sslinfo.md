<a id="SSLINFO"></a>

# F.42. sslinfo

[F.42.1. Functions Provided](#id-1.11.7.51.6)

[F.42.2. Author](#id-1.11.7.51.7)

<a id="id-1.11.7.51.2"></a>

The `sslinfo` module provides information about the SSL certificate that the current client provided when connecting to PostgreSQL. The module is useless (most functions will return NULL) if the current connection does not use SSL.

Some of the information available through this module can also be obtained using the built-in system view [`pg_stat_ssl`](https://www.postgresql.org/docs/15/monitoring-stats.html#MONITORING-PG-STAT-SSL-VIEW).

This extension won't build at all unless the installation was configured with `--with-ssl=openssl`.

<a id="id-1.11.7.51.6"></a>

## F.42.1. Functions Provided

`ssl_is_used() returns boolean` <a id="id-1.11.7.51.6.2.1.1.2"></a>

Returns true if current connection to server uses SSL, and false otherwise.

`ssl_version() returns text` <a id="id-1.11.7.51.6.2.2.1.2"></a>

Returns the name of the protocol used for the SSL connection (e.g., TLSv1.0, TLSv1.1, TLSv1.2 or TLSv1.3).

`ssl_cipher() returns text` <a id="id-1.11.7.51.6.2.3.1.2"></a>

Returns the name of the cipher used for the SSL connection (e.g., DHE-RSA-AES256-SHA).

`ssl_client_cert_present() returns boolean` <a id="id-1.11.7.51.6.2.4.1.2"></a>

Returns true if current client has presented a valid SSL client certificate to the server, and false otherwise. (The server might or might not be configured to require a client certificate.)

`ssl_client_serial() returns numeric` <a id="id-1.11.7.51.6.2.5.1.2"></a>

Returns serial number of current client certificate. The combination of certificate serial number and certificate issuer is guaranteed to uniquely identify a certificate (but not its owner — the owner ought to regularly change their keys, and get new certificates from the issuer).

So, if you run your own CA and allow only certificates from this CA to be accepted by the server, the serial number is the most reliable (albeit not very mnemonic) means to identify a user.

`ssl_client_dn() returns text` <a id="id-1.11.7.51.6.2.6.1.2"></a>

Returns the full subject of the current client certificate, converting character data into the current database encoding. It is assumed that if you use non-ASCII characters in the certificate names, your database is able to represent these characters, too. If your database uses the SQL_ASCII encoding, non-ASCII characters in the name will be represented as UTF-8 sequences.

The result looks like `/CN=Somebody /C=Some country/O=Some organization`.

`ssl_issuer_dn() returns text` <a id="id-1.11.7.51.6.2.7.1.2"></a>

Returns the full issuer name of the current client certificate, converting character data into the current database encoding. Encoding conversions are handled the same as for `ssl_client_dn`.

The combination of the return value of this function with the certificate serial number uniquely identifies the certificate.

This function is really useful only if you have more than one trusted CA certificate in your server's certificate authority file, or if this CA has issued some intermediate certificate authority certificates.

`ssl_client_dn_field(fieldname text) returns text` <a id="id-1.11.7.51.6.2.8.1.2"></a>

This function returns the value of the specified field in the certificate subject, or NULL if the field is not present. Field names are string constants that are converted into ASN1 object identifiers using the OpenSSL object database. The following values are acceptable:

```

commonName (alias CN)
surname (alias SN)
name
givenName (alias GN)
countryName (alias C)
localityName (alias L)
stateOrProvinceName (alias ST)
organizationName (alias O)
organizationalUnitName (alias OU)
title
description
initials
postalCode
streetAddress
generationQualifier
description
dnQualifier
x500UniqueIdentifier
pseudonym
role
emailAddress
```

All of these fields are optional, except `commonName`. It depends entirely on your CA's policy which of them would be included and which wouldn't. The meaning of these fields, however, is strictly defined by the X.500 and X.509 standards, so you cannot just assign arbitrary meaning to them.

`ssl_issuer_field(fieldname text) returns text` <a id="id-1.11.7.51.6.2.9.1.2"></a>

Same as `ssl_client_dn_field`, but for the certificate issuer rather than the certificate subject.

`ssl_extension_info() returns setof record` <a id="id-1.11.7.51.6.2.10.1.2"></a>

Provide information about extensions of client certificate: extension name, extension value, and if it is a critical extension.

<a id="id-1.11.7.51.7"></a>

## F.42.2. Author

Victor Wagner <code class="email">&lt;<a class="email" href="mailto:vitus@cryptocom.ru">vitus@cryptocom.ru</a>&gt;</code>, Cryptocom LTD

Dmitry Voronin <code class="email">&lt;<a class="email" href="mailto:carriingfate92@yandex.ru">carriingfate92@yandex.ru</a>&gt;</code>

E-Mail of Cryptocom OpenSSL development group: <code class="email">&lt;<a class="email" href="mailto:openssl@cryptocom.ru">openssl@cryptocom.ru</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sslinfo.html)（英文原文，待翻譯）
