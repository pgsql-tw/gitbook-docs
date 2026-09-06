# pgbench

pgbench — 進行 PostgreSQL 效能評估

## 語法

`pgbench-i`\[`option`...] \[`dbname`]

`pgbench`\[`option`...] \[`dbname`]

## 說明

pgbench 是一個簡易型 PostgreSQL 的效能評估工具。它可以重覆執行某一系列的 SQL 指令，也可能進行大量連線的模擬情境，然後計算其平均的交易完成率（TPS, Transaction Per Second）。預設上，pgbench 使用的是 TPC-B 的標準情境，它在 1 個資料交易中會進行 5 個階段的資料操作，包含 SELECT、UPDATE、INSERT 指令。然而，你也可以使用你的腳本檔案，輕易地評估其他不同的情境。

pgbench 大致上的輸出如下：

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

前 7 行列出了一些最主要的參數設定。第 6 行說明了 serialization 或 deadlock 交易錯誤的最大嘗試次數（相關更多資訊，請參閱“Failures and Serialization/Deadlock Retries”）。第 8 行為已完成的交易數量和預期的交易數量（後者是用戶端數量和每個用戶端的交易數量的乘積）；除非在完成前有交易失敗或某些 SQL 命令錯誤，否則這兩個值應該要相等。 （在 -T 模式下，僅列出實際的交易數量。）再接下來一行則列出由於序列化或死鎖錯誤而失敗的交易數量（相關更多資訊，請參閱“Failures and Serialization/Deadlock Retries”）。最後一行則為每秒的交易數量。

預設使用的 TPC-B 情境評估需要特定的資料庫結構，它們必須要在測試前先建立好。所以在測試之前，要先以「-i」參數執行初始化資料庫結構。（如果你使用自訂的情境測試，那就不需要進行這個步驟，但你可能需要另外自行建立你所需要的資料庫結構。）初始化指令如下：

```
pgbench -i [other-options] dbname
```

dbname 必須是已經存在的資料庫。（也許你還需要再加上 -h、-p、-U 等參數來設定資料庫的連線參數。）

###

{% hint style="info" %}
pgbench -i 將會建立 4 個表格：pgbench\_accounts、pgbench\_branches、pgbench\_history、以及 pgbench\_tellers。它會取代掉同名的表格。所以你如果和既有的資料庫共用的話，請注意同名的問題！
{% endhint %}

預設上，「scale factor」設定為 1，所產生的資料筆數如下：

```
table                   # of rows
---------------------------------
pgbench_branches        1
pgbench_tellers         10
pgbench_accounts        100000
pgbench_history         0
```

通常會使用 -s 參數來增加測試資料的數量。選項 -F 也可能在這時候使用。

一旦你完成了這個初始化的動作之後，後續的測試就不需要加上 -i 了：

```
pgbench [options] dbname
```

一般來說，你還會需要加上其他選項以進行更有意義的測試。最主要的測試選項為 -c （模擬用戶數量）、-t（資料交易數量）、-T（限時測試）、還有 -F（指定一個自訂的腳本檔案）。完整選項如下。

## 選項

下面的部份分成三個小節：資料庫初始化專用選項、評估階段專用選項、一些通用的選項。

### 資料庫初始化專用選項

pgbench 在資料庫初始化時可以使用下列選項：

`[-d]`` `_`dbname`_\
`[--dbname=]`_`dbname`_&#x20;

指定要測試的資料庫名稱。如果未指定的話，則會參考環境變數 `PGDATABASE` 。如果都沒有設定的話，將會使用建立連線的使用者名稱作為資料庫名稱。

`-i`

`--initialize`

Perform just a selected set of the normal initialization steps. _`init_steps`_ specifies the initialization steps to be performed, using one character per step. Each step is invoked in the specified order. The default is `dtgvp`. The available steps are:

`d` (Drop)&#x20;

Drop any existing pgbench tables.

`t` (create Tables)&#x20;

Create the tables used by the standard pgbench scenario, namely `pgbench_accounts`, `pgbench_branches`, `pgbench_history`, and `pgbench_tellers`.

`g` or `G` (Generate data, client-side or server-side)&#x20;

Generate data and load it into the standard tables, replacing any data already present.

With `g` (client-side data generation), data is generated in `pgbench` client and then sent to the server. This uses the client/server bandwidth extensively through a `COPY`. `pgbench` uses the `FREEZE` option with version 14 or later of PostgreSQL to speed up subsequent `VACUUM`, except on the `pgbench_accounts` table if partitions are enabled. Using `g` causes logging to print one message every 100,000 rows while generating data for all tables.

With `G` (server-side data generation), only small queries are sent from the `pgbench` client and then data is actually generated in the server. No significant bandwidth is required for this variant, but the server will do more work. Using `G` causes logging not to print any progress message while generating data.

The default initialization behavior uses client-side data generation (equivalent to `g`).

`v` (Vacuum)&#x20;

Invoke `VACUUM` on the standard tables.

`p` (create Primary keys)&#x20;

Create primary key indexes on the standard tables.

`f` (create Foreign keys)&#x20;

Create foreign key constraints between the standard tables. (Note that this step is not performed by default.)

`-F fillfactor`

`--fillfactor=fillfactor`

建立 4 個表格：pgbench\_accounts、pgbench\_branches、pgbench\_history、以及 pgbench\_tellers。以預設的 fillfactor 填入資料，其預設值為 100。

`-n`

`--no-vacuum`

在初始化後不要進行資料庫整理（vacuum）的動作。

`-q`

`--quiet`

切換為安靜模式，只會每 5 秒輸出執行階段訊息。預設的模式是每 10,000 筆資料就輸出訊息，通常每秒都有很多行訊息產生（特別是在一些比較好的硬體上執行時）。

`-s scale_factor`

`--scale=scale_factor`

資料的數量是以 scale factor 的倍數來計算的。舉例來說，-s 100 將會在表格 pgbench\_accounts 中產生 10,000,000 筆資料。其預設為 1。當 scale 到達 20,000 以上時，欄位 aid 就會宣告為 bigint，以有足夠的數值空間來處理。

`--foreign-keys`

在標準的表格結構之間建立外部鍵。

`--index-tablespace=index_tablespace`

把索引建在指定的表格空間（tablespace），而非預設的表格空間。

`--partition-method=`_`NAME`_&#x20;

Create a partitioned `pgbench_accounts` table with _`NAME`_ method. Expected values are `range` or `hash`. This option requires that `--partitions` is set to non-zero. If unspecified, default is `range`.

`--partitions=`_`NUM`_&#x20;

