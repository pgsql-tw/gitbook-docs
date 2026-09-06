# F.2. amcheck

amcheck 模塊提供的功能是讓你可以驗證關連結構邏輯的一致性。如果該結構看起來有效，就不會引發任何錯誤。

這些函式會驗證特定關聯表示結構中的各種*不變量*。索引掃描及其他重要作業所使用的存取方法函式是否正確，取決於這些不變量始終成立。例如，某些函式會驗證所有 B-Tree 頁面中的項目是否依「邏輯」順序排列（例如，`text` 的 B-Tree 索引中，索引資料列應依排序規則的字典順序排列）。若此不變量因故不成立，受影響頁面上的二元搜尋便可能錯誤引導索引掃描，導致 SQL 查詢傳回錯誤結果。

驗證採用與索引掃描本身相同的程序，其中可能包含使用者定義的運算子類別程式碼。例如，B-Tree 索引驗證仰賴一或多個 B-Tree 支援函式 1 例程進行比較。運算子類別支援函式的詳細資訊請參閱[第 37.16.3 節](../../server-programming/extending-sql/interfacing-extensions-to-indexes.md#XINDEX-SUPPORT)。

只有超級使用者可以使用 `amcheck` 函式。

## F.2.1. 函式

`bt_index_check(index regclass, heapallindexed boolean) returns void`

`bt_index_check` 測試其目標 B-Tree 索引是否符合多項不變量。使用範例：

```
test=# SELECT bt_index_check(index => c.oid, heapallindexed => i.indisunique),
               c.relname,
               c.relpages
FROM pg_index i
JOIN pg_opclass op ON i.indclass[0] = op.oid
JOIN pg_am am ON op.opcmethod = am.oid
JOIN pg_class c ON i.indexrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE am.amname = 'btree' AND n.nspname = 'pg_catalog'
-- Don't check temp tables, which may be from another session:
AND c.relpersistence != 't'
-- Function may throw an error when this is omitted:
AND c.relkind = 'i' AND i.indisready AND i.indisvalid
ORDER BY c.relpages DESC LIMIT 10;
 bt_index_check |             relname             | relpages 
----------------+---------------------------------+----------
                | pg_depend_reference_index       |       43
                | pg_depend_depender_index        |       40
                | pg_proc_proname_args_nsp_index  |       31
                | pg_description_o_c_o_index      |       21
                | pg_attribute_relid_attnam_index |       14
                | pg_proc_oid_index               |       10
                | pg_attribute_relid_attnum_index |        9
                | pg_amproc_fam_proc_index        |        5
                | pg_amop_opr_fam_index           |        5
                | pg_amop_fam_strat_index         |        5
(10 rows)
```

此範例顯示一個工作階段，驗證資料庫「test」中最大的 10 個系統目錄索引。對其中屬於唯一值索引的子集，要求驗證堆積資料列是否存在相應的索引資料列。由於未引發錯誤，所有受測索引看起來都具有邏輯一致性。當然，您可以輕易修改此查詢，對資料庫中所有支援驗證的索引呼叫 `bt_index_check`。

`bt_index_check` 會在目標索引及其所屬的堆積關聯上取得 `AccessShareLock`。這個鎖定模式與簡單 `SELECT` 陳述式在關聯上取得的模式相同。`bt_index_check` 不驗證跨越子項／父項關係的不變量；但當 _`heapallindexed`_ 為 `true` 時，會驗證索引中是否存在所有堆積資料列所對應的索引資料列。在運作中的正式環境需要例行且輕量的毀損測試時，使用 `bt_index_check` 通常能在驗證完整性與降低對應用程式效能及可用性的影響之間取得最佳折衷。

`bt_index_parent_check(index regclass, heapallindexed boolean, rootdescend boolean) returns void`

`bt_index_parent_check` 測試其目標 B-Tree 索引是否符合多項不變量。可選地，當 _`heapallindexed`_ 參數為 `true` 時，函式會驗證所有應存在於索引中的堆積資料列是否存在。當可選的 _`rootdescend`_ 參數為 `true` 時，驗證會針對每個資料列從根頁面重新搜尋，以重新找出葉節點層級的資料列。`bt_index_parent_check` 可以執行的檢查，是 `bt_index_check` 可執行檢查的超集。`bt_index_parent_check` 可視為更徹底的 `bt_index_check` 變體：它與 `bt_index_check` 不同，還會檢查跨越父項／子項關係的不變量，包括確認索引結構中沒有遺漏的下行連結。`bt_index_parent_check` 遵循一般慣例，發現邏輯不一致或其他問題時會引發錯誤。

`bt_index_parent_check` 要求在目標索引上取得 `ShareLock`（也會在堆積關聯上取得 `ShareLock`）。這些鎖會阻止 `INSERT`、`UPDATE` 及 `DELETE` 命令並行修改資料，也會阻止 `VACUUM` 及所有其他公用程式命令並行處理底層關聯。請注意，此函式只在執行期間持有鎖，而不是整個交易期間。

`bt_index_parent_check` 的額外驗證更可能偵測到各種異常情況。這些情況可能涉及受檢索引所使用、實作錯誤的 B-Tree 運算子類別，或是假設性的底層 B-Tree 索引存取方法程式碼未發現錯誤。請注意，`bt_index_parent_check` 與 `bt_index_check` 不同，無法在啟用 Hot Standby 模式時（亦即唯讀實體複本上）使用。

#### 提示

`bt_index_check` 與 `bt_index_parent_check` 都會以 `DEBUG1` 及 `DEBUG2` 嚴重性層級輸出關於驗證程序的日誌訊息。這些訊息提供驗證程序的詳細資訊，PostgreSQL 開發人員可能會感興趣。進階使用者也可能發現這些資訊有用，因為驗證實際偵測到不一致時，它能提供額外的上下文。在互動式 psql 工作階段中執行驗證查詢前執行：

```
SET client_min_messages = DEBUG1;
```

即可顯示驗證進度的訊息，詳細程度仍便於閱讀。

## F.2.2. 可選的 _`heapallindexed`_ 驗證

驗證函式的 _`heapallindexed`_ 參數為 `true` 時，會對與目標索引關聯相關的資料表執行額外的驗證階段。此階段由一次「虛擬」的 `CREATE INDEX` 作業組成，並依據暫存的記憶體內摘要結構，檢查所有假設的新索引資料列是否存在（此結構會在基本的第一個驗證階段中視需要建立）。摘要結構會為目標索引中找到的每個資料列建立「指紋」。_`heapallindexed`_ 驗證的高層原則是：與現有目標索引等價的新索引，所含項目必須都能在現有結構中找到。

額外的 _`heapallindexed`_ 階段會帶來大量額外負荷：驗證通常需要數倍的時間。不過，執行 _`heapallindexed`_ 驗證時所取得的關聯層級鎖並不會改變。

摘要結構的大小受 `maintenance_work_mem` 限制。為確保對每個應在索引中表示的堆積資料列，未能偵測到不一致的機率不超過 2%，每個資料列約需要 2 位元組的記憶體。每個資料列可用的記憶體越少，遺漏不一致的機率便會緩慢增加。此方法可大幅限制驗證負荷，同時只略微降低偵測問題的機率，尤其適合將驗證視為例行維護工作的安裝環境。每次新的驗證嘗試，都會再次有機會偵測到任何單一遺漏或格式錯誤的資料列。

## F.2.3. 有效使用 `amcheck`

`amcheck` 能有效偵測[資料頁面檢查碼](../../reference/server-applications/initdb.md#APP-INITDB-DATA-CHECKSUMS)必然無法捕捉的各類故障模式，其中包括：

*   運算子類別實作錯誤造成的結構不一致。

    這包括作業系統排序規則變更所造成的問題。像 `text` 這類可排序型別之資料值的比較必須是不可變的（如同所有用於 B-Tree 索引掃描的比較都必須不可變），這表示作業系統的排序規則絕不能變更。雖然罕見，作業系統排序規則的更新可能造成此類問題。更常見的是主要伺服器與待命伺服器之間的排序順序不一致，可能是所使用的作業系統*主要*版本不一致所致。這類不一致通常只會出現在待命伺服器上，因此通常也只能在待命伺服器上偵測到。

    發生此類問題時，不一定會影響使用受影響排序規則的每個個別索引，因為不論行為不一致與否，*已建立索引的*值可能剛好具有相同的絕對順序。關於 PostgreSQL 如何使用作業系統地區設定與排序規則的詳細資訊，請參閱[第 23.1 節](../../server-administration/localization/locale-support.md)與[第 23.2 節](../../server-administration/localization/collation-support.md)。
*   索引與已建立索引的堆積關聯之間的結構不一致（執行 _`heapallindexed`_ 驗證時）。

    正常作業期間不會將索引與其堆積關聯交叉檢查。堆積毀損的徵兆可能相當不明顯。
*   底層 PostgreSQL 存取方法程式碼、排序程式碼或交易管理程式碼中假設性未發現錯誤所造成的毀損。

    自動驗證索引的結構完整性，在測試可能引入邏輯不一致的新 PostgreSQL 功能或提議功能時扮演角色。驗證資料表結構及相關的可見性與交易狀態資訊也扮演類似角色。明顯的測試策略之一，是在執行標準迴歸測試時持續呼叫 `amcheck` 函式。執行測試的詳細資訊請參閱[第 32.1 節](../../server-administration/regression-tests/32.1.-running-the-tests.md)。
*   恰好未啟用檢查碼的檔案系統或儲存子系統故障。

    請注意，若存取區塊時只有共用緩衝區命中，`amcheck` 會檢查驗證當下該頁面在某個共用記憶體緩衝區中的表示。因此，`amcheck` 不一定會檢查驗證當下從檔案系統讀取的資料。啟用檢查碼時，若將毀損區塊讀入緩衝區，`amcheck` 可能因檢查碼失敗而引發錯誤。
*   故障 RAM 或更廣泛的記憶體子系統所造成的毀損。

    PostgreSQL 不防護可校正的記憶體錯誤，且假設您會使用採用業界標準錯誤校正碼（ECC）或更佳保護機制的 RAM 運作。然而，ECC 記憶體通常只對單位元錯誤免疫，不應假設它能對造成記憶體毀損的故障提供*絕對*保護。

    執行 _`heapallindexed`_ 驗證時，由於會測試嚴格的二進位相等性及堆積內已建立索引的屬性，通常大幅提高偵測單位元錯誤的機會。

一般而言，`amcheck` 只能證明毀損存在，無法證明毀損不存在。

## F.2.4. 修復毀損

`amcheck` 引發的任何毀損相關錯誤都不應是誤判。`amcheck` 只會在依定義不應發生的情況下引發錯誤，因此通常需要仔細分析 `amcheck` 錯誤。

沒有可修復 `amcheck` 所偵測問題的通用方法。應找出違反不變量的根本原因之說明。[pageinspect](pageinspect.md) 可能有助於診斷 `amcheck` 偵測到的毀損。`REINDEX` 不一定能有效修復毀損。
