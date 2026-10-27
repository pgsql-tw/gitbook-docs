<a id="LOGICAL-REPLICATION"></a>

## 第 29 章 邏輯複寫

**目錄**

- [29.1. 發佈](logical-replication-publication.md)
  - [29.1.1. 複寫識別](logical-replication-publication.md#logical-replication-publication-replica-identity)

- [29.2. 訂閱](logical-replication-subscription.md)
  - [29.2.1. 複寫插槽管理](logical-replication-subscription.md#logical-replication-subscription-slot)

  - [29.2.2. 範例：設定邏輯複寫](logical-replication-subscription.md#logical-replication-subscription-examples)

  - [29.2.3. 範例：延後建立複寫插槽](logical-replication-subscription.md#logical-replication-subscription-examples-deferred-slot)

- [29.3. 邏輯複寫失效切換](logical-replication-failover.md)

- [29.4. 資料列篩選器](logical-replication-row-filter.md)
  - [29.4.1. 資料列篩選器規則](logical-replication-row-filter.md#logical-replication-row-filter-rules)

  - [29.4.2. 運算式限制](logical-replication-row-filter.md#logical-replication-row-filter-restrictions)

  - [29.4.3. UPDATE 轉換](logical-replication-row-filter.md#logical-replication-row-filter-transformations)

  - [29.4.4. 分割資料表](logical-replication-row-filter.md#logical-replication-row-filter-partitioned-table)

  - [29.4.5. 初始資料同步](logical-replication-row-filter.md#logical-replication-row-filter-initial-data-sync)

  - [29.4.6. 合併多個資料列篩選器](logical-replication-row-filter.md#logical-replication-row-filter-combining)

  - [29.4.7. 範例](logical-replication-row-filter.md#logical-replication-row-filter-examples)

- [29.5. 欄位清單](logical-replication-col-lists.md)
  - [29.5.1. 範例](logical-replication-col-lists.md#logical-replication-col-list-examples)

- [29.6. 產生欄位的複寫](logical-replication-gencols.md)

- [29.7. 衝突](logical-replication-conflicts.md)

- [29.8. 限制](logical-replication-restrictions.md)

- [29.9. 架構](logical-replication-architecture.md)
  - [29.9.1. 初始快照](logical-replication-architecture.md#logical-replication-snapshot)

- [29.10. 監控](logical-replication-monitoring.md)

- [29.11. 安全性](logical-replication-security.md)

- [29.12. 組態設定](logical-replication-config.md)
  - [29.12.1. 發佈者](logical-replication-config.md#logical-replication-config-publisher)

  - [29.12.2. 訂閱者](logical-replication-config.md#logical-replication-config-subscriber)

- [29.13. 升級](logical-replication-upgrade.md)
  - [29.13.1. 為發佈者升級做準備](logical-replication-upgrade.md#prepare-publisher-upgrades)

  - [29.13.2. 為訂閱者升級做準備](logical-replication-upgrade.md#prepare-subscriber-upgrades)

  - [29.13.3. 升級邏輯複寫叢集](logical-replication-upgrade.md#upgrading-logical-replication-clusters)

- [29.14. 快速設定](logical-replication-quick-setup.md)

邏輯複寫是一種根據資料物件的複寫識別（通常是主鍵）來複寫資料物件及其
變更的方法。我們使用「邏輯」一詞，是為了與實體複寫相對照；實體複寫使用確切的
區塊位址並進行逐位元組的複寫。PostgreSQL 可同時支援這兩種
機制，請參閱[第 26 章](../high-availability/README.md)。邏輯
複寫可以對資料複寫與安全性兩者進行細粒度的
控制。

邏輯複寫採用 *發佈（publish）*
與 *訂閱（subscribe）* 模型，由一個或
多個 *訂閱者（subscriber）* 訂閱
*發佈者（publisher）* 節點上的一個或多個 *發佈（publication）*。
訂閱者從其所訂閱的發佈拉取資料，之後也可以
再發佈資料，以實現串聯複寫或更複雜的
組態。

一個資料表的邏輯複寫開始時，PostgreSQL 通常會在發佈者資料庫上
為該資料表的資料建立快照，並將其複製
到訂閱者。完成後，發佈者上自初始複製以來的
變更會持續傳送到訂閱者。訂閱者
以與發佈者相同的順序套用資料，
因此對單一訂閱內的發佈而言，可以保證交易一致性。
這種資料複寫方法有時也稱為交易式複寫。

邏輯複寫的典型使用情境如下：

* 在單一資料庫或資料庫的子集發生增量變更時，
  將這些變更傳送給訂閱者。
* 在個別變更抵達訂閱者時，針對這些變更
  觸發觸發程序。
* 將多個資料庫整併為單一資料庫（例如供
  分析之用）。
* 在 PostgreSQL 的不同主要版本之間進行複寫。
* 在不同平台上的 PostgreSQL 執行個體之間進行複寫（例如
  從 Linux 到 Windows）。
* 讓不同的使用者群組存取已複寫的資料。
* 在多個資料庫之間共享資料庫的一個子集。

訂閱者資料庫的行為與其他任何 PostgreSQL
執行個體相同，也可以透過定義自己的發佈，作為其他資料庫的
發佈者。當應用程式將訂閱者視為唯讀時，
單一訂閱不會產生衝突。另一方面，
如果應用程式或其他訂閱者對同一組資料表
進行了其他寫入，就可能發生衝突。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication.html)（原文版本：18.6；核對日期：2026-10-10）
