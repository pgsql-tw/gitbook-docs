<a id="AUTH-PAM"></a>

## 20.13. PAM 驗證 [#](#AUTH-PAM)

<a id="id-1.6.7.20.2"></a>

這種驗證方法的運作方式與
`password` 類似，差別在於它使用 PAM（Pluggable
Authentication Modules，可插拔驗證模組）作為驗證機制。
預設的 PAM 服務名稱為 `postgresql`。
PAM 只用來驗證使用者名稱／密碼組合，並可選擇性地驗證
所連線的遠端主機名稱或 IP 位址。因此，使用者必須已經
存在於資料庫中，才能使用 PAM 進行驗證。關於 PAM 的更多
資訊，請閱讀
[Linux-PAM 頁面](https://www.kernel.org/pub/linux/libs/pam/)。

PAM 支援下列設定選項：

`pamservice`
:   PAM 服務名稱。

`pam_use_hostname`
:   決定透過 `PAM_RHOST` 項目提供給 PAM 模組的是遠端 IP 位址
    還是主機名稱。預設使用 IP 位址。將此選項設為 1，即可改用
    解析後的主機名稱。主機名稱解析可能導致登入延遲。（大多數
    PAM 設定不會使用這項資訊，因此只有在某個 PAM 設定是特地為了
    使用這項資訊而建立時，才需要考慮這項設定。）

<a id="AUTH-PAM-NOTE"></a>

### 注意

如果 PAM 設定為讀取 `/etc/shadow`，驗證將會失敗，
因為 PostgreSQL 伺服器是由非 root 使用者啟動的。
不過，當 PAM 設定為使用 LDAP 或其他驗證方法時，
就不會有這個問題。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-pam.html)（原文版本：18.6；核對日期：2026-10-10）
