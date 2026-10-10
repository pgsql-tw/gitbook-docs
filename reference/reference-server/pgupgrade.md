<a id="PGUPGRADE"></a><a id="id-1.9.5.13.1"></a>

## pg_upgrade

pg_upgrade — 升級 PostgreSQL 伺服器實例

## 語法

<a id="id-1.9.5.13.4.1"></a>

`pg_upgrade` `-b` *`oldbindir`* [`-B` *`newbindir`*] `-d` *`oldconfigdir`* `-D` *`newconfigdir`* [*`option`*...]

<a id="id-1.9.5.13.5"></a>

## 說明

pg_upgrade（舊稱 pg_migrator）可以將儲存在 PostgreSQL 資料檔案中的資料升級到較新的 PostgreSQL 主要版本，而不需要主要版本升級通常所需的資料傾印／還原，例如從 12.14 升級到 13.10，或從 14.9 升級到 15.5。次要版本升級（例如從 12.7 升級到 12.8，或從 14.1 升級到 14.5）則不需要它。

PostgreSQL 的主要版本經常加入新功能，這些新功能常常會改變系統資料表的配置，但內部資料儲存格式很少改變。pg_upgrade 利用這一點，透過建立新的系統資料表並直接重複使用舊的使用者資料檔案，來進行快速升級。如果未來某個主要版本改變了資料儲存格式，使得舊的資料格式無法讀取，pg_upgrade 將無法用於這類升級。（社群會盡量避免這種情況。）

pg_upgrade 會盡力確保新舊叢集是二進位相容的，例如檢查編譯時期設定是否相容，包括 32/64 位元的執行檔。任何外部模組也必須是二進位相容的，這點很重要，不過 pg_upgrade 無法檢查這一點。

pg_upgrade 支援從 9.2.X 及之後的版本升級到 PostgreSQL 目前的主要版本，包括快照版與 beta 版。

<a id="id-1.9.5.13.5.6"></a>

### 警告

升級叢集會使目的端執行由來源端超級使用者所選擇的任意程式碼。升級之前，請確保來源端的超級使用者是可信任的。

<a id="id-1.9.5.13.6"></a>

## 選項

pg_upgrade 接受下列命令列引數：

`-b` *`bindir`*<br>`--old-bindir=`*`bindir`*
:   舊的 PostgreSQL 執行檔目錄；環境變數為 `PGBINOLD`

`-B` *`bindir`*<br>`--new-bindir=`*`bindir`*
:   新的 PostgreSQL 執行檔目錄；預設為 pg_upgrade 所在的目錄；環境變數為 `PGBINNEW`

`-c`<br>`--check`
:   只檢查叢集，不變更任何資料

`-d` *`configdir`*<br>`--old-datadir=`*`configdir`*
:   舊資料庫叢集的設定目錄；環境變數為 `PGDATAOLD`

`-D` *`configdir`*<br>`--new-datadir=`*`configdir`*
:   新資料庫叢集的設定目錄；環境變數為 `PGDATANEW`

`-j njobs`<br>`--jobs=njobs`
:   要使用的同時連線數與程序／執行緒數

`-k`<br>`--link`
:   使用硬連結，而不是將檔案複製到新叢集

`-N`<br>`--no-sync`
:   預設情況下，`pg_upgrade` 會等待已升級叢集的所有檔案都安全寫入磁碟。此選項會讓 `pg_upgrade` 不等待就返回，這樣比較快，但意味著之後的作業系統當機可能會使資料目錄損毀。一般而言，此選項適用於測試，但不應該用於正式環境的安裝。

`-o` *`options`*<br>`--old-options` *`options`*
:   要直接傳給舊 `postgres` 命令的選項；多次指定此選項時會附加在一起

`-O` *`options`*<br>`--new-options` *`options`*
:   要直接傳給新 `postgres` 命令的選項；多次指定此選項時會附加在一起

`-p` *`port`*<br>`--old-port=`*`port`*
:   舊叢集的連接埠號碼；環境變數為 `PGPORTOLD`

`-P` *`port`*<br>`--new-port=`*`port`*
:   新叢集的連接埠號碼；環境變數為 `PGPORTNEW`

`-r`<br>`--retain`
:   即使成功完成，仍保留 SQL 與日誌檔案

