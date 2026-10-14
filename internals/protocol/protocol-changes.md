<a id="PROTOCOL-CHANGES"></a>

## 54.10. 自協定 2.0 以來的變更摘要 [#](#PROTOCOL-CHANGES)

本節提供一份變更的快速檢查清單，供試圖將現有用戶端函式庫更新至協定 3.0 的開發人員參考。

最初的啟動封包改用彈性的字串清單格式，而不是固定格式。請注意，現在可以直接在啟動封包中指定執行期參數的工作階段預設值。（實際上，以前也可以使用 `options` 欄位做到這一點，但由於 `options` 的寬度有限，而且沒有任何方法可以為值中的空白字元加上引號，這並不是一種非常安全的技巧。）

現在所有訊息在訊息類型位元組之後都緊接著一個長度計數（啟動封包除外，它沒有類型位元組）。另請注意，PasswordMessage 現在有類型位元組。

ErrorResponse 與 NoticeResponse（'`E`' 與 '`N`'）訊息現在包含多個欄位，用戶端程式碼可以從中組合出所需詳細程度的錯誤訊息。請注意，個別欄位通常不會以換行字元結尾，而舊協定中所傳送的單一字串則一定會以換行字元結尾。

ReadyForQuery（'`Z`'）訊息包含交易狀態指示。

BinaryRow 與 DataRow 訊息類型之間的區別已經不存在；單一的 DataRow 訊息類型可用於傳回所有格式的資料。請注意，DataRow 的配置已經改變，使其更容易剖析。此外，二進位值的表示方式也已改變：它不再直接與伺服器的內部表示方式綁定。

新增了一個「延伸查詢」子協定，它加入了前端訊息類型 Parse、Bind、Execute、Describe、Close、Flush 與 Sync，以及後端訊息類型 ParseComplete、BindComplete、PortalSuspended、ParameterDescription、NoData 與 CloseComplete。現有的用戶端不必理會這個子協定，但使用它可能會帶來效能或功能上的改進。

`COPY` 資料現在封裝在 CopyData 與 CopyDone 訊息中。在 `COPY` 期間有一套明確定義的錯誤復原方式。不再需要特殊的「`\.`」最後一行，而且在 `COPY OUT` 期間也不會傳送它。（在文字模式的 `COPY
IN` 中，它仍會被辨識為結束符號，但在 CSV 模式中則不會。文字模式的這項行為已棄用，最終可能會被移除。）支援二進位 `COPY`。CopyInResponse 與 CopyOutResponse 訊息包含一些欄位，指出欄位的數量以及每個欄位的格式。

FunctionCall 與 FunctionCallResponse 訊息的配置已經改變。FunctionCall 現在支援將 NULL 引數傳給函式。它也可以處理以文字或二進位格式傳遞參數與取回結果。現在已沒有任何理由將 FunctionCall 視為潛在的安全漏洞，因為它不提供對伺服器內部資料表示方式的直接存取。

後端會在連線啟動期間，為所有它認為用戶端函式庫會感興趣的參數傳送 ParameterStatus（'`S`'）訊息。之後，只要其中任何一個參數的有效值改變，就會傳送 ParameterStatus 訊息。

RowDescription（'`T`'）訊息為所描述資料列的每個欄位帶有新的資料表 OID 與欄位編號欄位。它也會顯示每個欄位的格式代碼。

後端不再產生 CursorResponse（'`P`'）訊息。

NotificationResponse（'`A`'）訊息多了一個字串欄位，可以攜帶由 `NOTIFY` 事件傳送者所傳遞的「酬載」字串。

EmptyQueryResponse（'`I`'）訊息過去包含一個空字串參數；此參數已被移除。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-changes.html)（原文版本：18.6；核對日期：2026-10-12）
