<a id="id-1.9.3.167.1"></a>

## ROLLBACK

ROLLBACK — 中止目前的交易

## 語法

```

ROLLBACK [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.167.5"></a>

## 說明

`ROLLBACK` 會回復目前的交易，並使該交易所做的
所有更新都被捨棄。

<a id="id-1.9.3.167.6"></a>

## 參數

<a id="id-1.9.3.167.6.2"></a>

<a id="SQL-ROLLBACK-TRANSACTION"></a>

`WORK`<br>`TRANSACTION` [#](#SQL-ROLLBACK-TRANSACTION)
:   可省略的關鍵字，沒有任何效果。
<a id="SQL-ROLLBACK-CHAIN"></a>

`AND CHAIN` [#](#SQL-ROLLBACK-CHAIN)
:   如果指定了 `AND CHAIN`，系統會立即以與剛結束的交易相同的交易特性（請參閱
    [SET TRANSACTION](sql-set-transaction.md)），開始一個新的（未中止的）交易。否則，不會開始新的交易。

<a id="id-1.9.3.167.7"></a>

## 注意

請使用 [`COMMIT`](sql-commit.md) 來成功地
結束一個交易。

在交易區塊之外發出 `ROLLBACK` 會產生警告，
但除此之外沒有任何效果。在交易區塊之外的 `ROLLBACK AND
CHAIN` 則會產生錯誤。

<a id="id-1.9.3.167.8"></a>

## 範例

中止所有變更：

```

ROLLBACK;
```

<a id="id-1.9.3.167.9"></a>

## 相容性

`ROLLBACK` 指令符合 SQL 標準。
`ROLLBACK TRANSACTION` 這種形式則是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.167.10"></a>

## 另請參閱

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK TO SAVEPOINT](sql-rollback-to.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-rollback.html)（原文版本：18.6；核對日期：2026-09-28）
