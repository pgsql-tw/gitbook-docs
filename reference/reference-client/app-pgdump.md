<a id="APP-PGDUMP"></a><a id="id-1.9.4.14.1"></a>

## pg_dump

pg_dump — 將 PostgreSQL 資料庫匯出為 SQL 腳本或其他格式

<a id="id-1.9.4.14.4"></a>

## 語法

<a id="id-1.9.4.14.4.1"></a>

`pg_dump` [*`connection-option`*...] [*`option`*...] [*`dbname`*]

<a id="PG-DUMP-DESCRIPTION"></a>

## 說明

pg_dump 是用來匯出 PostgreSQL 資料庫的工具程式。即使資料庫正被並行使用，它也能產生一致的匯出結果。pg_dump 不會阻擋其他存取資料庫的使用者（無論是讀取者或寫入者）。不過請注意，除了簡單的情況之外，pg_dump 通常不是對正式環境資料庫進行定期備份的正確選擇。進一步的討論請參閱[第 25 章](../../server-administration/backup/README.md)。

pg_dump 只會傾印單一資料庫。若要匯出整個叢集，或匯出叢集中所有資料庫共用的全域物件（例如角色與資料表空間），請使用 [pg_dumpall](app-pg-dumpall.md)。

傾印可以輸出為腳本或封存檔格式。腳本傾印是純文字檔案，內含將資料庫重建為儲存當時狀態所需的 SQL 命令。若要從這種腳本還原，請將它餵給 [psql](app-psql.md)。腳本檔案甚至可以用來在其他機器與其他架構上重建資料庫；經過一些修改後，甚至可以用在其他 SQL 資料庫產品上。

其他的封存檔格式必須搭配 [pg_restore](app-pgrestore.md) 使用才能重建資料庫。這些格式讓 pg_restore 可以選擇要還原的內容，甚至可以在還原之前重新排列項目的順序。封存檔格式的設計可以在不同架構之間移植。

當使用其中一種封存檔格式並與 pg_restore 結合時，pg_dump 提供了一套彈性的封存與傳輸機制。pg_dump 可以用來匯出整個資料庫，接著可以用 pg_restore 檢視封存內容，以及／或選擇要還原資料庫的哪些部分。最具彈性的輸出檔案格式是「custom」格式（`-Fc`）與「directory」格式（`-Fd`）。它們允許選擇所有封存項目並重新排列其順序、支援平行還原，而且預設會壓縮。「directory」格式是唯一支援平行傾印的格式。

執行 pg_dump 時，應該檢查輸出中是否有任何警告（印在標準錯誤上），特別是考量到下文所列的限制。

<a id="PG-DUMP-DESCRIPTION-WARNING"></a>

### 警告

還原傾印會使目的端執行由來源端超級使用者所選擇的任意程式碼。部分傾印與部分還原並不會限制這一點。若來源端的超級使用者不受信任，就必須在還原之前檢查傾印出的 SQL 陳述式。非純文字的傾印可以使用 pg_restore 的 `--file` 選項來檢查。請注意，執行傾印與還原的用戶端不需要信任來源端或目的端的超級使用者。

<a id="PG-DUMP-OPTIONS"></a>

## 選項

下列命令列選項控制輸出的內容與格式。

*`dbname`*
:   指定要傾印的資料庫名稱。若未指定，則使用環境變數 `PGDATABASE`。若該變數也未設定，則使用連線時指定的使用者名稱。

`-a`<br>`--data-only`
:   只傾印資料，不傾印綱要（資料定義）或統計資訊。會傾印資料表資料、大型物件與序列值。

    此選項類似於指定 `--section=data`，但基於歷史因素並不完全相同。

`-b`<br>`--large-objects`<br>`--blobs`（已棄用）
:   在傾印中包含大型物件。這是預設行為，除非指定了 `--schema`、`--table`、`--schema-only`、`--statistics-only` 或 `--no-data`。因此 `-b` 選項只在已要求特定綱要或資料表的傾印中加入大型物件時才有用。請注意，大型物件被視為資料，因此使用 `--data-only` 時會被包含，但使用 `--schema-only` 或 `--statistics-only` 時則不會。

`-B`<br>`--no-large-objects`<br>`--no-blobs`（已棄用）
:   在傾印中排除大型物件。

    同時指定 `-b` 與 `-B` 時，行為是在傾印資料時輸出大型物件，請參閱 `-b` 的說明。

`-c`<br>`--clean`
:   在輸出建立資料庫物件的命令之前，先輸出 `DROP` 所有被傾印之資料庫物件的命令。當還原要覆寫現有資料庫時，這個選項很有用。若目的端資料庫中不存在其中任何物件，還原期間會回報可忽略的錯誤訊息，除非同時指定了 `--if-exists`。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`-C`<br>`--create`
:   在輸出的開頭加上建立資料庫本身並重新連線到所建立之資料庫的命令。（使用這種形式的腳本時，執行腳本之前連線到目的端安裝中的哪個資料庫都無所謂。）若同時指定了 `--clean`，腳本會在重新連線到目標資料庫之前，先移除並重新建立它。

    使用 `--create` 時，輸出還會包含資料庫的註解（若有的話），以及此資料庫專屬的任何組態變數設定，也就是任何提到此資料庫的 `ALTER DATABASE ... SET ...` 與 `ALTER ROLE ... IN DATABASE ... SET ...` 命令。資料庫本身的存取權限也會被傾印，除非指定了 `--no-acl`。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`-e pattern`<br>`--extension=pattern`
