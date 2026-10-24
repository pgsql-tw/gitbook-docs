<a id="APP-PGAMCHECK"></a><a id="id-1.9.4.9.1"></a>

## pg_amcheck

pg_amcheck — 檢查一個或多個 PostgreSQL 資料庫是否有毀損

<a id="id-1.9.4.9.4"></a>

## 語法

<a id="id-1.9.4.9.4.1"></a>

`pg_amcheck` [*`option`*...] [*`dbname`*]

<a id="id-1.9.4.9.5"></a>

## 說明

pg_amcheck 支援對一個或多個資料庫執行 [amcheck](../../appendixes/contrib/amcheck.md) 的毀損檢查函式，並提供選項來選擇要檢查哪些綱要、資料表與索引、要執行哪些種類的檢查、是否要平行執行檢查，以及若平行執行，要建立並使用多少個平行連線。

目前只支援一般資料表與 TOAST 資料表關聯、具體化檢視表、序列，以及 btree 索引。其他關聯類型會被默默略過。

若指定了 `dbname`，它應該是要檢查的單一資料庫名稱，且不應該出現其他資料庫選擇選項。否則，若出現任何資料庫選擇選項，所有符合的資料庫都會被檢查。若沒有出現這類選項，則會檢查預設資料庫。資料庫選擇選項包括 `--all`、`--database` 與 `--exclude-database`。它們也包括 `--relation`、`--exclude-relation`、`--table`、`--exclude-table`、`--index` 與 `--exclude-index`，但只限於這些選項搭配三段式樣式使用時（例如 `mydb*.myschema*.myrel*`）。最後，當 `--schema` 與 `--exclude-schema` 搭配兩段式樣式使用時（例如 `mydb*.myschema*`），它們也屬於資料庫選擇選項。

