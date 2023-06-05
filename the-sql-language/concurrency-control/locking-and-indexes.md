# 13.7. 鎖定與索引

儘管 PostgreSQL 提供了對資料庫表的 non-blocking 讀寫存取，但目前並沒有為 PostgreSQL 中的每種索引方法提供 non-blocking 的讀寫存取方法。各種索引類型的處理如下：

#### B-tree, GiST and SP-GiST indexes

短期共享或獨占 page-level 鎖定用於讀寫存取。在讀取或插入每個索引資料列後會立即釋放鎖定。這些索引類型提供最高的平行處理的一致性，不會有 deadlock 的情況。

#### Hash indexes

共享或獨占 hash-bucket-level 鎖定用於讀寫存取。處理完整個 bucket 後釋放鎖定。 Bucket-level 鎖定比索引層級的鎖定提供更好的平行作業能力，但由於鎖定的持有時間會超過一個索引操作，因此可能會出現 deadlock。

#### GIN indexes

短期共享或獨占 page-level 鎖定於讀寫存取。 在讀取或插入每個索引資料列後會立即釋放鎖定。 但請注意，插入 GIN 索引值通常會在每筆資料中產生多個索引鍵的插入，也就是說 GIN 可能會為單個值的插入產生大量的作業負載。

目前來說，B-tree 索引為平行的多連線應用程式提供最佳性能； 由於它們還具有比 Hash 索引更多的功能，因此對於需要索引基礎資料一致性應用程式的推薦索引類型。但在處理非基礎資料型別時，B-tree 並無法產生作用，應該改用 GiST、SP-GiST 或 GIN 索引。
