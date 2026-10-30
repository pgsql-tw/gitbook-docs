<a id="APP-PGBASEBACKUP"></a><a id="id-1.9.4.10.1"></a>

## pg_basebackup

pg_basebackup — 製作 PostgreSQL 叢集的基礎備份

<a id="id-1.9.4.10.4"></a>

## 語法

<a id="id-1.9.4.10.4.1"></a>

`pg_basebackup` [*`option`*...]

<a id="id-1.9.4.10.5"></a>

## 說明

pg_basebackup 用來對執行中的 PostgreSQL 資料庫叢集製作基礎備份。製作備份時不會影響資料庫的其他用戶端，而備份既可用於時間點復原（請參閱[第 25.3 節](../../server-administration/backup/continuous-archiving.md)），也可作為日誌傳送或串流複寫待命伺服器的起點（請參閱[第 26.2 節](../../server-administration/high-availability/warm-standby.md)）。

pg_basebackup 可以製作資料庫的完整基礎備份或增量基礎備份。用於製作完整備份時，它會產生資料庫叢集檔案的精確複本。用於製作增量備份時，某些原本會包含在完整備份中的檔案，可能會被替換為同一檔案的增量版本，其中只包含自參考備份以來已修改過的區塊。增量備份不能直接使用；必須先使用 [pg_combinebackup](app-pgcombinebackup.md)，將它與其所依賴的先前備份合併。關於增量備份的更多資訊，請參閱[第 25.3.3 節](../../server-administration/backup/continuous-archiving.md#backup-incremental-backup)；從備份復原的步驟，請參閱[第 25.3.5 節](../../server-administration/backup/continuous-archiving.md#backup-pitr-recovery)。

在任何模式下，pg_basebackup 都會確保伺服器自動進入與離開備份模式。備份一律針對整個資料庫叢集進行；無法只備份個別資料庫或資料庫物件。若要進行選擇性備份，必須使用其他工具，例如 [pg_dump](app-pgdump.md)。

備份是透過使用複寫協定的一般 PostgreSQL 連線進行的。連線必須以具有 `REPLICATION` 權限（請參閱[第 21.2 節](../../server-administration/user-manag/role-attributes.md)）或屬於超級使用者的使用者 ID 建立，而且 [`pg_hba.conf`](../../server-administration/client-authentication/auth-pg-hba-conf.md) 必須允許該複寫連線。伺服器也必須將 [max_wal_senders](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS) 設定得夠高，以便為備份提供至少一個 walsender，再加上一個供 WAL 串流使用（若有使用的話）。

可以同時執行多個 `pg_basebackup`，但從效能的角度來看，通常較好的做法是只製作一份備份，再複製其結果。

pg_basebackup 不僅可以從主要伺服器製作基礎備份，也可以從待命伺服器製作。若要從待命伺服器製作備份，請將待命伺服器設定為可以接受複寫連線（也就是設定 `max_wal_senders` 與 [hot_standby](../../server-administration/runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY)，並適當地設定它的 `pg_hba.conf`）。你還需要在主要伺服器上啟用 [full_page_writes](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES)。

請注意，從待命伺服器製作備份有一些限制：

* 被備份的資料庫叢集中不會建立備份歷程檔案。
* pg_basebackup 無法在備份結束時強制待命伺服器切換到新的 WAL 檔案。使用 `-X none` 時，若主要伺服器上的寫入活動很少，pg_basebackup 可能需要等待很長的時間，備份所需的最後一個 WAL 檔案才會被切換並封存。在這種情況下，在主要伺服器上執行 `pg_switch_wal` 以觸發立即的 WAL 檔案切換，可能會有幫助。
* 若待命伺服器在備份期間被提升為主要伺服器，備份會失敗。
* 備份所需的所有 WAL 紀錄都必須包含足夠的全頁寫入（full-page write），這需要你在主要伺服器上啟用 `full_page_writes`。

每當 pg_basebackup 正在製作基礎備份時，伺服器的 `pg_stat_progress_basebackup` 檢視表會回報備份的進度。詳細資訊請參閱[第 27.4.6 節](../../server-administration/monitoring/progress-reporting.md#basebackup-progress-reporting)。

<a id="id-1.9.4.10.6"></a>

## 選項

下列命令列選項控制輸出的位置與格式：

`-D directory`<br>`--pgdata=directory`

設定輸出要寫入的目標目錄。若此目錄不存在，pg_basebackup 會建立它（以及任何缺少的上層目錄）。若它已經存在，則必須是空的。

當備份為 tar 格式時，目標目錄可以指定為 `-`（破折號），使 tar 檔案寫入 `stdout`。

此選項為必要。

`-F format`<br>`--format=format`

選擇輸出的格式。*`format`* 可以是下列之一：

- `p`<br>`plain`

  將輸出寫成一般檔案，其配置與來源伺服器的資料目錄及資料表空間相同。當叢集沒有額外的資料表空間時，整個資料庫會放在目標目錄中。若叢集包含額外的資料表空間，主資料目錄會放在目標目錄中，但其他所有資料表空間會放在與它們在來源伺服器上相同的絕對路徑。（若要變更這一點，請參閱 `--tablespace-mapping`。）

  這是預設格式。

- `t`<br>`tar`

  將輸出寫成目標目錄中的 tar 檔案。主資料目錄的內容會寫入名為 `base.tar` 的檔案，而其他每個資料表空間會分別寫入一個以該資料表空間 OID 命名的獨立 tar 檔案。

  若目標目錄指定為 `-`（破折號），tar 內容會寫到標準輸出，適合以管線傳給（例如）gzip。只有在叢集沒有額外的資料表空間，且未使用 WAL 串流時，才允許這麼做。

`-i old_manifest_file`<br>`--incremental=old_manifest_file`
:   執行[增量備份](../../server-administration/backup/continuous-archiving.md#backup-incremental-backup)。必須提供參考備份的備份清單（backup manifest），它會被上傳到伺服器，伺服器則會傳送所要求的增量備份作為回應。

`-R`<br>`--write-recovery-conf`
:   在目標目錄中（或使用 tar 格式時，在基礎封存檔中）建立 [`standby.signal`](../../server-administration/high-availability/warm-standby.md#FILE-STANDBY-SIGNAL)
    <a id="id-1.9.4.10.6.2.1.4.3.1.2"></a>
    檔案，並將連線設定附加到 `postgresql.auto.conf` 檔案。這讓使用備份結果來設置待命伺服器變得更容易。

    `postgresql.auto.conf` 檔案會記錄連線設定，以及（若有指定）pg_basebackup 正在使用的複寫插槽，讓串流複寫與[邏輯複寫插槽同步](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)之後會使用相同的設定。只有在連線字串或[環境變數](../../client-interfaces/libpq/libpq-envars.md)中明確指定了 dbname 時，才會記錄 dbname。

`-t target`<br>`--target=target`

指示伺服器要將基礎備份放在哪裡。預設目標是 `client`，表示備份應該傳送到執行 pg_basebackup 的機器。若改將目標設為 `server:/some/path`，備份會儲存在執行伺服器的機器上的 `/some/path` 目錄中。將備份儲存在伺服器上，需要超級使用者權限，或具有 `pg_write_server_files` 角色的權限。若目標設為 `blackhole`，內容會被丟棄，不會儲存在任何地方。這只應該用於測試目的，因為你最終不會得到實際的備份。

由於 WAL 串流是由 pg_basebackup 而非伺服器實作的，此選項不能與 `-Xstream` 一起使用。由於那是預設值，指定此選項時，你也必須指定 `-Xfetch` 或 `-Xnone` 其中之一。

`-T olddir=newdir`<br>`--tablespace-mapping=olddir=newdir`

在備份期間，將目錄 *`olddir`* 中的資料表空間重新定位到 *`newdir`*。要生效，*`olddir`* 必須與該資料表空間在來源伺服器上定義的路徑規格完全相符。（不過，若來源伺服器上的 *`olddir`* 中沒有資料表空間，並不算錯誤。）而 *`newdir`* 則是接收端主機檔案系統中的目錄。與主目標目錄一樣，*`newdir`* 不需要事先存在，但若它已存在，則必須是空的。*`olddir`* 與 *`newdir`* 都必須是絕對路徑。若任一路徑需要包含等號（`=`），請在它前面加上反斜線。對於多個資料表空間，此選項可以指定多次。

若資料表空間以這種方式重新定位，主資料目錄內的符號連結會更新為指向新位置。因此，新的資料目錄已準備好供新的伺服器執行個體使用，且所有資料表空間都位於更新後的位置。

目前此選項只適用於 plain 輸出格式；若選擇 tar 格式，此選項會被忽略。

`--waldir=waldir`
:   設定 WAL（預寫式日誌）檔案要寫入的目錄。預設情況下，WAL 檔案會放在目標目錄的 `pg_wal` 子目錄中，但可以使用此選項將它們放到其他位置。*`waldir`* 必須是絕對路徑。與主目標目錄一樣，*`waldir`* 不需要事先存在，但若它已存在，則必須是空的。只有在備份為 plain 格式時，才能指定此選項。

`-X method`<br>`--wal-method=method`

在備份中包含所需的 WAL（預寫式日誌）檔案。這會包含備份期間產生的所有預寫式日誌。除非指定方法 `none`，否則可以在目標目錄中啟動 postmaster，而不需要查閱 WAL 封存，使輸出成為完全獨立的備份。

支援下列收集預寫式日誌的 *`method`*：

- `n`<br>`none`

  不在備份中包含預寫式日誌。

- `f`<br>`fetch`

  預寫式日誌檔案會在備份結束時收集。因此，來源伺服器的 [wal_keep_size](../../server-administration/runtime-config/runtime-config-replication.md#GUC-WAL-KEEP-SIZE) 參數必須設定得夠高，使所需的日誌資料在備份結束前不會被移除。若所需的日誌資料在要傳送之前已被回收，備份將會失敗且無法使用。

  使用 tar 格式時，預寫式日誌檔案會包含在 `base.tar` 檔案中。

- `s`<br>`stream`

  在製作備份的同時串流傳送預寫式日誌資料。此方法會開啟第二個連到伺服器的連線，並在執行備份的同時平行開始串流傳送預寫式日誌。因此，它需要兩個複寫連線，而不只是一個。只要用戶端能跟上預寫式日誌資料，使用此方法就不需要在來源伺服器上保存額外的預寫式日誌。

  使用 tar 格式時，預寫式日誌檔案會寫入名為 `pg_wal.tar` 的獨立檔案（若伺服器版本早於 10，檔案會命名為 `pg_xlog.tar`）。

  此值為預設值。

`-z`<br>`--gzip`
:   以預設壓縮等級對 tar 檔案輸出啟用 gzip 壓縮。只有在使用 tar 格式時才能使用壓縮，且所有 tar 檔名都會自動加上副檔名 `.gz`。

`-Z level`<br>`-Z [{client|server}-]method[:detail]`<br>`--compress=level`<br>`--compress=[{client|server}-]method[:detail]`

要求對備份進行壓縮。若包含 `client` 或 `server`，它指定要在哪一端進行壓縮。在伺服器端壓縮會減少傳輸頻寬，但會增加伺服器的 CPU 消耗。預設為 `client`，但使用 `--target` 時除外。在那種情況下，備份不會傳送到用戶端，因此只有伺服器端壓縮才合理。使用 `-Xstream`（這是預設值）時，伺服器端壓縮不會套用到 WAL。若要壓縮 WAL，請使用用戶端壓縮，或指定 `-Xfetch`。

壓縮方法可以設為 `gzip`、`lz4`、`zstd`、表示不壓縮的 `none`，或一個整數（為 0 時不壓縮，大於 0 時使用 `gzip`）。可以選擇性地指定壓縮細節字串。若細節字串是整數，它指定壓縮等級。否則，它應該是以逗號分隔的項目清單，每個項目的形式為 *`keyword`* 或 *`keyword=value`*。目前支援的關鍵字為 `level`、`long` 與 `workers`。當壓縮方法以單純的整數指定時，不能使用細節字串。

若未指定壓縮等級，會使用預設壓縮等級。若只指定等級而未提及演算法，則等級大於 0 時會使用 `gzip` 壓縮，等級為 0 時則不壓縮。

當 tar 格式搭配 `gzip`、`lz4` 或 `zstd` 使用時，所有 tar 檔名會分別自動加上副檔名 `.gz`、`.lz4` 或 `.zst`。使用 plain 格式時，不能指定用戶端壓縮，但仍然可以要求伺服器端壓縮。若這麼做，伺服器會壓縮備份以便傳輸，而用戶端會將它解壓縮並解開。

此選項與 `-Xstream` 合併使用時，若選擇用戶端 gzip 壓縮，`pg_wal.tar` 會以 `gzip` 壓縮；但若選擇任何其他壓縮演算法，或選擇伺服器端壓縮，則不會被壓縮。

下列命令列選項控制備份的產生方式與程式的呼叫方式：

`-c {fast|spread}`<br>`--checkpoint={fast|spread}`
:   將檢查點模式設為 fast（立即）或 spread（預設）（請參閱[第 25.3.4 節](../../server-administration/backup/continuous-archiving.md#backup-lowlevel-base-backup)）。

`-C`<br>`--create-slot`
:   指定應該在開始備份之前，建立由 `--slot` 選項命名的複寫插槽。若該插槽已存在，會引發錯誤。

`-l label`<br>`--label=label`
:   設定備份的標籤。若未指定，會使用預設值「`pg_basebackup base backup`」。

`-n`<br>`--no-clean`

預設情況下，當 `pg_basebackup` 因錯誤而中止時，它會移除在發現無法完成工作之前可能已建立的任何目錄（例如目標目錄與預寫式日誌目錄）。此選項會禁止這項清理，因此對除錯很有用。

請注意，無論如何都不會清理資料表空間目錄。

`-N`<br>`--no-sync`
:   預設情況下，`pg_basebackup` 會等待所有檔案都安全寫入磁碟。此選項使 `pg_basebackup` 不等待就返回，這樣比較快，但也表示之後若發生作業系統當機，可能會使基礎備份損毀。一般而言，此選項適用於測試，但在建立正式環境安裝時不應該使用。

`-P`<br>`--progress`
:   啟用進度回報。開啟此功能會在備份期間提供大約的進度報告。由於資料庫在備份期間可能會變更，這只是近似值，最後可能不會剛好停在 `100%`。特別是當備份中包含 WAL 日誌時，資料總量無法事先估計，在這種情況下，估計的目標大小在超過不含 WAL 的總估計值之後會增加。

`-r rate`<br>`--max-rate=rate`

設定從來源伺服器收集資料的最大傳輸速率。這可以用來限制 pg_basebackup 對伺服器的影響。值的單位為每秒千位元組（kilobytes）。使用後綴 `M` 表示每秒百萬位元組（megabytes）。後綴 `k` 也可接受，但沒有任何作用。有效值介於每秒 32 千位元組與每秒 1024 百萬位元組之間。

此選項一律會影響資料目錄的傳輸。只有在收集方法為 `fetch` 時，WAL 檔案的傳輸才會受到影響。

`-S slotname`<br>`--slot=slotname`

此選項只能與 `-X
stream` 一起使用。它使 WAL 串流使用指定的複寫插槽。若基礎備份打算用作使用複寫插槽的串流複寫待命伺服器，則該待命伺服器應該在 [primary_slot_name](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME) 中使用相同的複寫插槽名稱。這可確保主要伺服器在基礎備份結束到新待命伺服器開始串流複寫之間的這段時間內，不會移除任何必要的 WAL 資料。

除非也使用了 `-C` 選項，否則指定的複寫插槽必須已存在。

若未指定此選項，且伺服器支援暫時複寫插槽（版本 10 及以後），則會自動使用一個暫時複寫插槽進行 WAL 串流。

`--sync-method=method`

設為 `fsync`（這是預設值）時，`pg_basebackup` 會遞迴地開啟並同步備份目錄中的所有檔案。使用 plain 格式時，搜尋檔案時會跟隨 WAL 目錄與每個已設定資料表空間的符號連結。

在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含備份目錄的整個檔案系統。使用 plain 格式時，`pg_basebackup` 也會同步包含 WAL 檔案與每個資料表空間的檔案系統。關於使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

使用 `--no-sync` 時，此選項沒有作用。

`-v`<br>`--verbose`
:   啟用詳細模式。會在啟動與關閉期間輸出一些額外的步驟，若同時啟用了進度回報，也會顯示目前正在處理的確切檔名。

`--manifest-checksums=algorithm`

指定應該套用到備份清單中所列每個檔案的檢查碼演算法。目前可用的演算法為 `NONE`、`CRC32C`、`SHA224`、`SHA256`、`SHA384` 與 `SHA512`。預設為 `CRC32C`。

若選擇 `NONE`，備份清單將不包含任何檢查碼。否則，它會包含以指定演算法計算的備份中每個檔案的檢查碼。此外，備份清單一律會包含其自身內容的 `SHA256` 檢查碼。`SHA` 演算法比 `CRC32C` 耗用明顯更多的 CPU，因此選擇其中之一可能會增加完成備份所需的時間。

對於希望驗證備份未遭竄改的使用者，使用 SHA 雜湊函式可以為每個檔案提供密碼學上安全的摘要；而 CRC-32C 演算法提供的檢查碼計算速度快得多，它很擅長偵測意外變更所造成的錯誤，但無法抵禦惡意修改。請注意，若要能防範可以存取備份的攻擊者，備份清單需要安全地存放在其他地方，或以其他方式驗證它自備份製作以來未被修改。

可以使用 [pg_verifybackup](app-pgverifybackup.md) 依據備份清單檢查備份的完整性。

`--manifest-force-encode`
:   強制將備份清單中的所有檔名以十六進位編碼。若未指定此選項，只有非 UTF8 的檔名會以十六進位編碼。此選項主要用於測試讀取備份清單檔案的工具是否能正確處理這種情況。

`--no-estimate-size`

防止伺服器估計將要串流傳送的備份資料總量，結果是 `pg_stat_progress_basebackup` 檢視表中的 `backup_total` 欄位一律為 `NULL`。

若不使用此選項，備份一開始會先計算整個資料庫的大小，然後再回頭傳送實際內容。這可能使備份花費稍長的時間，特別是送出第一筆資料之前會花較久的時間。若這段估計時間太長，此選項可用來避免它。

使用 `--progress` 時不允許此選項。

`--no-manifest`
:   停用備份清單的產生。若未指定此選項，伺服器會產生並傳送一份備份清單，可以使用 [pg_verifybackup](app-pgverifybackup.md) 加以驗證。備份清單是備份中所有檔案的清單，但可能包含在內的任何 WAL 檔案除外。它也會儲存每個檔案的大小、最後修改時間，以及選擇性的檢查碼。

`--no-slot`

防止為備份建立暫時複寫插槽。

預設情況下，若選擇了日誌串流，但未以 `-S` 選項指定插槽名稱，則會建立一個暫時複寫插槽（若來源伺服器支援的話）。

此選項的主要目的是讓伺服器在沒有可用複寫插槽時，仍然可以製作基礎備份。使用複寫插槽幾乎總是較佳的做法，因為它可以防止伺服器在備份期間移除所需的 WAL。

`--no-verify-checksums`

停用檢查碼驗證（若製作基礎備份的來源伺服器有啟用檢查碼）。

預設情況下會驗證檢查碼，而檢查碼驗證失敗會導致非零的結束狀態。不過，在這種情況下基礎備份不會被移除，如同使用了 `--no-clean` 選項一樣。檢查碼驗證失敗也會回報在 [`pg_stat_database`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW) 檢視表中。

下列命令列選項控制與來源伺服器的連線：

`-d connstr`<br>`--dbname=connstr`

指定用來連線到伺服器的參數，形式為[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)；這些參數會覆寫任何相衝突的命令列選項。

為了與其他用戶端應用程式保持一致，此選項命名為 `--dbname`，但由於 pg_basebackup 不會連線到叢集中的任何特定資料庫，連線字串中包含的任何資料庫名稱都會被伺服器忽略。不過，以這種方式提供的資料庫名稱，在 `~/.pgpass` 中查找複寫連線的密碼時，會覆寫預設的資料庫名稱（`replication`）。同樣地，連線到 PostgreSQL 時所使用的中介軟體或代理伺服器，可能會將此名稱用於連線路由等目的。此資料庫名稱也可以由[邏輯複寫插槽同步](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)使用。

`-h host`<br>`--host=host`
:   指定執行伺服器之機器的主機名稱。若值以斜線開頭，它會被用作 Unix 網域通訊端的目錄。預設值取自 `PGHOST` 環境變數（若有設定），否則會嘗試以 Unix 網域通訊端連線。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。預設為 `PGPORT` 環境變數（若有設定），否則為編譯時內建的預設值。

`-s interval`<br>`--status-interval=interval`
:   指定傳回來源伺服器的狀態封包之間間隔的秒數。較小的值可以讓伺服器更精確地監控備份進度。值為零會完全停用定期狀態更新，不過當伺服器要求時仍然會傳送更新，以避免因逾時而中斷連線。預設值為 10 秒。

`-U username`<br>`--username=username`
:   指定要用來連線的使用者名稱。

`-w`<br>`--no-password`
:   不發出密碼提示。若伺服器要求密碼驗證，而又無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中很有用。

`-W`<br>`--password`

強制 pg_basebackup 在連線到來源伺服器之前提示輸入密碼。

此選項從來不是必要的，因為若伺服器要求密碼驗證，pg_basebackup 會自動提示輸入密碼。不過，pg_basebackup 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 來避免這次額外的連線嘗試。

另外也提供其他選項：

`-V`<br>`--version`
:   印出 pg_basebackup 的版本後結束。

`-?`<br>`--help`
:   顯示 pg_basebackup 命令列引數的說明後結束。

<a id="id-1.9.4.10.7"></a>

## 環境

此工具程式與大多數其他 PostgreSQL 工具程式一樣，會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.10.8"></a>

## 注意事項

在備份開始時，需要在來源伺服器上執行一次檢查點。這可能需要一些時間（特別是未使用 `--checkpoint=fast` 選項時），在此期間 pg_basebackup 看起來會像是處於閒置狀態。

備份會包含資料目錄與資料表空間中的所有檔案，包括設定檔以及第三方放在該目錄中的任何其他檔案，但由 PostgreSQL 管理的某些暫存檔與作業系統檔案除外。不過，只有一般檔案與目錄會被複製，例外的是用於資料表空間的符號連結會被保留。指向 PostgreSQL 已知的某些目錄的符號連結，會被複製為空目錄。其他符號連結與特殊裝置檔案會被略過。確切的細節請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)。

在 plain 格式中，資料表空間會備份到與它們在來源伺服器上相同的路徑，除非使用了 `--tablespace-mapping` 選項。若不使用此選項，當有使用資料表空間時，在與伺服器相同的主機上執行 plain 格式的基礎備份將無法運作，因為備份必須寫入與原始資料表空間相同的目錄位置。

使用 tar 格式時，在啟動使用這些資料的 PostgreSQL 伺服器之前，解開每個 tar 檔案是使用者的責任。若有額外的資料表空間，它們的 tar 檔案需要解開到正確的位置。在這種情況下，伺服器會依據 `base.tar` 檔案中所包含的 `tablespace_map` 檔案內容，建立這些資料表空間的符號連結。

pg_basebackup 可以搭配相同或較舊主要版本的伺服器使用，最舊到 9.1。不過，WAL 串流模式（`-X
stream`）只適用於伺服器版本 9.3 及以後，tar 格式（`--format=tar`）只適用於伺服器版本 9.5 及以後，而增量備份（`--incremental`）只適用於伺服器版本 17 及以後。

若來源叢集啟用了群組權限，pg_basebackup 會保留資料檔案的群組權限。

<a id="id-1.9.4.10.9"></a>

## 範例

若要為位於 `mydbserver` 的伺服器建立基礎備份，並將它儲存在本機目錄 `/usr/local/pgsql/data` 中：

```

$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
```

若要為本機伺服器建立備份，每個資料表空間各一個壓縮的 tar 檔案，儲存在目錄 `backup` 中，並在執行時顯示進度報告：

```

$ pg_basebackup -D backup -Ft -z -P
```

若要為只有單一資料表空間的本機資料庫建立備份，並以 bzip2 壓縮：

```

$ pg_basebackup -D - -Ft -X fetch | bzip2 > backup.tar.bz2
```

（若資料庫中有多個資料表空間，此命令將會失敗。）

若要為本機資料庫建立備份，並將位於 `/opt/ts` 的資料表空間重新定位到 `./backup/ts`：

```

$ pg_basebackup -D backup/data -T /opt/ts=$(pwd)/backup/ts
```

若要為本機伺服器建立備份，每個資料表空間各一個以 gzip 等級 9 壓縮的 tar 檔案，儲存在目錄 `backup` 中：

```

$ pg_basebackup -D backup -Ft --compress=gzip:9
```

<a id="id-1.9.4.10.10"></a>

## 另請參閱

[pg_dump](app-pgdump.md), [第 27.4.6 節](../../server-administration/monitoring/progress-reporting.md#basebackup-progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgbasebackup.html)（原文版本：18.6；核對日期：2026-10-09）
