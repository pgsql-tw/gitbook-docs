<a id="CONFIG-SETTING"></a>

## 19.1. 設定參數 [#](#CONFIG-SETTING)

[19.1.1. 參數名稱與數值](config-setting.md#CONFIG-SETTING-NAMES-VALUES)

[19.1.2. 透過組態設定檔進行參數互動](config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE)

[19.1.3. 透過 SQL 進行參數互動](config-setting.md#CONFIG-SETTING-SQL)

[19.1.4. 透過 Shell 進行參數互動](config-setting.md#CONFIG-SETTING-SHELL)

[19.1.5. 管理組態設定檔內容](config-setting.md#CONFIG-INCLUDES)

<a id="CONFIG-SETTING-NAMES-VALUES"></a>

### 19.1.1. 參數名稱與數值 [#](#CONFIG-SETTING-NAMES-VALUES)

所有參數名稱皆不區分大小寫。每個參數的值皆屬於五種型別之一：
布林（boolean）、字串（string）、整數（integer）、浮點數（floating point），
或列舉（enumerated，enum）。此型別決定了設定該參數的語法：

* *布林：*
  值可以寫成
  `on`、
  `off`、
  `true`、
  `false`、
  `yes`、
  `no`、
  `1`、
  `0`
  （皆不區分大小寫），或這些值任一者不會造成歧義的前綴。
* *字串：*
  一般而言，值應以單引號括住，值中若含有單引號則需重複兩次。
  不過，如果值是簡單的數字或識別字，通常可以省略引號。
  （若值恰好與 SQL 關鍵字相符，在某些情境下仍需加上引號。）
* *數值（整數與浮點數）：*
  數值參數可以用常見的整數與浮點數格式指定；如果參數為整數型別，
  小數值會四捨五入到最接近的整數。整數參數另外還接受
  十六進位輸入（以 `0x` 開頭）與八進位輸入
  （以 `0` 開頭），但這些格式不能含有小數部分。
  請勿使用千位數分隔符號。
  除十六進位輸入外，不需要加上引號。
* *附帶單位的數值：*
  部分數值參數帶有隱含的單位，因為它們描述的是記憶體
  或時間的量。此單位可能是位元組、千位元組、區塊
  （通常為八千位元組）、毫秒、秒，或分鐘。
  若對這類設定僅指定不含單位的數值，則會使用該設定的
  預設單位，可從
  `pg_settings`.`unit` 得知。
  為了方便起見，設定值可以明確指定單位，
  例如時間值可寫成 `'120 ms'`，這些值會被
  轉換為該參數實際使用的單位。請注意，
  若要使用此功能，該值必須以字串形式（加上引號）撰寫。
  單位名稱區分大小寫，且數值與單位之間可以有空白字元。

  * 合法的記憶體單位有 `B`（位元組）、
    `kB`（千位元組）、
    `MB`（百萬位元組）、`GB`
    （十億位元組），以及 `TB`（兆位元組）。
    記憶體單位的乘數為 1024，而非 1000。
  * 合法的時間單位有
    `us`（微秒）、
    `ms`（毫秒）、
    `s`（秒）、`min`（分鐘）、
    `h`（小時），以及 `d`（天）。

  若指定的小數值帶有單位，且存在次一級較小的單位，
  則會四捨五入為次一級單位的倍數。
  例如，`30.1 GB` 會被轉換
  為 `30822 MB`，而不是 `32319628902 B`。
  如果該參數為整數型別，則會在任何單位轉換之後，
  再進行一次最終的四捨五入為整數。
* *列舉：*
  列舉型別參數的寫法與字串參數相同，但只能是
  有限值集合中的其中一個。這類參數所允許的值可以從
  `pg_settings`.`enumvals` 中查得。
  列舉參數值不區分大小寫。

<a id="CONFIG-SETTING-CONFIGURATION-FILE"></a>

### 19.1.2. 透過組態設定檔進行參數互動 [#](#CONFIG-SETTING-CONFIGURATION-FILE)

設定這些參數最基本的方式，是編輯
`postgresql.conf`<a id="id-1.6.6.4.3.2.2"></a> 檔案，
此檔案通常放在資料目錄中。初始化資料庫叢集目錄時，
會安裝一份預設的副本。
此檔案的內容大致如下範例所示：

```

# This is a comment
log_connections = all
log_destination = 'syslog'
search_path = '"$user", public'
shared_buffers = 128MB
```

每一行指定一個參數。名稱與值之間的等號是可省略的。
空白字元不具意義（引號括住的參數值內部除外），
空白行則會被忽略。井字號（`#`）表示該行其餘部分
為註解。並非簡單識別字或數字的參數值，必須以單引號括住。
若要在參數值中內嵌單引號，可寫成兩個引號（建議）
或反斜線加引號。
若檔案中對同一個參數有多筆設定，
除最後一筆之外的設定都會被忽略。

以此方式設定的參數，會為叢集提供預設值。
除非有其他設定覆寫，否則作用中工作階段所看到的
即為這些設定值。以下各節說明管理者或使用者
可以用來覆寫這些預設值的方式。

<a id="id-1.6.6.4.3.4.1"></a>
每當主要伺服器程序收到 SIGHUP 訊號時，
組態設定檔就會被重新讀取；最簡單的觸發方式，
是在命令列上執行 `pg_ctl reload`，
或呼叫 SQL 函式 `pg_reload_conf()`。主要
伺服器程序也會將此訊號傳遞給所有目前執行中的
伺服器程序，因此既有的工作階段也會採用新的值
（這會在它們完成目前執行中的用戶端命令之後發生）。
你也可以直接
將訊號傳送給單一伺服器程序。有些參數
只能在伺服器啟動時設定；在伺服器重新啟動之前，
對組態設定檔中這些項目所做的任何變更都會被忽略。
在處理 SIGHUP 期間，組態設定檔中無效的參數設定
同樣會被忽略（但會記錄下來）。

除了 `postgresql.conf` 之外，
PostgreSQL 資料目錄還包含一個
`postgresql.auto.conf`<a id="id-1.6.6.4.3.5.4"></a> 檔案，
其格式與 `postgresql.conf` 相同，但
目的是供自動編輯，而非手動編輯。此檔案保存透過
[`ALTER SYSTEM`](../../reference/sql-commands/sql-altersystem.md) 命令提供的設定。
每當讀取 `postgresql.conf` 時，
此檔案也會被讀取，且其中的設定會以相同方式生效。
`postgresql.auto.conf` 中的設定
會覆寫 `postgresql.conf` 中的設定。

外部工具也可能
修改 `postgresql.auto.conf`。除非
[allow_alter_system](runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM) 設為 `off`，
否則不建議在伺服器執行期間這麼做，因為並行執行的
`ALTER SYSTEM` 命令可能會覆寫
這類變更。這類工具可能只是單純將新設定附加到檔案結尾，
也可能選擇移除重複的設定與（或）註解
（如同 `ALTER SYSTEM` 的做法）。

系統檢視表
[`pg_file_settings`](../../internals/views/view-pg-file-settings.md)
有助於預先測試組態設定檔的變更，或是在
SIGHUP 訊號未產生預期效果時用於診斷問題。

<a id="CONFIG-SETTING-SQL"></a>

### 19.1.3. 透過 SQL 進行參數互動 [#](#CONFIG-SETTING-SQL)

PostgreSQL 提供三個 SQL
命令，用來建立組態設定預設值。
前面已提過的 `ALTER SYSTEM` 命令，
提供了可透過 SQL 存取的方式來變更全域預設值；其功能
等同於編輯 `postgresql.conf`。
此外，還有兩個命令可以逐資料庫或逐角色設定
預設值：

* [`ALTER DATABASE`](../../reference/sql-commands/sql-alterdatabase.md) 命令允許
  逐資料庫覆寫全域設定。
* [`ALTER ROLE`](../../reference/sql-commands/sql-alterrole.md) 命令允許
  以使用者專屬的值覆寫全域設定與逐資料庫設定。

以 `ALTER DATABASE` 與 `ALTER ROLE` 設定的值，
只有在啟動新的資料庫工作階段時才會套用。這些值
會覆寫從組態設定檔或伺服器命令列取得的值，
並在此後成為該工作階段其餘時間的預設值。
請注意，有些設定在伺服器啟動後就無法變更，
因此也無法透過這些命令（或以下所列的命令）設定。

一旦用戶端連線到資料庫，PostgreSQL
提供另外兩個 SQL 命令（以及對應的函式），
可用於與工作階段層級的組態設定互動：

* [`SHOW`](../../reference/sql-commands/sql-show.md) 命令允許檢視
  任何參數的目前值。對應的 SQL 函式為
  `current_setting(setting_name text)`
  （參閱[9.28.1 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SET)）。
* [`SET`](../../reference/sql-commands/sql-set.md) 命令允許修改
  可在工作階段層級本機設定之參數的目前值；
  這對其他工作階段沒有影響。
  許多參數任何使用者皆可以此方式設定，但有些參數
  只能由超級使用者，以及被授予該參數
  `SET` 權限的使用者設定。
  對應的 SQL 函式為
  `set_config(setting_name, new_value, is_local)`
  （參閱[9.28.1 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SET)）。

此外，系統檢視表 [`pg_settings`](../../internals/views/view-pg-settings.md) 也可以
用來檢視與變更工作階段層級的值：

* 查詢此檢視表的效果類似於使用 `SHOW ALL`，
  但提供更多細節。此方式也更有彈性，因為
  可以指定篩選條件，或與其他關聯進行聯結。
* 對此檢視表使用 `UPDATE`，特別是
  更新 `setting` 欄位，等同於
  發出 `SET` 命令。舉例來說，以下命令

  ```

  SET configuration_parameter TO DEFAULT;
  ```

  等同於：

  ```

  UPDATE pg_settings SET setting = reset_val WHERE name = 'configuration_parameter';
  ```

<a id="CONFIG-SETTING-SHELL"></a>

### 19.1.4. 透過 Shell 進行參數互動 [#](#CONFIG-SETTING-SHELL)

除了設定全域預設值，或在資料庫或角色層級
附加覆寫值之外，你也可以透過 shell 機制
將設定值傳遞給 PostgreSQL。
伺服器與 libpq 用戶端函式庫
都接受透過 shell 傳入的參數值。

* 在伺服器啟動期間，可以透過
  `-c name=value` 命令列參數，或其等效寫法
  `--name=value`，將參數設定傳遞給
  `postgres` 命令。例如：

  ```

  postgres -c log_connections=all --log-destination='syslog'
  ```

  以此方式提供的設定，會覆寫透過
  `postgresql.conf` 或 `ALTER SYSTEM`
  設定的值，因此若不重新啟動伺服器，就無法全域變更這些值。
* 透過 libpq 啟動用戶端工作階段時，
  可以使用 `PGOPTIONS` 環境變數
  指定參數設定。
  以此方式建立的設定，會在整個工作階段期間
  成為預設值，但不會影響其他工作階段。
  由於歷史因素，`PGOPTIONS` 的格式
  與啟動 `postgres`
  命令時所用的格式類似；具體來說，名稱前必須指定
  `-c`，或加上前綴的
  `--`。例如：

  ```

  env PGOPTIONS="-c geqo=off --statement-timeout=5min" psql
  ```

  其他用戶端與函式庫可能會提供各自的機制，
  無論是透過 shell 或其他方式，讓使用者
  能夠變更工作階段設定，而不需直接使用 SQL 命令。

<a id="CONFIG-INCLUDES"></a>

### 19.1.5. 管理組態設定檔內容 [#](#CONFIG-INCLUDES)

PostgreSQL 提供多項功能，可將複雜的
`postgresql.conf` 檔案拆分為子檔案。
在管理多台組態設定相關、但不完全相同的伺服器時，
這些功能特別有用。

<a id="id-1.6.6.4.6.3.1"></a>
除了個別的參數設定之外，
`postgresql.conf` 檔案還可以包含*引入指示詞
（include directive）*，用來指定另一個檔案，該檔案會被讀取並處理，
如同它被插入到組態設定檔的這個位置一般。這項
功能可以將組態設定檔拆分成多個實體上分離的部分。引入指示詞
的寫法很簡單：

```

include 'filename'
```

如果檔案名稱不是絕對路徑，則會被視為相對於
包含此引入指示詞的組態設定檔所在的目錄。
引入可以巢狀。

<a id="id-1.6.6.4.6.4.1"></a>
另外還有一個 `include_if_exists` 指示詞，其行為
與 `include` 指示詞相同，唯一差別在於
當被參照的檔案不存在或無法讀取時的處理方式。一般的
`include` 會將此情況視為錯誤，但
`include_if_exists` 只會記錄一則訊息，並繼續
處理該引入指示詞所在的組態設定檔。

<a id="id-1.6.6.4.6.5.1"></a>
`postgresql.conf` 檔案也可以包含
`include_dir` 指示詞，用來指定要引入
一整個目錄的組態設定檔。其寫法如下

```

include_dir 'directory'
```

非絕對路徑的目錄名稱，會被視為相對於
包含此指示詞的組態設定檔所在的目錄。在指定的
目錄中，只有名稱以
`.conf` 結尾的非目錄檔案才會被引入。以
`.` 字元開頭的檔案名稱同樣會被忽略，
以避免因這類檔案在某些平台上是隱藏檔案而造成錯誤。
引入目錄中若有多個檔案，會依檔案名稱順序處理
（依照 C 地區設定規則，也就是數字排在字母之前，
大寫字母排在小寫字母之前）。

引入檔案或目錄可以用來在邏輯上分隔資料庫組態設定
的各個部分，而不必使用單一龐大的
`postgresql.conf` 檔案。試想一家公司有兩台
資料庫伺服器，各自擁有不同的記憶體容量。兩者的組態設定
很可能有部分是共通的，例如日誌相關的設定。但伺服器上
與記憶體相關的參數則會因兩者而異。此外可能還有一些
伺服器專屬的自訂設定。管理此情況的一種方式，
是將你站台的自訂組態設定變更拆分成三個檔案。你可以
在 `postgresql.conf` 檔案結尾加入以下內容，
以引入這些檔案：

```

include 'shared.conf'
include 'memory.conf'
include 'server.conf'
```

所有系統都會使用相同的 `shared.conf`。每台
記憶體容量相同的伺服器，可以共用
同一份 `memory.conf`；你可能會為所有擁有
8GB 記憶體的伺服器準備一份，為擁有 16GB 記憶體的伺服器準備另一份。
最後，`server.conf` 則可以放入真正
針對伺服器專屬的組態設定資訊。

另一種可能的做法，是建立一個組態設定檔目錄，
並將這些資訊放入該目錄下的檔案中。舉例來說，可以在
`postgresql.conf` 結尾參照一個 `conf.d`
目錄：

```

include_dir 'conf.d'
```

接著，你可以像這樣為 `conf.d` 目錄
中的檔案命名：

```

00shared.conf
01memory.conf
02server.conf
```

這種命名慣例，為這些檔案的載入順序建立了明確的規則。
這一點很重要，因為在伺服器讀取組態設定檔的過程中，
針對特定參數，只有最後遇到的設定才會被採用。
在此範例中，`conf.d/02server.conf` 中設定的值，
會覆寫 `conf.d/01memory.conf` 中設定的值。

你也可以改用以下方式，以更具描述性的方式為檔案命名：

```

00shared.conf
01memory-8GB.conf
02server-foo.conf
```

這種安排方式，為每個組態設定檔的變化版本
提供了唯一的名稱。當多台伺服器的組態設定都
存放在同一個地方（例如版本控制儲存庫）時，
這有助於消除混淆。（將資料庫組態設定檔納入版本
控制，也是值得考慮的另一項良好做法。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/config-setting.html)（原文版本：18.6；核對日期：2026-09-26）