`-s` *`dir`*<br>`--socketdir=`*`dir`*
:   升級期間 postmaster socket 所使用的目錄；預設為目前的工作目錄；環境變數為 `PGSOCKETDIR`

`-U` *`username`*<br>`--username=`*`username`*
:   叢集的安裝使用者名稱；環境變數為 `PGUSER`

`-v`<br>`--verbose`
:   啟用詳細的內部日誌記錄

`-V`<br>`--version`
:   顯示版本資訊後結束

`--clone`
:   使用有效率的檔案複製（clone，在某些系統上也稱為「reflinks」），而不是將檔案複製（copy）到新叢集。這可以讓資料檔案的複製幾乎在瞬間完成，具有 `-k`/`--link` 的速度優勢，同時讓舊叢集保持不變。

    只有部分作業系統與檔案系統支援檔案複製（clone）。如果選擇了此選項但系統不支援，pg_upgrade 的執行將會發生錯誤。目前，支援的環境有 Linux（核心 4.5 或更新版本）上的 Btrfs 與 XFS（在建立時啟用 reflink 支援的檔案系統上），以及 macOS 上的 APFS。

`--copy`
:   將檔案複製到新叢集。這是預設行為。（另請參閱 `--link`、`--clone`、`--copy-file-range` 與 `--swap`。）

`--copy-file-range`
:   使用 `copy_file_range` 系統呼叫進行有效率的複製。在某些檔案系統上，這會產生與 `--clone` 類似的結果，共用實體磁碟區塊；而在其他檔案系統上，它可能仍會複製區塊，但會透過最佳化的路徑來進行。目前，Linux 與 FreeBSD 支援此選項。

`--no-statistics`
:   不將統計資訊從舊叢集還原到新叢集。

`--set-char-signedness=`*`option`*
:   手動設定新叢集預設的 char 有號性（signedness）。可用值為 `signed` 與 `unsigned`。

    在 C 語言中，`char` 型別的預設有號性（在未明確指定時）因平台而異。例如，`char` 在 x86 CPU 上預設為 `signed char`，但在 ARM CPU 上預設為 `unsigned char`。

    從 PostgreSQL 18 開始，資料庫叢集會維護自己的預設 char 有號性設定，可用來確保在預設 char 有號性不同的平台之間行為一致。預設情況下，從現有叢集升級時，pg_upgrade 會保留 char 有號性設定。不過，從 PostgreSQL 17 或更早版本升級時，pg_upgrade 會採用其建置平台的 char 有號性。

    此選項可讓你明確設定新叢集的預設 char 有號性，覆寫任何繼承而來的值。此選項與下列兩種特定情境有關：

    * 如果你計劃在升級之後遷移到不同的平台，則不應該使用此選項。在這種情況下，預設行為就是正確的。請改為在原本的平台上不加此旗標進行升級，之後再遷移叢集。這是建議且最安全的做法。
    * 如果你已經將叢集遷移到 char 有號性不同的平台（例如從 x86 系統遷移到 ARM 系統），則應該使用此選項來指定與原平台預設 char 有號性相符的有號性。此外，在遷移資料檔案與執行 `pg_upgrade` 之間，務必不要修改任何資料檔案。`pg_upgrade` 應該是在新平台上啟動叢集的第一個操作。

