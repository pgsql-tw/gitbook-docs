<a id="LIBPQ-LDAP"></a>

## 32.18. 以 LDAP 查詢連線參數 [#](#LIBPQ-LDAP)

<a id="id-1.7.3.25.2"></a>

若 libpq 在編譯時加入了 LDAP 支援（`configure` 的選項 `--with-ldap`），就可以透過 LDAP 從中央伺服器取得 `host` 或 `dbname` 之類的連線選項。其優點是，當資料庫的連線參數變更時，不必在所有用戶端機器上更新連線資訊。

LDAP 連線參數查詢使用連線服務檔 `pg_service.conf`（請參閱[第 32.17 節](libpq-pgservice.md)）。`pg_service.conf` 的區段（stanza）中，以 `ldap://` 開頭的行會被識別為 LDAP URL，並據以執行 LDAP 查詢。查詢結果必須是一串 `keyword = value` 配對，用來設定連線選項。URL 必須符合 [RFC 1959](https://datatracker.ietf.org/doc/html/rfc1959)，格式如下

```

ldap://[hostname[:port]]/search_base?attribute?search_scope?filter
```

其中 *`hostname`* 預設為 `localhost`，*`port`* 預設為 389。

LDAP 查詢成功後，`pg_service.conf` 的處理即告終止；但若無法連上 LDAP 伺服器，則會繼續處理。這是為了提供備援：後面可以再放指向其他 LDAP 伺服器的 LDAP URL 行、傳統的 `keyword
= value` 配對，或者使用預設連線選項。若你希望在這種情況下改為收到錯誤訊息，請在該 LDAP URL 之後加上一行語法錯誤的內容。

以下列 LDIF 檔建立的範例 LDAP 項目

```

version:1
dn:cn=mydatabase,dc=mycompany,dc=com
changetype:add
objectclass:top
objectclass:device
cn:mydatabase
description:host=dbserver.mycompany.com
description:port=5439
description:dbname=mydb
description:user=mydb_user
description:sslmode=require
```

可以用下列 LDAP URL 查詢：

```

ldap://ldap.mycompany.com/dc=mycompany,dc=com?description?one?(cn=mydatabase)
```

你也可以將一般的服務檔項目與 LDAP 查詢混合使用。`pg_service.conf` 中一個區段的完整範例如下：

```

# only host and port are stored in LDAP, specify dbname and user explicitly
[customerdb]
dbname=customer
user=appuser
ldap://ldap.acme.com/cn=dbserver,cn=hosts?pgconnectinfo?base?(objectclass=*)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-ldap.html)（原文版本：18.6；核對日期：2026-10-18）
