## F.4. `basebackup_to_shell` — 「shell」`pg_basebackup` 模組範例 [#](#BASEBACKUP-TO-SHELL)

[F.4.1. 設定參數](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)

[F.4.2. 作者](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-AUTHOR)

<a id="id-1.11.7.14.2"></a>

`basebackup_to_shell` 新增名為 `shell` 的自訂基礎備份目標。這讓你可以執行 `pg_basebackup --target=shell`，或依此模組的設定執行 `pg_basebackup --target=shell:DETAIL_STRING`，使伺服器管理者選擇的伺服器命令針對備份程序產生的每個 tar 封存檔執行。該命令會透過標準輸入接收封存檔內容。

此模組主要是示範如何透過擴充功能模組建立新的備份目標，但在某些情況下本身也可能有用。此模組必須透過 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 或 [local_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-LOCAL-PRELOAD-LIBRARIES) 載入，才能運作。

<a id="BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS"></a>

### F.4.1. 設定參數 [#](#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)

`basebackup_to_shell.command` (`string`) <a id="id-1.11.7.14.5.2.1.1.3"></a>
:   伺服器應針對備份程序產生的每個封存檔執行的命令。若命令字串中出現 `%f`，會以封存檔名稱（例如 `base.tar`）取代。若命令字串中出現 `%d`，會以使用者提供的目標詳細資料取代。命令字串使用 `%d` 時必須提供目標詳細資料，否則禁止提供。基於安全性原因，目標詳細資料只能包含英數字元。若命令字串中出現 `%%`，會以單一 `%` 取代。若命令字串中的 `%` 後接其他任何字元，或位於字串末尾，便會發生錯誤。

`basebackup_to_shell.required_role` (`string`) <a id="id-1.11.7.14.5.2.2.1.3"></a>
:   使用 `shell` 備份目標所需的角色。若未設定，任何複寫使用者都可使用 `shell` 備份目標。

<a id="BASEBACKUP-TO-SHELL-AUTHOR"></a>

### F.4.2. 作者 [#](#BASEBACKUP-TO-SHELL-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/basebackup-to-shell.html)（原文版本：18.6；核對日期：2026-09-06）
