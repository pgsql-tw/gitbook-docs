## 第 13 章 並行控制

**目錄**

[13.1. 簡介](mvcc-intro.md)

[13.2. 交易隔離](transaction-iso.md)
:   [13.2.1. Read Committed 隔離等級](transaction-iso.md#XACT-READ-COMMITTED)

    [13.2.2. Repeatable Read 隔離等級](transaction-iso.md#XACT-REPEATABLE-READ)

    [13.2.3. Serializable 隔離等級](transaction-iso.md#XACT-SERIALIZABLE)

[13.3. 明確鎖定](explicit-locking.md)
:   [13.3.1. 資料表層級鎖定](explicit-locking.md#LOCKING-TABLES)

    [13.3.2. 資料列層級鎖定](explicit-locking.md#LOCKING-ROWS)

    [13.3.3. 頁面層級鎖定](explicit-locking.md#LOCKING-PAGES)

    [13.3.4. 死結](explicit-locking.md#LOCKING-DEADLOCKS)

    [13.3.5. 諮詢鎖定](explicit-locking.md#ADVISORY-LOCKS)

[13.4. 應用程式層級的資料一致性檢查](applevel-consistency.md)
:   [13.4.1. 以 Serializable 交易確保一致性](applevel-consistency.md#SERIALIZABLE-CONSISTENCY)

    [13.4.2. 以明確的阻擋式鎖定確保一致性](applevel-consistency.md#NON-SERIALIZABLE-CONSISTENCY)

[13.5. 序列化失敗的處理](mvcc-serialization-failure-handling.md)

[13.6. 注意事項](mvcc-caveats.md)

[13.7. 鎖定與索引](locking-indexes.md)

<a id="id-1.5.12.2"></a>

本章說明當兩個或更多工作階段同時嘗試存取相同資料時，PostgreSQL 資料庫系統的行為。在這種情況下的目標，是在維持嚴格資料完整性的同時，讓所有工作階段都能有效率地存取資料。每一位資料庫應用程式的開發人員都應該熟悉本章所涵蓋的主題。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc.html)（原文版本：18.6；核對日期：2026-09-11）
