<a id="AUTH-LDAP"></a>

## 20.10. LDAP 認證 [#](#AUTH-LDAP)

<a id="id-1.6.7.17.2"></a>

此認證方法的運作方式與
`password` 類似，差別在於它使用 LDAP
作為密碼驗證方法。LDAP 僅用於驗證
使用者名稱／密碼配對。因此在使用 LDAP 進行認證之前，該使用者必須
已存在於資料庫中。

LDAP 認證可以在兩種模式下運作。在第一種模式，
我們稱之為 simple bind（簡易繫結）模式，
伺服器會以 *`prefix`* *`username`* *`suffix`*
的方式組成 distinguished name（DN，區別名稱）並與之繫結。
通常，*`prefix`* 參數用於指定
`cn=`，或在 Active
Directory 環境中指定 *`DOMAIN`*`\`。*`suffix`* 則用於指定在非 Active Directory 環境中
DN 的其餘部分。

在第二種模式，我們稱之為 search+bind（搜尋加繫結）模式，
伺服器會先以由 *`ldapbinddn`*
與 *`ldapbindpasswd`* 指定的固定使用者名稱與密碼繫結到 LDAP 目錄，
然後搜尋正在嘗試
登入資料庫的使用者。如果未設定使用者與密碼，則會嘗試以匿名方式
繫結到該目錄。搜尋會在 *`ldapbasedn`* 所指定的子樹中執行，
並會嘗試對
*`ldapsearchattribute`* 所指定的屬性做完全相符的比對。
一旦在此次搜尋中找到該使用者，伺服器就會使用用戶端提供的密碼，
以該使用者身分重新繫結到目錄，以驗證此次
登入是否正確。這種模式與其他軟體中的 LDAP 認證機制相同，
例如 Apache 的 `mod_authnz_ldap` 與 `pam_ldap`。
這種方法能讓使用者物件在目錄中的位置具有明顯更高的
彈性，但會導致對 LDAP 伺服器多發出兩次額外的請求。

以下組態選項在兩種模式中皆會用到：

`ldapserver`
:   要連線的 LDAP 伺服器名稱或 IP 位址。可以指定多台
    伺服器，以空格分隔。

`ldapport`
:   要連線的 LDAP 伺服器連接埠號。若未指定連接埠，
    則會使用 LDAP 函式庫的預設連接埠設定。

`ldapscheme`
:   設為 `ldaps` 以使用 LDAPS。這是某些 LDAP 伺服器實作
    所支援的一種透過 SSL 使用 LDAP 的非標準
    方式。也可參考 `ldaptls` 選項作為替代方案。

`ldaptls`
:   設為 1，讓 PostgreSQL 與 LDAP 伺服器之間的連線
    使用 TLS 加密。此方式依照
    [RFC 4513](https://datatracker.ietf.org/doc/html/rfc4513) 使用 `StartTLS`
    操作。
    也可參考 `ldapscheme` 選項作為替代方案。

請注意，使用 `ldapscheme` 或
`ldaptls` 僅會加密
PostgreSQL 伺服器與 LDAP 伺服器之間的流量。PostgreSQL
伺服器與 PostgreSQL 用戶端之間的連線
仍然不會加密，除非在該處也使用了 SSL。

以下選項僅用於 simple bind 模式：

`ldapprefix`
:   在進行 simple bind 認證時，於組成用於繫結的 DN 時，
    加在使用者名稱前面的字串。

`ldapsuffix`
:   在進行 simple bind 認證時，於組成用於繫結的 DN 時，
    加在使用者名稱後面的字串。

以下選項僅用於 search+bind 模式：

`ldapbasedn`
:   在進行 search+bind 認證時，開始搜尋使用者的根 DN。

`ldapbinddn`
:   在進行 search+bind 認證時，用於執行搜尋而繫結到目錄的使用者 DN。

`ldapbindpasswd`
:   在進行 search+bind 認證時，用於執行搜尋而繫結到目錄的使用者
    密碼。

`ldapsearchattribute`
:   在進行 search+bind 認證的搜尋中，用來與使用者名稱比對的屬性。若未指定屬性，
    則會使用
    `uid` 屬性。

`ldapsearchfilter`
:   進行 search+bind 認證時所使用的搜尋篩選條件。
    `$username` 出現的位置都會被替換為
    使用者名稱。這可以提供比
    `ldapsearchattribute` 更有彈性的搜尋篩選條件。

以下選項可作為另一種方式，以更精簡且標準的形式撰寫上述部分 LDAP 選項：

`ldapurl`
:   一個符合 [RFC 4516](https://datatracker.ietf.org/doc/html/rfc4516) 的
    LDAP URL。其格式為

    ```

    ldap[s]://host[:port]/basedn[?[attribute][?[scope][?[filter]]]]
    ```

    *`scope`* 必須是
    `base`、`one`、`sub`
    其中之一，通常會使用最後一個。（預設值為 `base`，
    這在本應用場景中通常沒有用處。）*`attribute`* 可以
    指定單一屬性，此時它會被用作
    `ldapsearchattribute` 的值。若
    *`attribute`* 為空，則
    *`filter`* 可以被用作
    `ldapsearchfilter` 的值。

    URL 配置（scheme）`ldaps` 會選用 LDAPS 方法
    透過 SSL 建立 LDAP 連線，等同於使用
    `ldapscheme=ldaps`。若要使用
    `StartTLS` 操作來使用加密的 LDAP
    連線，請使用一般的 URL 配置（scheme）
    `ldap`，並額外指定
    `ldaptls` 選項與
    `ldapurl`。

    對於非匿名繫結，`ldapbinddn`
    與 `ldapbindpasswd` 必須以分開的
    選項指定。

    LDAP URL 目前僅在
    OpenLDAP 上受支援，Windows 上不支援。

不可混用 simple bind 與 search+bind 的組態選項。若要在 simple bind 模式中使用
`ldapurl`，則該 URL 不得包含
`basedn` 或查詢元素。

使用 search+bind 模式時，搜尋可以使用
`ldapsearchattribute` 指定的單一屬性，或使用
`ldapsearchfilter`
指定自訂搜尋篩選條件來執行。
指定 `ldapsearchattribute=foo` 等同於
指定 `ldapsearchfilter="(foo=$username)"`。若兩個
選項皆未指定，則預設為
`ldapsearchattribute=uid`。

若 PostgreSQL 是以
OpenLDAP 作為 LDAP 用戶端函式庫編譯而成，則可以省略
`ldapserver` 設定。在此情況下，會透過
[RFC 2782](https://datatracker.ietf.org/doc/html/rfc2782) 的 DNS SRV 紀錄查詢一份
主機名稱與連接埠的清單。
系統會查詢名稱 `_ldap._tcp.DOMAIN`，其中
`DOMAIN` 是從 `ldapbasedn` 中取出的。

以下是一個 simple-bind LDAP 組態的範例：

```

