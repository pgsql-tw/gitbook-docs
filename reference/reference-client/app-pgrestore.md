<a id="APP-PGRESTORE"></a><a id="id-1.9.4.19.1"></a>

## pg_restore

pg_restore — 從 pg_dump 建立的封存檔還原 PostgreSQL 資料庫

<a id="id-1.9.4.19.4"></a>

## 語法

<a id="id-1.9.4.19.4.1"></a>

`pg_restore` [*`connection-option`*...] [*`option`*...] [*`filename`*]

<a id="APP-PGRESTORE-DESCRIPTION"></a>

## 說明

pg_restore 是一個工具程式，用來從 [pg_dump](app-pgdump.md) 以某種非純文字格式建立的封存檔還原 PostgreSQL 資料庫。它會發出必要的命令，將資料庫重建回儲存當時的狀態。封存檔也讓 pg_restore 能夠選擇要還原的內容，甚至在還原之前重新排列項目的順序。封存檔的設計可以跨架構移植。

pg_restore 可以兩種模式運作。若指定了資料庫名稱，pg_restore 會連線到該資料庫，並將封存內容直接還原到資料庫中。否則，會建立一份包含重建資料庫所需 SQL 命令的指令稿，並寫入檔案或標準輸出。這份指令稿輸出等同於 pg_dump 的純文字輸出格式。因此，部分控制輸出的選項與 pg_dump 的選項相似。

顯然，pg_restore 無法還原封存檔中不存在的資訊。例如，若封存檔是使用「以 `INSERT` 命令傾印資料」選項製作的，pg_restore 將無法使用 `COPY` 陳述式載入資料。

<a id="APP-PGRESTORE-DESCRIPTION-WARNING"></a>

### 警告

還原傾印會使目的端執行由來源超級使用者所選擇的任意程式碼。部分傾印與部分還原並不會限制這一點。若來源超級使用者不受信任，則在還原之前必須檢查傾印出的 SQL 陳述式。非純文字傾印可以使用 pg_restore 的 `--file` 選項來檢查。請注意，執行傾印與還原的用戶端不需要信任來源或目的端的超級使用者。

<a id="APP-PGRESTORE-OPTIONS"></a>

## 選項

pg_restore 接受下列命令列引數。

*`filename`*
:   指定要還原之封存檔的位置（若為目錄格式封存，則為目錄）。若未指定，則使用標準輸入。

`-a`<br>`--data-only`

只還原資料，不還原綱要（資料定義）或統計資訊。若封存檔中有資料表資料、大型物件與序列值，則會還原它們。

此選項與指定 `--section=data` 相似，但由於歷史因素，兩者並不完全相同。

`-c`<br>`--clean`
:   在還原資料庫物件之前，發出以 `DROP` 移除所有將要還原之物件的命令。此選項適合用來覆寫現有的資料庫。若有任何物件不存在於目的資料庫中，會回報可忽略的錯誤訊息，除非同時指定了 `--if-exists`。

`-C`<br>`--create`

在還原到資料庫之前先建立該資料庫。若同時指定了 `--clean`，則在連線到目標資料庫之前先移除並重新建立它。

搭配 `--create` 時，pg_restore 也會還原資料庫的註解（若有），以及任何此資料庫專屬的設定變數設定，也就是任何提及此資料庫的 `ALTER DATABASE ... SET ...` 與 `ALTER ROLE ... IN DATABASE ... SET ...` 命令。資料庫本身的存取權限也會被還原，除非指定了 `--no-acl`。

使用此選項時，以 `-d` 指定的資料庫只用來發出最初的 `DROP DATABASE` 與 `CREATE DATABASE` 命令。所有資料都會還原到封存檔中所記載的資料庫名稱中。

`-d dbname`<br>`--dbname=dbname`
:   連線到資料庫 *`dbname`*，並直接還原到該資料庫中。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

`-e`<br>`--exit-on-error`
:   若在將 SQL 命令送往資料庫時遇到錯誤，就結束。預設是繼續執行，並在還原結束時顯示錯誤數量。

`-f filename`<br>`--file=filename`
:   指定所產生指令稿的輸出檔，或與 `-l` 一起使用時清單的輸出檔。使用 `-` 表示 stdout。

