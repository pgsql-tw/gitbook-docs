<a id="RUNTIME-CONFIG-LOCKS"></a>

## 19.12. 鎖定管理 [#](#RUNTIME-CONFIG-LOCKS)

<a id="GUC-DEADLOCK-TIMEOUT"></a>

`deadlock_timeout` (`integer`) <a id="id-1.6.6.15.2.1.1.3"></a> <a id="id-1.6.6.15.2.1.1.4"></a> <a id="id-1.6.6.15.2.1.1.5"></a> [#](#GUC-DEADLOCK-TIMEOUT)
:   這是在等待鎖定時、於檢查是否發生死結狀況之前
    所等待的時間量。檢查死結的成本相對較高，
    因此伺服器不會每次等待鎖定時都進行檢查。我們樂觀地
    假設死結在正式環境應用程式中並不常見，
    因此會先等待鎖定一段時間，再檢查
    死結。增加此值可減少不必要死結檢查所浪費的時間，
    但會拖慢真正死結錯誤的回報速度。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為一秒（`1s`），
    這大概是實務上你會想要使用的最小值。
    在負載較重的伺服器上，你可能會想要提高此值。
    理想情況下，此設定值應超過你典型的交易時間，
    以提高在等待者決定檢查死結之前鎖定已被釋放的機率。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    當 [log_lock_waits](runtime-config-logging.md#GUC-LOG-LOCK-WAITS) 設定時，
    此參數也決定了在發出關於鎖定等待的日誌訊息之前
    所等待的時間量。如果你正在調查鎖定延遲問題，
    可能會想將 `deadlock_timeout` 設得比一般情況短。
<a id="GUC-MAX-LOCKS-PER-TRANSACTION"></a>

`max_locks_per_transaction` (`integer`) <a id="id-1.6.6.15.2.2.1.3"></a> [#](#GUC-MAX-LOCKS-PER-TRANSACTION)
:   共享鎖定表為每個伺服器程序或已備妥交易（prepared transaction）
    提供 `max_locks_per_transaction` 個物件
    （例如資料表）的空間；因此，同一時間最多只能鎖定這麼多個
    不同的物件。此參數限制的是每個交易所使用的物件鎖定
    平均數量；只要所有交易的鎖定總數
    能放入鎖定表，個別交易就可以鎖定更多物件。這*並非*
    可鎖定的資料列數量；該數值不受限制。預設值
    64，經過實務證明一直以來都已足夠，但如果你有在單一交易中
    涉及許多不同資料表的查詢（例如查詢有許多子資料表的父資料表），
    可能需要提高此值。此參數只能在伺服器啟動時設定。

    在執行 standby 伺服器時，你必須將此參數設為與 primary
    伺服器相同或更高的值，否則在 standby 伺服器中
    將不允許執行查詢。
<a id="GUC-MAX-PRED-LOCKS-PER-TRANSACTION"></a>

`max_pred_locks_per_transaction` (`integer`) <a id="id-1.6.6.15.2.3.1.3"></a> [#](#GUC-MAX-PRED-LOCKS-PER-TRANSACTION)
:   共享謂詞鎖定表為每個伺服器程序或已備妥交易
    提供 `max_pred_locks_per_transaction` 個物件
    （例如資料表）的空間；因此，同一時間最多只能鎖定這麼多個
    不同的物件。此參數限制的是每個交易所使用的物件鎖定
    平均數量；只要所有交易的鎖定總數
    能放入鎖定表，個別交易就可以鎖定更多物件。這*並非*
    可鎖定的資料列數量；該數值不受限制。預設值
    64，經過實務證明一直以來都已足夠，但如果你有用戶端在單一可序列化
    交易中涉及許多不同資料表，可能需要提高此值。此參數
    只能在伺服器啟動時設定。
<a id="GUC-MAX-PRED-LOCKS-PER-RELATION"></a>

`max_pred_locks_per_relation` (`integer`) <a id="id-1.6.6.15.2.4.1.3"></a> [#](#GUC-MAX-PRED-LOCKS-PER-RELATION)
:   這控制單一關聯的多少頁面或資料列（tuple）可以被謂詞鎖定，
    超過此數量後鎖定就會被提升為涵蓋整個關聯。大於或等於零的值
    代表絕對上限，而負值則代表
    [max_pred_locks_per_transaction](runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-TRANSACTION) 除以
    此設定值絕對值的結果。預設值為 -2，這維持了
    先前版本 PostgreSQL 的行為。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-MAX-PRED-LOCKS-PER-PAGE"></a>

`max_pred_locks_per_page` (`integer`) <a id="id-1.6.6.15.2.5.1.3"></a> [#](#GUC-MAX-PRED-LOCKS-PER-PAGE)
:   這控制單一頁面上的多少資料列可以被謂詞鎖定，
    超過此數量後鎖定就會被提升為涵蓋整個頁面。預設值
    為 2。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-locks.html)（原文版本：18.6；核對日期：2026-09-24）
