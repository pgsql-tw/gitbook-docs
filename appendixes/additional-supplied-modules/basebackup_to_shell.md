<a id="BASEBACKUP-TO-SHELL"></a>

# F.5. basebackup_to_shell

[F.5.1. Configuration Parameters](#id-1.11.7.14.5)

[F.5.2. Author](#id-1.11.7.14.6)

<a id="id-1.11.7.14.2"></a>

`basebackup_to_shell` 新增名為 `shell` 的自訂基礎備份目標。這使得你可以執行 `pg_basebackup --target=shell`；或者依本模組的設定執行 <code class="command">pg&#95;basebackup --target=shell:<em class="replaceable"><code>DETAIL&#95;STRING</code></em></code>，讓伺服器管理者選定的伺服器端指令針對備份程序產生的每個 tar 封存檔執行。該指令會從標準輸入接收封存檔內容。

本模組主要用來示範如何透過延伸模組建立新的備份目標，但在某些情境下也可直接使用。若要運作，必須透過 [shared_preload_libraries](../../server-administration/server-configuration/client-connection-defaults.md#GUC-SHARED-PRELOAD-LIBRARIES) 或 [local_preload_libraries](../../server-administration/server-configuration/client-connection-defaults.md#GUC-LOCAL-PRELOAD-LIBRARIES) 載入此模組。

<a id="id-1.11.7.14.5"></a>

## F.5.1. Configuration Parameters

`basebackup_to_shell.command` (`string`) <a id="id-1.11.7.14.5.2.1.1.3"></a>

伺服器應針對備份程序產生的每個封存檔執行的指令。指令字串中的 `%f` 會替換為封存檔名稱，例如 `base.tar`。`%d` 會替換為使用者提供的目標詳細資訊。若指令字串使用 `%d`，就必須提供目標詳細資訊；否則禁止提供。基於安全考量，目標詳細資訊只能含英數字元。指令字串中的 `%%` 會替換為單一 `%`。若 `%` 後接其他字元，或位於字串末尾，會發生錯誤。

`basebackup_to_shell.required_role` (`string`) <a id="id-1.11.7.14.5.2.2.1.3"></a>

使用 `shell` 備份目標所需的角色。若未設定，任何複寫使用者都可使用 `shell` 備份目標。

<a id="id-1.11.7.14.6"></a>

## F.5.2. Author

Robert Haas <code class="email">&lt;<a class="email" href="mailto:rhaas@postgresql.org">rhaas@postgresql.org</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/basebackup-to-shell.html)
