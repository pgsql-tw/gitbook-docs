<a id="PROTOCOL-MESSAGE-FORMATS"></a>

## 54.7. 訊息格式 [#](#protocol-message-formats) <a href="#protocol-message-formats" id="protocol-message-formats"></a>

本節說明每種訊息的詳細格式。每種訊息都有標示，指出它可由前端 (F)、後端 (B) 或兩者 (F & B) 傳送。請注意，雖然每則訊息的開頭都包含位元組計數，但大多數訊息的定義方式，都讓人不必參考該位元組計數就能找到訊息結尾。這是出於歷史因素：原本、如今已淘汰的協定第 2 版並沒有明確的長度欄位。不過，這也有助於有效性檢查。

<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONOK"></a>

AuthenticationOk (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONOK)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(0)
    :   指定驗證已成功。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONKERBEROSV5"></a>

AuthenticationKerberosV5 (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONKERBEROSV5)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(2)
    :   指定需要 Kerberos V5 驗證。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONCLEARTEXTPASSWORD"></a>

AuthenticationCleartextPassword (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONCLEARTEXTPASSWORD)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(3)
    :   指定需要明文密碼。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONMD5PASSWORD"></a>

AuthenticationMD5Password (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONMD5PASSWORD)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(12)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(5)
    :   指定需要以 MD5 加密的密碼。

    Byte4
    :   加密密碼時所使用的鹽值（salt）。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSS"></a>

AuthenticationGSS (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSS)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(7)
    :   指定需要 GSSAPI 驗證。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSSCONTINUE"></a>

AuthenticationGSSContinue (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSSCONTINUE)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(8)
    :   指定此訊息包含 GSSAPI 或 SSPI 資料。

    Byte*`n`*
    :   GSSAPI 或 SSPI 驗證資料。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSSPI"></a>

AuthenticationSSPI (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSSPI)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(9)
    :   指定需要 SSPI 驗證。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASL"></a>

AuthenticationSASL (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASL)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(10)
    :   指定需要 SASL 驗證。

    訊息本體是 SASL 驗證機制的清單，依伺服器的偏好順序排列。最後一個驗證機制名稱之後必須有一個零位元組作為結束符。每個機制各有以下內容：

    String
    :   SASL 驗證機制的名稱。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLCONTINUE"></a>

AuthenticationSASLContinue (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLCONTINUE)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(11)
    :   指定此訊息包含 SASL 挑戰（challenge）。

    Byte*`n`*
    :   SASL 資料，依所使用的 SASL 機制而定。
<a id="PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLFINAL"></a>

AuthenticationSASLFinal (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLFINAL)
:   Byte1('R')
    :   將此訊息識別為驗證請求。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(12)
    :   指定 SASL 驗證已完成。

    Byte*`n`*
    :   SASL 結果的「附加資料」（additional data），依所使用的 SASL 機制而定。
<a id="PROTOCOL-MESSAGE-FORMATS-BACKENDKEYDATA"></a>

