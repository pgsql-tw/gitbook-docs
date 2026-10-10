<a id="APP-PGCREATESUBSCRIBER"></a><a id="id-1.9.5.7.1"></a>

## pg_createsubscriber

pg_createsubscriber — 將實體複本轉換為新的邏輯複本

<a id="id-1.9.5.7.4"></a>

## 語法

<a id="id-1.9.5.7.4.1"></a>

`pg_createsubscriber` [*`option`*...] { `-d` | `--database` }*`dbname`* { `-D` | `--pgdata` }*`datadir`* { `-P` | `--publisher-server` }*`connstr`*

<a id="id-1.9.5.7.5"></a>

## 說明

pg_createsubscriber 會從實體待命伺服器建立新的邏輯複本。指定資料庫中的所有資料表都會納入[邏輯複寫](../../server-administration/logical-replication/README.md)設定。每個資料庫都會建立一組發佈與訂閱物件。它必須在目標伺服器上執行。

成功執行後，目標伺服器的狀態相當於全新的邏輯複寫設定。邏輯複寫設定與 pg_createsubscriber 的主要差異在於資料同步的方式。pg_createsubscriber 不會複製初始的資料表資料。它只執行同步階段，確保每個資料表都達到同步狀態。

pg_createsubscriber 的目標是大型資料庫系統，因為在邏輯複寫設定中，大部分時間都花在初始資料複製上。此外，花費這麼長時間同步資料的副作用，通常是有大量待套用的變更（在初始資料複製期間產生），這會進一步拉長邏輯複本可供使用前的時間。對於較小的資料庫，建議以初始資料同步的方式設定邏輯複寫。詳情請參閱 `CREATE SUBSCRIPTION` 的 [`copy_data`](../sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA) 選項。

<a id="id-1.9.5.7.6"></a>

## 選項

pg_createsubscriber 接受下列命令列引數：

`-a`<br>`--all`
:   在目標伺服器上為每個資料庫各建立一個訂閱。例外的是範本資料庫，以及不允許連線的資料庫。為了找出所有資料庫的清單，會使用 `--publisher-server` 連線字串中指定的資料庫名稱連線到來源伺服器；若未指定，則使用 `postgres` 資料庫；若該資料庫不存在，則使用 `template1`。指定此選項時，訂閱、發佈與複寫插槽會使用自動產生的名稱。此選項不能與 `--database`、`--publication`、`--replication-slot` 或 `--subscription` 一起使用。

`-d dbname`<br>`--database=dbname`
:   要在其中建立訂閱的資料庫名稱。寫出多個 `-d` 選項即可選取多個資料庫。此選項不能與 `-a` 一起使用。若未提供 `-d` 選項，資料庫名稱會從 `-P` 選項取得。若 `-d` 選項與 `-P` 選項都沒有指定資料庫名稱，且未指定 `-a` 選項，則會回報錯誤。

`-D directory`<br>`--pgdata=directory`
:   包含實體複本之叢集目錄的目標目錄。

`-n`<br>`--dry-run`
:   執行所有動作，但不實際修改目標目錄。

`-p port`<br>`--subscriber-port=port`
:   目標伺服器監聽連線的連接埠號碼。預設在連接埠 50432 上執行目標伺服器，以避免非預期的用戶端連線。

`-P connstr`<br>`--publisher-server=connstr`
:   連到發佈者的連線字串。詳情請參閱[第 32.1.1 節](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING)。

`-s dir`<br>`--socketdir=dir`
:   目標伺服器上 postmaster 通訊端所使用的目錄。預設為目前目錄。

`-t seconds`<br>`--recovery-timeout=seconds`
:   等待復原結束的最長秒數。設為 0 表示停用。預設值為 0。

`-T`<br>`--enable-two-phase`
:   為訂閱啟用 [`two_phase`](../sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) 提交。指定多個資料庫時，此選項會一致地套用到在這些資料庫上建立的所有訂閱。預設值為 `false`。

`-U username`<br>`--subscriber-username=username`
:   在目標伺服器上用來連線的使用者名稱。預設為目前的作業系統使用者名稱。

`-v`<br>`--verbose`
:   啟用詳細模式。這會使 pg_createsubscriber 將進度訊息與每個步驟的詳細資訊輸出到標準錯誤。重複指定此選項，會使額外的除錯層級訊息出現在標準錯誤上。

`--clean=objtype`
:   從目標伺服器上的指定資料庫中，移除指定類型的所有物件。

    * `publications`：
      為此訂閱者建立的 `FOR ALL TABLES` 發佈一律會被移除；指定此物件類型，會使從來源伺服器複寫過來的所有其他發佈也一併被移除。

    選定要移除的物件會逐一記錄到日誌中，包括在 `--dry-run` 期間。你沒有機會影響或停止選定物件的移除，因此請考慮先使用 pg_dump 備份這些物件。

