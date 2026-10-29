<a id="APP-PG-DUMPALL"></a><a id="id-1.9.4.15.1"></a>

## pg_dumpall

pg_dumpall — 將 PostgreSQL 資料庫叢集匯出為腳本檔案

<a id="id-1.9.4.15.4"></a>

## 語法

<a id="id-1.9.4.15.4.1"></a>

`pg_dumpall` [*`connection-option`*...] [*`option`*...]

<a id="APP-PG-DUMPALL-DESCRIPTION"></a>

## 說明

pg_dumpall 是將叢集中所有 PostgreSQL 資料庫寫出（「傾印」）到單一腳本檔案的工具程式。此腳本檔案包含可作為 [psql](app-psql.md) 輸入來還原資料庫的 SQL 命令。它的做法是對叢集中的每個資料庫呼叫 [pg_dump](app-pgdump.md)。pg_dumpall 也會傾印所有資料庫共用的全域物件，也就是資料庫角色、資料表空間，以及設定參數的權限授予。（pg_dump 不會儲存這些物件。）

由於 pg_dumpall 會讀取所有資料庫中的資料表，你很可能必須以資料庫超級使用者身分連線，才能產生完整的傾印。此外，你也需要超級使用者權限來執行儲存下來的腳本，才能被允許新增角色與建立資料庫。

SQL 腳本會寫到標準輸出。請使用 `-f`/`--file` 選項或 shell 運算子將它重新導向到檔案。

pg_dumpall 需要多次連線到 PostgreSQL 伺服器（每個資料庫一次）。若你使用密碼驗證，它每次都會要求輸入密碼。在這種情況下，準備一個 `~/.pgpass` 檔案會很方便。更多資訊請參閱[第 32.16 節](../../client-interfaces/libpq/libpq-pgpass.md)。

<a id="APP-PG-DUMPALL-DESCRIPTION-WARNING"></a>

### 警告

還原傾印會使目的端執行由來源端超級使用者所選擇的任意程式碼。部分傾印與部分還原並不能限制這一點。若來源端超級使用者不受信任，則必須在還原之前檢查所傾印的 SQL 陳述式。請注意，執行傾印與還原的用戶端不需要信任來源端或目的端的超級使用者。

<a id="id-1.9.4.15.6"></a>

## 選項

下列命令列選項控制輸出的內容與格式。

`-a`<br>`--data-only`
:   只傾印資料，不傾印綱要（資料定義）或統計資訊。

`-c`<br>`--clean`
:   在重新建立所有被傾印的資料庫、角色與資料表空間之前，先輸出 `DROP` 它們的 SQL 命令。當還原要覆寫現有叢集時，這個選項很有用。若目的端叢集中不存在其中任何物件，還原期間會回報可忽略的錯誤訊息，除非同時指定了 `--if-exists`。

`-E encoding`<br>`--encoding=encoding`
:   以指定的字元集編碼建立傾印。預設情況下，傾印會以資料庫編碼建立。（取得相同結果的另一種方式，是將環境變數 `PGCLIENTENCODING` 設為所要的傾印編碼。）

`-f filename`<br>`--file=filename`
:   將輸出傳送到指定的檔案。若省略此選項，則使用標準輸出。

`-g`<br>`--globals-only`
:   只傾印全域物件（角色與資料表空間），不傾印資料庫。

`-O`<br>`--no-owner`
:   不輸出設定物件擁有權以符合原始資料庫的命令。預設情況下，pg_dumpall 會發出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 陳述式，以設定所建立之綱要元素的擁有權。除非腳本是由超級使用者（或擁有腳本中所有物件的同一個使用者）啟動，否則執行腳本時這些陳述式會失敗。若要產生任何使用者都可以還原、但會讓該使用者成為所有物件擁有者的腳本，請指定 `-O`。

`-r`<br>`--roles-only`
:   只傾印角色，不傾印資料庫或資料表空間。

`-s`<br>`--schema-only`
:   只傾印物件定義（綱要），不傾印資料。

`-S username`<br>`--superuser=username`
:   指定停用觸發程序時要使用的超級使用者名稱。只有在使用 `--disable-triggers` 時才有關係。（通常最好省略此選項，改為以超級使用者身分啟動產生的腳本。）

`-t`<br>`--tablespaces-only`
:   只傾印資料表空間，不傾印資料庫或角色。

`-v`<br>`--verbose`
:   指定詳細模式。這會使 pg_dumpall 將開始／結束時間輸出到傾印檔案中，並將進度訊息輸出到標準錯誤。重複指定此選項會使額外的除錯層級訊息出現在標準錯誤上。此選項也會傳遞給 pg_dump。

`-V`<br>`--version`
:   印出 pg_dumpall 的版本後結束。

