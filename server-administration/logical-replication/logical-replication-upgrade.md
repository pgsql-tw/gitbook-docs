<a id="LOGICAL-REPLICATION-UPGRADE"></a>

## 29.13. 升級 [#](#logical-replication-upgrade) <a href="#logical-replication-upgrade" id="logical-replication-upgrade"></a>

[29.13.1. 準備升級發佈者](logical-replication-upgrade.md#prepare-publisher-upgrades)

[29.13.2. 準備升級訂閱者](logical-replication-upgrade.md#prepare-subscriber-upgrades)

[29.13.3. 升級邏輯複寫叢集](logical-replication-upgrade.md#upgrading-logical-replication-clusters)

只有當舊邏輯複寫叢集的所有成員版本都是 17.0 或更新版本時，才能遷移
[*邏輯複寫叢集*](../../appendixes/glossary/README.md#glossary-logical-replication-cluster)。

<a id="PREPARE-PUBLISHER-UPGRADES"></a>

### 29.13.1. 準備升級發佈者 [#](#prepare-publisher-upgrades) <a href="#prepare-publisher-upgrades" id="prepare-publisher-upgrades"></a>

pg_upgrade 會嘗試遷移邏輯複寫插槽。
這樣可以避免你必須在新的發佈者上手動重新定義相同的
邏輯複寫插槽。只有當舊叢集版本是 17.0 或更新版本時，
才支援遷移邏輯複寫插槽。17.0 之前版本叢集上的
邏輯複寫插槽會被靜默忽略。

在開始升級發佈者叢集之前，請先確認訂閱已透過執行
[`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md)
暫時停用。升級完成後，請重新啟用該訂閱。

pg_upgrade 要能夠升級邏輯複寫插槽，需要滿足一些前置條件。
若未滿足這些條件，就會回報錯誤。

* 新叢集的
  [`wal_level`](../runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL) 必須設為
  `logical`。
* 新叢集的
  [`max_replication_slots`](../runtime-config/runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS)
  必須設定為大於或等於舊叢集中現有插槽數量的值。
* 舊叢集中插槽所參照的輸出外掛程式，必須安裝在新的
  PostgreSQL 執行檔目錄中。這些外掛程式也必須包含在新叢集的
  [output_plugin_libraries](../runtime-config/runtime-config-replication.md#GUC-OUTPUT-PLUGIN-LIBRARIES) 之中；
  安全性相關資訊請參閱該參數的說明文件。
* 舊叢集已將所有交易與邏輯解碼訊息複寫給訂閱者。
* 舊叢集上所有插槽都必須可用，也就是說，不能有任何插槽的
  [pg_replication_slots](../../internals/views/view-pg-replication-slots.md).`conflicting`
  不是 `true`。（譯註：原文此處的否定有誤：照字面是要求所有插槽的 conflicting 都為 true，也就是全部都已衝突失效；正確條件應是不得有任何 conflicting 為 true 的邏輯插槽，也就是所有邏輯插槽的 conflicting 都為 false（實體插槽的 conflicting 一律為 NULL，不在此條件範圍內）。）
* 新叢集不得有永久性邏輯複寫插槽，也就是說，
  不能有任何插槽的
  [pg_replication_slots](../../internals/views/view-pg-replication-slots.md).`temporary`
  是 `false`。

<a id="PREPARE-SUBSCRIBER-UPGRADES"></a>

### 29.13.2. 準備升級訂閱者 [#](#prepare-subscriber-upgrades) <a href="#prepare-subscriber-upgrades" id="prepare-subscriber-upgrades"></a>

在新的訂閱者上設定好 [訂閱者組態](logical-replication-config.md#logical-replication-config-subscriber)。
pg_upgrade 會嘗試遷移訂閱相依項目，
其中包括存放在
[pg_subscription_rel](../../internals/catalogs/catalog-pg-subscription-rel.md)
系統目錄中的訂閱資料表資訊，以及該訂閱的複寫來源（replication origin）。
這樣一來，新訂閱者上的邏輯複寫就能從舊訂閱者先前所在的位置
繼續進行。只有當舊叢集版本是 17.0 或更新版本時，才支援遷移
訂閱相依項目。17.0 之前版本叢集上的訂閱相依項目會被靜默忽略。

pg_upgrade 要能夠升級訂閱，需要滿足一些前置條件。
若未滿足這些條件，就會回報錯誤。

* 舊訂閱者上所有的訂閱資料表，狀態都應該是
  `i`（初始化中）或 `r`（就緒）。你可以透過檢查
  [pg_subscription_rel](../../internals/catalogs/catalog-pg-subscription-rel.md).`srsubstate`
  來確認這一點。
* 每個訂閱所對應的複寫來源項目，都應該存在於舊叢集中。
  你可以透過檢查
  [pg_subscription](../../internals/catalogs/catalog-pg-subscription.md) 與
  [pg_replication_origin](../../internals/catalogs/catalog-pg-replication-origin.md)
  系統資料表來找出這項資訊。
* 新叢集的
  [`max_active_replication_origins`](../runtime-config/runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS)
  必須設定為大於或等於舊叢集中現有訂閱數量的值。

<a id="UPGRADING-LOGICAL-REPLICATION-CLUSTERS"></a>

### 29.13.3. 升級邏輯複寫叢集 [#](#upgrading-logical-replication-clusters) <a href="#upgrading-logical-replication-clusters" id="upgrading-logical-replication-clusters"></a>

在升級訂閱者的過程中，發佈者仍然可以執行寫入操作。
這些變更會在訂閱者升級完成後，複寫到訂閱者。

### 注意

邏輯複寫的限制，同樣也適用於邏輯複寫叢集升級。
詳情請參閱[第 29.8 節](logical-replication-restrictions.md)。

發佈者升級的前置條件，同樣也適用於邏輯複寫叢集升級。
詳情請參閱[第 29.13.1 節](logical-replication-upgrade.md#prepare-publisher-upgrades)。

訂閱者升級的前置條件，同樣也適用於邏輯複寫叢集升級。
詳情請參閱[第 29.13.2 節](logical-replication-upgrade.md#prepare-subscriber-upgrades)。

### 警告

升級邏輯複寫叢集需要在多個節點上執行多個步驟。
由於並非所有操作都具有交易性，建議你依照
[第 25.3.2 節](../backup/continuous-archiving.md#backup-base-backup) 所述的方式先進行備份。

（以上為警告內容；以下步驟清單不屬於警告。）

以下詳細說明升級下列各類邏輯複寫叢集的步驟：

* 依照 [第 29.13.3.1 節](logical-replication-upgrade.md#STEPS-TWO-NODE-LOGICAL-REPLICATION-CLUSTER)
  所列步驟，升級雙節點邏輯複寫叢集。
* 依照 [第 29.13.3.2 節](logical-replication-upgrade.md#STEPS-CASCADED-LOGICAL-REPLICATION-CLUSTER)
  所列步驟，升級串接（cascaded）邏輯複寫叢集。
* 依照 [第 29.13.3.3 節](logical-replication-upgrade.md#STEPS-TWO-NODE-CIRCULAR-LOGICAL-REPLICATION-CLUSTER)
  所列步驟，升級雙節點環狀（circular）邏輯複寫叢集。

<a id="STEPS-TWO-NODE-LOGICAL-REPLICATION-CLUSTER"></a>

#### 29.13.3.1. 升級雙節點邏輯複寫叢集的步驟 [#](#STEPS-TWO-NODE-LOGICAL-REPLICATION-CLUSTER)

假設發佈者在 `node1`、訂閱者在
`node2`。訂閱者 `node2` 有一個
訂閱 `sub1_node1_node2`，用來訂閱來自
`node1` 的變更。

<a id="TWO-NODE-CLUSTER-DISABLE-SUBSCRIPTIONS-NODE2"></a>1. 使用
   [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)，
   停用 `node2` 上所有訂閱來自 `node1`
   變更的訂閱，例如：

   ```

   /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 DISABLE;
   ```
2. 停止 `node1` 上的發佈者伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1 stop
   ```
3. 使用所需的新版本，初始化 `data1_upgraded` 實例。
4. 將發佈者 `node1` 的伺服器升級到所需的
   新版本，例如：

   ```

   pg_upgrade
           --old-datadir "/opt/PostgreSQL/postgres/17/data1"
           --new-datadir "/opt/PostgreSQL/postgres/18/data1_upgraded"
           --old-bindir "/opt/PostgreSQL/postgres/17/bin"
           --new-bindir "/opt/PostgreSQL/postgres/18/bin"
   ```
5. 啟動 `node1` 上升級後的發佈者伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
   ```
6. 停止 `node2` 上的訂閱者伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data2 stop
   ```
7. 使用所需的新版本，初始化 `data2_upgraded` 實例。
8. 將訂閱者 `node2` 的伺服器升級到所需的
   新版本，例如：

   ```

   pg_upgrade
          --old-datadir "/opt/PostgreSQL/postgres/17/data2"
          --new-datadir "/opt/PostgreSQL/postgres/18/data2_upgraded"
          --old-bindir "/opt/PostgreSQL/postgres/17/bin"
          --new-bindir "/opt/PostgreSQL/postgres/18/bin"
   ```
9. 啟動 `node2` 上升級後的訂閱者伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
   ```
10. 在 `node2` 上，建立在
    [步驟 1](logical-replication-upgrade.md#TWO-NODE-CLUSTER-DISABLE-SUBSCRIPTIONS-NODE2)
    之後、到現在這段期間，在升級後的發佈者 `node1`
    伺服器上所建立的任何資料表，例如：

    ```

    /* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
    ```
11. 使用
    [`ALTER SUBSCRIPTION ... ENABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)，
    啟用 `node2` 上所有訂閱來自 `node1`
    變更的訂閱，例如：

    ```

    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
    ```
12. 使用
    [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)，
    重新整理 `node2` 訂閱的發佈，例如：

    ```

    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 REFRESH PUBLICATION;
    ```

譯註：本小節的範例程式碼依原文保留，但有兩處需留意：一是步驟 4、8 的 pg_upgrade 範例把命令與各個選項分成多行，卻沒有 shell 續行符號（行尾的 \），直接貼上執行時，各個選項會被當成獨立的命令，實際執行時請合併成一行，或除最後一行外，在各行行尾加上續行符號；二是步驟 2、5、6、9 的 pg_ctl 使用 /opt/PostgreSQL/data1、/opt/PostgreSQL/data1_upgraded 這類路徑，但對應的 pg_upgrade 使用的是 /opt/PostgreSQL/postgres/17/ 與 /opt/PostgreSQL/postgres/18/ 底下的資料目錄，兩者不一致，實際操作時 pg_ctl 與 pg_upgrade 必須指向同一組舊、新資料目錄。

### 注意

在上述步驟中，是先升級發佈者，再升級訂閱者。你也可以使用類似的
步驟，改為先升級訂閱者，再升級發佈者。

<a id="STEPS-CASCADED-LOGICAL-REPLICATION-CLUSTER"></a>

#### 29.13.3.2. 升級串接邏輯複寫叢集的步驟 [#](#STEPS-CASCADED-LOGICAL-REPLICATION-CLUSTER)

假設我們有一個串接邏輯複寫設定，
`node1`->`node2`->`node3`。
這裡 `node2` 訂閱來自
`node1` 的變更，`node3` 訂閱來自
`node2` 的變更。`node2`
有一個訂閱 `sub1_node1_node2`，用來
訂閱來自 `node1` 的變更。
`node3` 有一個訂閱
`sub1_node2_node3`，用來訂閱來自
`node2` 的變更。

<a id="CASCADED-CLUSTER-DISABLE-SUB-NODE1-NODE2"></a>1. 使用
   [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)，
   停用 `node2` 上所有訂閱來自 `node1`
   變更的訂閱，例如：

   ```

   /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 DISABLE;
   ```
2. 停止 `node1` 上的伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1 stop
   ```
3. 使用所需的新版本，初始化 `data1_upgraded` 實例。
4. 將 `node1` 的伺服器升級到所需的新
   版本，例如：

   ```

   pg_upgrade
           --old-datadir "/opt/PostgreSQL/postgres/17/data1"
           --new-datadir "/opt/PostgreSQL/postgres/18/data1_upgraded"
           --old-bindir "/opt/PostgreSQL/postgres/17/bin"
           --new-bindir "/opt/PostgreSQL/postgres/18/bin"
   ```
5. 啟動 `node1` 上升級後的伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
   ```
<a id="CASCADED-CLUSTER-DISABLE-SUB-NODE2-NODE3"></a>6. 使用
   [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)，
   停用 `node3` 上所有訂閱來自 `node2`
   變更的訂閱，例如：

   ```

   /* node3 # */ ALTER SUBSCRIPTION sub1_node2_node3 DISABLE;
   ```
7. 停止 `node2` 上的伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data2 stop
   ```
8. 使用所需的新版本，初始化 `data2_upgraded` 實例。
9. 將 `node2` 的伺服器升級到所需的
   新版本，例如：

   ```

   pg_upgrade
           --old-datadir "/opt/PostgreSQL/postgres/17/data2"
           --new-datadir "/opt/PostgreSQL/postgres/18/data2_upgraded"
           --old-bindir "/opt/PostgreSQL/postgres/17/bin"
           --new-bindir "/opt/PostgreSQL/postgres/18/bin"
   ```
10. 啟動 `node2` 上升級後的伺服器，例如：

    ```

    pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
    ```
11. 在 `node2` 上，建立在
    [步驟 1](logical-replication-upgrade.md#CASCADED-CLUSTER-DISABLE-SUB-NODE1-NODE2)
    之後、到現在這段期間，在升級後的發佈者 `node1`
    伺服器上所建立的任何資料表，例如：

    ```

    /* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
    ```
12. 使用
    [`ALTER SUBSCRIPTION ... ENABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)，
    啟用 `node2` 上所有訂閱來自 `node1`
    變更的訂閱，例如：

    ```

    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
    ```
13. 使用
    [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)，
    重新整理 `node2` 訂閱的發佈，例如：

    ```

    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 REFRESH PUBLICATION;
    ```
14. 停止 `node3` 上的伺服器，例如：

    ```

    pg_ctl -D /opt/PostgreSQL/data3 stop
    ```
15. 使用所需的新版本，初始化 `data3_upgraded` 實例。
16. 將 `node3` 的伺服器升級到所需的
    新版本，例如：

    ```

    pg_upgrade
            --old-datadir "/opt/PostgreSQL/postgres/17/data3"
            --new-datadir "/opt/PostgreSQL/postgres/18/data3_upgraded"
            --old-bindir "/opt/PostgreSQL/postgres/17/bin"
            --new-bindir "/opt/PostgreSQL/postgres/18/bin"
    ```
17. 啟動 `node3` 上升級後的伺服器，例如：

    ```

    pg_ctl -D /opt/PostgreSQL/data3_upgraded start -l logfile
    ```
18. 在 `node3` 上，建立在
    [步驟 6](logical-replication-upgrade.md#CASCADED-CLUSTER-DISABLE-SUB-NODE2-NODE3)
    之後、到現在這段期間，在升級後的 `node2` 上
    所建立的任何資料表，例如：

    ```

    /* node3 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
    ```
19. 使用
    [`ALTER SUBSCRIPTION ... ENABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)，
    啟用 `node3` 上所有訂閱來自 `node2`
    變更的訂閱，例如：

    ```

    /* node3 # */ ALTER SUBSCRIPTION sub1_node2_node3 ENABLE;
    ```
20. 使用
    [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)，
    重新整理 `node3` 訂閱的發佈，例如：

    ```

    /* node3 # */ ALTER SUBSCRIPTION sub1_node2_node3 REFRESH PUBLICATION;
    ```

譯註：本小節的範例程式碼依原文保留，但有兩處需留意：一是步驟 4、9、16 的 pg_upgrade 範例把命令與各個選項分成多行，卻沒有 shell 續行符號（行尾的 \），直接貼上執行時，各個選項會被當成獨立的命令，實際執行時請合併成一行，或除最後一行外，在各行行尾加上續行符號；二是步驟 2、5、7、10、14、17 的 pg_ctl 使用 /opt/PostgreSQL/data1、/opt/PostgreSQL/data1_upgraded 這類路徑，但對應的 pg_upgrade 使用的是 /opt/PostgreSQL/postgres/17/ 與 /opt/PostgreSQL/postgres/18/ 底下的資料目錄，兩者不一致，實際操作時 pg_ctl 與 pg_upgrade 必須指向同一組舊、新資料目錄。

<a id="STEPS-TWO-NODE-CIRCULAR-LOGICAL-REPLICATION-CLUSTER"></a>

#### 29.13.3.3. 升級雙節點環狀邏輯複寫叢集的步驟 [#](#STEPS-TWO-NODE-CIRCULAR-LOGICAL-REPLICATION-CLUSTER)

假設我們有一個環狀邏輯複寫設定，
`node1`->`node2` 及
`node2`->`node1`。這裡
`node2` 訂閱來自
`node1` 的變更，`node1` 訂閱來自
`node2` 的變更。`node1`
有一個訂閱 `sub1_node2_node1`，用來
訂閱來自 `node2` 的變更。
`node2` 有一個訂閱
`sub1_node1_node2`，用來訂閱來自
`node1` 的變更。

<a id="CIRCULAR-CLUSTER-DISABLE-SUB-NODE2"></a>1. 使用
   [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)，
   停用 `node2` 上所有訂閱來自 `node1`
   變更的訂閱，例如：

   ```

   /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 DISABLE;
   ```
2. 停止 `node1` 上的伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1 stop
   ```
3. 使用所需的新版本，初始化 `data1_upgraded` 實例。
4. 將 `node1` 的伺服器升級到所需的
   新版本，例如：

   ```

   pg_upgrade
           --old-datadir "/opt/PostgreSQL/postgres/17/data1"
           --new-datadir "/opt/PostgreSQL/postgres/18/data1_upgraded"
           --old-bindir "/opt/PostgreSQL/postgres/17/bin"
           --new-bindir "/opt/PostgreSQL/postgres/18/bin"
   ```
5. 啟動 `node1` 上升級後的伺服器，例如：

   ```

   pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
   ```
6. 使用
   [`ALTER SUBSCRIPTION ... ENABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)，
   啟用 `node2` 上所有訂閱來自 `node1`
   變更的訂閱，例如：

   ```

   /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
   ```
7. 在 `node1` 上，建立在
   [步驟 1](logical-replication-upgrade.md#CIRCULAR-CLUSTER-DISABLE-SUB-NODE2)
   之後、到現在這段期間，在 `node2` 上
   所建立的任何資料表，例如：

   ```

   /* node1 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
   ```
8. 使用
   [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)，
   重新整理 `node1` 訂閱的發佈，以便從
   `node2` 複製初始資料表資料，例如：

   ```

   /* node1 # */ ALTER SUBSCRIPTION sub1_node2_node1 REFRESH PUBLICATION;
   ```
<a id="CIRCULAR-CLUSTER-DISABLE-SUB-NODE1"></a>9. 使用
   [`ALTER SUBSCRIPTION ... DISABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)，
   停用 `node1` 上所有訂閱來自 `node2`
   變更的訂閱，例如：

   ```

   /* node1 # */ ALTER SUBSCRIPTION sub1_node2_node1 DISABLE;
   ```
10. 停止 `node2` 上的伺服器，例如：

    ```

    pg_ctl -D /opt/PostgreSQL/data2 stop
    ```
11. 使用所需的新版本，初始化 `data2_upgraded` 實例。
12. 將 `node2` 的伺服器升級到所需的
    新版本，例如：

    ```

    pg_upgrade
            --old-datadir "/opt/PostgreSQL/postgres/17/data2"
            --new-datadir "/opt/PostgreSQL/postgres/18/data2_upgraded"
            --old-bindir "/opt/PostgreSQL/postgres/17/bin"
            --new-bindir "/opt/PostgreSQL/postgres/18/bin"
    ```
13. 啟動 `node2` 上升級後的伺服器，例如：

    ```

    pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
    ```
14. 使用
    [`ALTER SUBSCRIPTION ... ENABLE`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)，
    啟用 `node1` 上所有訂閱來自 `node2`
    變更的訂閱，例如：

    ```

    /* node1 # */ ALTER SUBSCRIPTION sub1_node2_node1 ENABLE;
    ```
15. 在 `node2` 上，建立在
    [步驟 9](logical-replication-upgrade.md#CIRCULAR-CLUSTER-DISABLE-SUB-NODE1)
    之後、到現在這段期間，在升級後的 `node1` 上
    所建立的任何資料表，例如：

    ```

    /* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
    ```
16. 使用
    [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)，
    重新整理 `node2` 訂閱的發佈，以便從
    `node1` 複製初始資料表資料，例如：

    ```

    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 REFRESH PUBLICATION;
    ```

譯註：本小節的範例程式碼依原文保留，但有兩處需留意：一是步驟 4、12 的 pg_upgrade 範例把命令與各個選項分成多行，卻沒有 shell 續行符號（行尾的 \），直接貼上執行時，各個選項會被當成獨立的命令，實際執行時請合併成一行，或除最後一行外，在各行行尾加上續行符號；二是步驟 2、5、10、13 的 pg_ctl 使用 /opt/PostgreSQL/data1、/opt/PostgreSQL/data1_upgraded 這類路徑，但對應的 pg_upgrade 使用的是 /opt/PostgreSQL/postgres/17/ 與 /opt/PostgreSQL/postgres/18/ 底下的資料目錄，兩者不一致，實際操作時 pg_ctl 與 pg_upgrade 必須指向同一組舊、新資料目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-upgrade.html)（原文版本：18.6；核對日期：2026-10-23）
