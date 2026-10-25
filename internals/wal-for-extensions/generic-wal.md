<a id="GENERIC-WAL"></a>

## 64.1. 通用 WAL 記錄 [#](#generic-wal) <a href="#generic-wal" id="generic-wal"></a>

雖然所有內建且會寫入 WAL 的模組都有各自的 WAL 記錄類型，但另外也有一種通用 WAL 記錄類型，以通用的方式描述對頁面的變更。

<a id="GENERIC-WAL-NOTE"></a>

### 注意

通用 WAL 記錄在[邏輯解碼](../../server-programming/logicaldecoding/README.md)期間會被忽略。如果你的擴充功能需要邏輯解碼，請考慮使用自訂 WAL 資源管理器。

建構通用 WAL 記錄的 API 定義於 `access/generic_xlog.h`，實作於 `access/transam/generic_xlog.c`。

要使用通用 WAL 記錄機制執行會寫入 WAL 的資料更新，請依照下列步驟：

1. `state = GenericXLogStart(relation)` — 開始為指定的關聯建構通用 WAL 記錄。
2. `page = GenericXLogRegisterBuffer(state, buffer, flags)`
   — 註冊一個要在目前的通用 WAL 記錄中修改的緩衝區。此函式會傳回一個指標，指向該緩衝區頁面的暫存複本，修改應在該複本上進行。（不要直接修改緩衝區的內容。）第三個引數是適用於此操作的旗標位元遮罩。目前唯一的此類旗標是 `GENERIC_XLOG_FULL_IMAGE`，表示 WAL 記錄中應包含完整頁面映像，而非差異更新。通常在頁面是新的或已被完全重寫時，會設定此旗標。如果會寫入 WAL 的動作需要修改多個頁面，可以重複呼叫 `GenericXLogRegisterBuffer`。
3. 對前一步驟取得的頁面映像套用修改。
4. `GenericXLogFinish(state)` — 將變更套用到緩衝區，並送出通用 WAL 記錄。

在上述任何步驟之間，都可以呼叫 `GenericXLogAbort(state)` 來取消 WAL 記錄的建構。這會捨棄對頁面映像複本所做的所有變更。

使用通用 WAL 記錄機制時，請注意下列幾點：

* 不允許直接修改緩衝區！所有修改都必須在從 `GenericXLogRegisterBuffer()` 取得的複本中進行。換句話說，產生通用 WAL 記錄的程式碼絕不應自行呼叫 `BufferGetPage()`。不過，在適當的時機對緩衝區進行 pin／unpin 以及鎖定／解鎖，仍是呼叫端的責任。從 `GenericXLogRegisterBuffer()` 之前直到 `GenericXLogFinish()` 之後，都必須在每個目標緩衝區上持有排他鎖。
* 緩衝區的註冊（步驟 2）與頁面映像的修改（步驟 3）可以自由交錯，也就是說，兩個步驟都可以依任意順序重複。請記住，緩衝區的註冊順序應該與重播期間取得其鎖定的順序相同。
* 一筆通用 WAL 記錄可以註冊的緩衝區數量上限為 `MAX_GENERIC_XLOG_PAGES`。超過此限制時會擲出錯誤。
* 通用 WAL 假設要修改的頁面採用標準配置，特別是 `pd_lower` 與 `pd_upper` 之間沒有有用的資料。
* 由於你修改的是緩衝區頁面的複本，`GenericXLogStart()` 不會開始臨界區段（critical section）。因此，你可以在 `GenericXLogStart()` 與 `GenericXLogFinish()` 之間安全地進行記憶體配置、擲出錯誤等操作。唯一實際的臨界區段位於 `GenericXLogFinish()` 內部。在錯誤退出時，也不需要擔心要呼叫 `GenericXLogAbort()`。
* `GenericXLogFinish()` 會負責將緩衝區標記為 dirty 並設定其 LSN。你不需要自行明確地處理這些事。
* 對於無日誌關聯（unlogged relation），一切運作方式都相同，只是不會實際送出 WAL 記錄。因此，你通常不需要針對無日誌關聯做任何明確的檢查。
* 通用 WAL 的 redo 函式會依照緩衝區註冊的順序取得其排他鎖。在重做所有變更之後，會以相同的順序釋放這些鎖定。
* 如果某個已註冊的緩衝區未指定 `GENERIC_XLOG_FULL_IMAGE`，通用 WAL 記錄會包含新舊頁面映像之間的差異（delta）。此差異是以逐位元組比較為基礎。對於在頁面內移動資料的情況，這種方式並不十分精簡，未來可能會改進。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/generic-wal.html)（原文版本：18.6；核對日期：2026-10-09）