Create a partitioned `pgbench_accounts` table with _`NUM`_ partitions of nearly equal size for the scaled number of accounts. Default is `0`, meaning no partitioning.

`--tablespace=tablespace`

把表格建在指定的表格空間，而非預設的表格空間。

`--unlogged-tables`

把所有表格都建立成無日誌表格，而不是永久性表格。

### 評估階段專用選項

pgbench 在評估階段可使用下列選項：

`-b scriptname[@weight]`

`--builtin`=`scriptname[@weight]`

這個選項用於指定要使用哪一個內建的評估情境。而在 @ 後面可以給一個整數，調整產生腳本的機率參數。如果未指定的話，就會設定為 1。目前內建的情境是：tpcb-like、simple-update、select-only。只要是明確內建名稱的前置縮寫（如：tpc、simple、select）都是可以接受的。而有一個特別的名稱是 list，使用這個名稱的話，就只是列出有哪些內建的情境。

`-c clients`

`--client=clients`

模擬用戶的數量，指的是同一時間連入資料庫的連線數。預設為 1。

`-C`

`--connect`

在每一個交易執行前都重新建立連線，而不是都在同一個用戶連線中完成全部交易。這在測試連線成本時特別有用。

`-D varname=value`

`--define=varname=value`

定義給自訂腳本使用的變數。你可以使用多個 -D 來定義多個變數。

`-f filename[@weight]`

`--file=filename[@weight]`

從 filename 所指的檔案取得腳本，組成一個資料交易區段。選擇性的參數 @，後面接的整數，用來調整使用此腳本的機率。詳情後述。

`-j threads`

`--jobs=threads`

pgbench 執行緒的數量，能夠有效利用多 CPU 的運算能力。模擬用戶會盡可能平均分配在不同執行緒中執行。預設值為 1。

`-l`

`--log`

把執行的記錄存到檔案之中，後續詳述。

`-L limit`

`--latency-limit=limit`

交易執行時間超過 limit 以上時，將會被特別計算回報。其單位是 millisecond（千分之一秒）。

而如果也使用了「--rate=...」限流時，被評估一定會超時的交易，就會被跳過不執行，而它們也會被特別回報。

`-M querymode`

`--protocol=querymode`

選擇傳送指令的通訊協定：

* `simple`: 簡單查詢協定。
* `extended`: 延伸查詢協定。
* `prepared`: 延伸查詢協定，並使用預備宣告（prepared statement）方式。

預設是使用簡單查詢協定。（有關查詢協定，請參閱[第 52 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vii-internals/frontendbackend-protocol.md)）

`-n`

`--no-vacuum`

在執行測試評估前不要清理資料庫。如果你使用的是自訂的腳本，而且不包含前述四個內建表格的話，那這個選項是必要的。

`-N`

`--skip-some-updates`

使用內建的 simple-update 腳本，和 -b simple-update 是一樣的。

`-P sec`

`--progress=sec`

設定每 sec 秒回報一次進度。這個進度回報包含了執行累計時間，目前的 TPS 情況，還有每個進度階段的交易延遲時間平均值與標準差。如果使用 -R 的話，那麼延遲時間是相對於排定的啓動時間，而不是實際開始執行的時間，也就是說，它包含了平均的延遲時間。

`-r`

`--report-latencies`

回報每一個指令中每個語的平均回應時間。詳情後述。

`-R rate`

`--rate=rate`

執行的方式改為頻率而不是盡可能快速執行（預設）。執行頻率以 TPS 來指定。如果目標執行頻率高於最大可能的執行頻率的話，那就沒有意義。

目標執行頻率是以帕松分配（Poisson-distributed）來安排啓動時間的。預期的啓動時間表會隨用戶第一次開始的時間移動，而不是前一次交易結束的時間。這個方法表示，如果有交易誤點了，它仍有機會隨後趕上。

當限流機制啓動時，最後就會得到交易延遲的報告，其相對的是預排的啓動時間，所以它包含了每個交易必須要等待執行前的時間。等待時間稱作排程延遲時間，而其平均延遲與最大延遲都會被回報。交易延遲是相對於真正的開始執行間時，也就是說，交易在資料庫內被執行的時間，可視為是回報的延遲時間減去排程延遲時間。

如果 --latency-limit 和 --rate 兩個選項一起使用的話，交易可能會落後很多，當前一個交易結束時就已經超時了，因為超時是以排程的開始時間計算的。像這樣的交易就不會被執行了，它會被跳過，然後被統計出來。

如果一個系統有很長的排程延遲時間，那表示這個系統無法負擔超過某個執行頻率，當然需要搭配某個數量的用戶數及執行緒數。當平均的交易執行時間長於兩個交易排定的區間時，每一個接續的交易就會接著失敗，而排程延遲就會更長。當這種情況發生時，你就需要降低執行的頻率。

`-s scale_factor`

`--scale=scale_factor`

回報資料庫初始化的 scale factor。對於內建的測試而言，這個選項並不需要；其正確的 scale factor 將會自動以資料表 pgbench\_branches 的資料筆數計算而得。而如果測試使用的是自訂的情境腳步的話（選項 -f），那會回報 1。

`-S`

`--select-only`

執行內建 select-only 的情境腳步，等同於 -b select-only。

`-t transactions`

`--transactions=transactions`

每一個模擬用戶端要執行的交易數量，預設為 10。

`-T seconds`

`--time=seconds`

執行限時測試（以秒為單位），而不是固定的交易數量。-t 和 -T 是互斥的選項。

`-v`

`--vacuum-all`

在執行測試之前，先整理四個標準的資料表。如果沒有 -n 或 -v 的話，pgbench 會整理 pgbench\_tellers 和 pgbench\_branches，然後清空 pgbench\_history。

`--aggregate-interval=seconds`

彙整資訊的間隔時間（以秒為單位），通常只和 -l 選項一起使用。這個選項的執行記錄，將會包含每個間隔時間如上所述的彙整資料。

`--exit-on-abort`&#x20;

Exit immediately when any client is aborted due to some error. Without this option, even when a client is aborted, other clients could continue their run as specified by `-t` or `-T` option, and pgbench will print an incomplete results in this case.

