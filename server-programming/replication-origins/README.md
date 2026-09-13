## 第 48 章 複寫進度追蹤

<a id="id-1.8.15.2"></a><a id="id-1.8.15.3"></a>

複寫來源的目的，是讓人們更容易在[邏輯解碼](../logicaldecoding/README.md)之上實作邏輯複寫的解決方案。它們為兩個常見的問題提供了解答：

* 如何安全地追蹤複寫進度
* 如何依據資料列的來源改變複寫行為；例如，在雙向複寫的架構中防止產生迴圈

複寫來源只有兩個屬性：名稱與 ID。名稱是跨系統之間用來指涉該來源的依據，型別為自由格式的 `text`。使用時應該讓不同複寫解決方案所建立的複寫來源之間不容易發生名稱衝突；例如，在名稱前面加上該複寫解決方案的名稱作為前綴。ID 只是為了避免在重視空間效率的情況下還得儲存冗長的名稱而存在。它絕對不應該跨系統共用。

複寫來源可以用 [`pg_replication_origin_create()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-CREATE) 函式建立；用 [`pg_replication_origin_drop()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-DROP) 刪除；並且可以在 [`pg_replication_origin`](../../internals/catalogs/catalog-pg-replication-origin.md) 系統目錄中看到。

建構一個複寫解決方案時，有一個並不簡單的部分，就是以安全的方式追蹤重播進度。當套用的程序、或是整個叢集掛掉時，必須有辦法查出資料已經成功複寫到哪裡。針對這件事的天真作法，例如為每一筆重播的交易更新資料表中的一筆資料列，會有執行時期額外負擔與資料庫膨脹之類的問題。

利用複寫來源的基礎設施，可以把一個工作階段標記為正在從遠端節點重播（使用 [`pg_replication_origin_session_setup()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-SESSION-SETUP) 函式）。此外，每一筆來源交易的 LSN 與提交時間戳記，也可以使用 [`pg_replication_origin_xact_setup()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-XACT-SETUP) 以逐筆交易的方式來設定。如果這麼做，複寫進度就會以能夠承受當機的方式持續保存下來。所有複寫來源的重播進度都可以在 [`pg_replication_origin_status`](../../internals/views/view-pg-replication-origin-status.md) 檢視表中看到。個別來源的進度，例如在恢復複寫時所需要的，可以用 [`pg_replication_origin_progress()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-PROGRESS) 取得任一來源的進度，或是用 [`pg_replication_origin_session_progress()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-SESSION-PROGRESS) 取得目前工作階段所設定之來源的進度。

在比「恰好由一個系統複寫到另一個系統」更複雜的複寫拓樸中，另一個問題可能是很難避免把已經重播過的資料列再複寫一次。這可能同時造成複寫上的循環與效率不彰。複寫來源提供了一個選用的機制來辨識並防止這種情形。當使用前一段所提到的函式完成設定後，該工作階段所產生、並傳遞給輸出外掛回呼函式（參閱[第 47.6 節](../logicaldecoding/logicaldecoding-output-plugin.md)）的每一筆變更與交易，都會被標上產生它的那個工作階段的複寫來源。這使得輸出外掛可以對它們做不同的處理，例如忽略所有非本地產生的資料列。此外，也可以使用 [`filter_by_origin_cb`](../logicaldecoding/logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-FILTER-ORIGIN) 回呼函式，依據來源來過濾邏輯解碼的變更串流。雖然彈性較小，但透過這個回呼函式來過濾，效率遠比在輸出外掛中過濾來得高。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/replication-origins.html)（原文版本：18.6；核對日期：2026-09-13）
