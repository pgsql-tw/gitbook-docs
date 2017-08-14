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

### 注意

在 PostgreSQL 9.6 之前，腳本檔案裡的 SQL 指令是以換行結尾的，也就是不能跨行。現在使用分號是必要的了，在分隔連續的 SQL 指令時，你得加上分號（但如果這個 SQL 指令是由中繼指令所執行的話，就不需要分號）。如果你需要建立一份相容性的腳本檔案的話，請確認你的每一條 SQL 指令都是單行，並且以分號結尾。

腳本檔案可以進行簡易的變數代換動作。變數可以由命令列的 -D 來設定，或使用下面所介紹的中繼指令。進一步來說，任何變數都可以使用 -D 選項來預先設定，而在 Table 240 的變數則會自動產生。一旦設定好之後，變數內容就可以使用 :variablename 的形式放入 SQL 指令之中。而每一個模擬用戶的連線中，他們都擁有他們自己的變數內容。

**Table 240. Automatic Variables**

| Variable | Description |
| :--- | :--- |
| `scale` | 目前的 scale factor |
| `client_id` | 每一個用戶連線的唯一識別資訊（起始為零） |

中繼指令是以倒斜線（\）開頭的指令，一般就到行末結尾，而如果要多行的話，就在行末再加倒斜線。中繼指令的參數是以空白分隔。支援的中繼指令有：

`\set varname expression`

以 expression 表示式來計算 varname 數變的內容。表示式也可能包含整數常數，像 5432；或雙精確度浮點數 3.14159；或引用其他變數計算而得的表示式，可以使用的函數如後所述。

例如：

```
\set ntellers 10 * :scale
\set aid (1021 * random(1, 100000 * :scale)) % \
           (100000 * :scale) + 1
```

`\sleep number`\[ us \| ms \| s \]