Note that serialization failures or deadlock failures do not abort the client, so they are not affected by this option. See [Failures and Serialization/Deadlock Retries](https://www.postgresql.org/docs/current/pgbench.html#FAILURES-AND-RETRIES) for more information.

`--failures-detailed`&#x20;

Report failures in per-transaction and aggregation logs, as well as in the main and per-script reports, grouped by the following types:

* serialization failures;
* deadlock failures;

See [Failures and Serialization/Deadlock Retries](https://www.postgresql.org/docs/current/pgbench.html#FAILURES-AND-RETRIES) for more information.

`--log-prefix=prefix`

設定 --log 所建立檔案的檔名前置名稱。預設是 pgbench\_log。

`--max-tries=`_`number_of_tries`_&#x20;

Enable retries for transactions with serialization/deadlock errors and set the maximum number of these tries. This option can be combined with the `--latency-limit` option which limits the total time of all transaction tries; moreover, you cannot use an unlimited number of tries (`--max-tries=0`) without `--latency-limit` or `--time`. The default value is 1 and transactions with serialization/deadlock errors are not retried. See [Failures and Serialization/Deadlock Retries](https://www.postgresql.org/docs/current/pgbench.html#FAILURES-AND-RETRIES) for more information about retrying such transactions.

`--progress-timestamp`

當顯示進度（選項 -P）時，使用時間戳記（Unix epoch）取代相對的執行時間。其單位是秒，精確度至千分之一秒。這個選項用於在多種操作工具間比較時間。

`--random-seed=`_`seed`_&#x20;

Set random generator seed. Seeds the system random number generator, which then produces a sequence of initial generator states, one for each thread. Values for _`seed`_ may be: `time` (the default, the seed is based on the current time), `rand` (use a strong random source, failing if none is available), or an unsigned decimal integer value. The random generator is invoked explicitly from a pgbench script (`random...` functions) or implicitly (for instance option `--rate` uses it to schedule transactions). When explicitly set, the value used for seeding is shown on the terminal. Any value allowed for _`seed`_ may also be provided through the environment variable `PGBENCH_RANDOM_SEED`. To ensure that the provided seed impacts all possible uses, put this option first or use the environment variable.

Setting the seed explicitly allows to reproduce a `pgbench` run exactly, as far as random numbers are concerned. As the random state is managed per thread, this means the exact same `pgbench` run for an identical invocation if there is one client per thread and there are no external or data dependencies. From a statistical viewpoint reproducing runs exactly is a bad idea because it can hide the performance variability or improve performance unduly, e.g., by hitting the same pages as a previous run. However, it may also be of great help for debugging, for instance re-running a tricky case which leads to an error. Use wisely.

`--sampling-rate=rate`

取樣率，用於寫入資料到記錄檔時，可以減少記錄的輸出量。如果使用這個選項的話，只有指定比率的記錄會被輸出。如果是 1.0 的話，表示所有記錄都要輸出；而 0.05 的話，表示只輸出 5% 的記錄。

記得取樣率指的是輸出到記錄檔的比率，舉例來說，當計算 TPS 數值時，你會需要多個樣本數來彙整（使用 0.01 的取樣率時，你就只會得到原來百分之一個 TPS 數值輸出）。

`--show-script=`_`scriptname`_&#x20;

Show the actual code of builtin script _`scriptname`_ on stderr, and exit immediately.

`--verbose-errors`&#x20;

Print messages about all errors and failures (errors without retrying) including which limit for retries was exceeded and how far it was exceeded for the serialization/deadlock failures. (Note that in this case the output can be significantly increased.) See [Failures and Serialization/Deadlock Retries](https://www.postgresql.org/docs/current/pgbench.html#FAILURES-AND-RETRIES) for more information.

### 通用選項

以下是 pgbench 所支援的通用選項：

`-h hostname`

`--host=hostname`

資料庫伺服器的主機名稱。

`-p port`

`--port=port`

資料庫伺服器的連接埠號碼。

`-U login`

`--username=login`

連線時要使用的使用者名稱。

`-V`

`--version`

輸出 pgbench 的版本資訊，然後就結束程式。

`-?`

`--help`

顯示 pgbench 的命令列操作資訊，然後結束程式。

### Exit Status

A successful run will exit with status 0. Exit status 1 indicates static problems such as invalid command-line options or internal errors which are supposed to never occur. Early errors that occur when starting benchmark such as initial connection failures also exit with status 1. Errors during the run such as database errors or problems in the script will result in exit status 2. In the latter case, pgbench will print partial results if `--exit-on-abort` option is not specified.

### Environment

`PGDATABASE`\
`PGHOST`\
`PGPORT`\
`PGUSER`&#x20;

Default connection parameters.

This utility, like most other PostgreSQL utilities, uses the environment variables supported by libpq (see [Section 32.15](https://www.postgresql.org/docs/current/libpq-envars.html)).

The environment variable `PG_COLOR` specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

## 進階說明

### 實際上是什麼樣的交易在 pgbench 中執行呢？

pgbench 會隨機選取在某個列表中的腳本來執行，包含了使用 -b 的內建腳本及 -f 的自訂腳本。每一個腳本都可以使用 @ 來指定其被選取的機率。預設為 1，而設為 0 的話就會被忽略。

預設內建的交易腳本（也就是 -b tpcb-like），使用了七個指令，並且自動隨機代入不同變數：aid、tid、bid、和 balance。這個情境來自於 TPC-B 標準，但不完全符合 TPC-B，所以取名為 tpcb-like。

1. `BEGIN;`
2. `UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;`
3. `SELECT abalance FROM pgbench_accounts WHERE aid = :aid;`
4. `UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;`
5. `UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;`
6. `INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);`
7. `END;`

如果你選擇了 simple-update（也是 -N），那麼就不包含步驟 4 和 5。它會避免在這些資料表更新資料的競爭行為，但會接近 TPC-B 一些。

如果你使用了 select-only（也是 -S），就會只有 SELECT 的部份被執行。

### 自訂腳本

pgbench 支援使用自訂的情境腳步取代內建的測試腳本（如上所述），透過選項 -f 從檔案取得。這種情況的話，一個交易指的就是一個腳本檔案執行一次。

腳本檔案包含一個或多個 SQL 指令，以分號分隔結尾。空白行和以 -- 開頭的行都會被忽略。腳本檔案也可以包含「中繼指令（meta commands）」，用於 pgbench 執行測試時的參考指令，詳述於後。

{% hint style="info" %}
在 PostgreSQL 9.6 之前，腳本檔案裡的 SQL 指令是以換行結尾的，也就是不能跨行。現在使用分號是必要的了，在分隔連續的 SQL 指令時，你得加上分號（但如果這個 SQL 指令是由中繼指令所執行的話，就不需要分號）。如果你需要建立一份相容性的腳本檔案的話，請確認你的每一條 SQL 指令都是單行，並且以分號結尾。
{% endhint %}

腳本檔案可以進行簡易的變數代換動作。變數可以由命令列的 -D 來設定，或使用下面所介紹的中繼指令。進一步來說，任何變數都可以使用 -D 選項來預先設定，而在 Table 240 的變數則會自動產生。一旦設定好之後，變數內容就可以使用 :variablename 的形式放入 SQL 指令之中。而每一個模擬用戶的連線中，他們都擁有他們自己的變數內容。

**Table 298. pgbench Automatic Variables**

| Variable       | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `client_id`    | unique number identifying the client session (starts from zero)     |
| `default_seed` | seed used in hash and pseudorandom permutation functions by default |
| `random_seed`  | random generator seed (unless overwritten with `-D`)                |
| `scale`        | current scale factor                                                |

中繼指令是以倒斜線（\）開頭的指令，一般就到行末結尾，而如果要多行的話，就在行末再加倒斜線。中繼指令的參數是以空白分隔。支援的中繼指令有：

`\gset [`_`prefix`_`]` `\aset [`_`prefix`_`]`&#x20;

These commands may be used to end SQL queries, taking the place of the terminating semicolon (`;`).

When the `\gset` command is used, the preceding SQL query is expected to return one row, the columns of which are stored into variables named after column names, and prefixed with _`prefix`_ if provided.

When the `\aset` command is used, all combined SQL queries (separated by `\;`) have their columns stored into variables named after column names, and prefixed with _`prefix`_ if provided. If a query returns no row, no assignment is made and the variable can be tested for existence to detect this. If a query returns more than one row, the last value is kept.

`\gset` and `\aset` cannot be used in pipeline mode, since the query results are not yet available by the time the commands would need them.

The following example puts the final account balance from the first query into variable _`abalance`_, and fills variables _`p_two`_ and _`p_three`_ with integers from the third query. The result of the second query is discarded. The result of the two last combined queries are stored in variables _`four`_ and _`five`_.

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

`\if` _`expression`_\
`\elif` _`expression`_\
`\else`\
`\endif`&#x20;

This group of commands implements nestable conditional blocks, similarly to `psql`'s [`\if` _`expression`_](https://www.postgresql.org/docs/current/app-psql.html#PSQL-METACOMMAND-IF). Conditional expressions are identical to those with `\set`, with non-zero values interpreted as true.

`\set varname expression`

以 expression 表示式來計算 varname 數變的內容。表示式也可能包含整數常數，像 5432；或雙精確度浮點數 3.14159；或引用其他變數計算而得的表示式，可以使用的函數如後所述。

例如：

```
\set ntellers 10 * :scale
\set aid (1021 * random(1, 100000 * :scale)) % \
           (100000 * :scale) + 1
```

`\sleep number`\[ us | ms | s ]

使腳本執行暫停一段指定的時間，百萬分之一秒（us）、千分之一秒（ms）、或秒(s）。如果省略單位的話，預設是秒。nubmer 可以是整數常數，或引用其他整數變數的內容。

例如：

```
\sleep 10 ms
```

`\setshell varname command`\[`argument`... ]

設定 varname 的內容是執行另一個命令列指令的結果。該命令列指令必須透過標準輸出回傳整數。

command 和每一個 argument 都可以是文字常數或使用 :variablename 引用其他變數內容。如果你要使用 argument 的話，以冒號開始，而第一個 argument 要再多一個冒號。

例如：

```
\setshell variable_to_be_assigned command literal_argument :variable ::literal_starting_with_colon
```

`\shell command`\[`argument`... ]

和 \setshell 一樣，只是不處理回傳值。

例如：

```
\shell command literal_argument :variable ::literal_starting_with_colon
```

#### Built-in Operators

The arithmetic, bitwise, comparison and logical operators listed in [Table 299](https://www.postgresql.org/docs/current/pgbench.html#PGBENCH-OPERATORS) are built into pgbench and may be used in expressions appearing in [`\set`](https://www.postgresql.org/docs/current/pgbench.html#PGBENCH-METACOMMAND-SET). The operators are listed in increasing precedence order. Except as noted, operators taking two numeric inputs will produce a double value if either input is double, otherwise they produce an integer result.

**Table 299. pgbench Operators**

| <p>Operator</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><em><code>boolean</code></em> <code>OR</code> <em><code>boolean</code></em> → <em><code>boolean</code></em></p><p>Logical OR</p><p><code>5 or 0</code> → <code>TRUE</code></p>                                                       |
| <p><em><code>boolean</code></em> <code>AND</code> <em><code>boolean</code></em> → <em><code>boolean</code></em></p><p>Logical AND</p><p><code>3 and 0</code> → <code>FALSE</code></p>                                                   |
| <p><code>NOT</code> <em><code>boolean</code></em> → <em><code>boolean</code></em></p><p>Logical NOT</p><p><code>not false</code> → <code>TRUE</code></p>                                                                                |
| <p><em><code>boolean</code></em> <code>IS [NOT] (NULL|TRUE|FALSE)</code> → <em><code>boolean</code></em></p><p>Boolean value tests</p><p><code>1 is null</code> → <code>FALSE</code></p>                                                |
| <p><em><code>value</code></em> <code>ISNULL|NOTNULL</code> → <em><code>boolean</code></em></p><p>Nullness tests</p><p><code>1 notnull</code> → <code>TRUE</code></p>                                                                    |
| <p><em><code>number</code></em> <code>=</code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Equal</p><p><code>5 = 4</code> → <code>FALSE</code></p>                                                               |
| <p><em><code>number</code></em> <code>&#x3C;></code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Not equal</p><p><code>5 &#x3C;> 4</code> → <code>TRUE</code></p>                                                |
| <p><em><code>number</code></em> <code>!=</code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Not equal</p><p><code>5 != 5</code> → <code>FALSE</code></p>                                                         |
| <p><em><code>number</code></em> <code>&#x3C;</code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Less than</p><p><code>5 &#x3C; 4</code> → <code>FALSE</code></p>                                                 |
| <p><em><code>number</code></em> <code>&#x3C;=</code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Less than or equal to</p><p><code>5 &#x3C;= 4</code> → <code>FALSE</code></p>                                   |
| <p><em><code>number</code></em> <code>></code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Greater than</p><p><code>5 > 4</code> → <code>TRUE</code></p>                                                         |
| <p><em><code>number</code></em> <code>>=</code> <em><code>number</code></em> → <em><code>boolean</code></em></p><p>Greater than or equal to</p><p><code>5 >= 4</code> → <code>TRUE</code></p>                                           |
| <p><em><code>integer</code></em> <code>|</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise OR</p><p><code>1 | 2</code> → <code>3</code></p>                                                            |
| <p><em><code>integer</code></em> <code>#</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise XOR</p><p><code>1 # 3</code> → <code>2</code></p>                                                           |
| <p><em><code>integer</code></em> <code>&#x26;</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise AND</p><p><code>1 &#x26; 3</code> → <code>1</code></p>                                                 |
| <p><code>~</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise NOT</p><p><code>~ 1</code> → <code>-2</code></p>                                                                                          |
| <p><em><code>integer</code></em> <code>&#x3C;&#x3C;</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise shift left</p><p><code>1 &#x3C;&#x3C; 2</code> → <code>4</code></p>                              |
| <p><em><code>integer</code></em> <code>>></code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Bitwise shift right</p><p><code>8 >> 2</code> → <code>2</code></p>                                                 |
| <p><em><code>number</code></em> <code>+</code> <em><code>number</code></em> → <em><code>number</code></em></p><p>Addition</p><p><code>5 + 4</code> → <code>9</code></p>                                                                 |
| <p><em><code>number</code></em> <code>-</code> <em><code>number</code></em> → <em><code>number</code></em></p><p>Subtraction</p><p><code>3 - 2.0</code> → <code>1.0</code></p>                                                          |
| <p><em><code>number</code></em> <code>*</code> <em><code>number</code></em> → <em><code>number</code></em></p><p>Multiplication</p><p><code>5 * 4</code> → <code>20</code></p>                                                          |
| <p><em><code>number</code></em> <code>/</code> <em><code>number</code></em> → <em><code>number</code></em></p><p>Division (truncates the result towards zero if both inputs are integers)</p><p><code>5 / 3</code> → <code>1</code></p> |
| <p><em><code>integer</code></em> <code>%</code> <em><code>integer</code></em> → <em><code>integer</code></em></p><p>Modulo (remainder)</p><p><code>3 % 2</code> → <code>1</code></p>                                                    |
| <p><code>-</code> <em><code>number</code></em> → <em><code>number</code></em></p><p>Negation</p><p><code>- 2.0</code> → <code>-2.0</code></p>                                                                                           |

### 內建函數

Table 300 是 pgbench 內建，可以在 \set 的函數。

**Table 300. pgbench Functions**

| <p>Function</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>abs</code> ( <em><code>number</code></em> ) → same type as input</p><p>Absolute value</p><p><code>abs(-17)</code> → <code>17</code></p>                                                                                                                                                                                                                                                                                                                                                                                   |
| <p><code>debug</code> ( <em><code>number</code></em> ) → same type as input</p><p>Prints the argument to stderr, and returns the argument.</p><p><code>debug(5432.1)</code> → <code>5432.1</code></p>                                                                                                                                                                                                                                                                                                                              |
| <p><code>double</code> ( <em><code>number</code></em> ) → <code>double</code></p><p>Casts to double.</p><p><code>double(5432)</code> → <code>5432.0</code></p>                                                                                                                                                                                                                                                                                                                                                                     |
| <p><code>exp</code> ( <em><code>number</code></em> ) → <code>double</code></p><p>Exponential (<code>e</code> raised to the given power)</p><p><code>exp(1.0)</code> → <code>2.718281828459045</code></p>                                                                                                                                                                                                                                                                                                                           |
| <p><code>greatest</code> ( <em><code>number</code></em> [, <code>...</code> ] ) → <code>double</code> if any argument is double, else <code>integer</code></p><p>Selects the largest value among the arguments.</p><p><code>greatest(5, 4, 3, 2)</code> → <code>5</code></p>                                                                                                                                                                                                                                                       |
| <p><code>hash</code> ( <em><code>value</code></em> [, <em><code>seed</code></em> ] ) → <code>integer</code></p><p>This is an alias for <code>hash_murmur2</code>.</p><p><code>hash(10, 5432)</code> → <code>-5817877081768721676</code></p>                                                                                                                                                                                                                                                                                        |
| <p><code>hash_fnv1a</code> ( <em><code>value</code></em> [, <em><code>seed</code></em> ] ) → <code>integer</code></p><p>Computes <a href="https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function">FNV-1a hash</a>.</p><p><code>hash_fnv1a(10, 5432)</code> → <code>-7793829335365542153</code></p>                                                                                                                                                                                                             |
| <p><code>hash_murmur2</code> ( <em><code>value</code></em> [, <em><code>seed</code></em> ] ) → <code>integer</code></p><p>Computes <a href="https://en.wikipedia.org/wiki/MurmurHash">MurmurHash2 hash</a>.</p><p><code>hash_murmur2(10, 5432)</code> → <code>-5817877081768721676</code></p>                                                                                                                                                                                                                                      |
| <p><code>int</code> ( <em><code>number</code></em> ) → <code>integer</code></p><p>Casts to integer.</p><p><code>int(5.4 + 3.8)</code> → <code>9</code></p>                                                                                                                                                                                                                                                                                                                                                                         |
| <p><code>least</code> ( <em><code>number</code></em> [, <code>...</code> ] ) → <code>double</code> if any argument is double, else <code>integer</code></p><p>Selects the smallest value among the arguments.</p><p><code>least(5, 4, 3, 2.1)</code> → <code>2.1</code></p>                                                                                                                                                                                                                                                        |
| <p><code>ln</code> ( <em><code>number</code></em> ) → <code>double</code></p><p>Natural logarithm</p><p><code>ln(2.718281828459045)</code> → <code>1.0</code></p>                                                                                                                                                                                                                                                                                                                                                                  |
| <p><code>mod</code> ( <em><code>integer</code></em>, <em><code>integer</code></em> ) → <code>integer</code></p><p>Modulo (remainder)</p><p><code>mod(54, 32)</code> → <code>22</code></p>                                                                                                                                                                                                                                                                                                                                          |
| <p><code>permute</code> ( <em><code>i</code></em>, <em><code>size</code></em> [, <em><code>seed</code></em> ] ) → <code>integer</code></p><p>Permuted value of <em><code>i</code></em>, in the range <code>[0, size)</code>. This is the new position of <em><code>i</code></em> (modulo <em><code>size</code></em>) in a pseudorandom permutation of the integers <code>0...size-1</code>, parameterized by <em><code>seed</code></em>, see below.</p><p><code>permute(0, 4)</code> → <code>an integer between 0 and 3</code></p> |
| <p><code>pi</code> () → <code>double</code></p><p>Approximate value of π</p><p><code>pi()</code> → <code>3.14159265358979323846</code></p>                                                                                                                                                                                                                                                                                                                                                                                         |
| <p><code>pow</code> ( <em><code>x</code></em>, <em><code>y</code></em> ) → <code>double</code></p><p><code>power</code> ( <em><code>x</code></em>, <em><code>y</code></em> ) → <code>double</code></p><p><em><code>x</code></em> raised to the power of <em><code>y</code></em></p><p><code>pow(2.0, 10)</code> → <code>1024.0</code></p>                                                                                                                                                                                          |
| <p><code>random</code> ( <em><code>lb</code></em>, <em><code>ub</code></em> ) → <code>integer</code></p><p>Computes a uniformly-distributed random integer in <code>[lb, ub]</code>.</p><p><code>random(1, 10)</code> → <code>an integer between 1 and 10</code></p>                                                                                                                                                                                                                                                               |
| <p><code>random_exponential</code> ( <em><code>lb</code></em>, <em><code>ub</code></em>, <em><code>parameter</code></em> ) → <code>integer</code></p><p>Computes an exponentially-distributed random integer in <code>[lb, ub]</code>, see below.</p><p><code>random_exponential(1, 10, 3.0)</code> → <code>an integer between 1 and 10</code></p>                                                                                                                                                                                 |
| <p><code>random_gaussian</code> ( <em><code>lb</code></em>, <em><code>ub</code></em>, <em><code>parameter</code></em> ) → <code>integer</code></p><p>Computes a Gaussian-distributed random integer in <code>[lb, ub]</code>, see below.</p><p><code>random_gaussian(1, 10, 2.5)</code> → <code>an integer between 1 and 10</code></p>                                                                                                                                                                                             |
| <p><code>random_zipfian</code> ( <em><code>lb</code></em>, <em><code>ub</code></em>, <em><code>parameter</code></em> ) → <code>integer</code></p><p>Computes a Zipfian-distributed random integer in <code>[lb, ub]</code>, see below.</p><p><code>random_zipfian(1, 10, 1.5)</code> → <code>an integer between 1 and 10</code></p>                                                                                                                                                                                                |
| <p><code>sqrt</code> ( <em><code>number</code></em> ) → <code>double</code></p><p>Square root</p><p><code>sqrt(2.0)</code> → <code>1.414213562</code></p>                                                                                                                                                                                                                                                                                                                                                                          |

random 函數使用的是均勻分配亂數，也就是在指定範圍內的數值，都有相等的產生機率。random\_exponential 和 random\_gaussian 則需要額外的參數，來指定精確的分配情況。

* 指數分配，參數控制其分配情況是透過分段一個快速下降的指數分配，投影在指定範圍間的整數而得。精確來說，以下面的式子計算而得：\
  f(x) = exp(-parameter \* (x - min) / (max - min + 1)) / (1 - exp(-parameter))\
  區間中某個 i 值的機率為 f(i) - f(i + 1)。\
  直覺上，越大的輸入參數，就會越多較小的數值被輸出，而較少的大數值產生。如果參數接近 0 的話，就會很接近均勻分配。一個粗略的概念是，機率最高的 1%，落於靠近最小值的一端，機率大概是百分之（parameter）。此參數必須要是正整數。
* 高斯分配，指定區間會映射到一個標準常態分配的空間（典型的錐型高斯曲線），分佈於 -parameter 及 +parameter 之間。靠中間的值有更高的選取機率。精確來說，如果 PHI(x) 是該常態分配的累計分配函數的話，那麼平均數 mu 就是 (max + min) / 2.0，則：\
  f(x) = PHI(2.0 \* parameter \* (x - mu) / (max - min + 1)) / (2.0 \* PHI(parameter) - 1)\
  在區間中，數值 i 被選取的機率就是：f(i + 0.5) - f(i - 0.5)。直覺上，parameter 越大，就會有越多中間值被選值，而越小的話，兩側數側被選擇的機率就會增加。約有 67% 的結果會在靠近 1.0 / parameter 中間的值，相對於 0.5 / parameter 近乎在平均值的附近；2.0 / parameter 則是 95% 是靠近中間的值，相對於 1.0 / parameter 近乎在平均值的附近。舉例來說，如果 parameter = 4.0，大概有 67% 的值會來自於中間的四分之一（即 3.0 / 8.0 到 5.0 / 8.0），而 95% 來自於中間的一半（2.0 / 4.0），第二和第三的四分位數之間。以 Box-Muller 轉換的效率來說，parameter 最小值為 2.0。
* `random_zipfian` generates a bounded Zipfian distribution. _`parameter`_ defines how skewed the distribution is. The larger the _`parameter`_, the more frequently values closer to the beginning of the interval are drawn. The distribution is such that, assuming the range starts from 1, the ratio of the probability of drawing _`k`_ versus drawing _`k+1`_ is `((`_`k`_`+1)/`_`k`_`)**`_`parameter`_. For example, `random_zipfian(1, ..., 2.5)` produces the value `1` about `(2/1)**2.5 = 5.66` times more frequently than `2`, which itself is produced `(3/2)**2.5 = 2.76` times more frequently than `3`, and so on.

pgbench's implementation is based on "Non-Uniform Random Variate Generation", Luc Devroye, p. 550-551, Springer 1986. Due to limitations of that algorithm, the _`parameter`_ value is restricted to the range \[1.001, 1000].

#### Note

When designing a benchmark which selects rows non-uniformly, be aware that the rows chosen may be correlated with other data such as IDs from a sequence or the physical row ordering, which may skew performance measurements.

To avoid this, you may wish to use the `permute` function, or some other additional step with similar effect, to shuffle the selected rows and remove such correlations.

Hash functions `hash`, `hash_murmur2` and `hash_fnv1a` accept an input value and an optional seed parameter. In case the seed isn't provided the value of `:default_seed` is used, which is initialized randomly unless set by the command-line `-D` option.

`permute` accepts an input value, a size, and an optional seed parameter. It generates a pseudorandom permutation of integers in the range `[0, size)`, and returns the index of the input value in the permuted values. The permutation chosen is parameterized by the seed, which defaults to `:default_seed`, if not specified. Unlike the hash functions, `permute` ensures that there are no collisions or holes in the output values. Input values outside the interval are interpreted modulo the size. The function raises an error if the size is not positive. `permute` can be used to scatter the distribution of non-uniform random functions such as `random_zipfian` or `random_exponential` so that values drawn more often are not trivially correlated. For instance, the following pgbench script simulates a possible real world workload typical for social media and blogging platforms where a few accounts generate excessive load:

```
\set size 1000000
\set r random_zipfian(1, :size, 1.07)
\set k 1 + permute(:r, :size)
```

In some cases several distinct distributions are needed which don't correlate with each other and this is when the optional seed parameter comes in handy:

```
\set k1 1 + permute(:r, :size, :default_seed + 123)
\set k2 1 + permute(:r, :size, :default_seed + 321)
```

A similar behavior can also be approximated with `hash`:

```
\set size 1000000
\set r random_zipfian(1, 100 * :size, 1.07)
\set k 1 + abs(hash(:r)) % :size
```

However, since `hash` generates collisions, some values will not be reachable and others will be more frequent than expected from the original distribution.

下面是內建的 TPC-B like 交易的例子：

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

這個腳本讓每一個交易都引用不同且隨機的資料列。（這個例子也表示出每一個用戶擁有自己的變數的重要性—否則他們不會獨立地操作不同的資料列。）

### 記錄每筆交易

使用選項 -l（但沒有選項 --aggregate-interval）時，pgbench 將會把每一筆交易都寫入記錄檔。記錄檔的檔名會是 prefix.nnn 的形式，其中的 prefix 預設是 pgbench\_log，而 nnn 則是該 pgbench 程序的 PID。prefix 可以由選項 --log-prefix 來指定。如果選項 -j 是 2 以上時，也就是同時有多個執行緒在進行交易，那麼他們會被分別寫入不同的檔案，第一個執行緒會使用前述標準單一執行緒的檔名，而其他的執行緒將會命名為 prefix.nnn.mmm，其中 mmm 則由各執行緒依序編號而得，編號從 1 開始。

記錄檔內容格式如下：

```
client_id transaction_no time script_no time_epoch time_us [schedule_lag]
```

_`client_id`_

identifies the client session that ran the transaction

_`transaction_no`_

counts how many transactions have been run by that session

_`time`_

transaction's elapsed time, in microseconds

_`script_no`_

identifies the script file that was used for the transaction (useful when multiple scripts are specified with `-f` or `-b`)

_`time_epoch`_

transaction's completion time, as a Unix-epoch time stamp

_`time_us`_

fractional-second part of transaction's completion time, in microseconds

_`schedule_lag`_

transaction start delay, that is the difference between the transaction's scheduled start time and the time it actually started, in microseconds (present only if `--rate` is specified)

_`retries`_

count of retries after serialization or deadlock errors during the transaction (present only if `--max-tries` is not equal to one)

When both `--rate` and `--latency-limit` are used, the _`time`_ for a skipped transaction will be reported as `skipped`. If the transaction ends with a failure, its _`time`_ will be reported as `failed`. If you use the `--failures-detailed` option, the _`time`_ of the failed transaction will be reported as `serialization` or `deadlock` depending on the type of failure (see [Failures and Serialization/Deadlock Retries](https://www.postgresql.org/docs/current/pgbench.html#FAILURES-AND-RETRIES) for more information).

這裡是一小段記錄檔案，單一執行緒的結果：

```
0 199 2241 0 1175850568 995598
0 200 2465 0 1175850568 998079
0 201 2513 0 1175850569 608
0 202 2038 0 1175850569 2663
```

另一個例子，使用 --rate=100 及 --latency-limit=5（注意額外的 schedule\_lag 欄位）：

```
0 81 4621 0 1412881037 912698 3005
0 82 6173 0 1412881037 914578 4304
0 83 skipped 0 1412881037 914578 5217
0 83 skipped 0 1412881037 914578 5099
0 83 4722 0 1412881037 916203 3108
0 84 4142 0 1412881037 918023 2333
0 85 2465 0 1412881037 919759 740
```

在這個例子中，82 號交易誤點了，因為它延遲了 6.173 ms，超過限時的 5 ms。接下來的兩個交易就被跳過了，因為他們在開始前就已經超時了。

The following example shows a snippet of a log file with failures and retries, with the maximum number of tries set to 10 (note the additional _`retries`_ column):

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

If the `--failures-detailed` option is used, the type of failure is reported in the _`time`_ like this:

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

當某個主機執行長時間的交易時，記錄檔案可能會變得非常大。選項 --sampling-rate 就可以派上用場，只存下部份的交易樣本。

### 彙總記錄

使用 --aggregate-interval 選項時，會是另一種記錄檔格式：

_`interval_start`_

start time of the interval, as a Unix-epoch time stamp

_`num_transactions`_

number of transactions within the interval

_`sum_latency`_

sum of transaction latencies

_`sum_latency_2`_

sum of squares of transaction latencies

_`min_latency`_

minimum transaction latency

_`max_latency`_

maximum transaction latency

_`sum_lag`_

sum of transaction start delays (zero unless `--rate` is specified)

_`sum_lag_2`_

sum of squares of transaction start delays (zero unless `--rate` is specified)

_`min_lag`_

minimum transaction start delay (zero unless `--rate` is specified)

_`max_lag`_

maximum transaction start delay (zero unless `--rate` is specified)

_`skipped`_

number of transactions skipped because they would have started too late (zero unless `--rate` and `--latency-limit` are specified)

_`retried`_

number of retried transactions (zero unless `--max-tries` is not equal to one)

_`retries`_

number of retries after serialization or deadlock errors (zero unless `--max-tries` is not equal to one)

_`serialization_failures`_

number of transactions that got a serialization error and were not retried afterwards (zero unless `--failures-detailed` is specified)

_`deadlock_failures`_

number of transactions that got a deadlock error and were not retried afterwards (zero unless `--failures-detailed` is specified)

這裡是一些輸出範例結果：

<pre><code><strong>pgbench --aggregate-interval=10 --time=20 --client=10 --log --rate=1000 --latency-limit=10 --failures-detailed --max-tries=10 test
</strong>
1650260552 5178 26171317 177284491527 1136 44462 2647617 7321113867 0 9866 64 7564 28340 4148 0
1650260562 4808 25573984 220121792172 1171 62083 3037380 9666800914 0 9998 598 7392 26621 4527 0
</code></pre>

注意，一般的記錄檔（非彙總式）會記錄交易由哪一個腳本產生，但彙總式記錄則不會。所以如果你需要分別不同的腳本彙總，你需要自行處理。

### 每個指令報告

使用選項 -r 時，pgbench 就會收集每一個模擬用戶的每一個交易中的每一個指令的耗時，它會以平均值回報，放在最後報告中的每一個指令前。

以預設的腳本，輸出可能會是像這樣：

```
starting vacuum...end.
transaction type:<builtin: TPC-B (sort of)>

scaling factor: 1
query mode: simple
number of clients: 10
number of threads: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
latency average = 15.844 ms
latency stddev = 2.715 ms
tps = 618.764555 (including connections establishing)
tps = 622.977698 (excluding connections establishing)
script statistics:
 - statement latencies in milliseconds:
        0.002  \set aid random(1, 100000 * :scale)
        0.005  \set bid random(1, 1 * :scale)
        0.002  \set tid random(1, 10 * :scale)
        0.001  \set delta random(-5000, 5000)
        0.326  BEGIN;
        0.603  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
        0.454  SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
        5.528  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
        7.335  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
        0.371  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
        1.212  END;
```

如果有多個腳本被使用時，結果則會依不同的腳本檔分別回報。

注意收集每一個指令的執行時間也需要計算，會增加些許的負載。這個選項會降低一些平均執行速度和 TPS。具體上會有多少影響則視平台及硬體而定。可以比較切換此選項的 TPS 來瞭解額外負載的情況。

#### Failures and Serialization/Deadlock Retries

When executing pgbench, there are three main types of errors:

* Errors of the main program. They are the most serious and always result in an immediate exit from pgbench with the corresponding error message. They include:
  * errors at the beginning of pgbench (e.g. an invalid option value);
  * errors in the initialization mode (e.g. the query to create tables for built-in scripts fails);
  * errors before starting threads (e.g. could not connect to the database server, syntax error in the meta command, thread creation failure);
  * internal pgbench errors (which are supposed to never occur...).
* Errors when the thread manages its clients (e.g. the client could not start a connection to the database server / the socket for connecting the client to the database server has become invalid). In such cases all clients of this thread stop while other threads continue to work. However, `--exit-on-abort` is specified, all of the threads stop immediately in this case.
* Direct client errors. They lead to immediate exit from pgbench with the corresponding error message in the case of an internal pgbench error (which are supposed to never occur...) or when `--exit-on-abort` is specified. Otherwise in the worst case they only lead to the abortion of the failed client while other clients continue their run (but some client errors are handled without an abortion of the client and reported separately, see below). Later in this section it is assumed that the discussed errors are only the direct client errors and they are not internal pgbench errors.

A client's run is aborted in case of a serious error; for example, the connection with the database server was lost or the end of script was reached without completing the last transaction. In addition, if execution of an SQL or meta command fails for reasons other than serialization or deadlock errors, the client is aborted. Otherwise, if an SQL command fails with serialization or deadlock errors, the client is not aborted. In such cases, the current transaction is rolled back, which also includes setting the client variables as they were before the run of this transaction (it is assumed that one transaction script contains only one transaction; see [What Is the "Transaction" Actually Performed in pgbench?](https://www.postgresql.org/docs/current/pgbench.html#TRANSACTIONS-AND-SCRIPTS) for more information). Transactions with serialization or deadlock errors are repeated after rollbacks until they complete successfully or reach the maximum number of tries (specified by the `--max-tries` option) / the maximum time of retries (specified by the `--latency-limit` option) / the end of benchmark (specified by the `--time` option). If the last trial run fails, this transaction will be reported as failed but the client is not aborted and continues to work.

#### Note

Without specifying the `--max-tries` option, a transaction will never be retried after a serialization or deadlock error because its default value is 1. Use an unlimited number of tries (`--max-tries=0`) and the `--latency-limit` option to limit only the maximum time of tries. You can also use the `--time` option to limit the benchmark duration under an unlimited number of tries.

Be careful when repeating scripts that contain multiple transactions: the script is always retried completely, so successful transactions can be performed several times.

Be careful when repeating transactions with shell commands. Unlike the results of SQL commands, the results of shell commands are not rolled back, except for the variable value of the `\setshell` command.

The latency of a successful transaction includes the entire time of transaction execution with rollbacks and retries. The latency is measured only for successful transactions and commands but not for failed transactions or commands.

The main report contains the number of failed transactions. If the `--max-tries` option is not equal to 1, the main report also contains statistics related to retries: the total number of retried transactions and total number of retries. The per-script report inherits all these fields from the main report. The per-statement report displays retry statistics only if the `--max-tries` option is not equal to 1.

If you want to group failures by basic types in per-transaction and aggregation logs, as well as in the main and per-script reports, use the `--failures-detailed` option. If you also want to distinguish all errors and failures (errors without retrying) by type including which limit for retries was exceeded and how much it was exceeded by for the serialization/deadlock failures, use the `--verbose-errors` option.

#### Table Access Methods

You may specify the [Table Access Method](https://www.postgresql.org/docs/current/tableam.html) for the pgbench tables. The environment variable `PGOPTIONS` specifies database configuration options that are passed to PostgreSQL via the command line (See [Section 19.1.4](https://www.postgresql.org/docs/current/config-setting.html#CONFIG-SETTING-SHELL)). For example, a hypothetical default Table Access Method for the tables that pgbench creates called `wuzza` can be specified with:

```
PGOPTIONS='-c default_table_access_method=wuzza'
```

### 建議的作法

使用 pgbench 產生許多無用數字是很簡單的事。這裡提供一些作法，幫助你得到一些有用的結果。

首先，不要相信任何在數秒內就能得到的結果。善用 -t 或 -T 使測試至少能執行好幾分鐘，用平均的方式降低誤差。在某個情境你可能需要幾個小時使得結果數字是可重現的。至少嘗試執行時間數分鐘以上是好主意，可以瞭解你的結果是否具重見性。

對於預設的 TPC-B like 測試情境，scale factor （-s）應該要是一個足夠大的數，超過最大的用戶數（-c），否則你會遭遇更新競爭的情況。因為每個交易都需要更新 pgbench\_branches，所以如果 -c 大於 -s 時，將無可避免有些交易會被其他交易暫時阻擋。

預設的測試情境對於資料表被使用多久也很敏感：因為資料表變更會產生廢棄的資料列、資料空間。要瞭解這些情況，你必須追蹤更新資料的總數和整理資料表的時間。如果自動整理的功能開啓了，那麼就會在測試時產生無可預知的變化。

pgbench 的其中一項限制就是它自己也可能是瓶頸，在產生大量模擬用戶時。可以採用在多台主機使用多個 pgbench 來解決這個問題，雖然這樣也會帶來一些網路延遲。不過這樣就可以同時執行許多的 pgbench，在多個主機上，對同一個資料庫進行測試。

#### Security

If untrusted users have access to a database that has not adopted a [secure schema usage pattern](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATTERNS), do not run pgbench in that database. pgbench uses unqualified names and does not manipulate the search path.