BackendKeyData (B) [#](#PROTOCOL-MESSAGE-FORMATS-BACKENDKEYDATA)
:   Byte1('K')
    :   將此訊息識別為取消金鑰資料。若前端希望之後能夠發出 CancelRequest 訊息，就必須保存這些值。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32
    :   此後端的程序 ID。

    Byte*`n`*
    :   此後端的祕密金鑰。此欄位延伸至訊息結尾，其範圍由長度欄位指示。

        金鑰長度的最小值與最大值分別為 4 與 256 位元組。PostgreSQL 伺服器只會傳送最多 32 位元組的金鑰，但較大的上限讓未來的伺服器版本，以及連線池與其他中介軟體，都能使用更長的金鑰。一種可能的用途是以額外資訊擴增伺服器的金鑰。因此也鼓勵中介軟體不要用盡所有位元組，以因應多個中介軟體應用程式彼此層層疊加的情況，其中每一層都可能以額外資料包裝金鑰。

    在協定版本 3.2 之前，祕密金鑰的長度一律為 4 位元組。
<a id="PROTOCOL-MESSAGE-FORMATS-BIND"></a>

Bind (F) [#](#PROTOCOL-MESSAGE-FORMATS-BIND)
:   Byte1('B')
    :   將此訊息識別為 Bind 命令。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   目的 portal 的名稱（空字串表示選擇未命名的 portal）。

    String
    :   來源預備陳述式的名稱（空字串表示選擇未命名的預備陳述式）。

    Int16
    :   接下來的參數格式代碼數量（以下記為 *`C`*）。此值可以為零，表示沒有參數，或所有參數都使用預設格式（文字）；也可以為一，此時所指定的格式代碼會套用至所有參數；或者可以等於實際的參數數量。

    Int16[*`C`*]
    :   參數格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。

    Int16
    :   接下來的參數值數量（可能為零）。此數量必須與查詢所需的參數數量相符。

    接著，每個參數各會出現下列一對欄位：

    Int32
    :   參數值的長度，以位元組計（此計數不包含其本身）。可以為零。特殊情況下，-1 表示 NULL 參數值。在 NULL 的情況下，其後不會有值的位元組。

    Byte*`n`*
    :   參數的值，格式由對應的格式代碼指示。*`n`* 為上述長度。

    在最後一個參數之後，會出現下列欄位：

    Int16
    :   接下來的結果欄位格式代碼數量（以下記為 *`R`*）。此值可以為零，表示沒有結果欄位，或所有結果欄位都應使用預設格式（文字）；也可以為一，此時所指定的格式代碼會套用至所有結果欄位（若有的話）；或者可以等於查詢實際的結果欄位數量。

    Int16[*`R`*]
    :   結果欄位格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。
<a id="PROTOCOL-MESSAGE-FORMATS-BINDCOMPLETE"></a>

BindComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-BINDCOMPLETE)
:   Byte1('2')
    :   將此訊息識別為 Bind 完成指示。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-CANCELREQUEST"></a>

CancelRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-CANCELREQUEST)
:   Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(80877102)
    :   取消請求代碼。此值經過選定，使最高有效 16 位元包含 `1234`，最低有效 16 位元包含 `5678`。（為避免混淆，此代碼不得與任何協定版本號碼相同。）

    Int32
    :   目標後端的程序 ID。

    Byte*`n`*
    :   目標後端的祕密金鑰。此欄位延伸至訊息結尾，其範圍由長度欄位指示。金鑰長度上限為 256 位元組。

    在協定版本 3.2 之前，祕密金鑰的長度一律為 4 位元組。
<a id="PROTOCOL-MESSAGE-FORMATS-CLOSE"></a>

Close (F) [#](#PROTOCOL-MESSAGE-FORMATS-CLOSE)
:   Byte1('C')
    :   將此訊息識別為 Close 命令。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte1
    :   '`S`' 表示關閉預備陳述式；'`P`' 表示關閉 portal。

    String
    :   要關閉的預備陳述式或 portal 的名稱（空字串表示選擇未命名的預備陳述式或 portal）。
<a id="PROTOCOL-MESSAGE-FORMATS-CLOSECOMPLETE"></a>

CloseComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-CLOSECOMPLETE)
:   Byte1('3')
    :   將此訊息識別為 Close 完成指示。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-COMMANDCOMPLETE"></a>

CommandComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-COMMANDCOMPLETE)
:   Byte1('C')
    :   將此訊息識別為命令完成回應。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   命令標籤。通常是單一個字，用以識別完成的是哪一個 SQL 命令。

        對於 `INSERT` 命令，標籤為 `INSERT oid
        rows`，其中 *`rows`* 為插入的資料列數。過去在 *`rows`* 為 1 且目標資料表具有 OID 時，*`oid`* 是所插入資料列的物件 ID；但 OID 系統欄位已不再受支援，因此 *`oid`* 一律為 0。

        對於 `DELETE` 命令，標籤為 `DELETE rows`，其中 *`rows`* 為刪除的資料列數。

        對於 `UPDATE` 命令，標籤為 `UPDATE rows`，其中 *`rows`* 為更新的資料列數。

        對於 `MERGE` 命令，標籤為 `MERGE rows`，其中 *`rows`* 為插入、更新或刪除的資料列數。

        對於 `SELECT` 或 `CREATE TABLE AS` 命令，標籤為 `SELECT rows`，其中 *`rows`* 為擷取的資料列數。

        對於 `MOVE` 命令，標籤為 `MOVE rows`，其中 *`rows`* 為游標位置所移動的資料列數。

        對於 `FETCH` 命令，標籤為 `FETCH rows`，其中 *`rows`* 為從游標擷取的資料列數。

        對於 `COPY` 命令，標籤為 `COPY rows`，其中 *`rows`* 為複製的資料列數。（注意：資料列計數只出現在 PostgreSQL 8.2 及之後的版本。）
<a id="PROTOCOL-MESSAGE-FORMATS-COPYDATA"></a>

CopyData (F & B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYDATA)
:   Byte1('d')
    :   將此訊息識別為 `COPY` 資料。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte*`n`*
    :   構成 `COPY` 資料串流一部分的資料。後端傳送的訊息一律對應單一資料列，但前端傳送的訊息可能以任意方式切分資料串流。
<a id="PROTOCOL-MESSAGE-FORMATS-COPYDONE"></a>

CopyDone (F & B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYDONE)
:   Byte1('c')
    :   將此訊息識別為 `COPY` 完成指示。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-COPYFAIL"></a>

CopyFail (F) [#](#PROTOCOL-MESSAGE-FORMATS-COPYFAIL)
:   Byte1('f')
    :   將此訊息識別為 `COPY` 失敗指示。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   要回報為失敗原因的錯誤訊息。
<a id="PROTOCOL-MESSAGE-FORMATS-COPYINRESPONSE"></a>

CopyInResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYINRESPONSE)
:   Byte1('G')
    :   將此訊息識別為 Start Copy In 回應。前端此時必須傳送複製輸入（copy-in）資料（若尚未準備好，則傳送 CopyFail 訊息）。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int8
    :   0 表示整體 `COPY` 格式為文字格式（資料列以換行字元分隔、欄位以分隔字元分隔等）。1 表示整體複製格式為二進位格式（類似 DataRow 格式）。詳細資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。

    Int16
    :   要複製之資料中的欄位數（以下記為 *`N`*）。

    Int16[*`N`*]
    :   每個欄位要使用的格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。若整體複製格式為文字格式，則全部都必須為零。
<a id="PROTOCOL-MESSAGE-FORMATS-COPYOUTRESPONSE"></a>

CopyOutResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYOUTRESPONSE)
:   Byte1('H')
    :   將此訊息識別為 Start Copy Out 回應。此訊息之後會接著複製輸出（copy-out）資料。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int8
    :   0 表示整體 `COPY` 格式為文字格式（資料列以換行字元分隔、欄位以分隔字元分隔等）。1 表示整體複製格式為二進位格式（類似 DataRow 格式）。詳細資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。

    Int16
    :   要複製之資料中的欄位數（以下記為 *`N`*）。

    Int16[*`N`*]
    :   每個欄位要使用的格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。若整體複製格式為文字格式，則全部都必須為零。
<a id="PROTOCOL-MESSAGE-FORMATS-COPYBOTHRESPONSE"></a>

CopyBothResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYBOTHRESPONSE)
:   Byte1('W')
    :   將此訊息識別為 Start Copy Both 回應。此訊息僅用於串流複寫。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int8
    :   0 表示整體 `COPY` 格式為文字格式（資料列以換行字元分隔、欄位以分隔字元分隔等）。1 表示整體複製格式為二進位格式（類似 DataRow 格式）。詳細資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。

    Int16
    :   要複製之資料中的欄位數（以下記為 *`N`*）。

    Int16[*`N`*]
    :   每個欄位要使用的格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。若整體複製格式為文字格式，則全部都必須為零。
