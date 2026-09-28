<a id="id-1.9.3.168.1"></a>

## ROLLBACK PREPARED

ROLLBACK PREPARED — 取消一個先前已為兩階段提交而準備的交易

## 語法

```

ROLLBACK PREPARED transaction_id
```

<a id="id-1.9.3.168.5"></a>

## 說明

`ROLLBACK PREPARED` 會回復一個處於已準備狀態的交易。

<a id="id-1.9.3.168.6"></a>

## 參數

*`transaction_id`*
:   要被回復之交易的交易識別碼。

<a id="id-1.9.3.168.7"></a>

## 注意

若要回復一個已準備的交易，你必須是最初執行該交易的同一位使用者，或是超級使用者。但你不必身處執行該交易的同一個工作階段中。

此指令不能在交易區塊內執行。已準備的交易會被立即回復。

所有目前可用的已準備交易，都列在
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
系統檢視表中。

<a id="SQL-ROLLBACK-PREPARED-EXAMPLES"></a>

## 範例

回復以交易識別碼 `foobar` 所識別的交易：

```

ROLLBACK PREPARED 'foobar';
```

<a id="id-1.9.3.168.9"></a>

## 相容性

`ROLLBACK PREPARED` 是
PostgreSQL 的擴充功能，適用於外部交易管理系統。有些這類系統受標準（例如
X/Open XA）涵蓋，但這些系統的 SQL 端並未標準化。

<a id="id-1.9.3.168.10"></a>

## 另請參閱

[PREPARE TRANSACTION](sql-prepare-transaction.md), [COMMIT PREPARED](sql-commit-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-rollback-prepared.html)（原文版本：18.6；核對日期：2026-09-28）
