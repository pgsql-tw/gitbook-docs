<a id="RUNTIME-CONFIG-CLIENT"></a>

## 19.11. 用戶端連線預設值 [#](#RUNTIME-CONFIG-CLIENT)

[19.11.1. 陳述式行為](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)

[19.11.2. 地區設定與格式化](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)

[19.11.3. 共享程式庫預先載入](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)

[19.11.4. 其他預設值](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

<a id="RUNTIME-CONFIG-CLIENT-STATEMENT"></a>

### 19.11.1. 陳述式行為 [#](#RUNTIME-CONFIG-CLIENT-STATEMENT)

<a id="GUC-CLIENT-MIN-MESSAGES"></a>

`client_min_messages` (`enum`) <a id="id-1.6.6.14.2.2.1.1.3"></a> [#](#GUC-CLIENT-MIN-MESSAGES)
:   控制哪些
    [訊息等級](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS)
    會被傳送到用戶端。
    合法的值有 `DEBUG5`、
    `DEBUG4`、`DEBUG3`、`DEBUG2`、
    `DEBUG1`、`LOG`、`NOTICE`、
    `WARNING`，以及 `ERROR`。
    每個等級都包含其之後的所有等級。等級越後面，
    傳送的訊息就越少。預設值為
    `NOTICE`。請注意，`LOG` 在此處的
    順位，與在 [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 中不同。

    `INFO` 等級的訊息永遠會被傳送給用戶端。
<a id="GUC-SEARCH-PATH"></a>

`search_path` (`string`) <a id="id-1.6.6.14.2.2.2.1.3"></a> <a id="id-1.6.6.14.2.2.2.1.4"></a> [#](#GUC-SEARCH-PATH)
:   此變數指定當一個物件（資料表、資料型別、函式等）
    以未指定綱要的簡單名稱被參照時，
    要搜尋綱要的順序。當不同綱要中存在
    名稱相同的物件時，會使用在搜尋路徑中最先
    找到的那一個。若某個物件不在搜尋路徑中任何一個
    綱要內，就只能透過指定其所屬綱要的限定
    （加點）名稱來參照它。

    `search_path` 的值必須是以逗號分隔的
    綱要名稱清單。任何不是既有綱要、
    或使用者對其沒有 `USAGE` 權限的名稱，
    都會被默默忽略。

    如果清單項目之一是特殊名稱
    `$user`，且存在一個名稱為
    `CURRENT_USER` 傳回值的綱要，且使用者對其
    具備 `USAGE` 權限，則會替換為該綱要。
    （若否，`$user` 會被忽略。）

    無論是否在路徑中提及，系統目錄綱要
    `pg_catalog` 永遠都會被搜尋。若有在路徑中
    提及，則會依指定的順序搜尋。如果
    `pg_catalog` 不在路徑中，則會在搜尋任何
    路徑項目*之前*先搜尋它。

    同樣地，目前工作階段的暫存資料表綱要
    `pg_temp_nnn`，只要存在，永遠都會被搜尋。
    可以使用別名 `pg_temp`<a id="id-1.6.6.14.2.2.2.2.5.3"></a> 在路徑中明確列出它。
    如果未在路徑中列出，則會第一個被搜尋
    （甚至在 `pg_catalog` 之前）。不過，
    暫存綱要只會針對關聯（資料表、檢視表、
    序列等）與資料型別名稱進行搜尋，
    不會用於搜尋函式或運算子名稱。

    當建立物件時未指定特定目標綱要，
    這些物件會被放入
    `search_path` 中列出的第一個合法綱要。
    若搜尋路徑為空，則會回報錯誤。

    此參數的預設值為
    `"$user", public`。
    此設定支援共享使用資料庫（沒有任何使用者
    擁有私有綱要，所有人共用 `public`）、
    每個使用者專屬的私有綱要，以及兩者的組合。
    可以透過全域或逐使用者變更預設的搜尋
    路徑設定，達成其他效果。

    有關綱要處理的更多資訊，請參閱
    [5.10 節](../../the-sql-language/ddl/ddl-schemas.md)。特別要注意，預設
    組態設定僅適用於資料庫只有單一使用者，
    或少數彼此互信使用者的情況。

    可以透過 SQL 函式
    `current_schemas`
    （參閱[9.27 節](../../the-sql-language/functions/functions-info.md)），檢視搜尋路徑目前的
    有效值。這與檢視
    `search_path` 的值並不完全相同，因為
    `current_schemas` 會顯示
    `search_path` 中出現的項目
    實際上是如何被解析的。
<a id="GUC-ROW-SECURITY"></a>

`row_security` (`boolean`) <a id="id-1.6.6.14.2.2.3.1.3"></a> [#](#GUC-ROW-SECURITY)
:   此變數控制是否應在套用資料列安全性原則之外，
    改為引發錯誤。設為 `on` 時，
    原則會正常套用。設為 `off` 時，
    原本會套用至少一項原則的查詢會失敗。預設值為 `on`。
    在受限的資料列可見性可能導致不正確結果的情況下，
    請改為 `off`；舉例來說，pg_dump
    預設就會這麼做。此變數對繞過所有資料列安全性
    原則的角色（也就是超級使用者，以及具備
    `BYPASSRLS` 屬性的角色）沒有影響。

    有關資料列安全性原則的更多資訊，
    請參閱 [CREATE POLICY](../../reference/sql-commands/sql-createpolicy.md)。
<a id="GUC-DEFAULT-TABLE-ACCESS-METHOD"></a>

`default_table_access_method` (`string`) <a id="id-1.6.6.14.2.2.4.1.3"></a> [#](#GUC-DEFAULT-TABLE-ACCESS-METHOD)
:   此參數指定在建立資料表或實體化檢視表時，
    若 `CREATE` 命令未明確指定存取方法，
    或使用未允許指定資料表存取方法的
    `SELECT ... INTO` 時，
    要使用的預設資料表存取方法。預設值為 `heap`。
<a id="GUC-DEFAULT-TABLESPACE"></a>

`default_tablespace` (`string`) <a id="id-1.6.6.14.2.2.5.1.3"></a> <a id="id-1.6.6.14.2.2.5.1.4"></a> [#](#GUC-DEFAULT-TABLESPACE)
:   此變數指定在 `CREATE` 命令未明確指定
    表空間時，用來建立物件（資料表與索引）的
    預設表空間。

    此值可以是表空間的名稱，或是空字串（代表
    使用目前資料庫的預設表空間）。
    若此值與任何既有表空間的名稱都不相符，
    PostgreSQL 會自動使用目前資料庫的
    預設表空間。若指定了非預設的表空間，
    使用者必須對其具備 `CREATE` 權限，
    否則建立嘗試將會失敗。

    暫存資料表不使用此變數；對於暫存資料表，
    會改為查詢 [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES)。

    建立資料庫時也不會使用此變數。
    根據預設，新資料庫會繼承其複製自的範本
    資料庫的表空間設定。

    若在建立分割資料表時，此參數設為非空字串，
    該分割資料表的表空間會被設為此值，
    並會被用作未來建立的分割區的預設
    表空間，即使 `default_tablespace` 此後
    已經變更也一樣。

    有關表空間的更多資訊，
    請參閱[22.6 節](../managing-databases/manage-ag-tablespaces.md)。
<a id="GUC-DEFAULT-TOAST-COMPRESSION"></a>

`default_toast_compression` (`enum`) <a id="id-1.6.6.14.2.2.6.1.3"></a> [#](#GUC-DEFAULT-TOAST-COMPRESSION)
:   此變數設定可壓縮欄位值的預設
    [TOAST](../../internals/storage/storage-toast.md)
    壓縮方法。（可以透過在
    `CREATE TABLE` 或
    `ALTER TABLE` 中設定
    `COMPRESSION` 欄位選項，針對個別欄位覆寫此設定。）
    支援的壓縮方法有 `pglz`，
    以及（若 PostgreSQL 是以
    `--with-lz4` 編譯的）`lz4`。
    預設值為 `pglz`。
<a id="GUC-TEMP-TABLESPACES"></a>

`temp_tablespaces` (`string`) <a id="id-1.6.6.14.2.2.7.1.3"></a> <a id="id-1.6.6.14.2.2.7.1.4"></a> [#](#GUC-TEMP-TABLESPACES)
:   此變數指定在 `CREATE` 命令未明確指定
    表空間時，用來建立暫存物件（暫存資料表，
    以及暫存資料表上的索引）的表空間。
    用於例如排序大型資料集等用途的暫存檔案，
    也會建立在這些表空間中。

    此值是一份表空間名稱清單。若清單中有
    多於一個名稱，PostgreSQL 每次
    要建立暫存物件時，會從清單中隨機選擇
    一個成員；不過在同一個交易內，連續建立的
    暫存物件，會依序放入清單中連續的表空間。
    若清單中選中的項目是空字串，
    PostgreSQL 會自動改用目前資料庫的
    預設表空間。

    以互動方式設定 `temp_tablespaces` 時，
    指定不存在的表空間會導致錯誤，指定使用者
    沒有 `CREATE` 權限的表空間也一樣。不過，
    使用先前設定好的值時，不存在的表空間會被
    忽略，使用者缺少 `CREATE` 權限的表空間
    也一樣。特別是，此規則適用於使用
    `postgresql.conf` 中設定的值時。

    預設值為空字串，這會使所有暫存物件
    都建立在目前資料庫的預設
    表空間中。

    另請參閱 [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE)。
<a id="GUC-CHECK-FUNCTION-BODIES"></a>

`check_function_bodies` (`boolean`) <a id="id-1.6.6.14.2.2.8.1.3"></a> [#](#GUC-CHECK-FUNCTION-BODIES)
:   此參數通常為開啟。設為 `off` 時，
    會停用在 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 與
    [CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md) 期間對常式主體字串的驗證。
    停用驗證可以避免驗證流程的副作用，
    特別是防止因前向參照等問題造成的誤判。
    在代替其他使用者載入函式之前，請將此參數
    設為 `off`；pg_dump 會自動這麼做。
<a id="GUC-DEFAULT-TRANSACTION-ISOLATION"></a>

`default_transaction_isolation` (`enum`) <a id="id-1.6.6.14.2.2.9.1.3"></a> <a id="id-1.6.6.14.2.2.9.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-ISOLATION)
:   每個 SQL 交易都有一個隔離等級，可以是
    「read uncommitted（讀取未提交）」、「read
    committed（讀取已提交）」、「repeatable read（可重複讀取）」，
    或「serializable（可序列化）」。此參數控制
    每個新交易的預設隔離等級。預設值
    為「read committed」。

    詳情請參閱[第 13 章](../../the-sql-language/mvcc/README.md)與 [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md)。
<a id="GUC-DEFAULT-TRANSACTION-READ-ONLY"></a>

`default_transaction_read_only` (`boolean`) <a id="id-1.6.6.14.2.2.10.1.3"></a> <a id="id-1.6.6.14.2.2.10.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-READ-ONLY)
:   唯讀的 SQL 交易無法變更非暫存資料表。
    此參數控制每個新交易的預設唯讀狀態。
    預設值為 `off`（讀寫）。

    詳情請參閱 [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md)。
<a id="GUC-DEFAULT-TRANSACTION-DEFERRABLE"></a>

`default_transaction_deferrable` (`boolean`) <a id="id-1.6.6.14.2.2.11.1.3"></a> <a id="id-1.6.6.14.2.2.11.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-DEFERRABLE)
:   在 `serializable` 隔離等級下執行時，
    可延遲（deferrable）的唯讀 SQL 交易，
    在被允許繼續進行之前可能會被延遲。不過，
    一旦它開始執行，就不會產生任何確保
    可序列化性所需的額外負擔；因此序列化程式碼
    不會因為並行更新而強制中止此交易，
    使此選項適合用於長時間執行的唯讀交易。

    此參數控制每個新交易的預設可延遲狀態。
    目前對讀寫交易，或以低於
    `serializable` 隔離等級執行的交易
    沒有影響。預設值為 `off`。

    詳情請參閱 [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md)。
<a id="GUC-TRANSACTION-ISOLATION"></a>

`transaction_isolation` (`enum`) <a id="id-1.6.6.14.2.2.12.1.3"></a> <a id="id-1.6.6.14.2.2.12.1.4"></a> [#](#GUC-TRANSACTION-ISOLATION)
:   此參數反映目前交易的隔離等級。
    在每個交易開始時，此值會被設為
    [default_transaction_isolation](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-ISOLATION) 目前的值。
    後續任何嘗試變更此值的操作，都等同於
    [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) 命令。
<a id="GUC-TRANSACTION-READ-ONLY"></a>

`transaction_read_only` (`boolean`) <a id="id-1.6.6.14.2.2.13.1.3"></a> <a id="id-1.6.6.14.2.2.13.1.4"></a> [#](#GUC-TRANSACTION-READ-ONLY)
:   此參數反映目前交易的唯讀狀態。
    在每個交易開始時，此值會被設為
    [default_transaction_read_only](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-READ-ONLY) 目前的值。
    後續任何嘗試變更此值的操作，都等同於
    [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) 命令。
<a id="GUC-TRANSACTION-DEFERRABLE"></a>

`transaction_deferrable` (`boolean`) <a id="id-1.6.6.14.2.2.14.1.3"></a> <a id="id-1.6.6.14.2.2.14.1.4"></a> [#](#GUC-TRANSACTION-DEFERRABLE)
:   此參數反映目前交易的可延遲狀態。
    在每個交易開始時，此值會被設為
    [default_transaction_deferrable](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-DEFERRABLE) 目前的值。
    後續任何嘗試變更此值的操作，都等同於
    [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) 命令。
<a id="GUC-SESSION-REPLICATION-ROLE"></a>

`session_replication_role` (`enum`) <a id="id-1.6.6.14.2.2.15.1.3"></a> [#](#GUC-SESSION-REPLICATION-ROLE)
:   控制目前工作階段中複寫相關觸發程序與規則的
    觸發行為。
    可能的值有 `origin`（預設值）、
    `replica` 與 `local`。
    設定此參數會導致捨棄任何先前快取的
    查詢計畫。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    此設定的用途，是讓邏輯複寫系統在套用
    已複寫的變更時，將其設為 `replica`。
    這麼做的效果，是使（未從預設組態設定變更的）
    觸發程序與規則不會在複寫端觸發。詳情請參閱
    [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 中的
    `ENABLE TRIGGER` 與 `ENABLE RULE`
    子句。

    PostgreSQL 在內部將 `origin` 與
    `local` 這兩個設定視為相同。第三方複寫
    系統可能會將這兩個值用於其內部用途，
    例如使用 `local` 表示其變更
    不應被複寫的工作階段。

    由於外部索引鍵是以觸發程序實作的，將此參數
    設為 `replica` 也會停用所有外部索引鍵
    檢查，若使用不當，可能導致資料處於不一致的
    狀態。
<a id="GUC-STATEMENT-TIMEOUT"></a>

`statement_timeout` (`integer`) <a id="id-1.6.6.14.2.2.16.1.3"></a> [#](#GUC-STATEMENT-TIMEOUT)
:   中止耗時超過指定時間量的任何陳述式。
    若 `log_min_error_statement` 設為
    `ERROR` 或更低，逾時的陳述式
    也會被記錄下來。
    若此值指定時未帶單位，則以毫秒為單位。
    值為零（預設值）代表停用此逾時。

    此逾時是從命令抵達伺服器的時間點開始計算，
    直到伺服器完成該命令為止。若單一簡單查詢訊息中
    含有多個 SQL 陳述式，逾時會分別套用於
    每個陳述式。
    （13 之前的 PostgreSQL 版本通常將
    此逾時視為套用於整個查詢字串。）
    在擴充查詢通訊協定中，逾時會在任何與查詢相關的
    訊息（Parse、Bind、Execute、Describe）抵達時開始計時，
    並在 Execute 或 Sync 訊息完成時被取消。

    不建議在
    `postgresql.conf` 中設定 `statement_timeout`，
    因為這會影響所有工作階段。
<a id="GUC-TRANSACTION-TIMEOUT"></a>

`transaction_timeout` (`integer`) <a id="id-1.6.6.14.2.2.17.1.3"></a> [#](#GUC-TRANSACTION-TIMEOUT)
:   終止在交易中持續時間超過指定時間量的任何
    工作階段。此上限同時適用於明確的交易
    （以 `BEGIN` 開始）以及對應單一陳述式
    隱含開始的交易。
    若此值指定時未帶單位，則以毫秒為單位。
    值為零（預設值）代表停用此逾時。

    若 `transaction_timeout` 短於或等於
    `idle_in_transaction_session_timeout` 或 `statement_timeout`，
    則較長的逾時會被忽略。

    不建議在
    `postgresql.conf` 中設定 `transaction_timeout`，
    因為這會影響所有工作階段。

    ### 注意

    已備妥交易不受此逾時限制。
<a id="GUC-LOCK-TIMEOUT"></a>

`lock_timeout` (`integer`) <a id="id-1.6.6.14.2.2.18.1.3"></a> [#](#GUC-LOCK-TIMEOUT)
:   中止在嘗試取得資料表、索引、
    資料列或其他資料庫物件的鎖定時，等待時間超過
    指定時間量的任何陳述式。此時間上限是分別套用於
    每一次取得鎖定的嘗試。此上限同時適用於明確的
    鎖定請求（例如 `LOCK TABLE`，或未使用
    `NOWAIT` 的 `SELECT
    FOR UPDATE`），以及隱含取得的
    鎖定。
    若此值指定時未帶單位，則以毫秒為單位。
    值為零（預設值）代表停用此逾時。

    與 `statement_timeout` 不同，此逾時
    只可能在等待鎖定時發生。請注意，若
    `statement_timeout` 為非零值，將
    `lock_timeout` 設為與其相同或更大的值
    相當沒有意義，因為陳述式逾時永遠會先觸發。若
    `log_min_error_statement` 設為
    `ERROR` 或更低，逾時的陳述式將會
    被記錄下來。

    不建議在
    `postgresql.conf` 中設定 `lock_timeout`，
    因為這會影響所有工作階段。
<a id="GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT"></a>

`idle_in_transaction_session_timeout` (`integer`) <a id="id-1.6.6.14.2.2.19.1.3"></a> [#](#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
:   終止在開啟的交易中閒置（也就是等待用戶端查詢）
    超過指定時間量的任何工作階段。
    若此值指定時未帶單位，則以毫秒為單位。
    值為零（預設值）代表停用此逾時。

    此選項可用於確保閒置的工作階段不會
    持有鎖定過長的時間。即使沒有持有重要的
    鎖定，開啟中的交易仍會阻止清除可能僅對此
    交易可見的近期死亡 tuple；因此長時間保持
    閒置，可能導致資料表膨脹。
    詳情請參閱[24.1 節](../maintenance/routine-vacuuming.md)。
<a id="GUC-IDLE-SESSION-TIMEOUT"></a>

`idle_session_timeout` (`integer`) <a id="id-1.6.6.14.2.2.20.1.3"></a> [#](#GUC-IDLE-SESSION-TIMEOUT)
:   終止閒置（也就是等待用戶端查詢，但不在
    開啟的交易中）超過指定時間量的任何工作階段。
    若此值指定時未帶單位，則以毫秒為單位。
    值為零（預設值）代表停用此逾時。

    與開啟中交易的情況不同，沒有交易的閒置
    工作階段不會對伺服器造成太大成本，因此
    比起 `idle_in_transaction_session_timeout`，
    啟用此逾時的需求較小。

    對透過連線池軟體或其他中介軟體建立的連線
    強制執行此逾時時請務必小心，因為這類
    層級可能無法妥善應對非預期的連線關閉。
    僅對互動式工作階段啟用此逾時可能會有幫助，
    例如只針對特定使用者套用。
<a id="GUC-BYTEA-OUTPUT"></a>

`bytea_output` (`enum`) <a id="id-1.6.6.14.2.2.21.1.3"></a> [#](#GUC-BYTEA-OUTPUT)
:   設定 `bytea` 型別值的輸出格式。
    合法的值有 `hex`（預設值）
    與 `escape`（傳統的 PostgreSQL
    格式）。詳情請參閱[8.4 節](../../the-sql-language/datatype/datatype-binary.md)。
    無論此設定為何，`bytea` 型別
    輸入時永遠同時接受這兩種格式。
<a id="GUC-XMLBINARY"></a>

`xmlbinary` (`enum`) <a id="id-1.6.6.14.2.2.22.1.3"></a> [#](#GUC-XMLBINARY)
:   設定二進位值在 XML 中應如何編碼。此設定
    適用於，例如透過 `xmlelement` 或
    `xmlforest` 函式將 `bytea` 值
    轉換為 XML 的情況。可能的值有
    `base64` 與 `hex`，這兩者
    都定義於 XML Schema 標準中。預設值為
    `base64`。有關 XML 相關函式的
    更多資訊，請參閱[9.15 節](../../the-sql-language/functions/functions-xml.md)。

    此處實際的選擇主要取決於個人偏好，
    唯一的限制是用戶端應用程式可能存在的
    限制。兩種方法都支援所有可能的值，
    不過 hex 編碼會比
    base64 編碼稍大一些。
<a id="GUC-XMLOPTION"></a>

`xmloption` (`enum`) <a id="id-1.6.6.14.2.2.23.1.3"></a> <a id="id-1.6.6.14.2.2.23.1.4"></a> <a id="id-1.6.6.14.2.2.23.1.5"></a> [#](#GUC-XMLOPTION)
:   設定在 XML 與字元字串值之間轉換時，
    隱含使用 `DOCUMENT` 還是
    `CONTENT`。詳情請參閱[8.13 節](../../the-sql-language/datatype/datatype-xml.md)
    的說明。合法的
    值有 `DOCUMENT` 與
    `CONTENT`。預設值為
    `CONTENT`。

    依照 SQL 標準，設定此選項的命令為

    ```

    SET XML OPTION { DOCUMENT | CONTENT };
    ```

    此語法在 PostgreSQL 中同樣可用。
<a id="GUC-GIN-PENDING-LIST-LIMIT"></a>

`gin_pending_list_limit` (`integer`) <a id="id-1.6.6.14.2.2.24.1.3"></a> [#](#GUC-GIN-PENDING-LIST-LIMIT)
:   設定 GIN 索引待處理清單（pending list）的最大大小，
    此清單在啟用 `fastupdate` 時使用。若清單
    成長超過此最大大小，會透過將清單中的項目
    批次移入索引的主要 GIN 資料結構來清理。
    若此值指定時未帶單位，則以千位元組為單位。
    預設值為 4 百萬位元組（`4MB`）。可以透過變更
    索引儲存參數，針對個別 GIN 索引覆寫
    此設定。
    詳情請參閱[65.4.4.1 節](../../internals/indextypes/gin.md#GIN-FAST-UPDATE)與[65.4.5 節](../../internals/indextypes/gin.md#GIN-TIPS)。
<a id="GUC-CREATEROLE-SELF-GRANT"></a>

`createrole_self_grant` (`string`) <a id="id-1.6.6.14.2.2.25.1.3"></a> [#](#GUC-CREATEROLE-SELF-GRANT)
:   若一個具備 `CREATEROLE` 但不具備
    `SUPERUSER` 的使用者建立了一個角色，
    且此參數設為非空值，新建立的角色
    將以指定的選項授予給建立該角色的使用者。
    此值必須是
    `set`、`inherit`，或這兩者以逗號
    分隔的清單。預設值為空字串，
    代表停用此功能。

    此選項的目的，是讓不具超級使用者身分的
    `CREATEROLE` 使用者，能夠自動繼承，
    或自動取得對任何已建立使用者執行
    `SET ROLE` 的能力。由於
    `CREATEROLE` 使用者永遠會隱含被授予
    對已建立角色的 `ADMIN OPTION`，
    該使用者原本就一直可以執行
    `GRANT` 陳述式來達成與此設定相同的效果。
    不過，若能自動授予，對易用性而言可能較為方便。
    超級使用者會自動繼承每個角色的權限，
    也永遠可以對任何角色執行
    `SET ROLE`，此設定可以用來
    為 `CREATEROLE` 使用者針對其建立的
    使用者，產生類似的行為。
<a id="GUC-EVENT-TRIGGERS"></a>

`event_triggers` (`boolean`) <a id="id-1.6.6.14.2.2.26.1.3"></a> [#](#GUC-EVENT-TRIGGERS)
:   允許暫時停用事件觸發程序的執行，
    以便對有問題的事件觸發程序進行故障排除與修復。
    將此值設為 `false`，會停用所有事件
    觸發程序。設為 `true`，則允許所有事件
    觸發程序觸發，這是預設值。只有超級使用者以及
    具備相應 `SET` 權限的使用者可以變更此設定。
<a id="GUC-RESTRICT-NONSYSTEM-RELATION-KIND"></a>

`restrict_nonsystem_relation_kind` (`string`) <a id="id-1.6.6.14.2.2.27.1.3"></a> [#](#GUC-RESTRICT-NONSYSTEM-RELATION-KIND)
:   設定禁止存取非系統關聯的關聯種類。
    此值的格式為以逗號分隔的關聯種類清單。
    目前支援的關聯種類有 `view` 與
    `foreign-table`。

<a id="RUNTIME-CONFIG-CLIENT-FORMAT"></a>

### 19.11.2. 地區設定與格式化 [#](#RUNTIME-CONFIG-CLIENT-FORMAT)

<a id="GUC-DATESTYLE"></a>

`DateStyle` (`string`) <a id="id-1.6.6.14.3.2.1.1.3"></a> [#](#GUC-DATESTYLE)
:   設定日期與時間值的顯示格式，以及解讀模糊日期
    輸入值的規則。基於歷史因素，此變數
    包含兩個獨立的成分：輸出格式規範
    （`ISO`、
    `Postgres`、`SQL`，或 `German`），
    以及年／月／日順序的輸入／輸出規範
    （`DMY`、`MDY`，或 `YMD`）。這些
    可以分別設定，也可以一起設定。關鍵字 `Euro`
    與 `European` 是 `DMY` 的同義字；
    關鍵字 `US`、`NonEuro`，以及
    `NonEuropean` 是 `MDY` 的同義字。詳情請參閱
    [8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。內建的
    預設值為 `ISO, MDY`，但
    initdb 會以對應所選
    `lc_time` 地區設定行為的設定值，
    初始化組態設定檔。
<a id="GUC-INTERVALSTYLE"></a>

`IntervalStyle` (`enum`) <a id="id-1.6.6.14.3.2.2.1.3"></a> [#](#GUC-INTERVALSTYLE)
:   設定間隔（interval）值的顯示格式。
    值 `sql_standard` 會產生符合
    SQL 標準間隔常值的輸出。
    值 `postgres`（此為預設值）會產生
    與 8.4 之前的 PostgreSQL 版本
    在 [DateStyle](runtime-config-client.md#GUC-DATESTYLE)
    參數設為 `ISO` 時相符的輸出。
    值 `postgres_verbose` 會產生
    與 8.4 之前的 PostgreSQL 版本
    在 `DateStyle`
    參數設為非 `ISO` 輸出時相符的輸出。
    值 `iso_8601` 會產生符合 ISO 8601 第
    4.4.3.2 節所定義「帶有指定符的格式（format
    with designators）」的時間間隔輸出。

    `IntervalStyle` 參數也會影響
    對模糊間隔輸入的解讀。詳情請參閱
    [8.5.4 節](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-INTERVAL-INPUT)。
<a id="GUC-TIMEZONE"></a>

`TimeZone` (`string`) <a id="id-1.6.6.14.3.2.3.1.3"></a> <a id="id-1.6.6.14.3.2.3.1.4"></a> [#](#GUC-TIMEZONE)
:   設定用於顯示與解讀時間戳記的時區。
    內建的預設值為 `GMT`，但通常會在
    `postgresql.conf` 中被覆寫；initdb
    會在其中安裝與其系統環境相對應的設定。
    詳情請參閱[8.5.3 節](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-TIMEZONES)。
<a id="GUC-TIMEZONE-ABBREVIATIONS"></a>

`timezone_abbreviations` (`string`) <a id="id-1.6.6.14.3.2.4.1.3"></a> <a id="id-1.6.6.14.3.2.4.1.4"></a> [#](#GUC-TIMEZONE-ABBREVIATIONS)
:   設定伺服器在日期時間輸入時，除了目前
    `TimeZone` 設定所定義的任何縮寫外，
    還會接受的其他時區縮寫集合。預設值為
    `'Default'`，這是一套在世界大多數地方
    都適用的集合；此外還有
    `'Australia'` 與 `'India'`，
    也可以為特定安裝環境定義其他集合。
    詳情請參閱[附錄 B.4 節](../../appendixes/datetime-appendix/datetime-config-files.md)。
<a id="GUC-EXTRA-FLOAT-DIGITS"></a>

`extra_float_digits` (`integer`) <a id="id-1.6.6.14.3.2.5.1.3"></a> <a id="id-1.6.6.14.3.2.5.1.4"></a> <a id="id-1.6.6.14.3.2.5.1.5"></a> [#](#GUC-EXTRA-FLOAT-DIGITS)
:   此參數調整浮點數值（包括 `float4`、`float8`，
    以及幾何資料型別）文字輸出所使用的位數。

    若此值為 1（預設值）或以上，浮點數值會以
    最短精確格式輸出；參閱[8.1.3 節](../../the-sql-language/datatype/datatype-numeric.md#DATATYPE-FLOAT)。
    實際產生的位數，僅取決於被輸出的值，
    而非此參數的值。`float8` 值最多需要
    17 位數，`float4`
    值則最多需要 9 位數。此格式既快速又精確，
    正確讀取時能完全保留原始的二進位浮點值。
    基於歷史相容性考量，允許設為最多 3 的值。

    若此值為零或負值，則輸出會四捨五入到
    給定的十進位精確度。所使用的精確度，是該型別的
    標準位數（視情況為 `FLT_DIG`
    或 `DBL_DIG`），並依此參數的值減少。
    （舉例來說，指定 -1 會使
    `float4` 值輸出時四捨五入到 5 個有效
    位數，`float8` 值
    則四捨五入到 14 位數。）此格式較慢，
    且不會保留二進位浮點值的所有位元，
    但可能較易於人類閱讀。

    ### 注意

    此參數的意義及其預設值，在
    PostgreSQL 12 有所變更；
    詳情請參閱[8.1.3 節](../../the-sql-language/datatype/datatype-numeric.md#DATATYPE-FLOAT)。
<a id="GUC-CLIENT-ENCODING"></a>

`client_encoding` (`string`) <a id="id-1.6.6.14.3.2.6.1.3"></a> <a id="id-1.6.6.14.3.2.6.1.4"></a> [#](#GUC-CLIENT-ENCODING)
:   設定用戶端編碼（字元集）。
    預設會使用資料庫編碼。
    PostgreSQL 伺服器支援的字元集，
    說明於[23.3.1 節](../charset/multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)。
<a id="GUC-LC-MESSAGES"></a>

`lc_messages` (`string`) <a id="id-1.6.6.14.3.2.7.1.3"></a> [#](#GUC-LC-MESSAGES)
:   設定訊息顯示所使用的語言。可接受的
    值因系統而異；詳情請參閱[23.1 節](../charset/locale.md)。
    若此變數設為空字串（此為預設值），
    則此值會以因系統而異的方式，
    繼承自伺服器的執行環境。

    在某些系統上，此地區設定類別並不存在。
    設定此變數仍然可以運作，但不會有任何效果。
    此外，也有可能不存在所需語言的翻譯訊息。
    在這種情況下，你會繼續看到
    英文訊息。

    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-LC-MONETARY"></a>

`lc_monetary` (`string`) <a id="id-1.6.6.14.3.2.8.1.3"></a> [#](#GUC-LC-MONETARY)
:   設定用於格式化金額（例如透過
    `to_char` 系列函式）的地區設定。
    可接受的值因系統而異；詳情請參閱
    [23.1 節](../charset/locale.md)。若此變數設為空字串
    （此為預設值），則此值會以因系統而異的方式，
    繼承自伺服器的執行環境。
<a id="GUC-LC-NUMERIC"></a>

`lc_numeric` (`string`) <a id="id-1.6.6.14.3.2.9.1.3"></a> [#](#GUC-LC-NUMERIC)
:   設定用於格式化數字（例如透過
    `to_char` 系列函式）的地區設定。
    可接受的值因系統而異；詳情請參閱
    [23.1 節](../charset/locale.md)。若此變數設為空字串
    （此為預設值），則此值會以因系統而異的方式，
    繼承自伺服器的執行環境。
<a id="GUC-LC-TIME"></a>

`lc_time` (`string`) <a id="id-1.6.6.14.3.2.10.1.3"></a> [#](#GUC-LC-TIME)
:   設定用於格式化日期與時間（例如透過
    `to_char` 系列函式）的地區設定。
    可接受的值因系統而異；詳情請參閱
    [23.1 節](../charset/locale.md)。若此變數設為空字串
    （此為預設值），則此值會以因系統而異的方式，
    繼承自伺服器的執行環境。
<a id="GUC-ICU-VALIDATION-LEVEL"></a>

`icu_validation_level` (`enum`) <a id="id-1.6.6.14.3.2.11.1.3"></a> [#](#GUC-ICU-VALIDATION-LEVEL)
:   當遇到 ICU 地區設定驗證問題時，控制用來
    回報此問題的[訊息等級](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS)。
    合法的值有
    `DISABLED`、`DEBUG5`、
    `DEBUG4`、`DEBUG3`、
    `DEBUG2`、`DEBUG1`、
    `INFO`、`NOTICE`、
    `WARNING`、`ERROR`，以及
    `LOG`。

    若設為 `DISABLED`，則完全不會回報
    驗證問題。否則，會以給定的訊息等級
    回報問題。預設值為 `WARNING`。
<a id="GUC-DEFAULT-TEXT-SEARCH-CONFIG"></a>

`default_text_search_config` (`string`) <a id="id-1.6.6.14.3.2.12.1.3"></a> [#](#GUC-DEFAULT-TEXT-SEARCH-CONFIG)
:   選擇未明確指定組態設定引數之文字搜尋函式
    變體所使用的文字搜尋組態設定。
    詳情請參閱[第 12 章](../../the-sql-language/textsearch/README.md)。
    內建的預設值為 `pg_catalog.simple`，但
    initdb 會在能夠找到與所選
    `lc_ctype` 地區設定相符的組態設定時，
    以與此相對應的設定值，初始化組態設定檔。

<a id="RUNTIME-CONFIG-CLIENT-PRELOAD"></a>

### 19.11.3. 共享程式庫預先載入 [#](#RUNTIME-CONFIG-CLIENT-PRELOAD)

有多項設定可用於將共享程式庫預先載入
伺服器，以載入額外功能或達成效能上的
益處。舉例來說，設為
`'$libdir/mylib'`，會使
`mylib.so`（在某些平台上為
`mylib.sl`）從安裝環境的標準
程式庫目錄中被預先載入。這些設定之間的差異，
在於它們生效的時機，以及變更它們所需的權限。

PostgreSQL 程序語言程式庫
可以用這種方式預先載入，通常使用
`'$libdir/plXXX'` 語法，其中
`XXX` 是 `pgsql`、`perl`、
`tcl`，或 `python`。

只有特別為搭配 PostgreSQL 使用而設計的共享
程式庫，才能以這種方式載入。每個受 PostgreSQL
支援的程式庫，都有一個會被檢查以確保相容性的
「magic block」。因此，非 PostgreSQL
程式庫無法以這種方式載入。你可能可以使用
作業系統機制，例如 `LD_PRELOAD`
來達成此目的。

一般而言，請參閱特定模組的文件，以了解
載入該模組的建議方式。

<a id="GUC-LOCAL-PRELOAD-LIBRARIES"></a>

`local_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.1.1.3"></a> <a id="id-1.6.6.14.4.6.1.1.4"></a> [#](#GUC-LOCAL-PRELOAD-LIBRARIES)
:   此變數指定一個或多個要在連線開始時
    預先載入的共享程式庫。
    此值包含以逗號分隔的程式庫名稱清單，每個名稱
    的解讀方式與 [`LOAD`](../../reference/sql-commands/sql-load.md) 命令相同。
    項目之間的空白字元會被忽略；如果程式庫名稱中
    需要包含空白字元或逗號，請以雙引號括住該名稱。
    此參數的值只會在連線開始時生效。
    後續的變更沒有效果。若找不到指定的
    程式庫，連線嘗試就會失敗。

    此選項可以由任何使用者設定。因此，
    可以被載入的程式庫，僅限於安裝環境的
    標準程式庫目錄中
    `plugins` 子目錄下的程式庫。
    （確保只有「安全」的程式庫被安裝在該處，
    是資料庫管理員的責任。）
    `local_preload_libraries` 中的項目
    可以明確指定此目錄，例如
    `$libdir/plugins/mylib`，或直接指定
    程式庫名稱——`mylib` 的效果
    與 `$libdir/plugins/mylib` 相同。

    此功能的目的，是讓沒有特殊權限的使用者，
    能夠在不需要明確 `LOAD` 命令的情況下，
    將除錯或效能量測程式庫載入特定的
    工作階段。為此，通常會透過用戶端的
    `PGOPTIONS` 環境變數，或使用
    `ALTER ROLE SET`
    來設定此參數。

    不過，除非某個模組是特別設計供
    非超級使用者以這種方式使用，否則這通常
    不是正確的設定方式。請改用
    [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES)。
<a id="GUC-SESSION-PRELOAD-LIBRARIES"></a>

`session_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.2.1.3"></a> [#](#GUC-SESSION-PRELOAD-LIBRARIES)
:   此變數指定一個或多個要在連線開始時
    預先載入的共享程式庫。
    此值包含以逗號分隔的程式庫名稱清單，每個名稱
    的解讀方式與 [`LOAD`](../../reference/sql-commands/sql-load.md) 命令相同。
    項目之間的空白字元會被忽略；如果程式庫名稱中
    需要包含空白字元或逗號，請以雙引號括住該名稱。
    此參數的值只會在連線開始時生效。
    後續的變更沒有效果。若找不到指定的
    程式庫，連線嘗試就會失敗。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    此功能的目的，是讓除錯或效能量測程式庫，
    能夠在不需要明確給予
    `LOAD` 命令的情況下，被載入特定的工作階段。
    舉例來說，可以透過
    `ALTER ROLE SET` 設定此參數，
    對特定使用者名稱下的所有工作階段啟用
    [auto_explain](../../appendixes/contrib/auto-explain.md)。此外，此參數
    可以在不重新啟動伺服器的情況下變更
    （但變更只會在新工作階段開始時生效），
    因此即使某個模組應套用於所有工作階段，
    以這種方式新增模組也比較容易。

    與 [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 不同，
    在工作階段開始時載入程式庫，
    相較於第一次使用時才載入，並沒有太大的
    效能優勢。不過，在使用連線池時，
    確實有一些優勢。
<a id="GUC-SHARED-PRELOAD-LIBRARIES"></a>

`shared_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.3.1.3"></a> [#](#GUC-SHARED-PRELOAD-LIBRARIES)
:   此變數指定一個或多個要在伺服器啟動時
    預先載入的共享程式庫。
    此值包含以逗號分隔的程式庫名稱清單，每個名稱
    的解讀方式與 [`LOAD`](../../reference/sql-commands/sql-load.md) 命令相同。
    項目之間的空白字元會被忽略；如果程式庫名稱中
    需要包含空白字元或逗號，請以雙引號括住該名稱。
    此參數只能在伺服器啟動時設定。若找不到指定的
    程式庫，伺服器將無法啟動。

    有些程式庫需要執行只能在 postmaster 啟動時
    進行的特定操作，例如配置共享記憶體、
    保留輕量鎖，或啟動背景工作程序。這些
    程式庫必須透過此參數在伺服器啟動時載入。詳情
    請參閱各程式庫的文件。

    其他程式庫也可以預先載入。透過預先載入共享
    程式庫，可以在該程式庫第一次被使用時避免
    程式庫啟動時間。不過，每個新伺服器程序的
    啟動時間可能會稍微增加，即使該程序從未
    使用該程式庫。因此，此參數建議只用於
    大多數工作階段都會用到的程式庫。此外，變更
    此參數需要重新啟動伺服器，因此這通常不適合
    用於短期的除錯工作。請改用
    [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES)。

    ### 注意

    在 Windows 主機上，於伺服器啟動時預先載入
    程式庫，並不會縮短每個新伺服器程序的
    啟動所需時間；每個伺服器程序都會重新載入
    所有預先載入的程式庫。不過，對於需要在
    postmaster 啟動時執行操作的程式庫而言，
    `shared_preload_libraries` 在 Windows 主機上
    仍然有用。
<a id="GUC-JIT-PROVIDER"></a>

`jit_provider` (`string`) <a id="id-1.6.6.14.4.6.4.1.3"></a> [#](#GUC-JIT-PROVIDER)
:   此變數是要使用的 JIT 提供者程式庫名稱
    （參閱[30.4.2 節](../jit/jit-extensibility.md#JIT-PLUGGABLE)）。
    預設值為 `llvmjit`。
    此參數只能在伺服器啟動時設定。

    若設為不存在的程式庫，JIT 將無法
    使用，但不會引發錯誤。這使得 JIT 支援
    可以獨立於主要的
    PostgreSQL 套件安裝。

<a id="RUNTIME-CONFIG-CLIENT-OTHER"></a>

### 19.11.4. 其他預設值 [#](#RUNTIME-CONFIG-CLIENT-OTHER)

<a id="GUC-DYNAMIC-LIBRARY-PATH"></a>

`dynamic_library_path` (`string`) <a id="id-1.6.6.14.5.2.1.1.3"></a> <a id="id-1.6.6.14.5.2.1.1.4"></a> [#](#GUC-DYNAMIC-LIBRARY-PATH)
:   若需要開啟一個動態載入模組，且
    `CREATE FUNCTION` 或
    `LOAD` 命令中指定的檔案名稱
    不含目錄部分（也就是該
    名稱不包含斜線），系統將會在此
    路徑中搜尋所需的檔案。

    `dynamic_library_path` 的值必須是
    以冒號（在 Windows 上為分號）分隔的絕對目錄路徑
    清單。若清單中的某個項目以特殊字串
    `$libdir` 開頭，則會以編譯時內建的
    PostgreSQL 套件程式庫目錄取代 `$libdir`；
    這是標準
    PostgreSQL 發行版所提供之模組的
    安裝位置。
    （可以使用 `pg_config --pkglibdir`
    找出此目錄的名稱。）舉例來說：

    ```

    dynamic_library_path = '/usr/local/lib/postgresql:/home/my_project/lib:$libdir'
    ```

    或者，在 Windows 環境中：

    ```

    dynamic_library_path = 'C:\tools\postgresql;H:\my_project\lib;$libdir'
    ```

    此參數的預設值為
    `'$libdir'`。若此值設為空
    字串，會停用自動路徑搜尋。

    此參數可以在執行時期由超級使用者，
    以及具備相應 `SET` 權限的使用者變更，
    但以此方式設定的值，只會持續到
    用戶端連線結束為止，因此此方法應
    保留供開發用途使用。設定此參數
    建議的方式，是在
    `postgresql.conf` 組態設定
    檔案中設定。
<a id="GUC-EXTENSION-CONTROL-PATH"></a>

`extension_control_path` (`string`) <a id="id-1.6.6.14.5.2.2.1.3"></a> [#](#GUC-EXTENSION-CONTROL-PATH)
:   用於搜尋延伸模組，特別是延伸模組控制檔案
    （`name.control`）的路徑。其餘的
    延伸模組指令碼與次要控制檔案，
    則會從找到主要控制檔案的同一個目錄載入。
    詳情請參閱[36.17.1 節](../../server-programming/extend/extend-extensions.md#EXTEND-EXTENSIONS-FILES)。

    `extension_control_path` 的值必須是
    以冒號（在 Windows 上為分號）分隔的絕對目錄路徑
    清單。若清單中的某個項目以特殊字串
    `$system` 開頭，則會以編譯時內建的
    PostgreSQL 延伸模組目錄取代 `$system`；
    這是標準
    PostgreSQL 發行版所提供延伸模組的
    安裝位置。
    （可以使用 `pg_config --sharedir`
    找出此目錄的名稱。）舉例來說：

    ```

    extension_control_path = '/usr/local/share/postgresql:/home/my_project/share:$system'
    ```

    或者，在 Windows 環境中：

    ```

    extension_control_path = 'C:\tools\postgresql;H:\my_project\share;$system'
    ```

    請注意，指定的路徑項目應具有一個
    `extension` 子目錄，其中會存放
    `.control` 與 `.sql` 檔案；
    `extension` 後綴會自動附加到
    每個路徑項目後面。

    此參數的預設值為
    `'$system'`。若此值設為空
    字串，同樣會採用預設值 `'$system'`。

    若組態設定路徑中的多個目錄，皆存在名稱相同的
    延伸模組，則只會使用路徑中最先找到的那個
    實例。

    此參數可以在執行時期由超級使用者，
    以及具備相應 `SET` 權限的使用者變更，
    但以此方式設定的值，只會持續到
    用戶端連線結束為止，因此此方法應
    保留供開發用途使用。設定此參數
    建議的方式，是在
    `postgresql.conf` 組態設定
    檔案中設定。

    請注意，如果你設定此參數，以便能夠從
    非標準位置載入延伸模組，很可能也需要將
    [dynamic_library_path](runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH) 設為對應的
    位置，例如：

    ```

    extension_control_path = '/usr/local/share/postgresql:$system'
    dynamic_library_path = '/usr/local/lib/postgresql:$libdir'
    ```
<a id="GUC-GIN-FUZZY-SEARCH-LIMIT"></a>

`gin_fuzzy_search_limit` (`integer`) <a id="id-1.6.6.14.5.2.3.1.3"></a> [#](#GUC-GIN-FUZZY-SEARCH-LIMIT)
:   GIN 索引掃描所傳回結果集大小的軟性上限。詳情請參閱
    [65.4.5 節](../../internals/indextypes/gin.md#GIN-TIPS)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-client.html)（原文版本：18.6；核對日期：2026-09-25）
