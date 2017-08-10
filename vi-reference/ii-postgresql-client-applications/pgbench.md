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

下面的部份分成三個小節：資料庫初始化專用選項、評估階段專用選項、一些兩用的選項。

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

把所有表格都建立成非永久性表格，而不是永久性表格。

### 評估階段專用選項

pgbenchaccepts the following command-line benchmarking arguments:

`-b`

`scriptname[@weight]`

`--builtin`

=

`scriptname[@weight]`

Add the specified built-in script to the list of executed scripts. An optional integer weight after`@`allows to adjust the probability of drawing the script. If not specified, it is set to 1. Available built-in scripts are:`tpcb-like`,`simple-update`and`select-only`. Unambiguous prefixes of built-in names are accepted. With special name`list`, show the list of built-in scripts and exit immediately.

`-c`

`clients`

`--client=`

`clients`

Number of clients simulated, that is, number of concurrent database sessions. Default is 1.

`-C`

`--connect`

Establish a new connection for each transaction, rather than doing it just once per client session. This is useful to measure the connection overhead.

`-d`

`--debug`

Print debugging output.

`-D`

`varname`

`=`

`value`

`--define=`

`varname`

`=`

`value`

Define a variable for use by a custom script \(see below\). Multiple`-D`options are allowed.

`-f`

`filename[@weight]`

`--file=`

`filename[@weight]`

Add a transaction script read from\_`filename`\_to the list of executed scripts. An optional integer weight after`@`allows to adjust the probability of drawing the test. See below for details.

`-j`

`threads`

`--jobs=`

`threads`

Number of worker threads withinpgbench. Using more than one thread can be helpful on multi-CPU machines. Clients are distributed as evenly as possible among available threads. Default is 1.

`-l`

`--log`

Write information about each transaction to a log file. See below for details.

`-L`

`limit`

`--latency-limit=`

`limit`

Transaction which last more than`limit`_\_milliseconds are counted and reported separately, as\_late_.

When throttling is used \(`--rate=...`\), transactions that lag behind schedule by more than`limit`_\_ms, and thus have no hope of meeting the latency limit, are not sent to the server at all. They are counted and reported separately as\_skipped_.

`-M`

`querymode`

`--protocol=`

`querymode`

Protocol to use for submitting queries to the server:

* `simple`: use simple query protocol.

* `extended`: use extended query protocol.

* `prepared`: use extended query protocol with prepared statements.

The default is simple query protocol. \(See[Chapter 52](https://www.postgresql.org/docs/devel/static/protocol.html)for more information.\)

`-n`

`--no-vacuum`

Perform no vacuuming before running the test. This option is\_necessary\_if you are running a custom test scenario that does not include the standard tables`pgbench_accounts`,`pgbench_branches`,`pgbench_history`, and`pgbench_tellers`.

`-N`

`--skip-some-updates`

Run built-in simple-update script. Shorthand for`-b simple-update`.

`-P`

`sec`

`--progress=`

`sec`

Show progress report every\_`sec`\_seconds. The report includes the time since the beginning of the run, the tps since the last report, and the transaction latency average and standard deviation since the last report. Under throttling \(`-R`\), the latency is computed with respect to the transaction scheduled start time, not the actual transaction beginning time, thus it also includes the average schedule lag time.

`-r`

`--report-latencies`

Report the average per-statement latency \(execution time from the perspective of the client\) of each command after the benchmark finishes. See below for details.

`-R`

`rate`

`--rate=`

`rate`

Execute transactions targeting the specified rate instead of running as fast as possible \(the default\). The rate is given in transactions per second. If the targeted rate is above the maximum possible rate, the rate limit won't impact the results.

The rate is targeted by starting transactions along a Poisson-distributed schedule time line. The expected start time schedule moves forward based on when the client first started, not when the previous transaction ended. That approach means that when transactions go past their original scheduled end time, it is possible for later ones to catch up again.

When throttling is active, the transaction latency reported at the end of the run is calculated from the scheduled start times, so it includes the time each transaction had to wait for the previous transaction to finish. The wait time is called the schedule lag time, and its average and maximum are also reported separately. The transaction latency with respect to the actual transaction start time, i.e. the time spent executing the transaction in the database, can be computed by subtracting the schedule lag time from the reported latency.

If`--latency-limit`is used together with`--rate`, a transaction can lag behind so much that it is already over the latency limit when the previous transaction ends, because the latency is calculated from the scheduled start time. Such transactions are not sent to the server, but are skipped altogether and counted separately.

A high schedule lag time is an indication that the system cannot process transactions at the specified rate, with the chosen number of clients and threads. When the average transaction execution time is longer than the scheduled interval between each transaction, each successive transaction will fall further behind, and the schedule lag time will keep increasing the longer the test run is. When that happens, you will have to reduce the specified transaction rate.

`-s`

`scale_factor`

`--scale=`

`scale_factor`

Report the specified scale factor inpgbench's output. With the built-in tests, this is not necessary; the correct scale factor will be detected by counting the number of rows in the`pgbench_branches`table. However, when testing only custom benchmarks \(`-f`option\), the scale factor will be reported as 1 unless this option is used.

`-S`

`--select-only`

Run built-in select-only script. Shorthand for`-b select-only`.

`-t`

`transactions`

`--transactions=`

`transactions`

Number of transactions each client runs. Default is 10.

`-T`

`seconds`

`--time=`

`seconds`

Run the test for this many seconds, rather than a fixed number of transactions per client.`-t`and`-T`are mutually exclusive.

`-v`

`--vacuum-all`

Vacuum all four standard tables before running the test. With neither`-n`nor`-v`,pgbenchwill vacuum the`pgbench_tellers`and`pgbench_branches`tables, and will truncate`pgbench_history`.

`--aggregate-interval=`

`seconds`

Length of aggregation interval \(in seconds\). May be used only with`-l`option. With this option, the log contains per-interval summary data, as described below.

`--log-prefix=`

`prefix`

Set the filename prefix for the log files created by`--log`. The default is`pgbench_log`.

`--progress-timestamp`

When showing progress \(option`-P`\), use a timestamp \(Unix epoch\) instead of the number of seconds since the beginning of the run. The unit is in seconds, with millisecond precision after the dot. This helps compare logs generated by various tools.

`--sampling-rate=`

`rate`

Sampling rate, used when writing data into the log, to reduce the amount of log generated. If this option is given, only the specified fraction of transactions are logged. 1.0 means all transactions will be logged, 0.05 means only 5% of the transactions will be logged.

Remember to take the sampling rate into account when processing the log file. For example, when computing tps values, you need to multiply the numbers accordingly \(e.g. with 0.01 sample rate, you'll only get 1/100 of the actual tps\).

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

