<a id="PROTOCOL-LOGICAL-REPLICATION"></a>

## 54.5. 邏輯串流複寫協定 [#](#PROTOCOL-LOGICAL-REPLICATION)

[54.5.1. 邏輯串流複寫參數](protocol-logical-replication.md#PROTOCOL-LOGICAL-REPLICATION-PARAMS)

[54.5.2. 邏輯複寫協定訊息](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES)

[54.5.3. 邏輯複寫協定訊息流程](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES-FLOW)

本節說明邏輯複寫協定，也就是由 `START_REPLICATION` `SLOT` *`slot_name`* `LOGICAL` 複寫命令啟動的訊息流程。

邏輯串流複寫協定建立在實體串流複寫協定的基本機制之上。

PostgreSQL 的邏輯解碼支援輸出外掛程式。`pgoutput` 是內建邏輯複寫所使用的標準輸出外掛程式。

<a id="PROTOCOL-LOGICAL-REPLICATION-PARAMS"></a>

### 54.5.1. 邏輯串流複寫參數 [#](#PROTOCOL-LOGICAL-REPLICATION-PARAMS)

使用 `START_REPLICATION` 命令時，`pgoutput` 接受下列選項：

proto_version
:   協定版本。目前支援版本 `1`、`2`、`3` 與 `4`。必須提供有效的版本。

    版本 `2` 僅在伺服器版本 14 以上受支援，它允許串流傳送大型的進行中交易。

    版本 `3` 僅在伺服器版本 15 以上受支援，它允許串流傳送兩階段提交。

    版本 `4` 僅在伺服器版本 16 以上受支援，它允許平行套用大型進行中交易的串流。

publication_names
:   要訂閱（接收其變更）的發佈名稱清單，以逗號分隔。個別發佈名稱會被視為標準物件名稱，並可視需要以相同方式加上引號。至少需要一個發佈名稱。

binary
:   使用二進位傳輸模式的布林選項。二進位模式比文字模式快，但穩健性略差。

messages
:   啟用傳送由 `pg_logical_emit_message` 寫入之訊息的布林選項。

streaming
:   啟用串流傳送進行中交易的選項。有效值為 `off`（預設）、`on` 與 `parallel`。設定 `parallel` 會在部分訊息中傳送額外資訊，供平行化使用。要將其設為 `on`，至少需要協定版本 2。`parallel` 值至少需要協定版本 4。

two_phase
:   啟用兩階段交易的布林選項。要將其開啟，至少需要協定版本 3。

origin
:   依變更的來源傳送變更的選項。可能的值為 `none`，表示只傳送沒有關聯來源的變更；或 `any`，表示不論來源為何都傳送變更。這可用來避免複寫節點之間產生迴圈（相同資料無限複寫）。

<a id="PROTOCOL-LOGICAL-MESSAGES"></a>

### 54.5.2. 邏輯複寫協定訊息 [#](#PROTOCOL-LOGICAL-MESSAGES)

以下各小節將討論個別的協定訊息。個別訊息的說明請參閱[第 54.9 節](protocol-logicalrep-message-formats.md)。

所有最上層協定訊息都以一個訊息類型位元組開頭。雖然在程式碼中以字元表示，但它是沒有關聯編碼的有號位元組。

由於串流複寫協定會提供訊息長度，最上層協定訊息不需要在其標頭中嵌入長度。

<a id="PROTOCOL-LOGICAL-MESSAGES-FLOW"></a>

### 54.5.3. 邏輯複寫協定訊息流程 [#](#PROTOCOL-LOGICAL-MESSAGES-FLOW)

除了 `START_REPLICATION` 命令與重播進度訊息之外，所有資訊都只會從後端流向前端。

邏輯複寫協定會逐一傳送個別交易。這表示一對 Begin 與 Commit 訊息之間的所有訊息都屬於同一個交易。同樣地，一對 Begin Prepare 與 Prepare 訊息之間的所有訊息也屬於同一個交易。它也會在一對 Stream Start 與 Stream Stop 訊息之間傳送大型進行中交易的變更。此類交易的最後一個串流會包含 Stream Commit 或 Stream Abort 訊息。

每個傳送的交易都包含零個或多個 DML 訊息（Insert、Update、Delete）。在串聯設定的情況下，它也可能包含 Origin 訊息。Origin 訊息表示該交易源自不同的複寫節點。由於在邏輯複寫協定的範圍內，複寫節點幾乎可以是任何東西，唯一的識別資訊就是來源名稱。視需要（若有需要）處理此資訊是下游端的責任。Origin 訊息一律在交易中的任何 DML 訊息之前傳送。

每個 DML 訊息都包含一個關聯 OID，用以識別發佈者被操作的關聯。在針對某個關聯 OID 的第一個 DML 訊息之前，會先傳送 Relation 訊息，描述該關聯的結構。之後，若自上次為該關聯傳送 Relation 訊息以來，該關聯的定義已有變更，就會傳送新的 Relation 訊息。（此協定假設用戶端能夠為所需數量的關聯記住這些中繼資料。）

Relation 訊息以 OID 識別欄位型別。對於內建型別，會假設用戶端能夠在本機查詢該型別 OID，因此不需要額外資料。對於非內建的型別 OID，會在 Relation 訊息之前傳送 Type 訊息，以提供與該 OID 關聯的型別名稱。因此，需要明確識別關聯欄位型別的用戶端，應該快取 Type 訊息的內容，並先查閱該快取，確認該型別 OID 是否已定義於其中。若沒有，則在本機查詢該型別 OID。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-logical-replication.html)（原文版本：18.6；核對日期：2026-10-12）
