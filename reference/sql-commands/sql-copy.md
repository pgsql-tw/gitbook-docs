<a id="SQL-COPY"></a><a id="id-1.9.3.55.1"></a>

## COPY

COPY — 在檔案與資料表之間複製資料

<a id="id-1.9.3.55.4"></a>

## 語法

```

COPY table_name [ ( column_name [, ...] ) ]
    FROM { 'filename' | PROGRAM 'command' | STDIN }
    [ [ WITH ] ( option [, ...] ) ]
    [ WHERE condition ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) }
    TO { 'filename' | PROGRAM 'command' | STDOUT }
    [ [ WITH ] ( option [, ...] ) ]

where option can be one of:

    FORMAT format_name
    FREEZE [ boolean ]
    DELIMITER 'delimiter_character'
    NULL 'null_string'
    DEFAULT 'default_string'
    HEADER [ boolean | MATCH ]
    QUOTE 'quote_character'
    ESCAPE 'escape_character'
    FORCE_QUOTE { ( column_name [, ...] ) | * }
    FORCE_NOT_NULL { ( column_name [, ...] ) | * }
    FORCE_NULL { ( column_name [, ...] ) | * }
    ON_ERROR error_action
    REJECT_LIMIT maxerror
    ENCODING 'encoding_name'
    LOG_VERBOSITY verbosity
```

<a id="id-1.9.3.55.5"></a>

## 說明

`COPY` 在
PostgreSQL 資料表與標準檔案系統的
檔案之間搬移資料。`COPY TO` 會把資料表的內容複製
*到*檔案中，而 `COPY FROM` 則會把資料
*從*檔案複製到資料表中（將資料附加到
資料表中已有的內容之後）。`COPY TO`
也可以複製 `SELECT` 查詢的結果。

若指定了欄位清單，`COPY TO` 只會把
指定欄位中的資料複製到檔案。對於 `COPY
FROM`，檔案中的每個欄位值會依序插入
指定的欄位中。未在 `COPY
FROM` 欄位清單中指定的資料表欄位，將會取得其預設值。

帶有檔案名稱的 `COPY` 會指示
PostgreSQL 伺服器直接讀取
或寫入檔案。該檔案必須能讓
PostgreSQL 使用者（伺服器
執行時所用的使用者 ID）存取，而且名稱必須從
伺服器的角度來指定。指定 `PROGRAM` 時，伺服器
會執行給定的命令，並從該程式的標準輸出讀取，
或寫入該程式的標準輸入。該命令
必須從伺服器的角度來指定，且必須能讓
PostgreSQL 使用者執行。指定
`STDIN` 或 `STDOUT` 時，
資料會透過用戶端與伺服器之間的連線傳輸。