:   只傾印符合 *`pattern`* 的擴充功能。未指定此選項時，會傾印目標資料庫中所有的非系統擴充功能。可以寫多個 `-e` 選項來選擇多個擴充功能。*`pattern`* 參數會依照 psql 的 `\d` 命令所使用的相同規則解譯為模式（請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)），因此也可以在模式中寫入萬用字元來選擇多個擴充功能。使用萬用字元時，必要時請小心為模式加上引號，以免 shell 展開萬用字元。

    若某個擴充功能經由 `--extension` 指定，則由 `pg_extension_config_dump` 註冊的任何該擴充功能之組態關聯都會包含在傾印中。

    <a id="id-1.9.4.14.6.3.7.2.3"></a>

    ### 注意

    指定 `-e` 時，pg_dump 不會嘗試傾印所選擴充功能可能相依的任何其他資料庫物件。因此，無法保證特定擴充功能傾印的結果能單獨成功還原到乾淨的資料庫中。

`-E encoding`<br>`--encoding=encoding`
:   以指定的字元集編碼建立傾印。預設情況下，傾印會以資料庫編碼建立。（取得相同結果的另一種方式，是將環境變數 `PGCLIENTENCODING` 設為所要的傾印編碼。）支援的編碼說明於[第 23.3.1 節](../../server-administration/charset/multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)。

`-f file`<br>`--file=file`
:   將輸出送到指定的檔案。對於以檔案為基礎的輸出格式，可以省略此參數，此時會使用標準輸出。不過對於 directory 輸出格式則必須指定此參數，此時它指定的是目標目錄而不是檔案。在這種情況下，目錄由 `pg_dump` 建立，而且事先必須不存在。

`-F format`<br>`--format=format`
:   選擇輸出的格式。*`format`* 可以是下列其中之一：

    `p`<br>`plain`
    :   輸出純文字的 SQL 腳本檔案（預設）。

    `c`<br>`custom`
    :   輸出適合作為 pg_restore 輸入的 custom 格式封存檔。它與 directory 輸出格式同為最具彈性的輸出格式，因為它允許在還原期間手動選擇封存項目並重新排列其順序。此格式預設也會壓縮。

    `d`<br>`directory`
    :   輸出適合作為 pg_restore 輸入的 directory 格式封存檔。這會建立一個目錄，其中每個被傾印的資料表與大型物件各有一個檔案，另外還有一個所謂的目錄（Table of Contents）檔案，以 pg_restore 可以讀取的機器可讀格式描述被傾印的物件。directory 格式的封存檔可以用標準的 Unix 工具處理；例如，未壓縮封存檔中的檔案可以用 gzip、lz4 或 zstd 工具壓縮。此格式預設使用 `gzip` 壓縮，而且也支援平行傾印。

    `t`<br>`tar`
    :   輸出適合作為 pg_restore 輸入的 `tar` 格式封存檔。tar 格式與 directory 格式相容：解開 tar 格式的封存檔會產生有效的 directory 格式封存檔。不過，tar 格式不支援壓縮。此外，使用 tar 格式時，還原期間無法變更資料表資料項目的相對順序。

