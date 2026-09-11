<a id="MVCC-CAVEATS"></a>

## 13.6. 注意事項 [#](#MVCC-CAVEATS)

有些 DDL 指令（目前只有 [`TRUNCATE`](../../reference/sql-commands/sql-truncate.md) 與會重寫資料表的 [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 形式）並不是 MVCC 安全的。這表示在截斷或重寫提交之後，如果並行交易使用的是在該 DDL 指令提交之前所取得的快照，資料表對它們而言會顯示為空的。這只會對在 DDL 指令開始之前沒有存取過該資料表的交易造成問題；任何存取過該資料表的交易，至少都會持有一個 `ACCESS SHARE` 資料表鎖定，而這會阻擋 DDL 指令，直到該交易完成為止。因此，這些指令不會讓對目標資料表的連續查詢看到任何明顯的資料表內容不一致，但可能會造成目標資料表與資料庫中其他資料表的內容之間出現可見的不一致。

熱備援（hot standby）複寫目標（說明見[第 26.4 節](../../server-administration/high-availability/hot-standby.md)）尚未支援 Serializable 交易隔離等級。目前在熱備援模式下支援的最嚴格隔離等級是 Repeatable Read。雖然在主要伺服器上將所有永久性的資料庫寫入都放在 Serializable 交易中執行，可以確保所有備援伺服器最終都會達到一致的狀態，但在備援伺服器上執行的 Repeatable Read 交易，有時可能會看到與主要伺服器上交易的任何循序執行都不一致的暫時狀態。

對系統目錄的內部存取並不會使用目前交易的隔離等級。這表示新建立的資料庫物件（例如資料表），對並行的 Repeatable Read 與 Serializable 交易而言是可見的，即使它們所包含的資料列並不可見。相對地，在較高的隔離等級下，明確檢查系統目錄的查詢不會看到代表並行建立之資料庫物件的資料列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc-caveats.html)（原文版本：18.6；核對日期：2026-09-11）
