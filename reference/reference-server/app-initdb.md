<a id="APP-INITDB"></a><a id="id-1.9.5.3.1"></a>

## initdb

initdb — 建立新的 PostgreSQL 資料庫叢集

## 語法

<a id="id-1.9.5.3.4.1"></a>

`initdb` [*`option`*...] [ `--pgdata` | `-D` ] *`directory`*

<a id="R1-APP-INITDB-1"></a>

## 說明

`initdb` 會建立新的 PostgreSQL [*[資料庫叢集](../../appendixes/glossary/README.md#GLOSSARY-DB-CLUSTER)*](../../appendixes/glossary/README.md#GLOSSARY-DB-CLUSTER)。

建立資料庫叢集包括：建立存放叢集資料的[*[目錄](../../appendixes/glossary/README.md#GLOSSARY-DATA-DIRECTORY)*](../../appendixes/glossary/README.md#GLOSSARY-DATA-DIRECTORY)、產生共用的系統目錄資料表（屬於整個叢集、而非任何特定資料庫的資料表），以及建立 `postgres`、`template1` 與 `template0` 資料庫。`postgres` 資料庫是供使用者、工具程式與第三方應用程式使用的預設資料庫。`template1` 與 `template0` 是作為來源資料庫，供之後的 `CREATE
DATABASE` 命令複製。`template0` 永遠不應該被修改，但你可以將物件加入 `template1`，這些物件預設會被複製到之後建立的資料庫中。詳細資訊請參閱[第 22.3 節](../../server-administration/managing-databases/manage-ag-templatedbs.md)。

雖然 `initdb` 會嘗試建立指定的資料目錄，但若預期資料目錄的上層目錄由 root 擁有，它可能沒有權限這麼做。若要在這種環境中進行初始化，請以 root 身分建立一個空的資料目錄，接著使用 `chown` 將該目錄的擁有權指派給資料庫使用者帳號，然後使用 `su` 切換為資料庫使用者來執行 `initdb`。

`initdb` 必須以將會擁有伺服器程序的使用者身分執行，因為伺服器需要存取 `initdb` 所建立的檔案與目錄。由於伺服器不能以 root 身分執行，你也不得以 root 身分執行 `initdb`。（事實上它會拒絕這麼做。）

基於安全考量，`initdb` 所建立的新叢集預設只有叢集擁有者可以存取。`--allow-group-access` 選項允許與叢集擁有者同一群組的任何使用者讀取叢集中的檔案。這對於以非特權使用者身分執行備份很有用。

`initdb` 會初始化資料庫叢集的預設區域設定與字元集編碼。這些設定也可以在建立各個資料庫時分別設定。`initdb` 會決定範本資料庫的這些設定，而這些設定將作為所有其他資料庫的預設值。

預設情況下，`initdb` 使用區域設定提供者 `libc`（請參閱[第 23.1.4 節](../../server-administration/charset/locale.md#locale-providers)）。`libc` 區域設定提供者會從環境取得區域設定，並依據區域設定決定編碼。

若要為叢集選擇不同的區域設定，請使用 `--locale` 選項。另外也有個別的 `--lc-*` 與 `--icu-locale` 選項（見下文），可以為個別的區域設定類別設定值。請注意，不同區域設定類別的設定若不一致，可能會產生無意義的結果，因此使用時應該謹慎。

或者，`initdb` 也可以透過指定 `--locale-provider=icu`，使用 ICU 函式庫來提供區域設定服務。伺服器必須在建置時加入 ICU 支援。若要選擇要套用的特定 ICU 區域設定 ID，請使用 `--icu-locale` 選項。請注意，基於實作上的原因以及為了支援舊有程式碼，即使使用 ICU 區域設定提供者，`initdb` 仍然會選擇並初始化 libc 區域設定。

`initdb` 執行時，會印出它所選擇的區域設定。若你有複雜的需求或指定了多個選項，建議檢查結果是否符合預期。

關於區域設定的更多詳細資訊，請參閱[第 23.1 節](../../server-administration/charset/locale.md)。

若要變更預設編碼，請使用 `--encoding`。更多詳細資訊請參閱[第 23.3 節](../../server-administration/charset/multibyte.md)。

<a id="id-1.9.5.3.6"></a>

## 選項

<a id="APP-INITDB-OPTION-AUTH"></a>

`-A authmethod`<br>`--auth=authmethod` [#](#APP-INITDB-OPTION-AUTH)
:   此選項指定 `pg_hba.conf` 中本機使用者所用的預設驗證方法（`host` 與 `local` 行）。有效值的概述請參閱[第 20.1 節](../../server-administration/client-authentication/auth-pg-hba-conf.md)。

    `initdb` 會使用指定的驗證方法，為非複寫連線以及複寫連線預先填入 `pg_hba.conf` 項目。

    除非你信任系統上的所有本機使用者，否則不要使用 `trust`。為了方便安裝，`trust` 是預設值。
<a id="APP-INITDB-OPTION-AUTH-HOST"></a>

`--auth-host=authmethod` [#](#APP-INITDB-OPTION-AUTH-HOST)
:   此選項指定 `pg_hba.conf` 中本機使用者透過 TCP/IP 連線時所用的驗證方法（`host` 行）。
<a id="APP-INITDB-OPTION-AUTH-LOCAL"></a>

`--auth-local=authmethod` [#](#APP-INITDB-OPTION-AUTH-LOCAL)
:   此選項指定 `pg_hba.conf` 中本機使用者透過 Unix 網域通訊端連線時所用的驗證方法（`local` 行）。
<a id="APP-INITDB-OPTION-PGDATA"></a>

`-D directory`<br>`--pgdata=directory` [#](#APP-INITDB-OPTION-PGDATA)
:   此選項指定資料庫叢集應該存放的目錄。這是 `initdb` 唯一需要的資訊，但你可以透過設定環境變數 `PGDATA` 來避免寫出它；這樣做很方便，因為資料庫伺服器（`postgres`）之後可以透過同一個變數找到資料目錄。
<a id="APP-INITDB-OPTION-ENCODING"></a>

`-E encoding`<br>`--encoding=encoding` [#](#APP-INITDB-OPTION-ENCODING)
:   選擇範本資料庫的編碼。除非你屆時另行覆寫，這也會是你之後建立之任何資料庫的預設編碼。PostgreSQL 伺服器所支援的字元集說明請見[第 23.3.1 節](../../server-administration/charset/multibyte.md#multibyte-charset-supported)。

    預設情況下，範本資料庫的編碼是由區域設定推導而來。若指定了 [`--no-locale`](app-initdb.md#APP-INITDB-OPTION-NO-LOCALE)（或等價地，若區域設定為 `C` 或 `POSIX`），則 ICU 提供者的預設編碼為 `UTF8`，`libc` 提供者的預設編碼為 `SQL_ASCII`。
<a id="APP-INITDB-ALLOW-GROUP-ACCESS"></a>

`-g`<br>`--allow-group-access` [#](#APP-INITDB-ALLOW-GROUP-ACCESS)
:   允許與叢集擁有者同一群組的使用者讀取 `initdb` 所建立的所有叢集檔案。在 Windows 上會忽略此選項，因為 Windows 不支援 POSIX 風格的群組權限。
<a id="APP-INITDB-ICU-LOCALE"></a>

`--icu-locale=locale` [#](#APP-INITDB-ICU-LOCALE)
:   指定使用 ICU 提供者時的 ICU 區域設定。區域設定支援的說明請見[第 23.1 節](../../server-administration/charset/locale.md)。
<a id="APP-INITDB-ICU-RULES"></a>

`--icu-rules=rules` [#](#APP-INITDB-ICU-RULES)
:   指定額外的定序規則，用來自訂預設定序的行為。只有 ICU 支援此功能。
<a id="APP-INITDB-DATA-CHECKSUMS"></a>

`-k`<br>`--data-checksums` [#](#APP-INITDB-DATA-CHECKSUMS)
:   在資料頁面上使用校驗和，以協助偵測 I/O 系統造成、否則不會被察覺的損毀。此功能預設為啟用；使用 [`--no-data-checksums`](app-initdb.md#APP-INITDB-NO-DATA-CHECKSUMS) 可停用校驗和。

    啟用校驗和可能會帶來些微的效能損失。若有設定，所有資料庫中的所有物件都會計算校驗和。所有校驗和失敗都會在 [`pg_stat_database`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW) 檢視表中回報。詳細資訊請參閱[第 28.2 節](../../server-administration/wal/checksums.md)。
<a id="APP-INITDB-OPTION-LOCALE"></a>

`--locale=locale` [#](#APP-INITDB-OPTION-LOCALE)
:   設定資料庫叢集的預設區域設定。若未指定此選項，區域設定會從 `initdb` 的執行環境繼承。區域設定支援的說明請見[第 23.1 節](../../server-administration/charset/locale.md)。

    若 `--locale-provider` 為 `builtin`，則必須指定 `--locale` 或 `--builtin-locale`，並將其設為 `C`、`C.UTF-8` 或 `PG_UNICODE_FAST`。
<a id="APP-INITDB-OPTION-LC-COLLATE"></a>

`--lc-collate=locale`<br>`--lc-ctype=locale`<br>`--lc-messages=locale`<br>`--lc-monetary=locale`<br>`--lc-numeric=locale`<br>`--lc-time=locale` [#](#APP-INITDB-OPTION-LC-COLLATE)
:   與 `--locale` 類似，但只設定指定類別的區域設定。
<a id="APP-INITDB-OPTION-NO-LOCALE"></a>

`--no-locale` [#](#APP-INITDB-OPTION-NO-LOCALE)
:   等同於 `--locale=C`。
<a id="APP-INITDB-BUILTIN-LOCALE"></a>

`--builtin-locale=locale` [#](#APP-INITDB-BUILTIN-LOCALE)
:   指定使用 builtin 提供者時的區域設定名稱。區域設定支援的說明請見[第 23.1 節](../../server-administration/charset/locale.md)。
<a id="APP-INITDB-OPTION-LOCALE-PROVIDER"></a>

`--locale-provider={builtin|libc|icu}` [#](#APP-INITDB-OPTION-LOCALE-PROVIDER)
:   此選項設定新叢集中所建立之資料庫的區域設定提供者。之後建立新資料庫時，可以在 `CREATE
    DATABASE` 命令中覆寫此設定。預設值為 `libc`（請參閱[第 23.1.4 節](../../server-administration/charset/locale.md#locale-providers)）。
<a id="APP-INITDB-NO-DATA-CHECKSUMS"></a>

`--no-data-checksums` [#](#APP-INITDB-NO-DATA-CHECKSUMS)
:   不啟用資料校驗和。
<a id="APP-INITDB-OPTION-PWFILE"></a>

`--pwfile=filename` [#](#APP-INITDB-OPTION-PWFILE)
:   讓 `initdb` 從檔案讀取啟動用超級使用者的密碼。檔案的第一行會被當作密碼。
<a id="APP-INITDB-OPTION-TEXT-SEARCH-CONFIG"></a>

`-T config`<br>`--text-search-config=config` [#](#APP-INITDB-OPTION-TEXT-SEARCH-CONFIG)
:   設定預設的文字搜尋設定。更多資訊請參閱 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG)。
<a id="APP-INITDB-OPTION-USERNAME"></a>

`-U username`<br>`--username=username` [#](#APP-INITDB-OPTION-USERNAME)
:   設定[*[啟動用超級使用者](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)*](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)的使用者名稱。預設為執行 `initdb` 之作業系統使用者的名稱。
<a id="APP-INITDB-OPTION-PWPROMPT"></a>

`-W`<br>`--pwprompt` [#](#APP-INITDB-OPTION-PWPROMPT)
:   讓 `initdb` 提示輸入要給啟動用超級使用者的密碼。若你不打算使用密碼驗證，這並不重要。否則，在設定好密碼之前，你將無法使用密碼驗證。
<a id="APP-INITDB-OPTION-WALDIR"></a>

`-X directory`<br>`--waldir=directory` [#](#APP-INITDB-OPTION-WALDIR)
:   此選項指定預寫式日誌應該存放的目錄。
<a id="APP-INITDB-OPTION-WAL-SEGSIZE"></a>

`--wal-segsize=size` [#](#APP-INITDB-OPTION-WAL-SEGSIZE)
:   設定 *WAL 區段大小*，單位為 MB。這是 WAL 日誌中每個個別檔案的大小。預設大小為 16 MB。此值必須是 1 到 1024（MB）之間的 2 的冪次。此選項只能在初始化時設定，之後無法變更。

    調整此大小可能有助於控制 WAL 日誌傳送或封存的粒度。此外，在 WAL 量很大的資料庫中，每個目錄中 WAL 檔案的數量本身就可能成為效能與管理上的問題。增加 WAL 檔案大小會減少 WAL 檔案的數量。

另外還有其他較不常用的選項：

<a id="APP-INITDB-OPTION-SET"></a>

`-c name=value`<br>`--set name=value` [#](#APP-INITDB-OPTION-SET)
:   在 `initdb` 執行期間，強制將伺服器參數 *`name`* 設定為 *`value`*，並同時將該設定寫入產生的 `postgresql.conf` 檔案中，使其在日後伺服器執行時也會套用。此選項可以指定超過一次，以設定多個參數。它主要適用於環境使得伺服器以預設參數完全無法啟動的情況。
<a id="APP-INITDB-OPTION-DEBUG"></a>

`-d`<br>`--debug` [#](#APP-INITDB-OPTION-DEBUG)
:   印出來自啟動用後端（bootstrap backend）的除錯輸出，以及其他一些一般大眾較不感興趣的訊息。啟動用後端是 `initdb` 用來建立系統目錄資料表的程式。此選項會產生極大量且極為乏味的輸出。
<a id="APP-INITDB-OPTION-DISCARD-CACHES"></a>

`--discard-caches` [#](#APP-INITDB-OPTION-DISCARD-CACHES)
:   以 `debug_discard_caches=1` 選項執行啟動用後端。這會花費非常長的時間，只對深入除錯有用。
<a id="APP-INITDB-OPTION-L"></a>

`-L directory` [#](#APP-INITDB-OPTION-L)
:   指定 `initdb` 應該在何處尋找用來初始化資料庫叢集的輸入檔案。通常不需要這麼做。若你需要明確指定其位置，系統會告知你。
<a id="APP-INITDB-OPTION-NO-CLEAN"></a>

`-n`<br>`--no-clean` [#](#APP-INITDB-OPTION-NO-CLEAN)
:   預設情況下，當 `initdb` 判定有錯誤使它無法完整建立資料庫叢集時，會移除它在發現無法完成工作之前可能已建立的任何檔案。此選項會阻止這項清理工作，因此對除錯很有用。
<a id="APP-INITDB-OPTION-NO-SYNC"></a>

`-N`<br>`--no-sync` [#](#APP-INITDB-OPTION-NO-SYNC)
:   預設情況下，`initdb` 會等待所有檔案都安全地寫入磁碟。此選項會讓 `initdb` 不等待就返回，這樣比較快，但也表示之後若作業系統當機，可能會使資料目錄損毀。一般而言，此選項適用於測試，但在建立正式環境的安裝時不應該使用。
<a id="APP-INITDB-OPTION-NO-SYNC-DATA-FILES"></a>

`--no-sync-data-files` [#](#APP-INITDB-OPTION-NO-SYNC-DATA-FILES)
:   預設情況下，`initdb` 會將所有資料庫檔案安全地寫入磁碟。此選項會指示 `initdb` 略過同步個別資料庫目錄中的所有檔案、資料庫目錄本身以及資料表空間目錄，也就是 `base` 子目錄中的所有內容以及任何其他資料表空間目錄。其他檔案，例如 `pg_wal` 與 `pg_xact` 中的檔案，除非同時指定了 `--no-sync` 選項，否則仍然會被同步。

    請注意，若 `--no-sync-data-files` 與 `--sync-method=syncfs` 一起使用，前述的部分或全部檔案與目錄仍會被同步，因為 `syncfs` 處理的是整個檔案系統。

    此選項主要供會另行確保被略過的檔案已同步到磁碟的工具在內部使用。
<a id="APP-INITDB-OPTION-NO-INSTRUCTIONS"></a>

`--no-instructions` [#](#APP-INITDB-OPTION-NO-INSTRUCTIONS)
:   預設情況下，`initdb` 會在輸出的結尾寫出如何啟動叢集的指示。此選項會讓這些指示被省略。這主要是供那些以平台特定行為包裝 `initdb` 的工具使用，因為在這些情況下，那些指示很可能是錯誤的。
<a id="APP-INITDB-OPTION-SHOW"></a>

`-s`<br>`--show` [#](#APP-INITDB-OPTION-SHOW)
:   顯示內部設定後結束，不做任何其他事情。這可以用來為 initdb 的安裝進行除錯。
<a id="APP-INITDB-OPTION-SYNC-METHOD"></a>

`--sync-method=method` [#](#APP-INITDB-OPTION-SYNC-METHOD)
:   設定為預設值 `fsync` 時，`initdb` 會遞迴地開啟並同步資料目錄中的所有檔案。搜尋檔案時，會跟隨 WAL 目錄與每個已設定資料表空間的符號連結。

    在 Linux 上，可以改用 `syncfs`，要求作業系統同步包含資料目錄、WAL 檔案與每個資料表空間的整個檔案系統。使用 `syncfs` 時需要注意的事項，請參閱 [recovery_init_sync_method](../../server-administration/runtime-config/runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)。

    使用 `--no-sync` 時，此選項沒有作用。
<a id="APP-INITDB-OPTION-SYNC-ONLY"></a>

`-S`<br>`--sync-only` [#](#APP-INITDB-OPTION-SYNC-ONLY)
:   將所有資料庫檔案安全地寫入磁碟後結束。這不會執行任何一般的 initdb 操作。一般而言，此選項適用於在將 [fsync](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FSYNC) 從 `off` 變更為 `on` 之後，確保能夠可靠地復原。

其他選項：

<a id="APP-INITDB-OPTION-VERSION"></a>

`-V`<br>`--version` [#](#APP-INITDB-OPTION-VERSION)
:   印出 initdb 的版本後結束。
<a id="APP-INITDB-OPTION-HELP"></a>

`-?`<br>`--help` [#](#APP-INITDB-OPTION-HELP)
:   顯示 initdb 命令列引數的說明後結束。

<a id="id-1.9.5.3.7"></a>

## 環境

<a id="APP-INITDB-ENVIRONMENT-PGDATA"></a>

`PGDATA` [#](#APP-INITDB-ENVIRONMENT-PGDATA)
:   指定資料庫叢集要存放的目錄；可以用 `-D` 選項覆寫。
<a id="APP-INITDB-ENVIRONMENT-PG-COLOR"></a>

`PG_COLOR` [#](#APP-INITDB-ENVIRONMENT-PG-COLOR)
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。
<a id="APP-INITDB-ENVIRONMENT-TZ"></a>

`TZ` [#](#APP-INITDB-ENVIRONMENT-TZ)
:   指定所建立之資料庫叢集的預設時區。此值應該是完整的時區名稱（請參閱[第 8.5.3 節](../../the-sql-language/datatype/datatype-datetime.md#datatype-timezones)）。

<a id="id-1.9.5.3.8"></a>

## 注意事項

`initdb` 也可以透過 `pg_ctl initdb` 呼叫。

<a id="id-1.9.5.3.9"></a>

## 另請參閱

[pg_ctl](app-pg-ctl.md), [postgres](app-postgres.md), [第 20.1 節](../../server-administration/client-authentication/auth-pg-hba-conf.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-initdb.html)（原文版本：18.6；核對日期：2026-10-05）
