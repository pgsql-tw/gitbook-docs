<a id="LOGICAL-REPLICATION-PUBLICATION"></a>

## 29.1. 發佈 [#](#LOGICAL-REPLICATION-PUBLICATION)

[29.1.1. 複寫識別](logical-replication-publication.md#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

*發佈（publication）* 可以定義在任何實體
複寫的主要伺服器上。定義發佈的節點稱為
*發佈者（publisher）*。發佈是由一個資料表或一組資料表
所產生的一組變更，也可以稱為
變更集或複寫集。每個發佈只存在於一個資料庫中。

發佈與綱要不同，也不會影響資料表的
存取方式。若有需要，每個資料表都可以加入多個發佈。
目前發佈只能包含資料表，以及綱要中的所有資料表。
物件必須明確加入，除非發佈是針對
`ALL TABLES` 建立的。

發佈可以選擇將其產生的變更限制為
`INSERT`、`UPDATE`、
`DELETE` 與 `TRUNCATE` 的任意組合，類似於觸發程序由
特定事件類型觸發的方式。預設情況下，所有操作類型都會被複寫。
這些發佈設定只適用於 DML 操作；它們不會影響初始
資料同步的複製。（資料列篩選器對
`TRUNCATE` 沒有作用。請參閱[第 29.4 節](logical-replication-row-filter.md)）。

每個發佈都可以有多個訂閱者。

發佈使用 [`CREATE PUBLICATION`](../../reference/sql-commands/sql-createpublication.md)
命令建立，之後可以使用對應的命令修改或刪除。

個別資料表可以使用
[`ALTER PUBLICATION`](../../reference/sql-commands/sql-alterpublication.md) 動態加入與移除。`ADD
TABLE` 與 `DROP TABLE` 操作都是
交易性的，因此一旦交易提交，該資料表就會在正確的
快照開始或停止複寫。

<a id="LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY"></a>

### 29.1.1. 複寫識別 [#](#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

已發佈的資料表必須設定*複寫識別（replica identity）*，
才能複寫 `UPDATE`
與 `DELETE` 操作，以便在訂閱者端識別出
要更新或刪除的正確資料列。

預設情況下，複寫識別是主鍵（如果有的話）。另一個唯一值索引
（需符合某些額外要求）也可以設為複寫
識別。如果資料表沒有任何合適的鍵，則可以將其設為
複寫識別 `FULL`，這表示整個資料列
都成為鍵。指定複寫識別 `FULL` 時，
訂閱者端可以使用索引來搜尋
資料列。候選索引必須是 btree 或 hash、非部分索引，且
最左側的索引欄位必須是參照已發佈資料表欄位的
欄位（而不是運算式）。這些對非唯一值索引
屬性的限制，遵循了對主鍵所強制的
部分限制。如果沒有這類合適的索引，
訂閱者端的搜尋可能會非常沒有效率，因此複寫識別
`FULL` 應該只在沒有其他
解決方案可行時作為後備手段使用。

如果在發佈者端設定了 `FULL` 以外的複寫識別，
訂閱者端也必須設定由相同或更少欄位組成的
複寫識別。

複寫識別定義為 `NOTHING`、
沒有主鍵的 `DEFAULT`，或索引已被刪除的 `USING
INDEX` 的資料表，在被納入複寫這些動作的發佈時，
無法支援 `UPDATE` 或 `DELETE` 操作。
嘗試執行這類操作會在發佈者端產生錯誤。

無論複寫識別為何，`INSERT` 操作都可以進行。

關於如何設定複寫識別的詳細資訊，請參閱 [`ALTER TABLE...REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-publication.html)（原文版本：18.6；核對日期：2026-10-10）
