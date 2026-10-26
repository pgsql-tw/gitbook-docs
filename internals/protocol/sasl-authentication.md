<a id="SASL-AUTHENTICATION"></a>

## 54.3. SASL 身分驗證 [#](#sasl-authentication) <a href="#sasl-authentication" id="sasl-authentication"></a>

[54.3.1. SCRAM-SHA-256 身分驗證](sasl-authentication.md#sasl-scram-sha-256)

[54.3.2. OAUTHBEARER 身分驗證](sasl-authentication.md#sasl-oauthbearer)

*SASL* 是用於連線導向協定的身分驗證框架。目前，PostgreSQL 實作了三種 SASL 身分驗證機制：SCRAM-SHA-256、SCRAM-SHA-256-PLUS 與 OAUTHBEARER。未來可能會加入更多機制。下列步驟說明一般而言 SASL 身分驗證如何進行，而接下來的小節則會提供特定機制的更多細節。

<a id="id-1.10.6.8.3"></a>

**SASL 身分驗證訊息流程**

<a id="SASL-AUTH-BEGIN"></a>1. 為了開始 SASL 身分驗證交換，伺服器會送出 AuthenticationSASL 訊息。其中包含伺服器可以接受的 SASL 身分驗證機制清單，並依伺服器偏好的順序排列。
<a id="SASL-AUTH-INITIAL-RESPONSE"></a>2. 用戶端從清單中選擇一個支援的機制，並向伺服器送出 SASLInitialResponse 訊息。該訊息包含所選機制的名稱，以及選用的初始用戶端回應（Initial Client Response），如果所選機制有使用的話。
<a id="SASL-AUTH-CONTINUE"></a>3. 接著會有一則或多則伺服器挑戰（server-challenge）與用戶端回應（client-response）訊息。每個伺服器挑戰都以 AuthenticationSASLContinue 訊息送出，隨後由用戶端以 SASLResponse 訊息回應。這些訊息的具體內容取決於機制。
<a id="SASL-AUTH-END"></a>4. 最後，當身分驗證交換成功完成時，伺服器會送出一則選用的 AuthenticationSASLFinal 訊息，緊接著送出 AuthenticationOk 訊息。AuthenticationSASLFinal 包含額外的伺服器到用戶端資料，其內容依所選的身分驗證機制而定。如果該身分驗證機制不使用在完成時送出的額外資料，就不會送出 AuthenticationSASLFinal 訊息。

發生錯誤時，伺服器可以在任何階段中止身分驗證，並送出 ErrorMessage。

<a id="SASL-SCRAM-SHA-256"></a>

### 54.3.1. SCRAM-SHA-256 身分驗證 [#](#sasl-scram-sha-256) <a href="#sasl-scram-sha-256" id="sasl-scram-sha-256"></a>

`SCRAM-SHA-256` 及其具備通道綁定（channel binding）的變體 `SCRAM-SHA-256-PLUS`，都是以密碼為基礎的身分驗證機制。[RFC 7677](https://datatracker.ietf.org/doc/html/rfc7677) 與 [RFC 5802](https://datatracker.ietf.org/doc/html/rfc5802) 中有詳細說明。

在 PostgreSQL 中使用 SCRAM-SHA-256 時，伺服器會忽略用戶端在 `client-first-message` 中送出的使用者名稱，而改用先前已在啟動訊息中送出的使用者名稱。PostgreSQL 支援多種字元編碼，而 SCRAM 規定使用者名稱必須使用 UTF-8，因此 PostgreSQL 的使用者名稱可能無法以 UTF-8 表示。

SCRAM 規格規定密碼也要使用 UTF-8，並以 *SASLprep* 演算法處理。然而，PostgreSQL 並不要求密碼使用 UTF-8。設定使用者的密碼時，無論實際使用的編碼為何，都會把它當成 UTF-8 以 SASLprep 處理。不過，如果它不是合法的 UTF-8 位元組序列，或者包含 SASLprep 演算法所禁止的 UTF-8 位元組序列，就會直接使用原始密碼而不經 SASLprep 處理，而不是擲出錯誤。這讓密碼在使用 UTF-8 時可以被正規化，但仍允許使用非 UTF-8 的密碼，而且不需要系統知道密碼使用的是哪一種編碼。

具備 SSL 支援的 PostgreSQL 建置版本支援*通道綁定*（channel binding）。具備通道綁定之 SCRAM 的 SASL 機制名稱為 `SCRAM-SHA-256-PLUS`。PostgreSQL 使用的通道綁定類型為 `tls-server-end-point`。

在不具通道綁定的 SCRAM 中，伺服器會選擇一個隨機數並傳送給用戶端，用來與使用者提供的密碼混合成所傳送的密碼雜湊。雖然這可以防止密碼雜湊在之後的工作階段中被成功重送，卻無法防止位於真正伺服器與用戶端之間的假伺服器轉送伺服器的隨機值並成功通過身分驗證。

具備通道綁定的 SCRAM 會把伺服器憑證的簽章混入所傳送的密碼雜湊中，藉此防止這類中間人攻擊。雖然假伺服器可以重送真正伺服器的憑證，但它無法存取與該憑證相符的私鑰，因此無法證明自己是擁有者，進而導致 SSL 連線失敗。

<a id="id-1.10.6.8.5.8"></a>

**範例**

<a id="SCRAM-BEGIN"></a>1. 伺服器送出 AuthenticationSASL 訊息。其中包含伺服器可以接受的 SASL 身分驗證機制清單。如果伺服器建置時具備 SSL 支援，清單會是 `SCRAM-SHA-256-PLUS` 與 `SCRAM-SHA-256`，否則只有後者。
<a id="SCRAM-CLIENT-FIRST"></a>2. 用戶端以送出 SASLInitialResponse 訊息作為回應，該訊息指出所選的機制：`SCRAM-SHA-256` 或 `SCRAM-SHA-256-PLUS`。（用戶端可以自由選擇任一機制，但為了更好的安全性，如果它能支援，就應該選擇具通道綁定的變體。）在初始用戶端回應（Initial Client response）欄位中，該訊息包含 SCRAM `client-first-message`。`client-first-message` 也包含用戶端所選的通道綁定類型。
<a id="SCRAM-SERVER-FIRST"></a>3. 伺服器送出 AuthenticationSASLContinue 訊息，內容為 SCRAM `server-first-message`。
<a id="SCRAM-CLIENT-FINAL"></a>4. 用戶端送出 SASLResponse 訊息，內容為 SCRAM `client-final-message`。
<a id="SCRAM-SERVER-FINAL"></a>5. 伺服器送出 AuthenticationSASLFinal 訊息，內含 SCRAM `server-final-message`，並緊接著送出 AuthenticationOk 訊息。

<a id="SASL-OAUTHBEARER"></a>

### 54.3.2. OAUTHBEARER 身分驗證 [#](#sasl-oauthbearer) <a href="#sasl-oauthbearer" id="sasl-oauthbearer"></a>

`OAUTHBEARER` 是一種用於聯合身分驗證（federated authentication）、以權杖為基礎的機制。[RFC 7628](https://datatracker.ietf.org/doc/html/rfc7628) 中有詳細說明。

典型的交換過程，會依用戶端是否已為目前使用者快取了持有人權杖（bearer token）而有所不同。如果沒有，交換會透過兩個連線進行：第一個是「探索」（discovery）連線，用來從伺服器取得 OAuth 中繼資料；第二個連線則在用戶端取得權杖後用來送出權杖。（libpq 目前並未在其內建流程中實作快取方法，因此它使用雙連線交換。）

此機制與 SCRAM 一樣，由用戶端發起。用戶端初始回應由 SCRAM 所使用的標準「GS2」標頭組成，後面接著一串 `key=value` 配對。伺服器目前唯一支援的鍵是 `auth`，其中包含持有人權杖。`OAUTHBEARER` 另外還規定了用戶端初始回應的三個選用組成部分（GS2 標頭的 `authzid`，以及 `host` 與 `port` 鍵），伺服器目前會忽略它們。

`OAUTHBEARER` 不支援通道綁定，也沒有「OAUTHBEARER-PLUS」機制。此機制在身分驗證成功時不使用伺服器資料，因此交換過程中不會使用 AuthenticationSASLFinal 訊息。

<a id="id-1.10.6.8.6.6"></a>

**範例**

1. 在第一次交換期間，伺服器送出 AuthenticationSASL 訊息，其中宣告了 `OAUTHBEARER` 機制。
2. 用戶端以送出指出 `OAUTHBEARER` 機制的 SASLInitialResponse 訊息作為回應。假設用戶端尚未擁有目前使用者的有效持有人權杖，則 `auth` 欄位為空，表示這是一個探索連線。
3. 伺服器送出 AuthenticationSASLContinue 訊息，其中包含錯誤 `status`，以及用戶端進行 OAuth 流程時應該使用的公認 URI（well-known URI）與範圍（scope）。
4. 用戶端送出包含空集合（單一 `0x01` 位元組）的 SASLResponse 訊息，以完成它在探索交換中的那一半。
5. 伺服器送出 ErrorMessage，使第一次交換失敗。

   此時，用戶端會進行眾多可能的 OAuth 流程之一來取得持有人權杖，除了伺服器提供的中繼資料之外，也會使用它本身已設定的任何中繼資料。（此處的描述刻意保持模糊；`OAUTHBEARER` 並未規定或強制要求任何特定的權杖取得方法。）

   取得權杖之後，用戶端會重新連線到伺服器，進行最後的交換：
6. 伺服器再次送出 AuthenticationSASL 訊息，其中宣告了 `OAUTHBEARER` 機制。
7. 用戶端以送出 SASLInitialResponse 訊息作為回應，但這一次訊息中的 `auth` 欄位包含在用戶端流程中取得的持有人權杖。
8. 伺服器依照權杖提供者的指示驗證權杖。如果用戶端獲得連線授權，伺服器會送出 AuthenticationOk 訊息以結束 SASL 交換。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sasl-authentication.html)（原文版本：18.6；核對日期：2026-10-12）
