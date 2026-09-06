## 67.2. 交易與鎖定 [#](#XACT-LOCKING)

目前執行中交易的交易 ID 顯示於 [`pg_locks`](../views/view-pg-locks.md) 的 `virtualxid` 與 `transactionid` 欄位。唯讀交易有 `virtualxid`，但 `transactionid` 為 NULL；讀寫交易則會設定兩個欄位。

部分鎖定型別等待 `virtualxid`，其他則等待 `transactionid`。資料列層級的讀取與寫入鎖直接記錄在被鎖定的資料列中，可使用 [pgrowlocks](../../appendixes/contrib/pgrowlocks.md) 擴充功能檢查。資料列層級讀取鎖也可能需要指派多重交易 ID（`mxid`；請參閱[第 24.1.5.1 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xact-locking.html)（原文版本：18.6；核對日期：2026-09-06）
