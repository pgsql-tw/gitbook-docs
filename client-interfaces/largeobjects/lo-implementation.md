<a id="LO-IMPLEMENTATION"></a>

## 33.2. 實作特性 [#](#lo-implementation) <a href="#lo-implementation" id="lo-implementation"></a>

大型物件的實作會將大型物件分割成「區塊（chunk）」，
並將這些區塊存放在資料庫的資料列中。B-tree 索引可確保在進行隨機
存取的讀取與寫入時，能快速搜尋到正確的區塊編號。

為大型物件所存放的區塊不必是連續的。
例如，若應用程式開啟一個新的大型物件，移動到位移
1000000，並在該處寫入幾個位元組，這並不會導致配置
1000000 位元組的儲存空間；只會配置涵蓋實際寫入之資料位元組範圍的區塊。
不過，讀取操作對於最後一個既有區塊之前任何未配置的位置，
都會讀出零。
這與 Unix 檔案系統中「稀疏配置（sparsely allocated）」
檔案的常見行為相符。

自 PostgreSQL 9.0 起，大型物件具有擁有者
與一組存取權限，可以使用
[GRANT](../../reference/sql-commands/sql-grant.md) 與
[REVOKE](../../reference/sql-commands/sql-revoke.md) 來管理。
讀取大型物件需要 `SELECT` 權限，
而寫入或截斷大型物件則需要
`UPDATE` 權限。
只有大型物件的擁有者（或資料庫超級使用者）可以刪除大型物件、
為其加上註解，或變更其擁有者。
若要為了與先前版本相容而調整此行為，請參閱
[lo_compat_privileges](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-LO-COMPAT-PRIVILEGES) 執行期參數。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-implementation.html)（原文版本：18.6；核對日期：2026-10-18）
