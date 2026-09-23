<a id="GSSAPI-ENC"></a>

## 18.10. 使用 GSSAPI 加密的安全 TCP/IP 連線 [#](#GSSAPI-ENC)

[18.10.1. 基本設定](gssapi-enc.md#GSSAPI-SETUP)

<a id="id-1.6.5.13.2"></a>

PostgreSQL 也原生支援使用 GSSAPI，
為用戶端與伺服器之間的通訊加密，以提升安全性。
此支援要求用戶端與伺服器系統上，都必須安裝
GSSAPI 實作（例如 MIT Kerberos），
並且必須在建置時，啟用 PostgreSQL 中對此的支援
（請參閱[第 17 章](../installation/README.md)）。

<a id="GSSAPI-SETUP"></a>

### 18.10.1. 基本設定 [#](#GSSAPI-SETUP)

PostgreSQL 伺服器，會在同一個 TCP 連接埠上，
同時聆聽一般連線與 GSSAPI 加密連線，
並會與任何連線中的用戶端，協商是否要使用 GSSAPI
進行加密（以及驗證）。依預設，這項決定
由用戶端決定（這也意味著，攻擊者可能將其降級）；
關於如何設定伺服器，讓部分或所有連線，
都要求使用 GSSAPI，請參閱
[20.1 節](../client-authentication/auth-pg-hba-conf.md)。

在使用 GSSAPI 進行加密時，通常也會一併使用 GSSAPI
進行驗證，因為底層機制，無論如何都會（依據 GSSAPI 實作）
決定用戶端與伺服器的身分。不過，這並非必要條件；
您也可以選擇另一種 PostgreSQL 驗證方式，
來執行額外的驗證。

除了協商行為的設定之外，GSSAPI 加密，
不需要任何超出 GSSAPI 驗證所需設定的額外設定。
（關於相關設定的更多資訊，
請參閱[20.6 節](../client-authentication/gssapi-auth.md)。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gssapi-enc.html)（原文版本：18.6；核對日期：2026-09-22）
