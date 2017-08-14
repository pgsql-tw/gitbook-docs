# pgbench[^1]

pgbench — 進行 PostgreSQL 效能評估

## 語法

`pgbench-i`\[`option`...\] \[`dbname`\]

`pgbench`\[`option`...\] \[`dbname`\]

## 說明

pgbench 是一個簡易型 PostgreSQL 的效能評估工具。它可以重覆執行某一系列的 SQL 指令，也可能進行大量連線的模擬情境，然後計算其平均的交易完成率（TPS, Transaction Per Second）。預設上，pgbench 使用的是 TPC-B 的標準情境，它在 1 個資料交易中會進行 5 個階段的資料操作，包含 SELECT、UPDATE、INSERT 指令。然而，你也可以使用你的腳本，來測試你的情境。

pgbench 大致上的輸出如下：

```
transaction type: <builtin: TPC-B (sort of)>

scaling factor: 10
query mode: simple
number of clients: 10
number of threads: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
tps = 85.184871 (including connections establishing)
tps = 85.296346 (excluding connections establishing)
```

前 6 行說明該測試中最主要的操作參數。再下一行則是回報交易完成的數量，以及應該執行的數量（由 client 的數量與每個 client 須執行的交易量乘積而得）；這兩個數字應該要相等，如果每個交易都完成的話。（使用 -T 模式時，只會回報實際執行的交易數量）最後 2 行則以 TPS 回報，一行採計初始連線時間，另一行則沒有。

預設使用的 TPC-B 情境評估需要特定的資料庫結構，它們必須要在測試前先建立好。所以在測試之前，要先以「-i」參數執行初始化資料庫結構。（如果你使用自訂的情境測試，那就不需要進行這個步驟，但你可能需要另外自行建立你所需要的結構。）初始化指令如下：

```
pgbench -i [other-options] dbname
```

dbname 必須是已經存在的資料庫。（也許你需要再加上 -h、-p、--U 等參數來設定資料庫的連線參數。）

### 注意

pgbench -i 會建立 4 個表格：pgbench\_accounts、pgbench\_branches、pgbench\_history、以及 pgbench\_tellers。它會取代掉同名的表格。所以你如果和既有的資料庫共用的話，請注意同名的問題！

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

一般來說，你還會需要加上其他選項以進行更有意義的測試。最主要的測試選項為 -c （模擬用戶數量）、-t（資料交易數量）、-T（限時測試）、還有 -F（指定一個自訂的腳本）。完整選項如下。

## 選項

下面的部份分成三個小節：資料庫初始化專用選項、評估階段專用選項、一些通用的選項。

### 資料庫初始化專用選項

pgbench 在資料庫初始化時可以使用下列選項：

`-i`

`--initialize`

表示要進行資料庫初始化。

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

`-d`

`--debug`

輸出程式除錯用的訊息。

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

預設是使用簡單查詢協定。（有關查詢協定，請參閱[第 52 章](/vii-internals/frontendbackend-protocol.md)）

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

`--log-prefix=prefix`

設定 --log 所建立檔案的檔名前置名稱。預設是 pgbench\_log。

`--progress-timestamp`

當顯示進度（選項 -P）時，使用時間戳記（Unix epoch）取代相對的執行時間。其單位是秒，精確度至千分之一秒。這個選項用於在多種操作工具間比較時間。

`--sampling-rate=rate`

取樣率，用於寫入資料到記錄檔時，可以減少記錄的輸出量。如果使用這個選項的話，只有指定比率的記錄會被輸出。如果是 1.0 的話，表示所有記錄都要輸出；而 0.05 的話，表示只輸出 5% 的記錄。

記得取樣率指的是輸出到記錄檔的比率，舉例來說，當計算 TPS 數值時，你會需要多個樣本數來彙整（使用 0.01 的取樣率時，你就只會得到原來百分之一個 TPS 數值輸出）。

### Common Options

pgbenchaccepts the following command-line common arguments:

`-h`

