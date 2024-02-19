# 31.10. 系統設定

邏輯複寫需要設定幾個系統組態選項。

在發佈端，必須將 wal\_level 設定為 logical，並且必須將 max\_replication\_slots 設定為至少預計要連線的訂閱數量，並為資料表同步保留一些預留數量。然後 max\_wal\_senders 應至少設定為與 max\_replication\_slots 相同的數量再加上同時連線的實體副本數量。

用戶還需要設定 max\_replication\_slots。在這種情況下，它應至少設定為將加到訂閱伺服器的訂閱數。max\_logical\_replication\_workers 必須至少設定為訂閱數量，再加上資料表同步的一些保留數。此外，可能需要調整 max\_worker\_processes 以滿足複寫程序，至少為（max\_logical\_replication\_workers + 1）。請注意，某些延伸功能和平行查詢也需要 max\_worker\_processes 中的程序插槽。
