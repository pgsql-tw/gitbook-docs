<a id="LOGICAL-REPLICATION-RESTRICTIONS"></a>

## 29.8. 限制 [#](#LOGICAL-REPLICATION-RESTRICTIONS)

邏輯複寫目前有以下限制或尚未提供的功能。這些項目未來版本可能會加以改善。

* 資料庫綱要與 DDL 指令不會被複寫。初始綱要可以使用
  `pg_dump --schema-only` 手動複製。後續的綱要變更
  則需要手動保持同步。（不過請注意，兩端的綱要並不需要
  完全相同。）當即時運作中的資料庫綱要定義發生變更時，
  邏輯複寫仍能穩健運作：當發布端的綱要變更，而複寫的資料
  開始送達訂閱端，但卻無法對應到資料表綱要時，複寫會持續
  出現錯誤，直到綱要更新為止。在許多情況下，只要先對
  訂閱端套用新增式的綱要變更，就能避免這種間歇性的錯誤。
* 序列資料不會被複寫。由序列支援的 serial 或 identity
  欄位中的資料，當然會隨著資料表一起被複寫，但序列本身
  在訂閱端仍會顯示起始值。如果訂閱端是作為唯讀資料庫使用，
  這通常不會造成問題。但如果打算將訂閱端資料庫用於某種
  切換或容錯移轉情境，那麼序列就需要被更新到最新的值，
  可以透過從發布端複製目前的資料（或許可使用
  `pg_dump`），或是從資料表本身判斷出一個
  足夠高的值來達成。
* 系統支援複寫 `TRUNCATE` 指令，但在截斷以
  外鍵相連的資料表群組時，必須格外小心。在複寫截斷動作時，
  訂閱端會截斷發布端上被截斷的同一個資料表群組，
  無論這個群組是明確指定的，還是透過 `CASCADE`
  隱含收集而來，但會排除不屬於該訂閱的資料表。如果所有受
  影響的資料表都屬於同一個訂閱，這樣就能正確運作。但如果
  訂閱端上要被截斷的某些資料表，與不屬於同一個（或任何）
  訂閱的資料表之間存在外鍵連結，那麼在訂閱端套用截斷動作
  就會失敗。
* 大型物件（見[第 33 章](../../client-interfaces/largeobjects/README.md)）不會被複寫。
  除了將資料存放在一般資料表中之外，沒有其他變通方法。
* 複寫僅支援資料表，包括分區資料表。若嘗試複寫其他類型的
  關聯，例如檢視表、實體化檢視表或外部資料表，則會導致錯誤。
* 在分區資料表之間進行複寫時，實際的複寫預設是從發布端的
  葉分區發起，因此發布端的分區，也必須以有效目標資料表的
  形式存在於訂閱端。（它們可以本身就是葉分區，也可以進一步
  被再分區，甚至可以是獨立的資料表。）發布也可以指定改為
  依照分區根資料表的識別與綱要來複寫異動，而不是依照實際
  發生異動的個別葉分區（詳見 `CREATE PUBLICATION` 的
  [`publish_via_partition_root`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT)
  參數）。
* 在已發布的資料表上使用
  [`REPLICA IDENTITY FULL`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL)
  時，必須注意一點：如果資料表中含有沒有 B-tree 或 Hash
  預設運算子類別的資料型別（例如 point 或 box）的屬性，
  則 `UPDATE` 與 `DELETE` 操作將無法套用到
  訂閱端。不過，只要確保該資料表已定義主鍵或複寫識別，
  就能克服這項限制。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-restrictions.html)（原文版本：18.6；核對日期：2026-09-25）