`hostname`

`--host=`

`hostname`

The database server's host name

`-p`

`port`

`--port=`

`port`

The database server's port number

`-U`

`login`

`--username=`

`login`

The user name to connect as

`-V`

`--version`

Print thepgbenchversion and exit.

`-?`

`--help`

Show help aboutpgbenchcommand line arguments, and exit.

## Notes

### What is the“Transaction”Actually Performed inpgbench?

pgbenchexecutes test scripts chosen randomly from a specified list. They include built-in scripts with`-b`and user-provided custom scripts with`-f`. Each script may be given a relative weight specified after a`@`so as to change its drawing probability. The default weight is`1`. Scripts with a weight of`0`are ignored.

The default built-in transaction script \(also invoked with`-b tpcb-like`\) issues seven commands per transaction over randomly chosen`aid`,`tid`,`bid`and`balance`. The scenario is inspired by the TPC-B benchmark, but is not actually TPC-B, hence the name.

1. `BEGIN;`

2. `UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;`

3. `SELECT abalance FROM pgbench_accounts WHERE aid = :aid;`

4. `UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;`

5. `UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;`

6. `INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);`

7. `END;`

If you select the`simple-update`built-in \(also`-N`\), steps 4 and 5 aren't included in the transaction. This will avoid update contention on these tables, but it makes the test case even less like TPC-B.

If you select the`select-only`built-in \(also`-S`\), only the`SELECT`is issued.

### Custom Scripts

pgbenchhas support for running custom benchmark scenarios by replacing the default transaction script \(described above\) with a transaction script read from a file \(`-f`option\). In this case a“transaction”counts as one execution of a script file.

A script file contains one or more SQL commands terminated by semicolons. Empty lines and lines beginning with`--`are ignored. Script files can also contain“meta commands”, which are interpreted bypgbenchitself, as described below.

### Note

BeforePostgreSQL9.6, SQL commands in script files were terminated by newlines, and so they could not be continued across lines. Now a semicolon is\_required\_to separate consecutive SQL commands \(though a SQL command does not need one if it is followed by a meta command\). If you need to create a script file that works with both old and new versions ofpgbench, be sure to write each SQL command on a single line ending with a semicolon.

