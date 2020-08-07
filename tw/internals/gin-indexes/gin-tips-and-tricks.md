# 66.5. GIN Tips and Tricks

Create vs. insert

由於可能為每個項目插入了許多索引鍵，因此插入 GIN 索引可能會很慢。因此，對於批次插入表格，建議在完成批次插入後刪除 GIN 索引並重新建立。

從 PostgreSQL 8.4 開始，由於使用了延遲索引，因此此建議不太必要（詳見[第 64.4.1 節](implementation.md#64-4-1-gin-kuai-su-geng-xin-ji)）。但對於非常大的更新，還是最好刪除並重新建立索引。

[maintenance\_work\_mem](../../server-administration/server-configuration/resource-consumption.md#19-4-1-memory)

GIN 索引的建構時間對 maintenance\_work\_mem 設定非常敏感；在建立索引期間，不需要花費工作記憶體。

[gin\_pending\_list\_limit](../../server-administration/server-configuration/client-connection-defaults.md#19-11-2-xi-ge-shi)

在一系列插入已啟用 fastupdate 的現有 GIN 索引期間，只要列表大於 gin\_pending\_list\_limit，系統就會清理待處理項目列表。為了避免觀察的回應時間波動，希望在背景進行待處理列表清理（即透過 autovacuum）。透過增加 gin\_pending\_list\_limit 或使 autovacuum 更積極，可以減少手動清理操作。但是，擴大清理操作的閾值意味著如果確實發生了手動清理，則需要更長時間。

可以透過變更儲存參數來覆蓋各個 GIN 索引的 gin\_pending\_list\_limit，並允許每個 GIN 索引具有自己的清理閾值。例如，可以僅為可以大量更新的 GIN 索引增加閾值，否則可以減少閾值。

[gin\_fuzzy\_search\_limit](../../server-administration/server-configuration/client-connection-defaults.md#19-11-4-qi-ta-ding-ji-qi-zhi)

開發 GIN 索引的主要目標是在 PostgreSQL 中建立對可高度延展的全文檢索支援，並且通常情況下全文檢索會回傳非常大的結果集合。然而，當查詢包含非常頻繁的單詞時，通常會發生這種情況，因此大型結果集甚至不起作用。由於從磁碟讀取許多 tuple 並對它們進行排序可能需要花費大量時間，因此這對於產品環境來說是不可接受的。（請注意，索引搜尋本身非常快。）

為了便於控制執行此類查詢，GIN 對回傳的資料列數量有一個可配置的軟性上限：gin\_fuzzy\_search\_limit 配置參數。預設設定為 0（表示無限制）。如果設定了非零的限制，則回傳的集合是整個結果集合的子集，隨機選擇。

「軟性上限」表示回傳結果的實際數量可能與指定的限制略有不同，具體取決於查詢和系統隨機數産生器的情況。

從經驗來看，數千以上的值（例如 5000 - 20000）是比較好的範圍。