`-x`<br>`--no-privileges`<br>`--no-acl`
:   不傾印存取權限（grant/revoke 命令）。

`--binary-upgrade`
:   此選項供就地升級工具程式使用。不建議也不支援將它用於其他用途。此選項的行為可能會在未來的版本中變更，恕不另行通知。

`--column-inserts`<br>`--attribute-inserts`
:   將資料傾印為帶有明確欄位名稱的 `INSERT` 命令（`INSERT INTO
    table
    (column, ...) VALUES
    ...`）。這會使還原變得非常慢；它主要用於產生可以載入非 PostgreSQL 資料庫的傾印。

`--disable-dollar-quoting`
:   此選項會停止對函式主體使用錢字號引用，並強制以 SQL 標準的字串語法為其加上引號。

`--disable-triggers`

此選項只在建立包含資料但不包含綱要的傾印時才有關係。它指示 pg_dumpall 加入在還原資料期間暫時停用目標資料表上觸發程序的命令。若你在資料表上有參照完整性檢查或其他觸發程序，而不想在資料還原期間呼叫它們，請使用此選項。

目前，為 `--disable-triggers` 所發出的命令必須以超級使用者身分執行。因此，你也應該使用 `-S` 指定超級使用者名稱，或者最好小心地以超級使用者身分啟動產生的腳本。