`-j njobs`<br>`--jobs=njobs`
:   以同時傾印 *`njobs`* 個資料表的方式平行執行傾印。此選項可能會縮短執行傾印所需的時間，但也會增加資料庫伺服器的負載。你只能在 directory 輸出格式中使用此選項，因為這是唯一能讓多個程序同時寫入資料的輸出格式。

    pg_dump 會開啟 *`njobs`* + 1 個資料庫連線，因此請確認你的 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 設定夠高，足以容納所有連線。

    在執行平行傾印時，對資料庫物件要求排他鎖可能會導致傾印失敗。原因是 pg_dump 的領導程序會對工作程序稍後要傾印的物件要求共享鎖（[ACCESS SHARE](../../the-sql-language/mvcc/explicit-locking.md#LOCKING-TABLES)），以確保在傾印執行期間沒有人刪除它們而使它們消失。若此時另一個用戶端對某個資料表要求排他鎖，該鎖不會被授予，而是會排入佇列，等待領導程序的共享鎖被釋放。因此，對該資料表的任何其他存取也都不會被授予，而會排在該排他鎖要求之後。這也包括試圖傾印該資料表的工作程序。若不採取任何預防措施，這就會是典型的死結情況。為了偵測這種衝突，pg_dump 的工作程序會使用 `NOWAIT` 選項再要求一個共享鎖。若工作程序未被授予此共享鎖，表示必定有其他人在此期間要求了排他鎖，傾印無法繼續進行，因此 pg_dump 別無選擇，只能中止傾印。

    若要執行平行傾印，資料庫伺服器必須支援同步快照；這項功能對主要伺服器而言是在 PostgreSQL 9.2 引入，對待命伺服器則是在 10 版引入。有了這項功能，資料庫用戶端即使使用不同的連線，也能確保看到相同的資料集。`pg_dump -j` 會使用多個資料庫連線；它以領導程序連線到資料庫一次，並為每個工作者作業再各連線一次。若沒有同步快照功能，就無法保證不同的工作者作業在各個連線中看到相同的資料，這可能導致備份不一致。

`-n pattern`<br>`--schema=pattern`
:   只傾印符合 *`pattern`* 的綱要；這會同時選擇綱要本身及其包含的所有物件。未指定此選項時，會傾印目標資料庫中所有的非系統綱要。可以寫多個 `-n` 選項來選擇多個綱要。*`pattern`* 參數會依照 psql 的 `\d` 命令所使用的相同規則解譯為模式（請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)），因此也可以在模式中寫入萬用字元來選擇多個綱要。使用萬用字元時，必要時請小心為模式加上引號，以免 shell 展開萬用字元；請參閱下文的[範例](app-pgdump.md#PG-DUMP-EXAMPLES)。

    <a id="id-1.9.4.14.6.3.12.2.2"></a>

    ### 注意

    指定 `-n` 時，pg_dump 不會嘗試傾印所選綱要可能相依的任何其他資料庫物件。因此，無法保證特定綱要傾印的結果能單獨成功還原到乾淨的資料庫中。

    <a id="id-1.9.4.14.6.3.12.2.3"></a>

    ### 注意

    指定 `-n` 時，不會傾印大型物件之類的非綱要物件。你可以使用 `--large-objects` 選項把大型物件加回傾印中。

`-N pattern`<br>`--exclude-schema=pattern`
:   不傾印任何符合 *`pattern`* 的綱要。此模式的解譯規則與 `-n` 相同。`-N` 可以指定超過一次，以排除符合數個模式中任一個的綱要。

    同時指定 `-n` 與 `-N` 時，行為是只傾印至少符合一個 `-n` 選項、但不符合任何 `-N` 選項的綱要。若 `-N` 出現而沒有 `-n`，則符合 `-N` 的綱要會從原本的一般傾印中排除。

`-O`<br>`--no-owner`
:   不輸出設定物件擁有權以符合原始資料庫的命令。預設情況下，pg_dump 會發出 `ALTER OWNER` 或 `SET SESSION AUTHORIZATION` 陳述式，以設定所建立之資料庫物件的擁有權。除非腳本是由超級使用者（或擁有腳本中所有物件的同一個使用者）啟動，否則執行腳本時這些陳述式會失敗。若要產生任何使用者都可以還原、但會讓該使用者成為所有物件擁有者的腳本，請指定 `-O`。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`-R`<br>`--no-reconnect`
:   此選項已過時，但為了向後相容性仍然接受。

`-s`<br>`--schema-only`
:   只傾印物件定義（綱要），不傾印資料或統計資訊。

    此選項不能與 `--data-only` 或 `--statistics-only` 一起使用。它類似於指定 `--section=pre-data --section=post-data`，但基於歷史因素並不完全相同。

    （請勿將此選項與 `--schema` 選項混淆，後者使用的「schema」一詞是另一種意義。）

    若只要排除資料庫中部分資料表的資料，請參閱 `--exclude-table-data`。

`-S username`<br>`--superuser=username`
:   指定停用觸發程序時要使用的超級使用者名稱。只有在使用 `--disable-triggers` 時才有關係。（通常最好省略此選項，改為以超級使用者身分啟動產生的腳本。）

`-t pattern`<br>`--table=pattern`
:   只傾印名稱符合 *`pattern`* 的資料表。可以寫多個 `-t` 選項來選擇多個資料表。*`pattern`* 參數會依照 psql 的 `\d` 命令所使用的相同規則解譯為模式（請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)），因此也可以在模式中寫入萬用字元來選擇多個資料表。使用萬用字元時，必要時請小心為模式加上引號，以免 shell 展開萬用字元；請參閱下文的[範例](app-pgdump.md#PG-DUMP-EXAMPLES)。

    除了資料表之外，此選項也可以用來傾印符合之檢視表、具體化檢視表、外部資料表與序列的定義。它不會傾印檢視表或具體化檢視表的內容，而外部資料表的內容只有在以 `--include-foreign-data` 指定了對應的外部伺服器時才會被傾印。

    使用 `-t` 時，`-n` 與 `-N` 選項沒有作用，因為無論這些選項為何，以 `-t` 選擇的資料表都會被傾印，而非資料表物件則不會被傾印。

    <a id="id-1.9.4.14.6.3.18.2.4"></a>

    ### 注意

    指定 `-t` 時，pg_dump 不會嘗試傾印所選資料表可能相依的任何其他資料庫物件。因此，無法保證特定資料表傾印的結果能單獨成功還原到乾淨的資料庫中。

`-T pattern`<br>`--exclude-table=pattern`
:   不傾印任何符合 *`pattern`* 的資料表。此模式的解譯規則與 `-t` 相同。`-T` 可以指定超過一次，以排除符合數個模式中任一個的資料表。

    同時指定 `-t` 與 `-T` 時，行為是只傾印至少符合一個 `-t` 選項、但不符合任何 `-T` 選項的資料表。若 `-T` 出現而沒有 `-t`，則符合 `-T` 的資料表會從原本的一般傾印中排除。

`-v`<br>`--verbose`
:   指定詳細模式。這會使 pg_dump 將詳細的物件註解與開始／結束時間輸出到傾印檔案中，並將進度訊息輸出到標準錯誤。重複指定此選項會使額外的除錯層級訊息出現在標準錯誤上。

`-V`<br>`--version`
:   印出 pg_dump 的版本後結束。

`-x`<br>`--no-privileges`<br>`--no-acl`
:   不傾印存取權限（grant/revoke 命令）。

`-Z level`<br>`-Z method`[:*`detail`*]<br>`--compress=level`<br>`--compress=method`[:*`detail`*]
:   指定要使用的壓縮方法和／或壓縮層級。壓縮方法可以設為 `gzip`、`lz4`、`zstd`，或設為 `none` 表示不壓縮。可以選擇性地指定壓縮細節字串。若細節字串是整數，它指定的是壓縮層級。否則，它應該是以逗號分隔的項目清單，每個項目的形式為 `keyword` 或 `keyword=value`。目前支援的關鍵字為 `level` 與 `long`。

    若未指定壓縮層級，將使用預設的壓縮層級。若只指定層級而沒有提到演算法，則層級大於 `0` 時會使用 `gzip` 壓縮，層級為 `0` 時則不壓縮。

    對於 custom 與 directory 封存格式，這指定的是個別資料表資料區段的壓縮，預設是以中等層級使用 `gzip` 壓縮。對於純文字輸出，設定非零的壓縮層級會使整個輸出檔案被壓縮，就如同將它送入 gzip、lz4 或 zstd 處理一樣；但預設是不壓縮。使用 zstd 壓縮時，`long` 模式可能會提高壓縮率，代價是記憶體用量增加。

    tar 封存格式目前完全不支援壓縮。

`--binary-upgrade`
:   此選項供就地升級工具程式使用。不建議也不支援將它用於其他用途。此選項的行為可能會在未來的版本中變更，恕不另行通知。

`--column-inserts`<br>`--attribute-inserts`
:   將資料傾印為帶有明確欄位名稱的 `INSERT` 命令（`INSERT INTO
    table
    (column, ...) VALUES
    ...`）。這會使還原變得非常慢；它主要用於產生可以載入非 PostgreSQL 資料庫的傾印。還原期間的任何錯誤，只會使屬於出問題之 `INSERT` 的資料列遺失，而不是整個資料表的內容。

`--disable-dollar-quoting`
:   此選項會停止對函式主體使用錢字號引用，並強制以 SQL 標準的字串語法為其加上引號。

`--disable-triggers`
:   此選項只在建立包含資料但不包含綱要的傾印時才有關係。它指示 pg_dump 加入在還原資料期間暫時停用目標資料表上觸發程序的命令。若你在資料表上有參照完整性檢查或其他觸發程序，而不想在資料還原期間呼叫它們，請使用此選項。

    目前，為 `--disable-triggers` 所發出的命令必須以超級使用者身分執行。因此，你也應該使用 `-S` 指定超級使用者名稱，或者最好小心地以超級使用者身分啟動產生的腳本。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`--enable-row-security`
:   此選項只在傾印具有資料列安全性之資料表的內容時才有關係。預設情況下，pg_dump 會將 [row_security](../../server-administration/runtime-config/runtime-config-client.md#GUC-ROW-SECURITY) 設為 off，以確保傾印資料表中的所有資料。若使用者沒有足夠的權限繞過資料列安全性，就會擲出錯誤。此參數指示 pg_dump 改為將 [row_security](../../server-administration/runtime-config/runtime-config-client.md#GUC-ROW-SECURITY) 設為 on，讓使用者可以傾印資料表內容中其有權存取的部分。

    請注意，若你目前使用此選項，你可能也會希望傾印採用 `INSERT` 格式，因為還原期間的 `COPY FROM` 不支援資料列安全性。

`--exclude-extension=pattern`
:   不傾印任何符合 *`pattern`* 的擴充功能。此模式的解譯規則與 `-e` 相同。`--exclude-extension` 可以指定超過一次，以排除符合數個模式中任一個的擴充功能。

    同時指定 `-e` 與 `--exclude-extension` 時，行為是只傾印至少符合一個 `-e` 選項、但不符合任何 `--exclude-extension` 選項的擴充功能。若 `--exclude-extension` 出現而沒有 `-e`，則符合 `--exclude-extension` 的擴充功能會從原本的一般傾印中排除。

`--exclude-table-and-children=pattern`
:   此選項與 `-T`/`--exclude-table` 選項相同，只是它還會排除符合 *`pattern`* 之資料表的任何分割區或繼承子資料表。

`--exclude-table-data=pattern`
:   不傾印任何符合 *`pattern`* 之資料表的資料。此模式的解譯規則與 `-t` 相同。`--exclude-table-data` 可以指定超過一次，以排除符合數個模式中任一個的資料表。當你需要某個資料表的定義，但不需要其中的資料時，此選項很有用。

    若要排除資料庫中所有資料表的資料，請參閱 `--schema-only` 或 `--statistics-only`。

`--exclude-table-data-and-children=pattern`
:   此選項與 `--exclude-table-data` 選項相同，只是它還會排除符合 *`pattern`* 之資料表的任何分割區或繼承子資料表的資料。

`--extra-float-digits=ndigits`
:   傾印浮點數資料時，使用指定的 `extra_float_digits` 值，而不是可用的最大精確度。為備份目的而進行的例行傾印不應該使用此選項。

`--filter=filename`
:   指定一個檔名，從中讀取要在傾印中包含或排除之物件的模式。這些模式的解譯規則與對應的選項相同：資料表為 `-t`/`--table`、`--table-and-children`、`-T`/`--exclude-table` 與 `--exclude-table-and-children`；綱要為 `-n`/`--schema` 與 `-N`/`--exclude-schema`；外部伺服器上的資料為 `--include-foreign-data`；資料表資料為 `--exclude-table-data` 與 `--exclude-table-data-and-children`；擴充功能為 `-e`/`--extension` 與 `--exclude-extension`。若要從 `STDIN` 讀取，請使用 `-` 作為檔名。`--filter` 選項可以與上列用來包含或排除物件的選項一起指定，也可以為多個過濾檔案指定超過一次。

    此檔案每一列列出一個物件模式，格式如下：

    ```

    { include | exclude } { extension | foreign_data | table | table_and_children | table_data | table_data_and_children | schema } PATTERN
    ```

    第一個關鍵字指定符合該模式的物件是要包含還是排除。第二個關鍵字指定要以該模式過濾的物件類型：

    * `extension`：擴充功能。作用如同 `-e`/`--extension` 或 `--exclude-extension` 選項。
    * `foreign_data`：外部伺服器上的資料。作用如同 `--include-foreign-data` 選項。此關鍵字只能與 `include` 關鍵字一起使用。
    * `table`：資料表。作用如同 `-t`/`--table` 或 `-T`/`--exclude-table` 選項。
    * `table_and_children`：資料表，包括其任何分割區或繼承子資料表。作用如同 `--table-and-children` 或 `--exclude-table-and-children` 選項。
    * `table_data`：符合 *`pattern`* 之任何資料表的資料表資料。作用如同 `--exclude-table-data` 選項。此關鍵字只能與 `exclude` 關鍵字一起使用。
    * `table_data_and_children`：符合 *`pattern`* 之任何資料表的資料表資料，以及這些資料表之任何分割區或繼承子資料表的資料表資料。作用如同 `--exclude-table-data-and-children` 選項。此關鍵字只能與 `exclude` 關鍵字一起使用。
    * `schema`：綱要。作用如同 `-n`/`--schema` 或 `-N`/`--exclude-schema` 選項。

    以 `#` 開頭的行會被視為註解而忽略。註解也可以放在物件模式那一列的後面。空白行同樣會被忽略。關於如何在模式中使用引號，請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)。

    範例檔案列於下文的[範例](app-pgdump.md#PG-DUMP-EXAMPLES)一節。

`--if-exists`
:   在 `--clean` 模式中使用 `DROP ... IF EXISTS` 命令移除物件。這會抑制原本可能回報的「does not exist」錯誤。除非同時指定了 `--clean`，否則此選項無效。

`--include-foreign-data=foreignserver`
:   傾印外部伺服器符合 *`foreignserver`* 模式之任何外部資料表的資料。可以寫多個 `--include-foreign-data` 選項來選擇多個外部伺服器。此外，*`foreignserver`* 參數會依照 psql 的 `\d` 命令所使用的相同規則解譯為模式（請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)），因此也可以在模式中寫入萬用字元來選擇多個外部伺服器。使用萬用字元時，必要時請小心為模式加上引號，以免 shell 展開萬用字元；請參閱下文的[範例](app-pgdump.md#PG-DUMP-EXAMPLES)。唯一的例外是不允許空的模式。

    <a id="id-1.9.4.14.6.3.36.2.2"></a>

    ### 注意

    在 `--include-foreign-data` 中使用萬用字元，可能會存取到非預期的外部伺服器。此外，若要安全地使用此選項，請確認所指定的伺服器必須有受信任的擁有者。

    <a id="id-1.9.4.14.6.3.36.2.3"></a>

    ### 注意

    指定 `--include-foreign-data` 時，pg_dump 不會檢查外部資料表是否可寫入。因此，無法保證外部資料表傾印的結果能成功還原。

`--inserts`
:   將資料傾印為 `INSERT` 命令（而不是 `COPY`）。這會使還原變得非常慢；它主要用於產生可以載入非 PostgreSQL 資料庫的傾印。還原期間的任何錯誤，只會使屬於出問題之 `INSERT` 的資料列遺失，而不是整個資料表的內容。請注意，若你重新排列了欄位順序，還原可能會完全失敗。`--column-inserts` 選項不受欄位順序變更的影響，但速度更慢。

`--load-via-partition-root`
:   傾印資料表分割區的資料時，讓 `COPY` 或 `INSERT` 陳述式以包含該分割區之分割階層的根為目標，而不是以分割區本身為目標。這會使載入資料時為每一筆資料列重新決定合適的分割區。在還原資料到某個伺服器、而資料列不一定會落入與原始伺服器上相同之分割區時，這可能很有用。舉例來說，若分割欄位的型別為 text，而兩個系統對用來排序分割欄位的定序有不同的定義，就可能發生這種情況。

`--lock-wait-timeout=timeout`
:   在傾印開始時，不要無限期地等待取得資料表的共享鎖。若無法在指定的 *`timeout`* 內鎖定資料表，則改為失敗。逾時值可以用 `SET
    statement_timeout` 所接受的任何格式指定。（允許的格式依你所傾印之伺服器的版本而不同，但所有版本都接受以毫秒為單位的整數。）

`--no-comments`
:   不傾印 `COMMENT` 命令。

`--no-data`
:   不傾印資料。

`--no-policies`
:   不傾印資料列層級安全性政策。

`--no-publications`
:   不傾印發佈。

`--no-schema`
:   不傾印綱要（資料定義）。

`--no-security-labels`
:   不傾印安全標籤。

`--no-statistics`
:   不傾印統計資訊。這是預設行為。

`--no-subscriptions`
:   不傾印訂閱。

`--no-sync`
:   預設情況下，`pg_dump` 會等待所有檔案都安全地寫入磁碟。此選項會使 `pg_dump` 不等待就返回，這樣比較快，但表示之後若作業系統當機，可能使傾印損毀。一般而言，此選項適用於測試，但從正式環境的安裝傾印資料時不應該使用。

`--no-table-access-method`
:   不輸出選擇資料表存取方法的命令。使用此選項時，所有物件都會以還原期間預設的資料表存取方法建立。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`--no-tablespaces`
:   不輸出選擇資料表空間的命令。使用此選項時，所有物件都會建立在還原期間預設的資料表空間中。

    輸出封存（非文字）檔案時會忽略此選項。對於封存格式，你可以在呼叫 `pg_restore` 時指定此選項。

`--no-toast-compression`
:   不輸出設定 TOAST 壓縮方法的命令。使用此選項時，所有欄位都會以預設的壓縮設定還原。

`--no-unlogged-table-data`
:   不傾印無日誌資料表與序列的內容。此選項不影響是否傾印資料表與序列的定義（綱要）；它只會抑制傾印資料表與序列的資料。從待命伺服器傾印時，無日誌資料表與序列中的資料一律會被排除。

`--on-conflict-do-nothing`
:   在 `INSERT` 命令中加上 `ON CONFLICT DO NOTHING`。除非同時指定了 `--inserts`、`--column-inserts` 或 `--rows-per-insert`，否則此選項無效。

`--quote-all-identifiers`
:   強制為所有識別字加上引號。當從 PostgreSQL 主要版本與 pg_dump 不同的伺服器傾印資料庫，或輸出要載入到不同主要版本的伺服器時，建議使用此選項。預設情況下，pg_dump 只會為在其自身主要版本中屬於保留字的識別字加上引號。與其他版本的伺服器打交道時，由於保留字集合可能略有不同，這有時會造成相容性問題。使用 `--quote-all-identifiers` 可以避免這類問題，代價是傾印腳本較難閱讀。

`--restrict-key=restrict_key`
:   在傾印輸出中使用所提供的字串作為 psql 的 `\restrict` 金鑰。只有純文字傾印才能指定此選項，也就是 `--format` 設為 `plain` 或省略 `--format` 選項時。若未指定 restrict 金鑰，pg_dump 會視需要產生一個隨機金鑰。金鑰只能包含英數字元。

    此選項主要用於測試目的，以及其他需要可重現輸出的情境（例如比較傾印檔案）。不建議一般使用，因為事先知道金鑰的惡意伺服器，可能可以注入任意程式碼，並在以 psql 執行該傾印輸出的機器上執行。

`--rows-per-insert=nrows`
:   將資料傾印為 `INSERT` 命令（而不是 `COPY`）。控制每個 `INSERT` 命令的最大資料列數。指定的值必須是大於零的數字。還原期間的任何錯誤，只會使屬於出問題之 `INSERT` 的資料列遺失，而不是整個資料表的內容。

`--section=sectionname`
:   只傾印指定的區段。區段名稱可以是 `pre-data`、`data` 或 `post-data`。此選項可以指定超過一次以選擇多個區段。預設是傾印所有區段。

    data 區段包含實際的資料表資料、大型物件內容、序列值，以及資料表、具體化檢視表與外部資料表的統計資訊。post-data 項目包括索引、觸發程序、規則的定義，索引的統計資訊，以及已驗證之檢查限制條件與非空值限制條件以外的限制條件。pre-data 項目包括所有其他的資料定義項目。

`--sequence-data`
:   在傾印中包含序列資料。這是預設行為，除非指定了 `--no-data`、`--schema-only` 或 `--statistics-only`。

`--serializable-deferrable`
:   在傾印時使用 `serializable` 交易，以確保所使用的快照與之後的資料庫狀態一致；但做法是等待交易串流中一個不可能出現任何異常的時間點，因此不會有傾印失敗，或導致其他交易以 `serialization_failure` 回復的風險。關於交易隔離與並行控制的更多資訊，請參閱[第 13 章](../../the-sql-language/mvcc/README.md)。

    對於只用於災難復原的傾印，此選項沒有好處。對於在原始資料庫持續更新期間，用來載入資料庫副本以供報表或其他唯讀負載分擔的傾印，它可能很有用。若不使用此選項，傾印所反映的狀態可能與最終已提交之交易的任何序列執行結果都不一致。舉例來說，若使用了批次處理技術，某個批次在傾印中可能顯示為已結束，但該批次中的項目並沒有全部出現。

    若 pg_dump 啟動時沒有任何作用中的讀寫交易，此選項不會造成任何差異。若有作用中的讀寫交易，傾印的開始可能會延遲一段不確定的時間。一旦開始執行，有無此選項的效能都相同。

`--snapshot=snapshotname`
:   對資料庫進行傾印時使用指定的同步快照（更多細節請參閱[表 9.100](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE)）。

    當需要讓傾印與邏輯複寫槽（請參閱[第 47 章](../../server-programming/logicaldecoding/README.md)）或某個並行的工作階段同步時，此選項很有用。

    在平行傾印的情況下，會使用此選項所定義的快照名稱，而不是取得新的快照。

`--statistics`
:   傾印最佳化器統計資訊。

`--statistics-only`
:   只傾印統計資訊，不傾印綱要（資料定義）或資料。會傾印資料表、具體化檢視表、外部資料表與索引的最佳化器統計資訊。

`--strict-names`
:   要求每個擴充功能（`-e`/`--extension`）、綱要（`-n`/`--schema`）與資料表（`-t`/`--table`）模式，都至少符合要傾印之資料庫中的一個擴充功能／綱要／資料表。這也適用於搭配 `--filter` 使用的過濾條件。請注意，若擴充功能／綱要／資料表模式全都找不到符合者，即使沒有 `--strict-names`，pg_dump 也會產生錯誤。

    此選項對 `--exclude-extension`、`-N`/`--exclude-schema`、`-T`/`--exclude-table` 或 `--exclude-table-data` 沒有作用。排除模式未能符合任何物件不會被視為錯誤。

`--sync-method=method`
:   設為 `fsync`（預設值）時，`pg_dump --format=directory` 會遞迴地開啟並同步封存目錄中的所有檔案。

    在 Linux 上，可以改用 `syncfs` 要求作業系統同步包含封存目錄的整個檔案系統。關於使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

    使用 `--no-sync` 或 `--format` 未設為 `directory` 時，此選項沒有作用。

`--table-and-children=pattern`
:   此選項與 `-t`/`--table` 選項相同，只是它還會包含符合 *`pattern`* 之資料表的任何分割區或繼承子資料表。

`--use-set-session-authorization`
:   輸出符合 SQL 標準的 `SET SESSION AUTHORIZATION` 命令，而不是 `ALTER OWNER` 命令，來決定物件的擁有權。這會使傾印更符合標準，但依傾印中物件的歷史而定，可能無法正確還原。此外，使用 `SET SESSION AUTHORIZATION` 的傾印必定需要超級使用者權限才能正確還原，而 `ALTER OWNER` 所需的權限較低。

`-?`<br>`--help`
:   顯示 pg_dump 命令列引數的說明後結束。

下列命令列選項控制資料庫連線參數。

`-d dbname`<br>`--dbname=dbname`
:   指定要連線的資料庫名稱。這等同於在命令列上將 *`dbname`* 指定為第一個非選項引數。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING)。若是如此，連線字串中的參數會覆寫任何衝突的命令列選項。

`-h host`<br>`--host=host`
:   指定伺服器執行所在機器的主機名稱。若值以斜線開頭，則會用作 Unix 網域通訊端 的目錄。預設值取自環境變數 `PGHOST`（若有設定），否則會嘗試 Unix 網域通訊端 連線。

`-p port`<br>`--port=port`
:   指定伺服器監聽連線的 TCP 連接埠或本機 Unix 網域通訊端 檔案副檔名。預設為環境變數 `PGPORT` 的值（若有設定），否則為編譯時內建的預設值。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   永不發出密碼提示。若伺服器要求密碼驗證，而無法透過 `.pgpass` 檔案等其他方式取得密碼，連線嘗試將會失敗。在沒有使用者在場輸入密碼的批次作業與腳本中，此選項可能很有用。

`-W`<br>`--password`
:   強制 pg_dump 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_dump 會自動提示輸入密碼。不過，pg_dump 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

`--role=rolename`
:   指定建立傾印時要使用的角色名稱。此選項會使 pg_dump 在連線到資料庫之後發出 `SET ROLE` *`rolename`* 命令。當已驗證的使用者（以 `-U` 指定）缺少 pg_dump 所需的權限，但可以切換到具有所需權限的角色時，此選項很有用。某些安裝環境有禁止直接以超級使用者登入的政策，使用此選項可以在不違反該政策的情況下進行傾印。

<a id="id-1.9.4.14.7"></a>

## 環境

`PGDATABASE`<br>`PGHOST`<br>`PGOPTIONS`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數。

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式與大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="APP-PGDUMP-DIAGNOSTICS"></a>

## 診斷

pg_dump 在內部會執行 `SELECT` 陳述式。若你在執行 pg_dump 時遇到問題，請確認你能夠使用例如 [psql](app-psql.md) 從資料庫中查詢資訊。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都會套用。

pg_dump 的資料庫活動通常會由累計統計系統收集。若不希望如此，你可以透過 `PGOPTIONS` 或 `ALTER
USER` 命令將參數 `track_counts` 設為 false。

<a id="PG-DUMP-NOTES"></a>

## 注意事項

若你的資料庫叢集對 `template1` 資料庫有任何本地新增的內容，請小心將 pg_dump 的輸出還原到真正空的資料庫中；否則你很可能會因為新增物件的定義重複而遇到錯誤。若要建立沒有任何本地新增內容的空資料庫，請從 `template0` 而非 `template1` 複製，例如：

```

CREATE DATABASE foo WITH TEMPLATE template0;
```

當選擇不含綱要的傾印並使用 `--disable-triggers` 選項時，pg_dump 會發出命令，在插入資料之前停用使用者資料表上的觸發程序，然後在資料插入之後發出重新啟用它們的命令。若還原在中途停止，系統目錄可能會停留在錯誤的狀態。

指定 `--statistics` 時，`pg_dump` 會在產生的傾印檔案中包含大部分的最佳化器統計資訊。這並不包括所有的統計資訊，例如以 [CREATE STATISTICS](../sql-commands/sql-createstatistics.md) 明確建立的統計資訊、由擴充功能加入的自訂統計資訊，或由累計統計系統收集的統計資訊。因此，從傾印檔案還原之後，執行 `ANALYZE` 以確保最佳效能可能仍然有用；更多資訊請參閱[第 24.1.3 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-STATISTICS)與[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)。

由於 pg_dump 被用來將資料轉移到較新版本的 PostgreSQL，可以預期 pg_dump 的輸出能載入比 pg_dump 版本更新的 PostgreSQL 伺服器版本。pg_dump 也可以從比它自身版本更舊的 PostgreSQL 伺服器傾印。（目前支援回溯到 9.2 版的伺服器。）不過，pg_dump 無法從比它自身主要版本更新的 PostgreSQL 伺服器傾印；它甚至會拒絕嘗試，而不是冒著產生無效傾印的風險。此外，並不保證 pg_dump 的輸出能載入到較舊主要版本的伺服器中——即使傾印是從該版本的伺服器取得的也一樣。將傾印檔案載入較舊的伺服器，可能需要手動編輯傾印檔案，移除較舊伺服器無法理解的語法。在跨版本的情況下，建議使用 `--quote-all-identifiers` 選項，因為它可以避免因不同 PostgreSQL 版本的保留字清單不同而產生的問題。

傾印邏輯複寫訂閱時，pg_dump 會產生使用 `connect = false` 選項的 `CREATE
SUBSCRIPTION` 命令，如此還原訂閱時就不會為了建立複寫槽或進行初始資料表複製而建立遠端連線。這樣一來，還原傾印時就不需要存取遠端伺服器的網路。接著由使用者以合適的方式重新啟用訂閱。若相關的主機已經變更，連線資訊可能必須跟著變更。在啟動新的完整資料表複製之前，截斷目標資料表也可能是合適的做法。若使用者打算在重新整理（refresh）期間複製初始資料，就必須以 `two_phase = false` 建立複寫槽。初始同步之後，若訂閱原本是以 `two_phase = true` 選項建立的，訂閱端會自動啟用 [`two_phase`](../sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) 選項。

從純文字的 pg_dump 腳本還原資料庫時，一般建議使用 `-X`（`--no-psqlrc`）選項，以確保還原過程乾淨，並避免與非預設的 psql 設定發生潛在衝突。

<a id="PG-DUMP-EXAMPLES"></a>

## 範例

將名為 `mydb` 的資料庫傾印到 SQL 腳本檔案：

```

$ pg_dump mydb > db.sql
```

將這樣的腳本重新載入名為 `newdb` 的（新建立的）資料庫：

```

$ psql -X -d newdb -f db.sql
```

將資料庫傾印到 custom 格式的封存檔：

```

$ pg_dump -Fc mydb > db.dump
```

將資料庫傾印到 directory 格式的封存檔：

```

$ pg_dump -Fd mydb -f dumpdir
```

以 5 個工作者作業平行地將資料庫傾印到 directory 格式的封存檔：

```

$ pg_dump -Fd mydb -j 5 -f dumpdir
```

將封存檔重新載入名為 `newdb` 的（新建立的）資料庫：

```

$ pg_restore -d newdb db.dump
```

將封存檔重新載入到它當初傾印出來的同一個資料庫，並捨棄該資料庫目前的內容：

```

$ pg_restore -d postgres --clean --create db.dump
```

傾印名為 `mytab` 的單一資料表：

```

$ pg_dump -t mytab mydb > db.sql
```

傾印 `detroit` 綱要中名稱以 `emp` 開頭的所有資料表，但名為 `employee_log` 的資料表除外：

```

$ pg_dump -t 'detroit.emp*' -T detroit.employee_log mydb > db.sql
```

傾印名稱以 `east` 或 `west` 開頭且以 `gsm` 結尾的所有綱要，並排除名稱中含有 `test` 這個字的任何綱要：

```

$ pg_dump -n 'east*gsm' -n 'west*gsm' -N '*test*' mydb > db.sql
```

同樣的操作，改用正規表示式記法合併這些選項：

```

$ pg_dump -n '(east|west)*gsm' -N '*test*' mydb > db.sql
```

傾印所有資料庫物件，但名稱以 `ts_` 開頭的資料表除外：

```

$ pg_dump -T 'ts_*' mydb > db.sql
```

若要在 `-t` 及相關選項中指定大寫或大小寫混合的名稱，你需要為名稱加上雙引號；否則名稱會被轉為小寫（請參閱[模式](app-psql.md#APP-PSQL-PATTERNS)）。但雙引號對 shell 而言是特殊字元，因此它們本身也必須加上引號。因此，若要傾印名稱大小寫混合的單一資料表，你需要類似這樣的寫法：

```

$ pg_dump -t "\"MixedCaseName\"" mydb > mytab.sql
```

若要傾印名稱以 `mytable` 開頭的所有資料表，但資料表 `mytable2` 除外，請指定如下的過濾檔案 `filter.txt`：

```

include table mytable*
exclude table mytable2
```

```

$ pg_dump --filter=filter.txt mydb > db.sql
```

<a id="id-1.9.4.14.11"></a>

## 另請參閱

[pg_dumpall](app-pg-dumpall.md), [pg_restore](app-pgrestore.md), [psql](app-psql.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgdump.html)（原文版本：18.6；核對日期：2026-10-10）
