# 21.1. 設定檔：pg\_hba.conf

用戶端身份驗證由組態檔案控制，組態檔案通常名稱為 pg\_hba.conf，並儲存在資料庫叢集的資料目錄中。 （HBA 代表 host-based authentication。）當 initdb 初始化資料目錄時，將安裝預設的 pg\_hba.conf 檔案。但是，可以將身份驗證組態檔案放在其他路徑；請參閱 [hba\_file](../server-configuration/file-locations.md) 組態參數。

pg\_hba.conf 檔案的一般格式是一組記錄，每行一個。空白行將被忽略，# comment 字元後面的任何文字都將被忽略。記錄不能跨行。記錄由許多段落組成，這些段落由空格或 tab 分隔。如果段落的值用了雙引號，則段落可以包含空格。在資料庫，使用者或位址段落（例如，all 或 replication）中括起其中一個關鍵字會使該字失去其特殊含義，並且只是將資料庫，使用者或主機與該名稱相匹配。

每條記錄指定連線類型，用戶端 IP 位址範圍（如果與連線類型相關）、資料庫名稱、使用者名稱以及符合這些參數的連線身份驗證方法。具有符合的連線類型、用戶端位址、要求的資料庫和使用者名稱的第一個記錄用於執行身份驗證。沒有“fall-through”或“replication”：如果選擇了一條記錄而認證失敗，就不再考慮後續記錄。如果沒有記錄匹配，則拒絕存取。

記錄可以是下面的七種格式之一

```
local      database  user  auth-method  [auth-options]
host       database  user  address  auth-method  [auth-options]
hostssl    database  user  address  auth-method  [auth-options]
hostnossl  database  user  address  auth-method  [auth-options]
host       database  user  IP-address  IP-mask  auth-method  [auth-options]
hostssl    database  user  IP-address  IP-mask  auth-method  [auth-options]
hostnossl  database  user  IP-address  IP-mask  auth-method  [auth-options]
```

段落的含義如下：

`local`

此記錄搭配使用 Unix-domain socket 的連線嘗試。如果沒有此類型的記錄，則不允許使用 Unix-domain socket 連線。

`host`

此記錄用於使用 TCP/IP 進行的連線嘗試。主機記錄使用 SSL 或非 SSL 連線嘗試.

