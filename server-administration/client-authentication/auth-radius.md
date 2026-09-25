<a id="AUTH-RADIUS"></a>

## 20.11. RADIUS 驗證 [#](#AUTH-RADIUS)

<a id="id-1.6.7.18.2"></a>

這個驗證方法的運作方式與 `password` 類似，差別在於它使用
RADIUS 作為密碼驗證方法。RADIUS 只用來驗證使用者
名稱／密碼配對，因此使用者必須已經
存在於資料庫中，才能使用 RADIUS 進行驗證。

使用 RADIUS 驗證時，系統會向已設定的 RADIUS 伺服器傳送一則 Access Request
訊息。這則請求的類型為
`Authenticate Only`，並包含
`user name`、`password`（已加密）與
`NAS Identifier` 等參數。這則請求會以
與伺服器共享的密鑰加密。RADIUS 伺服器會以 `Access Accept` 或
`Access Reject` 回應這則請求。不支援 RADIUS 的記帳（accounting）功能。

可以指定多個 RADIUS 伺服器，此時系統會依序嘗試這些伺服器。若
從某個伺服器收到否定回應，驗證就會失敗。若沒有收到回應，
則會嘗試清單中的下一個伺服器。要指定多個伺服器，請以逗號分隔各伺服器名稱，
並用雙引號將整份清單括起來。若指定了多個伺服器，其他的
RADIUS 選項也可以用逗號分隔的清單形式提供，為每個伺服器
分別指定個別的值；也可以只指定單一值，此時該值會套用到所有伺服器。

以下是 RADIUS 支援的設定選項：

`radiusservers`
:   要連線的 RADIUS 伺服器的 DNS 名稱或 IP 位址。這個參數為必填。

`radiussecrets`
:   與 RADIUS 伺服器進行安全通訊時所使用的共享密鑰。這個值在
    PostgreSQL 與 RADIUS 伺服器上必須完全相同。建議使用長度至少 16 個字元
    的字串。這個參數為必填。

    ### 注意

    只有在 PostgreSQL 是以支援
    OpenSSL 的方式建置時，所使用的加密向量才具有密碼學上的強度。在其他
    情況下，傳送到 RADIUS 伺服器的內容應被視為只是經過混淆，而非真正安全，
    若有需要，應另外採取外部安全措施。

`radiusports`
:   要連線的 RADIUS 伺服器連接埠號碼。若未指定連接埠，
    則會使用預設的 RADIUS 連接埠（`1812`）。

`radiusidentifiers`
:   在 RADIUS 請求中作為 `NAS Identifier` 使用的字串。這個參數
    可以用來，舉例來說，識別使用者正嘗試連線的是哪一個資料庫叢集，這在
    RADIUS 伺服器上進行政策比對時會很有用。若未指定識別碼，則會使用
    預設值 `postgresql`。

若某個 RADIUS 參數值中需要包含逗號或空白字元，可以用雙引號將該值括起來，但
這會有點麻煩，因為現在需要兩層雙引號。以下是在 RADIUS 密鑰字串中加入空白字元的
範例：

```

host ... radius radiusservers="server1,server2" radiussecrets="""secret one"",""secret two"""
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-radius.html)（原文版本：18.6；核對日期：2026-09-26）
