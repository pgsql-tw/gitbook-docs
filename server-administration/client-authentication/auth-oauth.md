<a id="AUTH-OAUTH"></a>

## 20.15. OAuth 授權／認證 [#](#AUTH-OAUTH)

<a id="id-1.6.7.22.2"></a>

OAuth 2.0 是一個業界標準框架，定義於
[RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)，
用於讓第三方應用程式取得對受保護資源的有限存取權。
OAuth 用戶端支援必須在建置 PostgreSQL
時啟用，詳見[第 17 章](../installation/README.md)。

本文件在討論 OAuth 生態系統時使用下列術語：

Resource Owner（資源擁有者，或稱 End User／終端使用者）
:   擁有受保護資源，並能授予存取這些資源之權限的使用者或系統。本文件也在資源擁有者為個人時使用*終端使用者*一詞。當你使用
    psql 透過 OAuth 連線到資料庫時，
    你就是資源擁有者／終端使用者。

Client（用戶端）
:   使用存取權杖來存取受保護資源的系統。使用 libpq 的應用程式，例如 psql，
    在連線到
    PostgreSQL 叢集時即為 OAuth 用戶端。

Resource Server（資源伺服器）
:   代管受保護資源、供用戶端存取的系統。所連線的
    PostgreSQL 叢集即為資源伺服器。

Provider（提供者）
:   開發及／或管理某特定應用程式之 OAuth 授權伺服器與用戶端的組織、產品供應商或其他實體。
    不同的提供者通常會為其 OAuth 系統選擇不同的實作細節；某一提供者的用戶端通常
    無法保證能存取另一提供者的伺服器。

    「provider」一詞的這種用法並非標準用語，但在口語上似乎已相當普遍。（不應與 OpenID 中類似的
    「Identity Provider（身分識別提供者）」一詞混淆。雖然
    PostgreSQL 中 OAuth 的實作旨在
    與 OpenID Connect／OIDC 相容並可互通，但它本身並非 OIDC 用戶端，
    也不要求必須使用 OIDC。）

Authorization Server（授權伺服器）
:   在通過驗證的資源擁有者核准後，接收來自用戶端的請求並向其核發存取權杖的系統。
    PostgreSQL 本身不提供授權
    伺服器；此為 OAuth 提供者的職責。

<a id="AUTH-OAUTH-ISSUER"></a>Issuer（核發者）
:   授權伺服器的識別碼，以
    `https://` URL 的形式呈現，為 OAuth 用戶端與應用程式提供一個可信任的「命名空間」。
    核發者識別碼讓單一授權伺服器可以與互不信任之各方的用戶端溝通，
    只要它們各自維護獨立的核發者即可。

### 注意

對於小型部署而言，「provider（提供者）」、「authorization server（授權伺服器）」與「issuer（核發者）」之間
可能沒有明顯的區別。然而，對於較複雜的設定，
可能會存在一對多（或多對多）的
關係：一個提供者可能將多個核發者識別碼出租給
不同的租戶，然後提供多個授權伺服器，這些伺服器可能支援
不同的功能集合，用以與其用戶端互動。

PostgreSQL 支援 bearer token（持有者權杖），定義於
[RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750)，
這是一種用於 OAuth 2.0 的存取權杖類型，其中權杖本身是不透明的字串。存取權杖的格式屬於實作細節，
由各授權伺服器自行選擇。

OAuth 支援下列組態選項：

`issuer`
:   一個 HTTPS URL，須為授權伺服器發現文件所定義的準確
    [核發者識別碼](auth-oauth.md#AUTH-OAUTH-ISSUER)，或是直接指向該
    發現文件的知名（well-known）URI。此
    參數為必要參數。

    當 OAuth 用戶端連線到伺服器時，會使用核發者識別碼建構出發現
    文件的 URL。預設情況下，此 URL 採用 OpenID Connect Discovery 的慣例：
    會將路徑
    `/.well-known/openid-configuration` 附加到核發者識別碼的
    結尾。或者，若
    `issuer` 中包含 `/.well-known/`
    路徑片段，則該 URL 會原封不動地提供給用戶端。

    ### 警告

    libpq 中的 OAuth 用戶端要求伺服器的 issuer 設定必須
    與發現文件中所提供的核發者識別碼完全相符，而該識別碼又必須進一步與用戶端的
    [oauth_issuer](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) 設定相符。大小寫或格式上
    不允許有任何差異。

`scope`
:   以空格分隔的 OAuth scope（範圍）清單，是伺服器授權用戶端並驗證使用者所需的範圍。適當的值
    由授權伺服器及所使用的 OAuth 驗證
    模組決定（關於驗證器的更多資訊，詳見[第 50 章](../../server-programming/oauth-validators/README.md)）。此參數為必要參數。

`validator`
:   用於驗證 bearer token 的函式庫。若指定此參數，其名稱必須
    與 [oauth_validator_libraries](../runtime-config/runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES) 中列出的其中一個函式庫完全相符。此參數為
    選用參數，但若 `oauth_validator_libraries` 中包含
    一個以上的函式庫，則此參數為必要參數。

`map`
:   允許在 OAuth 身分識別提供者與資料庫使用者
    名稱之間進行對應。詳見[第 20.2 節](auth-username-maps.md)。若未指定
    對應，則權杖所關聯的使用者名稱（由
    OAuth 驗證器判定）必須與所請求的角色名稱完全相符。此參數為選用參數。

<a id="AUTH-OAUTH-DELEGATE-IDENT-MAPPING"></a> `delegate_ident_mapping`
:   一個進階選項，並非用於一般使用場合。

    當設為 `1` 時，會略過以
    `pg_ident.conf` 進行的標準使用者對應，改由 OAuth 驗證器
    全權負責將終端使用者身分對應到資料庫
    角色。若驗證器授權該權杖，伺服器便會信任
    該使用者被允許以所請求的角色連線，且無論該使用者的認證狀態為何，
    該連線都會被允許繼續進行。

    此參數與 `map` 互不相容。

    ### 警告

    `delegate_ident_mapping` 在認證系統的設計上
    提供了額外的彈性，但也
    要求 OAuth 驗證器必須經過謹慎的實作，除了所有驗證器都必須具備的
    [標準
    檢查](../../server-programming/oauth-validators/README.md)之外，還必須判定所提供的權杖是否
    帶有足夠的終端使用者權限。請謹慎使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-oauth.html)（原文版本：18.6；核對日期：2026-09-28）
