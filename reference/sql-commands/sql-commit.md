<a id="SQL-COMMIT"></a><a id="id-1.9.3.53.1"></a>

## COMMIT

COMMIT — 提交目前的交易

<a id="id-1.9.3.53.4"></a>

## 語法

```

COMMIT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.53.5"></a>

## 說明

`COMMIT` 會提交目前的交易。該交易所做的所有變更都會變得對其他人可見，並保證在發生當機時仍能持久保存。

<a id="id-1.9.3.53.6"></a>

## 參數

<a id="id-1.9.3.53.6.2"></a>

<a id="SQL-COMMIT-TRANSACTION"></a>

`WORK`<br>`TRANSACTION` [#](#SQL-COMMIT-TRANSACTION)
:   可省略的關鍵字，沒有任何效果。
<a id="SQL-COMMIT-CHAIN"></a>

`AND CHAIN` [#](#SQL-COMMIT-CHAIN)
:   若指定了 `AND CHAIN`，會立即啟動一個新交易，其交易特性（請參閱 [SET TRANSACTION](sql-set-transaction.md)）與剛結束的交易相同。否則，不會啟動新交易。

<a id="id-1.9.3.53.7"></a>

## 注意事項

使用 [ROLLBACK](sql-rollback.md) 來中止交易。

在交易外發出 `COMMIT` 不會造成損害，但會引發一則警告訊息。在交易外執行 `COMMIT AND
CHAIN` 則是錯誤。

<a id="id-1.9.3.53.8"></a>

## 範例

要提交目前的交易，並使所有變更永久生效：

```

COMMIT;
```

<a id="id-1.9.3.53.9"></a>

## 相容性

`COMMIT` 命令符合 SQL 標準。`COMMIT TRANSACTION` 這種形式是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.53.10"></a>

## 另請參閱

[BEGIN](sql-begin.md), [ROLLBACK](sql-rollback.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-commit.html)（原文版本：18.6；核對日期：2026-10-04）