`--config-file=filename`
:   對目標資料目錄使用指定的主要伺服器設定檔。pg_createsubscriber 內部使用 pg_ctl 命令來啟動與停止目標伺服器。若實際的 `postgresql.conf` 設定檔存放在資料目錄之外，此選項讓你能夠指定它。

`--publication=name`
:   用來設定邏輯複寫的發佈名稱。寫出多個 `--publication` 選項即可指定多個發佈。發佈名稱的數量必須與指定的資料庫數量相符，否則會回報錯誤。多個發佈名稱選項的順序必須與資料庫選項的順序相符。若未指定此選項，會為發佈名稱指派產生的名稱。此選項不能與 `--all` 一起使用。

`--replication-slot=name`
:   用來設定邏輯複寫的複寫插槽名稱。寫出多個 `--replication-slot` 選項即可指定多個複寫插槽。複寫插槽名稱的數量必須與指定的資料庫數量相符，否則會回報錯誤。多個複寫插槽名稱選項的順序必須與資料庫選項的順序相符。若未指定此選項，會以訂閱名稱作為複寫插槽名稱。此選項不能與 `--all` 一起使用。

`--subscription=name`
:   用來設定邏輯複寫的訂閱名稱。寫出多個 `--subscription` 選項即可指定多個訂閱。訂閱名稱的數量必須與指定的資料庫數量相符，否則會回報錯誤。多個訂閱名稱選項的順序必須與資料庫選項的順序相符。若未指定此選項，會為訂閱名稱指派產生的名稱。此選項不能與 `--all` 一起使用。

`-V`<br>`--version`
:   印出 pg_createsubscriber 版本後結束。

`-?`<br>`--help`
:   顯示 pg_createsubscriber 命令列引數的說明後結束。

<a id="id-1.9.5.7.7"></a>

## 注意事項

<a id="id-1.9.5.7.7.2"></a>

### 先決條件

