<a id="APP-PSQL"></a><a id="id-1.9.4.21.1"></a>

## psql

psql — PostgreSQL 互動式終端機

<a id="id-1.9.4.21.4"></a>

## 語法

<a id="id-1.9.4.21.4.1"></a>

`psql` [*`option`*...] [*`dbname`*
[*`username`*]]

<a id="id-1.9.4.21.5"></a>

## 說明

psql 是 PostgreSQL 的終端機式前端程式。它讓你能以互動方式輸入查詢、將查詢送給 PostgreSQL，並查看查詢結果。輸入也可以來自檔案或命令列引數。此外，psql 提供了許多中繼命令（meta-command）以及各種類似 shell 的功能，方便撰寫腳本並將各式各樣的工作自動化。

<a id="R1-APP-PSQL-3"></a>

## 選項

<a id="APP-PSQL-OPTION-ECHO-ALL"></a>

`-a`<br>`--echo-all` [#](#APP-PSQL-OPTION-ECHO-ALL)
:   在讀取所有非空的輸入行時，將其印到標準輸出。（這不適用於以互動方式讀取的輸入行。）這等同於將變數 `ECHO` 設為
    `all`。
<a id="APP-PSQL-OPTION-NO-ALIGN"></a>

`-A`<br>`--no-align` [#](#APP-PSQL-OPTION-NO-ALIGN)
:   切換為非對齊輸出模式。（預設的輸出模式為
    `aligned`。）這等同於
    `\pset format unaligned`。
<a id="APP-PSQL-OPTION-ECHO-ERRORS"></a>

`-b`<br>`--echo-errors` [#](#APP-PSQL-OPTION-ECHO-ERRORS)
:   將執行失敗的 SQL 命令印到標準錯誤輸出。這等同於將變數 `ECHO` 設為
    `errors`。
<a id="APP-PSQL-OPTION-COMMAND"></a>

`-c command`<br>`--command=command` [#](#APP-PSQL-OPTION-COMMAND)

指定 psql 要執行給定的命令字串 *`command`*。
此選項可以重複使用，並可與 `-f` 選項以任意順序組合。指定了 `-c`
或 `-f` 其中之一時，psql
不會從標準輸入讀取命令；而是依序處理完所有 `-c` 與 `-f`
選項後結束。

*`command`* 必須是可由伺服器完整剖析的命令字串（也就是不含任何 psql 專屬功能），或是單一個反斜線命令。因此，你不能在一個 `-c` 選項中混用 SQL 與 psql 中繼命令。若要達到這個目的，你可以重複使用 `-c` 選項，或將字串以管線傳給 psql，例如：

```

    psql -c '\x' -c 'SELECT * FROM foo;'
```

或

```

    echo '\x \\ SELECT * FROM foo;' | psql
```

（`\\` 是分隔用的中繼命令。）

傳給 `-c` 的每個 SQL 命令字串都會以單一請求送給伺服器。因此，即使字串中包含多個 SQL 命令，伺服器仍會將它當作單一交易執行，除非字串中包含明確的 `BEGIN`/`COMMIT`
命令把它分成多個交易。（關於伺服器如何處理含多個查詢的字串，詳情請參閱[第 54.2.2.1 節](../../internals/protocol/protocol-flow.md#PROTOCOL-FLOW-MULTI-STATEMENT)。）

若不希望多個命令在同一個交易中執行，請重複使用 `-c` 命令，或將多個命令餵給 psql 的標準輸入，可以像上面那樣使用 echo，或透過 shell 的 here-document，例如：

```

    psql <<EOF
    \x
    SELECT * FROM foo;
    EOF
```
<a id="APP-PSQL-OPTION-CSV"></a>

`--csv` [#](#APP-PSQL-OPTION-CSV)
:   切換為 CSV（逗號分隔值）輸出模式。這等同於 `\pset format csv`。
<a id="APP-PSQL-OPTION-DBNAME"></a>

`-d dbname`<br>`--dbname=dbname` [#](#APP-PSQL-OPTION-DBNAME)
:   指定要連線的資料庫名稱。這等同於在命令列上將 *`dbname`* 指定為第一個非選項引數。*`dbname`*
    可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。
    若是如此，連線字串參數會覆寫任何與之衝突的命令列選項。
<a id="APP-PSQL-OPTION-ECHO-QUERIES"></a>

`-e`<br>`--echo-queries` [#](#APP-PSQL-OPTION-ECHO-QUERIES)
:   將所有送給伺服器的 SQL 命令同時複製到標準輸出。這等同於將變數 `ECHO` 設為
    `queries`。
<a id="APP-PSQL-OPTION-ECHO-HIDDEN"></a>

`-E`<br>`--echo-hidden` [#](#APP-PSQL-OPTION-ECHO-HIDDEN)
:   回顯由 `\d` 及其他反斜線命令所產生的實際查詢。你可以藉此研究 psql 的內部運作。這等同於將變數 `ECHO_HIDDEN` 設為 `on`。
<a id="APP-PSQL-OPTION-FILE"></a>

`-f filename`<br>`--file=filename` [#](#APP-PSQL-OPTION-FILE)
:   從檔案 *`filename`* 讀取命令，而不是從標準輸入讀取。
    此選項可以重複使用，並可與 `-c` 選項以任意順序組合。指定了 `-c`
    或 `-f` 其中之一時，psql
    不會從標準輸入讀取命令；而是依序處理完所有 `-c` 與 `-f`
    選項後結束。
    除此之外，此選項大致等同於中繼命令 `\i`。

    若 *`filename`* 為 `-`
    （連字號），則會讀取標準輸入，直到遇到 EOF 標示或 `\q` 中繼命令為止。這可以用來將互動式輸入與來自檔案的輸入穿插使用。不過請注意，這種情況下不會使用 Readline（就如同指定了 `-n` 一樣）。

    使用此選項與寫成 `psql
    < filename` 有些微妙的差異。一般來說，兩者都會如你預期般運作，但使用 `-f`
    可以啟用一些好用的功能，例如附有行號的錯誤訊息。使用此選項也有些微可能降低啟動的負擔。另一方面，使用 shell 輸入重新導向的寫法（理論上）保證產生的輸出會與你全部以手動輸入時得到的輸出完全相同。
<a id="APP-PSQL-OPTION-FIELD-SEPARATOR"></a>

`-F separator`<br>`--field-separator=separator` [#](#APP-PSQL-OPTION-FIELD-SEPARATOR)
:   使用 *`separator`* 作為非對齊輸出的欄位分隔字元。這等同於
    `\pset fieldsep` 或 `\f`。
<a id="APP-PSQL-OPTION-FIELD-HOST"></a>

`-h hostname`<br>`--host=hostname` [#](#APP-PSQL-OPTION-FIELD-HOST)
:   指定伺服器所在機器的主機名稱。若此值以斜線開頭，則會用來作為 Unix 網域通訊端 的目錄。
<a id="APP-PSQL-OPTION-HTML"></a>

`-H`<br>`--html` [#](#APP-PSQL-OPTION-HTML)
:   切換為 HTML 輸出模式。這等同於 `\pset format html` 或
    `\H` 命令。
<a id="APP-PSQL-OPTION-LIST"></a>

`-l`<br>`--list` [#](#APP-PSQL-OPTION-LIST)
:   列出所有可用的資料庫，然後結束。其他非連線相關的選項會被忽略。這類似於中繼命令
    `\list`。

    使用此選項時，psql 會連線到資料庫 `postgres`，除非在命令列上指定了其他資料庫（以選項 `-d` 或非選項引數指定，也可以透過服務項目指定，但不能透過環境變數指定）。
<a id="APP-PSQL-OPTION-LOG-FILE"></a>

`-L filename`<br>`--log-file=filename` [#](#APP-PSQL-OPTION-LOG-FILE)
:   除了正常的輸出目的地之外，也將所有查詢輸出寫入檔案 *`filename`*。
<a id="APP-PSQL-OPTION-NO-READLINE"></a>

`-n`<br>`--no-readline` [#](#APP-PSQL-OPTION-NO-READLINE)
:   不使用 Readline 進行行編輯，也不使用命令歷史（請參閱下方的[「命令列編輯」一節](app-psql.md#APP-PSQL-READLINE)）。
<a id="APP-PSQL-OPTION-OUTPUT"></a>

`-o filename`<br>`--output=filename` [#](#APP-PSQL-OPTION-OUTPUT)
:   將所有查詢輸出寫入檔案 *`filename`*。這等同於命令 `\o`。
<a id="APP-PSQL-OPTION-PORT"></a>

`-p port`<br>`--port=port` [#](#APP-PSQL-OPTION-PORT)
:   指定伺服器用來監聽連線的 TCP 連接埠，或本機 Unix 網域通訊端 檔案的副檔名。預設為環境變數 `PGPORT`
    的值；若未設定，則為編譯時指定的連接埠，通常是 5432。
<a id="APP-PSQL-OPTION-PSET"></a>

`-P assignment`<br>`--pset=assignment` [#](#APP-PSQL-OPTION-PSET)
:   以 `\pset` 的形式指定列印選項。請注意，在這裡你必須用等號而不是空格來分隔名稱與值。例如，若要將輸出格式設為 LaTeX，你可以寫成
    `-P format=latex`。
<a id="APP-PSQL-OPTION-QUIET"></a>

`-q`<br>`--quiet` [#](#APP-PSQL-OPTION-QUIET)
:   指定 psql 應該安靜地執行工作。預設情況下，它會印出歡迎訊息與各種資訊性輸出。若使用此選項，這些都不會出現。這與 `-c` 選項搭配使用時很有用。
    這等同於將變數 `QUIET`
    設為 `on`。
<a id="APP-PSQL-OPTION-RECORD-SEPARATOR"></a>

`-R separator`<br>`--record-separator=separator` [#](#APP-PSQL-OPTION-RECORD-SEPARATOR)
:   使用 *`separator`* 作為非對齊輸出的記錄分隔字元。這等同於
    `\pset recordsep`。
<a id="APP-PSQL-OPTION-SINGLE-STEP"></a>

`-s`<br>`--single-step` [#](#APP-PSQL-OPTION-SINGLE-STEP)
:   以單步模式執行。這表示在每個命令送給伺服器之前，都會提示使用者，並提供取消執行的選擇。可用此模式來除錯腳本。
<a id="APP-PSQL-OPTION-SINGLE-LINE"></a>

`-S`<br>`--single-line` [#](#APP-PSQL-OPTION-SINGLE-LINE)
:   以單行模式執行，在此模式下，換行字元會像分號一樣結束一個 SQL 命令。

    <a id="APP-PSQL-OPTION-SINGLE-LINE-NOTE"></a>

    ### 注意

    提供此模式是為了堅持要使用它的人，但並不一定鼓勵你使用。特別是，若你在同一行混用 SQL 與中繼命令，對沒有經驗的使用者而言，執行順序未必總是清楚明白。
<a id="APP-PSQL-OPTION-TUPLES-ONLY"></a>

`-t`<br>`--tuples-only` [#](#APP-PSQL-OPTION-TUPLES-ONLY)
:   關閉欄位名稱與結果資料列數頁尾等的列印。這等同於 `\t` 或
    `\pset tuples_only`。
<a id="APP-PSQL-OPTION-TABLE-ATTR"></a>

`-T table_options`<br>`--table-attr=table_options` [#](#APP-PSQL-OPTION-TABLE-ATTR)
:   指定要放在 HTML `table` 標籤內的選項。詳情請參閱
    `\pset tableattr`。
<a id="APP-PSQL-OPTION-USERNAME"></a>

`-U username`<br>`--username=username` [#](#APP-PSQL-OPTION-USERNAME)
:   以使用者 *`username`* 而非預設使用者的身分連線到資料庫。
    （當然，你必須具有這麼做的權限。）
<a id="APP-PSQL-OPTION-VARIABLE"></a>

`-v assignment`<br>`--set=assignment`<br>`--variable=assignment` [#](#APP-PSQL-OPTION-VARIABLE)
:   進行變數指派，就像 `\set`
    中繼命令一樣。請注意，在命令列上你必須用等號分隔名稱與值（若有值的話）。若要取消設定變數，請省略等號。若要將變數設為空字串值，請保留等號但省略值。這些指派是在處理命令列時進行的，因此反映連線狀態的變數之後會被覆寫。
<a id="APP-PSQL-OPTION-VERSION"></a>

`-V`<br>`--version` [#](#APP-PSQL-OPTION-VERSION)
:   印出 psql 的版本後結束。
<a id="APP-PSQL-OPTION-NO-PASSWORD"></a>

`-w`<br>`--no-password` [#](#APP-PSQL-OPTION-NO-PASSWORD)

永不提示輸入密碼。若伺服器要求密碼認證，而又無法從其他來源（例如 `.pgpass` 檔案）取得密碼，連線嘗試就會失敗。此選項在沒有使用者可輸入密碼的批次作業與腳本中可能很有用。

請注意，此選項在整個工作階段中都會保持設定，因此它除了影響初始的連線嘗試之外，也會影響中繼命令
`\connect` 的使用。
<a id="APP-PSQL-OPTION-PASSWORD"></a>

`-W`<br>`--password` [#](#APP-PSQL-OPTION-PASSWORD)

強制 psql 在連線到資料庫之前提示輸入密碼，即使該密碼不會被使用。

若伺服器要求密碼認證，而又無法從其他來源（例如 `.pgpass`
檔案）取得密碼，psql 無論如何都會提示輸入密碼。不過，psql
會浪費一次連線嘗試才發現伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免這次額外的連線嘗試。

請注意，此選項在整個工作階段中都會保持設定，因此它除了影響初始的連線嘗試之外，也會影響中繼命令
`\connect` 的使用。
<a id="APP-PSQL-OPTION-EXPANDED"></a>

`-x`<br>`--expanded` [#](#APP-PSQL-OPTION-EXPANDED)
:   開啟展開式表格格式模式。這等同於
    `\x` 或 `\pset expanded`。
<a id="APP-PSQL-OPTION-NO-PSQLRC"></a>

`-X`<br>`--no-psqlrc` [#](#APP-PSQL-OPTION-NO-PSQLRC)
:   不讀取啟動檔（既不讀取全系統的
    `psqlrc` 檔案，也不讀取使用者的
    `~/.psqlrc` 檔案）。
<a id="APP-PSQL-OPTION-FIELD-SEPARATOR-ZERO"></a>

`-z`<br>`--field-separator-zero` [#](#APP-PSQL-OPTION-FIELD-SEPARATOR-ZERO)
:   將非對齊輸出的欄位分隔字元設為值為 0 的位元組（NUL）。這等同於 `\pset fieldsep_zero`。
<a id="APP-PSQL-OPTION-RECORD-SEPARATOR-ZERO"></a>

`-0`<br>`--record-separator-zero` [#](#APP-PSQL-OPTION-RECORD-SEPARATOR-ZERO)
:   將非對齊輸出的記錄分隔字元設為值為 0 的位元組（NUL）。這在與其他程式銜接時很有用，例如搭配 `xargs -0`。
    這等同於 `\pset recordsep_zero`。
<a id="APP-PSQL-OPTION-SINGLE-TRANSACTION"></a>

`-1`<br>`--single-transaction` [#](#APP-PSQL-OPTION-SINGLE-TRANSACTION)

此選項只能與一個或多個
`-c` 和／或 `-f` 選項組合使用。它會使
psql 在第一個這類選項之前發出 `BEGIN` 命令，並在最後一個之後發出 `COMMIT` 命令，藉此將所有命令包在單一交易中。若任何一個命令失敗，且已設定變數
`ON_ERROR_STOP`，則改為送出
`ROLLBACK` 命令。這可確保要嘛所有命令都成功完成，要嘛不套用任何變更。

若命令本身包含 `BEGIN`、`COMMIT`
或 `ROLLBACK`，此選項就無法達到預期效果。此外，若某個命令無法在交易區塊內執行，指定此選項會導致整個交易失敗。
<a id="APP-PSQL-OPTION-HELP"></a>

`-?`<br>`--help[=topic]` [#](#APP-PSQL-OPTION-HELP)
:   顯示 psql 的說明後結束。選擇性的
    *`topic`* 參數（預設為
    `options`）用來選擇要說明 psql 的哪一部分：`commands` 說明 psql 的反斜線命令；`options` 說明可以傳給 psql 的命令列選項；而 `variables` 顯示 psql 設定變數的說明。

<a id="id-1.9.4.21.7"></a>

## 結束狀態

若正常結束，psql 會傳回 0 給 shell；若發生它本身的嚴重錯誤（例如記憶體不足、找不到檔案），傳回 1；若與伺服器的連線中斷且工作階段不是互動式的，傳回 2；若腳本中發生錯誤且已設定變數 `ON_ERROR_STOP`，則傳回 3。

<a id="id-1.9.4.21.8"></a>

## 用法

<a id="R2-APP-PSQL-CONNECTING"></a>

### 連線到資料庫

psql 是一般的 PostgreSQL 用戶端應用程式。要連線到資料庫，你需要知道目標資料庫的名稱、伺服器的主機名稱與連接埠號碼，以及要以哪個資料庫使用者名稱連線。你可以透過命令列選項告訴 psql 這些參數，分別是
`-d`、`-h`、`-p` 與
`-U`。若發現不屬於任何選項的引數，它會被解讀為資料庫名稱（若已指定資料庫名稱，則解讀為資料庫使用者名稱）。這些選項並非全都必要；它們都有好用的預設值。若省略主機名稱，psql 會透過 Unix 網域通訊端 連線到本機上的伺服器，在 Windows 上則透過 TCP/IP 連線到 `localhost`。預設的連接埠號碼是在編譯時決定的。由於資料庫伺服器使用相同的預設值，大多數情況下你不需要指定連接埠。預設的資料庫使用者名稱是你的作業系統使用者名稱。資料庫使用者名稱決定之後，它也會被用作預設的資料庫名稱。請注意，你不能以任意資料庫使用者名稱連線到任意資料庫。你的資料庫管理員應該已經告知你的存取權限。

當預設值不太合適時，你可以將環境變數
`PGDATABASE`、`PGHOST`、
`PGPORT` 和／或 `PGUSER` 設為適當的值，以省去一些輸入。（其他環境變數請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)。）使用
`~/.pgpass` 檔案也很方便，可以避免經常需要輸入密碼。詳情請參閱[第 32.16 節](../../client-interfaces/libpq/libpq-pgpass.md)。

指定連線參數的另一種方式是使用
*`conninfo`* 字串或 URI，用來取代資料庫名稱。這個機制讓你對連線有非常廣泛的控制。例如：

```

$ psql "service=myservice sslmode=require"
$ psql postgresql://dbmaster:5433/mydb?sslmode=require
```

如此一來，你也可以如[第 32.18 節](../../client-interfaces/libpq/libpq-ldap.md)所述，使用 LDAP 查詢連線參數。
所有可用連線選項的詳細資訊，請參閱[第 32.1.2 節](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-paramkeywords)。

若因任何原因（例如權限不足、伺服器未在目標主機上執行等）而無法建立連線，psql 會傳回錯誤並結束。

若標準輸入與標準輸出都是終端機，psql 會將用戶端編碼設為「auto」，它會從語系設定（在 Unix 系統上為環境變數 `LC_CTYPE`）偵測適當的用戶端編碼。若結果不如預期，可以使用環境變數 `PGCLIENTENCODING` 覆寫用戶端編碼。

<a id="R2-APP-PSQL-4"></a>

### 輸入 SQL 命令

在正常運作下，psql 會提供一個提示字串，內容是 psql 目前所連線的資料庫名稱，後面接著字串 `=>`。例如：

```

$ psql testdb
psql (18.6)
Type "help" for help.

testdb=>
```

使用者可以在提示字串後輸入 SQL 命令。通常，輸入行會在遇到結束命令的分號時送給伺服器。行尾並不會結束命令。因此，為了清楚起見，命令可以分散在多行中。若命令已送出並且執行時沒有錯誤，命令的結果會顯示在螢幕上。

若不受信任的使用者可以存取一個尚未採用[安全綱要使用模式](../../the-sql-language/ddl/ddl-schemas.md#ddl-schemas-patterns)的資料庫，請在工作階段一開始就從 `search_path` 移除公開可寫入的綱要。你可以在連線字串中加入 `options=-csearch_path=`，或在其他 SQL 命令之前執行 `SELECT pg_catalog.set_config('search_path', '',
false)`。這項考量並非 psql 所特有；它適用於每一個可執行任意 SQL 命令的介面。

每當執行一個命令時，psql 也會輪詢由
[`LISTEN`](../sql-commands/sql-listen.md) 與
[`NOTIFY`](../sql-commands/sql-notify.md) 所產生的非同步通知事件。

C 風格的區塊註解會傳給伺服器處理並移除，而 SQL 標準的註解則由 psql 移除。

<a id="APP-PSQL-META-COMMANDS"></a>

### 中繼命令

你在 psql 中輸入的任何以未加引號的反斜線開頭的內容，都是由 psql 本身處理的 psql 中繼命令。這些命令讓 psql 在管理或撰寫腳本時更加好用。中繼命令通常也稱為斜線命令或反斜線命令。

psql 命令的格式是反斜線，緊接著命令動詞，然後是任何引數。引數與命令動詞之間、以及引數彼此之間，以任意數量的空白字元分隔。

若要在引數中包含空白，你可以用單引號將它括起來。若要在引數中包含單引號，請在單引號括起的文字中寫兩個單引號。此外，單引號中的任何內容都會進行類似 C 語言的替換：
`\n`（換行）、`\t`（定位字元）、
`\b`（退格字元）、`\r`（歸位字元）、
`\f`（換頁字元）、
`\`*`digits`*（八進位）以及
`\x`*`digits`*（十六進位）。
在單引號括起的文字中，位於任何其他字元之前的反斜線會將該單一字元視為字面字元，無論它是什麼字元。

若引數中出現未加引號的冒號（`:`）後接 psql 變數名稱，它會被替換為該變數的值，如下方[SQL 插值](app-psql.md#APP-PSQL-INTERPOLATION)所述。
那裡所描述的 `:'variable_name'` 與
`:"variable_name"` 形式在此也同樣適用。
`:{?variable_name}` 語法可以用來測試變數是否已定義。它會被替換為 TRUE 或 FALSE。
以反斜線跳脫冒號可以保護它不被替換。

在引數中，以反引號（`` ` ``）括起的文字會被視為傳給 shell 的命令列。該命令的輸出（移除任何結尾的換行字元後）會取代以反引號括起的文字。在以反引號括起的文字中，不會進行特殊的引號處理或其他處理，唯一的例外是：出現 `:variable_name`（其中
*`variable_name`* 是 psql 變數名稱）時，會被替換為該變數的值。此外，出現
`:'variable_name'` 時，會被替換為經過適當引號處理、可成為單一 shell 命令引數的變數值。（後一種形式幾乎總是比較好的選擇，除非你非常確定變數中的內容。）由於歸位字元與換行字元無法在所有平台上安全地加上引號，當值中出現這類字元時，
`:'variable_name'` 形式會印出錯誤訊息，且不會替換變數值。

有些命令接受 SQL 識別字（例如資料表名稱）作為引數。這些引數遵循 SQL 的語法規則：未加引號的字母會被強制轉為小寫，而雙引號（`"`）可保護字母不被轉換大小寫，並允許在識別字中包含空白。在雙引號中，成對的雙引號在產生的名稱中會簡化為單一個雙引號。例如，
`FOO"BAR"BAZ` 會被解讀為 `fooBARbaz`，
而 `"A weird"" name"` 會變成 `A weird"
name`。

引數的剖析會在行尾或遇到另一個未加引號的反斜線時停止。未加引號的反斜線會被視為新中繼命令的開頭。特殊序列 `\\`（兩個反斜線）標示引數的結束，並繼續剖析 SQL 命令（若有的話）。如此一來，SQL 與 psql 命令就可以在同一行中自由混用。但無論如何，中繼命令的引數都不能延續到行尾之後。

許多中繼命令會作用在*目前的查詢緩衝區*上。
這只是一個緩衝區，存放已輸入但尚未送給伺服器執行的任何 SQL 命令文字。這包括先前的輸入行，以及同一行中出現在中繼命令之前的任何文字。

許多中繼命令也允許附加 `x` 作為選項。這會使結果以展開模式顯示，就如同使用了 `\x` 或 `\pset expanded`
一樣。

已定義的中繼命令如下：

<a id="APP-PSQL-META-COMMAND-A"></a>

`\a` [#](#APP-PSQL-META-COMMAND-A)
:   若目前的表格輸出格式為非對齊，則切換為對齊。
    若不是非對齊，則設為非對齊。此命令是為了向後相容性而保留。更通用的解決方式請參閱 `\pset`。
<a id="APP-PSQL-META-COMMAND-BIND"></a>

`\bind` [ *`parameter`* ] ... [#](#APP-PSQL-META-COMMAND-BIND)

設定下一次查詢執行的查詢參數，所指定的參數會傳給任何參數佔位符號
（`$1` 等）。

範例：

```

    INSERT INTO tbl1 VALUES ($1, $2) \bind 'first value' 'second value' \g
```

這也適用於 `\g` 以外的查詢執行命令，例如 `\gx` 與
`\gset`。

此命令會使用延伸查詢協定（請參閱[第 54.1.2 節](../../internals/protocol/protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)），這與一般 psql 運作所使用的簡單查詢協定不同。因此，此命令可用於從 psql 測試延伸查詢協定。（即使查詢沒有參數，而此命令指定了零個參數，仍會使用延伸查詢協定。）此命令只影響下一個執行的查詢；之後的所有查詢預設都會使用簡單查詢協定。
<a id="APP-PSQL-META-COMMAND-BIND-NAMED"></a>

`\bind_named` *`statement_name`* [ *`parameter`* ] ... [#](#APP-PSQL-META-COMMAND-BIND-NAMED)

`\bind_named` 等同於 `\bind`，
差別在於它的第一個參數是現有預備陳述式的名稱。空字串表示未命名的預備陳述式。

範例：

```

    INSERT INTO tbls1 VALUES ($1, $2) \parse stmt1
    \bind_named stmt1 'first value' 'second value' \g
```

此命令會使用延伸查詢協定（請參閱
[第 54.1.2 節](../../internals/protocol/protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)），這與一般 psql 運作所使用的簡單查詢協定不同。因此，此命令可用於從 psql 測試延伸查詢協定。
<a id="APP-PSQL-META-COMMAND-C-LC"></a>

`\c` 或 `\connect [ -reuse-previous=on|off ] [ dbname [ username ] [ host ] [ port ] | conninfo ]` [#](#APP-PSQL-META-COMMAND-C-LC)

建立與 PostgreSQL 伺服器的新連線。要使用的連線參數可以用位置語法指定（資料庫名稱、使用者、主機與連接埠其中一項或多項），也可以使用
[第 32.1.1 節](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)所詳述的 *`conninfo`*
連線字串指定。若未提供任何引數，則會使用與先前相同的參數建立新連線。

將
*`dbname`*、
*`username`*、
*`host`* 或
*`port`*
其中任何一個指定為 `-`，等同於省略該參數。

新連線可以重複使用先前連線的連線參數；不只是資料庫名稱、使用者、主機與連接埠，還包括其他設定，例如 *`sslmode`*。預設情況下，使用位置語法時會重複使用參數，但提供 *`conninfo`* 字串時則不會。將第一個引數傳入 `-reuse-previous=on`
或 `-reuse-previous=off` 可覆寫這個預設行為。若會重複使用參數，則任何未以位置參數或在 *`conninfo`*
字串中明確指定的參數，都會取自現有連線的參數。例外的是，若使用位置語法將 *`host`* 設定從先前的值變更，則現有連線參數中的任何 *`hostaddr`* 設定都會被捨棄。
此外，只有在使用者、主機與連接埠設定都未變更時，才會重複使用現有連線所用的密碼。
當命令既未指定也未重複使用某個參數時，會使用 libpq 的預設值。

若新連線建立成功，先前的連線就會關閉。
若連線嘗試失敗（使用者名稱錯誤、存取被拒等），而 psql 處於互動模式，則會保留先前的連線。但在執行非互動式腳本時，舊連線會被關閉並回報錯誤。這可能會、也可能不會終止腳本；若未終止，則所有存取資料庫的命令都會失敗，直到另一個 `\connect` 命令成功執行為止。之所以選擇這樣的區別，一方面是為了在打錯字時方便使用者，另一方面則是一種安全機制，避免腳本意外地在錯誤的資料庫上執行。
請注意，每當 `\connect` 命令嘗試重複使用參數時，所重複使用的值是最後一次成功連線的值，而不是之後任何失敗嘗試的值。
不過，在非互動式 `\connect` 失敗的情況下，之後不允許重複使用任何參數，因為腳本很可能會預期重複使用失敗的 `\connect`
中的值。

範例：

```

    => \c mydb myuser host.dom 6432
    => \c service=foo
    => \c "host=localhost port=5432 dbname=mydb connect_timeout=10 sslmode=disable"
    => \c -reuse-previous=on sslmode=require    -- changes only sslmode
    => \c postgresql://tom@localhost/mydb?application_name=myapp
```
<a id="APP-PSQL-META-COMMAND-C-UC"></a>

`\C [ title ]` [#](#APP-PSQL-META-COMMAND-C-UC)
:   設定作為查詢結果所印出之任何表格的標題，或取消設定任何這類標題。此命令等同於
    `\pset title title`。（此命令的名稱源自「caption」，因為它先前只用來設定 HTML 表格的標題。）

<a id="APP-PSQL-META-COMMAND-CD"></a>

`\cd [ directory ]` [#](#APP-PSQL-META-COMMAND-CD)
:   將目前的工作目錄變更為
    *`directory`*。若沒有引數，則變更為目前使用者的家目錄。關於如何找出家目錄的詳細資訊，請參閱[第 32.16 節](../../client-interfaces/libpq/libpq-pgpass.md)。

    <a id="APP-PSQL-META-COMMAND-CD-TIP"></a>

    ### 提示

    若要印出目前的工作目錄，請使用 `\! pwd`。
<a id="APP-PSQL-META-COMMAND-CLOSE-PREPARED"></a>

`\close_prepared` *`prepared_statement_name`* [#](#APP-PSQL-META-COMMAND-CLOSE-PREPARED)

關閉指定的預備陳述式。空字串表示未命名的預備陳述式。若不存在此名稱的預備陳述式，此操作不會有任何作用。

範例：

```

    SELECT $1 \parse stmt1
    \close_prepared stmt1
```

此命令會使用延伸查詢協定，這與一般 psql 運作所使用的簡單查詢協定不同。因此，此命令可用於從
psql 測試延伸查詢協定。
<a id="APP-PSQL-META-COMMAND-CONNINFO"></a>

`\conninfo` [#](#APP-PSQL-META-COMMAND-CONNINFO)

輸出目前資料庫連線的相關資訊，若使用 SSL，也包括 SSL 相關資訊。

請注意，`Client User` 欄位顯示的是連線當時的使用者，而
`Superuser` 欄位則表示目前使用者（在目前的執行情境中）是否具有超級使用者權限。這兩個使用者通常相同，但也可能不同，例如目前使用者已透過
`SET ROLE` 命令變更時。
<a id="APP-PSQL-META-COMMANDS-COPY"></a>

`\copy { table [ ( column_list ) ] } from { 'filename' | program 'command' | stdin | pstdin } [ [ with ] ( option [, ...] ) ] [ where condition ]`<br>`\copy { table [ ( column_list ) ] | ( query ) } to { 'filename' | program 'command' | stdout | pstdout } [ [ with ] ( option [, ...] ) ]` [#](#APP-PSQL-META-COMMANDS-COPY)
:   執行前端（用戶端）複製。這項操作會執行 SQL [`COPY`](../sql-commands/sql-copy.md)
    命令，但不是由伺服器讀取或寫入指定的檔案，而是由 psql 讀取或寫入該檔案，並在伺服器與本機檔案系統之間傳遞資料。
    這表示檔案的可存取性與權限取決於本機使用者，而非伺服器，而且不需要 SQL 超級使用者權限。

    指定 `program` 時，
    *`command`* 會由 psql 執行，而傳自或傳往
    *`command`* 的資料會在伺服器與用戶端之間傳遞。
    同樣地，執行權限取決於本機使用者，而非伺服器，而且不需要 SQL 超級使用者權限。

    對於 `\copy ... from stdin`，資料列會從發出此命令的同一個來源讀取，直到讀到只含有
    `\.`
    的一行，或資料流到達 EOF 為止。此選項適合用於在 SQL 腳本檔中以內嵌方式填入資料表。
    對於 `\copy ... to stdout`，輸出會送到與 psql 命令輸出相同的地方，而且不會印出
    `COPY count` 命令狀態（因為它可能會與資料列混淆）。
    若要不論目前的命令來源或 `\o`
    選項為何，都讀取或寫入 psql 的標準輸入或輸出，請寫成 `from pstdin` 或 `to pstdout`。

    此命令的語法與 SQL [`COPY`](../sql-commands/sql-copy.md)
    命令的語法類似。除了資料來源／目的地之外，所有選項都與 `COPY` 的規定相同。
    因此，`\copy`
    中繼命令適用特殊的剖析規則。與大多數其他中繼命令不同，該行的其餘部分一律被視為 `\copy` 的引數，
    而且引數中既不會進行變數插值，也不會進行反引號展開。

    <a id="APP-PSQL-META-COMMANDS-COPY-TIP"></a>

    ### 提示

    要得到與 `\copy
    ... to` 相同結果的另一種方式，是使用 SQL `COPY
    ... TO STDOUT` 命令，並以
    `\g filename`
    或 `\g |program` 結束它。
    與 `\copy` 不同，此方法允許命令跨越多行；此外，也可以使用變數插值與反引號展開。

    <a id="APP-PSQL-META-COMMANDS-COPY-TIP-2"></a>

    ### 提示

    這些操作的效率不如以檔案或程式作為資料來源或目的地的 SQL
    `COPY` 命令，因為所有資料都必須經過用戶端／伺服器連線。對於大量資料，使用 SQL 命令可能比較好。
<a id="APP-PSQL-META-COMMAND-COPYRIGHT"></a>

`\copyright` [#](#APP-PSQL-META-COMMAND-COPYRIGHT)
:   顯示 PostgreSQL 的著作權與散布條款。
<a id="APP-PSQL-META-COMMANDS-CROSSTABVIEW"></a>

`\crosstabview [ colV [ colH [ colD [ sortcolH ] ] ] ]` [#](#APP-PSQL-META-COMMANDS-CROSSTABVIEW)
:   執行目前的查詢緩衝區（如同 `\g`），並以交叉表格格線顯示結果。
    查詢必須傳回至少三個欄位。
    由 *`colV`* 識別的輸出欄位會成為垂直標頭，而由
    *`colH`*
    識別的輸出欄位會成為水平標頭。
    *`colD`* 識別要在格線中顯示的輸出欄位。
    *`sortcolH`* 識別水平標頭的選擇性排序欄位。

    每個欄位規格可以是欄位編號（從 1 開始）或欄位名稱。欄位名稱適用一般的 SQL 大小寫轉換與引號規則。若省略，
    *`colV`* 視為第 1 欄，
    而 *`colH`* 視為第 2 欄。
    *`colH`* 必須與
    *`colV`* 不同。
    若未指定 *`colD`*，則查詢結果中必須恰好有三個欄位，而既不是
    *`colV`* 也不是
    *`colH`*
    的那個欄位會被視為 *`colD`*。

    垂直標頭顯示為最左邊的欄位，包含在欄位 *`colV`* 中找到的值，順序與查詢結果中的順序相同，但會移除重複值。

    水平標頭顯示為第一個資料列，包含在欄位 *`colH`* 中找到的值，並移除重複值。預設情況下，這些值的出現順序與查詢結果中的順序相同。但若提供了選擇性的 *`sortcolH`* 引數，它會識別一個值必須為整數的欄位，而來自 *`colH`* 的值會依照對應的 *`sortcolH`* 值排序後顯示在水平標頭中。

    在交叉表格格線中，對於 *`colH`* 的每個相異值 `x`
    以及 *`colV`* 的每個相異值 `y`，位於交點 `(x,y)` 的儲存格包含查詢結果中，*`colH`*
    的值為 `x` 且
    *`colV`*
    的值為 `y` 的那個資料列的 `colD` 欄位值。若沒有這樣的資料列，該儲存格為空。若有多個這樣的資料列，則會回報錯誤。
<a id="APP-PSQL-META-COMMAND-D"></a>

`\d[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-D)
:   對於每個符合
    *`pattern`* 的關聯（資料表、檢視表、具體化檢視表、索引、序列或外部資料表）或複合型別，顯示其所有欄位、欄位的型別、資料表空間（若不是預設值）以及任何特殊屬性，例如 `NOT NULL` 或預設值。
    相關的索引、限制條件、規則與觸發程序也會一併顯示。對於外部資料表，也會顯示相關的外部伺服器。
    （「符合模式」的定義請參閱下方的[模式](app-psql.md#APP-PSQL-PATTERNS)。）

    對於某些種類的關聯，`\d` 會為每個欄位顯示額外資訊：序列的欄位值、索引的索引運算式，以及外部資料表的外部資料包裝器選項。

    命令形式 `\d+` 完全相同，差別在於會顯示更多資訊：會顯示與資料表欄位相關聯的任何註解、資料表中是否有 OID、若關聯是檢視表則顯示檢視表定義、非預設的
    [replica
    identity](../sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY) 設定，以及若關聯具有存取方法則顯示[存取方法](../sql-commands/sql-create-access-method.md)名稱。

    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。

    <a id="APP-PSQL-META-COMMAND-D-NOTE"></a>

    ### 注意

    若使用 `\d` 時沒有
    *`pattern`* 引數，它等同於 `\dtvmsE`，會顯示所有可見的資料表、檢視表、具體化檢視表、序列與外部資料表的清單。
    這純粹是為了方便。

    與許多其他命令一樣，若在命令名稱後附加 `x`，結果會以展開模式顯示，但請注意，這只適用於使用 `\d` 時沒有
    *`pattern`* 引數的情況，而且
    `x` 修飾字不能緊接在
    `\d` 之後（因為 `\dx` 是另一個命令）；`x` 修飾字只能出現在
    `S` 或 `+` 修飾字之後。例如，
    `\d+x` 等同於 `\dtvmsE+x`，
    會以展開模式顯示所有關聯的清單。
<a id="APP-PSQL-META-COMMAND-DA-LC"></a>

`\da[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DA-LC)
:   列出彙總函式，以及它們的傳回型別與所處理的資料型別。若指定了 *`pattern`*，
    則只顯示名稱符合該模式的彙總函式。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
<a id="APP-PSQL-META-COMMAND-DA-UC"></a>

`\dA[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DA-UC)
:   列出存取方法。若指定了 *`pattern`*，則只顯示名稱符合該模式的存取方法。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個存取方法都會連同其相關聯的處理函式與描述一起列出。
<a id="APP-PSQL-META-COMMAND-DAC"></a>

`\dAc[x+] [access-method-pattern [input-type-pattern]]` [#](#APP-PSQL-META-COMMAND-DAC)
:   列出運算子類別
    （請參閱[第 36.16.1 節](../../server-programming/extend/xindex.md#xindex-opclass)）。
    若指定了 *`access-method-pattern`*，
    則只列出與名稱符合該模式之存取方法相關聯的運算子類別。
    若指定了 *`input-type-pattern`*，
    則只列出與名稱符合該模式之輸入型別相關聯的運算子類別。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個運算子類別都會連同其相關聯的運算子家族與擁有者一起列出。
<a id="APP-PSQL-META-COMMAND-DAF"></a>

`\dAf[x+] [access-method-pattern [input-type-pattern]]` [#](#APP-PSQL-META-COMMAND-DAF)
:   列出運算子家族
    （請參閱[第 36.16.5 節](../../server-programming/extend/xindex.md#xindex-opfamily)）。
    若指定了 *`access-method-pattern`*，
    則只列出與名稱符合該模式之存取方法相關聯的運算子家族。
    若指定了 *`input-type-pattern`*，
    則只列出與名稱符合該模式之輸入型別相關聯的運算子家族。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個運算子家族都會連同其擁有者一起列出。
<a id="APP-PSQL-META-COMMAND-DAO"></a>

`\dAo[x+] [access-method-pattern [operator-family-pattern]]` [#](#APP-PSQL-META-COMMAND-DAO)
:   列出與運算子家族相關聯的運算子
    （請參閱[第 36.16.2 節](../../server-programming/extend/xindex.md#xindex-strategies)）。
    若指定了 *`access-method-pattern`*，
    則只列出與名稱符合該模式之存取方法相關聯的運算子家族成員。
    若指定了 *`operator-family-pattern`*，
    則只列出名稱符合該模式之運算子家族的成員。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個運算子都會連同其排序運算子家族（若它是排序用運算子）一起列出，並顯示其底層函式是否為 leakproof。
<a id="APP-PSQL-META-COMMAND-DAP"></a>

`\dAp[x+] [access-method-pattern [operator-family-pattern]]` [#](#APP-PSQL-META-COMMAND-DAP)
:   列出與運算子家族相關聯的支援函式
    （請參閱[第 36.16.3 節](../../server-programming/extend/xindex.md#xindex-support)）。
    若指定了 *`access-method-pattern`*，
    則只列出與名稱符合該模式之存取方法相關聯的運算子家族的函式。
    若指定了 *`operator-family-pattern`*，
    則只列出名稱符合該模式之運算子家族的函式。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會詳細顯示函式，包括其實際的參數列表。
<a id="APP-PSQL-META-COMMAND-DB"></a>

`\db[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DB)
:   列出資料表空間。若指定了 *`pattern`*，
    則只顯示名稱符合該模式的資料表空間。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個資料表空間都會連同其相關聯的選項、磁碟上的大小、權限與描述一起列出。
<a id="APP-PSQL-META-COMMAND-DC-LC"></a>

`\dc[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DC-LC)
:   列出字元集編碼之間的轉換。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的轉換。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個物件都會連同其相關聯的描述一起列出。
<a id="APP-PSQL-META-COMMAND-DCONFIG"></a>

`\dconfig[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DCONFIG)
:   列出伺服器組態參數及其值。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的參數。若沒有
    *`pattern`*，則只列出被設為非預設值的參數。
    （使用 `\dconfig *` 可查看所有參數。）
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個參數都會連同其資料型別、可設定該參數的情境，以及存取權限（若已授予非預設的存取權限）一起列出。
<a id="APP-PSQL-META-COMMAND-DC-UC"></a>

`\dC[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DC-UC)
:   列出型別轉換。
    若指定了 *`pattern`*，
    則只列出來源型別或目標型別符合該模式的型別轉換。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個型別轉換的額外資訊，包括其底層函式是否為 leakproof，以及該型別轉換的描述。
<a id="APP-PSQL-META-COMMAND-DD-LC"></a>

`\dd[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DD-LC)
:   顯示型別為 `constraint`、
    `operator class`、`operator family`、
    `rule` 與 `trigger` 之物件的描述。所有其他註解可以透過這些物件型別各自的反斜線命令查看。

    `\dd` 會顯示符合
    *`pattern`* 之物件的描述；若未提供引數，則顯示適當型別之可見物件的描述。但無論哪種情況，都只會列出有描述的物件。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。

    物件的描述可以用 [`COMMENT`](../sql-commands/sql-comment.md)
    SQL 命令建立。
<a id="APP-PSQL-META-COMMAND-DD-UC"></a>

`\dD[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DD-UC)
:   列出網域。若指定了 *`pattern`*，
    則只顯示名稱符合該模式的網域。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個物件都會連同其相關聯的權限與描述一起列出。
<a id="APP-PSQL-META-COMMAND-DDP"></a>

`\ddp[x] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DDP)
:   列出預設存取權限設定。對於每個預設權限設定已從內建預設值變更過的角色（以及綱要，若適用的話），都會顯示一個項目。
    若指定了 *`pattern`*，
    則只列出角色名稱或綱要名稱符合該模式的項目。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。

    [`ALTER DEFAULT
    PRIVILEGES`](../sql-commands/sql-alterdefaultprivileges.md) 命令用來設定預設存取權限。權限顯示的意義說明於
    [第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。
<a id="APP-PSQL-META-COMMAND-DE"></a>

`\dE[Sx+] [ pattern ]`<br>`\di[Sx+] [ pattern ]`<br>`\dm[Sx+] [ pattern ]`<br>`\ds[Sx+] [ pattern ]`<br>`\dt[Sx+] [ pattern ]`<br>`\dv[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DE)
:   在這組命令中，字母 `E`、
    `i`、`m`、`s`、
    `t` 與 `v`
    分別代表外部資料表、索引、具體化檢視表、序列、資料表與檢視表。
    你可以以任意順序指定這些字母中的任意幾個或全部，以取得這些型別之物件的清單。例如，`\dti` 會列出資料表與索引。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個物件都會連同其持久性狀態（永久、暫時或 unlogged）、在磁碟上的實體大小，以及相關聯的描述（若有的話）一起列出。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的物件。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
<a id="APP-PSQL-META-COMMAND-DES"></a>

`\des[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DES)
:   列出外部伺服器（助記：「external
    servers」）。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的伺服器。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個伺服器的完整描述，包括伺服器的存取權限、型別、版本、選項與描述。
<a id="APP-PSQL-META-COMMAND-DET"></a>

`\det[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DET)
:   列出外部資料表（助記：「external tables」）。
    若指定了 *`pattern`*，
    則只列出資料表名稱或綱要名稱符合該模式的項目。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則也會顯示通用選項與外部資料表的描述。
<a id="APP-PSQL-META-COMMAND-DEU"></a>

`\deu[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DEU)
:   列出使用者對應（助記：「external
    users」）。
    若指定了 *`pattern`*，
    則只列出使用者名稱符合該模式的對應。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個對應的額外資訊。

    <a id="APP-PSQL-META-COMMAND-DEU-CAUTION"></a>

    ### 小心

    `\deu+` 也可能會顯示遠端使用者的使用者名稱與密碼，因此應小心不要洩露它們。

<a id="APP-PSQL-META-COMMAND-DEW"></a>

`\dew[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DEW)
:   列出外部資料包裝器（助記：「external
    wrappers」）。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的外部資料包裝器。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則也會顯示外部資料包裝器的存取權限、選項與描述。
<a id="APP-PSQL-META-COMMAND-DF-LC"></a>

`\df[anptwSx+] [ pattern [ arg_pattern ... ] ]` [#](#APP-PSQL-META-COMMAND-DF-LC)
:   列出函式，以及它們的結果資料型別、引數資料型別與函式類型；函式類型分為「agg」（彙總）、「normal」、「procedure」、「trigger」或「window」。
    若只要顯示特定類型的函式，請在命令後加上對應的字母 `a`、
    `n`、`p`、`t` 或 `w`。
    若指定了 *`pattern`*，則只顯示名稱符合該模式的函式。
    任何額外的引數都是型別名稱模式，會依序比對函式第一個、第二個等引數的型別名稱。（符合的函式可以擁有比你所指定的更多的引數。若要避免這種情況，請在最後一個 *`arg_pattern`* 寫上破折號 `-`。）
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S`
    修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個函式的額外資訊，包括易變性、平行安全性、擁有者、安全性分類、是否為 leakproof、存取權限、語言、內部名稱（僅限 C 函式與內部函式）以及描述。
    特定函式的原始碼可以使用 `\sf` 查看。
<a id="APP-PSQL-META-COMMAND-DF-UC"></a>

`\dF[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DF-UC)
:   列出文字搜尋設定。
    若指定了 *`pattern`*，
    則只顯示名稱符合該模式的設定。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個設定的完整描述，包括底層的文字搜尋剖析器，以及每種剖析器 token 類型的字典清單。
<a id="APP-PSQL-META-COMMAND-DFD"></a>

`\dFd[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFD)
:   列出文字搜尋字典。
    若指定了 *`pattern`*，
    則只顯示名稱符合該模式的字典。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個所選字典的額外資訊，包括底層的文字搜尋範本與選項值。
<a id="APP-PSQL-META-COMMAND-DFP"></a>

`\dFp[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFP)
:   列出文字搜尋剖析器。
    若指定了 *`pattern`*，
    則只顯示名稱符合該模式的剖析器。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個剖析器的完整描述，包括底層的函式與可辨識的 token 類型清單。
<a id="APP-PSQL-META-COMMAND-DFT"></a>

`\dFt[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFT)
:   列出文字搜尋範本。
    若指定了 *`pattern`*，
    則只顯示名稱符合該模式的範本。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個範本的額外資訊，包括底層的函式名稱。
<a id="APP-PSQL-META-COMMAND-DG"></a>

`\dg[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DG)
:   列出資料庫角色。
    （由於「使用者」與「群組」的概念已統一為「角色」，此命令現在等同於
    `\du`。）
    預設情況下，只會顯示使用者建立的角色；若要包含系統角色，請提供
    `S` 修飾字。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的角色。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個角色的額外資訊；目前這會加上每個角色的註解。
<a id="APP-PSQL-META-COMMAND-DL-LC"></a>

`\dl[x+]` [#](#APP-PSQL-META-COMMAND-DL-LC)
:   這是 `\lo_list` 的別名，會顯示大型物件的清單。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個大型物件都會連同其相關聯的權限（若有的話）一起列出。
<a id="APP-PSQL-META-COMMAND-DL-UC"></a>

`\dL[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DL-UC)
:   列出程序語言。若指定了 *`pattern`*，
    則只列出名稱符合該模式的語言。
    預設情況下，只會顯示使用者建立的語言；若要包含系統物件，請提供 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個語言都會連同其呼叫處理函式、驗證函式、存取權限，以及它是否為系統物件一起列出。
<a id="APP-PSQL-META-COMMAND-DN"></a>

`\dn[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DN)
:   列出綱要（命名空間）。若指定了 *`pattern`*，
    則只列出名稱符合該模式的綱要。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個物件都會連同其相關聯的權限與描述（若有的話）一起列出。
<a id="APP-PSQL-META-COMMAND-DO-LC"></a>

`\do[Sx+] [ pattern [ arg_pattern [ arg_pattern ] ] ]` [#](#APP-PSQL-META-COMMAND-DO-LC)
:   列出運算子，以及它們的運算元型別與結果型別。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的運算子。
    若指定了一個 *`arg_pattern`*，
    則只列出右側引數的型別名稱符合該模式的前置運算子。
    若指定了兩個 *`arg_pattern`*，
    則只列出引數型別名稱符合這些模式的二元運算子。（或者，也可以為一元運算子未使用的引數寫上 `-`。）
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個運算子的額外資訊，包括底層函式的名稱，以及它是否為 leakproof。
<a id="APP-PSQL-META-COMMAND-DO-UC"></a>

`\dO[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DO-UC)
:   列出定序。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的定序。預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個定序都會連同其相關聯的描述（若有的話）一起列出。
    請注意，只會顯示可用於目前資料庫編碼的定序，因此在同一個安裝中的不同資料庫，結果可能會不同。
<a id="APP-PSQL-META-COMMAND-DP-LC"></a>

`\dp[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DP-LC)
:   列出資料表、檢視表與序列，以及它們相關聯的存取權限。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的資料表、檢視表與序列。預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。

    [`GRANT`](../sql-commands/sql-grant.md) 與
    [`REVOKE`](../sql-commands/sql-revoke.md)
    命令用來設定存取權限。權限顯示的意義說明於
    [第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。
<a id="APP-PSQL-META-COMMAND-DP-UC"></a>

`\dP[itnx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DP-UC)

列出分割關聯。
若指定了 *`pattern`*，
則只列出名稱符合該模式的項目。
可以在命令後附加修飾字 `t`（資料表）與 `i`
（索引），以篩選要列出的關聯種類。預設情況下，會列出分割資料表與分割索引。

若使用修飾字 `n`（「nested」），或指定了模式，則會包含非根層級的分割關聯，並顯示一個欄位，呈現每個分割關聯的父關聯。

若在命令名稱後附加 `x`，結果會以展開模式顯示。
若在命令名稱後附加 `+`，則也會顯示每個關聯之分割區大小的總和，以及該關聯的描述。
若 `n` 與 `+` 組合使用，則會顯示兩種大小：一種是直接附加之葉分割區的總大小，另一種是所有分割區（包括間接附加的子分割區）的總大小。
<a id="APP-PSQL-META-COMMAND-DRDS"></a>

`\drds[x] [ role-pattern [ database-pattern ] ]` [#](#APP-PSQL-META-COMMAND-DRDS)
:   列出已定義的組態設定。這些設定可以是角色專屬、資料庫專屬，或兩者皆是。
    *`role-pattern`* 與
    *`database-pattern`* 分別用來選擇要列出的特定角色與資料庫。若省略，或指定了
    `*`，則會列出所有設定，包括分別不屬於特定角色或特定資料庫的設定。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。

    [`ALTER ROLE`](../sql-commands/sql-alterrole.md) 與
    [`ALTER DATABASE`](../sql-commands/sql-alterdatabase.md)
    命令用來定義各角色與各資料庫的組態設定。

<a id="APP-PSQL-META-COMMAND-DRG"></a>

`\drg[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRG)

列出每個已授予之角色成員資格的資訊，包括所指派的選項（`ADMIN`、
`INHERIT` 和／或 `SET`）以及授予者。
關於角色成員資格的資訊，請參閱 [`GRANT`](../sql-commands/sql-grant.md)
命令。

預設情況下，只會顯示授予使用者建立之角色的成員資格；若要包含系統角色，請提供
`S` 修飾字。
若指定了 *`pattern`*，
則只列出授予名稱符合該模式之角色的成員資格。
若在命令名稱後附加 `x`，結果會以展開模式顯示。
<a id="APP-PSQL-META-COMMAND-DRP"></a>

`\dRp[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRP)
:   列出複寫發布。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的發布。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則也會顯示與每個發布相關聯的資料表與綱要。
<a id="APP-PSQL-META-COMMAND-DRS"></a>

`\dRs[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRS)
:   列出複寫訂閱。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的訂閱。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示訂閱的額外屬性。
<a id="APP-PSQL-META-COMMAND-DT"></a>

`\dT[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DT)
:   列出資料型別。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的型別。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個型別都會連同其內部名稱與大小、允許的值（若它是 `enum` 型別），以及其相關聯的權限一起列出。
    預設情況下，只會顯示使用者建立的物件；若要包含系統物件，請提供模式或 `S` 修飾字。
<a id="APP-PSQL-META-COMMAND-DU"></a>

`\du[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DU)
:   列出資料庫角色。
    （由於「使用者」與「群組」的概念已統一為「角色」，此命令現在等同於
    `\dg`。）
    預設情況下，只會顯示使用者建立的角色；若要包含系統角色，請提供
    `S` 修飾字。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的角色。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會顯示每個角色的額外資訊；目前這會加上每個角色的註解。
<a id="APP-PSQL-META-COMMAND-DX-LC"></a>

`\dx[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DX-LC)
:   列出已安裝的擴充功能。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的擴充功能。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則會列出屬於每個符合之擴充功能的所有物件。
<a id="APP-PSQL-META-COMMAND-DX-UC"></a>

`\dX[x] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DX-UC)

列出擴充統計資訊。
若指定了 *`pattern`*，
則只列出名稱符合該模式的擴充統計資訊。
若在命令名稱後附加 `x`，結果會以展開模式顯示。

每一種擴充統計資訊的狀態，會顯示在以其統計種類命名的欄位中（例如 Ndistinct）。
`defined` 表示建立統計資訊時有要求此種類，而 NULL 表示未要求。
若你想知道是否已執行 [`ANALYZE`](../sql-commands/sql-analyze.md)
且統計資訊可供規劃器使用，可以使用 `pg_stats_ext`。
<a id="APP-PSQL-META-COMMAND-DY"></a>

`\dy[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DY)
:   列出事件觸發程序。
    若指定了 *`pattern`*，
    則只列出名稱符合該模式的事件觸發程序。
    若在命令名稱後附加 `x`，結果會以展開模式顯示。
    若在命令名稱後附加 `+`，則每個物件都會連同其相關聯的描述一起列出。
<a id="APP-PSQL-META-COMMAND-EDIT"></a>

`\e` 或 `\edit` `[ filename ] [ line_number ]` [#](#APP-PSQL-META-COMMAND-EDIT)
:   若指定了 *`filename`*，
    則會編輯該檔案；編輯器結束後，檔案的內容會複製到目前的查詢緩衝區中。若未提供 *`filename`*，則會將目前的查詢緩衝區複製到暫存檔，然後以相同方式編輯。或者，若目前的查詢緩衝區是空的，則會將最近執行的查詢複製到暫存檔，並以相同方式編輯。

    若你編輯的是檔案或前一個查詢，並且在未修改檔案的情況下結束編輯器，查詢緩衝區會被清除。
    否則，查詢緩衝區的新內容會依照 psql 的一般規則重新剖析，並將整個緩衝區視為單一行。任何完整的查詢都會立即執行；也就是說，若查詢緩衝區包含分號或以分號結尾，則到該處為止的所有內容都會被執行並從查詢緩衝區中移除。查詢緩衝區中剩下的內容會重新顯示。輸入分號或 `\g` 以送出它，
    或輸入 `\r` 以清除查詢緩衝區來取消它。

    將緩衝區視為單一行主要會影響中繼命令：緩衝區中位於中繼命令之後的任何內容，都會被視為該中繼命令的引數，即使它跨越多行也一樣。
    （因此，你無法以這種方式製作使用中繼命令的腳本。
    這種情況請使用 `\i`。）

    若指定了行號，psql 會將游標定位在檔案或查詢緩衝區的指定行。
    請注意，若只提供了一個全為數字的引數，
    psql 會假設它是行號，而不是檔案名稱。

    <a id="APP-PSQL-META-COMMAND-EDIT-TIP"></a>

    ### 提示

    關於如何設定與自訂你的編輯器，請參閱下方的[環境](app-psql.md#APP-PSQL-ENVIRONMENT)。
<a id="APP-PSQL-META-COMMAND-ECHO"></a>

`\echo text [ ... ]` [#](#APP-PSQL-META-COMMAND-ECHO)

將求值後的引數印到標準輸出，引數之間以空格分隔，最後接著換行字元。這可用於在腳本的輸出中穿插資訊。例如：

```

    => \echo `date`
    Tue Oct 26 21:40:57 CEST 1999
```

若第一個引數是未加引號的 `-n`，則不會寫出結尾的換行字元（也不會寫出第一個引數）。

<a id="APP-PSQL-META-COMMAND-ECHO-TIP"></a>

### 提示 [#](#psql-echo-tip) <a href="#psql-echo-tip" id="psql-echo-tip"></a>

若你使用 `\o` 命令重新導向查詢輸出，你可能會想改用 `\qecho`
而不是此命令。另請參閱 `\warn`。
<a id="APP-PSQL-META-COMMAND-EF"></a>

`\ef [ function_description [ line_number ] ]` [#](#APP-PSQL-META-COMMAND-EF)
:   此命令會擷取並編輯指定函式或程序的定義，形式為 `CREATE OR REPLACE FUNCTION` 或
    `CREATE OR REPLACE PROCEDURE` 命令。
    編輯方式與 `\edit` 相同。
    若你未儲存就結束編輯器，該陳述式會被捨棄。
    若你儲存後結束編輯器，而且你在更新後的命令中加上了分號，它就會立即執行。否則它會重新顯示；
    輸入分號或 `\g` 以送出它，或輸入 `\r`
    以取消。

    目標函式可以只以名稱指定，也可以以名稱與引數指定，例如 `foo(integer, text)`。
    若有超過一個同名函式，則必須提供引數型別。

    若未指定函式，則會呈現一個空白的 `CREATE FUNCTION`
    範本供你編輯。

    若指定了行號，psql 會將游標定位在函式主體的指定行。
    （請注意，函式主體通常不是從檔案的第一行開始。）

    與大多數其他中繼命令不同，該行的其餘部分一律被視為 `\ef` 的引數，而且引數中既不會進行變數插值，也不會進行反引號展開。

    <a id="APP-PSQL-META-COMMAND-EF-TIP"></a>

    ### 提示

    關於如何設定與自訂你的編輯器，請參閱下方的[環境](app-psql.md#APP-PSQL-ENVIRONMENT)。
<a id="APP-PSQL-META-COMMAND-ENCODING"></a>

`\encoding [ encoding ]` [#](#APP-PSQL-META-COMMAND-ENCODING)
:   設定用戶端字元集編碼。若沒有引數，此命令會顯示目前的編碼。
<a id="APP-PSQL-META-COMMAND-ERRVERBOSE"></a>

`\errverbose` [#](#APP-PSQL-META-COMMAND-ERRVERBOSE)
:   以最詳細的程度重複顯示最近一次的伺服器錯誤訊息，就如同 `VERBOSITY` 被設為
    `verbose`，且 `SHOW_CONTEXT` 被設為 `always` 一樣。
<a id="APP-PSQL-META-COMMAND-EV"></a>

`\ev [ view_name [ line_number ] ]` [#](#APP-PSQL-META-COMMAND-EV)

此命令會擷取並編輯指定檢視表的定義，形式為 `CREATE OR REPLACE VIEW` 命令。
編輯方式與 `\edit` 相同。
若你未儲存就結束編輯器，該陳述式會被捨棄。
若你儲存後結束編輯器，而且你在更新後的命令中加上了分號，它就會立即執行。否則它會重新顯示；
輸入分號或 `\g` 以送出它，或輸入 `\r`
以取消。

若未指定檢視表，則會呈現一個空白的 `CREATE VIEW`
範本供你編輯。

若指定了行號，psql 會將游標定位在檢視表定義的指定行。

與大多數其他中繼命令不同，該行的其餘部分一律被視為 `\ev` 的引數，而且引數中既不會進行變數插值，也不會進行反引號展開。
<a id="APP-PSQL-META-COMMAND-F"></a>

`\f [ string ]` [#](#APP-PSQL-META-COMMAND-F)
:   設定非對齊查詢輸出的欄位分隔字元。預設為垂直線（`|`）。它等同於 `\pset fieldsep`。
<a id="APP-PSQL-META-COMMAND-G"></a>

`\g [ (option=value [...]) ] [ filename ]`<br>`\g [ (option=value [...]) ] [ |command ]` [#](#APP-PSQL-META-COMMAND-G)

將目前的查詢緩衝區送到伺服器執行。

若 `\g` 之後出現括號，括號內是以空白分隔的 *`option`*`=`*`value`* 格式選項子句清單，其解讀方式與 `\pset` *`option`* *`value`* 命令相同，但只在這次查詢期間生效。在此清單中，`=` 符號兩側不允許有空白，但選項子句之間必須以空白分隔。若省略 `=`*`value`*，則所指定的 *`option`* 會以與不指定 *`value`* 的 `\pset` *`option`* 相同的方式變更。

若給定 *`filename`* 或 `|`*`command`* 引數，查詢的輸出會寫入指定的檔案，或以管線傳給指定的 shell 命令，而不是如平常一樣顯示出來。只有在查詢成功傳回零筆或更多筆資料列時，才會寫入該檔案或命令；查詢失敗或屬於不傳回資料的 SQL 命令時則不會寫入。

若目前的查詢緩衝區是空的，則改為重新執行最近一次送出的查詢。除了這個行為之外，不帶任何引數的 `\g` 基本上等同於分號。帶引數時，`\g` 提供了 `\o` 命令的「一次性」替代方式，並且還允許一次性地調整平常由 `\pset` 設定的輸出格式選項。

若最後一個引數以 `|` 開頭，該行的其餘部分全部會被當成要執行的 *`command`*，而且其中既不進行變數插值，也不進行反引號展開。該行的其餘部分只是原封不動地傳給 shell。
<a id="APP-PSQL-META-COMMAND-GDESC"></a>

`\gdesc` [#](#APP-PSQL-META-COMMAND-GDESC)

顯示目前查詢緩衝區之結果的描述（也就是欄位名稱與資料型別）。查詢並不會真正執行；不過，若其中含有某種語法錯誤，該錯誤會以一般方式回報。

若目前的查詢緩衝區是空的，則改為描述最近一次送出的查詢。
<a id="APP-PSQL-META-COMMAND-GETENV"></a>

`\getenv psql_var env_var` [#](#APP-PSQL-META-COMMAND-GETENV)

取得環境變數 *`env_var`* 的值，並指派給 psql 變數 *`psql_var`*。若 *`env_var`* 未定義於 psql 程序的環境中，*`psql_var`* 不會被變更。範例：

```

    => \getenv home HOME
    => \echo :home
    /home/postgres
```
<a id="APP-PSQL-META-COMMAND-GEXEC"></a>

`\gexec` [#](#APP-PSQL-META-COMMAND-GEXEC)

將目前的查詢緩衝區送到伺服器，然後把查詢輸出（若有）中每一筆資料列的每一個欄位都當成要執行的 SQL 陳述式。例如，要在 `my_table` 的每個欄位上建立索引：

```

    => SELECT format('create index on my_table(%I)', attname)
    -> FROM pg_attribute
    -> WHERE attrelid = 'my_table'::regclass AND attnum > 0
    -> ORDER BY attnum
    -> \gexec
    CREATE INDEX
    CREATE INDEX
    CREATE INDEX
    CREATE INDEX
```

產生的查詢會依資料列傳回的順序執行；若有超過一個欄位，則在每筆資料列內由左至右執行。NULL 欄位會被忽略。產生的查詢會原封不動地送到伺服器處理，因此它們不能是 psql 中繼命令，也不能包含 psql 變數參照。若其中任何一個查詢失敗，除非設定了 `ON_ERROR_STOP`，否則其餘查詢會繼續執行。每個查詢的執行都受 `ECHO` 處理的影響。（使用 `\gexec` 時，通常建議將 `ECHO` 設為 `all` 或 `queries`。）查詢記錄、單步模式、計時以及其他查詢執行功能，也同樣適用於每一個產生的查詢。

若目前的查詢緩衝區是空的，則改為重新執行最近一次送出的查詢。
<a id="APP-PSQL-META-COMMAND-GSET"></a>

`\gset [ prefix ]` [#](#APP-PSQL-META-COMMAND-GSET)

將目前的查詢緩衝區送到伺服器，並把查詢的輸出存入 psql 變數（請參閱下方的[變數](app-psql.md#APP-PSQL-VARIABLES)）。要執行的查詢必須恰好傳回一筆資料列。該資料列的每個欄位會分別存入一個獨立的變數，變數名稱與欄位名稱相同。例如：

```

    => SELECT 'hello' AS var1, 10 AS var2
    -> \gset
    => \echo :var1 :var2
    hello 10
```

若你指定了 *`prefix`*，該字串會加在查詢的欄位名稱前面，作為要使用的變數名稱：

```

    => SELECT 'hello' AS var1, 10 AS var2
    -> \gset result_
    => \echo :result_var1 :result_var2
    hello 10
```

若某個欄位結果為 NULL，對應的變數會被取消設定，而不是被設定。

若查詢失敗或沒有傳回一筆資料列，則不會變更任何變數。

若目前的查詢緩衝區是空的，則改為重新執行最近一次送出的查詢。
<a id="APP-PSQL-META-COMMAND-GX"></a>

`\gx [ (option=value [...]) ] [ filename ]`<br>`\gx [ (option=value [...]) ] [ |command ]` [#](#APP-PSQL-META-COMMAND-GX)
:   `\gx` 等同於 `\g`，差別在於它會對這次查詢強制使用擴展輸出模式，如同在 `\pset` 選項清單中加入了 `expanded=on`。另請參閱 `\x`。
<a id="APP-PSQL-META-COMMAND-HELP"></a>

`\h` 或 `\help` `[ command ]` [#](#APP-PSQL-META-COMMAND-HELP)
:   提供指定 SQL 命令的語法說明。若未指定 *`command`*，psql 會列出所有提供語法說明的命令。若 *`command`* 是星號（`*`），則顯示所有 SQL 命令的語法說明。

    與其他大多數中繼命令不同，該行的其餘部分一律會被當成 `\help` 的引數，而且引數中既不進行變數插值，也不進行反引號展開。

    <a id="APP-PSQL-META-COMMAND-HELP-NOTE"></a>

    ### 注意

    為了簡化輸入，由多個單字組成的命令不必加上引號。因此輸入 **`\help
    alter table`** 是可以的。
<a id="APP-PSQL-META-COMMAND-HTML"></a>

`\H` 或 `\html` [#](#APP-PSQL-META-COMMAND-HTML)
:   開啟 HTML 查詢輸出格式。若 HTML 格式已經開啟，則切換回預設的對齊文字格式。此命令是為了相容性與方便而提供，但設定其他輸出選項請參閱 `\pset`。
<a id="APP-PSQL-META-COMMAND-INCLUDE"></a>

`\i` 或 `\include` *`filename`* [#](#APP-PSQL-META-COMMAND-INCLUDE)
:   從檔案 *`filename`* 讀取輸入並執行，如同這些內容是從鍵盤輸入的一樣。

    若 *`filename`* 是 `-`（連字號），則會讀取標準輸入，直到遇到 EOF 指示或 `\q` 中繼命令為止。這可用來將互動式輸入與檔案輸入穿插使用。請注意，只有在最外層啟用 Readline 時，才會使用 Readline 的行為。

    <a id="APP-PSQL-META-COMMAND-INCLUDE-NOTE"></a>

    ### 注意

    若你想在讀取各行時於螢幕上看到它們，必須將變數 `ECHO` 設為 `all`。
<a id="PSQL-METACOMMAND-IF"></a>

`\if` *`expression`*<br>`\elif` *`expression`*<br>`\else`<br>`\endif` [#](#PSQL-METACOMMAND-IF)

這組命令實作可巢狀的條件區塊。條件區塊必須以 `\if` 開始，並以 `\endif` 結束。兩者之間可以有任意數量的 `\elif` 子句，其後可以選擇性地接一個 `\else` 子句。一般查詢與其他類型的反斜線命令可以（而且通常會）出現在構成條件區塊的命令之間。

`\if` 與 `\elif` 命令會讀取其引數，並將其當作布林運算式求值。若運算式得出 `true`，處理會正常繼續；否則會略過後續各行，直到遇到相對應的 `\elif`、`\else` 或 `\endif` 為止。一旦某個 `\if` 或 `\elif` 測試成功，同一區塊中後續 `\elif` 命令的引數就不會求值，而是視為 false。只有在先前相對應的 `\if` 或 `\elif` 都沒有成功時，才會處理 `\else` 之後的各行。

`\if` 或 `\elif` 命令的 *`expression`* 引數，與任何其他反斜線命令的引數一樣，會進行變數插值與反引號展開。之後，它會像 on/off 選項變數的值一樣被求值。因此，有效的值是與下列任一者不分大小寫且不產生歧義的相符字串：`true`、`false`、`1`、`0`、`on`、`off`、`yes`、`no`。例如，`t`、`T` 與 `tR` 都會被視為 `true`。

無法正確求值為 true 或 false 的運算式會產生警告，並被視為 false。

被略過的各行仍會正常剖析，以辨識查詢與反斜線命令，但查詢不會送到伺服器，而條件命令（`\if`、`\elif`、`\else`、`\endif`）以外的反斜線命令都會被忽略。對條件命令只檢查巢狀結構是否有效。被略過的各行中的變數參照不會展開，也不會進行反引號展開。

同一個條件區塊的所有反斜線命令都必須出現在同一個來源檔案中。若在所有區域的 `\if` 區塊關閉之前，就到達主輸入檔或某個以 `\include` 引入之檔案的 EOF，psql 會引發錯誤。

以下是一個範例：

```

    -- check for the existence of two separate records in the database and store
    -- the results in separate psql variables
    SELECT
        EXISTS(SELECT 1 FROM customer WHERE customer_id = 123) as is_customer,
        EXISTS(SELECT 1 FROM employee WHERE employee_id = 456) as is_employee
    \gset
    \if :is_customer
        SELECT * FROM customer WHERE customer_id = 123;
    \elif :is_employee
        \echo 'is not a customer but is an employee'
        SELECT * FROM employee WHERE employee_id = 456;
    \else
        \if yes
            \echo 'not a customer or employee'
        \else
            \echo 'this will never print'
        \endif
    \endif
```
<a id="APP-PSQL-META-COMMAND-INCLUDE-RELATIVE"></a>

`\ir` 或 `\include_relative` *`filename`* [#](#APP-PSQL-META-COMMAND-INCLUDE-RELATIVE)
:   `\ir` 命令與 `\i` 類似，但解析相對檔名的方式不同。在互動模式下執行時，這兩個命令的行為完全相同。然而，從腳本中呼叫時，`\ir` 會以腳本所在的目錄為基準解讀檔名，而不是以目前的工作目錄為基準。
<a id="APP-PSQL-META-COMMAND-LIST"></a>

`\l[x+]` 或 `\list[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-LIST)
:   列出伺服器中的資料庫，並顯示其名稱、擁有者、字元集編碼與存取權限。若指定了 *`pattern`*，只會列出名稱符合該模式的資料庫。若在命令名稱後加上 `x`，結果會以展開模式顯示。若在命令名稱後加上 `+`，還會顯示資料庫大小、預設資料表空間與描述。只有在目前使用者對該資料庫具有 `CONNECT` 權限，或目前使用者是超級使用者或具有 `pg_read_all_stats` 角色的權限時，才能取得該資料庫的大小資訊。
<a id="APP-PSQL-META-COMMAND-LO-EXPORT"></a>

`\lo_export loid filename` [#](#APP-PSQL-META-COMMAND-LO-EXPORT)
:   從資料庫讀取 OID 為 *`loid`* 的大型物件，並寫入 *`filename`*。請注意，這與伺服器函式 `lo_export` 有細微的差異；後者是以資料庫伺服器執行身分之使用者的權限，在伺服器的檔案系統上運作。

    <a id="APP-PSQL-META-COMMAND-LO-EXPORT-TIP"></a>

    ### 提示

    使用 `\lo_list` 查出大型物件的 OID。
<a id="APP-PSQL-META-COMMAND-LO-IMPORT"></a>

`\lo_import filename [ comment ]` [#](#APP-PSQL-META-COMMAND-LO-IMPORT)

將檔案存成 PostgreSQL 大型物件。也可以選擇為該物件附上指定的註解。範例：

```

    foo=> \lo_import '/home/peter/pictures/photo.xcf' 'a picture of me'
    lo_import 152801
```

此回應表示該大型物件取得了物件 ID 152801，日後可用它來存取這個新建立的大型物件。為了可讀性，建議一律為每個物件附上人類可讀的註解。OID 與註解都可以用 `\lo_list` 命令檢視。

請注意，此命令與伺服器端的 `lo_import` 有細微的差異，因為它是以本機使用者的身分在本機檔案系統上運作，而不是以伺服器的使用者身分與檔案系統運作。
<a id="APP-PSQL-META-COMMAND-LO-LIST"></a>

`\lo_list[x+]` [#](#APP-PSQL-META-COMMAND-LO-LIST)
:   顯示目前儲存在資料庫中的所有 PostgreSQL 大型物件清單，以及為它們提供的任何註解。若在命令名稱後加上 `x`，結果會以展開模式顯示。若在命令名稱後加上 `+`，每個大型物件會連同其相關權限（若有）一併列出。
<a id="APP-PSQL-META-COMMAND-LO-UNLINK"></a>

`\lo_unlink loid` [#](#APP-PSQL-META-COMMAND-LO-UNLINK)
:   從資料庫刪除 OID 為 *`loid`* 的大型物件。

    <a id="APP-PSQL-META-COMMAND-LO-UNLINK-TIP"></a>

    ### 提示

    使用 `\lo_list` 查出大型物件的 OID。
<a id="APP-PSQL-META-COMMAND-OUT"></a>

`\o` 或 `\out [ filename ]`<br>`\o` 或 `\out [ |command ]` [#](#APP-PSQL-META-COMMAND-OUT)
:   安排將之後的查詢結果存入檔案 *`filename`*，或將之後的結果以管線傳給 shell 命令 *`command`*。若未指定引數，查詢輸出會重設為標準輸出。

    若引數以 `|` 開頭，該行的其餘部分全部會被當成要執行的 *`command`*，而且其中既不進行變數插值，也不進行反引號展開。該行的其餘部分只是原封不動地傳給 shell。

    「查詢結果」包括從資料庫伺服器取得的所有資料表、命令回應與通知（notice），以及查詢資料庫的各種反斜線命令（例如 `\d`）的輸出；但不包括錯誤訊息。

    <a id="APP-PSQL-META-COMMAND-OUT-TIP"></a>

    ### 提示

    若要在查詢結果之間穿插文字輸出，請使用 `\qecho`。
<a id="APP-PSQL-META-COMMAND-PRINT"></a>

`\p` 或 `\print` [#](#APP-PSQL-META-COMMAND-PRINT)
:   將目前的查詢緩衝區印到標準輸出。若目前的查詢緩衝區是空的，則改為印出最近一次執行的查詢。
<a id="APP-PSQL-META-COMMAND-PARSE"></a>

`\parse statement_name` [#](#APP-PSQL-META-COMMAND-PARSE)

依據目標預備陳述式物件的名稱，從目前的查詢緩衝區建立一個預備陳述式。空字串表示未命名的預備陳述式。

範例：

```

    SELECT $1 \parse stmt1
```

與一般 psql 運作使用簡單查詢協定不同，此命令會使用延伸查詢協定。此命令會發出一個 [Parse (F)](../../internals/protocol/protocol-message-formats.md#PROTOCOL-MESSAGE-FORMATS-PARSE) 訊息，因此可用來從 psql 測試延伸查詢協定。此命令只影響下一個執行的查詢；之後的所有查詢預設都會使用簡單查詢協定。
<a id="APP-PSQL-META-COMMAND-PASSWORD"></a>

`\password [ username ]` [#](#APP-PSQL-META-COMMAND-PASSWORD)
:   變更指定使用者（預設為目前使用者）的密碼。此命令會提示輸入新密碼、將其加密，並以 `ALTER ROLE` 命令的形式送到伺服器。這可確保新密碼不會以明文出現在命令歷史、伺服器日誌或其他地方。
<a id="APP-PSQL-META-COMMAND-PROMPT"></a>

`\prompt [ text ] name` [#](#APP-PSQL-META-COMMAND-PROMPT)

提示使用者輸入文字，並將該文字指派給變數 *`name`*。可以指定選用的提示字串 *`text`*。（若提示字串由多個單字組成，請用單引號括住該文字。）

預設情況下，`\prompt` 使用終端機進行輸入與輸出。不過，若使用了 `-f` 命令列選項，`\prompt` 會使用標準輸入與標準輸出。
<a id="APP-PSQL-META-COMMAND-PSET"></a>

`\pset [ option [ value ] ]` [#](#APP-PSQL-META-COMMAND-PSET)
:   此命令設定影響查詢結果表格輸出的選項。*`option`* 指出要設定哪一個選項。*`value`* 的語意依所選選項而異。對於某些選項，省略 *`value`* 會使該選項切換開關或取消設定，如各選項的說明所述。若未提及此類行為，則省略 *`value`* 只會顯示目前的設定。

    不帶任何引數的 `\pset` 會顯示所有列印選項的目前狀態。

    可調整的列印選項有：

    <a id="APP-PSQL-META-COMMAND-PSET-BORDER"></a>

    `border` [#](#APP-PSQL-META-COMMAND-PSET-BORDER)
    :   *`value`* 必須是一個數字。一般而言，數字越大，表格的框線與分隔線就越多，但細節取決於特定的格式。在 HTML 格式中，此值會直接轉換為 `border=...` 屬性。在其他大多數格式中，只有 0（無框線）、1（內部分隔線）與 2（表格外框）這幾個值有意義，大於 2 的值會被視同 `border = 2`。`latex` 與 `latex-longtable` 格式另外允許值 3，以在資料列之間加上分隔線。
    <a id="APP-PSQL-META-COMMAND-PSET-COLUMNS"></a>

    `columns` [#](#APP-PSQL-META-COMMAND-PSET-COLUMNS)
    :   設定 `wrapped` 格式的目標寬度，同時也是判斷輸出是否寬到需要使用分頁程式，或在自動展開模式下切換為垂直顯示的寬度上限。零（預設值）表示目標寬度由環境變數 `COLUMNS` 控制；若未設定 `COLUMNS`，則由偵測到的螢幕寬度控制。此外，若 `columns` 為零，則 `wrapped` 格式只影響螢幕輸出。若 `columns` 不為零，則檔案與管線輸出也會換行到該寬度。
    <a id="APP-PSQL-META-COMMAND-PSET-CSV-FIELDSEP"></a>

    `csv_fieldsep` [#](#APP-PSQL-META-COMMAND-PSET-CSV-FIELDSEP)
    :   指定 CSV 輸出格式所使用的欄位分隔字元。若分隔字元出現在某個欄位的值中，該欄位會依標準 CSV 規則以雙引號括住輸出。預設為逗號。
    <a id="APP-PSQL-META-COMMAND-PSET-EXPANDED"></a>

    `expanded`（或 `x`） [#](#APP-PSQL-META-COMMAND-PSET-EXPANDED)
    :   若指定了 *`value`*，它必須是 `on` 或 `off`（分別啟用或停用展開模式），或是 `auto`。若省略 *`value`*，此命令會在 on 與 off 設定之間切換。啟用展開模式時，查詢結果會以兩個欄位顯示，左邊是欄位名稱，右邊是資料。若資料在一般的「水平」模式下無法放進螢幕，此模式就很有用。在 auto 設定下，只要查詢輸出有超過一個欄位且寬度超過螢幕，就會使用展開模式；否則使用一般模式。auto 設定只在對齊（aligned）與換行（wrapped）格式中有效。在其他格式中，它的行為一律如同展開模式為關閉。
    <a id="APP-PSQL-META-COMMAND-PSET-FIELDSEP"></a>

    `fieldsep` [#](#APP-PSQL-META-COMMAND-PSET-FIELDSEP)
    :   指定非對齊輸出格式所使用的欄位分隔字元。如此一來，就可以建立例如其他程式可能偏好的定位字元（tab）分隔輸出。若要將定位字元設為欄位分隔字元，請輸入 `\pset fieldsep
        '\t'`。預設的欄位分隔字元是 `'|'`（垂直線）。
    <a id="APP-PSQL-META-COMMAND-PSET-FIELDSEP-ZERO"></a>

    `fieldsep_zero` [#](#APP-PSQL-META-COMMAND-PSET-FIELDSEP-ZERO)
    :   將非對齊輸出格式所使用的欄位分隔字元設為值為 0 的位元組（NUL）。
    <a id="APP-PSQL-META-COMMAND-PSET-FOOTER"></a>

    `footer` [#](#APP-PSQL-META-COMMAND-PSET-FOOTER)
    :   若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用表格頁尾（`(n rows)` 計數）的顯示。若省略 *`value`*，此命令會切換頁尾顯示的開關。
    <a id="APP-PSQL-META-COMMAND-PSET-FORMAT"></a>

    `format` [#](#APP-PSQL-META-COMMAND-PSET-FORMAT)
    :   將輸出格式設為 `aligned`、`asciidoc`、`csv`、`html`、`latex`、`latex-longtable`、`troff-ms`、`unaligned` 或 `wrapped` 其中之一。允許使用不產生歧義的縮寫。

        `aligned` 格式是標準、人類可讀、排版整齊的文字輸出；這是預設格式。

        `unaligned` 格式會將一筆資料列的所有欄位寫在同一行，並以目前生效的欄位分隔字元分隔。這對於建立可能要給其他程式讀取的輸出很有用，例如定位字元分隔或逗號分隔的格式。不過，若欄位分隔字元出現在某個欄位的值中，並不會受到特別處理；因此 CSV 格式可能更適合這類用途。

        `csv` 格式
        <a id="id-1.9.4.21.8.4.11.1.81.2.3.1.8.2.4.2"></a>
        會寫出以逗號分隔的欄位值，並套用 [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180) 所描述的引號規則。此輸出與伺服器 `COPY` 命令的 CSV 格式相容。除非 `tuples_only` 參數為 `on`，否則會產生含有欄位名稱的標頭行。標題與頁尾不會印出。每筆資料列以系統相關的行尾字元結束；在類 Unix 系統上通常是單一換行字元（`\n`），在 Microsoft Windows 上則是歸位與換行字元序列（`\r\n`）。可以用 `\pset csv_fieldsep` 選擇逗號以外的欄位分隔字元。

        `wrapped` 格式與 `aligned` 類似，但會將較寬的資料值換行到多行，使輸出符合目標欄寬。目標寬度依 `columns` 選項所述方式決定。請注意，psql 不會嘗試對欄位標頭標題換行；因此，若欄位標頭所需的總寬度超過目標寬度，`wrapped` 格式的行為會與 `aligned` 相同。

        `asciidoc`、`html`、`latex`、`latex-longtable` 與 `troff-ms` 格式輸出的表格，是要分別放入使用對應標記語言的文件中。它們並不是完整的文件！在 HTML 中這可能不是必要的，但在 LaTeX 中你必須有完整的文件包裝。`latex` 格式使用 LaTeX 的 `tabular` 環境。`latex-longtable` 格式需要 LaTeX 的 `longtable` 與 `booktabs` 套件。
    <a id="APP-PSQL-META-COMMAND-PSET-LINESTYLE"></a>

    `linestyle` [#](#APP-PSQL-META-COMMAND-PSET-LINESTYLE)
    :   將框線的繪製樣式設為 `ascii`、`old-ascii` 或 `unicode` 其中之一。允許使用不產生歧義的縮寫。（這表示一個字母就夠了。）預設設定為 `ascii`。此選項只影響 `aligned` 與 `wrapped` 輸出格式。

        `ascii` 樣式使用純 ASCII 字元。資料中的換行會以右側邊界的 `+` 符號表示。當 `wrapped` 格式在沒有換行字元的情況下將資料從一行折到下一行時，會在第一行的右側邊界顯示一個點（`.`），並在下一行的左側邊界再顯示一次。

        `old-ascii` 樣式使用純 ASCII 字元，採用 PostgreSQL 8.4 及更早版本所使用的格式樣式。資料中的換行會以 `:` 符號取代左側的欄位分隔符號來表示。當資料在沒有換行字元的情況下從一行折到下一行時，會以 `;` 符號取代左側的欄位分隔符號。

        `unicode` 樣式使用 Unicode 框線繪製字元。資料中的換行會以右側邊界的歸位符號表示。當資料在沒有換行字元的情況下從一行折到下一行時，會在第一行的右側邊界顯示一個省略符號，並在下一行的左側邊界再顯示一次。

        當 `border` 設定大於零時，`linestyle` 選項也會決定繪製框線所用的字元。純 ASCII 字元在任何地方都能運作，但在能辨識 Unicode 字元的顯示器上，Unicode 字元看起來比較美觀。
    <a id="APP-PSQL-META-COMMAND-PSET-NULL"></a>

    `null` [#](#APP-PSQL-META-COMMAND-PSET-NULL)
    :   設定在空值（null）的位置要印出的字串。預設是什麼都不印，這很容易被誤認為空字串。例如，你可能會偏好使用 `\pset null
        '(null)'`。
    <a id="APP-PSQL-META-COMMAND-PSET-NUMERICLOCALE"></a>

    `numericlocale` [#](#APP-PSQL-META-COMMAND-PSET-NUMERICLOCALE)
    :   若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用以特定語言環境（locale）的字元來分隔小數點左側數字群組的顯示。若省略 *`value`*，此命令會在一般數字輸出與特定語言環境的數字輸出之間切換。
    <a id="APP-PSQL-META-COMMAND-PSET-PAGER"></a>

    `pager` [#](#APP-PSQL-META-COMMAND-PSET-PAGER)
    :   控制查詢輸出與 psql 說明輸出是否使用分頁程式。當 `pager` 選項為 `off` 時，不使用分頁程式。當 `pager` 選項為 `on` 時，會在適當的時候使用分頁程式，亦即輸出到終端機且無法在一個畫面中容納時。`pager` 選項也可以設為 `always`，這會使所有終端機輸出都使用分頁程式，不論是否能在一個畫面中容納。不帶 *`value`* 的 `\pset pager` 會切換分頁程式的使用開關。

        若設定了環境變數 `PSQL_PAGER` 或 `PAGER`，要分頁的輸出會以管線傳給指定的程式。否則會使用與平台相關的預設程式（例如 `more`）。

        在 Unix 系統上，使用 `\watch` 命令重複執行查詢時，會改用環境變數 `PSQL_WATCH_PAGER` 來尋找分頁程式。之所以另外設定，是因為這可能會讓傳統的分頁程式混淆，但可用來將輸出傳送給能理解 psql 輸出格式的工具（例如 `pspg --stream`）。
    <a id="APP-PSQL-META-COMMAND-PSET-PAGER-MIN-LINES"></a>

    `pager_min_lines` [#](#APP-PSQL-META-COMMAND-PSET-PAGER-MIN-LINES)
    :   若 `pager_min_lines` 設為大於頁面高度的數字，則除非至少有這麼多行輸出要顯示，否則不會呼叫分頁程式。預設設定為 0。
    <a id="APP-PSQL-META-COMMAND-PSET-RECORDSEP"></a>

    `recordsep` [#](#APP-PSQL-META-COMMAND-PSET-RECORDSEP)
    :   指定非對齊輸出格式所使用的記錄（行）分隔字元。預設為換行字元。
    <a id="APP-PSQL-META-COMMAND-PSET-RECORDSEP-ZERO"></a>

    `recordsep_zero` [#](#APP-PSQL-META-COMMAND-PSET-RECORDSEP-ZERO)
    :   將非對齊輸出格式所使用的記錄分隔字元設為值為 0 的位元組（NUL）。
    <a id="APP-PSQL-META-COMMAND-PSET-TABLEATTR"></a>

    `tableattr`（或 `T`） [#](#APP-PSQL-META-COMMAND-PSET-TABLEATTR)
    :   在 HTML 格式中，此選項指定要放在 `table` 標籤內的屬性。例如可以是 `cellpadding` 或 `bgcolor`。請注意，你大概不會想在這裡指定 `border`，因為那已經由 `\pset border` 處理了。若未給定 *`value`*，則會取消設定表格屬性。

        在 `latex-longtable` 格式中，此選項控制每個包含靠左對齊資料型別之欄位的比例寬度。它以空白分隔的值清單指定，例如 `'0.2 0.2 0.6'`。未指定的輸出欄位會使用最後一個指定的值。
    <a id="APP-PSQL-META-COMMAND-PSET-TITLE"></a>

    `title`（或 `C`） [#](#APP-PSQL-META-COMMAND-PSET-TITLE)
    :   設定之後所印出之任何表格的表格標題。這可用來為你的輸出加上描述性的標籤。若未給定 *`value`*，則會取消設定標題。
    <a id="APP-PSQL-META-COMMAND-PSET-TUPLES-ONLY"></a>

    `tuples_only`（或 `t`） [#](#APP-PSQL-META-COMMAND-PSET-TUPLES-ONLY)
    :   若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用僅資料列（tuples-only）模式。若省略 *`value`*，此命令會在一般輸出與僅資料列輸出之間切換。一般輸出包含額外資訊，例如欄位標頭、標題與各種頁尾。在僅資料列模式下，只會顯示實際的表格資料。
    <a id="APP-PSQL-META-COMMAND-PSET-UNICODE-BORDER-LINESTYLE"></a>

    `unicode_border_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-BORDER-LINESTYLE)
    :   將 `unicode` 線條樣式的框線繪製樣式設為 `single` 或 `double` 其中之一。
    <a id="APP-PSQL-META-COMMAND-PSET-UNICODE-COLUMN-LINESTYLE"></a>

    `unicode_column_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-COLUMN-LINESTYLE)
    :   將 `unicode` 線條樣式的欄位繪製樣式設為 `single` 或 `double` 其中之一。
    <a id="APP-PSQL-META-COMMAND-PSET-UNICODE-HEADER-LINESTYLE"></a>

    `unicode_header_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-HEADER-LINESTYLE)
    :   將 `unicode` 線條樣式的標頭繪製樣式設為 `single` 或 `double` 其中之一。
    <a id="APP-PSQL-META-COMMAND-PSET-XHEADER-WIDTH"></a>

    `xheader_width` [#](#APP-PSQL-META-COMMAND-PSET-XHEADER-WIDTH)
    :   將擴展輸出的標頭最大寬度設為 `full`（預設值）、`column`、`page` 或某個 *`integer value`* 其中之一。

        `full`：擴展標頭不會被截斷，寬度會與最寬的輸出行相同。

        `column`：將標頭行截斷為第一個欄位的寬度。

        `page`：將標頭行截斷為終端機的寬度。

        *`integer value`*：指定標頭行的確切最大寬度。

    這些不同格式的外觀範例，請參閱下方的[範例](app-psql.md#APP-PSQL-EXAMPLES)。

    <a id="APP-PSQL-META-COMMAND-PSET-TIP"></a>

    ### 提示

    `\pset` 有多個簡寫命令。請參閱 `\a`、`\C`、`\f`、`\H`、`\t`、`\T` 與 `\x`。
<a id="APP-PSQL-META-COMMAND-QUIT"></a>

`\q` 或 `\quit` [#](#APP-PSQL-META-COMMAND-QUIT)
:   結束 psql 程式。在腳本檔中，只會終止該腳本的執行。
<a id="APP-PSQL-META-COMMAND-QECHO"></a>

`\qecho text [ ... ]` [#](#APP-PSQL-META-COMMAND-QECHO)
:   此命令與 `\echo` 相同，差別在於輸出會寫入由 `\o` 設定的查詢輸出通道。
<a id="APP-PSQL-META-COMMAND-RESET"></a>

`\r` 或 `\reset` [#](#APP-PSQL-META-COMMAND-RESET)
:   重設（清除）查詢緩衝區。
<a id="APP-PSQL-META-COMMAND-RESTRICT"></a>

`\restrict restrict_key` [#](#APP-PSQL-META-COMMAND-RESTRICT)

以所提供的金鑰進入「受限」模式。在此模式下，唯一允許的中繼命令是用來離開受限模式的 `\unrestrict`。金鑰只能包含英數字元。

此命令主要供 pg_dump、pg_dumpall 與 pg_restore 所產生的純文字傾印使用，但在其他地方也可能有用。
<a id="APP-PSQL-META-COMMAND-S"></a>

`\s [ filename ]` [#](#APP-PSQL-META-COMMAND-S)
:   將 psql 的命令列歷史印到 *`filename`*。若省略 *`filename`*，歷史會寫到標準輸出（適當時會使用分頁程式）。若 psql 建置時未包含 Readline 支援，則無法使用此命令。
<a id="APP-PSQL-META-COMMAND-SET"></a>

`\set [ name [ value [ ... ] ] ]` [#](#APP-PSQL-META-COMMAND-SET)
:   將 psql 變數 *`name`* 設為 *`value`*；若給定超過一個值，則設為所有值串接的結果。若只給定一個引數，該變數會被設為空字串值。若要取消設定變數，請使用 `\unset` 命令。

    不帶任何引數的 `\set` 會顯示目前所有已設定之 psql 變數的名稱與值。

    有效的變數名稱可以包含字母、數字與底線。詳細資訊請參閱下方的[變數](app-psql.md#APP-PSQL-VARIABLES)。變數名稱區分大小寫。

    某些變數比較特殊，它們會控制 psql 的行為，或是會自動設定以反映連線狀態。這些變數記載於下方的[變數](app-psql.md#APP-PSQL-VARIABLES)。

    <a id="APP-PSQL-META-COMMAND-SET-NOTE"></a>

    ### 注意

    此命令與 SQL 命令 [`SET`](../sql-commands/sql-set.md) 無關。
<a id="APP-PSQL-META-COMMAND-SETENV"></a>

`\setenv name [ value ]` [#](#APP-PSQL-META-COMMAND-SETENV)

將環境變數 *`name`* 設為 *`value`*；若未提供 *`value`*，則取消設定該環境變數。範例：

```

    testdb=> \setenv PAGER less
    testdb=> \setenv LESS -imx4F
```
<a id="APP-PSQL-META-COMMAND-SF"></a>

`\sf[+] function_description` [#](#APP-PSQL-META-COMMAND-SF)

此命令會取得並顯示指定函式或程序的定義，形式為 `CREATE OR REPLACE FUNCTION` 或 `CREATE OR REPLACE PROCEDURE` 命令。定義會印到由 `\o` 設定的目前查詢輸出通道。

目標函式可以只用名稱指定，也可以用名稱加上引數指定，例如 `foo(integer, text)`。若有超過一個同名的函式，就必須提供引數型別。

若在命令名稱後加上 `+`，輸出的各行會加上行號，函式主體的第一行為第 1 行。

與其他大多數中繼命令不同，該行的其餘部分一律會被當成 `\sf` 的引數，而且引數中既不進行變數插值，也不進行反引號展開。
<a id="APP-PSQL-META-COMMAND-SV"></a>

`\sv[+] view_name` [#](#APP-PSQL-META-COMMAND-SV)

此命令會取得並顯示指定檢視表的定義，形式為 `CREATE OR REPLACE VIEW` 命令。定義會印到由 `\o` 設定的目前查詢輸出通道。

若在命令名稱後加上 `+`，輸出的各行會從 1 開始加上行號。

與其他大多數中繼命令不同，該行的其餘部分一律會被當成 `\sv` 的引數，而且引數中既不進行變數插值，也不進行反引號展開。
<a id="APP-PSQL-META-COMMAND-PIPELINE"></a>

`\startpipeline`<br>`\sendpipeline`<br>`\syncpipeline`<br>`\endpipeline`<br>`\flushrequest`<br>`\flush`<br>`\getresults [ number_results ]` [#](#APP-PSQL-META-COMMAND-PIPELINE)

這組命令實作 SQL 陳述式的管線化。管線必須以 `\startpipeline` 開始，並以 `\endpipeline` 結束。兩者之間可以有任意數量的 `\syncpipeline` 命令，它會送出一個 [sync 訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)，但不會結束進行中的管線，並會將傳送緩衝區中的資料送出（flush）。在管線模式下，陳述式會送到伺服器，而不等待先前陳述式的結果。詳細資訊請參閱[第 32.5 節](../../client-interfaces/libpq/libpq-pipeline-mode.md)。

管線進行期間執行的所有查詢都使用延伸查詢協定。查詢以分號結尾時會附加到管線中。中繼命令 `\bind`、`\bind_named`、`\close_prepared` 或 `\parse` 可以在進行中的管線中使用。管線進行期間，`\sendpipeline` 會將目前的查詢緩衝區附加到管線中。其他中繼命令，例如 `\g`、`\gx` 或 `\gdesc`，在管線模式下不允許使用。

`\flushrequest` 會在管線中附加一個 flush 命令，讓你可以用 `\getresults` 讀取結果，而不必發出 sync 或結束管線。`\getresults` 會自動將尚未送出的資料推送到伺服器。`\flush` 可用來手動推送尚未送出的資料。

`\getresults` 接受一個選用的 *`number_results`* 參數。若有提供，只會讀取前 *`number_results`* 個待處理的結果。若未提供或為 `0`，則會讀取所有待處理的結果。

管線模式啟用時，會有一個專用的提示字串變數可用來回報管線狀態。詳細資訊請參閱 [`%P`](app-psql.md#APP-PSQL-PROMPTING-P-UC)

管線模式下不支援 `COPY`。

範例：

```

    \startpipeline
    SELECT * FROM pg_class;
    SELECT 1 \bind \sendpipeline
    \flushrequest
    \getresults
    \endpipeline
```
<a id="APP-PSQL-META-COMMAND-T-LC"></a>

`\t` [#](#APP-PSQL-META-COMMAND-T-LC)
:   切換輸出欄位名稱標頭與資料列計數頁尾的顯示。此命令等同於 `\pset
    tuples_only`，是為了方便而提供的。
<a id="APP-PSQL-META-COMMAND-T-UC"></a>

`\T table_options` [#](#APP-PSQL-META-COMMAND-T-UC)
:   指定要放在 HTML 輸出格式之 `table` 標籤內的屬性。此命令等同於 `\pset
    tableattr table_options`。
<a id="APP-PSQL-META-COMMAND-TIMING"></a>

`\timing [ on | off ]` [#](#APP-PSQL-META-COMMAND-TIMING)
:   帶參數時，開啟或關閉每個 SQL 陳述式執行時間的顯示。不帶參數時，在開啟與關閉之間切換顯示。顯示的單位是毫秒；超過 1 秒的時間間隔也會以「分:秒」格式顯示，必要時會加上小時與天數欄位。
<a id="APP-PSQL-META-COMMAND-UNRESTRICT"></a>

`\unrestrict restrict_key` [#](#APP-PSQL-META-COMMAND-UNRESTRICT)

離開「受限」模式（也就是其他所有中繼命令都被封鎖的模式），前提是指定的金鑰與進入受限模式時提供給 `\restrict` 的金鑰相符。

此命令主要供 pg_dump、pg_dumpall 與 pg_restore 所產生的純文字傾印使用，但在其他地方也可能有用。

與其他大多數中繼命令不同，該行的其餘部分一律會被當成 `\unrestrict` 的引數，而且既不進行變數插值，也不進行反引號展開。
<a id="APP-PSQL-META-COMMAND-UNSET"></a>

`\unset name` [#](#APP-PSQL-META-COMMAND-UNSET)

取消設定（刪除）psql 變數 *`name`*。

大多數控制 psql 行為的變數無法取消設定；對它們執行 `\unset` 命令，會被解讀為將其設為預設值。請參閱下方的[變數](app-psql.md#APP-PSQL-VARIABLES)。
<a id="APP-PSQL-META-COMMAND-WRITE"></a>

`\w` 或 `\write` *`filename`*<br>`\w` 或 `\write` `|`*`command`* [#](#APP-PSQL-META-COMMAND-WRITE)

將目前的查詢緩衝區寫入檔案 *`filename`*，或以管線傳給 shell 命令 *`command`*。若目前的查詢緩衝區是空的，則改為寫出最近一次執行的查詢。

若引數以 `|` 開頭，該行的其餘部分全部會被當成要執行的 *`command`*，而且其中既不進行變數插值，也不進行反引號展開。該行的其餘部分只是原封不動地傳給 shell。
<a id="APP-PSQL-META-COMMAND-WARN"></a>

`\warn text [ ... ]` [#](#APP-PSQL-META-COMMAND-WARN)
:   此命令與 `\echo` 相同，差別在於輸出會寫入 psql 的標準錯誤通道，而不是標準輸出。
<a id="APP-PSQL-META-COMMAND-WATCH"></a>

`\watch [ i[nterval]=seconds ] [ c[ount]=times ] [ m[in_rows]=rows ] [ seconds ]` [#](#APP-PSQL-META-COMMAND-WATCH)

重複執行目前的查詢緩衝區（如同 `\g` 所做的），直到被中斷、查詢失敗、達到執行次數上限（若有給定），或查詢傳回的資料列數不再達到最小數量為止。每次執行之間等待指定的秒數（預設為 2）。預設的等待時間可以用變數 [`WATCH_INTERVAL`](app-psql.md#APP-PSQL-VARIABLES-WATCH-INTERVAL) 變更。為了向後相容性，*`seconds`* 可以加上或不加 `interval=` 前綴來指定。每個查詢結果都會連同一個標頭一起顯示，標頭包含 `\pset title` 字串（若有）、查詢開始的時間以及延遲間隔。

若目前的查詢緩衝區是空的，則改為重新執行最近一次送出的查詢。
<a id="APP-PSQL-META-COMMAND-X"></a>

`\x [ on | off | auto ]` [#](#APP-PSQL-META-COMMAND-X)
:   設定或切換擴展表格格式模式。因此它等同於 `\pset expanded`。
<a id="APP-PSQL-META-COMMAND-Z"></a>

`\z[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-Z)

列出資料表、檢視表與序列，以及它們相關的存取權限。若指定了 *`pattern`*，只會列出名稱符合該模式的資料表、檢視表與序列。預設只顯示使用者建立的物件；提供模式或 `S` 修飾字可將系統物件也包含進來。若在命令名稱後加上 `x`，結果會以展開模式顯示。

這是 `\dp`（「display privileges」，顯示權限）的別名。
<a id="APP-PSQL-META-COMMAND-EXCLAMATION-MARK"></a>

`\! [ command ]` [#](#APP-PSQL-META-COMMAND-EXCLAMATION-MARK)

不帶引數時，會跳出到子 shell；子 shell 結束後 psql 會繼續運作。帶引數時，會執行 shell 命令 *`command`*。

與其他大多數中繼命令不同，該行的其餘部分一律會被當成 `\!` 的引數，而且引數中既不進行變數插值，也不進行反引號展開。該行的其餘部分只是原封不動地傳給 shell。
<a id="APP-PSQL-META-COMMAND-QUESTION-MARK"></a>

`\? [ topic ]` [#](#APP-PSQL-META-COMMAND-QUESTION-MARK)
:   顯示說明資訊。選用的 *`topic`* 參數（預設為 `commands`）選擇要說明 psql 的哪一部分：`commands` 說明 psql 的反斜線命令；`options` 說明可傳給 psql 的命令列選項；`variables` 則顯示 psql 設定變數的說明。
<a id="APP-PSQL-META-COMMAND-SEMICOLON"></a>

`\;` [#](#APP-PSQL-META-COMMAND-SEMICOLON)

反斜線分號並不是與前述命令同類的中繼命令；它只是讓一個分號被加入查詢緩衝區，而不做任何進一步的處理。

一般而言，psql 一讀到結束命令的分號，就會將 SQL 命令送到伺服器，即使目前這一行還有更多輸入也一樣。因此，舉例來說，輸入

```

    select 1; select 2; select 3;
```

會使這三個 SQL 命令個別送到伺服器，並在繼續下一個命令之前顯示每個命令的結果。然而，以 `\;` 輸入的分號不會觸發命令處理，因此它前面的命令與後面的命令實際上會合併，並以單一請求送到伺服器。所以舉例來說，

```

    select 1\; select 2\; select 3;
```

會在遇到沒有反斜線的分號時，以單一請求將這三個 SQL 命令送到伺服器。除非字串中包含明確的 `BEGIN`/`COMMIT` 命令將其分成多個交易，否則伺服器會將這樣的請求當作單一交易執行。（關於伺服器如何處理多查詢字串的詳細資訊，請參閱[第 54.2.2.1 節](../../internals/protocol/protocol-flow.md#PROTOCOL-FLOW-MULTI-STATEMENT)。）

<a id="APP-PSQL-PATTERNS"></a>

#### 模式

<a id="id-1.9.4.21.8.4.12.2"></a>

各個 `\d` 命令都接受一個 *`pattern`* 參數，用來指定要顯示的物件名稱。在最簡單的情況下，模式就是物件的確切名稱。模式中的字元通常會轉為小寫，就像 SQL 名稱一樣；例如，`\dt FOO` 會顯示名為 `foo` 的資料表。與 SQL 名稱一樣，在模式兩側加上雙引號可以避免轉為小寫。若需要在模式中包含實際的雙引號字元，請在雙引號序列中將它寫成一對雙引號；這同樣符合 SQL 帶引號識別字的規則。例如，`\dt "FOO""BAR"` 會顯示名為 `FOO"BAR`（而不是 `foo"bar`）的資料表。與 SQL 名稱的一般規則不同，你可以只對模式的一部分加上雙引號，例如 `\dt FOO"FOO"BAR` 會顯示名為 `fooFOObar` 的資料表。

每當完全省略 *`pattern`* 參數時，`\d` 命令會顯示目前綱要搜尋路徑中所有可見的物件——這等同於使用 `*` 作為模式。（若一個物件所在的綱要位於搜尋路徑中，且搜尋路徑中較前面沒有出現同類同名的物件，就稱該物件為*可見*的。這等同於說，該物件不必明確加上綱要限定就能以名稱參照。）若要查看資料庫中所有物件而不論其可見性，請使用 `*.*` 作為模式。

在模式中，`*` 比對任意字元序列（包括零個字元），`?` 比對任意單一字元。（此表示法與 Unix shell 的檔名模式相當。）例如，`\dt int*` 會顯示名稱以 `int` 開頭的資料表。但在雙引號內，`*` 與 `?` 會失去這些特殊意義，只會按字面比對。

含有一個點（`.`）的關聯模式，會被解讀為綱要名稱模式後接物件名稱模式。例如，`\dt foo*.*bar*` 會顯示所有位於綱要名稱以 `foo` 開頭之綱要中、且資料表名稱包含 `bar` 的資料表。若沒有出現點，則模式只會比對在目前綱要搜尋路徑中可見的物件。同樣地，雙引號內的點會失去其特殊意義，只會按字面比對。含有兩個點（`.`）的關聯模式，會被解讀為資料庫名稱後接綱要名稱模式，再接物件名稱模式。資料庫名稱的部分不會被當成模式，而且必須與目前連線的資料庫名稱相符，否則會引發錯誤。

含有一個點（`.`）的綱要模式，會被解讀為資料庫名稱後接綱要名稱模式。例如，`\dn mydb.*foo*` 會顯示所有綱要名稱包含 `foo` 的綱要。資料庫名稱的部分不會被當成模式，而且必須與目前連線的資料庫名稱相符，否則會引發錯誤。

進階使用者可以使用正規表示式的表示法，例如字元類別，像是用 `[0-9]` 比對任何數字。所有正規表示式特殊字元的運作方式都如[第 9.7.3 節](../../the-sql-language/functions/functions-matching.md#functions-posix-regexp)所述，但以下例外：`.` 會如上所述被當成分隔符號，`*` 會被轉換為正規表示式表示法 `.*`，`?` 會被轉換為 `.`，而 `$` 則按字面比對。必要時，你可以寫 `?` 來代替 `.`、寫 `(R+|)` 來代替 `R*`，或寫 `(R|)` 來代替 `R?`，以模擬這些模式字元。`$` 不需要作為正規表示式字元，因為模式必須比對整個名稱，這與正規表示式的一般解讀方式不同（換句話說，`$` 會自動附加到你的模式後面）。若不希望模式被錨定，請在開頭和（或）結尾寫上 `*`。請注意，在雙引號內，所有正規表示式特殊字元都會失去其特殊意義，只會按字面比對。此外，在運算子名稱模式（亦即 `\do` 的引數）中，正規表示式特殊字元會按字面比對。

<a id="id-1.9.4.21.8.5"></a>

### 進階功能

<a id="APP-PSQL-VARIABLES"></a>

#### 變數

psql 提供與常見 Unix 命令 shell 類似的變數替換功能。
變數就是名稱／值的組合，其中值可以是任意長度的任意字串。名稱必須由字母（包括非拉丁字母）、數字與底線組成。

要設定變數，請使用 psql 中繼命令
`\set`。例如，

```

testdb=> \set foo bar
```

會把變數 `foo` 設為值
`bar`。要取得變數的內容，請在名稱前加上冒號，例如：

```

testdb=> \echo :foo
bar
```

這在一般 SQL 命令與中繼命令中都有效；詳細說明請參閱下方的[SQL 插值](app-psql.md#APP-PSQL-INTERPOLATION)。

如果呼叫 `\set` 時沒有第二個引數，該變數會被設為空字串值。要取消設定（也就是刪除）變數，請使用命令 `\unset`。要顯示所有變數的值，請呼叫不帶任何引數的 `\set`。

<a id="APP-PSQL-VARIABLES-NOTE"></a>

### 注意

`\set` 的引數與其他命令一樣，適用相同的替換規則。因此你可以建構出有趣的參照，例如 `\set :foo
'something'`，分別得到 Perl 或 PHP 中著名的「軟連結」或「變數的變數」。不幸的是（或者說幸運的是？），這些建構方式沒有辦法拿來做任何有用的事。另一方面，
`\set bar :foo` 是複製變數的完全有效方式。

其中一些變數會被 psql 特別處理。它們代表某些選項設定，可在執行時藉由改變變數的值來變更，或者在某些情況下代表 psql 中可變更的狀態。
依照慣例，所有特別處理之變數的名稱都完全由大寫 ASCII 字母（以及可能的數字與底線）組成。為了確保未來的最大相容性，請避免將這類變數名稱用於你自己的用途。

控制 psql 行為的變數通常無法取消設定，也無法設為無效的值。`\unset`
命令是允許的，但會被解讀為將該變數設為其預設值。不帶第二個引數的 `\set` 命令，對於接受 on 這個值的控制變數，會被解讀為將變數設為 `on`；對於其他控制變數則會被拒絕。此外，接受 `on`
與 `off` 值的控制變數，也會接受其他常見的布林值寫法，例如 `true` 與 `false`。

特別處理的變數如下：

<a id="APP-PSQL-VARIABLES-AUTOCOMMIT"></a>

`AUTOCOMMIT` <a id="id-1.9.4.21.8.5.2.9.1.1.2"></a> [#](#APP-PSQL-VARIABLES-AUTOCOMMIT)
:   設為 `on`（預設值）時，每個 SQL 命令在成功完成後都會自動提交。在此模式下若要延後提交，你必須輸入 `BEGIN` 或 `START
    TRANSACTION` SQL 命令。設為 `off` 或未設定時，SQL
    命令在你明確發出
    `COMMIT` 或 `END` 之前都不會提交。autocommit-off
    模式的運作方式是：在任何尚未位於交易區塊中、本身不是 `BEGIN` 或其他交易控制命令、也不是無法在交易區塊內執行的命令（例如 `VACUUM`）之前，替你隱含地發出 `BEGIN`。

    <a id="id-1.9.4.21.8.5.2.9.1.2.2"></a>

    ### 注意

    在 autocommit-off 模式下，你必須輸入 `ABORT` 或 `ROLLBACK` 來明確放棄任何失敗的交易。
    也請記住，如果你未提交就結束工作階段，你所做的工作將會遺失。

    <a id="id-1.9.4.21.8.5.2.9.1.2.3"></a>

    ### 注意

    autocommit-on 模式是 PostgreSQL 的傳統行為，但 autocommit-off 較接近 SQL 規格。如果你偏好 autocommit-off，可以考慮在系統層級的
    `psqlrc` 檔案或你的
    `~/.psqlrc` 檔案中設定它。
<a id="APP-PSQL-VARIABLES-COMP-KEYWORD-CASE"></a>

`COMP_KEYWORD_CASE` [#](#APP-PSQL-VARIABLES-COMP-KEYWORD-CASE)
:   決定補全 SQL 關鍵字時使用的大小寫。
    若設為 `lower` 或 `upper`，補全的字詞會分別是小寫或大寫。若設為 `preserve-lower`
    或 `preserve-upper`（預設值），補全的字詞會沿用已輸入字詞的大小寫，但在未輸入任何字元的情況下補全的字詞，則分別會是小寫或大寫。
<a id="APP-PSQL-VARIABLES-DBNAME"></a>

`DBNAME` [#](#APP-PSQL-VARIABLES-DBNAME)
:   你目前連線的資料庫名稱。每次連線到資料庫時（包括程式啟動時）都會設定此變數，但可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-ECHO"></a>

`ECHO` [#](#APP-PSQL-VARIABLES-ECHO)
:   若設為 `all`，所有非空的輸入行在讀取時都會被印到標準輸出。（這不適用於以互動方式讀取的行。）要在程式啟動時選擇此行為，請使用開關 `-a`。若設為
    `queries`，
    psql 會在每個查詢送往伺服器時將其印到標準輸出。選擇此行為的開關是
    `-e`。若設為 `errors`，則只有失敗的查詢會顯示在標準錯誤輸出上。此行為的開關是 `-b`。若設為
    `none`（預設值），則不顯示任何查詢。
<a id="APP-PSQL-VARIABLES-ECHO-HIDDEN"></a>

`ECHO_HIDDEN` [#](#APP-PSQL-VARIABLES-ECHO-HIDDEN)
:   當此變數設為 `on` 且某個反斜線命令會查詢資料庫時，會先顯示該查詢。
    此功能可協助你研究
    PostgreSQL 的內部運作，並在你自己的程式中提供類似的功能。（要在程式啟動時選擇此行為，請使用開關 `-E`。）如果你將此變數設為值 `noexec`，查詢只會被顯示，而不會實際送往伺服器執行。
    預設值為 `off`。
<a id="APP-PSQL-VARIABLES-ENCODING"></a>

`ENCODING` [#](#APP-PSQL-VARIABLES-ENCODING)
:   目前的用戶端字元集編碼。
    每次連線到資料庫時（包括程式啟動時），以及你用 `\encoding` 變更編碼時，都會設定此變數，但它可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-ERROR"></a>

`ERROR` [#](#APP-PSQL-VARIABLES-ERROR)
:   若最後一個 SQL 查詢失敗則為 `true`，成功則為 `false`。另請參閱 `SQLSTATE`。
<a id="APP-PSQL-VARIABLES-FETCH-COUNT"></a>

`FETCH_COUNT` [#](#APP-PSQL-VARIABLES-FETCH-COUNT)
:   若此變數設為大於零的整數值，
    `SELECT` 查詢的結果會以該數量的資料列為一組擷取並顯示，而不是採用預設行為：在顯示前收集整個結果集。因此，無論結果集多大，都只會使用有限的記憶體。啟用此功能時，常用的設定值為 100 到 1000。
    請記住，使用此功能時，查詢可能會在已經顯示部分資料列之後才失敗。

    <a id="id-1.9.4.21.8.5.2.9.8.2.2"></a>

    ### 提示

    雖然此功能可以搭配任何輸出格式使用，但預設的 `aligned` 格式往往看起來不佳，因為每組 `FETCH_COUNT` 筆資料列會分開格式化，導致各組資料列的欄位寬度不一。其他輸出格式的效果較好。
<a id="APP-PSQL-VARIABLES-HIDE-TABLEAM"></a>

`HIDE_TABLEAM` [#](#APP-PSQL-VARIABLES-HIDE-TABLEAM)
:   若此變數設為 `true`，就不會顯示資料表的存取方法細節。這主要用於迴歸測試。
<a id="APP-PSQL-VARIABLES-HIDE-TOAST-COMPRESSION"></a>

`HIDE_TOAST_COMPRESSION` [#](#APP-PSQL-VARIABLES-HIDE-TOAST-COMPRESSION)
:   若此變數設為 `true`，就不會顯示欄位壓縮方法的細節。這主要用於迴歸測試。
<a id="APP-PSQL-VARIABLES-HISTCONTROL"></a>

`HISTCONTROL` [#](#APP-PSQL-VARIABLES-HISTCONTROL)
:   若此變數設為 `ignorespace`，以空白開頭的行不會被加入歷史清單。若設為值 `ignoredups`，與前一筆歷史行相同的行不會被加入。值
    `ignoreboth` 結合了上述兩個選項。若設為 `none`（預設值），在互動模式中讀取的所有行都會儲存到歷史清單中。

    <a id="id-1.9.4.21.8.5.2.9.11.2.2"></a>

    ### 注意

    此功能是毫不客氣地從
    Bash 抄來的。
<a id="APP-PSQL-VARIABLES-HISTFILE"></a>

`HISTFILE` [#](#APP-PSQL-VARIABLES-HISTFILE)

用來儲存歷史清單的檔案名稱。若未設定，檔案名稱會取自 `PSQL_HISTORY`
環境變數。若該變數也未設定，預設值為 `~/.psql_history`，
在 Windows 上則為 `%APPDATA%\postgresql\psql_history`。
例如，將：

```

    \set HISTFILE ~/.psql_history-:DBNAME
```

放在 `~/.psqlrc` 中，會讓
psql 為每個資料庫分別維護一份歷史記錄。

<a id="id-1.9.4.21.8.5.2.9.12.2.2"></a>

### 注意 [#](#psql-histfile-note) <a href="#psql-histfile-note" id="psql-histfile-note"></a>

此功能是毫不客氣地從
Bash 抄來的。
<a id="APP-PSQL-VARIABLES-HISTSIZE"></a>

`HISTSIZE` [#](#APP-PSQL-VARIABLES-HISTSIZE)
:   命令歷史中最多儲存的命令數量（預設為 500）。若設為負值，則不設限制。

    <a id="id-1.9.4.21.8.5.2.9.13.2.2"></a>

    ### 注意

    此功能是毫不客氣地從
    Bash 抄來的。
<a id="APP-PSQL-VARIABLES-HOST"></a>

`HOST` [#](#APP-PSQL-VARIABLES-HOST)
:   你目前連線的資料庫伺服器主機。每次連線到資料庫時（包括程式啟動時）都會設定此變數，但可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-IGNOREEOF"></a>

`IGNOREEOF` [#](#APP-PSQL-VARIABLES-IGNOREEOF)
:   若設為 1 或更小，對 psql 的互動式工作階段送出 EOF 字元（通常是
    **Control**+**D**）
    會終止應用程式。若設為更大的數值，則必須連續輸入該數量的 EOF 字元，才能讓互動式工作階段終止。若變數設為非數值的值，會被解讀為 10。預設值為 0。

    <a id="id-1.9.4.21.8.5.2.9.15.2.2"></a>

    ### 注意

    此功能是毫不客氣地從
    Bash 抄來的。
<a id="APP-PSQL-VARIABLES-LASTOID"></a>

`LASTOID` [#](#APP-PSQL-VARIABLES-LASTOID)
:   最後一個受影響之 OID 的值，由
    `INSERT` 或 `\lo_import`
    命令傳回。此變數只保證有效到下一個 SQL 命令的結果顯示之後為止。
    PostgreSQL 伺服器自版本 12 起不再支援 OID 系統欄位，因此以這類伺服器為目標時，LASTOID 在 `INSERT` 之後一律為 0。
<a id="APP-PSQL-VARIABLES-LAST-ERROR-MESSAGE"></a>

`LAST_ERROR_MESSAGE`<br>`LAST_ERROR_SQLSTATE` [#](#APP-PSQL-VARIABLES-LAST-ERROR-MESSAGE)
:   目前 psql 工作階段中最近一次失敗查詢的主要錯誤訊息及相關的 SQLSTATE 代碼；若目前工作階段中沒有發生錯誤，則分別為空字串與 `00000`。
<a id="APP-PSQL-VARIABLES-ON-ERROR-ROLLBACK"></a>

`ON_ERROR_ROLLBACK` <a id="id-1.9.4.21.8.5.2.9.18.1.2"></a> [#](#APP-PSQL-VARIABLES-ON-ERROR-ROLLBACK)
:   設為 `on` 時，若交易區塊中的某個陳述式產生錯誤，該錯誤會被忽略，交易繼續進行。設為 `interactive` 時，只有在互動式工作階段中才會忽略這類錯誤，讀取腳本檔案時則不會。設為 `off`（預設值）時，交易區塊中產生錯誤的陳述式會中止整個交易。錯誤回復模式的運作方式是：在交易區塊中的每個命令之前，替你隱含地發出 `SAVEPOINT`，並在該命令失敗時回復到該儲存點。
<a id="APP-PSQL-VARIABLES-ON-ERROR-STOP"></a>

`ON_ERROR_STOP` [#](#APP-PSQL-VARIABLES-ON-ERROR-STOP)
:   預設情況下，發生錯誤後命令處理會繼續進行。當此變數設為 `on` 時，處理會改為立即停止。在互動模式中，
    psql 會回到命令提示字串；
    否則 psql 會結束，並傳回錯誤代碼 3，以便與使用錯誤代碼 1 回報的致命錯誤狀況區分。無論哪種情況，目前正在執行的所有腳本（頂層腳本，若有的話，以及它可能叫用的任何其他腳本）都會立即終止。若頂層命令字串包含多個 SQL 命令，處理會在目前的命令停止。
<a id="APP-PSQL-VARIABLES-PIPELINE-COMMAND-COUNT"></a>

`PIPELINE_COMMAND_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-COMMAND-COUNT)
:   進行中的管線裡已排入佇列的命令數量。
<a id="APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT"></a>

`PIPELINE_RESULT_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT)
:   進行中的管線裡，後面接著 `\flushrequest` 或
    `\syncpipeline`（強制伺服器送出結果）的命令數量。這些結果可以用
    `\getresults` 取得。
<a id="APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT"></a>

`PIPELINE_SYNC_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT)
:   進行中的管線裡已排入佇列的同步訊息數量。
<a id="APP-PSQL-VARIABLES-PORT"></a>

`PORT` [#](#APP-PSQL-VARIABLES-PORT)
:   你目前連線的資料庫伺服器連接埠。
    每次連線到資料庫時（包括程式啟動時）都會設定此變數，但可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-PROMPT"></a>

`PROMPT1`<br>`PROMPT2`<br>`PROMPT3` [#](#APP-PSQL-VARIABLES-PROMPT)
:   這些變數指定 psql 發出的提示字串應呈現的樣子。請參閱下方的[提示字串](app-psql.md#APP-PSQL-PROMPTING)。
<a id="APP-PSQL-VARIABLES-QUIET"></a>

`QUIET` [#](#APP-PSQL-VARIABLES-QUIET)
:   將此變數設為 `on` 等同於命令列選項 `-q`。它在互動模式中大概不太有用。
<a id="APP-PSQL-VARIABLES-ROW-COUNT"></a>

`ROW_COUNT` [#](#APP-PSQL-VARIABLES-ROW-COUNT)
:   最後一個 SQL 查詢傳回或影響的資料列數；若查詢失敗或未回報資料列數，則為 0。
<a id="APP-PSQL-VARIABLES-SERVER-VERSION-NAME"></a>

`SERVER_VERSION_NAME`<br>`SERVER_VERSION_NUM` [#](#APP-PSQL-VARIABLES-SERVER-VERSION-NAME)
:   伺服器的版本號，分別以字串形式（例如 `9.6.2`、`10.1` 或 `11beta1`）
    及數字形式（例如 `90602` 或 `100001`）表示。
    每次連線到資料庫時（包括程式啟動時）都會設定這些變數，但可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-SERVICE"></a>

`SERVICE` [#](#APP-PSQL-VARIABLES-SERVICE)
:   服務名稱（若適用）。
<a id="APP-PSQL-VARIABLES-SHELL-ERROR"></a>

`SHELL_ERROR` [#](#APP-PSQL-VARIABLES-SHELL-ERROR)
:   若最後一個 shell 命令失敗則為 `true`，成功則為 `false`。
    這適用於透過 `\!`、
    `\g`、`\o`、`\w`
    與 `\copy` 中繼命令叫用的 shell 命令，以及反引號
    （`` ` ``）展開。請注意，
    對於 `\o`，此變數會在輸出管道被下一個 `\o` 命令關閉時才更新。
    另請參閱 `SHELL_EXIT_CODE`。
<a id="APP-PSQL-VARIABLES-SHELL-EXIT-CODE"></a>

`SHELL_EXIT_CODE` [#](#APP-PSQL-VARIABLES-SHELL-EXIT-CODE)
:   最後一個 shell 命令傳回的結束狀態。
    0–127 代表程式的結束代碼，128–255
    表示因訊號而終止，-1 則表示無法啟動程式或無法收集其結束狀態。
    這適用於透過 `\!`、
    `\g`、`\o`、`\w`
    與 `\copy` 中繼命令叫用的 shell 命令，以及反引號
    （`` ` ``）展開。請注意，
    對於 `\o`，此變數會在輸出管道被下一個 `\o` 命令關閉時才更新。
    另請參閱 `SHELL_ERROR`。
<a id="APP-PSQL-VARIABLES-SHOW-ALL-RESULTS"></a>

`SHOW_ALL_RESULTS` [#](#APP-PSQL-VARIABLES-SHOW-ALL-RESULTS)
:   當此變數設為 `off` 時，組合查詢（`\;`）只會顯示最後一個結果，而不是全部結果。預設值為 `on`。off 行為是為了與舊版
    psql 相容。
<a id="APP-PSQL-VARIABLES-SHOW-CONTEXT"></a>

`SHOW_CONTEXT` [#](#APP-PSQL-VARIABLES-SHOW-CONTEXT)
:   此變數可以設為
    `never`、`errors` 或 `always` 這些值，
    以控制是否在來自伺服器的訊息中顯示 `CONTEXT` 欄位。預設值為 `errors`（表示錯誤訊息中會顯示上下文資訊，但通知或警告訊息中不會）。當 `VERBOSITY` 設為 `terse`
    或 `sqlstate` 時，此設定沒有作用。
    （另請參閱 `\errverbose`，可在你想看剛收到之錯誤的詳細版本時使用。）
<a id="APP-PSQL-VARIABLES-SINGLELINE"></a>

`SINGLELINE` [#](#APP-PSQL-VARIABLES-SINGLELINE)
:   將此變數設為 `on` 等同於命令列選項 `-S`。
<a id="APP-PSQL-VARIABLES-SINGLESTEP"></a>

`SINGLESTEP` [#](#APP-PSQL-VARIABLES-SINGLESTEP)
:   將此變數設為 `on` 等同於命令列選項 `-s`。
<a id="APP-PSQL-VARIABLES-SQLSTATE"></a>

`SQLSTATE` [#](#APP-PSQL-VARIABLES-SQLSTATE)
:   與最後一個 SQL 查詢失敗相關的錯誤代碼（請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)）；若查詢成功則為 `00000`。
<a id="APP-PSQL-VARIABLES-USER"></a>

`USER` [#](#APP-PSQL-VARIABLES-USER)
:   你目前連線所使用的資料庫使用者。每次連線到資料庫時（包括程式啟動時）都會設定此變數，但可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-VERBOSITY"></a>

`VERBOSITY` [#](#APP-PSQL-VARIABLES-VERBOSITY)
:   此變數可以設為 `default`、
    `verbose`、`terse`
    或 `sqlstate` 這些值，以控制錯誤報告的詳細程度。
    （另請參閱 `\errverbose`，可在你想看剛收到之錯誤的詳細版本時使用。）
<a id="APP-PSQL-VARIABLES-VERSION"></a>

`VERSION`<br>`VERSION_NAME`<br>`VERSION_NUM` [#](#APP-PSQL-VARIABLES-VERSION)
:   這些變數在程式啟動時設定，用以反映
    psql 的版本，分別以詳細字串、簡短字串（例如 `9.6.2`、`10.1`
    或 `11beta1`）及數字（例如 `90602`
    或 `100001`）表示。它們可以被變更或取消設定。
<a id="APP-PSQL-VARIABLES-WATCH-INTERVAL"></a>

`WATCH_INTERVAL` [#](#APP-PSQL-VARIABLES-WATCH-INTERVAL)
:   此變數設定
    `\watch` 兩次執行查詢之間預設等待的間隔（以秒為單位）。預設為 2 秒。在命令中指定間隔會覆寫此變數。

<a id="APP-PSQL-INTERPOLATION"></a>

#### SQL 插值

psql 變數的一項關鍵功能是，你可以將它們替換（「插值」）到一般 SQL 陳述式以及中繼命令的引數中。此外，
psql 提供了一些機制，確保作為 SQL 字面常數與識別字使用的變數值會被正確地加上引號。不加任何引號就插值一個值的語法，是在變數名稱前加上冒號
（`:`）。例如，

```

testdb=> \set foo 'my_table'
testdb=> SELECT * FROM :foo;
```

會查詢資料表 `my_table`。請注意，這可能並不安全：變數的值會被逐字複製，因此它可能包含不成對的引號，甚至是反斜線命令。你必須確保它放在該處是合理的。

當某個值要作為 SQL 字面常數或識別字使用時，最安全的做法是讓它加上引號。要將變數的值以 SQL 字面常數的形式加上引號，請寫一個冒號，後面接著以單引號括住的變數名稱。要將該值以 SQL 識別字的形式加上引號，請寫一個冒號，後面接著以雙引號括住的變數名稱。
這些建構方式能正確處理嵌入在變數值中的引號與其他特殊字元。
前面的範例用這種方式寫會更安全：

```

testdb=> \set foo 'my_table'
testdb=> SELECT * FROM :"foo";
```

在加上引號的 SQL 字面常數與識別字內，不會進行變數插值。因此，像 `':foo'` 這樣的寫法無法從變數的值產生加上引號的字面常數（而且即使它可行也不安全，因為它無法正確處理嵌入在值中的引號）。

此機制的一個應用範例，是將檔案的內容複製到資料表欄位中。
先將檔案載入到變數中，再將變數的值以加上引號的字串形式插值：

```

testdb=> \set content `cat my_file.txt`
testdb=> INSERT INTO my_table VALUES (:'content');
```

（請注意，如果 `my_file.txt` 包含 NUL 位元組，這仍然無法運作。
psql 不支援變數值中嵌入 NUL 位元組。）

由於冒號可以合法地出現在 SQL 命令中，看似要插值的寫法（也就是 `:name`、
`:'name'` 或 `:"name"`）只有在該名稱的變數目前已設定時才會被替換。無論如何，你都可以用反斜線跳脫冒號，以防止它被替換。

`:{?name}` 這個特殊語法會依變數是否存在而傳回 TRUE
或 FALSE，因此除非冒號經過反斜線跳脫，否則它一律會被替換。

變數的冒號語法是嵌入式查詢語言（例如 ECPG）的標準 SQL。
用於陣列切片與型別轉換的冒號語法是
PostgreSQL 的擴充語法，有時可能會與標準用法衝突。用於將變數的值跳脫為 SQL 字面常數或識別字的冒號加引號語法，是
psql 的擴充語法。

<a id="APP-PSQL-PROMPTING"></a>

#### 提示字串

psql 發出的提示字串可以依你的喜好自訂。三個變數 `PROMPT1`、
`PROMPT2` 與 `PROMPT3` 包含描述提示字串外觀的字串與特殊跳脫序列。提示字串 1 是
psql 要求輸入新命令時發出的一般提示字串。提示字串 2 會在輸入命令期間預期還有更多輸入時發出，例如因為命令尚未以分號結束，或引號尚未關閉。
提示字串 3 會在你執行 SQL
`COPY FROM STDIN` 命令、需要在終端機上輸入資料列值時發出。

所選提示字串變數的值會被逐字印出，但遇到百分比符號（`%`）時除外。
依下一個字元而定，會改以特定的其他文字替換。已定義的替換如下：

<a id="APP-PSQL-PROMPTING-M-UC"></a>

`%M` [#](#APP-PSQL-PROMPTING-M-UC)
:   資料庫伺服器的完整主機名稱（含網域名稱）；若連線是透過 Unix
    網域通訊端，則為 `[local]`；若 Unix 網域通訊端 不在編譯時的預設位置，則為
    `[local:/dir/name]`。
<a id="APP-PSQL-PROMPTING-M-LC"></a>

`%m` [#](#APP-PSQL-PROMPTING-M-LC)
:   資料庫伺服器的主機名稱，在第一個句點處截斷；若連線是透過 Unix 網域通訊端，則為 `[local]`。
<a id="APP-PSQL-PROMPTING-GT"></a>

`%>` [#](#APP-PSQL-PROMPTING-GT)
:   資料庫伺服器正在監聽的連接埠號。
<a id="APP-PSQL-PROMPTING-N"></a>

`%n` [#](#APP-PSQL-PROMPTING-N)
:   資料庫工作階段使用者名稱。（此值的展開結果可能會在資料庫工作階段期間，因命令 `SET SESSION
    AUTHORIZATION` 而改變。）
<a id="APP-PSQL-PROMPTING-S"></a>

`%s` [#](#APP-PSQL-PROMPTING-S)
:   服務的名稱。
<a id="APP-PSQL-PROMPTING-SLASH"></a>

`%/` [#](#APP-PSQL-PROMPTING-SLASH)
:   目前資料庫的名稱。
<a id="APP-PSQL-PROMPTING-TILDE"></a>

`%~` [#](#APP-PSQL-PROMPTING-TILDE)
:   與 `%/` 類似，但若該資料庫是你的預設資料庫，輸出為 `~`
    （波浪號）。
<a id="APP-PSQL-PROMPTING-NUMBERSIGN"></a>

`%#` [#](#APP-PSQL-PROMPTING-NUMBERSIGN)
:   若工作階段使用者是資料庫超級使用者，則為
    `#`，否則為 `>`。
    （此值的展開結果可能會在資料庫工作階段期間，因命令 `SET SESSION
    AUTHORIZATION` 而改變。）
<a id="APP-PSQL-PROMPTING-P"></a>

`%p` [#](#APP-PSQL-PROMPTING-P)
:   目前所連線之後端的程序 ID。
<a id="APP-PSQL-PROMPTING-P-UC"></a>

`%P` [#](#APP-PSQL-PROMPTING-P-UC)
:   管線狀態：不在管線中時為 `off`，
    在進行中的管線中時為 `on`，
    在已中止的管線中時為 `abort`。
<a id="APP-PSQL-PROMPTING-R"></a>

`%R` [#](#APP-PSQL-PROMPTING-R)
:   在提示字串 1 中通常為 `=`，
    但若工作階段位於條件區塊的非作用中分支則為 `@`，若處於單行模式則為 `^`，
    若工作階段已與資料庫中斷連線（這可能在 `\connect` 失敗時發生）則為 `!`。
    在提示字串 2 中，`%R` 會被替換為一個字元，取決於
    psql 為何預期還有更多輸入：
    若命令只是尚未結束則為 `-`，
    但若有尚未結束的
    `/* ... */` 註解則為 `*`，
    若有尚未結束的引號字串則為單引號，
    若有尚未結束的引號識別字則為雙引號，
    若有尚未結束的錢字號引用字串則為錢字號，
    若有不成對的左括號則為 `(`。
    在提示字串 3 中，`%R` 不會產生任何內容。
<a id="APP-PSQL-PROMPTING-X"></a>

`%x` [#](#APP-PSQL-PROMPTING-X)
:   交易狀態：不在交易區塊中時為空字串，
    在交易區塊中時為 `*`，
    在失敗的交易區塊中時為 `!`，交易狀態無法確定時（例如因為沒有連線）則為 `?`。
<a id="APP-PSQL-PROMPTING-L"></a>

`%l` [#](#APP-PSQL-PROMPTING-L)
:   目前陳述式中的行號，從 `1` 開始。
<a id="APP-PSQL-PROMPTING-DIGITS"></a>

`%`*`digits`* [#](#APP-PSQL-PROMPTING-DIGITS)
:   以指定八進位代碼所對應的字元替換。
<a id="APP-PSQL-PROMPTING-NAME"></a>

`%:`*`name`*`:` [#](#APP-PSQL-PROMPTING-NAME)
:   psql 變數
    *`name`* 的值。詳細資訊請參閱上方的
    [變數](app-psql.md#APP-PSQL-VARIABLES)。
<a id="APP-PSQL-PROMPTING-COMMAND"></a>

`` %` ``*`command`*`` ` `` [#](#APP-PSQL-PROMPTING-COMMAND)
:   *`command`* 的輸出，類似一般的
    「反引號」替換。
<a id="APP-PSQL-PROMPTING-SQUARE-BRACKETS"></a>

`%[` ... `%]` [#](#APP-PSQL-PROMPTING-SQUARE-BRACKETS)

提示字串可以包含終端機控制字元，例如用來改變提示字串文字的顏色、背景或樣式，或改變終端機視窗的標題。為了讓 Readline 的行編輯功能正常運作，這些不可列印的控制字元必須以 `%[` 與
`%]` 括住，標示為不可見。提示字串中可以出現多對這種標記。例如：

```

    testdb=> \set PROMPT1 '%[%033[1;33;40m%]%n@%/%R%[%033[0m%]%# '
```

會在相容 VT100、支援彩色的終端機上，產生粗體（`1;`）、黑底黃字
（`33;40`）的提示字串。
<a id="APP-PSQL-PROMPTING-W"></a>

`%w` [#](#APP-PSQL-PROMPTING-W)
:   與最近一次 `PROMPT1` 輸出寬度相同的空白。這可以作為
    `PROMPT2` 的設定，讓多行陳述式與第一行對齊，但不會出現可見的次要提示字串。

要在提示字串中插入百分比符號，請寫
`%%`。預設的提示字串為：提示字串 1 與 2 是
`'%/%R%x%# '`，提示字串 3 是
`'>> '`。

<a id="APP-PSQL-PROMPTING-NOTE"></a>

### 注意 [#](#zhu-yi-1) <a href="#zhu-yi-1" id="zhu-yi-1"></a>

此功能是毫不客氣地從
tcsh 抄來的。

<a id="APP-PSQL-READLINE"></a>

#### 命令列編輯

<a id="id-1.9.4.21.8.5.5.2"></a><a id="id-1.9.4.21.8.5.5.3"></a>

psql 會在可用時使用
Readline
或 libedit 函式庫，以便於行編輯與擷取。命令歷史會在 psql 結束時自動儲存，並在 psql 啟動時重新載入。輸入
向上方向鍵或 control-P 可取回先前的行。

你也可以在許多（但絕非全部）情境中，使用 Tab 鍵補全來填入輸入到一半的關鍵字與 SQL 物件名稱。例如，
在命令開頭輸入 `ins` 並按下
TAB，會填入 `insert into` 。接著，輸入資料表或綱要名稱的幾個字元並按下 `TAB`，
會填入未完成的名稱；若可能的補全超過一個，則會提供可能補全的選單。（依所使用的函式庫而定，你可能需要按 `TAB` 超過一次才能取得選單。）

SQL 物件名稱的 Tab 鍵補全需要向伺服器送出查詢以尋找可能的相符項目。在某些情境中，這可能會干擾其他操作。例如，在 `BEGIN`
之後，若中間發出了 Tab 鍵補全查詢，就來不及發出 `SET TRANSACTION ISOLATION
LEVEL` 了。
如果你完全不想要 Tab 鍵補全，可以在你的家目錄中名為
`.inputrc` 的檔案裡放入以下內容，將它永久關閉：

```

$if psql
set disable-completion on
$endif
```

（這不是 psql 的功能，而是
Readline 的功能。詳細資訊請閱讀其說明文件。）

`-n`（`--no-readline`）命令列選項也可以用來在單次執行
psql 時停用
Readline。這會停用 Tab 鍵補全、命令列歷史的使用或記錄，以及多行命令的編輯。當你需要複製貼上包含 `TAB` 字元的文字時，這特別有用。

<a id="APP-PSQL-ENVIRONMENT"></a>

## 環境

<a id="APP-PSQL-ENVIRONMENT-COLUMNS"></a>

`COLUMNS` [#](#APP-PSQL-ENVIRONMENT-COLUMNS)
:   若 `\pset columns` 為零，此變數控制
    `wrapped` 格式的寬度，以及用來判斷寬輸出是否需要分頁程式、或在擴展自動模式下是否應切換為垂直格式的寬度。
<a id="APP-PSQL-ENVIRONMENT-PGDATABASE"></a>

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER` [#](#APP-PSQL-ENVIRONMENT-PGDATABASE)
:   預設連線參數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。
<a id="APP-PSQL-ENVIRONMENT-PG-COLOR"></a>

`PG_COLOR` [#](#APP-PSQL-ENVIRONMENT-PG-COLOR)
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與
    `never`。
<a id="APP-PSQL-ENVIRONMENT-PSQL-EDITOR"></a>

`PSQL_EDITOR`<br>`EDITOR`<br>`VISUAL` [#](#APP-PSQL-ENVIRONMENT-PSQL-EDITOR)
:   `\e`、`\ef`
    與 `\ev` 命令所使用的編輯器。
    這些變數會依列出的順序檢查；
    使用第一個已設定的變數。
    若都未設定，預設在 Unix 系統上使用 `vi`，
    在 Windows 系統上使用 `notepad.exe`。
<a id="APP-PSQL-ENVIRONMENT-PSQL-EDITOR-LINENUMBER-ARG"></a>

`PSQL_EDITOR_LINENUMBER_ARG` [#](#APP-PSQL-ENVIRONMENT-PSQL-EDITOR-LINENUMBER-ARG)

當 `\e`、`\ef` 或
`\ev` 搭配行號引數使用時，此變數指定用來將起始行號傳給使用者編輯器的命令列引數。對於 Emacs 或
vi 等編輯器，這是一個加號。如果選項名稱與行號之間需要空格，請在變數的值結尾加上一個空格。範例：

```

    PSQL_EDITOR_LINENUMBER_ARG='+'
    PSQL_EDITOR_LINENUMBER_ARG='--line '
```

在 Unix 系統上預設為 `+`
（對應預設編輯器 `vi`，
也適用於許多其他常見編輯器）；但在 Windows 系統上沒有預設值。
<a id="APP-PSQL-ENVIRONMENT-PSQL-HISTORY"></a>

`PSQL_HISTORY` [#](#APP-PSQL-ENVIRONMENT-PSQL-HISTORY)
:   命令歷史檔案的替代位置。會進行波浪號（`~`）展開。
<a id="APP-PSQL-ENVIRONMENT-PAGER"></a>

`PSQL_PAGER`<br>`PAGER` [#](#APP-PSQL-ENVIRONMENT-PAGER)
:   若查詢結果無法在一個畫面中顯示完，就會透過此命令以管道輸出。典型的值為 `more`
    或 `less`。
    將 `PSQL_PAGER`
    或 `PAGER` 設為空字串，或調整
    `\pset` 命令中與分頁程式相關的選項，即可停用分頁程式。
    這些變數會依列出的順序檢查；
    使用第一個已設定的變數。
    若兩者都未設定，預設在大多數平台上使用 `more`，
    但在 Cygwin 上使用 `less`。
<a id="APP-PSQL-ENVIRONMENT-PSQL-WATCH-PAGER"></a>

`PSQL_WATCH_PAGER` [#](#APP-PSQL-ENVIRONMENT-PSQL-WATCH-PAGER)
:   以 `\watch`
    命令重複執行查詢時，預設不使用分頁程式。在 Unix 系統上，可以將 `PSQL_WATCH_PAGER` 設為某個分頁程式命令來改變此行為。`pspg` 分頁程式（不屬於
    PostgreSQL，但可在許多開放原始碼軟體發行版中取得）若以選項
    `--stream` 啟動，就能顯示
    `\watch` 的輸出。
<a id="APP-PSQL-ENVIRONMENT-PSQLRC"></a>

`PSQLRC` [#](#APP-PSQL-ENVIRONMENT-PSQLRC)
:   使用者 `.psqlrc` 檔案的替代位置。會進行波浪號（`~`）展開。
<a id="APP-PSQL-ENVIRONMENT-SHELL"></a>

`SHELL` [#](#APP-PSQL-ENVIRONMENT-SHELL)
:   `\!` 命令所執行的命令。
<a id="APP-PSQL-ENVIRONMENT-TMPDIR"></a>

`TMPDIR` [#](#APP-PSQL-ENVIRONMENT-TMPDIR)
:   儲存暫存檔案的目錄。預設為
    `/tmp`。

此工具程式與大多數其他 PostgreSQL 工具程式一樣，
也會使用 libpq 支援的環境變數
（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.21.10"></a>

## 檔案

<a id="APP-PSQL-FILES-PSQLRC"></a>

`psqlrc` 與 `~/.psqlrc` [#](#APP-PSQL-FILES-PSQLRC)
:   除非傳入 `-X` 選項，否則
    psql 會在連線到資料庫之後、接受一般命令之前，嘗試讀取並執行系統層級啟動檔案（`psqlrc`）中的命令，接著是使用者個人啟動檔案（`~/.psqlrc`）中的命令。
    這些檔案可以用來依個人喜好設定用戶端和／或伺服器，
    通常是使用 `\set` 與 `SET`
    命令。

    系統層級啟動檔案的名稱為 `psqlrc`。
    預設情況下，會在安裝環境的「系統設定」目錄中尋找它，
    而最可靠的確認方式是執行 `pg_config
    --sysconfdir`。
    此目錄通常是相對於
    PostgreSQL 執行檔所在目錄的 `../etc/`。
    要尋找的目錄可以透過
    `PGSYSCONFDIR` 環境變數明確設定。

    使用者個人啟動檔案的名稱為 `.psqlrc`，
    會在叫用者的家目錄中尋找。
    在 Windows 上，個人啟動檔案則改名為
    `%APPDATA%\postgresql\psqlrc.conf`。
    無論哪種情況，都可以藉由設定
    `PSQLRC` 環境變數來覆寫此預設檔案路徑。

    系統層級啟動檔案與使用者個人啟動檔案，
    都可以藉由在檔案名稱後加上一個連字號與 PostgreSQL
    主要或次要版本識別碼，使其專屬於特定 psql 版本，
    例如 `~/.psqlrc-18` 或
    `~/.psqlrc-18.6`。
    版本最相符的檔案會優先於不分版本的檔案被讀取。
    這些版本後綴是在依上述方式決定檔案路徑之後才加上的。
<a id="APP-PSQL-FILES-PSQL-HISTORY"></a>

`.psql_history` [#](#APP-PSQL-FILES-PSQL-HISTORY)

命令列歷史儲存在檔案
`~/.psql_history` 中，
在 Windows 上則為 `%APPDATA%\postgresql\psql_history`。

歷史檔案的位置可以透過
`HISTFILE` psql 變數或
`PSQL_HISTORY` 環境變數明確設定。

<a id="id-1.9.4.21.11"></a>

## 注意事項

* psql 搭配相同或較舊主要版本的伺服器時運作最佳。如果伺服器的版本比 psql
  本身新，反斜線命令特別容易失敗。不過，`\d` 系列的反斜線命令應該能搭配最早至 9.2 版的伺服器運作，但不一定能搭配比 psql 本身更新的伺服器。執行 SQL 命令與顯示查詢結果的一般功能，應該也能搭配較新主要版本的伺服器運作，但無法保證在所有情況下都是如此。

  如果你想用 psql 連線到數個不同主要版本的伺服器，建議使用最新版本的 psql。或者，你也可以保留每個主要版本的 psql 各一份，並確保使用與各伺服器相符的版本。但實務上，這種額外的複雜度應該是不必要的。
* 在 PostgreSQL 9.6 之前，
  `-c` 選項隱含 `-X`
  （`--no-psqlrc`）；現在已不再如此。
* 在 PostgreSQL 8.4 之前，
  psql 允許單字母反斜線命令的第一個引數直接緊接在命令之後開始，中間不需要空白。
  現在則必須有一些空白。

<a id="id-1.9.4.21.12"></a>

## Windows 使用者注意事項

psql 被建置為「主控台應用程式」。由於 Windows 主控台視窗使用的編碼與系統其他部分不同，在 psql 中使用 8 位元字元時，你必須特別小心。
如果 psql 偵測到有問題的主控台字碼頁，它會在啟動時警告你。要變更主控台字碼頁，需要做兩件事：

* 輸入 **`cmd.exe /c chcp
  1252`** 來設定字碼頁。（1252 是適用於德文的字碼頁；請換成你的值。）如果你使用 Cygwin，
  可以將此命令放在 `/etc/profile` 中。
* 將主控台字型設為 `Lucida Console`，因為點陣字型無法搭配 ANSI 字碼頁使用。

<a id="APP-PSQL-EXAMPLES"></a>

## 範例

第一個範例示範如何將一個命令分散到多行輸入。請注意提示字串的變化：

```

testdb=> CREATE TABLE my_table (
testdb(>  first integer not null default 0,
testdb(>  second text)
testdb-> ;
CREATE TABLE
```

現在再看一次資料表定義：

```

testdb=> \d my_table
              Table "public.my_table"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 first  | integer |           | not null | 0
 second | text    |           |          |
```

現在我們把提示字串改成更有趣的樣子：

```

testdb=> \set PROMPT1 '%n@%m %~%R%# '
peter@localhost testdb=>
```

假設你已經在資料表中填入資料，並想要查看它：

```

peter@localhost testdb=> SELECT * FROM my_table;
 first | second
-------+--------
     1 | one
     2 | two
     3 | three
     4 | four
(4 rows)
```

你可以使用
`\pset` 命令，以不同方式顯示資料表：

```

peter@localhost testdb=> \pset border 2
Border style is 2.
peter@localhost testdb=> SELECT * FROM my_table;
+-------+--------+
| first | second |
+-------+--------+
|     1 | one    |
|     2 | two    |
|     3 | three  |
|     4 | four   |
+-------+--------+
(4 rows)

peter@localhost testdb=> \pset border 0
Border style is 0.
peter@localhost testdb=> SELECT * FROM my_table;
first second
----- ------
    1 one
    2 two
    3 three
    4 four
(4 rows)

peter@localhost testdb=> \pset border 1
Border style is 1.
peter@localhost testdb=> \pset format csv
Output format is csv.
peter@localhost testdb=> \pset tuples_only
Tuples only is on.
peter@localhost testdb=> SELECT second, first FROM my_table;
one,1
two,2
three,3
four,4
peter@localhost testdb=> \pset format unaligned
Output format is unaligned.
peter@localhost testdb=> \pset fieldsep '\t'
Field separator is "    ".
peter@localhost testdb=> SELECT second, first FROM my_table;
one     1
two     2
three   3
four    4
```

或者，使用簡短命令：

```

peter@localhost testdb=> \a \t \x
Output format is aligned.
Tuples only is off.
Expanded display is on.
peter@localhost testdb=> SELECT * FROM my_table;
-[ RECORD 1 ]-
first  | 1
second | one
-[ RECORD 2 ]-
first  | 2
second | two
-[ RECORD 3 ]-
first  | 3
second | three
-[ RECORD 4 ]-
first  | 4
second | four
```

此外，也可以使用
`\g`，只針對單一查詢設定這些輸出格式選項：

```

peter@localhost testdb=> SELECT * FROM my_table
peter@localhost testdb-> \g (format=aligned tuples_only=off expanded=on)
-[ RECORD 1 ]-
first  | 1
second | one
-[ RECORD 2 ]-
first  | 2
second | two
-[ RECORD 3 ]-
first  | 3
second | three
-[ RECORD 4 ]-
first  | 4
second | four
```

以下範例使用 `\df` 命令，
只找出名稱符合 `int*pl`
且第二個引數型別為 `bigint` 的函式：

```

testdb=> \df int*pl * bigint
                          List of functions
   Schema   |  Name   | Result data type | Argument data types | Type
------------+---------+------------------+---------------------+------
 pg_catalog | int28pl | bigint           | smallint, bigint    | func
 pg_catalog | int48pl | bigint           | integer, bigint     | func
 pg_catalog | int8pl  | bigint           | bigint, bigint      | func
(3 rows)
```

這裡使用 `+` 選項來顯示其中一個函式的額外資訊，並使用 `x`
以展開模式顯示結果：

```

testdb=> \df+x int*pl integer bigint
List of functions
-[ RECORD 1 ]-------+-----------------------------
Schema              | pg_catalog
Name                | int48pl
Result data type    | bigint
Argument data types | integer, bigint
Type                | func
Volatility          | immutable
Parallel            | safe
Owner               | postgres
Security            | invoker
Leakproof?          | no
Access privileges   |
Language            | internal
Internal name       | int48pl
Description         | implementation of + operator
```

在適當的情況下，可以使用 `\crosstabview` 命令，
以交叉表的形式呈現查詢結果：

```

testdb=> SELECT first, second, first > 2 AS gt2 FROM my_table;
 first | second | gt2
-------+--------+-----
     1 | one    | f
     2 | two    | f
     3 | three  | t
     4 | four   | t
(4 rows)

testdb=> \crosstabview first second
 first | one | two | three | four
-------+-----+-----+-------+------
     1 | f   |     |       |
     2 |     | f   |       |
     3 |     |     | t     |
     4 |     |     |       | t
(4 rows)
```

第二個範例顯示一張乘法表，其中資料列依數字反向排序，而欄位則依獨立的數字遞增排序。

```

testdb=> SELECT t1.first as "A", t2.first+100 AS "B", t1.first*(t2.first+100) as "AxB",
testdb-> row_number() over(order by t2.first) AS ord
testdb-> FROM my_table t1 CROSS JOIN my_table t2 ORDER BY 1 DESC
testdb-> \crosstabview "A" "B" "AxB" ord
 A | 101 | 102 | 103 | 104
---+-----+-----+-----+-----
 4 | 404 | 408 | 412 | 416
 3 | 303 | 306 | 309 | 312
 2 | 202 | 204 | 206 | 208
 1 | 101 | 102 | 103 | 104
(4 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-psql.html)（原文版本：18.6；核對日期：2026-10-17）
