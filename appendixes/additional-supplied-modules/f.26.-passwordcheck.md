# F.26. passwordcheck

每當使用 [CREATE ROLE](../../reference/sql-commands/create-role.md) 或 [ALTER ROLE](../../reference/sql-commands/alter-role.md) 設定使用者密碼時，passwordcheck 模組都會檢查使用者的密碼。 如果密碼強度被認為太弱，它將被拒絕，命令將因錯誤而終止。

要啟用此模組，請將 “$libdir/passwordcheck” 加到 postgresql.conf 中的 [shared\_preload\_libraries](../../server-administration/server-configuration/client-connection-defaults.md#shared\_preload\_libraries-string)，然後重新啟動伺服器。

您可以透過修改原始碼來使此模組更符合您的需求。 例如，您可以使用 [CrackLib](https://github.com/cracklib/cracklib) 檢查密碼——這只需要在 Makefile 中取消註釋兩行並重新編譯模組。 （由於授權許可因素，我們不能預先包含 CrackLib。）如果沒有 CrackLib，該模組會強制執行一些簡單的密碼強度規則，您可以根據需要修改或延伸這些規則。

{% hint style="info" %}
注意\
為了防止未加密的密碼透過網路發送、寫入伺服器日誌或被資料庫管理員以其他方式竊取，PostgreSQL 允許使用者提供預先加密的密碼。 許多用戶端程式利用此功能並在將密碼發送到伺服器之前對其進行加密。

這限制了 passwordcheck 模組的用途，因為在那種情況下它只能嘗試猜測密碼。 因此，如果您的安全要求很高，則不建議使用 passwordcheck。 使用外部驗證方法如 GSSAPI（參見第 21 章）比依賴資料庫內的密碼反而更為安全。

或者，您可以修改 passwordcheck 以拒絕預先加密的密碼，但強制使用者以明碼形式設定密碼會帶來自身的安全風險。
{% endhint %}