*`dbname`* 也可以是[連線字串](../../client-interfaces/libpq/libpq-connect.md#libpq-connstring)。

<a id="id-1.9.4.9.6"></a>

## 選項

下列命令列選項控制要檢查的對象：

`-a`<br>`--all`
:   檢查所有資料庫，但透過 `--exclude-database` 排除的資料庫除外。

`-d pattern`<br>`--database=pattern`
:   檢查符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的資料庫，但被 `--exclude-database` 排除的資料庫除外。此選項可以指定超過一次。

`-D pattern`<br>`--exclude-database=pattern`
:   排除符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的資料庫。此選項可以指定超過一次。

`-i pattern`<br>`--index=pattern`
:   檢查符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的索引，除非它們以其他方式被排除。此選項可以指定超過一次。

    這類似於 `--relation` 選項，差別在於它只適用於索引，而不適用於其他關聯類型。

`-I pattern`<br>`--exclude-index=pattern`
:   排除符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的索引。此選項可以指定超過一次。

    這類似於 `--exclude-relation` 選項，差別在於它只適用於索引，而不適用於其他關聯類型。

`-r pattern`<br>`--relation=pattern`
:   檢查符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的關聯，除非它們以其他方式被排除。此選項可以指定超過一次。

    樣式可以不加限定，例如 `myrel*`；也可以以綱要限定，例如 `myschema*.myrel*`；或同時以資料庫與綱要限定，例如 `mydb*.myschema*.myrel*`。以資料庫限定的樣式會將符合的資料庫加入要檢查的資料庫清單中。

`-R pattern`<br>`--exclude-relation=pattern`
:   排除符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的關聯。此選項可以指定超過一次。

    與 `--relation` 一樣，[*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 可以不加限定、以綱要限定，或同時以資料庫與綱要限定。

`-s pattern`<br>`--schema=pattern`
:   檢查符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 之綱要中的資料表與索引，除非它們以其他方式被排除。此選項可以指定超過一次。

    若只要選擇符合特定樣式之綱要中的資料表，可以考慮使用類似 `--table=SCHEMAPAT.* --no-dependent-indexes` 的寫法。若只要選擇索引，可以考慮使用類似 `--index=SCHEMAPAT.*` 的寫法。

    綱要樣式可以用資料庫限定。例如，你可以寫 `--schema=mydb*.myschema*`，以選擇在符合 `mydb*` 的資料庫中、符合 `myschema*` 的綱要。

`-S pattern`<br>`--exclude-schema=pattern`
:   排除符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 之綱要中的資料表與索引。此選項可以指定超過一次。

    與 `--schema` 一樣，此樣式可以用資料庫限定。

`-t pattern`<br>`--table=pattern`
:   檢查符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的資料表，除非它們以其他方式被排除。此選項可以指定超過一次。

    這類似於 `--relation` 選項，差別在於它只適用於資料表、具體化檢視表與序列，而不適用於索引。

`-T pattern`<br>`--exclude-table=pattern`
:   排除符合指定 [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS) 的資料表。此選項可以指定超過一次。

    這類似於 `--exclude-relation` 選項，差別在於它只適用於資料表、具體化檢視表與序列，而不適用於索引。

`--no-dependent-indexes`
:   預設情況下，若檢查某個資料表，該資料表的任何 btree 索引也會被檢查，即使它們並未被 `--index` 或 `--relation` 等選項明確選擇。此選項會抑制這種行為。

`--no-dependent-toast`
:   預設情況下，若檢查某個資料表，它的 TOAST 資料表（若有的話）也會被檢查，即使它並未被 `--table` 或 `--relation` 等選項明確選擇。此選項會抑制這種行為。

`--no-strict-names`
:   預設情況下，若 `--database`、`--table`、`--index` 或 `--relation` 的引數沒有符合任何物件，會是嚴重錯誤。此選項會將該錯誤降級為警告。

下列命令列選項控制資料表的檢查：

`--exclude-toast-pointers`
:   預設情況下，每當在資料表中遇到 TOAST 指標時，都會執行一次查找，以確保它參照的是 TOAST 資料表中看似有效的項目。這些檢查可能相當慢，可以使用此選項略過它們。

`--on-error-stop`
:   在回報資料表中發現毀損的第一個頁面上的所有毀損之後，停止處理該資料表關聯，並繼續處理下一個資料表或索引。

    請注意，索引檢查一律會在第一個毀損的頁面之後停止。此選項只對資料表關聯有意義。

`--skip=option`
:   若指定 `all-frozen`，資料表毀損檢查會略過所有資料表中被標示為全凍結的頁面。

    若指定 `all-visible`，資料表毀損檢查會略過所有資料表中被標示為全可見的頁面。

    預設情況下，不會略過任何頁面。可以將此選項指定為 `none`，但由於這是預設值，不需要特別寫出。

`--startblock=block`
:   從指定的區塊編號開始檢查。若被檢查的資料表關聯的區塊數少於這個數字，會發生錯誤。此選項不適用於索引，而且可能只在檢查單一資料表關聯時才有用。進一步的注意事項請參閱 `--endblock`。

`--endblock=block`
:   在指定的區塊編號結束檢查。若被檢查的資料表關聯的區塊數少於這個數字，會發生錯誤。此選項不適用於索引，而且可能只在檢查單一資料表關聯時才有用。若同時檢查一般資料表與 TOAST 資料表，此選項會套用到兩者，但在驗證 TOAST 指標時，編號較高的 TOAST 區塊仍可能被存取，除非使用 `--exclude-toast-pointers` 抑制了這項驗證。

下列命令列選項控制 B-tree 索引的檢查：

`--checkunique`
:   對每個受檢查且具有唯一限制條件的索引，使用 [amcheck](../../appendixes/contrib/amcheck.md) 的 `checkunique` 選項，驗證重複項目中在索引中可見的不超過一個。

`--heapallindexed`
:   對每個受檢查的索引，使用 [amcheck](../../appendixes/contrib/amcheck.md) 的 `heapallindexed` 選項，驗證所有堆積 tuple 都以索引 tuple 的形式存在於索引中。

`--parent-check`
:   對每個受檢查的 btree 索引，使用 [amcheck](../../appendixes/contrib/amcheck.md) 的 `bt_index_parent_check` 函式，它會在索引檢查期間對父／子關係執行額外的檢查。

    預設是使用 amcheck 的 `bt_index_check` 函式，但請注意，使用 `--rootdescend` 選項會隱含地選擇 `bt_index_parent_check`。

`--rootdescend`
:   對每個受檢查的索引，使用 [amcheck](../../appendixes/contrib/amcheck.md) 的 `rootdescend` 選項，為每個 tuple 從根頁面執行一次新的搜尋，以在葉層級重新找到 tuple。

    使用此選項也會隱含地選擇 `--parent-check` 選項。

    這種驗證形式最初是為了協助開發 btree 索引功能而撰寫的。在協助偵測實務上會發生的各種毀損方面，它可能用處有限，甚至毫無用處。它也可能使毀損檢查花費比原本長得多的時間，並在伺服器上耗用比原本多得多的資源。

<a id="id-1.9.4.9.6.8"></a>

### 警告

指定 `--parent-check` 選項或 `--rootdescend` 選項時，對 B-tree 索引所執行的額外檢查需要相對較強的關聯層級鎖定。這些檢查是唯一會阻擋 `INSERT`、`UPDATE` 與 `DELETE` 命令所進行之並行資料修改的檢查。

下列命令列選項控制與伺服器的連線：

`-h hostname`<br>`--host=hostname`
:   指定伺服器執行所在機器的主機名稱。若值以斜線開頭，則會用作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器監聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。

`-U`<br>`--username=username`
:   要用來連線的使用者名稱。

`-w`<br>`--no-password`
:   永不發出密碼提示。若伺服器要求密碼驗證，而無法透過 `.pgpass` 檔案等其他方式取得密碼，連線嘗試將會失敗。在沒有使用者在場輸入密碼的批次作業與腳本中，此選項可能很有用。

`-W`<br>`--password`
:   強制 pg_amcheck 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_amcheck 會自動提示輸入密碼。不過，pg_amcheck 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--maintenance-db=dbname`
:   指定用來找出要檢查之資料庫清單的資料庫或[連線字串](../../client-interfaces/libpq/libpq-connect.md#libpq-connstring)。若既未使用 `--all`，也未使用任何包含資料庫樣式的選項，就不需要這個連線，此選項也不會有任何作用。否則，此選項的值中所包含的資料庫名稱以外的任何連線字串參數，也會在連線到被檢查的資料庫時使用。若省略此選項，預設為 `postgres`，若連線失敗，則為 `template1`。

另外也提供其他選項：

`-e`<br>`--echo`
:   將所有送往伺服器的 SQL 回顯到 stdout。

`-j num`<br>`--jobs=num`
:   對伺服器使用 *`num`* 個並行連線，或每個要檢查的物件一個連線，以兩者中較少者為準。

    預設是使用單一連線。

`-P`<br>`--progress`
:   顯示進度資訊。進度資訊包括已完成檢查的關聯數量，以及這些關聯的總大小。它也包括最終將被檢查的關聯總數，以及這些關聯的估計大小。

`-v`<br>`--verbose`
:   印出更多訊息。特別是，這會為每個被檢查的關聯印出一則訊息，並提高伺服器錯誤所顯示的詳細程度。

`-V`<br>`--version`
:   印出 pg_amcheck 的版本後結束。

`--install-missing`<br>`--install-missing=schema`
:   安裝檢查資料庫所需但缺少的任何擴充功能。若尚未安裝，每個擴充功能的物件會安裝到指定的 *`schema`* 中，若未指定，則安裝到綱要 `pg_catalog` 中。

    目前唯一需要的擴充功能是 [amcheck](../../appendixes/contrib/amcheck.md)。

`-?`<br>`--help`
:   顯示 pg_amcheck 命令列引數的說明後結束。

<a id="id-1.9.4.9.7"></a>

## 環境

`pg_amcheck` 與大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.9.8"></a>

## 注意事項

pg_amcheck 設計為搭配 PostgreSQL 14.0 及以後的版本使用。

<a id="id-1.9.4.9.9"></a>

## 另請參閱

[amcheck](../../appendixes/contrib/amcheck.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgamcheck.html)（原文版本：18.6；核對日期：2026-10-10）