<a id="PROTOCOL-MESSAGE-FORMATS-DATAROW"></a>

DataRow (B) [#](#PROTOCOL-MESSAGE-FORMATS-DATAROW)
:   Byte1('D')
    :   將此訊息識別為一筆資料列。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int16
    :   接下來的欄位值數量（可能為零）。

    接著，每個欄位各會出現下列一對欄位：

    Int32
    :   欄位值的長度，以位元組計（此計數不包含其本身）。可以為零。特殊情況下，-1 表示 NULL 欄位值。在 NULL 的情況下，其後不會有值的位元組。

    Byte*`n`*
    :   欄位的值，格式由對應的格式代碼指示。*`n`* 為上述長度。
<a id="PROTOCOL-MESSAGE-FORMATS-DESCRIBE"></a>

Describe (F) [#](#PROTOCOL-MESSAGE-FORMATS-DESCRIBE)
:   Byte1('D')
    :   將此訊息識別為 Describe 命令。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte1
    :   '`S`' 表示描述預備陳述式；'`P`' 表示描述 portal。

    String
    :   要描述的預備陳述式或 portal 的名稱（空字串表示選擇未命名的預備陳述式或 portal）。
<a id="PROTOCOL-MESSAGE-FORMATS-EMPTYQUERYRESPONSE"></a>

EmptyQueryResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-EMPTYQUERYRESPONSE)
:   Byte1('I')
    :   將此訊息識別為對空查詢字串的回應。（此訊息取代 CommandComplete。）

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-ERRORRESPONSE"></a>

ErrorResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-ERRORRESPONSE)
:   Byte1('E')
    :   將此訊息識別為錯誤。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    訊息本體由一個或多個已識別的欄位組成，之後接著一個零位元組作為結束符。欄位可以依任意順序出現。每個欄位各有以下內容：

    Byte1
    :   識別欄位類型的代碼；若為零，表示這是訊息結束符，其後不接字串。目前已定義的欄位類型列於[第 54.8 節](protocol-error-fields.md)。由於未來可能新增更多欄位類型，前端應該默默忽略無法辨識類型的欄位。

    String
    :   欄位值。
<a id="PROTOCOL-MESSAGE-FORMATS-EXECUTE"></a>

Execute (F) [#](#PROTOCOL-MESSAGE-FORMATS-EXECUTE)
:   Byte1('E')
    :   將此訊息識別為 Execute 命令。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   要執行的 portal 名稱（空字串表示選擇未命名的 portal）。

    Int32
    :   若 portal 包含會傳回資料列的查詢，此為要傳回的資料列數上限（否則忽略）。零表示「無限制」。
<a id="PROTOCOL-MESSAGE-FORMATS-FLUSH"></a>

Flush (F) [#](#PROTOCOL-MESSAGE-FORMATS-FLUSH)
:   Byte1('H')
    :   將此訊息識別為 Flush 命令。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALL"></a>

FunctionCall (F) [#](#PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALL)
:   Byte1('F')
    :   將此訊息識別為函式呼叫。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32
    :   指定要呼叫之函式的物件 ID。

    Int16
    :   接下來的引數格式代碼數量（以下記為 *`C`*）。此值可以為零，表示沒有引數，或所有引數都使用預設格式（文字）；也可以為一，此時所指定的格式代碼會套用至所有引數；或者可以等於實際的引數數量。

    Int16[*`C`*]
    :   引數格式代碼。目前每個代碼都必須為零（文字）或一（二進位）。

    Int16
    :   指定提供給函式的引數數量。

    接著，每個引數各會出現下列一對欄位：

    Int32
    :   引數值的長度，以位元組計（此計數不包含其本身）。可以為零。特殊情況下，-1 表示 NULL 引數值。在 NULL 的情況下，其後不會有值的位元組。

    Byte*`n`*
    :   引數的值，格式由對應的格式代碼指示。*`n`* 為上述長度。

    在最後一個引數之後，會出現下列欄位：

    Int16
    :   函式結果的格式代碼。目前必須為零（文字）或一（二進位）。
<a id="PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALLRESPONSE"></a>

FunctionCallResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALLRESPONSE)
:   Byte1('V')
    :   將此訊息識別為函式呼叫結果。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32
    :   函式結果值的長度，以位元組計（此計數不包含其本身）。可以為零。特殊情況下，-1 表示 NULL 函式結果。在 NULL 的情況下，其後不會有值的位元組。

    Byte*`n`*
    :   函式結果的值，格式由對應的格式代碼指示。*`n`* 為上述長度。
<a id="PROTOCOL-MESSAGE-FORMATS-GSSENCREQUEST"></a>

GSSENCRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-GSSENCREQUEST)
:   Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(80877104)
    :   GSSAPI 加密請求代碼。此值經過選定，使最高有效 16 位元包含 `1234`，最低有效 16 位元包含 `5680`。（為避免混淆，此代碼不得與任何協定版本號碼相同。）
<a id="PROTOCOL-MESSAGE-FORMATS-GSSRESPONSE"></a>

GSSResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-GSSRESPONSE)
:   Byte1('p')
    :   將此訊息識別為 GSSAPI 或 SSPI 回應。請注意，這也用於 SASL 與密碼回應訊息。確切的訊息類型可由上下文推斷。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte*`n`*
    :   GSSAPI/SSPI 特定的訊息資料。
