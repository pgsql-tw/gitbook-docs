# 48. Logical Decoding

PostgreSQL 提供了將 SQL 執行的資料變更串流傳輸到外部資料庫的基礎結構。此功能可用於多種目的，包括了複寫解決方案和稽核需求。

變更會以邏輯複寫插槽的串流形式發送出去。

串流傳輸這些變更的格式由所使用的輸出模組決定。PostgreSQL 發行版中提供了一個範例模組。可以撰寫其他模組來擴展可用的格式，而毋須修改任何核心程式。每個輸出模組都可以存取 INSERT 所產生的每個新資料列以及 UPDATE 所建立的新資料列版本。UPDATE 和 DELETE 舊資料列版本的可用性取決於其所設定的副本識別（請參閱 [REPLICA IDENTITY](../../reference/sql-commands/alter-table.md#replica-identity)）。

可以使用串流複寫協定（請參閱[第 52.4 節](../../internals/52.-frontend-backend-protocol/streaming-replication-protocol.md)和[第 48.3 節](streaming-replication-protocol-interface.md)）或透過 SQL 呼叫函數（請參閱[第 48.4 節](logical-decoding-sql-interface.md)）來使用資料變更的內容。也可以撰寫其他方法來處理複寫插槽的輸出，而毋須修改核心程式（請參閱[第 48.7 節](logical-decoding-output-writers.md)）。
