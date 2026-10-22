<a id="SSLINFO"></a>

## F.42. sslinfo — 取得用戶端 SSL 資訊 [#](#SSLINFO)

[F.42.1. 提供的函式](sslinfo.md#SSLINFO-FUNCTIONS)

[F.42.2. 作者](sslinfo.md#SSLINFO-AUTHOR)

<a id="id-1.11.7.52.2"></a>

`sslinfo` 模組提供目前用戶端連線至 PostgreSQL 時所提供之 SSL 憑證的相關資訊。若目前連線未使用 SSL，此模組就沒有用處（大多數函式會傳回 NULL）。

透過此模組取得的部分資訊，也可以使用內建系統檢視表 [`pg_stat_ssl`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW) 取得。

除非安裝時以 `--with-ssl=openssl` 進行設定，否則此擴充功能完全無法建置。

<a id="SSLINFO-FUNCTIONS"></a>

### F.42.1. 提供的函式 [#](#SSLINFO-FUNCTIONS)

`ssl_is_used() returns boolean` <a id="id-1.11.7.52.6.2.1.1.2"></a>
:   若目前與伺服器的連線使用 SSL 則傳回 true，否則傳回 false。

`ssl_version() returns text` <a id="id-1.11.7.52.6.2.2.1.2"></a>
:   傳回 SSL 連線所使用之通訊協定的名稱（例如 TLSv1.0、TLSv1.1、TLSv1.2 或 TLSv1.3）。

`ssl_cipher() returns text` <a id="id-1.11.7.52.6.2.3.1.2"></a>
:   傳回 SSL 連線所使用之加密演算法（cipher）的名稱（例如 DHE-RSA-AES256-SHA）。

`ssl_client_cert_present() returns boolean` <a id="id-1.11.7.52.6.2.4.1.2"></a>
:   若目前用戶端已向伺服器出示有效的 SSL 用戶端憑證則傳回 true，否則傳回 false。（伺服器可能設定為要求用戶端憑證，也可能沒有。）

`ssl_client_serial() returns numeric` <a id="id-1.11.7.52.6.2.5.1.2"></a>
:   傳回目前用戶端憑證的序號。憑證序號與憑證簽發者的組合保證能唯一識別一張憑證（但無法識別其擁有者——擁有者理應定期更換金鑰，並向簽發者取得新憑證）。

    因此，若你自行經營 CA，並只允許伺服器接受此 CA 簽發的憑證，序號就是識別使用者最可靠（雖然不太好記）的方式。

`ssl_client_dn() returns text` <a id="id-1.11.7.52.6.2.6.1.2"></a>
:   傳回目前用戶端憑證的完整主體（subject），並將字元資料轉換為目前資料庫的編碼。此處假設若你在憑證名稱中使用非 ASCII 字元，你的資料庫也能表示這些字元。若你的資料庫使用 SQL_ASCII 編碼，名稱中的非 ASCII 字元會以 UTF-8 序列表示。

    結果看起來類似 `/CN=Somebody /C=Some country/O=Some organization`。

`ssl_issuer_dn() returns text` <a id="id-1.11.7.52.6.2.7.1.2"></a>
:   傳回目前用戶端憑證的完整簽發者名稱，並將字元資料轉換為目前資料庫的編碼。編碼轉換的處理方式與 `ssl_client_dn` 相同。

    此函式的傳回值與憑證序號的組合可唯一識別該憑證。

    只有在伺服器的憑證授權單位檔案中有超過一個受信任的 CA 憑證，或此 CA 曾簽發一些中繼憑證授權單位憑證時，此函式才真正有用。

`ssl_client_dn_field(fieldname text) returns text` <a id="id-1.11.7.52.6.2.8.1.2"></a>
:   此函式傳回憑證主體中指定欄位的值；若該欄位不存在，則傳回 NULL。欄位名稱是字串常數，會使用 OpenSSL 物件資料庫轉換為 ASN1 物件識別碼。可接受下列值：

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

    除了 `commonName` 以外，這些欄位都是選用的。要包含哪些欄位、不包含哪些欄位，完全取決於你的 CA 政策。不過，這些欄位的意義由 X.500 與 X.509 標準嚴格定義，因此你不能任意賦予它們意義。

    譯註：上列清單中 description 出現兩次，為原文重複列出，並非兩個不同的欄位。

`ssl_issuer_field(fieldname text) returns text` <a id="id-1.11.7.52.6.2.9.1.2"></a>
:   與 `ssl_client_dn_field` 相同，但對象是憑證簽發者，而非憑證主體。

`ssl_extension_info() returns setof record` <a id="id-1.11.7.52.6.2.10.1.2"></a>
:   提供用戶端憑證擴充項目（extension）的相關資訊：擴充項目名稱、擴充項目值，以及它是否為關鍵（critical）擴充項目。

<a id="SSLINFO-AUTHOR"></a>

### F.42.2. 作者 [#](#SSLINFO-AUTHOR)

Victor Wagner `<vitus@cryptocom.ru>`, Cryptocom LTD

Dmitry Voronin `<carriingfate92@yandex.ru>`

Cryptocom OpenSSL 開發小組的電子郵件：
`<openssl@cryptocom.ru>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sslinfo.html)（原文版本：18.6；核對日期：2026-10-22）
