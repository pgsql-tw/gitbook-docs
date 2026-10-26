<a id="PGBENCH"></a><a id="id-1.9.4.11.1"></a>

## pgbench

pgbench — 在 PostgreSQL 上執行效能基準測試

<a id="id-1.9.4.11.4"></a>

## 語法

<a id="id-1.9.4.11.4.1"></a>

`pgbench` `-i` [*`option`*...] [*`dbname`*]

<a id="id-1.9.4.11.4.2"></a>

`pgbench` [*`option`*...] [*`dbname`*]

<a id="id-1.9.4.11.5"></a>

## 說明

pgbench 是一個在 PostgreSQL 上執行效能基準測試的簡單程式。它會一再重複執行同一系列的 SQL 命令，可能是在多個並行的資料庫工作階段中執行，然後計算平均交易速率（每秒交易數）。預設情況下，pgbench 測試的情境大致以 TPC-B 為基礎，每筆交易包含五個 `SELECT`、`UPDATE` 與 `INSERT` 命令。不過，只要撰寫你自己的交易腳本檔，就能輕鬆測試其他情況。

pgbench 的典型輸出如下：

```

transaction type: <builtin: TPC-B (sort of)>
scaling factor: 10
query mode: simple
number of clients: 10
number of threads: 1
maximum number of tries: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
number of failed transactions: 0 (0.000%)
latency average = 11.013 ms
latency stddev = 7.351 ms
initial connection time = 45.758 ms
tps = 896.967014 (without initial connection time)
```

前七行回報了一些最重要的參數設定。第六行回報在發生序列化錯誤或死結錯誤時，交易的最大嘗試次數（詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)）。第八行回報已完成與預期的交易數（後者就是用戶端數乘以每個用戶端的交易數）；除非執行在完成前失敗，或有 SQL 命令失敗，否則這兩個數字會相等。（在 `-T` 模式下，只會印出實際的交易數。）下一行回報因序列化錯誤或死結錯誤而失敗的交易數（詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)）。最後一行回報每秒交易數。

預設的類 TPC-B 交易測試需要事先建立特定的資料表。應該以 `-i`（初始化）選項呼叫 pgbench 來建立這些資料表並填入資料。（測試自訂腳本時不需要這個步驟，但你需要改為進行測試所需的任何設定。）初始化看起來像這樣：

```

pgbench -i [ other-options ] dbname
```

其中 *`dbname`* 是要在其中進行測試、已建立好的資料庫名稱。（你可能也需要使用 `-h`、`-p` 與／或 `-U` 選項，來指定如何連線到資料庫伺服器。）

<a id="id-1.9.4.11.5.9"></a>

### 小心

`pgbench -i` 會建立四個資料表 `pgbench_accounts`、`pgbench_branches`、`pgbench_history` 與 `pgbench_tellers`，並摧毀任何同名的現有資料表。如果你有資料表使用這些名稱，務必非常小心地改用另一個資料庫！

在預設的「縮放因子」（scale factor）1 之下，這些資料表一開始包含的資料列數如下：

```

table                   # of rows
---------------------------------
pgbench_branches        1
pgbench_tellers         10
pgbench_accounts        100000
pgbench_history         0
```

你可以（而且就大多數用途而言，或許應該）使用 `-s`（縮放因子）選項來增加資料列數。此時也可以使用 `-F`（fillfactor）選項。

完成必要的設定之後，你就可以用不含 `-i` 的命令執行效能基準測試，也就是

```

pgbench [ options ] dbname
```

幾乎在所有情況下，你都需要一些選項才能進行有用的測試。最重要的選項是 `-c`（用戶端數）、`-t`（交易數）、`-T`（時間限制）與 `-f`（指定自訂腳本檔）。完整清單請參閱下文。

<a id="id-1.9.4.11.6"></a>

## 選項

以下分為三個小節。資料庫初始化期間與執行效能基準測試時使用的選項不同，但有些選項在兩種情況下都有用。

<a id="PGBENCH-INIT-OPTIONS"></a>

### 初始化選項

pgbench 接受下列命令列初始化引數：

<a id="PGBENCH-OPTION-DBNAME"></a>

