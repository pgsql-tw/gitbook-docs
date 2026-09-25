<a id="SSPI-AUTH"></a>

## 20.7. SSPI 驗證 [#](#SSPI-AUTH)

<a id="id-1.6.7.14.2"></a>

SSPI 是 Windows 的一項技術，可提供具備單一登入（single sign-on）功能的
安全驗證機制。PostgreSQL 會以
`negotiate` 模式使用 SSPI，這個模式會盡可能使用
Kerberos，在其他情況下則自動退回使用 NTLM。
SSPI 與 GSSAPI 可以互通，
彼此作為用戶端與伺服器使用，例如：
SSPI 用戶端可以向
GSSAPI 伺服器進行驗證。建議在 Windows
用戶端與伺服器上使用 SSPI，
在非 Windows 平台上則使用 GSSAPI。

在使用 Kerberos 驗證時，
SSPI 的運作方式與
GSSAPI 相同；詳見[20.6 節](gssapi-auth.md)。

SSPI 支援下列設定選項：

`include_realm`
:   若設為 0，則在通過使用者名稱對應
    （[20.2 節](auth-username-maps.md)）之前，會先移除
    已驗證使用者主體中的領域（realm）名稱。這種做法並不建議，
    主要是為了向下相容才保留，因為除非同時使用
    `krb_realm`，否則在多領域環境中並不安全。
    建議將 `include_realm` 保持在預設值（1），
    並在 `pg_ident.conf` 中提供明確的對應，
    將主體名稱轉換為 PostgreSQL 使用者名稱。

`compat_realm`
:   若設為 1，則 `include_realm` 選項會使用該
    網域相容於 SAM 的名稱（也就是 NetBIOS 名稱）。
    這是預設值。若設為 0，則會使用來自 Kerberos
    使用者主體名稱的真實領域名稱。

    除非你的伺服器是在網域帳號下執行（這也包括網域成員系統上的
    虛擬服務帳號），且所有透過 SSPI 進行驗證的用戶端也都使用
    網域帳號，否則請不要停用這個選項，不然驗證會失敗。

`upn_username`
:   若這個選項與 `compat_realm` 一併啟用，
    驗證時會使用來自 Kerberos UPN 的使用者名稱。
    若停用（預設值），則會使用相容於 SAM 的使用者名稱。
    對新建立的使用者帳號而言，這兩個名稱預設是相同的。

    請注意，如果沒有明確指定使用者名稱，libpq
    會使用相容於 SAM 的名稱。如果你使用
    libpq 或以它為基礎的驅動程式，
    應該將這個選項保持停用，或是在連線字串中
    明確指定使用者名稱。

`map`
:   允許在系統使用者名稱與資料庫使用者名稱之間建立對應。
    詳見[20.2 節](auth-username-maps.md)。對於像
    `username@EXAMPLE.COM`（或較少見的
    `username/hostbased@EXAMPLE.COM`）這樣的
    SSPI/Kerberos 主體，用於對應的使用者名稱會是
    `username@EXAMPLE.COM`（或分別為
    `username/hostbased@EXAMPLE.COM`），
    除非 `include_realm` 已設為 0，在這種情況下，
    `username`（或 `username/hostbased`）
    就會被視為對應時所看到的系統使用者名稱。

`krb_realm`
:   設定用來比對使用者主體名稱的領域。若設定了這個參數，
    則只有該領域的使用者會被接受。若未設定，則任何領域的
    使用者都可以連線，但仍須遵循所執行的使用者名稱對應規則。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sspi-auth.html)（原文版本：18.6；核對日期：2026-09-25）