`-F format`<br>`--format=format`

指定封存檔的格式。不需要指定格式，因為 pg_restore 會自動判斷格式。若有指定，可以是下列其中之一：

- `c`<br>`custom`

  封存檔為 pg_dump 的自訂格式。

- `d`<br>`directory`

  封存檔為目錄封存。

- `t`<br>`tar`

  封存檔為 `tar` 封存。

`-I index`<br>`--index=index`
:   只還原指定索引的定義。可以使用多個 `-I` 選項指定多個索引。

`-j number-of-jobs`<br>`--jobs=number-of-jobs`

以並行方式執行 pg_restore 中最耗時的步驟（載入資料、建立索引或建立限制條件的步驟），最多使用 *`number-of-jobs`* 個並行工作階段。此選項可以大幅縮短將大型資料庫還原到在多處理器機器上執行之伺服器所需的時間。輸出指令稿而非直接連線到資料庫伺服器時，此選項會被忽略。

每個工作是一個程序或一個執行緒（取決於作業系統），並使用各自獨立的伺服器連線。

此選項的最佳值取決於伺服器、用戶端與網路的硬體配置。影響因素包括 CPU 核心數與磁碟配置。一個不錯的起點是伺服器上的 CPU 核心數，但在許多情況下，比這更大的值也可能帶來更快的還原時間。當然，過高的值會因為系統顛簸（thrashing）而導致效能下降。

此選項只支援自訂與目錄封存格式。輸入必須是一般檔案或目錄（而不是例如管線或標準輸入）。此外，多個工作不能與 `--single-transaction` 選項一起使用。

`-l`<br>`--list`
:   列出封存檔的目錄（table of contents）。此操作的輸出可以作為 `-L` 選項的輸入。請注意，若 `-n` 或 `-t` 等過濾選項與 `-l` 一起使用，它們會限制列出的項目。

`-L list-file`<br>`--use-list=list-file`

只還原 *`list-file`* 中列出的封存元素，並依它們在檔案中出現的順序還原。請注意，若 `-n` 或 `-t` 等過濾選項與 `-L` 一起使用，它們會進一步限制還原的項目。

*`list-file`* 通常是編輯先前 `-l` 操作的輸出而建立的。各行可以移動或移除，也可以在行首加上分號（`;`）將其註解掉。範例請見下文。

`-n schema`<br>`--schema=schema`
:   只還原位於指定綱要中的物件。可以使用多個 `-n` 選項指定多個綱要。此選項可以與 `-t` 選項合併使用，以只還原特定資料表。

`-N schema`<br>`--exclude-schema=schema`

不還原位於指定綱要中的物件。可以使用多個 `-N` 選項指定多個要排除的綱要。

當同一個綱要名稱同時給了 `-n` 與 `-N` 時，以 `-N` 選項為準，該綱要會被排除。

`-O`<br>`--no-owner`
:   不輸出用來將物件擁有權設定成與原始資料庫一致的命令。預設情況下，pg_restore 會發出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 陳述式，來設定所建立之綱要元素的擁有權。除非最初的資料庫連線是由超級使用者（或擁有指令稿中所有物件的同一使用者）建立，否則這些陳述式會失敗。使用 `-O` 時，可以用任何使用者名稱進行最初的連線，而該使用者將擁有所有建立的物件。

`-P function-name(argtype [, ...])`<br>`--function=function-name(argtype [, ...])`
:   只還原指定的函式。請小心地將函式名稱與引數拼寫成與它們在傾印檔目錄中出現的完全相同。可以使用多個 `-P` 選項指定多個函式。

`-R`<br>`--no-reconnect`
:   此選項已過時，但為了向後相容性仍可接受。

`-s`<br>`--schema-only`

只還原綱要（資料定義），不還原資料，範圍以封存檔中存在的綱要項目為限。

此選項不能與 `--data-only` 或 `--statistics-only` 一起使用。它與指定 `--section=pre-data --section=post-data --no-statistics` 相似，但由於歷史因素，兩者並不完全相同。

（請勿將此選項與 `--schema` 選項混淆，後者以不同的意義使用「schema」一詞。）

