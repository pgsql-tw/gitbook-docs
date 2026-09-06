## 67.4. 兩階段交易 [#](#TWO-PHASE)

PostgreSQL 支援兩階段提交（2PC）協定，讓多個分散式系統以交易方式共同運作。相關命令為 `PREPARE TRANSACTION`、`COMMIT PREPARED` 與 `ROLLBACK PREPARED`。兩階段交易是供外部交易管理系統使用的。PostgreSQL 遵循 X/Open XA 標準提出的功能與模型，但未實作部分較少使用的項目。

使用者執行 `PREPARE TRANSACTION` 後，接下來能用來處理該交易的命令只有 `COMMIT PREPARED` 或 `ROLLBACK PREPARED`。一般而言，這種已備妥狀態應該只持續很短的時間，但外部可用性問題可能使交易長時間停留在此狀態。短暫存在的已備妥交易只儲存在共享記憶體與 WAL 中。跨越檢查點的交易會記錄在 `pg_twophase` 目錄中。目前已備妥的交易可以使用 [`pg_prepared_xacts`](../views/view-pg-prepared-xacts.md) 檢視。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/two-phase.html)（原文版本：18.6；核對日期：2026-09-07）