There is a simple variable-substitution facility for script files. Variables can be set by the command-line`-D`option, explained above, or by the meta commands explained below. In addition to any variables preset by`-D`command-line options, there are a few variables that are preset automatically, listed in[Table 240](https://www.postgresql.org/docs/devel/static/pgbench.html#pgbench-automatic-variables). A value specified for these variables using`-D`takes precedence over the automatic presets. Once set, a variable's value can be inserted into a SQL command by writing`:variablename`. When running more than one client session, each session has its own set of variables.

**Table 240. Automatic Variables**

| Variable | Description |
| :--- | :--- |
| `scale` | current scale factor |
| `client_id` | unique number identifying the client session \(starts from zero\) |

Script file meta commands begin with a backslash \(`\`\) and normally extend to the end of the line, although they can be continued to additional lines by writing backslash-return. Arguments to a meta command are separated by white space. These meta commands are supported:

`\set`

`varname`

`expression`

Sets variable`varname`_\_to a value calculated from_`expression`_. The expression may contain integer constants such as_`5432`_, double constants such as_`3.14159`_, references to variables_`:variablename`\_, unary operators \(`+`,`-`\) and binary operators \(`+`,`-`,`*`,`/`,`%`\) with their usual precedence and associativity,[function calls](https://www.postgresql.org/docs/devel/static/pgbench.html#pgbench-builtin-functions), and parentheses.

Examples:

```
\set ntellers 10 * :scale
\set aid (1021 * random(1, 100000 * :scale)) % \
           (100000 * :scale) + 1
```

`\sleep`

`number`

\[ us \| ms \| s \]

Causes script execution to sleep for the specified duration in microseconds \(`us`\), milliseconds \(`ms`\) or seconds \(`s`\). If the unit is omitted then seconds are the default.`number`_\_can be either an integer constant or a_`:variablename`\_reference to a variable having an integer value.

Example:

```
\sleep 10 ms
```

`\setshell`

`varname`

`command`

\[

`argument`

... \]

Sets variable`varname`_\_to the result of the shell command_`command`_with the given_`argument`\_\(s\). The command must return an integer value through its standard output.

`command`_\_and each_`argument`_can be either a text constant or a_`:variablename`_reference to a variable. If you want to use an_`argument`_starting with a colon, write an additional colon at the beginning of_`argument`\_.

Example:

```
\setshell variable_to_be_assigned command literal_argument :variable ::literal_starting_with_colon
```

`\shell`

`command`

\[

`argument`

... \]

Same as`\setshell`, but the result of the command is discarded.

Example:

```
\shell command literal_argument :variable ::literal_starting_with_colon
```

### Built-In Functions

The functions listed in[Table 241](https://www.postgresql.org/docs/devel/static/pgbench.html#pgbench-functions)are built intopgbenchand may be used in expressions appearing in[`\set`](https://www.postgresql.org/docs/devel/static/pgbench.html#pgbench-metacommand-set).

**Table 241. pgbench Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `abs(a`\) | same as`a` | absolute value | `abs(-17)` | `17` |
| `debug(a`\) | same as`a` | print`a`_\_tostderr, and return_`a`\_ | `debug(5432.1)` | `5432.1` |
| `double(i`\) | double | cast to double | `double(5432)` | `5432.0` |
| `greatest(a`\[,`...`\] \) | double if any\_`a`\_is double, else integer | largest value among arguments | `greatest(5, 4, 3, 2)` | `5` |
| `int(x`\) | integer | cast to int | `int(5.4 + 3.8)` | `9` |
| `least(a`\[,`...`\] \) | double if any\_`a`\_is double, else integer | smallest value among arguments | `least(5, 4, 3, 2.1)` | `2.1` |
| `pi()` | double | value of the constant PI | `pi()` | `3.14159265358979323846` |
| `random(lb`,`ub`\) | integer | uniformly-distributed random integer in`[lb, ub]` | `random(1, 10)` | an integer between`1`and`10` |
| `random_exponential(lb`,`ub`,`parameter`\) | integer | exponentially-distributed random integer in`[lb, ub]`, see below | `random_exponential(1, 10, 3.0)` | an integer between`1`and`10` |
| `random_gaussian(lb`,`ub`,`parameter`\) | integer | Gaussian-distributed random integer in`[lb, ub]`, see below | `random_gaussian(1, 10, 2.5)` | an integer between`1`and`10` |
| `sqrt(x`\) | double | square root | `sqrt(2.0)` | `1.414213562` |

The`random`function generates values using a uniform distribution, that is all the values are drawn within the specified range with equal probability. The`random_exponential`and`random_gaussian`functions require an additional double parameter which determines the precise shape of the distribution.

* For an exponential distribution,`parameter`_\_controls the distribution by truncating a quickly-decreasing exponential distribution at_`parameter`\_, and then projecting onto integers between the bounds. To be precise, with

  f\(x\) = exp\(-parameter \* \(x - min\) / \(max - min + 1\)\) / \(1 - exp\(-parameter\)\)

  Then value`i`_\_between_`min`_and_`max`\_inclusive is drawn with probability:`f(i) - f(i + 1)`.

  Intuitively, the larger the`parameter`, the more frequently values close to`min`_\_are accessed, and the less frequently values close to_`max`_are accessed. The closer to 0_`parameter`_is, the flatter \(more uniform\) the access distribution. A crude approximation of the distribution is that the most frequent 1% values in the range, close to_`min`_, are drawn_`parameter`_% of the time. The_`parameter`\_value must be strictly positive.

* For a Gaussian distribution, the interval is mapped onto a standard normal distribution \(the classical bell-shaped Gaussian curve\) truncated at`-parameter`on the left and`+parameter`on the right. Values in the middle of the interval are more likely to be drawn. To be precise, if`PHI(x)`is the cumulative distribution function of the standard normal distribution, with mean`mu`defined as`(max + min) / 2.0`, with

  f\(x\) = PHI\(2.0 \* parameter \* \(x - mu\) / \(max - min + 1\)\) /  
         \(2.0 \* PHI\(parameter\) - 1\)

  then value`i`_\_between_`min`_and_`max`_inclusive is drawn with probability:_`f(i + 0.5) - f(i - 0.5)`_. Intuitively, the larger the_`parameter`_, the more frequently values close to the middle of the interval are drawn, and the less frequently values close to the_`min`_and_`max`_bounds. About 67% of values are drawn from the middle_`1.0 / parameter`_, that is a relative_`0.5 / parameter`_around the mean, and 95% in the middle_`2.0 / parameter`_, that is a relative_`1.0 / parameter`_around the mean; for instance, if_`parameter`_is 4.0, 67% of values are drawn from the middle quarter \(1.0 / 4.0\) of the interval \(i.e. from_`3.0 / 8.0`_to_`5.0 / 8.0`_\) and 95% from the middle half \(_`2.0 / 4.0`_\) of the interval \(second and third quartiles\). The minimum_`parameter`\_is 2.0 for performance of the Box-Muller transform.

As an example, the full definition of the built-in TPC-B-like transaction is:

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

This script allows each iteration of the transaction to reference different, randomly-chosen rows. \(This example also shows why it's important for each client session to have its own variables — otherwise they'd not be independently touching different rows.\)

### Per-Transaction Logging

With the`-l`option \(but without the`--aggregate-interval`option\),pgbenchwrites information about each transaction to a log file. The log file will be named`prefix`.`nnn`, where`prefix`_\_defaults to_`pgbench_log`_, and_`nnn`_is the PID of thepgbenchprocess. The prefix can be changed by using the_`--log-prefix`_option. If the_`-j`_option is 2 or higher, so that there are multiple worker threads, each will have its own log file. The first worker will use the same name for its log file as in the standard single worker case. The additional log files for the other workers will be named_`prefix`_._`nnn`_._`mmm`_, where_`mmm`\_is a sequential number for each worker starting with 1.

The format of the log is:

```
client_id
transaction_no
time
script_no
time_epoch
time_us
 [
schedule_lag
]
```

where`client_id`_\_indicates which client session ran the transaction,_`transaction_no`_counts how many transactions have been run by that session,_`time`_is the total elapsed transaction time in microseconds,_`script_no`_identifies which script file was used \(useful when multiple scripts were specified with_`-f`_or_`-b`_\), and_`time_epoch`_/_`time_us`_are a Unix-epoch time stamp and an offset in microseconds \(suitable for creating an ISO 8601 time stamp with fractional seconds\) showing when the transaction completed. The_`schedule_lag`_field is the difference between the transaction's scheduled start time, and the time it actually started, in microseconds. It is only present when the_`--rate`_option is used. When both_`--rate`_and_`--latency-limit`_are used, the_`time`\_for a skipped transaction will be reported as`skipped`.

Here is a snippet of a log file generated in a single-client run:

```
0 199 2241 0 1175850568 995598
0 200 2465 0 1175850568 998079
0 201 2513 0 1175850569 608
0 202 2038 0 1175850569 2663
```

Another example with`--rate=100`and`--latency-limit=5`\(note the additional\_`schedule_lag`\_column\):

```
0 81 4621 0 1412881037 912698 3005
0 82 6173 0 1412881037 914578 4304
0 83 skipped 0 1412881037 914578 5217
0 83 skipped 0 1412881037 914578 5099
0 83 4722 0 1412881037 916203 3108
0 84 4142 0 1412881037 918023 2333
0 85 2465 0 1412881037 919759 740
```

In this example, transaction 82 was late, because its latency \(6.173 ms\) was over the 5 ms limit. The next two transactions were skipped, because they were already late before they were even started.

When running a long test on hardware that can handle a lot of transactions, the log files can become very large. The`--sampling-rate`option can be used to log only a random sample of transactions.

### Aggregated Logging

With the`--aggregate-interval`option, a different format is used for the log files:

```
interval_start
num_transactions
sum_latency
sum_latency_2
min_latency
max_latency
 [
sum_lag
sum_lag_2
min_lag
max_lag
 [
skipped
] 
]
```

where`interval_start`_\_is the start of the interval \(as a Unix epoch time stamp\),_`num_transactions`_is the number of transactions within the interval,_`sum_latency`_is the sum of the transaction latencies within the interval,_`sum_latency_2`_is the sum of squares of the transaction latencies within the interval,_`min_latency`_is the minimum latency within the interval, and_`max_latency`_is the maximum latency within the interval. The next fields,_`sum_lag`_,_`sum_lag_2`_,_`min_lag`_, and_`max_lag`_, are only present if the_`--rate`_option is used. They provide statistics about the time each transaction had to wait for the previous one to finish, i.e. the difference between each transaction's scheduled start time and the time it actually started. The very last field,_`skipped`\_, is only present if the`--latency-limit`option is used, too. It counts the number of transactions skipped because they would have started too late. Each transaction is counted in the interval when it was committed.

Here is some example output:

```
1345828501 5601 1542744 483552416 61 2573
1345828503 7884 1979812 565806736 60 1479
1345828505 7208 1979422 567277552 59 1391
1345828507 7685 1980268 569784714 60 1398
1345828509 7073 1979779 573489941 236 1411
```

Notice that while the plain \(unaggregated\) log file shows which script was used for each transaction, the aggregated log does not. Therefore if you need per-script data, you need to aggregate the data on your own.

### Per-Statement Latencies

With the`-r`option,pgbenchcollects the elapsed transaction time of each statement executed by every client. It then reports an average of those values, referred to as the latency for each statement, after the benchmark has finished.

For the default script, the output will look similar to this:

```
starting vacuum...end.
transaction type: 
<
builtin: TPC-B (sort of)
>

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

If multiple script files are specified, the averages are reported separately for each script file.

Note that collecting the additional timing information needed for per-statement latency computation adds some overhead. This will slow average execution speed and lower the computed TPS. The amount of slowdown varies significantly depending on platform and hardware. Comparing average TPS values with and without latency reporting enabled is a good way to measure if the timing overhead is significant.

### Good Practices

It is very easy to usepgbenchto produce completely meaningless numbers. Here are some guidelines to help you get useful results.

In the first place,\_never\_believe any test that runs for only a few seconds. Use the`-t`or`-T`option to make the run last at least a few minutes, so as to average out noise. In some cases you could need hours to get numbers that are reproducible. It's a good idea to try the test run a few times, to find out if your numbers are reproducible or not.

For the default TPC-B-like test scenario, the initialization scale factor \(`-s`\) should be at least as large as the largest number of clients you intend to test \(`-c`\); else you'll mostly be measuring update contention. There are only`-s`rows in the`pgbench_branches`table, and every transaction wants to update one of them, so`-c`values in excess of`-s`will undoubtedly result in lots of transactions blocked waiting for other transactions.

The default test scenario is also quite sensitive to how long it's been since the tables were initialized: accumulation of dead rows and dead space in the tables changes the results. To understand the results you must keep track of the total number of updates and when vacuuming happens. If autovacuum is enabled it can result in unpredictable changes in measured performance.

A limitation ofpgbenchis that it can itself become the bottleneck when trying to test a large number of client sessions. This can be alleviated by runningpgbenchon a different machine from the database server, although low network latency will be essential. It might even be useful to run severalpgbenchinstances concurrently, on several client machines, against the same database server.

---

[^1]:  [PostgreSQL: Documentation: devel: pgbench](https://www.postgresql.org/docs/devel/static/pgbench.html)