`-S username`<br>`--superuser=username`
:   指定停用觸發程序時要使用的超級使用者名稱。只有在使用 `--disable-triggers` 時才有關係。

`-t table`<br>`--table=table`

只還原指定資料表的定義和／或資料。就此目的而言，「資料表」包含檢視表、具體化檢視表、序列與外部資料表。寫出多個 `-t` 選項即可選取多個資料表。此選項可以與 `-n` 選項合併使用，以指定特定綱要中的資料表。

<a id="id-1.9.4.19.6.3.20.2.2"></a>

### 注意 [#](#app-pgrestore-restored-note-1) <a href="#app-pgrestore-restored-note-1" id="app-pgrestore-restored-note-1"></a>

指定 `-t` 時，pg_restore 不會嘗試還原所選資料表可能相依的任何其他資料庫物件。因此，無法保證將特定資料表還原到乾淨的資料庫中一定會成功。

<a id="id-1.9.4.19.6.3.20.2.3"></a>

### 注意 [#](#app-pgrestore-restored-note-2) <a href="#app-pgrestore-restored-note-2" id="app-pgrestore-restored-note-2"></a>

此旗標的行為與 pg_dump 的 `-t` 旗標並不完全相同。目前 pg_restore 不提供萬用字元比對，你也不能在其 `-t` 中包含綱要名稱。而且，pg_dump 的 `-t` 旗標也會傾印所選資料表的附屬物件（例如索引），但 pg_restore 的 `-t` 旗標不包含這類附屬物件。

<a id="id-1.9.4.19.6.3.20.2.4"></a>

### 注意 [#](#app-pgrestore-restored-note-3) <a href="#app-pgrestore-restored-note-3" id="app-pgrestore-restored-note-3"></a>

在 PostgreSQL 9.6 之前的版本中，此旗標只比對資料表，不比對任何其他類型的關聯。

`-T trigger`<br>`--trigger=trigger`
:   只還原指定的觸發程序。可以使用多個 `-T` 選項指定多個觸發程序。

`-v`<br>`--verbose`
:   指定詳細模式。這會使 pg_restore 將詳細的物件註解與開始／結束時間輸出到輸出檔，並將進度訊息輸出到標準錯誤。重複指定此選項，會使額外的除錯層級訊息出現在標準錯誤上。

`-V`<br>`--version`
:   印出 pg_restore 版本後結束。

`-x`<br>`--no-privileges`<br>`--no-acl`
:   不還原存取權限（grant／revoke 命令）。

`-1`<br>`--single-transaction`
:   以單一交易執行還原（也就是將發出的命令包在 `BEGIN`/`COMMIT` 中）。這可確保要嘛所有命令都成功完成，要嘛不套用任何變更。此選項隱含 `--exit-on-error`。

`--disable-triggers`

此選項只在執行不含綱要的還原時才有關係。它指示 pg_restore 在還原資料期間，執行暫時停用目標資料表上觸發程序的命令。若你的資料表上有參照完整性檢查或其他觸發程序，而你不希望在資料還原期間觸發它們，請使用此選項。

目前，為 `--disable-triggers` 發出的命令必須以超級使用者身分執行。因此，你也應該以 `-S` 指定超級使用者名稱，或者更好的做法是以 PostgreSQL 超級使用者身分執行 pg_restore。

`--enable-row-security`

