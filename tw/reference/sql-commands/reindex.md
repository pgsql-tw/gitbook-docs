# REINDEX

REINDEX — 重建索引

## 語法

```text
REINDEX [ ( VERBOSE ) ] { INDEX | TABLE | SCHEMA | DATABASE | SYSTEM } name
```

## 說明

REINDEX 使用索引資料表中所儲存的資料重建索引，替換索引舊的版本。有幾種情況可以使用 REINDEX：

* 索引損壞，不再包含有效的資料。雖然理論上這種情況永遠不會發生，但實際上索引會因程式錯誤或硬體故障而損壞。REINDEX 提供了一種恢復的方法。
* 索引變得「臃腫」，即它包含許多空或幾乎空的頁面。在某些不常見的存取模式下，PostgreSQL 中 的 B-tree 索引會發生這種情況。REINDEX 提供了一種透過寫入無死頁的索引新版本來減少索引空間消耗的方法。有關更多訊息，請參閱[第 24.2 節](../../server-administration/routine-database-maintenance-tasks/routine-reindexing.md)。
* 您變更了索引的儲存參數（例如 fillfactor），並希望確保變更能完全生效。
* 使用 CONCURRENTLY 選項的索引建構失敗，留下「無效」的索引。 這些索引沒用，但使用 REINDEX 重建它們會很方便。請注意，REINDEX 將不執行同步建構。要在不干擾線上查詢的情況下建構索引，您應該刪除索引並重新發出 CREATE INDEX CONCURRENTLY 指令。

## 參數

`INDEX`

重新建立指定的索引。

`TABLE`

重新建立指定資料表的所有索引。如果資料表具有額外的「TOAST」資料表，那麼也會重新編制索引。

`SCHEMA`

重新建立指定綱要的所有索引。如果此綱要的資料表具有額外的「TOAST」資料表，那麼也會重新編制索引。還會處理共享系統目錄上的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

`DATABASE`

重新建立目前資料庫中的所有索引。還會處理共享系統目錄上的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

`SYSTEM`

重新建立目前資料庫中系統目錄的所有索引。包含共享系統目錄的索引。但不處理使用者資料表的索引。這種形式的 REINDEX 不能在交易事務區塊中執行。

_`name`_

要重新編制索引的特定索引，資料表或資料庫的名稱。索引和資料表名稱可以是加上綱要名稱的。目前，REINDEX DATABASE 和 REINDEX SYSTEM 只能重新索引目前資料庫，因此它們的參數必須符合目前資料庫的名稱。

`CONCURRENTLY`