`--exclude-database=pattern`
:   不傾印名稱符合 *`pattern`* 的資料庫。可以寫多個 `--exclude-database` 開關來排除多個樣式。*`pattern`* 參數會依照與 psql 的 `\d` 命令相同的規則解讀為樣式（請參閱[樣式](app-psql.md#APP-PSQL-PATTERNS)），因此也可以在樣式中寫入萬用字元來排除多個資料庫。使用萬用字元時，若有需要，請小心為樣式加上引號，以防止 shell 展開萬用字元。

`--extra-float-digits=ndigits`
:   傾印浮點數資料時，使用指定的 extra_float_digits 值，而不是可用的最大精確度。為備份目的而進行的例行傾印不應該使用此選項。

`--filter=filename`

指定一個檔案，從中讀取要從傾印中排除之資料庫的樣式。這些樣式依照與 `--exclude-database` 相同的規則解讀。若要從 `STDIN` 讀取，請使用 `-` 作為檔名。`--filter` 選項可以與 `--exclude-database` 一起指定來排除資料庫，也可以指定超過一次以使用多個過濾檔案。

此檔案每一行列出一個資料庫樣式，格式如下：

```

    exclude database PATTERN
```

以 `#` 開頭的行會被視為註解並忽略。註解也可以放在物件樣式行之後。空白行也會被忽略。關於如何在樣式中加上引號，請參閱[樣式](app-psql.md#APP-PSQL-PATTERNS)。

`--if-exists`
:   在 `--clean` 模式中使用 `DROP ... IF EXISTS` 命令移除物件。這會抑制原本可能回報的「does not exist」錯誤。除非同時指定了 `--clean`，否則此選項無效。

`--inserts`
:   將資料傾印為 `INSERT` 命令（而不是 `COPY`）。這會使還原變得非常慢；它主要用於產生可以載入非 PostgreSQL 資料庫的傾印。請注意，若你重新排列了欄位順序，還原可能會完全失敗。`--column-inserts` 選項比較安全，但速度更慢。

`--load-via-partition-root`
:   傾印資料表分割區的資料時，讓 `COPY` 或 `INSERT` 陳述式以包含該分割區之分割階層的根為目標，而不是以分割區本身為目標。這會使載入資料時為每一筆資料列重新決定合適的分割區。在還原資料到某個伺服器、而資料列不一定會落入與原始伺服器上相同之分割區時，這可能很有用。舉例來說，若分割欄位的型別為 text，而兩個系統對用來排序分割欄位的定序有不同的定義，就可能發生這種情況。

`--lock-wait-timeout=timeout`
:   在傾印開始時，不要無限期地等待取得資料表的共享鎖。若無法在指定的 *`timeout`* 內鎖定資料表，則改為失敗。逾時值可以用 `SET
    statement_timeout` 所接受的任何格式指定。

`--no-comments`
:   不傾印 `COMMENT` 命令。

`--no-data`
:   不傾印資料。

`--no-policies`
:   不傾印資料列層級安全性政策。

`--no-publications`
:   不傾印發佈。

`--no-role-passwords`
:   不傾印角色的密碼。還原時，角色的密碼會是空值（null），在設定密碼之前，密碼驗證一律會失敗。由於指定此選項時不需要密碼值，角色資訊會從系統目錄檢視表 `pg_roles` 讀取，而不是從 `pg_authid` 讀取。因此，若對 `pg_authid` 的存取受到某些安全政策限制，此選項也會有幫助。

`--no-schema`
:   不傾印綱要（資料定義）。

`--no-security-labels`
:   不傾印安全標籤。

`--no-statistics`
:   不傾印統計資訊。這是預設行為。

`--no-subscriptions`
:   不傾印訂閱。

`--no-sync`
:   預設情況下，`pg_dumpall` 會等待所有檔案都安全地寫入磁碟。此選項會使 `pg_dumpall` 不等待就返回，這樣比較快，但表示之後若作業系統當機，可能使傾印損毀。一般而言，此選項適用於測試，但從正式環境的安裝傾印資料時不應該使用。

`--no-table-access-method`
:   不輸出選擇資料表存取方法的命令。使用此選項時，所有物件都會以還原期間預設的資料表存取方法建立。

`--no-tablespaces`
:   既不輸出建立資料表空間的命令，也不輸出為物件選擇資料表空間的命令。使用此選項時，所有物件都會建立在還原期間預設的資料表空間中。

`--no-toast-compression`
:   不輸出設定 TOAST 壓縮方法的命令。使用此選項時，所有欄位都會以預設的壓縮設定還原。

`--no-unlogged-table-data`
:   不傾印無日誌資料表的內容。此選項不影響是否傾印資料表定義（綱要）；它只會抑制傾印資料表資料。

`--on-conflict-do-nothing`
:   在 `INSERT` 命令中加上 `ON CONFLICT DO NOTHING`。除非同時指定了 `--inserts` 或 `--column-inserts`，否則此選項無效。

`--quote-all-identifiers`
:   強制為所有識別字加上引號。當從 PostgreSQL 主要版本與 pg_dumpall 不同的伺服器傾印資料庫，或輸出要載入到不同主要版本的伺服器時，建議使用此選項。預設情況下，pg_dumpall 只會為在其自身主要版本中屬於保留字的識別字加上引號。與其他版本的伺服器打交道時，由於保留字集合可能略有不同，這有時會造成相容性問題。使用 `--quote-all-identifiers` 可以避免這類問題，代價是傾印腳本較難閱讀。

`--restrict-key=restrict_key`

使用所提供的字串作為傾印輸出中 psql `\restrict` 的金鑰。若未指定 restrict 金鑰，pg_dumpall 會視需要產生一個隨機金鑰。金鑰只能包含英數字元。

此選項主要用於測試目的，以及其他需要可重現輸出的情境（例如比較傾印檔案）。不建議一般使用，因為事先知道金鑰的惡意伺服器，可能可以注入任意程式碼，而這些程式碼會在以 psql 執行傾印輸出的機器上被執行。

`--rows-per-insert=nrows`
:   將資料傾印為 `INSERT` 命令（而不是 `COPY`）。控制每個 `INSERT` 命令的最大資料列數。指定的值必須是大於零的數字。還原期間的任何錯誤，只會使屬於出問題之 `INSERT` 的資料列遺失，而不是整個資料表的內容。

`--statistics`
:   傾印最佳化器統計資訊。

`--statistics-only`
:   只傾印統計資訊，不傾印綱要（資料定義）或資料。會傾印資料表、具體化檢視表、外部資料表與索引的最佳化器統計資訊。

`--sequence-data`
:   在傾印中包含序列資料。這是預設行為，除非指定了 `--no-data`、`--schema-only` 或 `--statistics-only`。

`--use-set-session-authorization`
:   輸出符合 SQL 標準的 `SET SESSION AUTHORIZATION` 命令，而不是 `ALTER OWNER` 命令，來決定物件的擁有權。這會使傾印更符合標準，但依傾印中物件的歷史而定，可能無法正確還原。

`-?`<br>`--help`
:   顯示 pg_dumpall 命令列引數的說明後結束。

下列命令列選項控制資料庫連線參數。

`-d connstr`<br>`--dbname=connstr`

指定用來連線到伺服器的參數，形式為[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)；這些參數會覆寫任何相衝突的命令列選項。

為了與其他用戶端應用程式保持一致，此選項命名為 `--dbname`，但由於 pg_dumpall 需要連線到許多資料庫，連線字串中的資料庫名稱會被忽略。請使用 `-l` 選項指定初次連線所用的資料庫名稱，該連線會傾印全域物件，並找出還有哪些其他資料庫應該被傾印。

`-h host`<br>`--host=host`
:   指定資料庫伺服器執行所在機器的主機名稱。若值以斜線開頭，則會用作 Unix 網域通訊端的目錄。預設值取自環境變數 `PGHOST`（若有設定），否則會嘗試 Unix 網域通訊端連線。

`-l dbname`<br>`--database=dbname`
:   指定為了傾印全域物件並找出還有哪些其他資料庫應該被傾印而要連線的資料庫名稱。若未指定，會使用 `postgres` 資料庫；若該資料庫不存在，則會使用 `template1`。

`-p port`<br>`--port=port`
:   指定伺服器監聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。預設為環境變數 `PGPORT` 的值（若有設定），否則為編譯時內建的預設值。

`-U username`<br>`--username=username`
:   要用來連線的使用者名稱。

`-w`<br>`--no-password`
:   永不發出密碼提示。若伺服器要求密碼驗證，而無法透過 `.pgpass` 檔案等其他方式取得密碼，連線嘗試將會失敗。在沒有使用者在場輸入密碼的批次作業與腳本中，此選項可能很有用。

`-W`<br>`--password`

強制 pg_dumpall 在連線到資料庫之前提示輸入密碼。

此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_dumpall 會自動提示輸入密碼。不過，pg_dumpall 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

請注意，對每個要傾印的資料庫，密碼提示都會再出現一次。通常，設定一個 `~/.pgpass` 檔案會比依賴手動輸入密碼更好。

`--role=rolename`
:   指定建立傾印時要使用的角色名稱。此選項會使 pg_dumpall 在連線到資料庫之後發出 `SET ROLE` *`rolename`* 命令。當已驗證的使用者（以 `-U` 指定）缺少 pg_dumpall 所需的權限，但可以切換到具有所需權限的角色時，此選項很有用。某些安裝環境有禁止直接以超級使用者登入的政策，使用此選項可以在不違反該政策的情況下進行傾印。

<a id="id-1.9.4.15.7"></a>

## 環境

`PGHOST`<br>`PGOPTIONS`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式與大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.15.8"></a>

## 注意事項

由於 pg_dumpall 會在內部呼叫 pg_dump，某些診斷訊息會提到 pg_dump。

即使你打算將傾印腳本還原到全新的叢集，`--clean` 選項也可能有用。使用 `--clean` 會授權腳本移除並重新建立內建的 `postgres` 與 `template1` 資料庫，確保這些資料庫保有它們在來源叢集中相同的屬性（例如區域設定與編碼）。若不使用此選項，這些資料庫會保留它們現有的資料庫層級屬性，以及任何既有的內容。

指定 `--statistics` 時，`pg_dumpall` 會在產生的傾印檔案中包含大部分的最佳化器統計資訊。這並不包含所有統計資訊，例如以 [CREATE STATISTICS](../sql-commands/sql-createstatistics.md) 明確建立的統計資訊、由擴充功能加入的自訂統計資訊，或由累計統計系統收集的統計資訊。因此，從傾印檔案還原之後，對每個資料庫執行 `ANALYZE` 以確保最佳效能，可能仍然有用。你也可以執行 `vacuumdb -a
-z` 來分析所有資料庫。

不應該期望傾印腳本能完全無錯誤地執行。特別是，由於腳本會為來源叢集中存在的每個角色發出 `CREATE ROLE`，因此一定會對引導超級使用者（bootstrap superuser）得到「role already exists」錯誤，除非目的端叢集是以不同的引導超級使用者名稱初始化的。這個錯誤無害，應該忽略。使用 `--clean` 選項很可能會產生額外的、關於不存在物件的無害錯誤訊息，不過你可以加上 `--if-exists` 來將它們減到最少。

pg_dumpall 要求所有需要的資料表空間目錄在還原之前就已存在；否則，位於非預設位置之資料庫的建立將會失敗。

從 pg_dumpall 腳本還原資料庫時，一般建議使用 `-X`（`--no-psqlrc`）選項，以確保乾淨的還原過程，並避免與非預設的 psql 設定發生潛在衝突。此外，由於 pg_dumpall 腳本可能包含 psql 中繼命令，它可能與 psql 以外的用戶端不相容。

<a id="APP-PG-DUMPALL-EX"></a>

## 範例

若要傾印所有資料庫：

```

$ pg_dumpall > db.out
```

若要從此檔案還原資料庫，你可以使用：

```

$ psql -X -f db.out -d postgres
```

在這裡連線到哪個資料庫並不重要，因為 pg_dumpall 所建立的腳本檔案會包含建立並連線到所儲存資料庫的適當命令。例外的是，若你指定了 `--clean`，一開始就必須連線到 `postgres` 資料庫；腳本會立即嘗試移除其他資料庫，而對你所連線的資料庫，這項移除將會失敗。

<a id="id-1.9.4.15.10"></a>

## 另請參閱

關於可能的錯誤情況的詳細資訊，請查看 [pg_dump](app-pgdump.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pg-dumpall.html)（原文版本：18.6；核對日期：2026-10-09）
