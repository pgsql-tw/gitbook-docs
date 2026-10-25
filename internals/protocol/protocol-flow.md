<a id="PROTOCOL-FLOW"></a>

## 54.2. 訊息流程 [#](#protocol-flow) <a href="#protocol-flow" id="protocol-flow"></a>

[54.2.1. 啟動](protocol-flow.md#PROTOCOL-FLOW-START-UP)

[54.2.2. 簡單查詢](protocol-flow.md#PROTOCOL-FLOW-SIMPLE-QUERY)

[54.2.3. 延伸查詢](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)

[54.2.4. 管線化](protocol-flow.md#PROTOCOL-FLOW-PIPELINING)

[54.2.5. 函式呼叫](protocol-flow.md#PROTOCOL-FLOW-FUNCTION-CALL)

[54.2.6. COPY 操作](protocol-flow.md#PROTOCOL-COPY)

[54.2.7. 非同步操作](protocol-flow.md#PROTOCOL-ASYNC)

[54.2.8. 取消進行中的請求](protocol-flow.md#PROTOCOL-FLOW-CANCELING-REQUESTS)

[54.2.9. 終止](protocol-flow.md#PROTOCOL-FLOW-TERMINATION)

[54.2.10. SSL 工作階段加密](protocol-flow.md#PROTOCOL-FLOW-SSL)

[54.2.11. GSSAPI 工作階段加密](protocol-flow.md#PROTOCOL-FLOW-GSSAPI)

本節說明訊息流程以及各訊息類型的語意。（各訊息確切的表示方式請參閱[第 54.7 節](protocol-message-formats.md)。）依連線狀態的不同，有幾種不同的子協定：啟動、查詢、函式呼叫、`COPY` 以及終止。另外也有針對非同步操作（包括通知回應與命令取消）的特別規定，這些操作可能在啟動階段之後的任何時間發生。

<a id="PROTOCOL-FLOW-START-UP"></a>

### 54.2.1. 啟動 [#](#PROTOCOL-FLOW-START-UP)

要開始一個工作階段，前端會開啟與伺服器的連線並傳送啟動訊息。此訊息包含使用者名稱以及該使用者想要連線的資料庫名稱；它也指出要使用的特定協定版本。（啟動訊息也可以選擇性地包含執行期參數的額外設定。）接著，伺服器會使用這些資訊以及其設定檔（例如 `pg_hba.conf`）的內容，判斷此連線是否可暫時接受，以及需要哪些額外的認證（若有的話）。

接著，伺服器會傳送適當的認證請求訊息，前端必須以適當的認證回應訊息（例如密碼）回覆。除了 GSSAPI、SSPI 與 SASL 之外，所有認證方法最多只有一次請求與一次回應。某些方法完全不需要前端回應，因此也不會發生認證請求。對於 GSSAPI、SSPI 與 SASL，可能需要多次交換封包才能完成認證。

認證循環的結束方式是：伺服器拒絕連線嘗試（ErrorResponse），或是傳送 AuthenticationOk。

此階段中伺服器可能傳送的訊息有：

ErrorResponse

連線嘗試已被拒絕。伺服器接著會立即關閉連線。

AuthenticationOk

認證交換已成功完成。

AuthenticationKerberosV5

前端現在必須與伺服器進行 Kerberos V5 認證對話（此處不加說明，屬於 Kerberos 規格的一部分）。若成功，伺服器會回應 AuthenticationOk，否則回應 ErrorResponse。此方式已不再支援。

AuthenticationCleartextPassword

前端現在必須傳送一個以明文形式包含密碼的 PasswordMessage。若密碼正確，伺服器會回應 AuthenticationOk，否則回應 ErrorResponse。

AuthenticationMD5Password

前端現在必須傳送一個 PasswordMessage，其中的密碼（連同使用者名稱）先以 MD5 加密，再使用 AuthenticationMD5Password 訊息中指定的 4 位元組隨機鹽值（salt） 再加密一次。若密碼正確，伺服器會回應 AuthenticationOk，否則回應 ErrorResponse。實際的 PasswordMessage 可以在 SQL 中以 `concat('md5',
    md5(concat(md5(concat(password, username)), random-salt)))` 計算。（請記得 `md5()` 函式會以十六進位字串傳回其結果。）

### 警告

對 MD5 加密密碼的支援已棄用，並將在 PostgreSQL 的未來版本中移除。關於改用其他密碼類型的詳細資訊，請參閱[第 20.5 節](../../server-administration/client-authentication/auth-password.md)。

AuthenticationGSS

前端現在必須啟動 GSSAPI 協商。前端會傳送一個 GSSResponse 訊息作為回應，其中包含 GSSAPI 資料串流的第一部分。若需要更多訊息，伺服器會回應 AuthenticationGSSContinue。

AuthenticationSSPI

前端現在必須啟動 SSPI 協商。前端會傳送一個 GSSResponse 作為回應，其中包含 SSPI 資料串流的第一部分。若需要更多訊息，伺服器會回應 AuthenticationGSSContinue。

AuthenticationGSSContinue

此訊息包含 GSSAPI 或 SSPI 協商前一步驟（AuthenticationGSS、AuthenticationSSPI 或前一個 AuthenticationGSSContinue）的回應資料。若此訊息中的 GSSAPI 或 SSPI 資料表示還需要更多資料才能完成認證，前端必須將那些資料以另一個 GSSResponse 訊息傳送。若 GSSAPI 或 SSPI 認證已由此訊息完成，伺服器接下來會傳送 AuthenticationOk 表示認證成功，或傳送 ErrorResponse 表示失敗。

AuthenticationSASL

前端現在必須使用訊息中所列的其中一種 SASL 機制啟動 SASL 協商。前端會傳送一個 SASLInitialResponse 作為回應，其中包含所選機制的名稱以及 SASL 資料串流的第一部分。若需要更多訊息，伺服器會回應 AuthenticationSASLContinue。詳細資訊請參閱[第 54.3 節](sasl-authentication.md)。

AuthenticationSASLContinue

此訊息包含 SASL 協商前一步驟（AuthenticationSASL 或前一個 AuthenticationSASLContinue）的挑戰資料。前端必須以 SASLResponse 訊息回應。

AuthenticationSASLFinal

SASL 認證已完成，並附帶給用戶端的額外機制專屬資料。伺服器接下來會傳送 AuthenticationOk 表示認證成功，或傳送 ErrorResponse 表示失敗。只有在 SASL 機制規定完成時要從伺服器傳送額外資料給用戶端時，才會傳送此訊息。

NegotiateProtocolVersion

伺服器不支援用戶端所請求的次要協定版本，但支援較早的協定版本；此訊息指出所支援的最高次要版本。若用戶端在啟動封包中請求了不支援的協定選項（亦即以 `_pq_.` 開頭者），也會傳送此訊息。

收到此訊息後，認證會使用伺服器所指出的版本繼續進行。若用戶端不支援該較舊版本，應該立即關閉連線。若伺服器未傳送此訊息，表示它支援用戶端所請求的協定版本以及所有協定選項。

若前端不支援伺服器所請求的認證方法，則應該立即關閉連線。

收到 AuthenticationOk 之後，前端必須等待伺服器傳來更多訊息。在此階段中，後端程序正在啟動，前端只是一個關心結果的旁觀者。啟動嘗試仍有可能失敗（ErrorResponse），伺服器也可能拒絕支援所請求的次要協定版本（NegotiateProtocolVersion），但在正常情況下，後端會傳送一些 ParameterStatus 訊息、BackendKeyData，最後是 ReadyForQuery。

在此階段中，後端會嘗試套用啟動訊息中所給的任何額外執行期參數設定。若成功，這些值會成為工作階段的預設值。發生錯誤時會產生 ErrorResponse 並結束。

此階段中後端可能傳送的訊息有：

BackendKeyData

此訊息提供祕密金鑰資料；前端若希望之後能發出取消請求，就必須保存這些資料。前端不應該回應此訊息，而應該繼續等待 ReadyForQuery 訊息。

PostgreSQL 伺服器一定會傳送此訊息，但已知某些不支援查詢取消的第三方後端協定實作不會傳送。

ParameterStatus

此訊息告知前端後端參數目前的（初始）設定，例如 [client_encoding](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-ENCODING) 或 [DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE)。前端可以忽略此訊息，或記錄這些設定以供日後使用；詳細資訊請參閱[第 54.2.7 節](protocol-flow.md#PROTOCOL-ASYNC)。前端不應該回應此訊息，而應該繼續等待 ReadyForQuery 訊息。

ReadyForQuery

啟動已完成。前端現在可以發出命令。

ErrorResponse

啟動失敗。傳送此訊息後連線即關閉。

NoticeResponse

已發出一則警告訊息。前端應該顯示該訊息，但繼續等待 ReadyForQuery 或 ErrorResponse。

ReadyForQuery 訊息與後端在每個命令循環之後發出的訊息相同。依前端程式撰寫上的需要，可以合理地將 ReadyForQuery 視為一個命令循環的開始，也可以將 ReadyForQuery 視為啟動階段以及其後每個命令循環的結束。

<a id="PROTOCOL-FLOW-SIMPLE-QUERY"></a>

### 54.2.2. 簡單查詢 [#](#PROTOCOL-FLOW-SIMPLE-QUERY)

簡單查詢循環由前端傳送 Query 訊息給後端而開始。此訊息包含以文字字串表示的一個 SQL 命令（或多個命令）。接著，後端會依查詢命令字串的內容傳送一個或多個回應訊息，最後傳送 ReadyForQuery 回應訊息。ReadyForQuery 告知前端它可以安全地傳送新命令。（前端其實不一定要等到 ReadyForQuery 才發出下一個命令，但這樣一來，前端就必須自行負責處理較早的命令失敗、而已發出的較晚命令卻成功時的情況。）

後端可能傳送的回應訊息有：

CommandComplete

一個 SQL 命令已正常完成。

CopyInResponse

後端已準備好將資料從前端複製到資料表；請參閱[第 54.2.6 節](protocol-flow.md#PROTOCOL-COPY)。

CopyOutResponse

後端已準備好將資料從資料表複製到前端；請參閱[第 54.2.6 節](protocol-flow.md#PROTOCOL-COPY)。

RowDescription

表示即將傳回資料列，以回應 `SELECT`、`FETCH` 等查詢。此訊息的內容描述資料列的欄位配置。之後，每個傳回給前端的資料列都會有一個 DataRow 訊息。

DataRow

由 `SELECT`、`FETCH` 等查詢傳回的資料列集合中的一列。

EmptyQueryResponse

辨識到空的查詢字串。

ErrorResponse

發生錯誤。

ReadyForQuery

查詢字串的處理已完成。之所以另外傳送一則訊息來表示這點，是因為查詢字串可能包含多個 SQL 命令。（CommandComplete 標示的是一個 SQL 命令處理的結束，而不是整個字串的結束。）無論處理是成功結束或因錯誤而結束，一定都會傳送 ReadyForQuery。

NoticeResponse

已發出一則與該查詢相關的警告訊息。通知是附加在其他回應之外的，也就是說，後端會繼續處理該命令。

對 `SELECT` 查詢（或其他傳回資料列集合的查詢，例如 `EXPLAIN` 或 `SHOW`）的回應，通常由 RowDescription、零個或多個 DataRow 訊息，以及最後的 CommandComplete 組成。往返前端的 `COPY`（複製到前端或從前端複製）會啟動特殊的協定，如[第 54.2.6 節](protocol-flow.md#PROTOCOL-COPY)所述。所有其他類型的查詢通常只會產生一個 CommandComplete 訊息。

由於一個查詢字串可能包含多個查詢（以分號分隔），在後端完成查詢字串的處理之前，可能會有多個這樣的回應序列。當整個字串都已處理完畢、且後端已準備好接受新的查詢字串時，就會發出 ReadyForQuery。

若收到完全空白（除了空白字元之外沒有任何內容）的查詢字串，回應是 EmptyQueryResponse，接著是 ReadyForQuery。

發生錯誤時，會發出 ErrorResponse，接著是 ReadyForQuery。ErrorResponse 會中止查詢字串所有後續的處理（即使其中還有剩餘的查詢）。請注意，這可能發生在單一查詢所產生的訊息序列的中途。

在簡單 Query 模式中，所擷取值的格式一律是文字，除非所給的命令是從以 `BINARY` 選項宣告的游標執行 `FETCH`。在那種情況下，所擷取的值是二進位格式。RowDescription 訊息中所給的格式代碼會指出正在使用哪一種格式。

前端只要在等待任何其他類型的訊息時，都必須準備好接受 ErrorResponse 與 NoticeResponse 訊息。關於後端可能因外部事件而產生的訊息，另請參閱[第 54.2.7 節](protocol-flow.md#PROTOCOL-ASYNC)。

建議的做法是以狀態機的風格撰寫前端程式，在任何合理的時間點都能接受任何訊息類型，而不是把對確切訊息順序的假設寫死在程式中。

<a id="PROTOCOL-FLOW-MULTI-STATEMENT"></a>

#### 54.2.2.1. 簡單查詢中的多個陳述式 [#](#PROTOCOL-FLOW-MULTI-STATEMENT)

當簡單 Query 訊息包含超過一個 SQL 陳述式（以分號分隔）時，這些陳述式會作為單一交易執行，除非其中包含明確的交易控制命令來強制採取不同的行為。例如，若訊息包含

```

INSERT INTO mytable VALUES(1);
SELECT 1/0;
INSERT INTO mytable VALUES(2);
```

則 `SELECT` 中的除以零錯誤會強制回復第一個 `INSERT`。此外，由於訊息的執行會在第一個錯誤處放棄，第二個 `INSERT` 根本不會被嘗試執行。

若訊息改為包含

```

BEGIN;
INSERT INTO mytable VALUES(1);
COMMIT;
INSERT INTO mytable VALUES(2);
SELECT 1/0;
```

則第一個 `INSERT` 會由明確的 `COMMIT` 命令提交。第二個 `INSERT` 與 `SELECT` 仍會被視為單一交易，因此除以零錯誤會回復第二個 `INSERT`，但不會回復第一個。

此行為的實作方式是：除非已有某個明確的交易區塊可供執行，否則多陳述式 Query 訊息中的陳述式會在一個*隱含交易區塊*中執行。隱含交易區塊與一般交易區塊的主要差別在於，隱含區塊會在 Query 訊息結束時自動關閉：若沒有錯誤，就以隱含提交關閉；若有錯誤，就以隱含回復關閉。這類似於單獨執行（不在交易區塊中）的陳述式所發生的隱含提交或回復。

若工作階段因為先前某個訊息中的 `BEGIN` 而已經位於交易區塊中，那麼無論 Query 訊息包含一個或多個陳述式，它都只是延續該交易區塊。然而，若 Query 訊息包含關閉現有交易區塊的 `COMMIT` 或 `ROLLBACK`，則其後的所有陳述式都會在隱含交易區塊中執行。反過來說，若多陳述式 Query 訊息中出現 `BEGIN`，它會開始一個一般交易區塊，該區塊只會由明確的 `COMMIT` 或 `ROLLBACK` 終止，無論這個命令出現在此 Query 訊息或之後的訊息中。若 `BEGIN` 出現在某些已作為隱含交易區塊執行的陳述式之後，那些陳述式不會立即提交；實際上，它們會被追溯納入新的一般交易區塊中。

出現在隱含交易區塊中的 `COMMIT` 或 `ROLLBACK` 會照常執行並關閉隱含區塊；不過，系統會發出警告，因為沒有先前 `BEGIN` 的 `COMMIT` 或 `ROLLBACK` 可能代表一個錯誤。若之後還有其他陳述式，會為它們開始一個新的隱含交易區塊。

隱含交易區塊中不允許使用儲存點，因為儲存點會與發生任何錯誤時自動關閉區塊的行為相衝突。

請記住，無論可能出現哪些交易控制命令，Query 訊息的執行都會在第一個錯誤處停止。因此，例如在單一 Query 訊息中給定

```

BEGIN;
SELECT 1/0;
ROLLBACK;
```

工作階段會停留在一個已失敗的一般交易區塊中，因為在除以零錯誤之後不會執行到 `ROLLBACK`。還需要再一個 `ROLLBACK` 才能將工作階段恢復到可用的狀態。

另一個值得注意的行為是，在執行任何部分之前，會先對整個查詢字串進行初步的詞法與語法分析。因此，較後面陳述式中的簡單錯誤（例如拼錯的關鍵字）可能導致所有陳述式都無法執行。這對使用者來說通常是看不出來的，因為這些陳述式作為隱含交易區塊執行時，無論如何都會全部回復。然而，當試圖在一個多陳述式 Query 中執行多個交易時，這就可能看得出來。舉例來說，若打字錯誤把我們先前的範例變成

```

BEGIN;
INSERT INTO mytable VALUES(1);
COMMIT;
INSERT INTO mytable VALUES(2);
SELCT 1/0;
```

那麼所有陳述式都不會執行，造成的明顯差異是第一個 `INSERT` 沒有被提交。在語意分析或之後階段才偵測到的錯誤（例如拼錯的資料表或欄位名稱）則不會有這種效果。

最後請注意，Query 訊息中的所有陳述式都會看到相同的 `statement_timestamp()` 值，因為該時間戳記只在收到 Query 訊息時才會更新。這也會使它們看到相同的 `transaction_timestamp()` 值，除非查詢字串結束了一個先前已開始的交易並開始一個新的交易。

<a id="PROTOCOL-FLOW-EXT-QUERY"></a>

### 54.2.3. 延伸查詢 [#](#PROTOCOL-FLOW-EXT-QUERY)

延伸查詢協定將上述的簡單查詢協定拆成多個步驟。預備步驟的結果可以重複使用多次，以提高效率。此外，還可以使用其他功能，例如能以個別參數的形式提供資料值，而不必將它們直接插入查詢字串中。

在延伸協定中，前端首先傳送 Parse 訊息，其中包含文字查詢字串、參數預留位置資料型別的選擇性資訊，以及目標預備陳述式物件的名稱（空字串表示選擇未命名的預備陳述式）。回應是 ParseComplete 或 ErrorResponse。參數的資料型別可以用 OID 指定；若未指定，剖析器會嘗試以推斷無型別字面字串常數的相同方式來推斷資料型別。

### 注意

參數的資料型別可以藉由設為零而保持未指定，或者讓參數型別 OID 陣列比查詢字串中使用的參數符號（`$`*`n`*）數量短。另一個特殊情況是，參數的型別可以指定為 `void`（也就是 `void` 虛擬型別的 OID）。這是為了讓參數符號可以用於實際上是 OUT 參數的函式參數。一般而言，`void` 參數沒有任何可以使用的情境，但若這樣的參數符號出現在函式的參數清單中，實際上就會被忽略。例如，若 `$3` 與 `$4` 被指定為 `void` 型別，像 `foo($1,$2,$3,$4)` 這樣的函式呼叫就可以符合具有兩個 IN 引數與兩個 OUT 引數的函式。

### 注意

Parse 訊息中所包含的查詢字串不能包含超過一個 SQL 陳述式；否則會回報語法錯誤。簡單查詢協定中沒有這項限制，但延伸協定中有，因為允許預備陳述式或 portal 包含多個命令會使協定過度複雜。

具名的預備陳述式物件一旦成功建立，會持續到目前工作階段結束為止，除非被明確銷毀。未命名的預備陳述式只會持續到下一個以未命名陳述式為目標的 Parse 陳述式發出為止。（請注意，簡單 Query 訊息也會銷毀未命名的陳述式。）具名的預備陳述式必須先明確關閉，才能被另一個 Parse 訊息重新定義，但未命名的陳述式不需要這樣做。具名的預備陳述式也可以在 SQL 命令層級使用 `PREPARE` 與 `EXECUTE` 來建立與存取。

預備陳述式存在之後，可以使用 Bind 訊息使其準備好執行。Bind 訊息提供來源預備陳述式的名稱（空字串表示未命名的預備陳述式）、目標 portal 的名稱（空字串表示未命名的 portal），以及預備陳述式中任何參數預留位置所要使用的值。所提供的參數集合必須符合預備陳述式所需要的參數。（若你在 Parse 訊息中宣告了任何 `void` 參數，請在 Bind 訊息中為它們傳入 NULL 值。）Bind 也指定查詢所傳回的任何資料要使用的格式；格式可以整體指定，也可以逐欄指定。回應是 BindComplete 或 ErrorResponse。

### 注意

文字輸出與二進位輸出之間的選擇，是由 Bind 中所給的格式代碼決定，與所涉及的 SQL 命令無關。使用延伸查詢協定時，游標宣告中的 `BINARY` 屬性無關緊要。

查詢規劃通常在處理 Bind 訊息時進行。若預備陳述式沒有參數，或被重複執行，伺服器可能會保存所建立的計畫，並在之後對同一預備陳述式的 Bind 訊息中重複使用。然而，只有在它發現可以建立一個效率不會比依賴所提供特定參數值的計畫差太多的通用計畫時，才會這麼做。就協定而言，這一切是透明的。

具名的 portal 物件一旦成功建立，會持續到目前交易結束為止，除非被明確銷毀。未命名的 portal 會在交易結束時銷毀，或在下一個以未命名 portal 為目標的 Bind 陳述式發出時立即銷毀。（請注意，簡單 Query 訊息也會銷毀未命名的 portal。）具名的 portal 必須先明確關閉，才能被另一個 Bind 訊息重新定義，但未命名的 portal 不需要這樣做。具名的 portal 也可以在 SQL 命令層級使用 `DECLARE CURSOR` 與 `FETCH` 來建立與存取。

portal 存在之後，可以使用 Execute 訊息執行它。Execute 訊息指定 portal 名稱（空字串表示未命名的 portal）以及最大結果列數（零表示「擷取所有資料列」）。結果列數只對包含傳回資料列集合之命令的 portal 有意義；在其他情況下，命令一律會執行到完成，並忽略該列數。Execute 可能的回應與上述透過簡單查詢協定發出之查詢的回應相同，只是 Execute 不會導致發出 ReadyForQuery 或 RowDescription。

若 Execute 在完成 portal 的執行之前就結束（因為達到非零的結果列數），它會傳送 PortalSuspended 訊息；此訊息的出現告訴前端，應該對同一個 portal 再發出一個 Execute 以完成操作。表示來源 SQL 命令已完成的 CommandComplete 訊息，要等到 portal 的執行完成後才會傳送。因此，一個 Execute 階段一定會以下列訊息中恰好一個的出現作為結束：CommandComplete、EmptyQueryResponse（若 portal 是由空的查詢字串建立）、ErrorResponse 或 PortalSuspended。

每一系列延伸查詢訊息完成時，前端應該發出 Sync 訊息。這個沒有參數的訊息會使後端在不位於 `BEGIN`/`COMMIT` 交易區塊內時關閉目前的交易（「關閉」的意思是：若沒有錯誤就提交，若有錯誤就回復）。接著會發出 ReadyForQuery 回應。Sync 的用途是提供錯誤復原時的重新同步點。在處理任何延伸查詢訊息時偵測到錯誤，後端會發出 ErrorResponse，然後讀取並丟棄訊息，直到遇到 Sync 為止，接著發出 ReadyForQuery 並回到正常的訊息處理。（但請注意，若錯誤是在*處理* Sync 時偵測到的，就不會發生略過——這確保每個 Sync 都會傳送一個且只有一個 ReadyForQuery。）

### 注意

Sync 不會導致以 `BEGIN` 開啟的交易區塊被關閉。由於 ReadyForQuery 訊息包含交易狀態資訊，因此可以偵測到這種情況。

除了這些基本、必要的操作之外，還有幾種可以搭配延伸查詢協定使用的選擇性操作。

Describe 訊息（portal 版本）指定現有 portal 的名稱（或以空字串表示未命名的 portal）。回應是描述執行該 portal 將傳回之資料列的 RowDescription 訊息；若 portal 不包含會傳回資料列的查詢，則回應 NoData 訊息；若沒有這樣的 portal，則回應 ErrorResponse。

Describe 訊息（陳述式版本）指定現有預備陳述式的名稱（或以空字串表示未命名的預備陳述式）。回應是描述該陳述式所需參數的 ParameterDescription 訊息，接著是描述該陳述式最終執行時將傳回之資料列的 RowDescription 訊息（若該陳述式不會傳回資料列，則為 NoData 訊息）。若沒有這樣的預備陳述式，會發出 ErrorResponse。請注意，由於尚未發出 Bind，後端還不知道傳回欄位要使用的格式；在這種情況下，RowDescription 訊息中的格式代碼欄位會是零。

### 提示

在大多數情境中，前端應該在發出 Execute 之前發出其中一種版本的 Describe，以確保它知道如何解讀將取回的結果。

Close 訊息會關閉現有的預備陳述式或 portal，並釋放資源。對不存在的陳述式或 portal 名稱發出 Close 不算錯誤。回應通常是 CloseComplete，但若在釋放資源時遇到某些困難，也可能是 ErrorResponse。請注意，關閉預備陳述式會隱含地關閉所有由該陳述式建構的已開啟 portal。

Flush 訊息不會導致產生任何特定的輸出，而是強制後端送出其輸出緩衝區中任何待送的資料。若前端希望在發出更多命令之前檢查某個延伸查詢命令的結果，就必須在 Sync 以外的任何延伸查詢命令之後傳送 Flush。若沒有 Flush，後端傳回的訊息會被合併成盡可能少的封包，以將網路負擔降到最低。

### 注意

簡單 Query 訊息大約等同於使用未命名預備陳述式與 portal 物件且不帶參數的 Parse、Bind、portal Describe、Execute、Close、Sync 系列。差別之一是，它可以在查詢字串中接受多個 SQL 陳述式，並自動對每個陳述式依序執行 bind/describe/execute 序列。另一個差別是，它不會傳回 ParseComplete、BindComplete、CloseComplete 或 NoData 訊息。

<a id="PROTOCOL-FLOW-PIPELINING"></a>

### 54.2.4. 管線化 [#](#PROTOCOL-FLOW-PIPELINING)

<a id="id-1.10.6.7.6.2"></a>

使用延伸查詢協定可以進行*管線化*，也就是傳送一系列查詢而不等待較早的查詢完成。這可以減少完成一系列操作所需的網路往返次數。不過，使用者必須仔細考量其中某個步驟失敗時所需的行為，因為較後面的查詢已經在送往伺服器的途中。

處理這個問題的一種方式是讓整個查詢系列成為單一交易，也就是用 `BEGIN` ... `COMMIT` 包起來。然而，若希望某些命令能獨立於其他命令提交，這種方式就沒有幫助。

延伸查詢協定提供了另一種處理此問題的方式，就是在相依的步驟之間不傳送 Sync 訊息。由於發生錯誤後，後端會略過命令訊息直到找到 Sync 為止，這使得較早的命令失敗時，管線中較後面的命令可以自動被略過，而用戶端不必明確地以 `BEGIN` 與 `COMMIT` 來管理。管線中可以獨立提交的區段，可以用 Sync 訊息分隔。

若用戶端尚未發出明確的 `BEGIN`，就會開始一個隱含交易區塊，而每個 Sync 通常會在前面的步驟成功時造成隱含的 `COMMIT`，或在失敗時造成隱含的 `ROLLBACK`。只有當第一個命令結束時沒有接著 Sync，伺服器才會偵測到這個隱含交易區塊。有少數 DDL 命令（例如 `CREATE DATABASE`）不能在交易區塊內執行。若在管線中執行其中一個命令，除非它是 Sync 之後的第一個命令，否則就會失敗。此外，成功時它會強制立即提交，以維持資料庫的一致性。因此，緊接在這類命令之後的 Sync，除了回應 ReadyForQuery 之外沒有任何效果。

使用此方法時，必須藉由計算 ReadyForQuery 訊息的數量，並等到其數量達到所傳送的 Sync 數量，來判斷管線是否完成。計算命令完成的回應並不可靠，因為某些命令可能被略過，因而不會產生完成訊息。

<a id="PROTOCOL-FLOW-FUNCTION-CALL"></a>

### 54.2.5. 函式呼叫 [#](#PROTOCOL-FLOW-FUNCTION-CALL)

函式呼叫子協定允許用戶端請求直接呼叫資料庫 `pg_proc` 系統目錄中存在的任何函式。用戶端必須擁有該函式的執行權限。

### 注意

函式呼叫子協定是一項舊有功能，在新的程式碼中最好避免使用。設定一個執行 `SELECT function($1, ...)` 的預備陳述式，就可以達到類似的結果。如此一來，函式呼叫循環就可以用 Bind/Execute 取代。

函式呼叫循環由前端傳送 FunctionCall 訊息給後端而開始。接著，後端會依函式呼叫的結果傳送一個或多個回應訊息，最後傳送 ReadyForQuery 回應訊息。ReadyForQuery 告知前端它可以安全地傳送新的查詢或函式呼叫。

後端可能傳送的回應訊息有：

ErrorResponse

發生錯誤。

FunctionCallResponse

函式呼叫已完成，並傳回訊息中所給的結果。（請注意，函式呼叫協定只能處理單一純量結果，不能處理資料列型別或結果集合。）

ReadyForQuery

函式呼叫的處理已完成。無論處理是成功結束或因錯誤而結束，一定都會傳送 ReadyForQuery。

NoticeResponse

已發出一則與該函式呼叫相關的警告訊息。通知是附加在其他回應之外的，也就是說，後端會繼續處理該命令。

<a id="PROTOCOL-COPY"></a>

### 54.2.6. COPY 操作 [#](#PROTOCOL-COPY)

`COPY` 命令可以與伺服器之間進行高速的大量資料傳輸。複製輸入（copy-in）與複製輸出（copy-out）操作各自會將連線切換到不同的子協定，並持續到操作完成為止。

當後端執行 `COPY FROM STDIN` SQL 陳述式時，就會開始複製輸入模式（將資料傳輸到伺服器）。後端會傳送 CopyInResponse 訊息給前端。接著，前端應該傳送零個或多個 CopyData 訊息，形成輸入資料的串流。（訊息邊界不需要與資料列邊界有任何關係，雖然讓兩者一致通常是合理的選擇。）前端可以傳送 CopyDone 訊息（使複製順利結束）或 CopyFail 訊息（會使 `COPY` SQL 陳述式以錯誤失敗）來結束複製輸入模式。接著，後端會回到 `COPY` 開始之前所處的命令處理模式，也就是簡單查詢協定或延伸查詢協定。接下來，它會傳送 CommandComplete（若成功）或 ErrorResponse（若不成功）。

若後端在複製輸入模式期間偵測到錯誤（包括收到 CopyFail 訊息），後端會發出 ErrorResponse 訊息。若 `COPY` 命令是透過延伸查詢訊息發出的，後端此時會丟棄前端訊息，直到收到 Sync 訊息為止，接著發出 ReadyForQuery 並回到正常處理。若 `COPY` 命令是在簡單 Query 訊息中發出的，該訊息的其餘部分會被丟棄，並發出 ReadyForQuery。無論哪一種情況，前端之後發出的任何 CopyData、CopyDone 或 CopyFail 訊息都會直接被丟棄。

後端會忽略在複製輸入模式期間收到的 Flush 與 Sync 訊息。收到任何其他非複製類的訊息類型都會構成錯誤，並如上所述中止複製輸入狀態。（對 Flush 與 Sync 的例外處理，是為了方便那些總是在 Execute 訊息之後傳送 Flush 或 Sync、而不檢查要執行的命令是否為 `COPY FROM STDIN` 的用戶端函式庫。）

當後端執行 `COPY TO STDOUT` SQL 陳述式時，就會開始複製輸出模式（從伺服器傳輸資料）。後端會傳送 CopyOutResponse 訊息給前端，接著是零個或多個 CopyData 訊息（一律每個資料列一個），然後是 CopyDone。接著，後端會回到 `COPY` 開始之前所處的命令處理模式，並傳送 CommandComplete。前端無法中止傳輸（除非關閉連線或發出取消請求），但可以丟棄不需要的 CopyData 與 CopyDone 訊息。

若後端在複製輸出模式期間偵測到錯誤，後端會發出 ErrorResponse 訊息並回到正常處理。前端應該將收到 ErrorResponse 視為複製輸出模式的結束。

NoticeResponse 與 ParameterStatus 訊息可能穿插在 CopyData 訊息之間；前端必須處理這些情況，也應該準備好處理其他非同步訊息類型（請參閱[第 54.2.7 節](protocol-flow.md#PROTOCOL-ASYNC)）。除此之外，CopyData 或 CopyDone 以外的任何訊息類型都可以視為複製輸出模式的結束。

還有另一種與複製相關的模式，稱為雙向複製（copy-both），它可以*雙向*（往返伺服器）進行高速的大量資料傳輸。當處於 walsender 模式的後端執行 `START_REPLICATION` 陳述式時，就會開始雙向複製模式。後端會傳送 CopyBothResponse 訊息給前端。接著，後端與前端都可以傳送 CopyData 訊息，直到其中一端傳送 CopyDone 訊息為止。用戶端傳送 CopyDone 訊息之後，連線會從雙向複製模式轉為複製輸出模式，而用戶端不可以再傳送任何 CopyData 訊息。同樣地，當伺服器傳送 CopyDone 訊息時，連線會轉為複製輸入模式，而伺服器不可以再傳送任何 CopyData 訊息。雙方都傳送了 CopyDone 訊息之後，複製模式即結束，後端會回到命令處理模式。若後端在雙向複製模式期間偵測到錯誤，後端會發出 ErrorResponse 訊息，丟棄前端訊息直到收到 Sync 訊息為止，然後發出 ReadyForQuery 並回到正常處理。前端應該將收到 ErrorResponse 視為兩個方向的複製都已結束；這種情況下不應該傳送 CopyDone。關於透過雙向複製模式傳輸的子協定，詳細資訊請參閱[第 54.4 節](protocol-replication.md)。

CopyInResponse、CopyOutResponse 與 CopyBothResponse 訊息包含一些欄位，告知前端每個資料列的欄位數，以及每個欄位所使用的格式代碼。（就目前的實作而言，一次 `COPY` 操作中的所有欄位都會使用相同的格式，但訊息的設計並不假設這一點。）

<a id="PROTOCOL-ASYNC"></a>

### 54.2.7. 非同步操作 [#](#PROTOCOL-ASYNC)

在某些情況下，後端會傳送並非由前端命令串流特別引發的訊息。前端必須隨時準備好處理這些訊息，即使沒有在進行查詢時也一樣。至少，在開始讀取查詢回應之前，應該先檢查這些情況。

NoticeResponse 訊息可能因外部活動而產生；例如，若資料庫管理者下令「快速」關閉資料庫，後端會在關閉連線之前傳送一則 NoticeResponse 來表示這件事。因此，即使連線名義上處於閒置狀態，前端也應該隨時準備好接受並顯示 NoticeResponse 訊息。

只要後端認為前端應該知道的任何參數其有效值發生變化，就會產生 ParameterStatus 訊息。最常見的情況是回應前端所執行的 `SET` SQL 命令，這種情況實際上是同步的——但參數狀態也可能因為管理者修改了設定檔，然後向伺服器傳送 SIGHUP 訊號而改變。此外，若 `SET` 命令被回復，也會產生適當的 ParameterStatus 訊息，以回報目前的有效值。

目前，會產生 ParameterStatus 的參數是一組寫死的集合，包括：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="varname">application_name</code></td><td><code class="varname">scram_iterations</code></td></tr><tr><td><code class="varname">client_encoding</code></td><td><code class="varname">search_path</code></td></tr><tr><td><code class="varname">DateStyle</code></td><td><code class="varname">server_encoding</code></td></tr><tr><td><code class="varname">default_transaction_read_only</code></td><td><code class="varname">server_version</code></td></tr><tr><td><code class="varname">in_hot_standby</code></td><td><code class="varname">session_authorization</code></td></tr><tr><td><code class="varname">integer_datetimes</code></td><td><code class="varname">standard_conforming_strings</code></td></tr><tr><td><code class="varname">IntervalStyle</code></td><td><code class="varname">TimeZone</code></td></tr><tr><td><code class="varname">is_superuser</code></td><td> </td></tr></table>

（14 版之前的版本不會回報 `default_transaction_read_only` 與 `in_hot_standby`；16 版之前的版本不會回報 `scram_iterations`；18 版之前的版本不會回報 `search_path`。）請注意，`server_version`、`server_encoding` 與 `integer_datetimes` 是啟動後就不能改變的虛擬參數。這個集合在未來可能會改變，甚至可能變成可設定的。因此，前端對於它不理解或不在意的參數，應該直接忽略其 ParameterStatus。

若前端發出 `LISTEN` 命令，那麼只要有針對相同通道名稱執行的 `NOTIFY` 命令，後端就會傳送 NotificationResponse 訊息（不要與 NoticeResponse 混淆！）。

### 注意

目前，NotificationResponse 只能在交易之外傳送，因此它不會出現在命令與回應系列的中途，但可能會在 ReadyForQuery 之前出現。不過，設計前端邏輯時假設這一點並不明智。良好的做法是能夠在協定中的任何時間點接受 NotificationResponse。

<a id="PROTOCOL-FLOW-CANCELING-REQUESTS"></a>

### 54.2.8. 取消進行中的請求 [#](#PROTOCOL-FLOW-CANCELING-REQUESTS)

在查詢處理期間，前端可能會請求取消該查詢。基於實作效率的考量，取消請求不會直接在與後端已開啟的連線上傳送：我們不希望後端在查詢處理期間持續檢查是否有來自前端的新輸入。取消請求應該相對不常發生，因此我們讓它稍微麻煩一些，以避免在正常情況下付出代價。

要發出取消請求，前端會開啟一條連往伺服器的新連線，並傳送 CancelRequest 訊息，而不是一般在新連線上會傳送的 StartupMessage 訊息。伺服器會處理此請求，然後關閉連線。基於安全考量，不會對取消請求訊息做出直接回覆。

除非 CancelRequest 訊息包含與連線啟動期間傳給前端的相同金鑰資料（PID 與祕密金鑰），否則該訊息會被忽略。若請求與目前正在執行的後端的 PID 與祕密金鑰相符，目前查詢的處理就會被中止。（在現有的實作中，這是藉由向正在處理該查詢的後端程序傳送特殊訊號來完成的。）

取消訊號不一定會有任何效果——例如，若它在後端已經完成查詢處理之後才抵達，就不會有任何效果。若取消有效，會使目前的命令提早終止，並產生錯誤訊息。

這一切的結果是，基於安全與效率兩方面的考量，前端沒有直接的方法可以得知取消請求是否成功。它必須繼續等待後端對查詢做出回應。發出取消只是提高目前查詢很快結束的機率，並提高它以錯誤訊息失敗而不是成功的機率。

由於取消請求是透過連往伺服器的新連線傳送，而不是透過一般的前端／後端通訊連結傳送，因此任何程序都可以發出取消請求，而不只是查詢要被取消的那個前端。在建構多程序應用程式時，這可能提供額外的彈性。但它也帶來安全風險，因為未經授權的人可能會試圖取消查詢。這項安全風險的解決方式，是要求取消請求必須提供一個動態產生的祕密金鑰。

<a id="PROTOCOL-FLOW-TERMINATION"></a>

### 54.2.9. 終止 [#](#PROTOCOL-FLOW-TERMINATION)

正常而得體的終止程序是：前端傳送 Terminate 訊息，並立即關閉連線。收到此訊息後，後端會關閉連線並終止。

在少數情況下（例如管理者下令關閉資料庫），後端可能在前端沒有提出任何請求的情況下中斷連線。在這種情況下，後端會在關閉連線之前，嘗試傳送一則說明中斷原因的錯誤或通知訊息。

其他終止情境來自各種失敗情況，例如某一端發生核心傾印（core dump）、通訊連結中斷、失去訊息邊界同步等。若前端或後端任一方發現連線意外關閉，就應該進行清理並終止。若前端不想終止自己，可以選擇重新聯繫伺服器以啟動新的後端。若收到無法辨識的訊息類型，也建議關閉連線，因為這可能表示已失去訊息邊界同步。

無論是正常或異常終止，任何未結束的交易都會被回復，而不會被提交。不過應該注意，若前端在非 `SELECT` 查詢處理期間中斷連線，後端很可能會在察覺連線中斷之前完成該查詢。若該查詢不在任何交易區塊（`BEGIN` ... `COMMIT` 序列）之內，它的結果可能會在察覺連線中斷之前就被提交。

<a id="PROTOCOL-FLOW-SSL"></a>

### 54.2.10. SSL 工作階段加密 [#](#PROTOCOL-FLOW-SSL)

若 PostgreSQL 建置時含有 SSL 支援，前端／後端之間的通訊就可以使用 SSL 加密。這可以在攻擊者可能擷取工作階段流量的環境中提供通訊安全。關於以 SSL 加密 PostgreSQL 工作階段的更多資訊，請參閱[第 18.9 節](../../server-administration/runtime/ssl-tcp.md)。

要啟動 SSL 加密連線，前端一開始會傳送 SSLRequest 訊息，而不是 StartupMessage。接著，伺服器會回應一個包含 `S` 或 `N` 的單一位元組，分別表示它願意或不願意進行 SSL。若前端對回應不滿意，可以在此時關閉連線。要在收到 `S` 之後繼續，請與伺服器進行 SSL 啟動交握（此處不加說明，屬於 SSL 規格的一部分）。若成功，就繼續傳送一般的 StartupMessage。在這種情況下，StartupMessage 以及所有後續資料都會以 SSL 加密。要在收到 `N` 之後繼續，請傳送一般的 StartupMessage，並在不加密的情況下繼續進行。（或者，也可以在收到 `N` 回應之後發出 GSSENCRequest 訊息，嘗試改用 GSSAPI 加密而非 SSL。）

前端也應該準備好處理伺服器對 SSLRequest 的 ErrorMessage 回應。前端不應該將此錯誤訊息顯示給使用者／應用程式，因為伺服器尚未經過認證（[CVE-2024-10977](https://www.postgresql.org/support/security/CVE-2024-10977/)）。在這種情況下，必須關閉連線，但前端可以選擇開啟一條新的連線，並在不請求 SSL 的情況下繼續進行。

當可以進行 SSL 加密時，伺服器應該只傳送單一的 `S` 位元組，然後等待前端啟動 SSL 交握。若此時還有額外的位元組可以讀取，很可能表示有中間人正在嘗試進行緩衝區填塞攻擊（[CVE-2021-23222](https://www.postgresql.org/support/security/CVE-2021-23222/)）。前端程式應該撰寫成：在將通訊端（socket）交給其 SSL 函式庫之前，從通訊端中恰好讀取一個位元組；或者，若發現自己讀到了額外的位元組，就將其視為違反協定。

同樣地，伺服器預期用戶端在收到伺服器對 SSL 請求的單一位元組回應之前，不會開始 SSL 協商。若用戶端不等待收到伺服器回應就立即開始 SSL 協商，可以減少一次往返的連線延遲。然而，這樣做的代價是無法處理伺服器對 SSL 請求傳送否定回應的情況。在那種情況下，伺服器不會繼續使用 GSSAPI 或未加密連線，也不會回報協定錯誤，而是直接中斷連線。

在為了傳送 CancelRequest 訊息而開啟的連線中，也可以先使用 SSLRequest。

還有第二種啟動 SSL 加密的替代方式。伺服器會辨識那些不先傳送任何 SSLRequest 封包、而立即開始 SSL 協商的連線。一旦 SSL 連線建立，伺服器會預期收到一般的啟動請求封包，並在加密通道上繼續協商。在這種情況下，任何其他的加密請求都會被拒絕。對於一般用途的工具而言，不建議使用這種方式，因為它無法協商可用的最佳連線加密方式，也無法處理未加密的連線。不過，在伺服器與用戶端由同一方共同控管的環境中，這種方式很有用。在那種情況下，它可以省去一次往返的延遲，並允許使用依賴標準 SSL 連線的網路工具。以這種方式使用 SSL 連線時，用戶端必須使用 [RFC 7301](https://tools.ietf.org/html/rfc7301) 所定義的 ALPN 擴充，以防範協定混淆攻擊。PostgreSQL 協定在 [IANA
TLS ALPN Protocol IDs](https://www.iana.org/assignments/tls-extensiontype-values/tls-extensiontype-values.xhtml#alpn-protocol-ids) 登錄表中註冊的名稱是 "postgresql"。

雖然協定本身並未提供讓伺服器強制使用 SSL 加密的方法，但管理者可以將伺服器設定為拒絕未加密的工作階段，作為認證檢查的附帶效果。

<a id="PROTOCOL-FLOW-GSSAPI"></a>

### 54.2.11. GSSAPI 工作階段加密 [#](#PROTOCOL-FLOW-GSSAPI)

若 PostgreSQL 建置時含有 GSSAPI 支援，前端／後端之間的通訊就可以使用 GSSAPI 加密。這可以在攻擊者可能擷取工作階段流量的環境中提供通訊安全。關於以 GSSAPI 加密 PostgreSQL 工作階段的更多資訊，請參閱[第 18.10 節](../../server-administration/runtime/gssapi-enc.md)。

要啟動 GSSAPI 加密連線，前端一開始會傳送 GSSENCRequest 訊息，而不是 StartupMessage。接著，伺服器會回應一個包含 `G` 或 `N` 的單一位元組，分別表示它願意或不願意進行 GSSAPI 加密。若前端對回應不滿意，可以在此時關閉連線。要在收到 `G` 之後繼續，請使用 [RFC 2744](https://datatracker.ietf.org/doc/html/rfc2744) 所述的 GSSAPI C 繫結或同等機制進行 GSSAPI 初始化：在迴圈中呼叫 `gss_init_sec_context()` 並將結果傳送給伺服器，一開始使用空的輸入，之後依序使用伺服器傳來的每個結果，直到它不再傳回任何輸出為止。將 `gss_init_sec_context()` 的結果傳送給伺服器時，要在前面加上以網路位元組順序表示的四位元組整數訊息長度。要在收到 `N` 之後繼續，請傳送一般的 StartupMessage，並在不加密的情況下繼續進行。（或者，也可以在收到 `N` 回應之後發出 SSLRequest 訊息，嘗試改用 SSL 加密而非 GSSAPI。）

前端也應該準備好處理伺服器對 GSSENCRequest 的 ErrorMessage 回應。前端不應該將此錯誤訊息顯示給使用者／應用程式，因為伺服器尚未經過認證（[CVE-2024-10977](https://www.postgresql.org/support/security/CVE-2024-10977/)）。在這種情況下，必須關閉連線，但前端可以選擇開啟一條新的連線，並在不請求 GSSAPI 加密的情況下繼續進行。

當可以進行 GSSAPI 加密時，伺服器應該只傳送單一的 `G` 位元組，然後等待前端啟動 GSSAPI 交握。若此時還有額外的位元組可以讀取，很可能表示有中間人正在嘗試進行緩衝區填塞攻擊（[CVE-2021-23222](https://www.postgresql.org/support/security/CVE-2021-23222/)）。前端程式應該撰寫成：在將通訊端（socket）交給其 GSSAPI 函式庫之前，從通訊端中恰好讀取一個位元組；或者，若發現自己讀到了額外的位元組，就將其視為違反協定。

在為了傳送 CancelRequest 訊息而開啟的連線中，也可以先使用 GSSENCRequest。

GSSAPI 加密成功建立之後，請使用 `gss_wrap()` 加密一般的 StartupMessage 以及所有後續資料，並在實際的加密酬載前面加上以網路位元組順序表示的四位元組整數，作為 `gss_wrap()` 結果的長度。請注意，伺服器只會接受用戶端傳來小於 16kB 的加密封包；用戶端應該使用 `gss_wrap_size_limit()` 來決定能符合此限制的未加密訊息大小，較大的訊息應該拆成多次 `gss_wrap()` 呼叫。典型的區段是 8kB 的未加密資料，產生的加密封包會略大於 8kB，但遠低於 16kB 的上限。可以預期伺服器不會傳送大於 16kB 的加密封包給用戶端。

雖然協定本身並未提供讓伺服器強制使用 GSSAPI 加密的方法，但管理者可以將伺服器設定為拒絕未加密的工作階段，作為認證檢查的附帶效果。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-flow.html)（原文版本：18.6；核對日期：2026-10-12）