<a id="PROTOCOL-MESSAGE-FORMATS-NEGOTIATEPROTOCOLVERSION"></a>

NegotiateProtocolVersion (B) [#](#PROTOCOL-MESSAGE-FORMATS-NEGOTIATEPROTOCOLVERSION)
:   Byte1('v')
    :   將此訊息識別為協定版本協商訊息。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32
    :   對於用戶端所請求的主要協定版本，伺服器所支援的最新次要協定版本。

    Int32
    :   伺服器無法辨識的協定選項數量。

    接著，對於伺服器無法辨識的每個協定選項，各有以下內容：

    String
    :   選項名稱。
<a id="PROTOCOL-MESSAGE-FORMATS-NODATA"></a>

NoData (B) [#](#PROTOCOL-MESSAGE-FORMATS-NODATA)
:   Byte1('n')
    :   將此訊息識別為無資料指示。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-NOTICERESPONSE"></a>

NoticeResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-NOTICERESPONSE)
:   Byte1('N')
    :   將此訊息識別為提醒訊息（notice）。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    訊息本體由一個或多個已識別的欄位組成，之後接著一個零位元組作為結束符。欄位可以依任意順序出現。每個欄位各有以下內容：

    Byte1
    :   識別欄位類型的代碼；若為零，表示這是訊息結束符，其後不接字串。目前已定義的欄位類型列於[第 54.8 節](protocol-error-fields.md)。由於未來可能新增更多欄位類型，前端應該默默忽略無法辨識類型的欄位。

    String
    :   欄位值。
<a id="PROTOCOL-MESSAGE-FORMATS-NOTIFICATIONRESPONSE"></a>

NotificationResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-NOTIFICATIONRESPONSE)
:   Byte1('A')
    :   將此訊息識別為通知回應。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32
    :   發出通知之後端程序的程序 ID。

    String
    :   引發通知的頻道名稱。

    String
    :   由發出通知的程序所傳遞的「payload」字串。
<a id="PROTOCOL-MESSAGE-FORMATS-PARAMETERDESCRIPTION"></a>

ParameterDescription (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARAMETERDESCRIPTION)
:   Byte1('t')
    :   將此訊息識別為參數描述。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int16
    :   陳述式所使用的參數數量（可以為零）。

    接著，每個參數各有以下內容：

    Int32
    :   指定參數資料型別的物件 ID。
<a id="PROTOCOL-MESSAGE-FORMATS-PARAMETERSTATUS"></a>

