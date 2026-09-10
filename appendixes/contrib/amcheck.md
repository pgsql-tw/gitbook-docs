## F.1. amcheck — 驗證資料表與索引一致性的工具 [#](#AMCHECK)

[F.1.1. 函式](amcheck.md#AMCHECK-FUNCTIONS)

[F.1.2. 選用的 *`heapallindexed`* 驗證](amcheck.md#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)

[F.1.3. 有效使用 `amcheck`](amcheck.md#AMCHECK-USING-AMCHECK-EFFECTIVELY)

[F.1.4. 修復毀損](amcheck.md#AMCHECK-REPAIRING-CORRUPTION)

<a id="id-1.11.7.11.2"></a>

`amcheck` 模組提供函式，讓你驗證關聯結構的邏輯一致性。

B-tree 檢查函式會驗證特定關聯表示法結構中的各種*不變量*。索引掃描與其他重要作業背後的存取方法函式正確性，依賴這些不變量始終成立。舉例來說，某些函式會驗證所有 B-tree 頁面中的項目都處於「邏輯」順序（例如，對 `text` 建立的 B-tree 索引，其索引 tuple 應依排序規則的字典順序排列）。若該不變量因故不成立，受影響頁面的二元搜尋可能會錯誤地引導索引掃描，導致 SQL 查詢傳回錯誤結果。若結構看起來有效，不會引發錯誤。執行這些檢查函式時，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog, pg_temp`。

驗證作業使用與索引掃描本身相同的程序，這些程序可能是使用者定義的運算子類別程式碼。舉例來說，B-tree 索引驗證依賴一個或多個 B-tree 支援函式 1 常式進行的比較。運算子類別支援函式的詳細資訊請參閱[第 36.16.3 節](../../server-programming/extend/xindex.md#XINDEX-SUPPORT)。

不同於透過引發錯誤來報告毀損的 B-tree 檢查函式，堆積檢查函式 `verify_heapam` 會檢查資料表，並嘗試傳回一個資料列集合，每個偵測到的毀損對應一列。即使如此，若 `verify_heapam` 依賴的機制本身已毀損，函式仍可能無法繼續，並改為引發錯誤。

可以將執行 `amcheck` 函式的權限授與非超級使用者，但在授與前應仔細考量資料安全與隱私問題。雖然這些函式產生的毀損報告著重於資料結構與發現的毀損性質，而非毀損資料內容，但取得函式執行權限的攻擊者，特別是也能誘發毀損者，仍可能從訊息中推測部分資料內容。

<a id="AMCHECK-FUNCTIONS"></a>

### F.1.1. 函式 [#](#AMCHECK-FUNCTIONS)

`bt_index_check(index regclass, heapallindexed boolean, checkunique boolean) returns void` <a id="id-1.11.7.11.8.2.1.1.2"></a>
:   `bt_index_check` 測試其目標 B-tree 索引是否遵守各種不變量。使用範例如下：

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

    此範例顯示一個工作階段，驗證資料庫「test」中最大的 10 個系統目錄索引。對其中的唯一值索引要求驗證堆積 tuple 是否存在為索引 tuple。由於沒有引發錯誤，所有測試的索引看起來在邏輯上都一致。當然，也可輕易修改此查詢，以便對資料庫內支援驗證的每個索引呼叫 `bt_index_check`。

    `bt_index_check` 會在目標索引及其所屬堆積關聯上取得 `AccessShareLock`。此鎖定模式與簡單 `SELECT` 陳述式在關聯上取得的鎖定模式相同。`bt_index_check` 不會驗證跨越子項／父項關係的不變量；但當 *`heapallindexed`* 為 `true` 時，會驗證所有堆積 tuple 都存在為索引中的索引 tuple。當 *`checkunique`* 為 `true` 時，`bt_index_check` 會檢查唯一值索引中的重複項目至多只有一個可見。在正式環境需要例行且輕量的毀損測試時，使用 `bt_index_check` 通常可在驗證完整性與降低對應用程式效能及可用性影響之間取得最佳平衡。

`bt_index_parent_check(index regclass, heapallindexed boolean, rootdescend boolean, checkunique boolean) returns void` <a id="id-1.11.7.11.8.2.2.1.2"></a>
:   `bt_index_parent_check` 測試其目標 B-tree 索引是否遵守各種不變量。選擇性地，當 *`heapallindexed`* 引數為 `true` 時，函式會驗證所有應存在於索引中的堆積 tuple。當 *`checkunique`* 為 `true` 時，`bt_index_parent_check` 會檢查唯一值索引中的重複項目至多只有一個可見。選用的 *`rootdescend`* 引數為 `true` 時，驗證會針對每個 tuple 自根頁面開始執行新搜尋，以重新找出葉層中的 tuple。`bt_index_parent_check` 可執行的檢查是 `bt_index_check` 可執行檢查的超集。可將 `bt_index_parent_check` 視為更完整的 `bt_index_check` 版本：它也檢查跨越父項／子項關係的不變量，包括確認索引結構中沒有遺漏的下行連結。若發現邏輯不一致或其他問題，`bt_index_parent_check` 會依一般慣例引發錯誤。

    `bt_index_parent_check` 需要在目標索引上取得 `ShareLock`（也會在堆積關聯上取得 `ShareLock`）。這些鎖定會阻止 `INSERT`、`UPDATE` 及 `DELETE` 指令的並行資料修改，也會阻止基礎關聯遭 `VACUUM` 與所有其他公用程式指令並行處理。請注意，函式只在執行期間持有鎖定，不會持有整個交易期間。

    `bt_index_parent_check` 的額外驗證更可能偵測各種病態情況。這些情況可能涉及被檢查索引所使用、實作不正確的 B-tree 運算子類別，或假設性地涉及基礎 B-tree 索引存取方法程式碼中尚未發現的錯誤。請注意，不同於 `bt_index_check`，啟用熱待命模式時（亦即唯讀實體複本上）無法使用 `bt_index_parent_check`。

`gin_index_check(index regclass) returns void` <a id="id-1.11.7.11.8.2.3.1.2"></a>
:   `gin_index_check` 測試目標 GIN 索引是否具有一致的父項／子項 tuple 關係（不需調整任何父項 tuple），以及頁面圖形是否遵守平衡樹不變量（內部頁面只參照葉頁或只參照內部頁面）。

### 提示

`bt_index_check` 與 `bt_index_parent_check` 都會以 `DEBUG1` 與 `DEBUG2` 嚴重性層級輸出驗證過程的日誌訊息。這些訊息提供驗證過程的詳細資訊，PostgreSQL 開發人員可能會感興趣；進階使用者也可能發現這些資訊很有幫助，因為驗證實際偵測到不一致時，它可提供額外的脈絡。請執行：

```

SET client_min_messages = DEBUG1;
```

在互動式 psql 工作階段中、執行驗證查詢之前設定，即可顯示驗證進度訊息，其詳細程度足以管理。

`verify_heapam(relation regclass, on_error_stop boolean, check_toast boolean, skip text, startblock bigint, endblock bigint, blkno OUT bigint, offnum OUT integer, attnum OUT integer, msg OUT text) returns setof record`
:   檢查資料表、序列或具體化檢視表是否有結構毀損（關聯中的頁面含有格式無效的資料），以及邏輯毀損（頁面在結構上有效，但與資料庫叢集其餘部分不一致）。

    可識別下列選用引數：

    `on_error_stop`
    :   若為 true，毀損檢查會在發現任何毀損的第一個區塊結束時停止。

        預設為 false。

    `check_toast`
    :   若為 true，會對照目標關聯的 TOAST 資料表檢查已 TOAST 化的值。

        此選項已知速度較慢。此外，若 TOAST 資料表或其索引已毀損，對照 TOAST 值進行檢查可能會使伺服器當機，雖然許多情況下只會產生錯誤。

        預設為 false。

    `skip`
    :   若非 `none`，毀損檢查會依指定方式略過標示為全可見或全凍結的區塊。有效選項為 `all-visible`、`all-frozen` 與 `none`。

        預設為 `none`。

    `startblock`
    :   若已指定，毀損檢查會從指定區塊開始，略過所有先前的區塊。若指定的 *`startblock`* 超出目標資料表的區塊範圍，會產生錯誤。

        預設從第一個區塊開始檢查。

    `endblock`
    :   若已指定，毀損檢查會在指定區塊結束，略過所有剩餘區塊。若指定的 *`endblock`* 超出目標資料表的區塊範圍，會產生錯誤。

        預設會檢查所有區塊。

    對於每個偵測到的毀損，`verify_heapam` 會傳回包含下列欄位的一列：

    `blkno`
    :   含有毀損頁面的區塊編號。

    `offnum`
    :   毀損 tuple 的 OffsetNumber。

    `attnum`
    :   若毀損專屬於某個欄位而非整個 tuple，則為該 tuple 中毀損欄位的屬性編號。

    `msg`
    :   說明偵測到問題的訊息。

<a id="AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION"></a>

### F.1.2. 選用的 *`heapallindexed`* 驗證 [#](#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)

當 B-tree 驗證函式的 *`heapallindexed`* 引數為 `true` 時，會對與目標索引關聯相關的資料表執行額外驗證階段。這相當於「虛擬」的 `CREATE INDEX CONCURRENTLY` 作業，會使用暫存的記憶體內摘要結構檢查所有假設的新索引 tuple 是否存在（此結構會在基本的第一驗證階段按需要建立）。摘要結構會對目標索引中找到的每個 tuple 建立「指紋」。*`heapallindexed`* 驗證背後的高層原理是：等同於既有目標索引的新索引，其項目必定可以在既有結構中找到。

額外的 *`heapallindexed`* 階段會增加顯著負擔：驗證通常需要數倍時間。不過，執行 *`heapallindexed`* 驗證時所取得的關聯層級鎖定不會改變。

摘要結構的大小受 `maintenance_work_mem` 限制。為確保索引中每個應有表示的堆積 tuple，其不一致未被偵測到的機率不超過 2%，每個 tuple 約需 2 位元組記憶體。每個 tuple 可用記憶體越少，遺漏不一致的機率就會緩慢增加。此方法可大幅限制驗證負擔，卻只略微降低偵測問題的機率，尤其適用於將驗證視為例行維護工作的安裝環境。每個單獨缺失或格式錯誤的 tuple，在每次新的驗證嘗試中都有新的被偵測機會。

<a id="AMCHECK-USING-AMCHECK-EFFECTIVELY"></a>

### F.1.3. 有效使用 `amcheck` [#](#AMCHECK-USING-AMCHECK-EFFECTIVELY)

`amcheck` 可有效偵測[資料校驗和](../../server-administration/wal/checksums.md)無法捕捉的各種故障模式，包括：

* 由不正確運算子類別實作造成的結構不一致。

  這包括作業系統定序比較規則變更所造成的問題。像 `text` 這類可定序型別的 datum 比較必須是不可變的（所有用於 B-tree 索引掃描的比較也必須不可變），這表示作業系統定序規則絕不能變更。雖然罕見，作業系統定序規則更新仍可能造成問題。更常見的情況是主要伺服器與待命伺服器之間的定序順序不一致，可能是所用的*主要*作業系統版本不同所致。此類不一致通常只會發生在待命伺服器上，因此通常也只能在待命伺服器上偵測到。

  如果發生此類問題，未必影響每個使用受影響定序排序的索引，因為不論行為不一致，*已建立索引的*值可能剛好具有相同的絕對順序。PostgreSQL 如何使用作業系統 locale 與定序的進一步資訊，請參閱[第 23.1 節](../../server-administration/charset/locale.md)與[第 23.2 節](../../server-administration/charset/collation.md)。
* 索引與其已建立索引之堆積關聯間的結構不一致（執行 *`heapallindexed`* 驗證時）。

  正常作業時不會交叉檢查索引與其堆積關聯。堆積毀損的徵兆可能很細微。
* 假設性、尚未發現的基礎 PostgreSQL 存取方法程式碼、排序程式碼或交易管理程式碼錯誤所造成的毀損。

  索引結構完整性的自動驗證，在新功能或提案中的 PostgreSQL 功能一般測試中扮演角色，因為這些功能可能導入邏輯不一致。資料表結構以及相關可見性和交易狀態資訊的驗證，也有類似作用。一個明顯的測試策略是在執行標準迴歸測試時持續呼叫 `amcheck` 函式。執行測試的詳細資訊請參閱[第 31.1 節](../../server-administration/regress/regress-run.md)。
* 停用資料校驗和時的檔案系統或儲存子系統故障。

  請注意，若存取區塊時只有共享緩衝區命中，`amcheck` 會檢查驗證當下該共享記憶體緩衝區中所表示的頁面。因此，`amcheck` 不一定會檢查驗證當下從檔案系統讀取的資料。啟用校驗和時，將毀損區塊讀入緩衝區可能因校驗和失敗而使 `amcheck` 引發錯誤。
* 有問題的 RAM 或更廣泛記憶體子系統造成的毀損。

  PostgreSQL 不會防護可修正的記憶體錯誤，並假設你使用採用業界標準錯誤更正碼（ECC）或更佳防護的 RAM。然而，ECC 記憶體通常只對單位元錯誤免疫，不應假定它可提供對造成記憶體毀損之故障的*絕對*防護。

  執行 *`heapallindexed`* 驗證時，偵測單位元錯誤的機率通常大幅提高，因為會測試嚴格的二進位相等性，以及堆積中已建立索引的屬性。

結構毀損可能因故障的儲存硬體，或關聯檔案遭無關軟體覆寫或修改而發生。此類毀損也可透過[資料頁校驗和](../../server-administration/wal/checksums.md)偵測。

格式正確、內部一致且相對於其內部校驗和正確的關聯頁面，仍可能含有邏輯毀損。因此，校驗和無法偵測此類毀損。例子包括主要資料表中缺少 TOAST 資料表相應項目的已 TOAST 化值，以及主要資料表中交易 ID 早於資料庫或叢集中最舊有效交易 ID 的 tuple。

已在正式系統中觀察到邏輯毀損的多種原因，包括 PostgreSQL 伺服器軟體錯誤、有瑕疵或設計不佳的備份與還原工具，以及使用者錯誤。

毀損的關聯在正式執行環境中最令人憂慮，而高風險活動在這些環境中最不受歡迎。因此，`verify_heapam` 設計為可在不造成過度風險的情況下診斷毀損。它無法防護所有後端當機原因，因為在嚴重毀損的系統上，即使執行呼叫查詢也可能不安全。它會存取[系統目錄資料表](../../internals/catalogs/catalogs-overview.md)，而系統目錄本身毀損時可能造成問題。

一般而言，`amcheck` 只能證明存在毀損，無法證明不存在毀損。

<a id="AMCHECK-REPAIRING-CORRUPTION"></a>

### F.1.4. 修復毀損 [#](#AMCHECK-REPAIRING-CORRUPTION)

`amcheck` 所引發、與毀損相關的錯誤絕不應是誤判。`amcheck` 在定義上不應發生的情況下引發錯誤，因此經常需要仔細分析 `amcheck` 錯誤。

沒有可修復 `amcheck` 偵測問題的一般方法。應找出不變量違反的根本原因說明。[pageinspect](pageinspect.md) 在診斷 `amcheck` 偵測到的毀損時可能很有幫助。`REINDEX` 未必能有效修復毀損。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/amcheck.html)