pg_createsubscriber 要將目標伺服器轉換為邏輯複本，有一些先決條件。若不符合這些條件，會回報錯誤。來源與目標伺服器的主要版本必須與 pg_createsubscriber 相同。指定的目標資料目錄必須與來源資料目錄具有相同的系統識別碼。目標資料目錄所指定的資料庫使用者，必須具有建立[訂閱](../sql-commands/sql-createsubscription.md)以及使用 [`pg_replication_origin_advance()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE) 的權限。

目標伺服器必須作為實體待命伺服器使用。目標伺服器的 [max_active_replication_origins](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) 與 [max_logical_replication_workers](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS) 必須設定為大於或等於指定資料庫數量的值。目標伺服器的 [max_worker_processes](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 必須設定為大於指定資料庫數量的值。目標伺服器必須接受本機連線。若你打算使用 `--enable-two-phase` 選項，則還需要適當設定 [max_prepared_transactions](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PREPARED-TRANSACTIONS)。

來源伺服器必須接受來自目標伺服器的連線。來源伺服器不得處於復原狀態。來源伺服器的 [wal_level](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL) 必須為 `logical`。來源伺服器的 [max_replication_slots](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS) 必須設定為大於或等於指定資料庫數量加上現有複寫插槽數量的值。來源伺服器的 [max_wal_senders](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS) 必須設定為大於或等於「指定資料庫數量加上現有 WAL 傳送程序數量」的值。

<a id="id-1.9.5.7.7.3"></a>

### 警告

若 pg_createsubscriber 在目標伺服器被提升之後失敗，資料目錄很可能處於無法復原的狀態。在這種情況下，建議建立新的待命伺服器。

pg_createsubscriber 在轉換期間通常會以不同的連線設定啟動目標伺服器。因此，連到目標伺服器的連線應該會失敗。

由於邏輯複寫不會複寫 DDL 命令，在執行 pg_createsubscriber 期間，請避免執行會變更資料庫結構定義的 DDL 命令。若目標伺服器已經轉換為邏輯複本，DDL 命令可能不會被複寫，這可能會導致錯誤。

若 pg_createsubscriber 在處理過程中失敗，在來源伺服器上建立的物件（發佈、複寫插槽）會被移除。若目標伺服器無法連線到來源伺服器，移除可能會失敗。在這種情況下，會有警告訊息告知遺留下來的物件。若目標伺服器正在執行，它會被停止。

若複寫使用了 [primary_slot_name](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)，在邏輯複寫設定完成後，它會從來源伺服器上被移除。

若目標伺服器是同步複本，在執行 pg_createsubscriber 期間，主要伺服器上的交易提交可能會等待複寫。

除非指定了 `--enable-two-phase` 選項，否則 pg_createsubscriber 會以停用兩階段提交的方式設定邏輯複寫。這表示任何預備交易都會在 `COMMIT PREPARED` 時才被複寫，而不會事先準備。設定完成後，你可以手動移除訂閱，並以啟用 [`two_phase`](../sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) 選項的方式重新建立。

pg_createsubscriber 會使用 pg_resetwal 變更系統識別碼。這可以避免目標伺服器可能使用來源伺服器之 WAL 檔案的情況。若目標伺服器有待命伺服器，複寫將會中斷，應該建立新的待命伺服器。

若缺少必要的 WAL 檔案，可能會發生複寫失敗。為了防止這種情況，來源伺服器必須將 [max_slot_wal_keep_size](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE) 設為 `-1`，以確保必要的 WAL 檔案不會被過早移除。

<a id="id-1.9.5.7.7.4"></a>

### 運作方式

基本概念是從來源伺服器取得一個複寫起點，並設定邏輯複寫從這個起點開始：

1. 以指定的命令列選項啟動目標伺服器。若目標伺服器已在執行中，pg_createsubscriber 會以錯誤終止。
2. 檢查目標伺服器是否可以轉換。也會對來源伺服器進行一些檢查。若有任何先決條件不符合，pg_createsubscriber 會以錯誤終止。
3. 在來源伺服器上為每個指定的資料庫建立一個發佈與複寫插槽。每個發佈都以 [`FOR ALL
   TABLES`](../sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 建立。若未指定 `--publication` 選項，發佈名稱採用下列模式：「`pg_createsubscriber_%u_%x`」（參數：資料庫 *`oid`*、隨機 *`int`*）。若未指定 `--replication-slot` 選項，複寫插槽名稱採用下列模式：「`pg_createsubscriber_%u_%x`」（參數：資料庫 *`oid`*、隨機 *`int`*）。這些複寫插槽會在後續步驟中供訂閱使用。最後一個複寫插槽的 LSN 會在 [recovery_target_lsn](../../server-administration/runtime-config/runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN) 參數中作為停止點，並供訂閱作為複寫起點。這可確保不會遺失任何交易。
4. 將復原參數寫入目標資料目錄，並重新啟動目標伺服器。它會指定一個 LSN（[recovery_target_lsn](../../server-administration/runtime-config/runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN)），即復原要進行到的預寫日誌位置。它也會指定 `promote` 作為到達復原目標後伺服器應採取的動作。另外還會加入其他[復原參數](../../server-administration/runtime-config/runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)，以避免復原過程中出現非預期的行為，例如一達到一致狀態就結束復原（WAL 應該要套用到複寫起始位置為止），以及可能導致失敗的多個復原目標。當伺服器結束待命模式並開始接受讀寫交易時，此步驟即完成。若設定了 `--recovery-timeout` 選項，而復原未在指定的秒數內結束，pg_createsubscriber 會終止。
5. 在目標伺服器上為每個指定的資料庫建立一個訂閱。若未指定 `--subscription` 選項，訂閱名稱採用下列模式：「`pg_createsubscriber_%u_%x`」（參數：資料庫 *`oid`*、隨機 *`int`*）。它不會從來源伺服器複製現有資料，也不會建立複寫插槽，而是使用在先前步驟中建立的複寫插槽。訂閱會被建立，但尚未啟用。原因是在開始複寫之前，必須先將複寫進度設定到複寫起點。
6. 移除目標伺服器上那些因為建立於複寫起始位置之前而被複寫過來的發佈。它們在訂閱者上沒有用處。
7. 為每個訂閱將複寫進度設定到複寫起點。當目標伺服器開始復原程序時，它會追上複寫起點。這正是每個訂閱要作為初始複寫位置使用的確切 LSN。由於訂閱已建立，可以取得複寫來源（replication origin）名稱。複寫來源名稱與複寫起點會用於 [`pg_replication_origin_advance()`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE) 來設定初始複寫位置。
8. 在目標伺服器上為每個指定的資料庫啟用訂閱。訂閱會從複寫起點開始套用交易。
9. 若待命伺服器原本使用 [primary_slot_name](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)，從此之後它已沒有用處，因此將其移除。
10. 若待命伺服器包含[容錯移轉複寫插槽](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)，這些插槽無法再被同步，因此將其移除。
11. 更新目標伺服器上的系統識別碼。會執行 [pg_resetwal](app-pgresetwal.md) 來修改系統識別碼。由於 `pg_resetwal` 的要求，目標伺服器會被停止。

<a id="id-1.9.5.7.8"></a>

## 範例

從位於 `foo` 的實體複本，為資料庫 `hr` 與 `finance` 建立邏輯複本：

```

$ pg_createsubscriber -D /usr/local/pgsql/data -P "host=foo" -d hr -d finance
```

<a id="id-1.9.5.7.9"></a>

## 另請參閱

[pg_basebackup](../reference-client/app-pgbasebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgcreatesubscriber.html)（原文版本：18.6；核對日期：2026-10-10）