ParameterStatus (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARAMETERSTATUS)
:   Byte1('S')
    :   將此訊息識別為執行期參數狀態報告。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   所回報之執行期參數的名稱。

    String
    :   參數的目前值。
<a id="PROTOCOL-MESSAGE-FORMATS-PARSE"></a>

Parse (F) [#](#PROTOCOL-MESSAGE-FORMATS-PARSE)
:   Byte1('P')
    :   將此訊息識別為 Parse 命令。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   目的預備陳述式的名稱（空字串表示選擇未命名的預備陳述式）。

    String
    :   要剖析的查詢字串。

    Int16
    :   指定的參數資料型別數量（可以為零）。請注意，這並不表示查詢字串中可能出現的參數數量，而只是前端想要預先指定型別的參數數量。

    接著，每個參數各有以下內容：

    Int32
    :   指定參數資料型別的物件 ID。在此放置零，等同於不指定型別。
<a id="PROTOCOL-MESSAGE-FORMATS-PARSECOMPLETE"></a>

ParseComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARSECOMPLETE)
:   Byte1('1')
    :   將此訊息識別為 Parse 完成指示。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-PASSWORDMESSAGE"></a>

PasswordMessage (F) [#](#PROTOCOL-MESSAGE-FORMATS-PASSWORDMESSAGE)
:   Byte1('p')
    :   將此訊息識別為密碼回應。請注意，這也用於 GSSAPI、SSPI 與 SASL 回應訊息。確切的訊息類型可由上下文推斷。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   密碼（若有要求，則經過加密）。
<a id="PROTOCOL-MESSAGE-FORMATS-PORTALSUSPENDED"></a>

PortalSuspended (B) [#](#PROTOCOL-MESSAGE-FORMATS-PORTALSUSPENDED)
:   Byte1('s')
    :   將此訊息識別為 portal 暫停指示。請注意，只有在達到 Execute 訊息的資料列數限制時，才會出現此訊息。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-QUERY"></a>

Query (F) [#](#PROTOCOL-MESSAGE-FORMATS-QUERY)
:   Byte1('Q')
    :   將此訊息識別為簡單查詢。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   查詢字串本身。
<a id="PROTOCOL-MESSAGE-FORMATS-READYFORQUERY"></a>

ReadyForQuery (B) [#](#PROTOCOL-MESSAGE-FORMATS-READYFORQUERY)
:   Byte1('Z')
    :   識別訊息類型。每當後端準備好進入新的查詢週期時，就會傳送 ReadyForQuery。

    Int32(5)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte1
    :   目前後端的交易狀態指示。可能的值為：閒置（不在交易區塊中）時為 '`I`'；在交易區塊中時為 '`T`'；在失敗的交易區塊中時為 '`E`'（在區塊結束之前，查詢都會被拒絕）。
<a id="PROTOCOL-MESSAGE-FORMATS-ROWDESCRIPTION"></a>

RowDescription (B) [#](#PROTOCOL-MESSAGE-FORMATS-ROWDESCRIPTION)
:   Byte1('T')
    :   將此訊息識別為資料列描述。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int16
    :   指定一筆資料列中的欄位數（可以為零）。

    接著，每個欄位各有以下內容：

    String
    :   欄位名稱。

    Int32
    :   若該欄位可識別為特定資料表的欄位，則為該資料表的物件 ID；否則為零。

    Int16
    :   若該欄位可識別為特定資料表的欄位，則為該欄位的屬性編號；否則為零。

    Int32
    :   該欄位資料型別的物件 ID。

    Int16
    :   資料型別的大小（請參閱 `pg_type.typlen`）。請注意，負值表示變動寬度的型別。

    Int32
    :   型別修飾詞（請參閱 `pg_attribute.atttypmod`）。修飾詞的意義依型別而定。

    Int16
    :   該欄位所使用的格式代碼。目前會是零（文字）或一（二進位）。在由 Describe 的陳述式變體所傳回的 RowDescription 中，格式代碼尚未得知，且一律為零。
<a id="PROTOCOL-MESSAGE-FORMATS-SASLINITIALRESPONSE"></a>

SASLInitialResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-SASLINITIALRESPONSE)
:   Byte1('p')
    :   將此訊息識別為初始 SASL 回應。請注意，這也用於 GSSAPI、SSPI 與密碼回應訊息。確切的訊息類型由上下文推斷。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    String
    :   用戶端所選擇之 SASL 驗證機制的名稱。

    Int32
    :   其後 SASL 機制特定之 "Initial Client Response"（初始用戶端回應）的長度；若沒有 Initial Response，則為 -1。

    Byte*`n`*
    :   SASL 機制特定的 "Initial Response"（初始回應）。
<a id="PROTOCOL-MESSAGE-FORMATS-SASLRESPONSE"></a>

SASLResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-SASLRESPONSE)
:   Byte1('p')
    :   將此訊息識別為 SASL 回應。請注意，這也用於 GSSAPI、SSPI 與密碼回應訊息。確切的訊息類型可由上下文推斷。

    Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Byte*`n`*
    :   SASL 機制特定的訊息資料。
<a id="PROTOCOL-MESSAGE-FORMATS-SSLREQUEST"></a>

SSLRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-SSLREQUEST)
:   Int32(8)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(80877103)
    :   SSL 請求代碼。此值經過選定，使最高有效 16 位元包含 `1234`，最低有效 16 位元包含 `5679`。（為避免混淆，此代碼不得與任何協定版本號碼相同。）
<a id="PROTOCOL-MESSAGE-FORMATS-STARTUPMESSAGE"></a>

StartupMessage (F) [#](#PROTOCOL-MESSAGE-FORMATS-STARTUPMESSAGE)
:   Int32
    :   訊息內容的長度，以位元組計，包含此欄位本身。

    Int32(196610)
    :   協定版本號碼。最高有效 16 位元為主要版本號碼（此處所述的協定為 3）。最低有效 16 位元為次要版本號碼（此處所述的協定為 2）。

    協定版本號碼之後接著一對或多對參數名稱與值字串。最後一對名稱／值之後必須有一個零位元組作為結束符。參數可以依任意順序出現。`user` 為必要參數，其他則為選擇性。每個參數的指定方式如下：

    String
    :   參數名稱。目前可辨識的名稱有：

        `user`
        :   用以連線的資料庫使用者名稱。此參數為必要；沒有預設值。

        `database`
        :   要連線的資料庫。預設為使用者名稱。

        `options`
        :   後端的命令列引數。（此方式已棄用，建議改為設定個別的執行期參數。）此字串中的空白會被視為引數分隔，除非以反斜線（`\`）跳脫；寫成 `\\` 可表示字面上的反斜線。

        `replication`
        :   用於以串流複寫模式連線，在此模式下可以發出一小組複寫命令，而非 SQL 陳述式。值可以是 `true`、`false` 或 `database`，預設為 `false`。詳細資訊請參閱[第 54.4 節](protocol-replication.md)。

        除了上述參數之外，也可以列出其他參數。以 `_pq_.` 開頭的參數名稱保留供協定擴充使用，其他參數則會被視為在後端啟動時要設定的執行期參數。這些設定會在後端啟動期間套用（若有命令列引數，則在剖析命令列引數之後），並作為工作階段的預設值。

    String
    :   參數值。
<a id="PROTOCOL-MESSAGE-FORMATS-SYNC"></a>

Sync (F) [#](#PROTOCOL-MESSAGE-FORMATS-SYNC)
:   Byte1('S')
    :   將此訊息識別為 Sync 命令。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。
<a id="PROTOCOL-MESSAGE-FORMATS-TERMINATE"></a>

Terminate (F) [#](#PROTOCOL-MESSAGE-FORMATS-TERMINATE)
:   Byte1('X')
    :   將此訊息識別為終止訊息。

    Int32(4)
    :   訊息內容的長度，以位元組計，包含此欄位本身。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-message-formats.html)（原文版本：18.6；核對日期：2026-10-12）