此選項只在還原具有資料列安全性之資料表的內容時才有關係。預設情況下，pg_restore 會將 [row_security](../../server-administration/runtime-config/runtime-config-client.md#GUC-ROW-SECURITY) 設為 off，以確保所有資料都還原到資料表中。若使用者沒有足夠的權限略過資料列安全性，則會擲出錯誤。此參數指示 pg_restore 改將 [row_security](../../server-administration/runtime-config/runtime-config-client.md#GUC-ROW-SECURITY) 設為 on，讓使用者能夠嘗試在啟用資料列安全性的情況下還原資料表的內容。若使用者沒有將傾印中的資料列插入該資料表的權利，這仍然可能會失敗。

請注意，此選項目前也要求傾印必須是 `INSERT` 格式，因為 `COPY FROM` 不支援資料列安全性。

`--filter=filename`

指定一個檔案，從中讀取要從還原中排除或納入之物件的模式。這些模式依下列選項的相同規則解讀：`-n`/`--schema` 用於納入綱要中的物件、`-N`/`--exclude-schema` 用於排除綱要中的物件、`-P`/`--function` 用於還原指定的函式、`-I`/`--index` 用於還原指定的索引、`-t`/`--table` 用於還原指定的資料表，或 `-T`/`--trigger` 用於還原觸發程序。若要從 `STDIN` 讀取，請使用 `-` 作為檔名。`--filter` 選項可以與上面列出、用於納入或排除物件的選項一起指定，也可以為多個過濾檔案指定超過一次。

此檔案每一行列出一個資料庫模式，格式如下：

```

    { include | exclude } { function | index | schema | table | trigger } PATTERN
```

第一個關鍵字指定符合該模式的物件要被納入還是排除。第二個關鍵字指定要使用該模式過濾的物件類型：

* `function`：函式，作用如同 `-P`/`--function` 選項。此關鍵字只能與 `include` 關鍵字一起使用。
* `index`：索引，作用如同 -I/--index 選項（原文此處誤植為 `-I`/`--indexes`）。此關鍵字只能與 `include` 關鍵字一起使用。
* `schema`：綱要，作用如同 `-n`/`--schema` 與 `-N`/`--exclude-schema` 選項。
* `table`：資料表，作用如同 `-t`/`--table` 選項。此關鍵字只能與 `include` 關鍵字一起使用。
* `trigger`：觸發程序，作用如同 `-T`/`--trigger` 選項。此關鍵字只能與 `include` 關鍵字一起使用。

以 `#` 開頭的行會被視為註解並被忽略。註解也可以放在物件模式行之後。空白行也會被忽略。關於如何在模式中進行引用，請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)。

`--if-exists`
:   在 `--clean` 模式下，使用 `DROP ... IF EXISTS` 命令移除物件。這會抑制原本可能回報的「does not exist」錯誤。除非同時指定了 `--clean`，否則此選項無效。

`--no-comments`
:   即使封存檔中包含註解，也不輸出還原註解的命令。

`--no-data`
:   即使封存檔中包含資料，也不輸出還原資料的命令。

`--no-data-for-failed-tables`

預設情況下，即使資料表的建立命令失敗（例如因為資料表已存在），仍會還原該資料表的資料。使用此選項時，會略過這類資料表的資料。若目標資料庫已包含所需的資料表內容，這種行為很有用。例如，PostGIS 等 PostgreSQL 擴充功能的輔助資料表可能已經載入目標資料庫；指定此選項可以防止重複或過時的資料被載入其中。

此選項只在直接還原到資料庫時有效，產生 SQL 指令稿輸出時則無效。

`--no-policies`
:   即使封存檔中包含資料列安全性政策，也不輸出還原它們的命令。

`--no-publications`
:   即使封存檔中包含發佈，也不輸出還原它們的命令。

`--no-schema`
:   即使封存檔中包含綱要（資料定義），也不輸出還原它的命令。

`--no-security-labels`
:   即使封存檔中包含安全標籤，也不輸出還原它們的命令。

`--no-statistics`
:   即使封存檔中包含統計資訊，也不輸出還原它們的命令。

`--no-subscriptions`
:   即使封存檔中包含訂閱，也不輸出還原它們的命令。

`--no-table-access-method`
:   不輸出選擇資料表存取方法的命令。使用此選項時，所有物件都會以還原期間的預設資料表存取方法建立。

`--no-tablespaces`
:   不輸出選擇資料表空間的命令。使用此選項時，所有物件都會建立在還原期間的預設資料表空間中。

`--restrict-key=restrict_key`

將提供的字串作為傾印輸出中 psql 的 `\restrict` 金鑰。此選項只能在 SQL 指令稿輸出時指定，也就是使用 `--file` 選項時。若未指定 restrict 金鑰，pg_restore 會視需要產生一個隨機金鑰。金鑰只能包含英數字元。