`--swap`
:   將資料目錄從舊叢集移動到新叢集。接著，以為新叢集產生的系統目錄檔案取代原本的系統目錄檔案。此模式的效能可能優於 `--link`、`--clone`、`--copy` 與 `--copy-file-range`，特別是在有許多關聯的叢集上。

    不過，此模式會在舊叢集中產生許多垃圾檔案，若使用 `--sync-method=syncfs`，可能會拉長檔案同步步驟的時間。因此，建議搭配 `--swap` 使用 `--sync-method=fsync`。

    此外，一旦檔案傳輸步驟開始，舊叢集將遭到破壞性的修改，因此將無法再安全地啟動。詳情請參閱[步驟 17](pgupgrade.md#PGUPGRADE-STEP-REVERT)。

`--sync-method=`*`method`*
:   設為預設值 `fsync` 時，`pg_upgrade` 會遞迴地開啟並同步已升級叢集資料目錄中的所有檔案。搜尋檔案時會跟隨 WAL 目錄與每個已設定之資料表空間的符號連結。

    在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含已升級叢集之資料目錄、其 WAL 檔案與每個資料表空間的整個檔案系統。關於使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

    使用 `--no-sync` 時，此選項沒有作用。

`-?`<br>`--help`
:   顯示說明後結束

<a id="id-1.9.5.13.7"></a>

## 用法

以下是使用 pg_upgrade 進行升級的步驟：

<a id="id-1.9.5.13.7.3"></a>

### 注意

升級[*[邏輯複寫叢集](../../appendixes/glossary/README.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER)*](../../appendixes/glossary/README.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER)的步驟不在此說明；詳情請參閱[第 29.13 節](../../server-administration/logical-replication/logical-replication-upgrade.md)。

1. **（選擇性）移動舊叢集**

   如果你使用的是依版本區分的安裝目錄，例如 `/opt/PostgreSQL/18`，就不需要移動舊叢集。圖形化安裝程式都使用依版本區分的安裝目錄。

   如果你的安裝目錄不是依版本區分的，例如 `/usr/local/pgsql`，就必須移動目前的 PostgreSQL 安裝目錄，以免它干擾新的 PostgreSQL 安裝。目前的 PostgreSQL 伺服器關閉之後，就可以安全地重新命名 PostgreSQL 安裝目錄；假設舊目錄是 `/usr/local/pgsql`，你可以執行：

   ```

   mv /usr/local/pgsql /usr/local/pgsql.old
   ```

   來重新命名該目錄。
2. **若從原始碼安裝，建置新版本**

   使用與舊叢集相容的 `configure` 旗標建置新的 PostgreSQL 原始碼。pg_upgrade 會在開始升級之前檢查 `pg_controldata`，以確保所有設定都相容。
3. **安裝新的 PostgreSQL 執行檔**

   安裝新伺服器的執行檔與支援檔案。預設安裝中已包含 pg_upgrade。

   若從原始碼安裝，而你希望將新伺服器安裝在自訂位置，請使用 `prefix` 變數：

   ```

   make prefix=/usr/local/pgsql.new install
   ```
4. **初始化新的 PostgreSQL 叢集**

   使用 `initdb` 初始化新叢集。同樣地，請使用與舊叢集相符的相容 `initdb` 旗標。許多預先建置的安裝程式會自動執行此步驟。不需要啟動新叢集。
5. **安裝擴充功能的共享物件檔案**

   許多擴充功能與自訂模組，無論來自 `contrib` 或其他來源，都會使用共享物件檔案（或 DLL），例如 `pgcrypto.so`。如果舊叢集使用了這些檔案，就必須在新叢集中安裝與新伺服器執行檔相符的共享物件檔案，通常是透過作業系統命令來安裝。不要載入綱要定義，例如 `CREATE
   EXTENSION pgcrypto`，因為這些定義會從舊叢集複製過來。如果有可用的擴充功能更新，pg_upgrade 會回報此情況，並建立一個之後可執行以更新它們的腳本。
6. **複製自訂的全文檢索檔案**

   將任何自訂的全文檢索檔案（字典、同義詞、同義詞庫、停用詞）從舊叢集複製到新叢集。
7. **調整認證**

   `pg_upgrade` 會多次連線到舊伺服器與新伺服器，因此你可能會想在 `pg_hba.conf` 中將認證設為 `peer`，或使用 `~/.pgpass` 檔案（請參閱[第 32.16 節](../../client-interfaces/libpq/libpq-pgpass.md)）。
8. **停止兩部伺服器**

   確認兩部資料庫伺服器都已停止，例如在 Unix 上使用：

   ```

   pg_ctl -D /opt/PostgreSQL/12 stop
   pg_ctl -D /opt/PostgreSQL/18 stop
   ```

   或在 Windows 上，使用適當的服務名稱：

   ```

   NET STOP postgresql-12
   NET STOP postgresql-18
   ```

   在此關閉過程中，串流複寫與日誌傳送的待命伺服器必須保持執行，才能接收所有變更。
9. **為待命伺服器的升級做準備**

   如果你要使用[步驟 11](pgupgrade.md#PGUPGRADE-STEP-REPLICAS) 中所述的方法升級待命伺服器，請對舊的主要叢集與待命叢集執行 pg_controldata，以確認舊的待命伺服器已經追上進度。確認所有叢集中的「Latest checkpoint location」值都相符。此外，請確認新主要叢集的 `postgresql.conf` 檔案中，`wal_level` 沒有設為 `minimal`。
10. **執行 pg_upgrade**

    一律執行新伺服器的 pg_upgrade 執行檔，而不是舊伺服器的。pg_upgrade 需要指定新舊叢集的資料目錄與執行檔（`bin`）目錄。你也可以指定使用者與連接埠值，以及是否要以連結、複製（clone）或交換的方式處理資料檔案，而不是預設的複製（copy）行為。

    如果你使用連結模式，升級會快得多（不需要複製檔案）且使用較少的磁碟空間，但在升級後啟動新叢集之後，你將無法存取舊叢集。連結模式也要求新舊叢集的資料目錄位於同一個檔案系統中。（資料表空間與 `pg_wal` 可以位於不同的檔案系統上。）複製（clone）模式提供相同的速度與磁碟空間優勢，但不會在新叢集啟動後使舊叢集無法使用。複製（clone）模式也要求新舊資料目錄位於同一個檔案系統中。此模式只在特定的作業系統與檔案系統上可用。如果有許多關聯，交換模式可能是最快的，但一旦檔案傳輸步驟開始，你將無法存取舊叢集。交換模式也要求新舊叢集的資料目錄位於同一個檔案系統中。

    將 `--jobs` 設為 2 或更高，可讓 pg_upgrade 平行處理多個資料庫與資料表空間。一個好的起點是機器上的 CPU 核心數。對於有多個資料庫與多個資料表空間的伺服器，此選項可以大幅縮短升級時間。

    Windows 使用者必須登入系統管理員帳號，然後以加上引號的目錄執行 pg_upgrade，例如：

    ```

    pg_upgrade.exe
            --old-datadir "C:/Program Files/PostgreSQL/12/data"
            --new-datadir "C:/Program Files/PostgreSQL/18/data"
            --old-bindir "C:/Program Files/PostgreSQL/12/bin"
            --new-bindir "C:/Program Files/PostgreSQL/18/bin"
    ```

    啟動後，`pg_upgrade` 會驗證兩個叢集是否相容，然後進行升級。你可以使用 `pg_upgrade --check` 只執行檢查，即使舊伺服器仍在執行中也可以。`pg_upgrade --check` 也會概述升級後你需要進行的任何手動調整。如果你將使用連結、複製（clone）、copy-file-range 或交換模式，應該將 `--link`、`--clone`、`--copy-file-range` 或 `--swap` 選項與 `--check` 一起使用，以啟用該模式特有的檢查。`pg_upgrade` 需要目前目錄的寫入權限。

    顯然，升級期間不應該有任何人存取這些叢集。pg_upgrade 預設在連接埠 50432 上執行伺服器，以避免非預期的用戶端連線。進行升級時，你可以讓兩個叢集使用相同的連接埠號碼，因為新舊叢集不會同時執行。不過，檢查執行中的舊伺服器時，新舊連接埠號碼必須不同。

    如果在還原資料庫綱要時發生錯誤，`pg_upgrade` 會結束，而你必須依照下方[步驟 17](pgupgrade.md#PGUPGRADE-STEP-REVERT) 所述還原到舊叢集。若要再次嘗試 `pg_upgrade`，你需要修改舊叢集，讓 pg_upgrade 的綱要還原能夠成功。如果問題出在某個 `contrib` 模組，你可能需要從舊叢集解除安裝該 `contrib` 模組，並在升級後將它安裝到新叢集中，前提是該模組沒有被用來儲存使用者資料。
<a id="PGUPGRADE-STEP-REPLICAS"></a>

11. **升級串流複寫與日誌傳送的待命伺服器**

    如果你使用了連結模式，並且有串流複寫（請參閱[第 26.2.5 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)）或日誌傳送（請參閱[第 26.2 節](../../server-administration/high-availability/warm-standby.md)）的待命伺服器，你可以依照下列步驟快速升級它們。你不會在待命伺服器上執行 pg_upgrade，而是在主要伺服器上執行 rsync。先不要啟動任何伺服器。

    如果你*沒有*使用連結模式、沒有或不想使用 rsync，或者想要更簡單的做法，請略過本節的說明，在 pg_upgrade 完成且新的主要伺服器開始執行之後，直接重新建立待命伺服器即可。

    1. **在待命伺服器上安裝新的 PostgreSQL 執行檔**

       確認所有待命伺服器上都已安裝新的執行檔與支援檔案。
    2. **確認新的待命資料目錄*不*存在**

       確認新的待命資料目錄*不*存在或是空的。如果已經執行過 initdb，請刪除待命伺服器的新資料目錄。
    3. **安裝擴充功能的共享物件檔案**

       在新的待命伺服器上安裝與新主要叢集中相同的擴充功能共享物件檔案。
    4. **停止待命伺服器**

       如果待命伺服器仍在執行，請立即依照上述說明停止它們。
    5. **儲存設定檔**

       從舊待命伺服器的設定目錄中儲存你需要保留的任何設定檔，例如 `postgresql.conf`（以及它所引入的任何檔案）、`postgresql.auto.conf`、`pg_hba.conf`，因為這些檔案在下一個步驟中會被覆寫或移除。
    6. **執行 rsync**

       使用連結模式時，可以使用 rsync 快速升級待命伺服器。做法是在主要伺服器上，從位於新舊資料庫叢集目錄上層的某個目錄，針對每部待命伺服器在*主要伺服器*上執行：

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive old_cluster new_cluster remote_dir
       ```

       其中 `old_cluster` 與 `new_cluster` 是相對於主要伺服器上目前目錄的路徑，而 `remote_dir` 是待命伺服器上新舊叢集目錄的*上層*目錄。主要伺服器與待命伺服器上指定目錄之下的目錄結構必須相符。關於指定遠端目錄的細節，請參閱 rsync 的手冊頁面，例如：

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive /opt/PostgreSQL/12 \
             /opt/PostgreSQL/18 standby.example.com:/opt/PostgreSQL
       ```

       你可以使用 rsync 的 `--dry-run` 選項來確認該命令會做什麼。雖然 rsync 必須至少針對一部待命伺服器在主要伺服器上執行，但只要已升級的待命伺服器尚未啟動，也可以在已升級的待命伺服器上執行 rsync 來升級其他待命伺服器。

       這個做法會記錄 pg_upgrade 的連結模式在主要伺服器上所建立、用來連接新舊叢集中檔案的連結。接著，它會在待命伺服器的舊叢集中找出相符的檔案，並在待命伺服器的新叢集中為它們建立連結。在主要伺服器上未被連結的檔案，會從主要伺服器複製到待命伺服器。（這些檔案通常很小。）這樣就能快速升級待命伺服器。遺憾的是，rsync 會不必要地複製與暫存資料表及無日誌資料表相關的檔案，因為這些檔案通常不存在於待命伺服器上。

       如果你有資料表空間，就需要為每個資料表空間目錄執行類似的 rsync 命令，例如：

       ```

       rsync --archive --delete --hard-links --size-only --no-inc-recursive /vol1/pg_tblsp/PG_12_201909212 \
             /vol1/pg_tblsp/PG_18_202307071 standby.example.com:/vol1/pg_tblsp
       ```

       如果你已將 `pg_wal` 移到資料目錄之外，也必須對那些目錄執行 rsync。
    7. **設定串流複寫與日誌傳送的待命伺服器**

       設定伺服器以進行日誌傳送。（你不需要執行 `pg_backup_start()` 與 `pg_backup_stop()`，也不需要製作檔案系統備份，因為待命伺服器仍與主要伺服器保持同步。）如果舊的主要伺服器早於 17.0 版，則主要伺服器上的複寫槽都不會被複製到新的待命伺服器，因此舊待命伺服器上的所有複寫槽都必須手動重新建立。如果舊的主要伺服器是 17.0 版或更新版本，則只有主要伺服器上的邏輯複寫槽會被複製到新的待命伺服器，而舊待命伺服器上的其他複寫槽不會被複製，因此必須手動重新建立。
12. **還原 `pg_hba.conf`**

    如果你修改過 `pg_hba.conf`，請還原它原本的設定。可能也需要調整新叢集中的其他設定檔，使其與舊叢集相符，例如 `postgresql.conf`（以及它所引入的任何檔案）、`postgresql.auto.conf`。
13. **啟動新伺服器**

    現在可以安全地啟動新伺服器，接著再啟動任何以 rsync 升級的待命伺服器。
14. **升級後處理**

    如果需要任何升級後處理，pg_upgrade 會在完成時發出警告。它也會產生必須由管理者執行的腳本檔案。這些腳本檔案會連線到每個需要升級後處理的資料庫。每個腳本都應該使用下列方式執行：

    ```

    psql --username=postgres --file=script.sql postgres
    ```

    這些腳本可以依任何順序執行，執行過後即可刪除。

    <a id="id-1.9.5.13.7.4.14.5"></a>

    ### 小心

    一般而言，在重建腳本執行完成之前，存取重建腳本中所參照的資料表是不安全的；這樣做可能會產生不正確的結果或不佳的效能。重建腳本中未參照的資料表則可以立即存取。
15. **統計資訊**

    除非指定了 `--no-statistics` 選項，否則 `pg_upgrade` 會將大部分最佳化器統計資訊從舊叢集轉移到新叢集。這不會轉移所有的統計資訊，例如以 [CREATE STATISTICS](../sql-commands/sql-createstatistics.md) 明確建立的統計資訊、擴充功能所加入的自訂統計資訊，或累積統計系統所收集的統計資訊。

    由於並非所有統計資訊都會由 `pg_upgrade` 轉移，升級結束時會指示你執行命令來重新產生這些資訊。你可能需要設定連線參數以符合你的新叢集。

    首先，使用 `vacuumdb --all --analyze-in-stages --missing-stats-only` 為沒有任何最佳化器統計資訊的關聯快速產生最少量的統計資訊。接著，使用 `vacuumdb --all --analyze-only` 確保所有關聯都有更新過的累積統計資訊，以觸發清理與分析。這兩個命令都可以使用 `--jobs` 來加快速度。如果 `vacuum_cost_delay` 設為非零值，可以使用 `PGOPTIONS` 覆寫它以加快統計資訊的產生，例如 `PGOPTIONS='-c
    vacuum_cost_delay=0' vacuumdb ...`。
16. **刪除舊叢集**

    確認升級結果令你滿意之後，你可以執行 `pg_upgrade` 完成時所提到的腳本，刪除舊叢集的資料目錄。（如果你在舊資料目錄中有使用者定義的資料表空間，就無法自動刪除。）你也可以刪除舊的安裝目錄（例如 `bin`、`share`）。
<a id="PGUPGRADE-STEP-REVERT"></a>

17. **還原到舊叢集**

    如果在執行 `pg_upgrade` 之後，你希望還原到舊叢集，有以下幾種做法：

    * 如果使用了 `--check` 選項，舊叢集未被修改；可以重新啟動它。
    * 如果既沒有使用 `--link`，也沒有使用 `--swap`，舊叢集未被修改；可以重新啟動它。
    * 如果使用了 `--link` 選項，資料檔案可能由新舊叢集共用：

      * 如果 `pg_upgrade` 在連結開始之前就中止，舊叢集未被修改；可以重新啟動它。
      * 如果你*沒有*啟動新叢集，則舊叢集除了在連結開始時於 `$PGDATA/global/pg_control` 加上 `.old` 字尾之外，未被修改。若要重新使用舊叢集，請移除 `$PGDATA/global/pg_control` 的 `.old` 字尾；然後就可以重新啟動舊叢集。
      * 如果你已經啟動了新叢集，它已經寫入共用檔案，使用舊叢集是不安全的。在這種情況下，需要從備份還原舊叢集。
    * 如果使用了 `--swap` 選項，舊叢集可能已遭到破壞性的修改：

      * 如果 `pg_upgrade` 在回報舊叢集已無法安全啟動之前就中止，舊叢集未被修改；可以重新啟動它。
      * 如果 `pg_upgrade` 已經回報舊叢集無法再安全啟動，則舊叢集已遭到破壞性的修改。在這種情況下，需要從備份還原舊叢集。

<a id="id-1.9.5.13.8"></a>

## 環境

有些環境變數可以用來提供命令列選項的預設值：

`PGBINOLD`
:   舊的 PostgreSQL 執行檔目錄；對應選項 `-b`/`--old-bindir`。

`PGBINNEW`
:   新的 PostgreSQL 執行檔目錄；對應選項 `-B`/`--new-bindir`。

`PGDATAOLD`
:   舊資料庫叢集的設定目錄；對應選項 `-d`/`--old-datadir`。

`PGDATANEW`
:   新資料庫叢集的設定目錄；對應選項 `-D`/`--new-datadir`。

`PGPORTOLD`
:   舊叢集的連接埠號碼；對應選項 `-p`/`--old-port`。

`PGPORTNEW`
:   新叢集的連接埠號碼；對應選項 `-P`/`--new-port`。

`PGSOCKETDIR`
:   升級期間 postmaster socket 所使用的目錄；對應選項 `-s`/`--socketdir`。

`PGUSER`
:   叢集的安裝使用者名稱；對應選項 `-U`/`--username`。

<a id="id-1.9.5.13.9"></a>

## 注意事項

pg_upgrade 會建立各種工作檔案，例如綱要傾印，這些檔案儲存在新叢集目錄中的 `pg_upgrade_output.d` 內。每次執行都會建立一個以 ISO 8601 格式時間戳記（`%Y%m%dT%H%M%S`）命名的新子目錄，其所產生的所有檔案都儲存在該子目錄中。如果 pg_upgrade 成功完成，`pg_upgrade_output.d` 及其中所包含的檔案會被自動移除；但如果發生問題，其中的檔案可能會提供有用的除錯資訊。

pg_upgrade 會在新舊資料目錄中啟動短暫存在的 postmaster。預設情況下，用來與這些 postmaster 通訊的暫存 Unix socket 檔案，會建立在目前的工作目錄中。在某些情況下，目前目錄的路徑名稱可能太長，而無法成為有效的 socket 名稱。在這種情況下，你可以使用 `-s` 選項，將 socket 檔案放在某個路徑名稱較短的目錄中。基於安全考量，請確保該目錄不能被任何其他使用者讀取或寫入。（Windows 上不支援此功能。）

所有會影響你的安裝的失敗、重建與重建索引情況，pg_upgrade 都會回報；用來重建資料表與索引的升級後腳本會自動產生。如果你想要將許多叢集的升級自動化，你應該會發現，具有相同資料庫綱要的叢集，在所有叢集升級中都需要相同的升級後步驟；這是因為升級後步驟是根據資料庫綱要，而不是使用者資料。

進行部署測試時，請建立舊叢集的僅綱要副本，插入虛擬資料，然後升級該副本。

pg_upgrade 不支援升級含有使用下列 `reg*` OID 參照系統資料型別之資料表欄位的資料庫：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="type">regcollation</code></td></tr><tr><td><code class="type">regconfig</code></td></tr><tr><td><code class="type">regdictionary</code></td></tr><tr><td><code class="type">regnamespace</code></td></tr><tr><td><code class="type">regoper</code></td></tr><tr><td><code class="type">regoperator</code></td></tr><tr><td><code class="type">regproc</code></td></tr><tr><td><code class="type">regprocedure</code></td></tr></table>

（`regclass`、`regrole` 與 `regtype` 可以升級。）

如果你想使用連結模式，但不希望舊叢集在新叢集啟動時被修改，請考慮使用複製（clone）模式。如果無法使用該模式，請製作舊叢集的副本，並以連結模式升級該副本。若要製作舊叢集的有效副本，請在伺服器執行時使用 `rsync` 建立舊叢集的不一致副本（dirty copy），然後關閉舊伺服器，再次執行 `rsync --checksum`，以任何變更更新該副本，使其達到一致。（之所以需要 `--checksum`，是因為 `rsync` 的檔案修改時間精細度只有一秒。）你可能會想排除某些檔案，例如 `postmaster.pid`，如[第 25.3.4 節](../../server-administration/backup/continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)所述。如果你的檔案系統支援檔案系統快照或寫入時複製（copy-on-write）的檔案副本，你可以利用它來製作舊叢集與資料表空間的備份，不過快照與副本必須同時建立，或在資料庫伺服器停止時建立。

<a id="id-1.9.5.13.10"></a>

## 另請參閱

[initdb](app-initdb.md), [pg_ctl](app-pg-ctl.md), [pg_dump](../reference-client/app-pgdump.md), [postgres](app-postgres.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgupgrade.html)（原文版本：18.6；核對日期：2026-10-10）