每個執行 `COPY` 的後端都會在
`pg_stat_progress_copy` 檢視表中回報其進度。詳情請參閱
[第 27.4.3 節](../../server-administration/monitoring/progress-reporting.md#copy-progress-reporting)。

預設情況下，若 `COPY` 在處理過程中遇到錯誤，
就會失敗。對於希望盡力載入
整個檔案的使用情境，可以使用 `ON_ERROR` 子句
來指定其他行為。

<a id="id-1.9.3.55.6"></a>

## 參數

*`table_name`*
:   現有資料表的名稱（可選擇以綱要限定）。

*`column_name`*
:   選用的要複製的欄位清單。若未指定
    欄位清單，則會複製資料表中除了產生欄位以外的所有欄位。

*`query`*
:   一個 [`SELECT`](sql-select.md)、
    [`VALUES`](sql-values.md)、
    [`INSERT`](sql-insert.md)、
    [`UPDATE`](sql-update.md)、
    [`DELETE`](sql-delete.md) 或
    [`MERGE`](sql-merge.md) 命令，
    其結果將被複製。請注意，查詢的前後必須
    加上括號。

    對於 `INSERT`、`UPDATE`、
    `DELETE` 與 `MERGE` 查詢，必須提供
    `RETURNING` 子句，而且目標
    關聯不得有條件式規則，也不得有
    `ALSO` 規則，也不得有會展開成多個陳述式的
    `INSTEAD` 規則。

*`filename`*
:   輸入或輸出檔案的路徑名稱。輸入檔案名稱可以是
    絕對或相對路徑，但輸出檔案名稱必須是絕對
    路徑。Windows 使用者可能需要使用 `E''` 字串，並將
    路徑名稱中使用的所有反斜線加倍。

`PROGRAM`

要執行的命令。在 `COPY FROM` 中，輸入是
從該命令的標準輸出讀取；在 `COPY TO` 中，
輸出則會寫入該命令的標準輸入。

請注意，該命令是由 shell 呼叫的，因此若你需要傳遞
任何來自不受信任來源的引數，就
必須小心移除或跳脫任何可能
對 shell 具有特殊意義的特殊字元。基於安全理由，最好
使用固定的命令字串，或者至少避免在其中包含任何使用者輸入。

`STDIN`
:   指定輸入來自用戶端應用程式。

`STDOUT`
:   指定輸出送往用戶端應用程式。

*`boolean`*
:   指定所選的選項應該開啟還是關閉。
    你可以寫 `TRUE`、`ON` 或
    `1` 來啟用該選項，寫 `FALSE`、
    `OFF` 或 `0` 來停用它。
    *`boolean`* 值也可以
    省略，此時視為 `TRUE`。

`FORMAT`
:   選擇要讀取或寫入的資料格式：
    `text`、
    `csv`（逗號分隔值，Comma Separated Values）
    或 `binary`。
    預設為 `text`。
    詳情請參閱下方的[檔案格式](sql-copy.md#SQL-COPY-FILE-FORMATS)。

`FREEZE`

要求以資料列已凍結的狀態複製資料，就如同
執行 `VACUUM FREEZE` 命令之後的狀態一樣。
這是作為初始資料載入的效能選項。
只有當被載入的資料表是在目前的子交易中建立
或截斷、沒有開啟的游標，
且此交易沒有持有較舊的快照時，資料列才會被凍結。
目前無法對
分割資料表或外部資料表執行 `COPY FREEZE`。
此選項只允許用於 `COPY FROM`。

請注意，一旦資料成功載入，所有其他工作階段都會立即能看到這些資料。
這違反了 MVCC 可見性的一般規則，使用者應該留意
這可能造成的潛在問題。

`DELIMITER`
:   指定在檔案的每一資料列（行）中分隔欄位的字元。
    在文字格式中預設為 tab 字元，
    在 `CSV` 格式中預設為逗號。
    這必須是單一個單位元組字元。
    使用 `binary` 格式時不允許此選項。

`NULL`
:   指定代表空值的字串。在文字格式中預設為
    `\N`（反斜線-N），在 `CSV` 格式中則為未加引號的空
    字串。若你不想
    區分空值與空字串，即使在文字格式中，你可能也會偏好使用空字串。
    使用 `binary` 格式時不允許此選項。

    <a id="id-1.9.3.55.6.2.12.2.2"></a>

    ### 注意

    使用 `COPY FROM` 時，任何與
    此字串相符的資料項目都會被儲存為空值，因此你應該
    確定使用的字串與你在
    `COPY TO` 中使用的字串相同。

`DEFAULT`
:   指定代表預設值的字串。每當在輸入檔案中找到該字串時，
    就會使用對應欄位的預設值。
    此選項只允許用於 `COPY FROM`，且只有在
    不使用 `binary` 格式時才允許。

`HEADER`
:   指定檔案包含一個標頭行，內有檔案中每個
    欄位的名稱。輸出時，第一行包含資料表的欄位
    名稱。輸入時，若此
    選項設為 `true`（或等效的布林值），第一行會被捨棄。
    若此選項設為 `MATCH`，則標頭行中欄位的數量與名稱
    必須依序與資料表實際的欄位名稱
    相符；否則會引發錯誤。
    使用 `binary` 格式時不允許此選項。
    `MATCH` 選項只對 `COPY
    FROM` 命令有效。

`QUOTE`
:   指定當資料值加上引號時所使用的引號字元。
    預設為雙引號。
    這必須是單一個單位元組字元。
    此選項只允許在使用 `CSV` 格式時使用。

`ESCAPE`
:   指定應該出現在與 `QUOTE` 值相符的
    資料字元之前的字元。
    預設與 `QUOTE` 值相同（因此
    若引號字元出現在資料中，會被重複兩次）。
    這必須是單一個單位元組字元。
    此選項只允許在使用 `CSV` 格式時使用。

`FORCE_QUOTE`
:   強制對每個指定欄位中所有非 `NULL` 的值
    加上引號。
    `NULL` 輸出永遠不會加上引號。若指定了 `*`，
    則所有欄位中非 `NULL` 的值都會加上引號。
    此選項只允許用於 `COPY TO`，且只有在
    使用 `CSV` 格式時才允許。

`FORCE_NOT_NULL`
:   不將指定欄位的值與空值字串進行比對。
    在空值字串為空的預設情況下，這表示
    空的值會被讀取為長度為零的字串，而不是空值，
    即使它們沒有加上引號也一樣。
    若指定了 `*`，此選項將套用至所有欄位。
    此選項只允許用於 `COPY FROM`，且只有在
    使用 `CSV` 格式時才允許。

`FORCE_NULL`
:   將指定欄位的值與空值字串進行比對，即使
    該值已加上引號也一樣；若找到相符者，就將該值設為
    `NULL`。在空值字串為空的預設情況下，
    這會將加上引號的空字串轉換為 NULL。
    若指定了 `*`，此選項將套用至所有欄位。
    此選項只允許用於 `COPY FROM`，且只有在
    使用 `CSV` 格式時才允許。

`ON_ERROR`

指定在將欄位的輸入值轉換為其資料型別時遇到錯誤時，
應如何處理。
*`error_action`* 值為
`stop` 表示讓命令失敗，而
`ignore` 表示捨棄該輸入資料列並繼續處理下一筆。
預設為 `stop`。

`ignore` 選項只適用於 `COPY FROM`，
且 `FORMAT` 為 `text` 或 `csv` 的情況。

若至少有一筆
資料列被捨棄，則會在 `COPY FROM` 結束時發出一則包含被忽略資料列數量的
`NOTICE` 訊息。當 `LOG_VERBOSITY` 選項設為
`verbose` 時，每一筆被捨棄的資料列都會發出一則 `NOTICE` 訊息，
其中包含輸入檔案中的該行，以及輸入
轉換失敗的欄位名稱。
當它設為 `silent` 時，不會發出任何
關於被忽略資料列的訊息。

`REJECT_LIMIT`
:   指定當 `ON_ERROR` 設為
    `ignore` 時，將欄位的輸入值轉換為其資料型別的過程中
    所容許的最大錯誤數。
    若輸入造成的錯誤超過指定的值，即使 `ON_ERROR` 設為 `ignore`，`COPY`
    命令仍會失敗。
    此子句必須與 `ON_ERROR`=`ignore` 一起使用，
    且 *`maxerror`* 必須是正的 `bigint`。
    若未指定，`ON_ERROR`=`ignore`
    會允許無限數量的錯誤，這表示 `COPY` 會
    略過所有錯誤的資料。

`ENCODING`
:   指定檔案是以 *`encoding_name`* 編碼。若省略此選項，
    則會使用目前的用戶端編碼。詳情請參閱下方的
    注意事項。

`LOG_VERBOSITY`
:   指定 `COPY`
    命令發出的訊息量：`default`、`verbose` 或
    `silent`。
    若指定了 `verbose`，則會在處理過程中發出
    額外的訊息。
    `silent` 會同時抑制詳細訊息與預設訊息。

    目前這用於 `COPY FROM` 命令中
    `ON_ERROR` 選項設為 `ignore` 的情況。

`WHERE`
:   選用的 `WHERE` 子句具有一般形式

    ```

    WHERE condition
    ```

    其中 *`condition`* 是
    任何求值結果為
    `boolean` 型別的運算式。任何不滿足此
    條件的資料列都不會被插入資料表。當以實際的資料列值
    代換任何變數參照後，若條件傳回 true，該資料列即滿足
    此條件。

    目前，`WHERE` 運算式中不允許使用子查詢與產生欄位，
    而且求值時不會看到
    `COPY` 本身所做的任何變更（當
    運算式包含對 `VOLATILE`
    函式的呼叫時，這一點很重要）。

<a id="id-1.9.3.55.7"></a>

## 輸出

成功完成時，`COPY` 命令會傳回下列形式的命令
標籤

```

COPY count
```

*`count`* 是
複製的資料列數。

<a id="id-1.9.3.55.7.5"></a>

### 注意

只有當命令
不是 `COPY ... TO STDOUT`，也不是
等效的 psql 元命令
`\copy ... to stdout` 時，psql 才會印出此命令標籤。這是為了避免把
命令標籤與剛印出的資料混淆。

<a id="id-1.9.3.55.8"></a>

## 注意事項

`COPY TO` 可用於一般
資料表以及已填入資料的具體化檢視表。
例如，
`COPY table
TO` 會複製與
`SELECT * FROM ONLY table` 相同的資料列。
不過，它並不直接支援其他關聯類型，
例如分割資料表、繼承子資料表或檢視表。
若要複製這類關聯的所有資料列，請使用 `COPY (SELECT * FROM
table) TO`。

`COPY FROM` 可用於一般資料表、外部資料表或
分割資料表，或是具有
`INSTEAD OF INSERT` 觸發程序的檢視表。

你必須對 `COPY TO` 讀取其值的資料表擁有 SELECT 權限，
並對 `COPY FROM` 插入值的資料表擁有
INSERT 權限。只要對命令中列出的欄位
擁有欄位權限就足夠了。

若資料表啟用了資料列層級安全性，則相關的
`SELECT` 政策將套用於 `COPY
table TO` 陳述式。
目前，對於啟用資料列層級安全性的資料表，不支援 `COPY FROM`。
請改用等效的 `INSERT`
陳述式。

`COPY` 命令中指名的檔案是由伺服器直接讀取或寫入，
而不是由用戶端應用程式。因此，
它們必須位於資料庫伺服器主機上，或能讓資料庫伺服器主機存取，
而不是用戶端。它們必須能讓
PostgreSQL 使用者（伺服器
執行時所用的使用者 ID）存取並讀取或寫入，而不是用戶端。同樣地，
以 `PROGRAM` 指定的命令是由伺服器直接執行，
而不是由用戶端應用程式，且必須能讓
PostgreSQL 使用者執行。
指名檔案或命令的 `COPY` 只允許
資料庫超級使用者，或被授予下列其中一個角色的使用者使用：
`pg_read_server_files`、
`pg_write_server_files`
或 `pg_execute_server_program`，因為它允許讀取
或寫入伺服器有權限存取的任何檔案，或執行伺服器有權限存取的任何程式。

不要將 `COPY` 與
psql 指令
`\copy` 混淆。`\copy` 會呼叫
`COPY FROM STDIN` 或 `COPY TO
STDOUT`，然後在
psql 用戶端可存取的檔案中擷取／儲存資料。因此，
使用 `\copy` 時，檔案的可存取性與存取權限取決於用戶端，而不是
伺服器。

建議 `COPY` 中使用的檔案名稱
一律指定為絕對路徑。在 `COPY TO` 的情況下，
伺服器會強制要求這一點，但對於
`COPY FROM`，你確實可以選擇從
以相對路徑指定的檔案讀取。該路徑將相對於
伺服器程序的工作目錄（通常是
叢集的資料目錄）來解讀，而不是用戶端的工作目錄。

以 `PROGRAM` 執行命令可能會受到
作業系統存取控制機制（例如 SELinux）的限制。

`COPY FROM` 會呼叫目標資料表上的任何觸發程序與檢查
限制條件。不過，它不會呼叫規則。

對於識別欄位，`COPY FROM` 命令一律會
寫入輸入資料中提供的欄位值，就像
`INSERT` 的 `OVERRIDING SYSTEM
VALUE` 選項一樣。

`COPY` 的輸入與輸出會受到
`DateStyle` 影響。為了確保能移植到其他
可能使用非預設 `DateStyle` 設定的
PostgreSQL 安裝，
使用 `COPY TO` 之前應該將 `DateStyle` 設為 `ISO`。
同樣建議避免在
`IntervalStyle` 設為
`sql_standard` 時傾印資料，因為負的時間間隔值可能會
被 `IntervalStyle` 設定不同的伺服器
誤解。

輸入資料會依照 `ENCODING`
選項或目前的用戶端編碼來解讀，而輸出資料則會以
`ENCODING` 或目前的用戶端編碼進行編碼，即使
資料並未經過用戶端，而是由伺服器直接從檔案讀取或寫入檔案也一樣。

`COPY FROM` 命令會在執行過程中，將輸入資料列實際插入
資料表。若命令失敗，這些資料列會
留在已刪除的狀態；這些資料列將不可見，但仍會
佔用磁碟空間。若失敗發生在大型複製
作業的相當後段，這可能會浪費可觀的
磁碟空間。應該使用 `VACUUM` 來回收
被浪費的空間。

`FORCE_NULL` 與 `FORCE_NOT_NULL` 可以
同時用於同一個欄位。這會將加上引號的
空值字串轉換為空值，並將未加引號的空值字串轉換為空字串。

<a id="SQL-COPY-FILE-FORMATS"></a>

## 檔案格式

<a id="SQL-COPY-TEXT-FORMAT"></a>

### 文字格式

使用 `text` 格式時，
讀取或寫入的資料是一個文字檔，每個資料表資料列一行。
資料列中的欄位以分隔字元分隔。
欄位值本身是由每個
屬性資料型別的輸出函式所產生的字串，或是其輸入函式可接受的字串。
為空值的欄位，會以指定的空值字串代替。
若輸入檔案的任何一行包含比預期更多或更少的欄位，
`COPY FROM` 就會引發錯誤。

資料結尾可以用只包含
反斜線-句點（`\.`）的一行來表示。從檔案讀取時，
並不需要資料結尾標記，因為檔案結尾
就完全足以達成此目的；在該情境下，這項規定只是為了
向後相容性而存在。不過，psql
會使用 `\.` 來結束 `COPY FROM
STDIN` 作業（也就是在 SQL 腳本中讀取
內嵌的 `COPY` 資料）。在該
情境下，需要這項規則才能在腳本結束之前
結束該作業。

反斜線字元（`\`）可以在
`COPY` 資料中用來引用那些
否則可能被當作資料列或欄位分隔符號的資料字元。特別是，
下列字元若作為欄位值的一部分出現，前面*必須*加上反斜線：
反斜線本身、
換行字元、歸位字元，以及目前的分隔字元。

`COPY TO` 送出指定的空值字串時，
不會加上任何反斜線；反過來說，`COPY FROM` 會在
移除反斜線之前，先將輸入與空值字串比對。因此，
像 `\N` 這樣的空值字串，不會與
實際的資料值 `\N`（其表示方式
為 `\\N`）混淆。

`COPY FROM` 能辨識下列特殊的反斜線序列：

<table border="1" class="informaltable"><colgroup><col/><col/></colgroup><thead><tr><th>序列</th><th>代表</th></tr></thead><tbody><tr><td><code class="literal">\b</code></td><td>退格（ASCII 8）</td></tr><tr><td><code class="literal">\f</code></td><td>換頁（ASCII 12）</td></tr><tr><td><code class="literal">\n</code></td><td>換行（ASCII 10）</td></tr><tr><td><code class="literal">\r</code></td><td>歸位（ASCII 13）</td></tr><tr><td><code class="literal">\t</code></td><td>Tab（ASCII 9）</td></tr><tr><td><code class="literal">\v</code></td><td>垂直 Tab（ASCII 11）</td></tr><tr><td><code class="literal">\</code><em class="replaceable"><code>digits</code></em></td><td>反斜線後接一到三個八進位數字，指定
       具有該數字代碼的位元組</td></tr><tr><td><code class="literal">\x</code><em class="replaceable"><code>digits</code></em></td><td>反斜線 <code class="literal">x</code> 後接一或兩個十六進位數字，指定
       具有該數字代碼的位元組</td></tr></tbody></table>

目前，`COPY TO` 永遠不會輸出八進位或
十六進位數字的反斜線序列，但對於那些控制字元，它確實會使用
上表列出的其他序列。

上表中未提及的任何其他加上反斜線的字元，
都會被視為代表其本身。不過，要注意不要
不必要地加上反斜線，因為這可能會意外產生與
資料結尾標記（`\.`）或空值字串（預設為 `\N`）相符的字串。
這些字串會在進行任何其他反斜線
處理之前就被辨識出來。

強烈建議產生 `COPY` 資料的應用程式，將
資料中的換行與歸位分別轉換為 `\n` 與
`\r` 序列。目前
可以用反斜線加歸位字元來表示資料中的歸位字元，
並用反斜線加換行字元來表示資料中的換行字元。
不過，這些表示方式在未來的版本中可能不被接受。
若 `COPY` 檔案在不同機器之間傳輸
（例如從 Unix 傳到 Windows，
或反之），它們也非常容易遭到損毀。

所有反斜線序列都是在編碼轉換之後才解讀。
以八進位與十六進位數字反斜線序列指定的位元組，必須
在資料庫編碼中構成有效的字元。

`COPY TO` 會以 Unix 風格的
換行字元（「`\n`」）結束每一資料列。在 Microsoft Windows 上執行的伺服器則改為
輸出歸位／換行（「`\r\n`」），但僅限於
`COPY` 到伺服器檔案的情況；為了跨平台的一致性，
無論伺服器平台為何，`COPY TO STDOUT` 一律送出「`\n`」。
`COPY FROM` 可以處理以換行、
歸位或歸位／換行結尾的行。為了降低
因未加反斜線、原本要作為資料的換行或歸位而造成錯誤的風險，
若輸入中的行尾不全都相同，`COPY FROM` 就會發出抱怨。

<a id="SQL-COPY-CSV-FORMAT"></a>

### CSV 格式

此格式選項用於匯入與匯出許多其他
程式（例如試算表）所使用的逗號
分隔值（`CSV`）檔案格式。它不使用
PostgreSQL 標準文字格式所用的跳脫規則，
而是產生並辨識常見的 `CSV` 跳脫機制。

每筆記錄中的值以 `DELIMITER`
字元分隔。若值包含分隔字元、
`QUOTE` 字元、`NULL` 字串、歸位字元
或換行字元，則整個值的前後都會加上
`QUOTE` 字元，而值中出現的任何
`QUOTE` 字元或
`ESCAPE` 字元，前面都會加上跳脫字元。
你也可以使用 `FORCE_QUOTE`，在輸出
特定欄位中非 `NULL` 的值時強制加上引號。

`CSV` 格式沒有標準的方式來區分
`NULL` 值與空字串。
PostgreSQL 的 `COPY` 以加引號的方式來處理這個問題。
`NULL` 會輸出為 `NULL` 參數字串，
且不加引號；而與
`NULL` 參數字串相符的非 `NULL` 值則會加上引號。例如，在
預設設定下，`NULL` 會寫成未加引號的空
字串，而空字串資料值則會以雙引號
（`""`）寫出。讀取值時也遵循類似的規則。你可以
使用 `FORCE_NOT_NULL`，防止特定欄位進行 `NULL` 輸入
比對。你也可以使用
`FORCE_NULL`，將加上引號的空值字串資料值轉換為
`NULL`。

由於反斜線在 `CSV`
格式中不是特殊字元，文字模式中使用的資料結尾標記（`\.`）
在讀取 `CSV`
資料時通常不會被視為特殊標記。例外的是，psql 會在
只包含 `\.` 的一行結束
`COPY FROM STDIN` 作業（也就是在 SQL 腳本中讀取
內嵌的 `COPY` 資料），無論是文字模式還是 `CSV`
模式。

<a id="id-1.9.3.55.9.3.6"></a>

### 注意

v18 之前的 PostgreSQL 版本一律
將未加引號的 `\.` 辨識為資料結尾標記，
即使是從獨立的檔案讀取時也一樣。為了與舊
版本相容，當 `\.` 單獨出現在一行時，`COPY TO` 會為它加上引號，
即使這已不再必要。

<a id="id-1.9.3.55.9.3.7"></a>

### 注意

在 `CSV` 格式中，所有字元都有意義。一個前後
被空白或
`DELIMITER` 以外的任何字元包圍的加引號值，將會包含這些字元。若你從一個會用空白把 `CSV`
行補齊到某個固定寬度的系統匯入資料，這可能會造成
錯誤。若發生
這種情況，你可能需要先預先處理 `CSV` 檔案，移除
尾端的空白，再將資料匯入
PostgreSQL。

<a id="id-1.9.3.55.9.3.8"></a>

### 注意

`CSV` 格式既能辨識也能產生 `CSV` 檔案，其中包含
內嵌歸位字元與換行字元的加引號值。因此，
這些檔案並不像文字格式的檔案那樣嚴格地每個資料表資料列一行。

<a id="id-1.9.3.55.9.3.9"></a>

### 注意

許多程式會產生奇怪、有時甚至不合常理的 `CSV` 檔案，
因此這種檔案格式與其說是標準，不如說是一種慣例。所以你
可能會遇到某些無法使用此
機制匯入的檔案，而 `COPY` 也可能產生其他
程式無法處理的檔案。

<a id="SQL-COPY-BINARY-FORMAT"></a>

### 二進位格式

`binary` 格式選項會使所有資料以
二進位格式（而非文字）儲存／讀取。它比
文字與 `CSV` 格式稍快一些，
但二進位格式的檔案在不同機器架構與
PostgreSQL 版本之間的可攜性較差。
此外，二進位格式與資料型別高度相關；例如，
從 `smallint` 欄位輸出二進位資料，
再將其讀入 `integer` 欄位是行不通的，即使這在
文字格式中完全可行。

`binary` 檔案格式由
一個檔案標頭、零個或多個包含資料列資料的元組，以及
一個檔案結尾區組成。標頭與資料皆採用網路位元組順序。

<a id="id-1.9.3.55.9.4.4"></a>

### 注意

7.4 之前的 PostgreSQL 版本使用
不同的二進位檔案格式。

<a id="id-1.9.3.55.9.4.5"></a>

#### 檔案標頭

檔案標頭由 19 個位元組的固定欄位組成（原文寫作 15 個位元組，但依下列各欄位計算，11 位元組的簽章加上兩個 32 位元整數欄位共為 19 位元組），其後接著
一個長度可變的標頭擴充區域。固定欄位如下：

簽章
:   11 個位元組的序列 `PGCOPY\n\377\r\n\0`——請注意，零位元組
    是簽章中必要的一部分。（此簽章的設計，是為了能
    輕易識別出因非 8 位元乾淨（non-8-bit-clean）的傳輸而遭到破壞的檔案。
    此簽章會因行尾轉換
    過濾器、零位元組被丟棄、高位元被丟棄或同位元變更而改變。）

旗標欄位
:   32 位元整數位元遮罩，用來表示檔案格式的重要面向。位元
    從 0（LSB）編號到 31（MSB）。請注意，
    此欄位以網路位元組順序（最高有效位元組在前）儲存，
    檔案格式中使用的所有整數欄位也都是如此。位元
    16–31 保留用來表示關鍵的檔案格式問題；讀取端
    若在此範圍內發現非預期的位元被設定，應該中止。位元 0–15
    保留用來標示向後相容的格式問題；讀取端
    應該直接忽略此範圍內任何被設定的非預期位元。目前
    只定義了一個旗標位元，其餘位元必須為零：

    位元 16
    :   若為 1，資料中包含 OID；若為 0，則不包含。PostgreSQL
        已不再支援 Oid 系統欄位，
        但此格式仍然包含這個指示位元。

標頭擴充區域長度
:   32 位元整數，標頭其餘部分的長度（以位元組計），不包含此欄位本身。
    目前此值為零，第一個元組緊接在其後。
    未來對格式的變更可能允許
    在標頭中加入額外的資料。讀取端應該默默略過任何
    它不知道如何處理的標頭擴充資料。

標頭擴充區域預計包含一連串
可自我識別的區塊。旗標欄位並非用來告訴讀取端
擴充區域中有什麼內容。標頭擴充內容的具體設計
留待日後的版本決定。

此設計既允許向後相容的標頭新增（加入
標頭擴充區塊，或設定低位旗標位元），也允許
不向後相容的變更（設定高位旗標位元來標示此類
變更，並視需要在擴充區域中加入輔助資料）。

<a id="id-1.9.3.55.9.4.6"></a>

#### 元組

每個元組開頭是一個 16 位元整數，表示該
元組中的欄位數量。（目前，資料表中所有元組的這個數量都相同，但
不一定永遠如此。）接著，對元組中的每個欄位重複以下內容：
一個 32 位元的長度字，後面接著該長度位元組數的欄位資料。（
長度字不包含其本身，且可以為零。）作為特殊情況，
-1 表示 NULL 欄位值。在 NULL 的情況下，其後不接任何值位元組。

欄位之間沒有對齊填補，也沒有任何其他額外資料。

目前，二進位格式檔案中的所有資料值都
假定為二進位格式（格式代碼 1）。預期
未來的擴充可能會加入一個標頭欄位，允許
為每個欄位指定格式代碼。

若要判斷實際元組資料的適當二進位格式，你
應該參考 PostgreSQL 原始碼，
特別是每個欄位資料型別的 `*send` 與 `*recv` 函式
（這些函式通常位於原始碼發行版的
`src/backend/utils/adt/` 目錄中）。

若檔案中包含 OID，OID 欄位會緊接在
欄位數量字之後。它是一個一般欄位，只是它不計入
欄位數量。請注意，目前版本的 PostgreSQL 已不支援 oid 系統欄位。

<a id="id-1.9.3.55.9.4.7"></a>

#### 檔案結尾區

檔案結尾區由一個包含 -1 的 16 位元整數字組成。這
很容易與元組的欄位數量字區分。

若欄位數量字既不是 -1，
也不是預期的欄位數，讀取端應該回報錯誤。這提供了一道額外的
檢查，用來偵測讀取端在解析資料時以某種方式失去同步。

<a id="id-1.9.3.55.10"></a>

## 範例

下列範例使用直線符號（`|`）作為欄位分隔符號，
將資料表複製到用戶端：

```

COPY country TO STDOUT (DELIMITER '|');
```

將檔案中的資料複製到 `country` 資料表：

```

COPY country FROM '/usr1/proj/bray/sql/country_data';
```

只將名稱以 'A' 開頭的國家複製到檔案中：

```

COPY (SELECT * FROM country WHERE country_name LIKE 'A%') TO '/usr1/proj/bray/sql/a_list_countries.copy';
```

若要複製到壓縮檔，你可以將輸出透過外部
壓縮程式以管線傳送：

```

COPY country TO PROGRAM 'gzip > /usr1/proj/bray/sql/country_data.gz';
```

以下是適合從
`STDIN` 複製到資料表的資料範例：

```

AF      AFGHANISTAN
AL      ALBANIA
DZ      ALGERIA
ZM      ZAMBIA
ZW      ZIMBABWE
```

請注意，每一行中的空白實際上是 tab 字元。

以下是相同的資料以二進位格式輸出的結果。
這些資料是經過
Unix 工具程式 `od -c` 過濾後顯示的。該資料表有三個欄位；
第一個的型別是 `char(2)`，第二個的型別是 `text`，
第三個的型別是 `integer`。所有資料列在第三個欄位中都是
空值。

```

0000000   P   G   C   O   P   Y  \n 377  \r  \n  \0  \0  \0  \0  \0  \0
0000020  \0  \0  \0  \0 003  \0  \0  \0 002   A   F  \0  \0  \0 013   A
0000040   F   G   H   A   N   I   S   T   A   N 377 377 377 377  \0 003
0000060  \0  \0  \0 002   A   L  \0  \0  \0 007   A   L   B   A   N   I
0000100   A 377 377 377 377  \0 003  \0  \0  \0 002   D   Z  \0  \0  \0
0000120 007   A   L   G   E   R   I   A 377 377 377 377  \0 003  \0  \0
0000140  \0 002   Z   M  \0  \0  \0 006   Z   A   M   B   I   A 377 377
0000160 377 377  \0 003  \0  \0  \0 002   Z   W  \0  \0  \0  \b   Z   I
0000200   M   B   A   B   W   E 377 377 377 377 377 377
```

<a id="id-1.9.3.55.11"></a>

## 相容性

SQL 標準中沒有 `COPY` 陳述式。

下列語法在 PostgreSQL
9.0 版之前使用，目前仍受支援：

```

COPY table_name [ ( column_name [, ...] ) ]
    FROM { 'filename' | STDIN }
    [ [ WITH ]
          [ BINARY ]
          [ DELIMITER [ AS ] 'delimiter_character' ]
          [ NULL [ AS ] 'null_string' ]
          [ CSV [ HEADER ]
                [ QUOTE [ AS ] 'quote_character' ]
                [ ESCAPE [ AS ] 'escape_character' ]
                [ FORCE NOT NULL column_name [, ...] ] ] ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) }
    TO { 'filename' | STDOUT }
    [ [ WITH ]
          [ BINARY ]
          [ DELIMITER [ AS ] 'delimiter_character' ]
          [ NULL [ AS ] 'null_string' ]
          [ CSV [ HEADER ]
                [ QUOTE [ AS ] 'quote_character' ]
                [ ESCAPE [ AS ] 'escape_character' ]
                [ FORCE QUOTE { column_name [, ...] | * } ] ] ]
```

請注意，在此語法中，`BINARY` 與 `CSV` 是
被視為獨立的關鍵字，而不是 `FORMAT`
選項的引數。

下列語法在 PostgreSQL
7.3 版之前使用，目前仍受支援：

```

COPY [ BINARY ] table_name
    FROM { 'filename' | STDIN }
    [ [USING] DELIMITERS 'delimiter_character' ]
    [ WITH NULL AS 'null_string' ]

COPY [ BINARY ] table_name
    TO { 'filename' | STDOUT }
    [ [USING] DELIMITERS 'delimiter_character' ]
    [ WITH NULL AS 'null_string' ]
```

<a id="id-1.9.3.55.12"></a>

## 另請參閱

[第 27.4.3 節](../../server-administration/monitoring/progress-reporting.md#copy-progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-copy.html)（原文版本：18.6；核對日期：2026-10-05）