使用此選項時，PostgreSQL 將重建索引而不會採取任何防止在資料表上進行同時的插入、更新或刪除的鎖定； 而標準索引重建會鎖定資料表上的寫入（但不會影響讀取），直到完成。使用此選項時需要注意一些注意事項—請參閱[同步重建索引](reindex.md#tong-bu-zhong-jian-suo-yin)。

對於臨時資料表，REINDEX 都是以非平行同步\(non-concurrent\)的方式處理，因為其他任何連線都無法存取它們，更何況非平行同步的重新索引的成本更為便宜。

`VERBOSE`

在重新索引每個索引時輸出進度報告。

## 注意

如果您懷疑使用者資料表上的索引損壞，您可以使用 REINDEX INDEX 或 REINDEX TABLE 簡單地重建該索引或資料表上的所有索引。

如果您需要從系統資料表上的索引損壞中恢復，則事情會比較困難。在這種情況下，系統沒有使用到任何可疑索引很重要。（實際上，在這種情況下，由於依賴於損壞的索引，您可能會發現伺服器程序在啟動時立即終止。）要安全恢復，必須使用 -P 選項啟動伺服器，這樣可以防止伺服器程序使用索引進行系統目錄查詢。

一種方法是關閉伺服器並啟動單一使用者模式的 PostgreSQL 伺服器，其命令列中包含 -P 選項。然後，可以發出 REINDEX DATABASE，REINDEX SYSTEM，REINDEX TABLE 或 REINDEX INDEX，具體取決於您需要重建的程度。如有疑問，請使用 REINDEX SYSTEM 選擇資料庫中所有系統索引的重建。然後退出單一使用者模式伺服器連線再重新啟動一般模式伺服器。有關如何與單一使用者模式伺服器界面交互的更多訊息，請參閱 [postgres](../server-applications/postgres.md) 參考頁面。

或者，可以在其命令列選項中包含 -P 的情況下啟動一般模式的伺服器連線。執行此操作的方法因用戶端而異，但在所有基於 libpq 的客戶端中，可以在啟動用戶端之前將 PGOPTIONS 環境變數設定為 -P。請注意，雖然此方法不需要鎖定其他用戶端，但在修復完成之前阻止其他用戶連線到損壞的資料庫仍然是明智之舉。

REINDEX 類似於索引的刪除和重新建立，因為索引內容是從頭開始建立的。但是，鎖定考慮情況是相當不同的。REINDEX 鎖定寫入但不讀取索引的父資料表。它還對正在處理的特定索引進行獨占鎖定，這將阻止嘗試使用該索引的讀取。相反，DROP INDEX 會暫時對父資料表進行獨占鎖定，從而阻止寫入和讀取。隨後的 CREATE INDEX 鎖定寫入但不讀取；由於索引不在那裡，沒有讀取會嘗試使用它，這意味著沒有阻塞但是讀取可能會被強制進入昂貴的循序掃描。

重新索引單個索引或資料表需要成為該索引或資料表的擁有者。重新索引資料庫需要成為資料庫的擁有者（請注意，擁有者因此可以重建其他使用者擁有的資料表索引）。當然，超級使用者總是可以重新索引任何東西。

Reindexing partitioned tables or partitioned indexes is not supported. Each individual partition can be reindexed separately instead.

### 同步重建索引

重建索引可能會干擾資料庫的一般操作。通常來說，PostgreSQL 會鎖定針對寫入操作重建索引的資料表，並透過對資料表的全表掃描來執行整個索引建構。其他交易事務仍然可以讀取資料表，但是如果它們嘗試在資料表中插入，更新或刪除資料，則它們將被暫時阻擋直到索引重建完成。如果系統是線上的正式資料庫，則可能會產生嚴重影響。非常大的資料表可能需要花費數小時才能建立索引，即使對於較小的表，索引重建也可能會將寫入者鎖定在線上系統無法接受的時間之內。

PostgreSQL 支援以最小的寫入鎖定來重建索引。透過指定 REINDEX 的 CONCURRENTLY 選項來使用此方法。使用此選項時，PostgreSQL 必須對每個需要重建的索引執行兩次資料表掃描，並等待終止所有可能使用該索引的現有交易事務。與標準索引重建相比，此方法總共需要更多的工作量，並且由於需要等待可能會修改索引的未完成交易事務而需要更長的時間才能完成。但是，由於它允許重建索引時繼續正常操作，因此此方法對於在生產環境中重建索引很有用。當然，索引重建帶來的額外 CPU，記憶體和 I/O 負載也可能會減慢其他操作的速度。

在同步重建索引的過程中，將以下列步驟實行。 每個步驟都在單獨的交易事務中運行。如果重建多個索引，則每個步驟都會循環遍歷所有索引，然後再進行下一步。

1. A new temporary index definition is added to the catalog `pg_index`. This definition will be used to replace the old index. A `SHARE UPDATE EXCLUSIVE` lock at session level is taken on the indexes being reindexed as well as their associated tables to prevent any schema modification while processing.
2. A first pass to build the index is done for each new index. Once the index is built, its flag `pg_index.indisready` is switched to “true” to make it ready for inserts, making it visible to other sessions once the transaction that performed the build is finished. This step is done in a separate transaction for each index.
3. Then a second pass is performed to add tuples that were added while the first pass was running. This step is also done in a separate transaction for each index.
4. All the constraints that refer to the index are changed to refer to the new index definition, and the names of the indexes are changed. At this point, `pg_index.indisvalid` is switched to “true” for the new index and to “false” for the old, and a cache invalidation is done causing all sessions that referenced the old index to be invalidated.
5. The old indexes have `pg_index.indisready` switched to “false” to prevent any new tuple insertions, after waiting for running queries that might reference the old index to complete.
6. The old indexes are dropped. The `SHARE UPDATE EXCLUSIVE` session locks for the indexes and the table are released.

如果在重建索引時出現問題，例如唯一索引中的唯一性衝突，則 REINDEX 命令將失敗，但除現有索引外，還會留下「INVALID」的新索引。該索引出於查詢目的將被忽略，因為它可能不完整。但是它將仍然消耗更新資料的開銷。`psql \d` 命令將回報諸如 INVALID 的索引：

```text
postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Modifiers
--------+---------+-----------
 col    | integer |
Indexes:
    "idx" btree (col)
    "idx_ccnew" btree (col) INVALID
```

在這種情況下，建議的恢復方法是刪除無效索引，然後再次嘗試執行REINDEX CONCURRENTLY。在處理期間建立的同步索引的名稱會以 ccnew 結尾，如果它是舊索引定義而我們未能刪除，則以 ccold 結尾。 可以使用 DROP INDEX 刪除無效的索引，包括無效的 TOAST 索引。

一般索引建立允許在同一資料表上同時進行其他一般索引的建立，但是一次只能在一個資料表上進行一個同步索引建構。而在以上這兩種情況下，都不允許同時在資料表上進行其他類型的架構修改。另一個區別是，可以在交易事務內執行一般的 REINDEX TABLE 或 REINDEX INDEX 指令，但 REINDEX CONCURRENTLY 則無法執行。

REINDEX SYSTEM 不支援 CONCURRENTLY，因為不能同時為系統目錄重新建立索引。

此外，排除限制條件的索引不能同步重新索引。如果在此命令中直接命名了這樣的索引，則會引發錯誤。如果同時對具有排除限制條件索引的資料表或資料庫重新建立索引，則將跳過這些索引。 （可以在沒有 CONCURRENTLY 選項的情況下重新索引此類索引。）

## 範例

重建單個索引：

```text
REINDEX INDEX my_index;
```

重建資料表 my\_table 上的所有索引：

```text
REINDEX TABLE my_table;
```

重建特定資料庫中的所有索引，而不管系統索引是否有效：

```text
$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

重建資料表的索引，而在進行重建索引的過程中，不會阻止任何相關物件的讀寫操作：

```text
REINDEX TABLE CONCURRENTLY my_broken_table;
```

## 相容性

SQL 標準中沒有 REINDEX 指令。

