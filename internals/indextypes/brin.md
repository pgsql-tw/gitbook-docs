<a id="BRIN"></a>

## 65.5. BRIN 索引 [#](#brin) <a href="#brin" id="brin"></a>

[65.5.1. 簡介](brin.md#brin-intro)

[65.5.2. 內建運算子類別](brin/brin-builtin-opclasses.md#brin-builtin-opclasses)

[65.5.3. 擴充性](brin/brin-extensibility.md#brin-extensibility)

<a id="id-1.10.17.6.2"></a>
<a id="BRIN-INTRO"></a>

### 65.5.1. 簡介 [#](#brin-intro) <a href="#brin-intro" id="brin-intro"></a>

BRIN 是 Block Range Index（區塊範圍索引）的縮寫。BRIN 的設計目的是處理非常大的資料表，其中某些欄位與其在資料表中的實體位置具有某種自然的相關性。

BRIN 以*區塊範圍*（或稱「頁面範圍」）為單位運作。區塊範圍是資料表中實體上相鄰的一組頁面；索引會為每個區塊範圍儲存一些摘要資訊。舉例來說，儲存商店銷售訂單的資料表可能有一個記錄每筆訂單下單日期的日期欄位，而且大多數情況下，較早訂單的項目在資料表中也會出現在較前面的位置；儲存郵遞區號欄位的資料表，則可能自然地將同一城市的所有郵遞區號歸在一起。

BRIN 索引可以透過一般的點陣圖索引掃描來滿足查詢；若索引所儲存的摘要資訊與查詢條件*一致*，就會傳回每個範圍內所有頁面中的所有 tuple。查詢執行器負責重新檢查這些 tuple，並捨棄不符合查詢條件的 tuple——換句話說，這些索引是有損的（lossy）。由於 BRIN 索引非常小，與循序掃描相比，掃描索引只會增加很少的額外負擔，但可能可以避免掃描資料表中已知不含符合條件之 tuple 的大部分區域。

BRIN 索引實際儲存哪些資料，以及索引能夠滿足哪些查詢，取決於為索引的每個欄位所選用的運算子類別。例如，具有線性排序順序的資料型別，可以有儲存每個區塊範圍內最小值與最大值的運算子類別；幾何型別則可能儲存區塊範圍內所有物件的外接矩形（bounding box）。

區塊範圍的大小在建立索引時由 `pages_per_range` 儲存參數決定。索引項目的數量會等於以頁面計的關聯大小除以為 `pages_per_range` 選定的值。因此，這個數字越小，索引就越大（因為需要儲存更多索引項目），但同時所儲存的摘要資料也可以更精確，而且在索引掃描期間可以跳過更多資料區塊。

<a id="BRIN-OPERATION"></a>

#### 65.5.1.1. 索引維護 [#](#BRIN-OPERATION)

建立索引時，會掃描所有現有的堆積頁面，並為每個範圍建立一個摘要索引 tuple，包括結尾處可能不完整的範圍。當新頁面填入資料時，已摘要的頁面範圍會使摘要資訊以新 tuple 的資料更新。當建立的新頁面不在最後一個已摘要的範圍內時，該新頁面所屬的範圍不會自動取得摘要 tuple；這些 tuple 會維持未摘要的狀態，直到之後執行摘要作業，為該範圍建立初始摘要為止。

有幾種方式可以觸發頁面範圍的初始摘要。如果資料表被執行 vacuum，無論是手動執行或由 [autovacuum](../../server-administration/maintenance/routine-vacuuming.md#autovacuum) 執行，所有現有的未摘要頁面範圍都會被摘要。此外，如果啟用了索引的 [autosummarize](../../reference/sql-commands/sql-createindex.md#INDEX-RELOPTION-AUTOSUMMARIZE) 參數（預設並未啟用），則每當 autovacuum 在該資料庫中執行時，所有已填滿的未摘要頁面範圍都會進行摘要，無論資料表本身是否被 autovacuum 處理；請參閱下文。

最後，也可以使用下列函式（這些函式執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog, pg_temp`）：

<table border="0" class="simplelist" summary="簡單清單"><tr><td>
<code class="function">brin_summarize_new_values(regclass)</code>
     摘要所有未摘要的範圍；
    </td></tr><tr><td>
<code class="function">brin_summarize_range(regclass, bigint)</code>
     僅摘要包含指定頁面的範圍（若該範圍尚未摘要）。
    </td></tr></table>

啟用自動摘要時，當偵測到有資料插入下一個區塊範圍第一個頁面的第一個項目時，會向 `autovacuum` 送出一個請求，要求對該區塊範圍執行定向摘要，這個請求會在下一次 autovacuum 工作程序於同一資料庫中執行完畢時完成。如果請求佇列已滿，該請求不會被記錄，並且會向伺服器日誌送出一則訊息：

```

LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded
```

發生這種情況時，該範圍會維持未摘要的狀態，直到下一次對該資料表執行一般的 vacuum，或呼叫上述函式之一為止。

反過來說，可以使用 `brin_desummarize_range(regclass, bigint)` 函式取消某個範圍的摘要；當現有的值已經改變，使得索引 tuple 不再能很好地代表它們時，這個函式就很有用。詳細資訊請參閱[第 9.28.8 節](../../the-sql-language/functions/functions-admin/functions-admin-index.md#functions-admin-index)。

### 65.5.2. 內建運算子類別 [#](#brin-builtin-opclasses) <a href="#brin-builtin-opclasses" id="brin-builtin-opclasses"></a>

完整內容請見 [65.5.2. 內建運算子類別](brin/brin-builtin-opclasses.md#brin-builtin-opclasses)。

### 65.5.3. 擴充性 [#](#brin-extensibility) <a href="#brin-extensibility" id="brin-extensibility"></a>

完整內容請見 [65.5.3. 擴充性](brin/brin-extensibility.md#brin-extensibility)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/brin.html)（原文版本：18.6；核對日期：2026-10-12）
