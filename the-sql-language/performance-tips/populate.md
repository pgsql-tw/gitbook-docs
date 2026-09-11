<a id="POPULATE"></a>

## 14.4. 填入資料庫 [#](#POPULATE)

[14.4.1. 停用自動提交](populate.md#DISABLE-AUTOCOMMIT)

[14.4.2. 使用 `COPY`](populate.md#POPULATE-COPY-FROM)

[14.4.3. 移除索引](populate.md#POPULATE-RM-INDEXES)

[14.4.4. 移除外鍵限制條件](populate.md#POPULATE-RM-FKEYS)

[14.4.5. 增加 `maintenance_work_mem`](populate.md#POPULATE-WORK-MEM)

[14.4.6. 增加 `max_wal_size`](populate.md#POPULATE-MAX-WAL-SIZE)

[14.4.7. 停用 WAL 封存與串流複寫](populate.md#POPULATE-PITR)

[14.4.8. 事後執行 `ANALYZE`](populate.md#POPULATE-ANALYZE)

[14.4.9. 關於 pg_dump 的一些說明](populate.md#POPULATE-PG-DUMP)

初次填入資料庫時，可能需要插入大量資料。本節提供一些建議，說明如何讓這個過程盡可能有效率。

<a id="DISABLE-AUTOCOMMIT"></a>

### 14.4.1. 停用自動提交 [#](#DISABLE-AUTOCOMMIT)

<a id="id-1.5.13.7.3.2"></a>

使用多個 `INSERT` 時，請關閉自動提交，只在最後進行一次提交。（在一般 SQL 中，這表示在開頭發出 `BEGIN`，並在結尾發出 `COMMIT`。有些用戶端函式庫可能會在背後替你這麼做，在這種情況下，你需要確認函式庫會在你希望的時機這麼做。）如果你讓每一次插入都分別提交，PostgreSQL 就要為每一筆新增的資料列做很多工作。在單一交易中完成所有插入還有一個額外的好處：如果某一筆資料列插入失敗，那麼到那時為止已插入的所有資料列都會被回復，因此你不會卡在只載入了一部分資料的狀態。

<a id="POPULATE-COPY-FROM"></a>

### 14.4.2. 使用 `COPY` [#](#POPULATE-COPY-FROM)

請使用 [`COPY`](../../reference/sql-commands/sql-copy.md) 以單一命令載入所有資料列，而不要使用一連串的 `INSERT` 命令。`COPY` 命令針對載入大量資料列做了最佳化；它不如 `INSERT` 靈活，但在大量載入資料時，額外負擔明顯少得多。由於 `COPY` 是單一命令，如果你使用這種方法填入資料表，就不需要停用自動提交。

如果你無法使用 `COPY`，使用 [`PREPARE`](../../reference/sql-commands/sql-prepare.md) 建立一個預備好的 `INSERT` 陳述式，然後依需要多次使用 `EXECUTE`，可能會有所幫助。這可以避免重複剖析與規劃 `INSERT` 的部分額外負擔。不同的介面以不同的方式提供這項功能；請在介面的說明文件中尋找「預備陳述式」（prepared statements）。

請注意，即使使用了 `PREPARE`，並將多次插入批次處理在單一交易中，使用 `COPY` 載入大量資料列幾乎總是比使用 `INSERT` 快。

當 `COPY` 與先前的 `CREATE TABLE` 或 `TRUNCATE` 命令在同一個交易中使用時，速度最快。在這種情況下不需要寫入任何 WAL，因為萬一發生錯誤，包含新載入資料的檔案無論如何都會被移除。不過，這項考量只在 [wal_level](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL) 為 `minimal` 時才適用，因為在其他情況下，所有命令都必須寫入 WAL。

<a id="POPULATE-RM-INDEXES"></a>

### 14.4.3. 移除索引 [#](#POPULATE-RM-INDEXES)

如果你要載入的是新建立的資料表，最快的方法是先建立資料表，使用 `COPY` 大量載入該資料表的資料，然後再為該資料表建立所需的索引。在既有資料上建立索引，比在載入每一筆資料列時逐步更新索引來得快。

如果你要將大量資料加入現有的資料表中，先刪除索引、載入資料表，然後再重新建立索引，可能會比較划算。當然，在索引不存在的這段期間，其他使用者的資料庫效能可能會受到影響。刪除唯一索引之前也應該三思，因為在索引不存在期間，唯一限制條件所提供的錯誤檢查也會失效。

<a id="POPULATE-RM-FKEYS"></a>

### 14.4.4. 移除外鍵限制條件 [#](#POPULATE-RM-FKEYS)

就像索引一樣，「整批」檢查外鍵限制條件，會比逐筆資料列檢查更有效率。因此，先刪除外鍵限制條件、載入資料，再重新建立限制條件，可能會很有用。同樣地，這需要在資料載入速度與限制條件不存在期間失去錯誤檢查之間取捨。

此外，當你將資料載入到已有外鍵限制條件的資料表時，每一筆新資料列都需要在伺服器的待處理觸發程序事件清單中占用一個項目（因為檢查資料列之外鍵限制條件的，正是觸發程序的觸發）。載入數百萬筆資料列可能會使觸發程序事件佇列超出可用記憶體，導致無法忍受的置換，甚至讓命令直接失敗。因此，在載入大量資料時，刪除並重新套用外鍵可能是*必要的*，而不只是比較理想而已。如果無法接受暫時移除限制條件，那麼唯一的替代辦法可能就是將載入操作拆分成較小的交易。

<a id="POPULATE-WORK-MEM"></a>

### 14.4.5. 增加 `maintenance_work_mem` [#](#POPULATE-WORK-MEM)

在載入大量資料時暫時增加組態變數 [maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM)，可以提升效能。這有助於加快 `CREATE INDEX` 命令與 `ALTER TABLE ADD FOREIGN KEY` 命令。它對 `COPY` 本身並沒有太大幫助，因此這項建議只在你使用上述其中一種或兩種技巧時才有用。

<a id="POPULATE-MAX-WAL-SIZE"></a>

### 14.4.6. 增加 `max_wal_size` [#](#POPULATE-MAX-WAL-SIZE)

暫時增加組態變數 [max_wal_size](../../server-administration/runtime-config/runtime-config-wal.md#GUC-MAX-WAL-SIZE)，也可以讓大量資料的載入更快。這是因為將大量資料載入 PostgreSQL，會使檢查點比正常的檢查點頻率（由組態變數 `checkpoint_timeout` 指定）更頻繁地發生。每當發生檢查點時，所有髒頁都必須排清到磁碟。在大量載入資料期間暫時增加 `max_wal_size`，就可以減少所需的檢查點數量。

<a id="POPULATE-PITR"></a>

### 14.4.7. 停用 WAL 封存與串流複寫 [#](#POPULATE-PITR)

將大量資料載入到使用 WAL 封存或串流複寫的系統時，在載入完成之後建立新的基礎備份，可能會比處理大量的增量 WAL 資料更快。為了避免在載入期間記錄增量 WAL，請停用封存與串流複寫，方法是將 [wal_level](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL) 設為 `minimal`、將 [archive_mode](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-MODE) 設為 `off`，並將 [max_wal_senders](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS) 設為零。但請注意，變更這些設定需要重新啟動伺服器，而且會使先前建立的所有基礎備份都無法用於封存復原與備援伺服器，這可能導致資料遺失。

除了省下封存程序或 WAL 傳送程序處理 WAL 資料的時間之外，這麼做實際上還會讓某些命令更快，因為如果 `wal_level` 為 `minimal`，而且目前的子交易（或最上層交易）建立或截斷了這些命令所變更的資料表或索引，它們就完全不需要寫入 WAL。（它們可以在最後執行一次 `fsync`，以比寫入 WAL 更低的成本保證當機安全性。）

<a id="POPULATE-ANALYZE"></a>

### 14.4.8. 事後執行 `ANALYZE` [#](#POPULATE-ANALYZE)

每當你大幅改變了資料表中的資料分布時，強烈建議執行 [`ANALYZE`](../../reference/sql-commands/sql-analyze.md)。這包括將大量資料批次載入資料表的情況。執行 `ANALYZE`（或 `VACUUM ANALYZE`）可以確保規劃器擁有關於該資料表的最新統計資訊。如果沒有統計資訊或統計資訊已經過時，規劃器在規劃查詢時可能會做出不好的決策，導致任何統計資訊不準確或不存在的資料表效能不佳。請注意，如果啟用了 autovacuum 常駐程式，它可能會自動執行 `ANALYZE`；更多資訊請參閱[第 24.1.3 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-STATISTICS)與[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)。

<a id="POPULATE-PG-DUMP"></a>

### 14.4.9. 關於 pg_dump 的一些說明 [#](#POPULATE-PG-DUMP)

pg_dump 產生的傾印指令碼會自動套用上述準則中的幾項，但不是全部。要盡可能快速地還原 pg_dump 的傾印，你需要手動做一些額外的事情。（請注意，這些要點適用於*還原*傾印時，而不是*建立*傾印時。無論是使用 psql 載入文字格式的傾印，還是使用 pg_restore 從 pg_dump 封存檔載入，都適用相同的要點。）

預設情況下，pg_dump 會使用 `COPY`，而且在產生完整的綱要與資料傾印時，它會小心地先載入資料，再建立索引與外鍵。因此在這種情況下，有幾項準則會自動處理。剩下需要你做的是：

* 為 `maintenance_work_mem` 與 `max_wal_size` 設定適當的值（也就是比平常更大的值）。
* 如果使用 WAL 封存或串流複寫，請考慮在還原期間停用它們。要這麼做，請在載入傾印之前，將 `archive_mode` 設為 `off`、將 `wal_level` 設為 `minimal`，並將 `max_wal_senders` 設為零。之後，再將它們設回正確的值，並建立新的基礎備份。
* 實驗 pg_dump 與 pg_restore 的平行傾印與還原模式，找出最佳的並行工作數量。藉由 `-j` 選項平行傾印與還原，應該能獲得比序列模式明顯更高的效能。
* 考慮是否應將整個傾印作為單一交易還原。要這麼做，請將 `-1` 或 `--single-transaction` 命令列選項傳給 psql 或 pg_restore。使用這個模式時，即使是最小的錯誤也會回復整個還原作業，可能會捨棄好幾個小時的處理成果。視資料之間的關聯程度而定，這可能比手動清理更可取，也可能不是。如果你使用單一交易並關閉 WAL 封存，`COPY` 命令會執行得最快。
* 如果資料庫伺服器上有多顆 CPU 可用，請考慮使用 pg_restore 的 `--jobs` 選項。這可以讓資料載入與索引建立並行進行。
* 事後執行 `ANALYZE`。

只含資料的傾印仍然會使用 `COPY`，但它不會刪除或重新建立索引，而且通常也不會處理外鍵。[<a id="id-1.5.13.7.11.4.2"></a>[14]](#ftn.id-1.5.13.7.11.4.2) 因此，載入只含資料的傾印時，如果你想使用這些技巧，就要自行刪除並重新建立索引與外鍵。在載入資料時增加 `max_wal_size` 仍然有用，但不必增加 `maintenance_work_mem`；你應該在事後手動重新建立索引與外鍵時再這麼做。完成之後，別忘了執行 `ANALYZE`；更多資訊請參閱[第 24.1.3 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-STATISTICS)與[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)。

<br>

---

<a id="ftn.id-1.5.13.7.11.4.2"></a>

[[14]](#id-1.5.13.7.11.4.2) 
你可以使用 `--disable-triggers` 選項來達到停用外鍵的效果——但要了解，這會取消外鍵驗證，而不只是延後驗證，因此如果使用它，就有可能插入不良的資料。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/populate.html)（原文版本：18.6；核對日期：2026-09-11）
