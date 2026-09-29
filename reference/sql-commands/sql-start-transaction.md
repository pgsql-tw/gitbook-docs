<a id="id-1.9.3.180.1"></a>

## START TRANSACTION

START TRANSACTION — 開始一個交易區塊

<a id="id-1.9.3.180.2"></a>

## 語法

```

START TRANSACTION [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

<a id="id-1.9.3.180.5"></a>

## 說明

本指令會開始一個新的交易區塊。若指定了隔離等級、讀寫模式，
或 deferrable 模式，新交易就會具備這些特性，如同執行了
[`SET TRANSACTION`](sql-set-transaction.md) 一般。這與
[`BEGIN`](sql-begin.md) 指令的效果相同。

<a id="id-1.9.3.180.6"></a>

## 參數

關於本陳述式各參數的意義，請參閱
[SET TRANSACTION](sql-set-transaction.md)。

<a id="id-1.9.3.180.7"></a>

## 相容性

在標準中，開始一個交易區塊並不需要發出 `START TRANSACTION`：
任何 SQL 指令都會隱含地開始一個區塊。PostgreSQL
的行為可以看作是在每個未接續在 `START TRANSACTION`
（或 `BEGIN`）之後的指令執行完畢後，隱含地發出一次
`COMMIT`，因此常被稱為「自動提交（autocommit）」。
其他關聯式資料庫系統也可能提供自動提交功能，以求方便。

`DEFERRABLE`
*`transaction_mode`*
是 PostgreSQL 的語言擴充功能。

SQL 標準要求在連續的 *`transaction_modes`* 之間使用逗號，
但基於歷史因素，PostgreSQL 允許省略逗號。

另請參閱 [SET TRANSACTION](sql-set-transaction.md) 的相容性一節。

<a id="id-1.9.3.180.8"></a>

## 參見

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md), [SAVEPOINT](sql-savepoint.md), [SET TRANSACTION](sql-set-transaction.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-start-transaction.html)（原文版本：18.6；核對日期：2026-09-28）
