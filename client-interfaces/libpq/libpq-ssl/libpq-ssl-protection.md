# 32.19.3. 不同模式所提供的保護

<a id="LIBPQ-SSL-PROTECTION"></a>

## 32.19.3. 不同模式所提供的保護 [#](#libpq-ssl-protection) <a href="#libpq-ssl-protection" id="libpq-ssl-protection"></a>

`sslmode` 參數的不同值會提供不同
層級的保護。SSL 可以
針對三種攻擊提供保護：

竊聽（Eavesdropping）

若第三方能夠檢視用戶端與伺服器之間的網路流量，
它就能讀取連線資訊（包括
使用者名稱與密碼）以及所傳遞的資料。SSL
使用加密來防止這種情況。

中間人攻擊（Man-in-the-middle，MITM）

若第三方能夠在資料於用戶端與伺服器之間傳遞時修改資料，
它就能假冒伺服器，因而能看到並
修改資料，*即使資料已經加密*。接著，第三方可以
將連線資訊與資料轉送到原本的伺服器，
使這種攻擊無從察覺。達成這種攻擊的常見途徑
包括 DNS 下毒（DNS poisoning）與位址劫持，使用戶端被導向
非預期的另一台伺服器。另外也有其他幾種
攻擊方法可以達成這種攻擊。SSL 使用憑證
驗證來防止這種情況，方法是向用戶端驗證伺服器的身分。

冒充（Impersonation）

若第三方能夠假冒經授權的用戶端，它就能
直接存取原本不應有權存取的資料。這通常
是由不安全的密碼管理所造成。SSL 使用
用戶端憑證來防止這種情況，方法是確保只有持有
有效憑證者才能存取伺服器。

若要讓一個連線確定受到 SSL 保護，必須在建立連線之前，
於*用戶端與伺服器雙方*都設定使用 SSL。
若只在伺服器上設定，用戶端可能會在
得知伺服器要求高度安全性之前，就送出敏感資訊（例如密碼）。
在 libpq 中，可以藉由
將 `sslmode` 參數設定為 `verify-full` 或
`verify-ca`，並向系統提供用來驗證的根憑證，
來確保連線是安全的。這類似於使用 `https`
URL 進行加密的網頁瀏覽。

伺服器的身分經過驗證之後，用戶端就可以傳送敏感資料。
這表示在此之前，用戶端不需要知道是否
會使用憑證進行驗證，因此只在伺服器設定中指定這一點是安全的。

所有 SSL 選項都會帶來加密與
金鑰交換的額外負擔，因此必須在效能
與安全性之間做出取捨。[表 32.1](#libpq-ssl-sslmode-statements)
說明了不同 `sslmode` 值
所防範的風險，以及它們對安全性與額外負擔所代表的陳述。

<a id="LIBPQ-SSL-SSLMODE-STATEMENTS"></a>

### 表 32.1. SSL 模式說明 [#](#libpq-ssl-sslmode-statements) <a href="#libpq-ssl-sslmode-statements" id="libpq-ssl-sslmode-statements"></a>

<table border="1" class="table" summary="表 32.1. SSL 模式說明"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th><code class="literal">sslmode</code></th><th>防範竊聽</th><th>防範 <acronym class="acronym">MITM</acronym></th><th>陳述</th></tr></thead><tbody><tr><td><code class="literal">disable</code></td><td>否</td><td>否</td><td>我不在乎安全性，也不想付出加密的
       額外負擔。
      </td></tr><tr><td><code class="literal">allow</code></td><td>可能</td><td>否</td><td>我不在乎安全性，但若伺服器堅持，
       我願意付出加密的額外負擔。
      </td></tr><tr><td><code class="literal">prefer</code></td><td>可能</td><td>否</td><td>我不在乎加密，但若伺服器支援，
       我希望付出加密的額外負擔。
      </td></tr><tr><td><code class="literal">require</code></td><td>是</td><td>否</td><td>我希望資料經過加密，並接受額外負擔。我相信
       網路會確保我始終連線到我想要的伺服器。
      </td></tr><tr><td><code class="literal">verify-ca</code></td><td>是</td><td>取決於 CA 政策</td><td>我希望資料經過加密，並接受額外負擔。我想要
       確定我連線到的是我信任的伺服器。
      </td></tr><tr><td><code class="literal">verify-full</code></td><td>是</td><td>是</td><td>我希望資料經過加密，並接受額外負擔。我想要
        確定我連線到的是我信任的伺服器，而且就是我
        所指定的那一台。
       </td></tr></tbody></table>

<br>

`verify-ca` 與 `verify-full` 之間的差異
取決於根 CA 的政策。若使用的是公開的
CA，`verify-ca` 會允許連線到
*其他人*可能已向該 CA 註冊的伺服器。
在這種情況下，應該一律使用 `verify-full`。若
使用的是本機 CA，甚至是自我簽署的憑證，使用
`verify-ca` 通常就能提供足夠的保護。

`sslmode` 的預設值是 `prefer`。如
表中所示，從安全性的角度來看，這個設定沒有意義，它只
承諾在可能時帶來效能上的額外負擔。它之所以作為預設值，
只是為了向後相容性，不建議用於安全的部署環境。

[返回 32.19. SSL 支援](../libpq-ssl.md#libpq-ssl)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-ssl.html)（原文版本：18.6；核對日期：2026-10-17）
