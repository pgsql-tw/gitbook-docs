<a id="AUTH-PG-HBA-CONF"></a>

## 20.1. `pg_hba.conf` 檔案 [#](#AUTH-PG-HBA-CONF)

<a id="id-1.6.7.8.2"></a>

用戶端認證是由一個設定檔控制的，該檔案傳統上命名為
`pg_hba.conf`，並存放在資料庫
叢集的資料目錄中。
（HBA 代表 host-based authentication，主機基礎認證。）當資料
目錄由 [initdb](../../reference/reference-server/app-initdb.md) 初始化時，會安裝一份預設的
`pg_hba.conf` 檔案。你也
可以將認證設定檔放在別處；請參閱
[hba_file](../runtime-config/runtime-config-file-locations.md#GUC-HBA-FILE) 設定參數。

`pg_hba.conf` 檔案會在啟動時讀取，也會在
主要伺服器程序收到
SIGHUP<a id="id-1.6.7.8.4.3"></a>
訊號時讀取。如果你在一套
運作中的系統上編輯此檔案，就需要對 postmaster 發出訊號
（可使用 `pg_ctl reload`、呼叫 SQL 函式
`pg_reload_conf()`，或使用 `kill
-HUP`），讓它重新讀取該檔案。

### 注意

上述說法在 Microsoft Windows 上並不成立：在該平台上，
`pg_hba.conf` 檔案的任何變更都會立即
套用到之後的新連線。

系統檢視表
[`pg_hba_file_rules`](../../internals/views/view-pg-hba-file-rules.md)
有助於預先測試對 `pg_hba.conf`
檔案所做的變更，或是在檔案載入後未達到預期效果時用來診斷問題。檢視表中
`error` 欄位非 null 的資料列，代表
檔案中對應那幾行存在問題。

`pg_hba.conf` 檔案的一般格式
是一組記錄，每行一筆。空白行會被忽略，`#`
註解字元之後的任何文字也會被忽略。
一筆記錄可以在行尾加上反斜線來延續到下一行。（反斜線
除了在行尾之外並不具有特殊意義。）一筆記錄是
由多個以空格及／或定位字元分隔的欄位所組成。
若欄位值使用雙引號括住，欄位便可以包含空白字元。
若將資料庫、使用者或位址欄位中的某個關鍵字（例如
`all` 或 `replication`）加上引號，就會讓該字詞失去其特殊
意義，只單純比對名稱與該字詞相同的資料庫、使用者或主機。
即使在加了引號的文字或註解內，反斜線的接行規則仍然適用。

每筆認證記錄都指定了連線類型、用戶端 IP 位址
範圍（若該連線類型需要）、資料庫名稱、使用者名稱，
以及要用於符合這些參數之連線的認證方法。系統會採用
第一筆連線類型、用戶端位址、要求的資料庫及使用者名稱皆
相符的記錄來執行認證。這裡沒有「順延」（fall-through）或
「備援」（backup）機制：一旦選定某筆記錄而認證
失敗，後續的記錄就不會再被考慮。若沒有任何記錄相符，
則拒絕存取。

每筆記錄可以是一個 include 指示詞，也可以是一筆認證記錄。
Include 指示詞用來指定可以被納入、內含其他記錄的檔案。
這些記錄會被插入到 include 指示詞所在的位置。Include 指示詞只
包含兩個欄位：`include`、`include_if_exists` 或
`include_dir` 指示詞，以及要納入的檔案或目錄。
檔案或目錄可以是相對路徑或絕對路徑，也可以
加上雙引號。對於 `include_dir` 形式，所有
不以 `.` 開頭且以 `.conf` 結尾
的檔案都會被納入。同一個 include 目錄中的多個檔案會依
檔名順序處理（依 C locale 規則，也就是數字排在字母
之前，大寫字母排在小寫字母之前）。

一筆記錄可以有下列幾種格式：

```

local               database  user  auth-method [auth-options]
host                database  user  address     auth-method  [auth-options]
hostssl             database  user  address     auth-method  [auth-options]
hostnossl           database  user  address     auth-method  [auth-options]
hostgssenc          database  user  address     auth-method  [auth-options]
hostnogssenc        database  user  address     auth-method  [auth-options]
host                database  user  IP-address  IP-mask      auth-method  [auth-options]
hostssl             database  user  IP-address  IP-mask      auth-method  [auth-options]
hostnossl           database  user  IP-address  IP-mask      auth-method  [auth-options]
hostgssenc          database  user  IP-address  IP-mask      auth-method  [auth-options]
hostnogssenc        database  user  IP-address  IP-mask      auth-method  [auth-options]
include             file
include_if_exists   file
include_dir         directory
```

各欄位的意義如下：

`local`
:   此記錄比對使用 Unix 網域通訊端（Unix-domain socket）的連線嘗試。
    若沒有這種類型的記錄，Unix 網域通訊端
    連線將被禁止。

`host`
:   此記錄比對使用 TCP/IP 進行的連線嘗試。
    `host` 記錄可比對
    SSL 或非 SSL 連線
    嘗試，也可比對 GSSAPI 加密或
    非 GSSAPI 加密的連線嘗試。

    ### 注意

    除非伺服器在啟動時設定了適當的
    [listen_addresses](../runtime-config/runtime-config-connection.md#GUC-LISTEN-ADDRESSES) 設定參數，否則無法使用遠端 TCP/IP
    連線，因為預設行為僅在本地回送位址
    `localhost` 上監聽 TCP/IP 連線。

`hostssl`
:   此記錄比對使用 TCP/IP 進行的連線嘗試，
    但僅限於連線是以 SSL
    加密建立時。

    若要使用此選項，伺服器必須以支援
    SSL 的方式建置。此外，還必須透過設定
    [ssl](../runtime-config/runtime-config-connection.md#GUC-SSL) 設定參數來啟用
    SSL（詳情請見
    [第 18.9 節](../runtime/ssl-tcp.md)）。
    否則，`hostssl` 記錄會被忽略，只會記錄一則
    警告，說明它無法比對任何連線。

`hostnossl`
:   此記錄類型的行為與 `hostssl` 相反；
    它只比對透過
    TCP/IP 進行、且未使用 SSL 的連線嘗試。

`hostgssenc`
:   此記錄比對使用 TCP/IP 進行的連線嘗試，
    但僅限於連線是以 GSSAPI
    加密建立時。

    若要使用此選項，伺服器必須以支援
    GSSAPI 的方式建置。否則，
    `hostgssenc` 記錄會被忽略，只會記錄
    一則警告，說明它無法比對任何連線。

`hostnogssenc`
:   此記錄類型的行為與 `hostgssenc` 相反；
    它只比對透過
    TCP/IP 進行、且未使用 GSSAPI 加密的連線嘗試。

*`database`*
:   指定此記錄比對哪個（些）資料庫名稱。值為
    `all` 表示比對所有資料庫。
    值為 `sameuser` 表示只有在要求的資料庫
    與要求的使用者同名時才比對。值為 `samerole`
    表示要求的使用者必須是與該資料庫同名之角色的
    成員。（`samegroup` 是 `samerole` 的
    過時但仍可接受的拼法。）
    就 `samerole` 的判定而言，超級使用者
    並不會被視為某角色的成員，除非他們是直接或間接地
    明確屬於該角色，而不只是因為身為超級使用者。
    值為 `replication` 表示只有在要求的是實體複寫
    連線時才比對，但不會比對邏輯複寫連線。請注意，
    實體複寫連線不會指定任何特定資料庫，而邏輯複寫
    連線則會指定。
    除此之外，這裡填入的就是某個特定
    PostgreSQL 資料庫的名稱，或是一個正規表示式。
    可以用逗號分隔，指定多個資料庫名稱及／或正規表示式。

    若資料庫名稱以斜線（`/`）開頭，則該
    名稱其餘的部分會被視為正規表示式。
    （關於 PostgreSQL 正規表示式語法的詳情，請參閱
    [第 9.7.3.1 節](../../the-sql-language/functions/functions-matching.md#POSIX-SYNTAX-DETAILS)。）

    也可以在檔名前加上 `@`，指定一個內含
    資料庫名稱及／或正規表示式的獨立檔案。

*`user`*
:   指定此記錄比對哪個（些）資料庫使用者
    名稱。值為 `all` 表示
    比對所有使用者。除此之外，這裡填入的可以是某個
    特定資料庫使用者的名稱、以斜線
    （`/`）開頭的正規表示式，或是以 `+`
    開頭的群組名稱。
    （請回想一下，PostgreSQL 中使用者與群組並沒有
    真正的區別；`+` 記號的意思其實是
    「比對所有直接或間接是該角色成員的所有角色」，
    而沒有 `+` 記號的名稱則只比對該特定角色本身。）
    就此而言，超級使用者只有在他們直接或間接地明確
    屬於該角色時，才會被視為該角色的成員，而不只是
    因為身為超級使用者。
    可以用逗號分隔，指定多個使用者名稱及／或正規表示式。

    若使用者名稱以斜線（`/`）開頭，則該
    名稱其餘的部分會被視為正規表示式。
    （關於 PostgreSQL 正規表示式語法的詳情，請參閱
    [第 9.7.3.1 節](../../the-sql-language/functions/functions-matching.md#POSIX-SYNTAX-DETAILS)。）

    也可以在檔名前加上 `@`，指定一個內含
    使用者名稱及／或正規表示式的獨立檔案。

*`address`*
:   指定此記錄比對哪個（些）用戶端機器
    位址。這個欄位可以包含主機名稱、IP
    位址範圍，或下列所述的特殊關鍵字之一。

    IP 位址範圍以標準數字表示法指定，先寫出
    範圍起始位址，接著加上斜線（`/`）
    及 CIDR 遮罩長度。遮罩
    長度表示用戶端 IP 位址中必須相符的高位元
    數目。這個位元數右側的部分，在給定的 IP 位址中
    應該為零。
    在 IP 位址、`/`
    與 CIDR 遮罩長度之間，不能有任何空白字元。

    以這種方式指定的 IPv4 位址範圍，典型範例為
    `172.20.143.89/32`（表示單一主機），或
    `172.20.143.0/24`（表示一個小型網路），或
    `10.6.0.0/16`（表示一個較大的網路）。
    IPv6 位址範圍看起來可能像 `::1/128`
    （表示單一主機，此例中為 IPv6 回送位址），或
    `fe80::7a31:c1ff:0000:0000/96`（表示一個
    小型網路）。
    `0.0.0.0/0` 代表所有
    IPv4 位址，而 `::0/0` 代表
    所有 IPv6 位址。
    若要指定單一主機，IPv4 請使用遮罩長度 32，IPv6 請使用
    128。在網路位址中，不要省略尾端的零。

    以 IPv4 格式指定的項目只會比對 IPv4 連線，
    而以 IPv6 格式指定的項目只會比對 IPv6 連線，
    即使所代表的位址落在 IPv4-in-IPv6 範圍內也一樣。

    你也可以寫 `all` 來比對任何 IP 位址，
    寫 `samehost` 來比對伺服器自身的任一
    IP 位址，或寫 `samenet` 來比對伺服器
    直接連接之任一子網路中的任何位址。

    若指定的是主機名稱（凡不是 IP 位址
    範圍或特殊關鍵字的內容，都會被視為主機名稱），
    該名稱會與用戶端 IP 位址反解析
    （例如反向 DNS 查詢，若使用 DNS）的結果進行比對。主機名稱比對
    不區分大小寫。若相符，接著會對該主機
    名稱執行正向名稱解析（例如正向 DNS 查詢），以檢查
    其解析出的位址中，是否有任一個等於用戶端的
    IP 位址。若兩個方向都相符，則此
    項目視為相符。（`pg_hba.conf` 中所
    使用的主機名稱，應該是用戶端 IP 位址反解析
    所得到的那一個，否則該行不會被比對成功。有些主機名稱
    資料庫允許將一個 IP 位址關聯到多個主機名稱，但
    作業系統在被要求解析某個 IP 位址時只會回傳
    一個主機名稱。）

    以點號（`.`）開頭的主機名稱
    指定方式，比對的是實際主機名稱的後綴。因此
    `.example.com` 會比對
    `foo.example.com`（但不會比對單獨的
    `example.com`）。

    在 `pg_hba.conf` 中指定主機名稱
    時，你應該確認名稱解析的速度夠快。設置像
    `nscd` 這樣的本地名稱解析快取，會有
    幫助。此外，你可能會想啟用
    `log_hostname` 設定參數，讓記錄檔中
    顯示用戶端的主機名稱，而不是 IP 位址。

    這些欄位不適用於 `local` 記錄。

    ### 注意

    使用者有時會納悶，為什麼主機名稱要以這種看似
    複雜的方式處理，需要進行兩次名稱解析，其中包含
    一次對用戶端 IP 位址的反向查詢。這使得在用戶端
    的反向 DNS 項目未設定，或解析出不理想主機名稱的
    情況下，此功能的使用變得複雜。之所以這麼做，主要是
    為了效率：以這種方式，一次連線嘗試最多只需要兩次
    名稱解析查詢，一次反向、一次正向。若某個位址存在
    解析器問題，也只會成為那個用戶端自己的問題。假設
    改用一種只做正向查詢的替代實作方式，則每次連線嘗試
    都必須解析
    `pg_hba.conf` 中所提到的每一個主機名稱。
    若列出的名稱很多，這可能會相當緩慢。
    而且若其中某個主機名稱存在解析器問題，
    就會變成每個人的問題。

    此外，反向查詢也是實作後綴比對功能所必需的，
    因為必須先知道實際的用戶端主機名稱，
    才能拿它去比對模式。

    請注意，這種行為與其他常見的主機名稱基礎存取
    控制實作方式（例如 Apache HTTP 伺服器與
    TCP Wrappers）是一致的。

*`IP-address`*<br>*`IP-mask`*
:   這兩個欄位可以做為
    *`IP-address`*`/`*`mask-length`*
    表示法的替代方式使用。此時不是指定遮罩
    長度，而是在另一個獨立欄位中指定實際的遮罩。
    例如，`255.0.0.0` 代表 IPv4
    CIDR 遮罩長度 8，而 `255.255.255.255` 代表
    CIDR 遮罩長度 32。

    這些欄位不適用於 `local` 記錄。

*`auth-method`*
:   指定連線符合此記錄時要使用的認證方法。可用的
    選項摘要如下；詳情請見
    [第 20.3 節](auth-methods.md)。所有選項
    皆為小寫，且區分大小寫比對，因此即使是像
    `ldap` 這樣的縮寫，也必須以小寫指定。

    `trust`
    :   無條件允許連線。此方法
        允許任何能夠連上
        PostgreSQL 資料庫伺服器的人，以他們想要的任何
        PostgreSQL 使用者身分登入，
        不需要密碼或任何其他認證。詳情請見 [第 20.4 節](auth-trust.md)。

    `reject`
    :   無條件拒絕連線。這對於
        從一個群組中「過濾掉」某些主機很有用，例如一行
        `reject` 可以擋掉某個特定主機的連線，
        同時後面的一行則允許特定網路中其餘的主機連線。

    `scram-sha-256`
    :   執行 SCRAM-SHA-256 認證，以驗證使用者的
        密碼。詳情請見 [第 20.5 節](auth-password.md)。

    `md5`
    :   執行 SCRAM-SHA-256 或 MD5 認證，以驗證
        使用者的密碼。詳情請見 [第 20.5 節](auth-password.md)。

        ### 警告

        對 MD5 加密密碼的支援已被棄用，並將在
        PostgreSQL 未來的版本中
        移除。關於遷移至其他密碼類型的詳情，請參閱
        [第 20.5 節](auth-password.md)。

    `password`
    :   要求用戶端提供未加密的密碼以進行
        認證。
        由於密碼是以明文方式在網路上
        傳送，不應該在不受信任的網路上使用此方式。
        詳情請見 [第 20.5 節](auth-password.md)。

    `gss`
    :   使用 GSSAPI 認證使用者。此方式僅
        適用於 TCP/IP 連線。詳情請見 [第 20.6 節](gssapi-auth.md)。它可以與
        GSSAPI 加密搭配使用。

    `sspi`
    :   使用 SSPI 認證使用者。此方式僅
        適用於 Windows。詳情請見 [第 20.7 節](sspi-auth.md)。

    `ident`
    :   透過與用戶端上的 ident 伺服器聯繫，取得
        用戶端的作業系統使用者名稱，
        並檢查是否與要求的資料庫使用者名稱相符。
        Ident 認證只能用於 TCP/IP
        連線。若對本地連線指定此方式，則會改用
        peer 認證。
        詳情請見 [第 20.8 節](auth-ident.md)。

    `peer`
    :   從作業系統取得用戶端的作業系統
        使用者名稱，並檢查是否與要求的資料庫使用者名稱相符。
        此方式僅適用於本地連線。
        詳情請見 [第 20.9 節](auth-peer.md)。

    `ldap`
    :   使用 LDAP 伺服器進行認證。詳情請見 [第 20.10 節](auth-ldap.md)。

    `radius`
    :   使用 RADIUS 伺服器進行認證。詳情請見 [第 20.11 節](auth-radius.md)。

    `cert`
    :   使用 SSL 用戶端憑證進行認證。詳情請見
        [第 20.12 節](auth-cert.md)。

    `pam`
    :   使用作業系統提供的 Pluggable Authentication
        Modules（PAM）服務進行認證。詳情請見 [第 20.13 節](auth-pam.md)。

    `bsd`
    :   使用作業系統提供的 BSD Authentication 服務
        進行認證。詳情請見 [第 20.14 節](auth-bsd.md)。

    `oauth`
    :   使用第三方 OAuth 2.0
        身分識別提供者進行授權，並可選擇性地進行認證。詳情請見 [第 20.15 節](auth-oauth.md)。

*`auth-options`*
:   在 *`auth-method`* 欄位之後，可以有一個或多個
    *`name`*`=`*`value`* 形式的欄位，用來
    指定該認證方法的選項。哪些選項可用於哪些
    認證方法，詳情列於下方。

    除了下方列出的各方法專屬選項之外，還有一個
    與方法無關的認證選項 `clientcert`，
    可以在任何 `hostssl` 記錄中指定。
    此選項可設為 `verify-ca` 或
    `verify-full`。這兩個選項都要求用戶端
    出示有效（受信任）的 SSL 憑證，而
    `verify-full` 另外還會強制要求憑證中的
    `cn`（Common Name）
    必須與使用者名稱或某個適用的對應相符。
    此行為與 `cert` 認證方式
    （見 [第 20.12 節](auth-cert.md)）相似，但可讓你將用戶端憑證
    的驗證，與任何支援 `hostssl` 項目的
    認證方法搭配使用。

    在任何使用用戶端憑證認證的記錄上（也就是使用
    `cert` 認證方法，或使用
    `clientcert` 選項的記錄），你可以透過
    `clientname` 選項指定要比對用戶端憑證中的
    哪個部分。此選項可以有兩種
    值。若指定 `clientname=CN`（此為
    預設值），使用者名稱會與憑證的
    `Common Name (CN)` 比對。若改為指定
    `clientname=DN`，使用者名稱則會與憑證的
    整個 `Distinguished Name (DN)` 比對。
    此選項可能最適合搭配使用者名稱對應表使用。
    比對時使用的 `DN` 格式為
    [RFC 2253](https://datatracker.ietf.org/doc/html/rfc2253)
    格式。若要以這種格式查看用戶端憑證的
    `DN`，可執行

    ```

    openssl x509 -in myclient.crt -noout -subject -nameopt RFC2253 | sed "s/^subject=//"
    ```

    使用此選項時需要特別小心，尤其是在對
    `DN` 使用正規表示式比對時。

`include`
:   這一行會被替換為指定檔案的內容。

`include_if_exists`
:   若指定檔案存在，這一行會被替換為該檔案的內容；
    否則會記錄一則訊息，指出該檔案已被略過。

`include_dir`
:   這一行會被替換為在該目錄中找到的所有檔案的內容，
    只要檔名不以 `.` 開頭、且以
    `.conf` 結尾，並依檔名順序（依
    C locale 規則，也就是數字排在字母之前，大寫字母
    排在小寫字母之前）處理。

以 `@` 結構納入的檔案，會被讀取為名稱清單，
可以用空白字元或逗號分隔。註解以
`#` 開頭，與
`pg_hba.conf` 中相同，也允許巢狀的
`@` 結構。除非 `@` 後面接的檔名
是絕對路徑，否則會被視為相對於引用該檔名之
檔案所在的目錄。

由於 `pg_hba.conf` 的每筆記錄會針對每次
連線嘗試依序檢查，因此記錄的順序很
重要。一般來說，前面的記錄會有較嚴格的連線
比對參數與較弱的認證方法，而後面的
記錄則會有較寬鬆的比對參數與較強的認證
方法。例如，你可能希望對本地 TCP/IP 連線使用
`trust` 認證，但要求遠端 TCP/IP 連線
提供密碼。在這種情況下，指定針對來自 127.0.0.1
連線使用 `trust` 認證的記錄，就應該出現在
針對更廣範圍之允許用戶端 IP 位址指定密碼認證的
記錄之前。

### 提示

要連線到特定資料庫，使用者不僅要通過
`pg_hba.conf` 的檢查，還必須擁有該資料庫的
`CONNECT` 權限。如果你想限制哪些使用者可以連線到
哪些資料庫，通常透過授予／撤銷 `CONNECT` 權限
來控制，會比把規則寫進 `pg_hba.conf` 項目中更容易。

[範例 20.1](auth-pg-hba-conf.md#EXAMPLE-PG-HBA.CONF) 展示了一些
`pg_hba.conf` 項目的範例。關於各種
認證方法的詳情，請參閱下一節。

<a id="EXAMPLE-PG-HBA.CONF"></a>

**範例 20.1. `pg_hba.conf` 項目範例**

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

# The same using a regular expression for DATABASE, that allows connection
# to any databases with a name beginning with "db" and finishing with a
# number using two to four digits (like "db1234" or "db12").
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    "/^db\d{2,4}$"  all             localhost               trust

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

# In the absence of preceding "host" lines, these three lines will
# reject all connections from 192.168.54.1 (since that entry will be
# matched first), but allow GSSAPI-encrypted connections from anywhere else
# on the Internet.  The zero mask causes no bits of the host IP address to
# be considered, so it matches any host.  Unencrypted GSSAPI connections
# (which "fall through" to the third line since "hostgssenc" only matches
# encrypted GSSAPI connections) are allowed, but only from 192.168.12.10.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.54.1/32         reject
hostgssenc all          all             0.0.0.0/0               gss
host    all             all             192.168.12.10/32        gss

# Allow users from 192.168.x.x hosts to connect to any database, if
# they pass the ident check.  If, for example, ident says the user is
# "bryanh" and he requests to connect as PostgreSQL user "guest1", the
# connection is allowed if there is an entry in pg_ident.conf for map
# "omicron" that says "bryanh" is allowed to connect as "guest1".
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.0.0/16          ident map=omicron

# If these are the only four lines for local connections, they will
# allow local users to connect only to their own databases (databases
# with the same name as their database user name) except for users whose
# name end with "helpdesk", administrators and members of role "support",
# who can connect to all databases.  The file $PGDATA/admins contains a
# list of names of administrators.  Passwords are required in all cases.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   sameuser        all                                     scram-sha-256
local   all             /^.*helpdesk$                           scram-sha-256
local   all             @admins                                 scram-sha-256
local   all             +support                                scram-sha-256

# The last two lines above can be combined into a single line:
local   all             @admins,+support                        scram-sha-256

# The database column can also use lists and file names:
local   db1,db2,@demodbs  all                                   scram-sha-256
```

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-pg-hba-conf.html)（原文版本：18.6；核對日期：2026-09-26）
