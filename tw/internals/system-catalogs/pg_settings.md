# 52.85. pg\_settings

檢視表 pg\_settings 提供對伺服器的執行時參數的存取。它本質上是 [SHOW](../../reference/sql-commands/show.md) 和 [SET ](../../reference/sql-commands/set.md)指令的替代介面。它也提供 SHOW 無法直接獲得的一些資訊存取，例如最小值和最大值。

#### **Table 52.86. `pg_settings` Columns**

| 名稱 | 型別 | 說明 |
| :--- | :--- | :--- |
| `name` | `text` | 執行階段的組態參數名稱 |
| `setting` | `text` | 參數的現值 |
| `unit` | `text` | 參數隱含的單位 |
| `category` | `text` | 參數的邏輯分類 |
| `short_desc` | `text` | 參數的簡要說明 |
| `extra_desc` | `text` | 附加的，更詳細的參數說明 |
| `context` | `text` | 組態參數值的必要內容（詳見下文） |
| `vartype` | `text` | 參數型別（bool、enum、integer、real 或 string） |
| `source` | `text` | 目前參數值的來源 |
| `min_val` | `text` | 參數的最小允許值（非數字型別為 null） |
| `max_val` | `text` | 參數的最大允許值（非數字型別為 null） |
| `enumvals` | `text[]` | 列舉參數的允許值（非列舉型別為 null） |
| `boot_val` | `text` | 如果未另行設定參數，則在伺服器啟動時預先給予參數值 |
| `reset_val` | `text` | RESET 將參數重置為目前連線中的值 |
| `sourcefile` | `text` | 組態檔案目前設定為何（對於從組態檔案以外來源設定的值，或者由非超級使用者也不是 pg\_read\_all\_settings 的成員所給予，為null）；在組態檔案中使用 include 指令時會很有幫助 |
| `sourceline` | `integer` | 組態檔案中目前設定所在的行號（對於從組態檔案以外來源所設定的值，或者由非超級使用者，也不是 pg\_read\_all\_settings 成員所給予的值，則為 null）。 |
| `pending_restart` | `boolean` | 如果組態檔案中的值已更改但需要重新啟動，則為 true；否則為 false。 |

設定內容有幾種可能的值，是為了降低變更組態的複雜度，它們是：

`internal`

這些設定無法直接更改；它們反映了內部所決定的值，其中一些可以透過使用不同的組態選項重建伺服器，或透過更改提供給 initdb 的選項來調整。

`postmaster`

這些設定只能在伺服器啟動時套用，因此任何變更都需要重新啟動伺服器。這些設定的值通常儲存在 postgresql.conf 檔案中，或在啟動伺服器時在命令列中給予。當然，也可以在伺服器啟動時設定任何層級較低的設定。

`sighup`

可以在 postgresql.conf 中對這些設定進行變更，而毌須重新啟動伺服器。只要向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf 並套用變更。postmaster 還會將 SIGHUP 信號轉發給其子程序，以便它們都獲取新值。

`superuser-backend`

可以在 postgresql.conf 中對這些設定進行變更，而毌須重新啟動伺服器。它們也可以在連線要求的封包中設定為特別連線（例如，透過 libpq 的 PGOPTIONS 環境變數），但前提是連線使用者是超級使用者。但是，這些設定在啟動後的連線中永遠不會變更。如果你在 postgresql.conf 中更改它們，請向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf。新值只會影響隨後啟動的連線。

`backend`

可以在 postgresql.conf 中對這些設定進行變更，而毌須重新啟動伺服器。它們也可以在連線請求封包中設定為特別連線（例如，透過 libpq 的 PGOPTIONS 環境變數）；任何使用者都可以為他們的連線進行這樣的變更。但是，這些設定在啟動後的連線中永遠無法變更。如果你在 postgresql.conf 中更改它們，請向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf。新值只會影響隨後啟動的連線。

`superuser`

這些設定可以從 postgresql.conf 設定，也可以透過 SET 指令在連線中設定；但只有超級使用者可以透過 SET 來更改。僅當沒有使用 SET 建立連線專用的值時，postgresql.conf 中的變更才會影響現有連線。

`user`

這些設定可以從 postgresql.conf 設定，也可以透過 SET 指令在連線中設定。允許任何使用者變更其連線中所使用的值。僅當未使用 SET 未建立連線專用值時，postgresql.conf 中的變更才會影響現有連線。

有關變更這些參數的各種方法和更多資訊，請參閱[第 19.1 節](../../server-administration/server-configuration/19.1.-setting-parameters.md)。

pg\_settings 檢視表無法INSERT 或 DELETE，但可以 UPDATE。套用於一行 pg\_settings 的 UPDATE 相當於對該參數執行 [SET](../../reference/sql-commands/set.md) 指令。此變更僅影響目前連線所使用的值。如果在稍後中止的交易事務中發出 UPDATE，則在回溯事務時 UPDATE 指令的效果會消失。一旦提交了相關的事務，則效果將持續到連線結束，除非被另一個 UPDATE 或 SET 覆蓋。

