<a id="SQL-COMMIT-PREPARED"></a><a id="id-1.9.3.54.1"></a>

## COMMIT PREPARED

COMMIT PREPARED — 提交先前已為兩階段提交而準備的交易

<a id="id-1.9.3.54.4"></a>

## 語法

```

COMMIT PREPARED transaction_id
```

<a id="id-1.9.3.54.5"></a>

## 說明

`COMMIT PREPARED` 會提交處於已準備狀態的交易。

<a id="id-1.9.3.54.6"></a>

## 參數

*`transaction_id`*
:   要提交之交易的交易識別碼。

<a id="id-1.9.3.54.7"></a>

## 注意事項

若要提交已準備的交易，你必須是最初執行該交易的同一位使用者，或是超級使用者。但你不必位於執行該交易的同一個工作階段中。

此命令不能在交易區塊內執行。已準備的交易會立即提交。

所有目前可用的已準備交易，都列在
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
系統檢視表中。

<a id="SQL-COMMIT-PREPARED-EXAMPLES"></a>

## 範例

提交以交易識別碼 `foobar` 識別的交易：

```

COMMIT PREPARED 'foobar';
```

<a id="id-1.9.3.54.9"></a>

## 相容性

`COMMIT PREPARED` 是 PostgreSQL 的擴充語法。它是供外部交易管理系統使用的，其中有些系統受標準（例如 X/Open XA）涵蓋，但這些系統的 SQL 端並未標準化。

<a id="id-1.9.3.54.10"></a>

## 另請參閱

[PREPARE TRANSACTION](sql-prepare-transaction.md), [ROLLBACK PREPARED](sql-rollback-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-commit-prepared.html)（原文版本：18.6；核對日期：2026-10-04）