此選項主要用於測試用途，以及其他需要可重現輸出的情境（例如比較傾印檔）。不建議一般使用，因為事先知道該金鑰的惡意伺服器，可能可以注入任意程式碼，而這些程式碼會在以 psql 執行該傾印輸出的機器上被執行。

`--section=sectionname`

只還原指定的區段。區段名稱可以是 `pre-data`、`data` 或 `post-data`。此選項可以指定超過一次，以選取多個區段。預設是還原所有區段。

data 區段包含實際的資料表資料以及大型物件定義。post-data 項目包含索引、觸發程序、規則，以及已驗證之檢查限制條件以外的限制條件定義。pre-data 項目包含所有其他資料定義項目。

`--statistics`
:   若封存檔中包含統計資訊，則輸出還原它們的命令。這是預設行為。

`--statistics-only`
:   只還原統計資訊，不還原綱要（資料定義）或資料。

`--strict-names`
:   要求每個綱要（`-n`/`--schema`）與資料表（`-t`/`--table`）限定詞，都至少符合要還原之檔案中的一個綱要／資料表。

`--transaction-size=N`

將還原以一系列交易執行，每個交易最多處理 *`N`* 個資料庫物件。此選項隱含 `--exit-on-error`。

`--transaction-size` 提供介於預設行為（每個 SQL 命令一個交易）與 `-1`/`--single-transaction`（所有還原的物件一個交易）之間的折衷選擇。雖然 `--single-transaction` 的額外負擔最小，但對大型資料庫而言可能不切實際，因為該交易會對每個還原的物件取得鎖定，可能耗盡伺服器鎖定表的空間。使用 `--transaction-size` 並將大小設為數千個物件，可以獲得幾乎相同的效能好處，同時限制鎖定表所需的空間量。

`--use-set-session-authorization`
:   輸出符合 SQL 標準的 `SET SESSION AUTHORIZATION` 命令，而不是 `ALTER OWNER` 命令，來決定物件的擁有權。這會使傾印更符合標準，但視傾印中物件的歷史而定，可能無法正確還原。

`-?`<br>`--help`
:   顯示 pg_restore 命令列引數的說明後結束。

pg_restore 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則作為 Unix 網域通訊端的目錄。預設值取自 `PGHOST` 環境變數（若有設定），否則會嘗試使用 Unix 網域通訊端連線。

`-p port`<br>`--port=port`
:   指定伺服器監聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。預設為 `PGPORT` 環境變數（若有設定），或編譯時內建的預設值。

`-U username`<br>`--username=username`
:   要用來連線的使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而密碼無法透過 `.pgpass` 檔案等其他方式取得，連線嘗試將會失敗。此選項在沒有使用者可輸入密碼的批次作業與指令稿中可能很有用。

`-W`<br>`--password`

強制 pg_restore 在連線到資料庫之前提示輸入密碼。

此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_restore 會自動提示輸入密碼。不過，pg_restore 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--role=rolename`
:   指定用來執行還原的角色名稱。此選項會使 pg_restore 在連線到資料庫後發出 `SET ROLE` *`rolename`* 命令。當已驗證的使用者（以 `-U` 指定）缺少 pg_restore 所需的權限，但可以切換到具有所需權利的角色時，此選項很有用。有些安裝環境有禁止直接以超級使用者身分登入的政策，使用此選項可以在不違反該政策的情況下執行還原。

<a id="id-1.9.4.19.7"></a>

## 環境

`PGHOST`<br>`PGOPTIONS`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可能的值為 `always`、`auto` 與 `never`。

此工具與大多數其他 PostgreSQL 工具一樣，也使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。不過，在未提供資料庫名稱時，它不會讀取 `PGDATABASE`。

<a id="APP-PGRESTORE-DIAGNOSTICS"></a>

## 診斷

以 `-d` 選項指定直接的資料庫連線時，pg_restore 會在內部執行 SQL 陳述式。若你在執行 pg_restore 時遇到問題，請確認你能夠使用例如 [psql](app-psql.md) 從資料庫中選取資訊。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都會適用。

<a id="APP-PGRESTORE-NOTES"></a>

## 注意事項

若你的安裝環境對 `template1` 資料庫有任何本地新增的內容，請小心將 pg_restore 的輸出載入真正空白的資料庫；否則，你很可能會因為新增物件的重複定義而遇到錯誤。若要建立不含任何本地新增內容的空白資料庫，請從 `template0` 而非 `template1` 複製，例如：

```

