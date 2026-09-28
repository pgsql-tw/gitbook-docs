<a id="id-1.9.3.160.1"></a>

## PREPARE TRANSACTION

PREPARE TRANSACTION — 為兩階段提交準備目前的交易

## 語法

```

PREPARE TRANSACTION transaction_id
```

<a id="id-1.9.3.160.5"></a>

## 說明

`PREPARE TRANSACTION` 會為兩階段提交準備目前的交易。此指令執行後，該交易便不再與目前的工作階段相關聯；取而代之的是，該交易的狀態會完整儲存於磁碟上，即使在請求提交之前發生資料庫當機，該交易仍極有可能可以成功提交。

準備完成後，該交易之後便可以分別使用 [`COMMIT PREPARED`](sql-commit-prepared.md) 或 [`ROLLBACK PREPARED`](sql-rollback-prepared.md) 來提交或回復。這些指令可以從任何工作階段發出，不限於原先執行該交易的工作階段。

就發出指令的工作階段而言，`PREPARE TRANSACTION` 與 `ROLLBACK` 指令頗為類似：執行之後，就沒有正在進行中的目前交易，而已準備好之交易的效果也不再可見。（若該交易之後被提交，這些效果就會再次變為可見。）

若 `PREPARE TRANSACTION` 指令因任何原因失敗，它就會變成一次 `ROLLBACK`：目前的交易會被取消。

<a id="id-1.9.3.160.6"></a>

## 參數

*`transaction_id`*
:   一個任意的識別字，之後可用來在 `COMMIT PREPARED` 或 `ROLLBACK PREPARED` 中識別此交易。此識別字必須以字串常值寫出，且長度必須小於 200 位元組。它不得與任何目前已準備好之交易所使用的識別字相同。

<a id="id-1.9.3.160.7"></a>

## 注意事項

`PREPARE TRANSACTION` 並非設計供應用程式或互動式工作階段使用。它的目的是讓外部交易管理員能夠跨多個資料庫或其他交易性資源，執行原子性的全域交易。除非你正在撰寫交易管理員，否則你可能不應該使用 `PREPARE TRANSACTION`。

此指令必須在交易區塊內使用。請使用 [`BEGIN`](sql-begin.md) 來開始一個交易區塊。

目前不允許對已執行過任何涉及暫存資料表或工作階段暫存命名空間之操作、已建立任何 `WITH HOLD` 游標，或已執行過 `LISTEN`、`UNLISTEN` 或 `NOTIFY` 的交易執行 `PREPARE`。這些功能與目前的工作階段緊密相關，無法在待準備的交易中發揮作用。

若該交易曾使用 `SET`（不含 `LOCAL` 選項）修改過任何執行期參數，這些效果會在 `PREPARE TRANSACTION` 之後持續存在，且不會受到之後任何 `COMMIT PREPARED` 或 `ROLLBACK PREPARED` 的影響。因此，就這一點而言，`PREPARE TRANSACTION` 的行為比較像 `COMMIT`，而不像 `ROLLBACK`。

所有目前可用的已準備交易，都會列在 [`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md) 系統檢視表中。

### 注意

不建議讓交易長時間停留在已準備狀態。這會妨礙 `VACUUM` 回收儲存空間的能力，在極端情況下甚至可能導致資料庫為了防止交易 ID 回捲而關閉（請參閱[第 24.1.5 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)）。也請記住，該交易會持續持有它原本所持有的所有鎖定。這項功能原本設計的用法是：一旦外部交易管理員確認其他資料庫也都已準備好可以提交，已準備好的交易通常就會馬上被提交或回復。

若你尚未設定外部交易管理員來追蹤已準備好的交易並確保它們能及時結束，最好將 [max_prepared_transactions](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PREPARED-TRANSACTIONS) 設為零，停用已準備交易功能。這樣可以防止不小心建立了之後可能被遺忘、進而造成問題的已準備交易。

<a id="SQL-PREPARE-TRANSACTION-EXAMPLES"></a>

## 範例

以 `foobar` 作為交易識別字，為兩階段提交準備目前的交易：

```

PREPARE TRANSACTION 'foobar';
```

<a id="id-1.9.3.160.9"></a>

## 相容性

`PREPARE TRANSACTION` 是 PostgreSQL 的擴充功能。它是設計供外部交易管理系統使用的，這類系統有些已納入標準（例如 X/Open XA），但這些系統的 SQL 端並未標準化。

<a id="id-1.9.3.160.10"></a>

## 另請參閱

[COMMIT PREPARED](sql-commit-prepared.md), [ROLLBACK PREPARED](sql-rollback-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-prepare-transaction.html)（原文版本：18.6；核對日期：2026-09-28）