**重要**\
除非使用 [listen\_addresses](../server-configuration/connections-and-authentication.md#19-3-1-ding) 組態參數的適當值啟動伺服器，否則將無法進行遠端 TCP/IP 連線，因為預設行為是僅在 localhost 上監聽 TCP/IP 連線。

`hostssl`

此記錄會套用於使用 TCP/IP 進行的連線嘗試，但僅限於使用 SSL 加密進行連線時。

要使用此選項，必須以 SSL 建置伺服器，也必須透過設定 [ssl 組態參數](../server-configuration/connections-and-authentication.md#19-3-3-ssl)來啟用 SSL（有關更多訊息，請參閱[第 18.9 節](../server-setup-and-operation/secure-tcp-ip-connections-with-ssl.md)）。否則，將會忽略 hostssl 記錄，除非是為了記錄不能與任何連線相符合的警告。

`hostnossl`

此記錄類型與 hostssl 具有相反的行為；它僅套用於透過 TCP/IP 且不使用 SSL 的連線嘗試。

_`database`_

指定此記錄所要求搭配的資料庫名稱。值 all 使其搭配所有資料庫。如果請求的資料庫與請求的使用者具有相同的名稱，則可以用 sameuser 值來指定。值 samerole 指定所請求的使用者必須是與請求的資料庫同名的角色成員。 （ samegroup 是一個過時但仍然被接受的 samerole 別名。）超級使用者不被認為是同一角色的成員，除非他們直接或間接地明確地成為角色的成員，而不僅僅是作為超級使用者。值 replication 指定在請求 physical replication 連線時的記錄搭配（請注意，複寫連線不指定任何特定資料庫）。否則，這是特定 PostgreSQL 資料庫的名稱。可以透過用逗號分隔它們來設定多個資料庫名稱，也可以透過在檔案名稱前加上 @ 來指定包含資料庫名稱的額外檔案。

_`user`_

指定此記錄所限制的資料庫使用者名稱。all 表示所有使用者都適用。否則，它就是是特定資料庫使用者的名稱，要就是帶有 + 的群組名稱。（回想一下，PostgreSQL 中的使用者和群組之間並沒有真正的差別； + 標記實際上表示「符合直接或間接地成為該角色成員的任何角色」，而沒有 + 標記的名稱僅適用該特定角色。 ）為此，只有超級使用者直接或間接明確地是角色的成員，而不僅僅是憑藉超級使用者，才將其視為角色的成員。可以使用逗號分隔多個使用者名稱。透過在檔案名稱前面加上 @ 來指定包含使用者名稱的獨立設定檔案。

_`address`_

Specifies the client machine address(es) that this record matches. This field can contain either a host name, an IP address range, or one of the special key words mentioned below.

An IP address range is specified using standard numeric notation for the range's starting address, then a slash (`/`) and a CIDR mask length. The mask length indicates the number of high-order bits of the client IP address that must match. Bits to the right of this should be zero in the given IP address. There must not be any white space between the IP address, the `/`, and the CIDR mask length.

Typical examples of an IPv4 address range specified this way are `172.20.143.89/32` for a single host, or `172.20.143.0/24` for a small network, or `10.6.0.0/16` for a larger one. An IPv6 address range might look like `::1/128` for a single host (in this case the IPv6 loopback address) or `fe80::7a31:c1ff:0000:0000/96` for a small network. `0.0.0.0/0` represents all IPv4 addresses, and `::0/0` represents all IPv6 addresses. To specify a single host, use a mask length of 32 for IPv4 or 128 for IPv6. In a network address, do not omit trailing zeroes.

An entry given in IPv4 format will match only IPv4 connections, and an entry given in IPv6 format will match only IPv6 connections, even if the represented address is in the IPv4-in-IPv6 range. Note that entries in IPv6 format will be rejected if the system's C library does not have support for IPv6 addresses.

You can also write `all` to match any IP address, `samehost` to match any of the server's own IP addresses, or `samenet` to match any address in any subnet that the server is directly connected to.

If a host name is specified (anything that is not an IP address range or a special key word is treated as a host name), that name is compared with the result of a reverse name resolution of the client's IP address (e.g., reverse DNS lookup, if DNS is used). Host name comparisons are case insensitive. If there is a match, then a forward name resolution (e.g., forward DNS lookup) is performed on the host name to check whether any of the addresses it resolves to are equal to the client's IP address. If both directions match, then the entry is considered to match. (The host name that is used in `pg_hba.conf` should be the one that address-to-name resolution of the client's IP address returns, otherwise the line won't be matched. Some host name databases allow associating an IP address with multiple host names, but the operating system will only return one host name when asked to resolve an IP address.)

以點（.）開頭的主機名稱表示與實際主機名稱的後段比對。因此，.example.com 與 foo.example.com 比較是相符的（不僅限於 example.com）。

當在 pg\_hba.conf 中指定了主機名稱時，您應該確保名稱解析足夠快。設定本地名稱解析暫存（例如 nscd）可能是有幫助的。另外，您可能希望啟用配置參數 log\_hostname 來查看用戶端的主機名稱，而不是日誌中的 IP 位址。

此欄位僅適用於 host、hostssl 和 hostnossl 規則項目。

{% hint style="info" %}
使用者有時會想知道為什麼以這種看似複雜的方式來處理主機名稱，並具有兩種名稱解析，其中包括對用戶端 IP 地址的反向查詢。如果未設定用戶端的反向 DNS 項目或設定了某些不良的主機名稱，則會使該功能的使用複雜化。這樣做主要是為了提高效率：透過這種方式，連線嘗試最多需要兩次 DNS 查詢，一次反向查詢和一次正向查詢。如果某個位址存在 DNS 問題，則僅成為該使用者的問題。假設僅執行正向查詢的替代實作方式，必須在每次連線嘗試期間解析 pg\_hba.conf 中提到的每個主機名稱。 如果列出了許多名稱，那可能會很慢。而且，如果其中一個主機名稱存在有 DNS 問題，那麼它將成為每個人的問題。

另外，必須執行反向查詢以實作後段樣式比對的功能，因為需要知道實際的用戶端主機名稱，以便將其與樣式進行比對。

請注意，此行為與基於主機名稱的存取控制的其他常見的實作方式一致，例如 Apache HTTP Server 和 TCP Wrappers。
{% endhint %}

_`IP-address`_\
_`IP-mask`_

These two fields can be used as an alternative to the _`IP-address`_`/`_`mask-length`_ notation. Instead of specifying the mask length, the actual mask is specified in a separate column. For example, `255.0.0.0` represents an IPv4 CIDR mask length of 8, and `255.255.255.255`represents a CIDR mask length of 32.

These fields only apply to `host`, `hostssl`, and `hostnossl` records.

_`auth-method`_

Specifies the authentication method to use when a connection matches this record. The possible choices are summarized here; details are in [Section 20.3](https://www.postgresql.org/docs/10/static/auth-methods.html).

`trust`

無條件地允許連線。此方法允許可以連線到 PostgreSQL 資料庫伺服器的任何人以他們希望的任何 PostgreSQL 使用者身份登入，而毌需密碼或任何其他身份驗證。有關詳細資訊，請參閱[第 20.3.1 節](authentication-methods.md#20-3-1-trust-authentication)。

`reject`

無條件地拒絕連線。這對於「過濾」群組網路中的某些主機很有用。例如拒絕阻止特定主機的連接，而更前面的規則則允許特定網路中的其餘主機進行連線。

`scram-sha-256`

Perform SCRAM-SHA-256 authentication to verify the user's password. See [Section 20.3.2](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PASSWORD) for details.

`md5`

Perform SCRAM-SHA-256 or MD5 authentication to verify the user's password. See [Section 20.3.2](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PASSWORD) for details.

`password`

Require the client to supply an unencrypted password for authentication. Since the password is sent in clear text over the network, this should not be used on untrusted networks. See [Section 20.3.2](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PASSWORD) for details.

`gss`

Use GSSAPI to authenticate the user. This is only available for TCP/IP connections. See [Section 20.3.3](https://www.postgresql.org/docs/10/static/auth-methods.html#GSSAPI-AUTH) for details.

`sspi`

Use SSPI to authenticate the user. This is only available on Windows. See [Section 20.3.4](https://www.postgresql.org/docs/10/static/auth-methods.html#SSPI-AUTH) for details.

`ident`

Obtain the operating system user name of the client by contacting the ident server on the client and check if it matches the requested database user name. Ident authentication can only be used on TCP/IP connections. When specified for local connections, peer authentication will be used instead. See [Section 20.3.5](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-IDENT) for details.

`peer`

Obtain the client's operating system user name from the operating system and check if it matches the requested database user name. This is only available for local connections. See [Section 20.3.6](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PEER) for details.

`ldap`

Authenticate using an LDAP server. See [Section 20.3.7](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-LDAP) for details.

`radius`

Authenticate using a RADIUS server. See [Section 20.3.8](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-RADIUS) for details.

`cert`

Authenticate using SSL client certificates. See [Section 20.3.9](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-CERT) for details.

`pam`

Authenticate using the Pluggable Authentication Modules (PAM) service provided by the operating system. See [Section 20.3.10](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-PAM) for details.

`bsd`

Authenticate using the BSD Authentication service provided by the operating system. See [Section 20.3.11](https://www.postgresql.org/docs/10/static/auth-methods.html#AUTH-BSD) for details.

_`auth-options`_

After the _`auth-method`_ field, there can be field(s) of the form _`name`_`=`_`value`_ that specify options for the authentication method. Details about which options are available for which authentication methods appear below.

In addition to the method-specific options listed below, there is one method-independent authentication option `clientcert`, which can be specified in any `hostssl` record. When set to `1`, this option requires the client to present a valid (trusted) SSL certificate, in addition to the other requirements of the authentication method.

@ 語法結構包含的檔案會被入為名稱列表，可以用空格或逗號分隔。就像在 pg\_hba.conf 中一樣，註釋由 ＃ 引入，並且允許巢狀式的 @ 結構。除非 @ 之後的檔案名稱是絕對路徑，否則它將被視為相對於包含引用檔案的目錄。

Since the `pg_hba.conf` records are examined sequentially for each connection attempt, the order of the records is significant. Typically, earlier records will have tight connection match parameters and weaker authentication methods, while later records will have looser match parameters and stronger authentication methods. For example, one might wish to use `trust` authentication for local TCP/IP connections but require a password for remote TCP/IP connections. In this case a record specifying `trust` authentication for connections from 127.0.0.1 would appear before a record specifying password authentication for a wider range of allowed client IP addresses.

The `pg_hba.conf` file is read on start-up and when the main server process receives a SIGHUP signal. If you edit the file on an active system, you will need to signal the postmaster (using `pg_ctl reload` or `kill -HUP`) to make it re-read the file.

{% hint style="info" %}
前面的宣告在 Microsoft Windows 上是不正確的：在 Windows，pg\_hba.conf 檔案中的任何變更都會在後續的新連線立即適用。
{% endhint %}

系統檢視表 [pg\_hba\_file\_rules](../../internals/system-catalogs/pg\_hba\_file\_rules.md) 有助於預先測試對 pg\_hba.conf 檔案的變更，或者在檔案載入未達到預期效果時診斷問題。檢視表中帶有非空白錯誤欄位會指示檔案相應規則項目中的問題。

{% hint style="info" %}
要連線到特定的資料庫，使用者不僅必須通過 pg\_hba.conf 檢查，而且必須具有資料庫的 CONNECT 權限。如果您希望限制哪些使用者可以連接到哪些資料庫，通常比設定 pg\_hba.conf 項目更容易，透過授權/撤銷 CONNECT 權限來控制。
{% endhint %}

Some examples of `pg_hba.conf` entries are shown in [Example 20.1](https://www.postgresql.org/docs/10/static/auth-pg-hba-conf.html#EXAMPLE-PG-HBA.CONF). See the next section for details on the different authentication methods.

**Example 20.1. Example `pg_hba.conf` Entries**

```
# Allow any user on the local system to connect to any database with
# any database user name using Unix-domain sockets (the default for local
# connections).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust

# The same using local loopback TCP/IP connections.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             127.0.0.1/32            trust

# The same as the previous line, but using a separate netmask column
#
# TYPE  DATABASE        USER            IP-ADDRESS      IP-MASK             METHOD
host    all             all             127.0.0.1       255.255.255.255     trust

# The same over IPv6.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             ::1/128                 trust

# The same using a host name (would typically cover both IPv4 and IPv6).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             localhost               trust

# Allow any user from any host with IP address 192.168.93.x to connect
# to database "postgres" as the same user name that ident reports for
# the connection (typically the operating system user name).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    postgres        all             192.168.93.0/24         ident

# Allow any user from host 192.168.12.10 to connect to database
# "postgres" if the user's password is correctly supplied.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    postgres        all             192.168.12.10/32        scram-sha-256

# Allow any user from hosts in the example.com domain to connect to
# any database if the user's password is correctly supplied.
#
# Require SCRAM authentication for most users, but make an exception
# for user 'mike', who uses an older client that doesn't support SCRAM
# authentication.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             mike            .example.com            md5
host    all             all             .example.com            scram-sha-256

# In the absence of preceding "host" lines, these two lines will
# reject all connections from 192.168.54.1 (since that entry will be
# matched first), but allow GSSAPI connections from anywhere else
# on the Internet.  The zero mask causes no bits of the host IP
# address to be considered, so it matches any host.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.54.1/32         reject
host    all             all             0.0.0.0/0               gss

# Allow users from 192.168.x.x hosts to connect to any database, if
# they pass the ident check.  If, for example, ident says the user is
# "bryanh" and he requests to connect as PostgreSQL user "guest1", the
# connection is allowed if there is an entry in pg_ident.conf for map
# "omicron" that says "bryanh" is allowed to connect as "guest1".
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.0.0/16          ident map=omicron

# If these are the only three lines for local connections, they will
# allow local users to connect only to their own databases (databases
# with the same name as their database user name) except for administrators
# and members of role "support", who can connect to all databases.  The file
# $PGDATA/admins contains a list of names of administrators.  Passwords
# are required in all cases.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   sameuser        all                                     md5
local   all             @admins                                 md5
local   all             +support                                md5

# The last two lines above can be combined into a single line:
local   all             @admins,+support                        md5

# The database column can also use lists and file names:
local   db1,db2,@demodbs  all                                   md5
```