CREATE DATABASE foo WITH TEMPLATE template0;
```

pg_restore 的限制詳述如下。

* 將資料還原到既有的資料表並使用 `--disable-triggers` 選項時，pg_restore 會在插入資料之前發出停用使用者資料表上觸發程序的命令，並在資料插入之後發出重新啟用它們的命令。若還原在中途停止，系統目錄可能會停留在錯誤的狀態。
* pg_restore 無法選擇性地還原大型物件；例如，只還原特定資料表的大型物件。若封存檔包含大型物件，則會還原所有大型物件；若透過 `-L`、`-t` 或其他選項排除它們，則一個也不會還原。

關於 pg_dump 的限制詳情，另請參閱 [pg_dump](app-pgdump.md) 文件。

預設情況下，若傾印檔中包含最佳化器統計資訊，`pg_restore` 會還原它們。若並非所有統計資訊都已還原，對每個還原的資料表執行 `ANALYZE` 可能會有幫助，讓最佳化器擁有有用的統計資訊；更多資訊請參閱[第 24.1.3 節](../../server-administration/maintenance/routine-vacuuming.md#vacuum-for-statistics)與[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#autovacuum)。

<a id="APP-PGRESTORE-EXAMPLES"></a>

## 範例

假設我們已經將名為 `mydb` 的資料庫傾印到自訂格式的傾印檔中：

```

$ pg_dump -Fc mydb > db.dump
```

若要移除該資料庫並從傾印重新建立它：

```

$ dropdb mydb
$ pg_restore -C -d postgres db.dump
```

`-d` 選項中指定的資料庫可以是叢集中任何現有的資料庫；pg_restore 只用它來發出 `mydb` 的 `CREATE DATABASE` 命令。使用 `-C` 時，資料一律會還原到傾印檔中所記載的資料庫名稱中。

若要將傾印還原到名為 `newdb` 的新資料庫：

```

$ createdb -T template0 newdb
$ pg_restore -d newdb db.dump
```

請注意，我們沒有使用 `-C`，而是直接連線到要還原進去的資料庫。另請注意，我們是從 `template0` 而非 `template1` 複製新資料庫，以確保它一開始是空的。

若要重新排列資料庫項目的順序，首先必須傾印封存檔的目錄：

```

$ pg_restore -l db.dump > db.list
```

清單檔由一個標頭以及每個項目一行所組成，例如：

```

;
; Archive created at Mon Sep 14 13:55:39 2009
;     dbname: DBDEMOS
;     TOC Entries: 81
;     Compression: 9
;     Dump Version: 1.10-0
;     Format: CUSTOM
;     Integer: 4 bytes
;     Offset: 8 bytes
;     Dumped from database version: 8.3.5
;     Dumped by pg_dump version: 8.3.8
;
;
; Selected TOC Entries:
;
3; 2615 2200 SCHEMA - public pasha
1861; 0 0 COMMENT - SCHEMA public pasha
1862; 0 0 ACL - public pasha
317; 1247 17715 TYPE public composite pasha
319; 1247 25899 DOMAIN public domain0 pasha
```

分號表示註解的開始，行首的數字代表指派給每個項目的內部封存 ID。

檔案中的各行可以被註解掉、刪除及重新排序。例如：

```

10; 145433 TABLE map_resolutions postgres
;2; 145344 TABLE species postgres
;4; 145359 TABLE nt_header postgres
6; 145402 TABLE species_records postgres
;8; 145416 TABLE ss_old postgres
```

可以作為 pg_restore 的輸入，並且只會依此順序還原項目 10 與 6：

```

$ pg_restore -L db.list db.dump
```

<a id="id-1.9.4.19.11"></a>

## 另請參閱

[pg_dump](app-pgdump.md), [pg_dumpall](app-pg-dumpall.md), [psql](app-psql.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgrestore.html)（原文版本：18.6；核對日期：2026-10-09）