使腳本執行暫停一段指定的時間，百萬分之一秒（us）、千分之一秒（ms）、或秒\(s）。如果省略單位的話，預設是秒。nubmer 可以是整數常數，或引用其他整數變數的內容。

例如：

```
\sleep 10 ms
```

`\setshell varname command`\[`argument`... \]

設定 varname 的內容是執行另一個命令列指令的結果。該命令列指令必須透過標準輸出回傳整數。

command 和每一個 argument 都可以是文字常數或使用 :variablename 引用其他變數內容。如果你要使用 argument 的話，以冒號開始，而第一個 argument 要再多一個冒號。

例如：

```
\setshell variable_to_be_assigned command literal_argument :variable ::literal_starting_with_colon
```

`\shell command`\[`argument`... \]

和 \setshell 一樣，只是不處理回傳值。

例如：

```
\shell command literal_argument :variable ::literal_starting_with_colon
```

### 內建函數

Table 241 是 pgbench 內建，可以在 \set 的函數。

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

random 函數使用的是均勻分配亂數，也就是在指定範圍內的數值，都有相等的產生機率。random\_exponential 和 random\_gaussian 則需要額外的參數，來指定精確的分配情況。

* 指數分配，參數控制其分配情況是透過分段一個快速下降的指數分配，投影在指定範圍間的整數而得。精確來說，以下面的式子計算而得：  
  f\(x\) = exp\(-parameter \* \(x - min\) / \(max - min + 1\)\) / \(1 - exp\(-parameter\)\)  
  區間中某個 i 值的機率為 f\(i\) - f\(i + 1\)。  
  直覺上，越大的輸入參數，就會越多較小的數值被輸出，而較少的大數值產生。如果參數接近 0 的話，就會很接近均勻分配。一個粗略的概念是，機率最高的 1%，落於靠近最小值的一端，機率大概是百分之（parameter）。此參數必須要是正整數。

* 高斯分配，指定區間會映射到一個標準常態分配的空間（典型的錐型高斯曲線），分佈於 -parameter 及 +parameter 之間。靠中間的值有更高的選取機率。精確來說，如果 PHI\(x\) 是該常態分配的累計分配函數的話，那麼平均數 mu 就是 \(max + min\) / 2.0，則：  
  f\(x\) = PHI\(2.0 \* parameter \* \(x - mu\) / \(max - min + 1\)\) / \(2.0 \* PHI\(parameter\) - 1\)  
  在區間中，數值 i 被選取的機率就是：f\(i + 0.5\) - f\(i - 0.5\)。直覺上，parameter 越大，就會有越多中間值被選值，而越小的話，兩側數側被選擇的機率就會增加。約有 67% 的結果會在靠近 1.0 / parameter 中間的值，相對於 0.5 / parameter 近乎在平均值的附近；2.0 / parameter 則是 95% 是靠近中間的值，相對於 1.0 / parameter 近乎在平均值的附近。舉例來說，如果 parameter = 4.0，大概有 67% 的值會來自於中間的四分之一（即 3.0 / 8.0 到 5.0 / 8.0），而 95% 來自於中間的一半（2.0 / 4.0），第二和第三的四分位數之間。以 Box-Muller 轉換的效率來說，parameter 最小值為 2.0。

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

其中 client\_id 指的是哪一個用戶的連線代號，transaction\_no 計算有多交易在該連線中被執行了，time 是整個交易的持續時間，單位是亳秒，script\_no 指出是使用哪一個腳本（當透過 -f 或 -b 使用多個腳本時會很有用），而 time\_epoch／timeus 是 Unix-epoch 格式的時間戳記，記錄該交易的完成時間，單位是亳秒（適當地建立一個 ISO 8601 時間戳記再加上小數）。schedule\_lag 欄位是交易排程時間的差值，以及實際開始的時間，單位是亳秒，只有在 --rate 使用時才會出現。當 --rate 和 --latecy-limit 一起使用時，time 欄位在被跳過的交易上，會註明 skipped。

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

當某個主機執行長時間的交易時，記錄檔案可能會變得非常大。選項 --sampling-rate 就可以派上用場，只存下部份的交易樣本。

### 彙總記錄

使用 --aggregate-interval 選項時，會是另一種記錄檔格式：

```
interval_start num_transactions sum_latency sum_latency_2 min_latency max_latency [sum_lag sum_lag_2 min_lag max_lag [ skipped ] ]
```

其中 interval\_start 是區間的起始時間（Unix epoch 時間戳記），num\_transactions 是區間裡交易的總數，sum\_latency 是區間裡交易的延遲量，sum\_latency\_2 則是交易延遲的平方和，min\_latency 是區間中最短延遲，而 max\_latency 則是區間中的最長延遲。接下來的欄位，sum\_lag、sum\_lag\_2、min\_lag、max\_lag，只有在指定 --rate 選項時才會出現。它們提供了每一個交易等待前一個交易結束時間的統計，也就是每一個交易的排程時間和實際執行時間的差異。而最後一個欄位 skipped，只會出現在也用了 --latency-limit 選項時，它計算交易被跳過的數目，因為他們太晚啓動了。每一個交易在區間中的都會被計算，當該交易被提交時。

這裡是一些輸出範例：

```
1345828501 5601 1542744 483552416 61 2573
1345828503 7884 1979812 565806736 60 1479
1345828505 7208 1979422 567277552 59 1391
1345828507 7685 1980268 569784714 60 1398
1345828509 7073 1979779 573489941 236 1411
```

注意，一般的記錄檔（非彙總式）會記錄交易由哪一個腳本產生，但彙總式記錄則不會。所以如果你需要分別不同的腳本彙總，你需要自行處理。

### Per-Statement Latencies

With the`-r`option,pgbenchcollects the elapsed transaction time of each statement executed by every client. It then reports an average of those values, referred to as the latency for each statement, after the benchmark has finished.

For the default script, the output will look similar to this:

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