`[-d] dbname`<br>`[--dbname=]dbname` [#](#PGBENCH-OPTION-DBNAME)
:   指定要在其中進行測試的資料庫名稱。若未指定，則使用環境變數 `PGDATABASE`。若該變數也未設定，則使用連線所指定的使用者名稱。
<a id="PGBENCH-OPTION-INITIALIZE"></a>

`-i`<br>`--initialize` [#](#PGBENCH-OPTION-INITIALIZE)
:   要啟動初始化模式時，此選項為必要。
<a id="PGBENCH-OPTION-INIT-STEPS"></a>

`-I init_steps`<br>`--init-steps=init_steps` [#](#PGBENCH-OPTION-INIT-STEPS)
:   只執行一般初始化步驟中所選定的一組步驟。*`init_steps`* 指定要執行的初始化步驟，每個步驟使用一個字元。各步驟會依指定的順序執行。預設值為 `dtgvp`。可用的步驟如下：

    <a id="PGBENCH-OPTION-INIT-STEPS-D"></a>

    `d` (Drop) [#](#PGBENCH-OPTION-INIT-STEPS-D)
    :   移除任何現有的 pgbench 資料表。
    <a id="PGBENCH-OPTION-INIT-STEPS-T"></a>

    `t` (create Tables) [#](#PGBENCH-OPTION-INIT-STEPS-T)
    :   建立標準 pgbench 情境所使用的資料表，也就是 `pgbench_accounts`、`pgbench_branches`、`pgbench_history` 與 `pgbench_tellers`。
    <a id="PGBENCH-OPTION-INIT-STEPS-G"></a>

    `g` 或 `G`（Generate data，用戶端或伺服器端） [#](#PGBENCH-OPTION-INIT-STEPS-G)
    :   產生資料並載入標準資料表，取代任何已存在的資料。

        使用 `g`（用戶端資料產生）時，資料會在 `pgbench` 用戶端中產生，然後傳送到伺服器。這會透過 `COPY` 大量使用用戶端／伺服器之間的頻寬。對於 PostgreSQL 14 或更新版本，`pgbench` 會使用 `FREEZE` 選項將資料載入一般（非分割區）資料表，以加快後續的 `VACUUM`。使用 `g` 時，在為所有資料表產生資料的期間，日誌每 100,000 個資料列會印出一則訊息。

        使用 `G`（伺服器端資料產生）時，`pgbench` 用戶端只會送出小型查詢，而資料實際上是在伺服器中產生。這種方式不需要可觀的頻寬，但伺服器會做更多工作。使用 `G` 時，日誌在產生資料期間不會印出任何進度訊息。

        預設的初始化行為使用用戶端資料產生（等同於 `g`）。
    <a id="PGBENCH-OPTION-INIT-STEPS-V"></a>

    `v` (Vacuum) [#](#PGBENCH-OPTION-INIT-STEPS-V)
    :   對標準資料表執行 `VACUUM`。
    <a id="PGBENCH-OPTION-INIT-STEPS-P"></a>

    `p` (create Primary keys) [#](#PGBENCH-OPTION-INIT-STEPS-P)
    :   在標準資料表上建立主鍵索引。
    <a id="PGBENCH-OPTION-INIT-STEPS-F"></a>

    `f` (create Foreign keys) [#](#PGBENCH-OPTION-INIT-STEPS-F)
    :   在標準資料表之間建立外部鍵限制條件。（請注意，預設不會執行此步驟。）
<a id="PGBENCH-OPTION-FILLFACTOR"></a>

`-F` *`fillfactor`*<br>`--fillfactor=`*`fillfactor`* [#](#PGBENCH-OPTION-FILLFACTOR)
:   以指定的 fillfactor 建立 `pgbench_accounts`、`pgbench_tellers` 與 `pgbench_branches` 資料表。預設值為 100。
<a id="PGBENCH-OPTION-NO-VACUUM-INIT"></a>

`-n`<br>`--no-vacuum` [#](#PGBENCH-OPTION-NO-VACUUM-INIT)
:   初始化期間不執行清理（vacuum）。（即使在 `-I` 中指定了 `v` 初始化步驟，此選項也會抑制該步驟。）
<a id="PGBENCH-OPTION-QUIET"></a>

`-q`<br>`--quiet` [#](#PGBENCH-OPTION-QUIET)
:   將日誌切換為安靜模式，每 5 秒只產生一則進度訊息。預設的日誌每 100,000 個資料列印出一則訊息，這經常每秒輸出許多行（尤其是在硬體效能良好時）。

    若在 `-I` 中指定了 `G`，此設定沒有作用。
<a id="PGBENCH-OPTION-SCALE-INIT"></a>

`-s` *`scale_factor`*<br>`--scale=`*`scale_factor`* [#](#PGBENCH-OPTION-SCALE-INIT)
:   將產生的資料列數乘以縮放因子。例如，`-s 100` 會在 `pgbench_accounts` 資料表中建立 10,000,000 個資料列。預設值為 1。當縮放值為 20,000 或更大時，用來存放帳戶識別碼的欄位（`aid` 欄位）會改用較大的整數（`bigint`），以便大到足以容納帳戶識別碼的範圍。
<a id="PGBENCH-OPTION-FOREIGN-KEYS"></a>

`--foreign-keys` [#](#PGBENCH-OPTION-FOREIGN-KEYS)
:   在標準資料表之間建立外部鍵限制條件。（若初始化步驟序列中尚未包含 `f` 步驟，此選項會將其加入。）
<a id="PGBENCH-OPTION-INDEX-TABLESPACE"></a>

`--index-tablespace=index_tablespace` [#](#PGBENCH-OPTION-INDEX-TABLESPACE)
:   在指定的資料表空間中建立索引，而不是在預設的資料表空間中。
<a id="PGBENCH-OPTION-PARTITION-METHOD"></a>

`--partition-method=NAME` [#](#PGBENCH-OPTION-PARTITION-METHOD)
:   以 *`NAME`* 方法建立分割的 `pgbench_accounts` 資料表。預期的值為 `range` 或 `hash`。此選項要求 `--partitions` 設為非零值。若未指定，預設為 `range`。
<a id="PGBENCH-OPTION-PARTITIONS"></a>

`--partitions=NUM` [#](#PGBENCH-OPTION-PARTITIONS)
:   建立一個分割的 `pgbench_accounts` 資料表，依縮放後的帳戶數分成 *`NUM`* 個大小幾乎相等的分割區。預設值為 `0`，表示不進行分割。
<a id="PGBENCH-OPTION-TABLESPACE"></a>

`--tablespace=tablespace` [#](#PGBENCH-OPTION-TABLESPACE)
:   在指定的資料表空間中建立資料表，而不是在預設的資料表空間中。
<a id="PGBENCH-OPTION-UNLOGGED-TABLES"></a>

`--unlogged-tables` [#](#PGBENCH-OPTION-UNLOGGED-TABLES)
:   將所有資料表建立為無日誌（unlogged）資料表，而不是永久資料表。

<a id="PGBENCH-RUN-OPTIONS"></a>

### 效能基準測試選項

pgbench 接受下列命令列效能基準測試引數：

<a id="PGBENCH-OPTION-BUILTIN"></a>

`-b` *`scriptname[@weight]`*<br>`--builtin`=*`scriptname[@weight]`* [#](#PGBENCH-OPTION-BUILTIN)
:   將指定的內建腳本加入要執行的腳本清單。可用的內建腳本有：`tpcb-like`、`simple-update` 與 `select-only`。內建名稱可接受不致混淆的前綴。若使用特殊名稱 `list`，會顯示內建腳本清單並立即結束。

    你可以選擇在 `@` 之後寫一個整數權重，以調整選中此腳本相對於其他腳本的機率。預設權重為 1。詳細資訊請參閱下文。
<a id="PGBENCH-OPTION-CLIENT"></a>

`-c` *`clients`*<br>`--client=`*`clients`* [#](#PGBENCH-OPTION-CLIENT)
:   模擬的用戶端數，也就是並行資料庫工作階段的數量。預設值為 1。
<a id="PGBENCH-OPTION-CONNECT"></a>

`-C`<br>`--connect` [#](#PGBENCH-OPTION-CONNECT)
:   為每筆交易建立一個新連線，而不是每個用戶端工作階段只建立一次。這對於測量連線的額外負擔很有用。
<a id="PGBENCH-OPTION-DEFINE"></a>

`-D` *`varname`*`=`*`value`*<br>`--define=`*`varname`*`=`*`value`* [#](#PGBENCH-OPTION-DEFINE)
:   定義一個供自訂腳本使用的變數（請參閱下文）。允許使用多個 `-D` 選項。
<a id="PGBENCH-OPTION-FILE"></a>

`-f` *`filename[@weight]`*<br>`--file=`*`filename[@weight]`* [#](#PGBENCH-OPTION-FILE)
:   將從 *`filename`* 讀取的交易腳本加入要執行的腳本清單。

    你可以選擇在 `@` 之後寫一個整數權重，以調整選中此腳本相對於其他腳本的機率。預設權重為 1。（若要使用包含 `@` 字元的腳本檔名，請附加一個權重以避免混淆，例如 `filen@me@1`。）詳細資訊請參閱下文。
<a id="PGBENCH-OPTION-JOBS"></a>

`-j` *`threads`*<br>`--jobs=`*`threads`* [#](#PGBENCH-OPTION-JOBS)
:   pgbench 內的工作執行緒數。在多 CPU 的機器上，使用超過一個執行緒可能有幫助。用戶端會盡可能平均地分配到可用的執行緒。預設值為 1。
<a id="PGBENCH-OPTION-LOG"></a>

`-l`<br>`--log` [#](#PGBENCH-OPTION-LOG)
:   將每筆交易的相關資訊寫入日誌檔。詳細資訊請參閱下文。
<a id="PGBENCH-OPTION-LATENCY-LIMIT"></a>

`-L` *`limit`*<br>`--latency-limit=`*`limit`* [#](#PGBENCH-OPTION-LATENCY-LIMIT)
:   持續時間超過 *`limit`* 毫秒的交易會被計數，並以 *late*（延遲）另外回報。

    使用節流（`--rate=...`）時，落後排程超過 *`limit`* 毫秒、因而不可能符合延遲限制的交易，完全不會被送到伺服器。這些交易會被計數，並以 *skipped*（略過）另外回報。

    使用 `--max-tries` 選項時，因序列化異常或死結而失敗的交易，若其所有嘗試的總時間大於 *`limit`* 毫秒，就不會再重試。若只要限制嘗試的時間而不限制嘗試次數，請使用 `--max-tries=0`。預設情況下，選項 `--max-tries` 設為 1，發生序列化／死結錯誤的交易不會重試。關於重試這類交易的詳細資訊，請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。
<a id="PGBENCH-OPTION-PROTOCOL"></a>

`-M` *`querymode`*<br>`--protocol=`*`querymode`* [#](#PGBENCH-OPTION-PROTOCOL)
:   向伺服器提交查詢時所使用的協定：

    * `simple`：使用簡單查詢協定。
    * `extended`：使用延伸查詢協定。
    * `prepared`：使用延伸查詢協定並搭配預備陳述式。

    在 `prepared` 模式下，pgbench 從第二次查詢迭代開始會重複使用剖析分析的結果，因此 pgbench 執行得比其他模式快。

    預設為簡單查詢協定。（詳細資訊請參閱[第 54 章](../../internals/protocol/README.md)。）
<a id="PGBENCH-OPTION-NO-VACUUM-RUN"></a>

`-n`<br>`--no-vacuum` [#](#PGBENCH-OPTION-NO-VACUUM-RUN)
:   執行測試前不進行清理（vacuum）。若你執行的自訂測試情境不包含標準資料表 `pgbench_accounts`、`pgbench_branches`、`pgbench_history` 與 `pgbench_tellers`，此選項是*必要的*。
<a id="PGBENCH-OPTION-SKIP-SOME-UPDATES"></a>

`-N`<br>`--skip-some-updates` [#](#PGBENCH-OPTION-SKIP-SOME-UPDATES)
:   執行內建的 simple-update 腳本。為 `-b simple-update` 的簡寫。
<a id="PGBENCH-OPTION-PROGRESS"></a>

`-P` *`sec`*<br>`--progress=`*`sec`* [#](#PGBENCH-OPTION-PROGRESS)
:   每 *`sec`* 秒顯示一次進度報告。報告內容包括自執行開始以來的時間、自上次報告以來的 TPS，以及自上次報告以來交易延遲的平均值、標準差與失敗交易數。在節流（`-R`）之下，延遲是相對於交易的排程開始時間計算，而不是相對於交易實際開始的時間，因此它也包含平均排程落後時間。當使用 `--max-tries` 啟用序列化／死結錯誤後的交易重試時，報告會包含重試過的交易數與所有重試的總和。
<a id="PGBENCH-OPTION-REPORT-LATENCIES"></a>

`-r`<br>`--report-per-command` [#](#PGBENCH-OPTION-REPORT-LATENCIES)
:   在效能基準測試結束後，為每個命令回報下列統計資料：每個陳述式的平均延遲（從用戶端角度看的執行時間）、失敗次數，以及此命令中因序列化或死結錯誤而重試的次數。只有在 `--max-tries` 選項不等於 1 時，報告才會顯示重試統計資料。
<a id="PGBENCH-OPTION-RATE"></a>

`-R` *`rate`*<br>`--rate=`*`rate`* [#](#PGBENCH-OPTION-RATE)
:   以指定的速率為目標執行交易，而不是盡可能快地執行（預設）。速率以每秒交易數表示。若目標速率高於可能達到的最大速率，速率限制不會影響結果。

    達成目標速率的方式，是依照卜瓦松分布（Poisson distribution）的排程時間軸來啟動交易。預期開始時間的排程，是依據用戶端第一次啟動的時間向前推進，而不是依據前一筆交易結束的時間。這種做法表示，當交易超過其原本排定的結束時間時，後續的交易有可能再次趕上。

    啟用節流時，執行結束時回報的交易延遲是從排程開始時間起算，因此包含每筆交易等待前一筆交易完成所花的時間。這段等待時間稱為排程落後時間，其平均值與最大值也會另外回報。相對於交易實際開始時間的交易延遲，也就是在資料庫中執行該交易所花的時間，可以從回報的延遲減去排程落後時間來算出。

    若 `--latency-limit` 與 `--rate` 一起使用，由於延遲是從排程開始時間起算，交易可能落後太多，以致在前一筆交易結束時就已經超過延遲限制。這類交易不會送到伺服器，而是完全略過並另外計數。

    排程落後時間偏高，表示在所選的用戶端數與執行緒數下，系統無法以指定的速率處理交易。當平均交易執行時間比各交易之間的排程間隔更長時，每一筆後續交易都會落後得更多，而且測試執行得越久，排程落後時間就會持續增加。發生這種情況時，你必須降低指定的交易速率。
<a id="PGBENCH-OPTION-SCALE-RUN"></a>

`-s` *`scale_factor`*<br>`--scale=`*`scale_factor`* [#](#PGBENCH-OPTION-SCALE-RUN)
:   在 pgbench 的輸出中回報指定的縮放因子。使用內建測試時不需要這麼做；正確的縮放因子會透過計算 `pgbench_branches` 資料表中的資料列數來偵測。不過，當只測試自訂效能基準（`-f` 選項）時，除非使用此選項，否則縮放因子會回報為 1。
<a id="PGBENCH-OPTION-SELECT-ONLY"></a>

`-S`<br>`--select-only` [#](#PGBENCH-OPTION-SELECT-ONLY)
:   執行內建的 select-only 腳本。為 `-b select-only` 的簡寫。
<a id="PGBENCH-OPTION-TRANSACTIONS"></a>

`-t` *`transactions`*<br>`--transactions=`*`transactions`* [#](#PGBENCH-OPTION-TRANSACTIONS)
:   每個用戶端執行的交易數。預設值為 10。
<a id="PGBENCH-OPTION-TIME"></a>

`-T` *`seconds`*<br>`--time=`*`seconds`* [#](#PGBENCH-OPTION-TIME)
:   執行測試達這麼多秒，而不是每個用戶端執行固定數量的交易。`-t` 與 `-T` 互斥。
<a id="PGBENCH-OPTION-VACUUM-ALL"></a>

`-v`<br>`--vacuum-all` [#](#PGBENCH-OPTION-VACUUM-ALL)
:   在執行測試之前清理全部四個標準資料表。若既未指定 `-n`，也未指定 `-v`，pgbench 會清理 `pgbench_tellers` 與 `pgbench_branches` 資料表，並截斷 `pgbench_history`。
<a id="PGBENCH-OPTION-AGGREGATE-INTERVAL"></a>

`--aggregate-interval=seconds` [#](#PGBENCH-OPTION-AGGREGATE-INTERVAL)
:   彙總間隔的長度（以秒為單位）。只能與 `-l` 選項一起使用。使用此選項時，日誌包含每個間隔的摘要資料，如下文所述。
<a id="PGBENCH-OPTION-EXIT-ON-ABORT"></a>

`--exit-on-abort` [#](#PGBENCH-OPTION-EXIT-ON-ABORT)
:   當有任何用戶端因某個錯誤而中止時，立即結束。若不使用此選項，即使有用戶端中止，其他用戶端仍可能依 `-t` 或 `-T` 選項的指定繼續執行，而在這種情況下 pgbench 會印出不完整的結果。

    請注意，序列化失敗或死結失敗不會中止用戶端，因此不受此選項影響。詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。
<a id="PGBENCH-OPTION-FAILURES-DETAILED"></a>

`--failures-detailed` [#](#PGBENCH-OPTION-FAILURES-DETAILED)
:   在每筆交易日誌與彙總日誌中，以及在主要報告與每個腳本的報告中，依下列類型分組回報失敗：

    * 序列化失敗；
    * 死結失敗；

    詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。
<a id="PGBENCH-OPTION-LOG-PREFIX"></a>

`--log-prefix=prefix` [#](#PGBENCH-OPTION-LOG-PREFIX)
:   設定 `--log` 所建立之日誌檔的檔名前綴。預設值為 `pgbench_log`。
<a id="PGBENCH-OPTION-MAX-TRIES"></a>

`--max-tries=number_of_tries` [#](#PGBENCH-OPTION-MAX-TRIES)
:   啟用發生序列化／死結錯誤之交易的重試，並設定這類嘗試的最大次數。此選項可以與 `--latency-limit` 選項合併使用，後者會限制所有交易嘗試的總時間；此外，若沒有 `--latency-limit` 或 `--time`，就不能使用無限次的嘗試（`--max-tries=0`）。預設值為 1，發生序列化／死結錯誤的交易不會重試。關於重試這類交易的詳細資訊，請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。
<a id="PGBENCH-OPTION-PROGRESS-TIMESTAMP"></a>

`--progress-timestamp` [#](#PGBENCH-OPTION-PROGRESS-TIMESTAMP)
:   顯示進度（選項 `-P`）時，使用時間戳記（Unix epoch），而不是自執行開始以來的秒數。單位為秒，小數點後具有毫秒精確度。這有助於比較各種工具所產生的日誌。
<a id="PGBENCH-OPTION-RANDOM-SEED"></a>

`--random-seed=`*`seed`* [#](#PGBENCH-OPTION-RANDOM-SEED)
:   設定亂數產生器的種子。此種子用於系統亂數產生器，而該產生器再產生一系列初始產生器狀態，每個執行緒一個。*`seed`* 的值可以是：`time`（預設值，種子以目前時間為基礎）、`rand`（使用強亂數來源，若無可用來源則失敗），或一個無號十進位整數值。亂數產生器會由 pgbench 腳本明確呼叫（`random...` 函式），或隱含地呼叫（例如選項 `--rate` 會用它來排程交易）。明確設定時，用於設定種子的值會顯示在終端機上。任何 *`seed`* 允許的值，也可以透過環境變數 `PGBENCH_RANDOM_SEED` 提供。為確保所提供的種子影響所有可能的用途，請將此選項放在最前面，或使用環境變數。

    明確設定種子，就亂數而言，可以精確重現一次 `pgbench` 執行。由於亂數狀態是以執行緒為單位管理，這表示若每個執行緒只有一個用戶端，而且沒有外部或資料上的相依性，相同的呼叫會得到完全相同的 `pgbench` 執行。從統計的觀點來看，精確重現執行是個壞主意，因為它可能隱藏效能的變異性，或不當地提升效能，例如存取到與前一次執行相同的頁面。不過，它也可能對除錯有很大幫助，例如重新執行一個導致錯誤的棘手案例。請明智地使用。
<a id="PGBENCH-OPTION-SAMPLING-RATE"></a>

`--sampling-rate=rate` [#](#PGBENCH-OPTION-SAMPLING-RATE)
:   抽樣率，用於將資料寫入日誌時，以減少所產生的日誌量。若指定此選項，只有指定比例的交易會被記錄。1.0 表示所有交易都會被記錄，0.05 表示只有 5% 的交易會被記錄。

    處理日誌檔時，請記得將抽樣率納入考量。例如，計算 TPS 值時，你需要相應地將數字相乘（例如，抽樣率為 0.01 時，你只會得到實際 TPS 的 1/100）。
<a id="PGBENCH-OPTION-SHOW-SCRIPT"></a>

`--show-script=`*`scriptname`* [#](#PGBENCH-OPTION-SHOW-SCRIPT)
:   在 stderr 上顯示內建腳本 *`scriptname`* 的實際程式碼，並立即結束。
<a id="PGBENCH-OPTION-VERBOSE-ERRORS"></a>

`--verbose-errors` [#](#PGBENCH-OPTION-VERBOSE-ERRORS)
:   印出所有錯誤與失敗（未重試的錯誤）的相關訊息，對於序列化／死結失敗，還包括超過了哪一個重試限制，以及超過了多少。（請注意，在這種情況下，輸出量可能大幅增加。）詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。

<a id="PGBENCH-COMMON-OPTIONS"></a>

### 通用選項

pgbench 也接受下列用於連線參數與其他通用設定的通用命令列引數：

<a id="PGBENCH-OPTION-DEBUG"></a>

`--debug` [#](#PGBENCH-OPTION-DEBUG)
:   印出除錯輸出。
<a id="PGBENCH-OPTION-HOST"></a>

`-h` *`hostname`*<br>`--host=`*`hostname`* [#](#PGBENCH-OPTION-HOST)
:   資料庫伺服器的主機名稱
<a id="PGBENCH-OPTION-PORT"></a>

`-p` *`port`*<br>`--port=`*`port`* [#](#PGBENCH-OPTION-PORT)
:   資料庫伺服器的連接埠號碼
<a id="PGBENCH-OPTION-USERNAME"></a>

`-U` *`login`*<br>`--username=`*`login`* [#](#PGBENCH-OPTION-USERNAME)
:   用來連線的使用者名稱
<a id="PGBENCH-OPTION-VERSION"></a>

`-V`<br>`--version` [#](#PGBENCH-OPTION-VERSION)
:   印出 pgbench 版本，然後結束。
<a id="PGBENCH-OPTION-HELP"></a>

`-?`<br>`--help` [#](#PGBENCH-OPTION-HELP)
:   顯示 pgbench 命令列引數的說明，然後結束。

<a id="id-1.9.4.11.7"></a>

## 結束狀態

成功的執行會以狀態 0 結束。結束狀態 1 表示靜態問題，例如無效的命令列選項，或理應永遠不會發生的內部錯誤。啟動效能基準測試時發生的早期錯誤（例如初始連線失敗）也會以狀態 1 結束。執行期間的錯誤（例如資料庫錯誤或腳本中的問題）會導致結束狀態 2。在後者的情況下，若未指定 `--exit-on-abort` 選項，pgbench 會印出部分結果。

<a id="id-1.9.4.11.8"></a>

## 環境

<a id="PGBENCH-ENVIRONMENT-PGDATABASE"></a>

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER` [#](#PGBENCH-ENVIRONMENT-PGDATABASE)
:   預設連線參數。

這個工具程式和大多數其他 PostgreSQL 工具程式一樣，會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.11.9"></a>

## 注意事項

<a id="TRANSACTIONS-AND-SCRIPTS"></a>

### pgbench 中實際執行的「交易」是什麼？

pgbench 會執行從指定清單中隨機選出的測試腳本。這些腳本可能包括以 `-b` 指定的內建腳本，以及以 `-f` 指定的使用者提供腳本。每個腳本都可以在 `@` 之後指定一個相對權重，以改變其被選中的機率。預設權重為 `1`。權重為 `0` 的腳本會被忽略。

預設的內建交易腳本（也可以用 `-b tpcb-like` 呼叫）在每筆交易中，會針對隨機選取的 `aid`、`tid`、`bid` 與 `delta` 發出七個命令。此情境的靈感來自 TPC-B 效能基準，但實際上並不是 TPC-B，因此有此名稱。

1. `BEGIN;`
2. `UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;`
3. `SELECT abalance FROM pgbench_accounts WHERE aid = :aid;`
4. `UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;`
5. `UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;`
6. `INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);`
7. `END;`

若你選擇內建的 `simple-update`（也可用 `-N`），交易中不會包含步驟 4 與 5。這可以避免在這些資料表上的更新競爭，但會讓測試案例更不像 TPC-B。

若你選擇內建的 `select-only`（也可用 `-S`），只會發出 `SELECT`。

<a id="id-1.9.4.11.9.3"></a>

### 自訂腳本

pgbench 支援執行自訂的效能基準情境，方法是以從檔案讀取的交易腳本（`-f` 選項）取代預設的交易腳本（如上所述）。在這種情況下，一次「交易」計為一個腳本檔的一次執行。

腳本檔包含一個或多個以分號結尾的 SQL 命令。空行以及以 `--` 開頭的行會被忽略。腳本檔也可以包含「中繼命令」（meta command），由 pgbench 本身解譯，如下所述。

<a id="id-1.9.4.11.9.3.4"></a>

### 注意

在 PostgreSQL 9.6 之前，腳本檔中的 SQL 命令以換行字元結尾，因此無法跨行延續。現在則*必須*使用分號來分隔連續的 SQL 命令（不過，若 SQL 命令後面接著中繼命令，該 SQL 命令就不需要分號）。若你需要建立一個能同時用於新舊版本 pgbench 的腳本檔，請務必將每個 SQL 命令寫在單獨一行，並以分號結尾。

pgbench 腳本被假定不包含不完整的 SQL 交易區塊。若在執行時，用戶端到達腳本結尾時尚未完成最後一個交易區塊，該用戶端會被中止。

腳本檔有一個簡單的變數替換機制。變數名稱必須由字母（包括非拉丁字母）、數字與底線組成，且第一個字元不能是數字。變數可以由上文說明的命令列 `-D` 選項設定，或由下文說明的中繼命令設定。除了由 `-D` 命令列選項預先設定的任何變數之外，還有一些會自動預先設定的變數，列於[表 301](pgbench.md#PGBENCH-AUTOMATIC-VARIABLES)。使用 `-D` 為這些變數指定的值，優先於自動預設值。變數一旦設定，就可以在 SQL 命令中寫入 `:`*`variablename`*，將變數的值插入其中。執行超過一個用戶端工作階段時，每個工作階段都有自己的一組變數。pgbench 在單一陳述式中最多支援 255 次變數使用。

<a id="PGBENCH-AUTOMATIC-VARIABLES"></a>

**表 301. pgbench 自動變數**

<table border="1" class="table" summary="pgbench Automatic Variables"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>變數</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">client_id</code> </td><td>識別用戶端工作階段的唯一編號（從零開始）</td></tr><tr><td> <code class="literal">default_seed</code> </td><td>雜湊函式與偽隨機排列函式預設使用的種子</td></tr><tr><td> <code class="literal">random_seed</code> </td><td>亂數產生器種子（除非以 <code class="option">-D</code> 覆寫）</td></tr><tr><td> <code class="literal">scale</code> </td><td>目前的縮放因子</td></tr></tbody></table>

<br>

腳本檔的中繼命令以反斜線（`\`）開頭，通常延伸到該行結尾，不過可以透過寫入反斜線加換行，延續到額外的行。中繼命令的引數以空白分隔。支援下列中繼命令：

<a id="PGBENCH-METACOMMAND-GSET"></a>

`\gset [prefix]` `\aset [prefix]` [#](#PGBENCH-METACOMMAND-GSET)
:   這些命令可以用來結束 SQL 查詢，取代結尾的分號（`;`）。

    使用 `\gset` 命令時，前面的 SQL 查詢預期會傳回一個資料列，其各欄位會存入以欄位名稱命名的變數；若有提供 *`prefix`*，變數名稱會加上該前綴。

    使用 `\aset` 命令時，所有合併的 SQL 查詢（以 `\;` 分隔）的欄位都會存入以欄位名稱命名的變數；若有提供 *`prefix`*，變數名稱會加上該前綴。若某個查詢沒有傳回任何資料列，則不會進行指派，此時可以測試變數是否存在來偵測這種情況。若某個查詢傳回超過一個資料列，則保留最後一個值。

    `\gset` 與 `\aset` 不能在管線模式中使用，因為到了這些命令需要查詢結果的時候，結果還無法取得。

    下列範例將第一個查詢的最終帳戶餘額放入變數 *`abalance`*，並以第三個查詢的整數填入變數 *`p_two`* 與 *`p_three`*。第二個查詢的結果會被捨棄。最後兩個合併查詢的結果會存入變數 *`four`* 與 *`five`*。

    ```

    UPDATE pgbench_accounts
      SET abalance = abalance + :delta
      WHERE aid = :aid
      RETURNING abalance \gset
    -- compound of two queries
    SELECT 1 \;
    SELECT 2 AS two, 3 AS three \gset p_
    SELECT 4 AS four \; SELECT 5 AS five \aset
    ```
<a id="PGBENCH-METACOMMAND-IF-ELSE"></a>

`\if` *`expression`*<br>`\elif` *`expression`*<br>`\else`<br>`\endif` [#](#PGBENCH-METACOMMAND-IF-ELSE)
:   這組命令實作可巢狀的條件區塊，類似於 `psql` 的 [`\if` *`expression`*](app-psql.md#PSQL-METACOMMAND-IF)。條件運算式與 `\set` 所用的相同，非零值會被解讀為真。
<a id="PGBENCH-METACOMMAND-SET"></a>

`\set varname expression` [#](#PGBENCH-METACOMMAND-SET)
:   將變數 *`varname`* 設為由 *`expression`* 計算出的值。運算式可以包含 `NULL` 常數、布林常數 `TRUE` 與 `FALSE`、整數常數（例如 `5432`）、倍精度常數（例如 `3.14159`）、對變數的參照 `:`*`variablename`*、具有一般 SQL 優先順序與結合性的[運算子](pgbench.md#PGBENCH-BUILTIN-OPERATORS)、[函式呼叫](pgbench.md#PGBENCH-BUILTIN-FUNCTIONS)、SQL [`CASE` 通用條件運算式](../../the-sql-language/functions/functions-conditional.md#functions-case)以及括號。

    函式與大多數運算子在輸入為 `NULL` 時會傳回 `NULL`。

    就條件判斷而言，非零的數值為 `TRUE`，為零的數值以及 `NULL` 為 `FALSE`。

    過大或過小的整數與倍精度常數，以及整數算術運算子（`+`、`-`、`*` 與 `/`），在溢位時會引發錯誤。

    當 `CASE` 沒有提供最後的 `ELSE` 子句時，預設值為 `NULL`。

    範例：

    ```

    \set ntellers 10 * :scale
    \set aid (1021 * random(1, 100000 * :scale)) % \
               (100000 * :scale) + 1
    \set divx CASE WHEN :x <> 0 THEN :y/:x ELSE NULL END
    ```
<a id="PGBENCH-METACOMMAND-SLEEP"></a>

`\sleep number [ us | ms | s ]` [#](#PGBENCH-METACOMMAND-SLEEP)
:   使腳本執行暫停指定的時間長度，單位為微秒（`us`）、毫秒（`ms`）或秒（`s`）。若省略單位，則預設為秒。*`number`* 可以是整數常數，也可以是對具有整數值之變數的 `:`*`variablename`* 參照。

    範例：

    ```

    \sleep 10 ms
    ```
<a id="PGBENCH-METACOMMAND-SETSHELL"></a>

`\setshell varname command [ argument ... ]` [#](#PGBENCH-METACOMMAND-SETSHELL)
:   將變數 *`varname`* 設為以指定的 *`argument`* 執行 shell 命令 *`command`* 的結果。該命令必須透過其標準輸出傳回一個整數值。

    *`command`* 與每個 *`argument`* 可以是文字常數，也可以是對變數的 `:`*`variablename`* 參照。若你想使用以冒號開頭的 *`argument`*，請在 *`argument`* 的開頭再多寫一個冒號。

    範例：

    ```

    \setshell variable_to_be_assigned command literal_argument :variable ::literal_starting_with_colon
    ```
<a id="PGBENCH-METACOMMAND-SHELL"></a>

`\shell command [ argument ... ]` [#](#PGBENCH-METACOMMAND-SHELL)
:   與 `\setshell` 相同，但命令的結果會被捨棄。

    範例：

    ```

    \shell command literal_argument :variable ::literal_starting_with_colon
    ```
<a id="PGBENCH-METACOMMAND-PIPELINE"></a>

`\startpipeline`<br>`\syncpipeline`<br>`\endpipeline` [#](#PGBENCH-METACOMMAND-PIPELINE)
:   這組命令實作 SQL 陳述式的管線化。管線必須以 `\startpipeline` 開始，並以 `\endpipeline` 結束。兩者之間可以有任意數量的 `\syncpipeline` 命令，它會送出一個[同步訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)，而不結束進行中的管線，並把傳送緩衝區的內容送出（flush）。在管線模式中，陳述式會送到伺服器，而不等待先前陳述式的結果。詳細資訊請參閱[第 32.5 節](../../client-interfaces/libpq/libpq-pipeline-mode.md)。管線模式需要使用延伸查詢協定。

<a id="PGBENCH-BUILTIN-OPERATORS"></a>

### 內建運算子

[表 302](pgbench.md#PGBENCH-OPERATORS) 所列的算術、位元、比較與邏輯運算子內建於 pgbench 中，可用於出現在 [`\set`](pgbench.md#PGBENCH-METACOMMAND-SET) 中的運算式。這些運算子依優先順序由低到高列出。除非另有註明，接受兩個數值輸入的運算子，若任一輸入為倍精度，會產生倍精度值，否則會產生整數結果。

<a id="PGBENCH-OPERATORS"></a>

**表 302. pgbench 運算子**

<table border="1" class="table" summary="pgbench Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">OR</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        邏輯 OR
       </p>
<p>
<code class="literal">5 or 0</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">AND</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        邏輯 AND
       </p>
<p>
<code class="literal">3 and 0</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">NOT</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        邏輯 NOT
       </p>
<p>
<code class="literal">not false</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">IS [NOT] (NULL|TRUE|FALSE)</code>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        布林值測試
       </p>
<p>
<code class="literal">1 is null</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">ISNULL|NOTNULL</code>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        是否為 NULL 的測試
       </p>
<p>
<code class="literal">1 notnull</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">=</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        等於
       </p>
<p>
<code class="literal">5 = 4</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">&lt;&gt;</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        不等於
       </p>
<p>
<code class="literal">5 &lt;&gt; 4</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">!=</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        不等於
       </p>
<p>
<code class="literal">5 != 5</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">&lt;</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        小於
       </p>
<p>
<code class="literal">5 &lt; 4</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">&lt;=</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        小於或等於
       </p>
<p>
<code class="literal">5 &lt;= 4</code>
        → <code class="returnvalue">FALSE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">&gt;</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        大於
       </p>
<p>
<code class="literal">5 &gt; 4</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">&gt;=</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        大於或等於
       </p>
<p>
<code class="literal">5 &gt;= 4</code>
        → <code class="returnvalue">TRUE</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">|</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元 OR
       </p>
<p>
<code class="literal">1 | 2</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">#</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元 XOR
       </p>
<p>
<code class="literal">1 # 3</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">&amp;</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元 AND
       </p>
<p>
<code class="literal">1 &amp; 3</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元 NOT
       </p>
<p>
<code class="literal">~ 1</code>
        → <code class="returnvalue">-2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">&lt;&lt;</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元左移
       </p>
<p>
<code class="literal">1 &lt;&lt; 2</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">&gt;&gt;</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        位元右移
       </p>
<p>
<code class="literal">8 &gt;&gt; 2</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        加法
       </p>
<p>
<code class="literal">5 + 4</code>
        → <code class="returnvalue">9</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        減法
       </p>
<p>
<code class="literal">3 - 2.0</code>
        → <code class="returnvalue">1.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">*</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        乘法
       </p>
<p>
<code class="literal">5 * 4</code>
        → <code class="returnvalue">20</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">/</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        除法（若兩個輸入都是整數，結果會向零截斷）
       </p>
<p>
<code class="literal">5 / 3</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integer</code></em> <code class="literal">%</code> <em class="replaceable"><code>integer</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        模數（餘數）
       </p>
<p>
<code class="literal">3 % 2</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        取負值
       </p>
<p>
<code class="literal">- 2.0</code>
        → <code class="returnvalue">-2.0</code>
</p></td></tr></tbody></table>

<br>

<a id="PGBENCH-BUILTIN-FUNCTIONS"></a>

### 內建函式

[表 303](pgbench.md#PGBENCH-FUNCTIONS) 所列的函式內建於 pgbench 中，可用於出現在 [`\set`](pgbench.md#PGBENCH-METACOMMAND-SET) 中的運算式。

下表「範例」欄中以程式碼格式呈現的「an integer between 1 and 10」與「an integer between 0 and 3」，分別表示「介於 1 與 10 之間的整數」與「介於 0 與 3 之間的整數」。

<a id="PGBENCH-FUNCTIONS"></a>

**表 303. pgbench 函式**

<table border="1" class="table" summary="pgbench Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">abs</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue"></code> 與輸入相同的型別
       </p>
<p>
        絕對值
       </p>
<p>
<code class="literal">abs(-17)</code>
        → <code class="returnvalue">17</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">debug</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue"></code> 與輸入相同的型別
       </p>
<p>
        將引數印到 <span class="systemitem">stderr</span>，並傳回該引數。
       </p>
<p>
<code class="literal">debug(5432.1)</code>
        → <code class="returnvalue">5432.1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">double</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p>
        轉型為 double。
       </p>
<p>
<code class="literal">double(5432)</code>
        → <code class="returnvalue">5432.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">exp</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p>
        指數（<code class="literal">e</code> 的給定次方）
       </p>
<p>
<code class="literal">exp(1.0)</code>
        → <code class="returnvalue">2.718281828459045</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">greatest</code> ( <em class="replaceable"><code>number</code></em> [<span class="optional">, <code class="literal">...</code> </span>] )
        → <code class="returnvalue"></code> <code class="type">double</code>（若任一引數為 double），否則為 <code class="type">integer</code>
</p>
<p>
        從引數中選出最大的值。
       </p>
<p>
<code class="literal">greatest(5, 4, 3, 2)</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hash</code> ( <em class="parameter"><code>value</code></em> [<span class="optional">, <em class="parameter"><code>seed</code></em> </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        這是 <code class="function">hash_murmur2</code> 的別名。
       </p>
<p>
<code class="literal">hash(10, 5432)</code>
        → <code class="returnvalue">-5817877081768721676</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hash_fnv1a</code> ( <em class="parameter"><code>value</code></em> [<span class="optional">, <em class="parameter"><code>seed</code></em> </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <a class="ulink" href="https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function" target="_top">FNV-1a 雜湊</a>。
       </p>
<p>
<code class="literal">hash_fnv1a(10, 5432)</code>
        → <code class="returnvalue">-7793829335365542153</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">hash_murmur2</code> ( <em class="parameter"><code>value</code></em> [<span class="optional">, <em class="parameter"><code>seed</code></em> </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <a class="ulink" href="https://en.wikipedia.org/wiki/MurmurHash" target="_top">MurmurHash2 雜湊</a>。
       </p>
<p>
<code class="literal">hash_murmur2(10, 5432)</code>
        → <code class="returnvalue">-5817877081768721676</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">int</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        轉型為 integer。
       </p>
<p>
<code class="literal">int(5.4 + 3.8)</code>
        → <code class="returnvalue">9</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">least</code> ( <em class="replaceable"><code>number</code></em> [<span class="optional">, <code class="literal">...</code> </span>] )
        → <code class="returnvalue"></code> <code class="type">double</code>（若任一引數為 double），否則為 <code class="type">integer</code>
</p>
<p>
        從引數中選出最小的值。
       </p>
<p>
<code class="literal">least(5, 4, 3, 2.1)</code>
        → <code class="returnvalue">2.1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">ln</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p>
        自然對數
       </p>
<p>
<code class="literal">ln(2.718281828459045)</code>
        → <code class="returnvalue">1.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">mod</code> ( <em class="replaceable"><code>integer</code></em>, <em class="replaceable"><code>integer</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        模數（餘數）
       </p>
<p>
<code class="literal">mod(54, 32)</code>
        → <code class="returnvalue">22</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">permute</code> ( <em class="parameter"><code>i</code></em>, <em class="parameter"><code>size</code></em> [, <em class="parameter"><code>seed</code></em> ] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        <em class="parameter"><code>i</code></em> 排列後的值，範圍為
        <code class="literal">[0, size)</code>。這是
        <em class="parameter"><code>i</code></em>（模 <em class="parameter"><code>size</code></em>）在整數 <code class="literal">0...size-1</code> 的偽隨機排列中的新位置，
        該排列以 <em class="parameter"><code>seed</code></em> 為參數，請參閱下文。
       </p>
<p>
<code class="literal">permute(0, 4)</code>
        → <code class="returnvalue">an integer between 0 and 3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pi</code> ()
        → <code class="returnvalue">double</code>
</p>
<p>
        <span class="symbol_font">π</span> 的近似值
</p>
<p>
<code class="literal">pi()</code>
        → <code class="returnvalue">3.14159265358979323846</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pow</code> ( <em class="parameter"><code>x</code></em>, <em class="parameter"><code>y</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p class="func_signature">
<code class="function">power</code> ( <em class="parameter"><code>x</code></em>, <em class="parameter"><code>y</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p>
<em class="parameter"><code>x</code></em> 的 <em class="parameter"><code>y</code></em> 次方
</p>
<p>
<code class="literal">pow(2.0, 10)</code>
        → <code class="returnvalue">1024.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">random</code> ( <em class="parameter"><code>lb</code></em>, <em class="parameter"><code>ub</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <code class="literal">[lb,
        ub]</code> 中均勻分布的隨機整數。
       </p>
<p>
<code class="literal">random(1, 10)</code>
        → <code class="returnvalue">an integer between 1 and 10</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">random_exponential</code> ( <em class="parameter"><code>lb</code></em>, <em class="parameter"><code>ub</code></em>, <em class="parameter"><code>parameter</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <code class="literal">[lb,
        ub]</code> 中指數分布的隨機整數，請參閱下文。
       </p>
<p>
<code class="literal">random_exponential(1, 10, 3.0)</code>
        → <code class="returnvalue">an integer between 1 and 10</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">random_gaussian</code> ( <em class="parameter"><code>lb</code></em>, <em class="parameter"><code>ub</code></em>, <em class="parameter"><code>parameter</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <code class="literal">[lb,
        ub]</code> 中高斯分布的隨機整數，請參閱下文。
       </p>
<p>
<code class="literal">random_gaussian(1, 10, 2.5)</code>
        → <code class="returnvalue">an integer between 1 and 10</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">random_zipfian</code> ( <em class="parameter"><code>lb</code></em>, <em class="parameter"><code>ub</code></em>, <em class="parameter"><code>parameter</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        計算 <code class="literal">[lb,
        ub]</code> 中 Zipfian 分布的隨機整數，請參閱下文。
       </p>
<p>
<code class="literal">random_zipfian(1, 10, 1.5)</code>
        → <code class="returnvalue">an integer between 1 and 10</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sqrt</code> ( <em class="replaceable"><code>number</code></em> )
        → <code class="returnvalue">double</code>
</p>
<p>
        平方根
       </p>
<p>
<code class="literal">sqrt(2.0)</code>
        → <code class="returnvalue">1.414213562</code>
</p></td></tr></tbody></table>

<br>

`random` 函式使用均勻分布產生值，也就是所有的值都以相同的機率從指定範圍內抽取。`random_exponential`、`random_gaussian` 與 `random_zipfian` 函式需要一個額外的倍精度參數，用來決定分布的精確形狀。

* 對於指數分布，*`parameter`* 控制分布的方式，是在 *`parameter`* 處截斷一個快速遞減的指數分布，然後投影到界限之間的整數上。精確地說，令

  <br>
  f(x) = exp(-parameter \* (x - min) / (max - min + 1)) / (1 - exp(-parameter))<br>

  則介於 *`min`* 與 *`max`*（含兩端）之間的值 *`i`* 被抽取的機率為：`f(i) - f(i + 1)`。

  直觀來說，*`parameter`* 越大，接近 *`min`* 的值就越常被存取，接近 *`max`* 的值就越少被存取。*`parameter`* 越接近 0，存取分布就越平坦（越均勻）。此分布的一個粗略近似是：範圍中最常出現的 1% 值（接近 *`min`*）會有 *`parameter`*% 的時間被抽取。*`parameter`* 的值必須嚴格為正。
* 對於高斯分布，區間會對應到一個標準常態分布（經典的鐘形高斯曲線），並在左側的 `-parameter` 與右側的 `+parameter` 處截斷。區間中間的值較有可能被抽取。精確地說，若 `PHI(x)` 是標準常態分布的累積分布函式，平均值 `mu` 定義為 `(max + min) / 2.0`，並令

  <br>
  f(x) = PHI(2.0 \* parameter \* (x - mu) / (max - min + 1)) /<br>
         (2.0 \* PHI(parameter) - 1)<br>

  則介於 *`min`* 與 *`max`*（含兩端）之間的值 *`i`* 被抽取的機率為：`f(i + 0.5) - f(i - 0.5)`。直觀來說，*`parameter`* 越大，接近區間中間的值就越常被抽取，而接近 *`min`* 與 *`max`* 界限的值就越少被抽取。大約 67% 的值是從中間的 `1.0 / parameter` 抽取，也就是平均值周圍相對 `0.5 / parameter` 的範圍；95% 的值是從中間的 `2.0 / parameter` 抽取，也就是平均值周圍相對 `1.0 / parameter` 的範圍。例如，若 *`parameter`* 為 4.0，67% 的值是從區間中間的四分之一（1.0 / 4.0）抽取（也就是從 `3.0 / 8.0` 到 `5.0 / 8.0`），95% 的值是從區間中間的一半（`2.0 / 4.0`）抽取（第二與第三個四分位區間）。*`parameter`* 允許的最小值為 2.0。
* `random_zipfian` 產生有界的 Zipfian 分布。*`parameter`* 定義分布的偏斜程度。*`parameter`* 越大，越接近區間開頭的值就越常被抽取。此分布的性質是：假設範圍從 1 開始，抽取 *`k`* 與抽取 *`k+1`* 的機率比為 `((k+1)/k)**parameter`。例如，`random_zipfian(1, ..., 2.5)` 產生值 `1` 的頻率約為產生 `2` 的 `(2/1)**2.5 =
  5.66` 倍，而 2 本身被產生的頻率又約為 `3` 的 `(3/2)**2.5 = 2.76` 倍，依此類推。

  pgbench 的實作是以 Luc Devroye 所著 "Non-Uniform Random Variate Generation"（Springer 1986）第 550-551 頁為基礎。由於該演算法的限制，*`parameter`* 的值限定在 [1.001, 1000] 的範圍內。

<a id="PGBENCH-BUILTIN-FUNCTIONS-NOTE"></a>

### 注意

設計以非均勻方式選取資料列的效能基準時，請注意所選取的資料列可能與其他資料相關，例如來自序列的 ID 或資料列的實體順序，這可能使效能測量產生偏差。

為了避免這種情況，你可以考慮使用 `permute` 函式，或其他具有類似效果的額外步驟，來打亂所選取的資料列並消除這類相關性。

雜湊函式 `hash`、`hash_murmur2` 與 `hash_fnv1a` 接受一個輸入值與一個選擇性的種子參數。若未提供種子，則使用 `:default_seed` 的值；除非由命令列 `-D` 選項設定，否則該值會隨機初始化。

`permute` 接受一個輸入值、一個大小，以及一個選擇性的種子參數。它會產生範圍 `[0, size)` 中整數的偽隨機排列，並傳回輸入值在排列後的值之中的索引。所選擇的排列以種子為參數；若未指定，種子預設為 `:default_seed`。與雜湊函式不同，`permute` 確保輸出值中沒有碰撞或空洞。區間之外的輸入值會以大小取模來解讀。若大小不是正數，此函式會引發錯誤。`permute` 可以用來打散非均勻隨機函式（例如 `random_zipfian` 或 `random_exponential`）的分布，使較常被抽取的值不會有明顯的相關性。例如，下列 pgbench 腳本模擬社群媒體與部落格平台上一種可能的典型真實世界工作負載，其中少數帳戶產生過多的負載：

```

\set size 1000000
\set r random_zipfian(1, :size, 1.07)
\set k 1 + permute(:r, :size)
```

在某些情況下，需要數個彼此不相關的不同分布，這時選擇性的種子參數就派上用場了：

```

\set k1 1 + permute(:r, :size, :default_seed + 123)
\set k2 1 + permute(:r, :size, :default_seed + 321)
```

使用 `hash` 也可以近似類似的行為：

```

\set size 1000000
\set r random_zipfian(1, 100 * :size, 1.07)
\set k 1 + abs(hash(:r)) % :size
```

不過，由於 `hash` 會產生碰撞，有些值將無法到達，而其他值出現的頻率會比原始分布所預期的更高。

舉例來說，內建類 TPC-B 交易的完整定義如下：

```

\set aid random(1, 100000 * :scale)
\set bid random(1, 1 * :scale)
\set tid random(1, 10 * :scale)
\set delta random(-5000, 5000)
BEGIN;
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
END;
```

這個腳本讓交易的每次迭代都能參照不同的、隨機選取的資料列。（這個範例也說明了為什麼每個用戶端工作階段擁有自己的變數很重要——否則它們就不會各自獨立地存取不同的資料列。）

<a id="id-1.9.4.11.9.6"></a>

### 每筆交易的日誌

使用 `-l` 選項（但不使用 `--aggregate-interval` 選項）時，pgbench 會將每筆交易的相關資訊寫入日誌檔。日誌檔會命名為 `prefix.nnn`，其中 *`prefix`* 預設為 `pgbench_log`，而 *`nnn`* 是 pgbench 程序的 PID。前綴可以使用 `--log-prefix` 選項變更。若 `-j` 選項為 2 或更高，因而有多個工作執行緒，則每個執行緒都會有自己的日誌檔。第一個工作執行緒的日誌檔，會使用與標準單一工作執行緒情況相同的名稱。其他工作執行緒的額外日誌檔會命名為 `prefix.nnn.mmm`，其中 *`mmm`* 是每個工作執行緒從 1 開始的序號。

日誌檔中的每一行描述一筆交易。它包含下列以空格分隔的欄位：

*`client_id`*
:   識別執行該交易的用戶端工作階段

*`transaction_no`*
:   計算該工作階段已執行了多少筆交易

*`time`*
:   交易經過的時間，以微秒為單位

*`script_no`*
:   識別該交易所使用的腳本檔（在以 `-f` 或 `-b` 指定多個腳本時很有用）

*`time_epoch`*
:   交易的完成時間，以 Unix epoch 時間戳記表示

*`time_us`*
:   交易完成時間中不足一秒的部分，以微秒為單位

*`schedule_lag`*
:   交易開始延遲，也就是交易的排程開始時間與實際開始時間之間的差距，以微秒為單位（只有在指定 `--rate` 時才會出現）

*`retries`*
:   交易期間因序列化錯誤或死結錯誤而重試的次數（只有在 `--max-tries` 不等於 1 時才會出現）

同時使用 `--rate` 與 `--latency-limit` 時，被略過之交易的 *`time`* 會回報為 `skipped`。若交易以失敗告終，其 *`time`* 會回報為 `failed`。若你使用 `--failures-detailed` 選項，失敗交易的 *`time`* 會依失敗類型回報為 `serialization` 或 `deadlock`（詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)）。

以下是單一用戶端執行所產生之日誌檔的片段：

```

0 199 2241 0 1175850568 995598
0 200 2465 0 1175850568 998079
0 201 2513 0 1175850569 608
0 202 2038 0 1175850569 2663
```

另一個使用 `--rate=100` 與 `--latency-limit=5` 的範例（請注意額外的 *`schedule_lag`* 欄位）：

```

0 81 4621 0 1412881037 912698 3005
0 82 6173 0 1412881037 914578 4304
0 83 skipped 0 1412881037 914578 5217
0 83 skipped 0 1412881037 914578 5099
0 83 4722 0 1412881037 916203 3108
0 84 4142 0 1412881037 918023 2333
0 85 2465 0 1412881037 919759 740
```

在這個範例中，交易 82 延遲了，因為它的延遲時間（6.173 毫秒）超過了 5 毫秒的限制。接下來的兩筆交易被略過，因為它們在開始之前就已經延遲了。

下列範例顯示一個包含失敗與重試的日誌檔片段，最大嘗試次數設為 10（請注意額外的 *`retries`* 欄位）：

```

3 0 47423 0 1499414498 34501 3
3 1 8333 0 1499414498 42848 0
3 2 8358 0 1499414498 51219 0
4 0 72345 0 1499414498 59433 6
1 3 41718 0 1499414498 67879 4
1 4 8416 0 1499414498 76311 0
3 3 33235 0 1499414498 84469 3
0 0 failed 0 1499414498 84905 9
2 0 failed 0 1499414498 86248 9
3 4 8307 0 1499414498 92788 0
```

若使用 `--failures-detailed` 選項，失敗類型會在 *`time`* 中回報，如下所示：

```

3 0 47423 0 1499414498 34501 3
3 1 8333 0 1499414498 42848 0
3 2 8358 0 1499414498 51219 0
4 0 72345 0 1499414498 59433 6
1 3 41718 0 1499414498 67879 4
1 4 8416 0 1499414498 76311 0
3 3 33235 0 1499414498 84469 3
0 0 serialization 0 1499414498 84905 9
2 0 serialization 0 1499414498 86248 9
3 4 8307 0 1499414498 92788 0
```

在能夠處理大量交易的硬體上執行長時間測試時，日誌檔可能會變得非常大。可以使用 `--sampling-rate` 選項，只記錄交易的隨機樣本。

<a id="id-1.9.4.11.9.7"></a>

### 彙總日誌

使用 `--aggregate-interval` 選項時，日誌檔會使用不同的格式。每一行日誌描述一個彙總間隔。它包含下列以空格分隔的欄位：

*`interval_start`*
:   間隔的開始時間，以 Unix epoch 時間戳記表示

*`num_transactions`*
:   間隔內的交易數

*`sum_latency`*
:   交易延遲的總和

*`sum_latency_2`*
:   交易延遲的平方和

*`min_latency`*
:   最小交易延遲

*`max_latency`*
:   最大交易延遲

*`sum_lag`*
:   交易開始延遲的總和（除非指定 `--rate`，否則為零）

*`sum_lag_2`*
:   交易開始延遲的平方和（除非指定 `--rate`，否則為零）

*`min_lag`*
:   最小交易開始延遲（除非指定 `--rate`，否則為零）

*`max_lag`*
:   最大交易開始延遲（除非指定 `--rate`，否則為零）

*`skipped`*
:   因為會太晚開始而被略過的交易數（除非指定 `--rate` 與 `--latency-limit`，否則為零）

*`retried`*
:   重試過的交易數（除非 `--max-tries` 不等於 1，否則為零）

*`retries`*
:   因序列化錯誤或死結錯誤而重試的次數（除非 `--max-tries` 不等於 1，否則為零）

*`serialization_failures`*
:   發生序列化錯誤且之後未重試的交易數（除非指定 `--failures-detailed`，否則為零）

*`deadlock_failures`*
:   發生死結錯誤且之後未重試的交易數（除非指定 `--failures-detailed`，否則為零）

以下是使用此選項所產生的一些範例輸出：

```

pgbench --aggregate-interval=10 --time=20 --client=10 --log --rate=1000 --latency-limit=10 --failures-detailed --max-tries=10 test

1650260552 5178 26171317 177284491527 1136 44462 2647617 7321113867 0 9866 64 7564 28340 4148 0
1650260562 4808 25573984 220121792172 1171 62083 3037380 9666800914 0 9998 598 7392 26621 4527 0
```

請注意，一般（未彙總）的日誌格式會顯示每筆交易使用了哪個腳本，但彙總格式不會。因此，若你需要每個腳本的資料，就必須自行彙總資料。

<a id="id-1.9.4.11.9.8"></a>

### 每個陳述式的報告

使用 `-r` 選項時，pgbench 會為每個陳述式收集下列統計資料：

* `latency`——每個陳述式所經過的交易時間。pgbench 回報該陳述式所有成功執行的平均值。
* 此陳述式中的失敗次數。詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。
* 此陳述式中因序列化錯誤或死結錯誤而重試的次數。詳細資訊請參閱[失敗與序列化／死結重試](pgbench.md#FAILURES-AND-RETRIES)。

只有在 `--max-tries` 選項不等於 1 時，報告才會顯示重試統計資料。

所有的值都是針對每個用戶端所執行的每個陳述式計算，並在效能基準測試結束後回報。

對於預設腳本，輸出會類似這樣：

```

starting vacuum...end.
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 1
query mode: simple
number of clients: 10
number of threads: 1
maximum number of tries: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
number of failed transactions: 0 (0.000%)
number of transactions above the 50.0 ms latency limit: 1311/10000 (13.110 %)
latency average = 28.488 ms
latency stddev = 21.009 ms
initial connection time = 69.068 ms
tps = 346.224794 (without initial connection time)
statement latencies in milliseconds and failures:
   0.012  0  \set aid random(1, 100000 * :scale)
   0.002  0  \set bid random(1, 1 * :scale)
   0.002  0  \set tid random(1, 10 * :scale)
   0.002  0  \set delta random(-5000, 5000)
   0.319  0  BEGIN;
   0.834  0  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
   0.641  0  SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
  11.126  0  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
  12.961  0  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
   0.634  0  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
   1.957  0  END;
```

另一個預設腳本的輸出範例，使用 serializable 作為預設交易隔離等級（`PGOPTIONS='-c
default_transaction_isolation=serializable' pgbench ...`）：

```

starting vacuum...end.
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 1
query mode: simple
number of clients: 10
number of threads: 1
maximum number of tries: 10
number of transactions per client: 1000
number of transactions actually processed: 6317/10000
number of failed transactions: 3683 (36.830%)
number of transactions retried: 7667 (76.670%)
total number of retries: 45339
number of transactions above the 50.0 ms latency limit: 106/6317 (1.678 %)
latency average = 17.016 ms
latency stddev = 13.283 ms
initial connection time = 45.017 ms
tps = 186.792667 (without initial connection time)
statement latencies in milliseconds, failures and retries:
  0.006     0      0  \set aid random(1, 100000 * :scale)
  0.001     0      0  \set bid random(1, 1 * :scale)
  0.001     0      0  \set tid random(1, 10 * :scale)
  0.001     0      0  \set delta random(-5000, 5000)
  0.385     0      0  BEGIN;
  0.773     0      1  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
  0.624     0      0  SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
  1.098   320   3762  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
  0.582  3363  41576  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
  0.465     0      0  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
  1.933     0      0  END;
```

若指定了多個腳本檔，所有統計資料都會針對每個腳本檔分別回報。

請注意，收集計算每個陳述式延遲所需的額外計時資訊，會增加一些額外負擔。這會減慢平均執行速度，並降低計算出的 TPS。減慢的程度會因平台與硬體而有顯著差異。比較啟用與未啟用延遲回報時的平均 TPS 值，是衡量計時額外負擔是否顯著的好方法。

<a id="FAILURES-AND-RETRIES"></a>

### 失敗與序列化／死結重試

執行 pgbench 時，主要有三種類型的錯誤：

* 主程式的錯誤。這類錯誤最為嚴重，一律會導致 pgbench 立即結束並顯示對應的錯誤訊息。這類錯誤包括：

  * pgbench 啟動時的錯誤（例如無效的選項值）；
  * 初始化模式中的錯誤（例如為內建腳本建立資料表的查詢失敗）；
  * 啟動執行緒之前的錯誤（例如無法連線到資料庫伺服器、中繼命令的語法錯誤、執行緒建立失敗）；
  * pgbench 的內部錯誤（理應永遠不會發生……）。
* 執行緒管理其用戶端時的錯誤（例如用戶端無法啟動與資料庫伺服器的連線／用於將用戶端連線到資料庫伺服器的 socket 已變得無效）。在這類情況下，此執行緒的所有用戶端都會停止，而其他執行緒則繼續運作。不過，若指定了 `--exit-on-abort`，在這種情況下所有執行緒都會立即停止。
* 用戶端的直接錯誤。在 pgbench 內部錯誤（理應永遠不會發生……）的情況下，或指定了 `--exit-on-abort` 時，這類錯誤會導致 pgbench 立即結束並顯示對應的錯誤訊息。否則，在最壞的情況下，這類錯誤只會導致失敗的用戶端中止，而其他用戶端繼續執行（但有些用戶端錯誤的處理方式不會中止用戶端，並會另外回報，請參閱下文）。在本節後續內容中，假定所討論的錯誤只有用戶端的直接錯誤，而且不是 pgbench 的內部錯誤。

發生嚴重錯誤時，用戶端的執行會被中止；例如，與資料庫伺服器的連線中斷，或在未完成最後一筆交易的情況下到達腳本結尾。此外，若 SQL 命令或中繼命令的執行因序列化錯誤或死結錯誤以外的原因而失敗，用戶端會被中止。否則，若 SQL 命令因序列化錯誤或死結錯誤而失敗，用戶端不會被中止。在這類情況下，目前的交易會被復原，這也包括將用戶端變數設回執行此交易之前的狀態（這裡假定一個交易腳本只包含一筆交易；詳細資訊請參閱[pgbench 中實際執行的「交易」是什麼？](pgbench.md#TRANSACTIONS-AND-SCRIPTS)）。發生序列化錯誤或死結錯誤的交易，會在復原之後重複執行，直到成功完成，或達到最大嘗試次數（由 `--max-tries` 選項指定）／重試的最長時間（由 `--latency-limit` 選項指定）／效能基準測試的結束（由 `--time` 選項指定）為止。若最後一次嘗試執行失敗，此交易會被回報為失敗，但用戶端不會被中止，並繼續運作。

<a id="FAILURES-AND-RETRIES-NOTE"></a>

### 注意

若未指定 `--max-tries` 選項，交易在發生序列化錯誤或死結錯誤後永遠不會重試，因為其預設值為 1。若只要限制嘗試的最長時間，請使用無限次的嘗試（`--max-tries=0`）並搭配 `--latency-limit` 選項。在無限次嘗試之下，你也可以使用 `--time` 選項來限制效能基準測試的持續時間。

重複執行包含多筆交易的腳本時要小心：腳本一律會被完整重試，因此成功的交易可能會被執行數次。

重複執行包含 shell 命令的交易時要小心。與 SQL 命令的結果不同，shell 命令的結果不會被復原，但 `\setshell` 命令的變數值除外。

成功交易的延遲包含交易執行的全部時間，含復原與重試。延遲只針對成功的交易與命令測量，而不針對失敗的交易或命令測量。

主要報告包含失敗交易數。若 `--max-tries` 選項不等於 1，主要報告也會包含與重試相關的統計資料：重試過的交易總數與重試總次數。每個腳本的報告會從主要報告繼承所有這些欄位。只有在 `--max-tries` 選項不等於 1 時，每個陳述式的報告才會顯示重試統計資料。

若你想在每筆交易日誌與彙總日誌中，以及在主要報告與每個腳本的報告中，依基本類型將失敗分組，請使用 `--failures-detailed` 選項。若你還想依類型區分所有錯誤與失敗（未重試的錯誤），對於序列化／死結失敗還包括超過了哪一個重試限制，以及超過了多少，請使用 `--verbose-errors` 選項。

<a id="id-1.9.4.11.9.10"></a>

### 資料表存取方法

你可以為 pgbench 資料表指定[資料表存取方法](../../internals/tableam/README.md)。環境變數 `PGOPTIONS` 指定透過命令列傳給 PostgreSQL 的資料庫組態選項（請參閱[第 19.1.4 節](../../server-administration/runtime-config/config-setting.md#config-setting-shell)）。例如，可以用下列方式，為 pgbench 所建立的資料表指定一個名為 `wuzza` 的假想預設資料表存取方法：

```

PGOPTIONS='-c default_table_access_method=wuzza'
```

<a id="id-1.9.4.11.9.11"></a>

### 良好實務

使用 pgbench 產生完全沒有意義的數字是非常容易的。以下是一些可幫助你取得有用結果的準則。

首先，*絕對不要*相信任何只執行幾秒鐘的測試。請使用 `-t` 或 `-T` 選項讓執行至少持續幾分鐘，以平均掉雜訊。在某些情況下，你可能需要數小時才能得到可重現的數字。多試跑幾次測試，以確認你的數字是否可重現，是個好主意。

對於預設的類 TPC-B 測試情境，初始化縮放因子（`-s`）應該至少與你打算測試的最大用戶端數（`-c`）一樣大；否則你測量到的大多會是更新競爭。`pgbench_branches` 資料表中只有 `-s` 個資料列，而每筆交易都要更新其中一列，因此超過 `-s` 的 `-c` 值，無疑會導致許多交易因等待其他交易而被阻擋。

預設的測試情境對於資料表初始化後經過了多久也相當敏感：資料表中死亡資料列與無用空間的累積會改變結果。要理解結果，你必須追蹤更新的總數以及清理發生的時機。若啟用了 autovacuum，可能會導致測得的效能出現無法預期的變化。

pgbench 的一個限制是，在嘗試測試大量用戶端工作階段時，它本身可能成為瓶頸。在與資料庫伺服器不同的機器上執行 pgbench 可以緩解這個問題，不過低網路延遲將是不可或缺的。在數台用戶端機器上，針對同一個資料庫伺服器同時執行數個 pgbench 實例，甚至可能也有幫助。

<a id="id-1.9.4.11.9.12"></a>

### 安全性

若不受信任的使用者可以存取一個尚未採用[安全的綱要使用模式](../../the-sql-language/ddl/ddl-schemas.md#ddl-schemas-patterns)的資料庫，請不要在該資料庫中執行 pgbench。pgbench 使用未限定的名稱，而且不會操作搜尋路徑。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbench.html)（原文版本：18.6；核對日期：2026-10-10）