host ... ldap ldapserver=ldap.example.net ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

當有人請求以資料庫
使用者 `someuser` 的身分連線到資料庫伺服器時，PostgreSQL 會嘗試
使用 DN `cn=someuser, dc=example,
dc=net`，以及用戶端所提供的密碼，繫結到 LDAP 伺服器。若該連線
成功，就會授予資料庫存取權。

以下是另一個 simple-bind 組態範例，使用 LDAPS 協定
與自訂連接埠號，並以 URL 形式撰寫：

```

host ... ldap ldapurl="ldaps://ldap.example.net:49151" ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

這比分別指定 `ldapserver`、
`ldapscheme` 與 `ldapport` 更為精簡。

以下是一個 search+bind 組態的範例：

```

host ... ldap ldapserver=ldap.example.net ldapbasedn="dc=example, dc=net" ldapsearchattribute=uid
```

當有人請求以資料庫
使用者 `someuser` 的身分連線到資料庫伺服器時，PostgreSQL 會嘗試
（由於未指定 `ldapbinddn`）以匿名方式繫結到
LDAP 伺服器，並在指定的 base DN 下搜尋
`(uid=someuser)`。若找到符合的項目，就會嘗試
以該找到的資訊及用戶端提供的密碼
進行繫結。若第二次繫結
成功，就會授予資料庫存取權。

以下是以 URL 形式撰寫的相同 search+bind 組態：

```

host ... ldap ldapurl="ldap://ldap.example.net/dc=example,dc=net?uid?sub"
```

其他支援以 LDAP 進行認證的軟體也使用相同的
URL 格式，因此更容易共用組態。

以下是一個 search+bind 組態的範例，使用
`ldapsearchfilter` 而非
`ldapsearchattribute`，以允許使用
使用者 ID 或電子郵件地址進行認證：

```

host ... ldap ldapserver=ldap.example.net ldapbasedn="dc=example, dc=net" ldapsearchfilter="(|(uid=$username)(mail=$username))"
```

以下是一個 search+bind 組態範例，使用 DNS SRV
探索方式來尋找網域名稱 `example.net`
所對應之 LDAP 服務的主機名稱與連接埠：

```

host ... ldap ldapbasedn="dc=example,dc=net"
```

### 提示

由於 LDAP 經常使用逗號與空格來分隔 DN 的不同
部分，在設定 LDAP 選項時通常需要使用雙引號括住參數
值，如上述範例所示。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-ldap.html)（原文版本：18.6；核對日期：2026-09-28）
