<a id="SQL-END"></a><a id="id-1.9.3.146.1"></a>

## END

END — 提交目前的交易

<a id="id-1.9.3.146.4"></a>

## 語法

```

END [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.146.5"></a>

## 說明

`END` 會提交目前的交易。該交易所做的所有變更都會變得對其他人可見，並保證在發生當機時仍能持久保存。此命令是 PostgreSQL 的擴充功能，等同於 [`COMMIT`](sql-commit.md)。

<a id="id-1.9.3.146.6"></a>

## 參數

`WORK`<br>`TRANSACTION`
:   可選的關鍵字。它們沒有任何作用。

`AND CHAIN`
:   若指定了 `AND CHAIN`，會立即啟動一個新交易，其交易特性（請參閱 [SET TRANSACTION](sql-set-transaction.md)）與剛結束的交易相同。否則，不會啟動新交易。

<a id="id-1.9.3.146.7"></a>

## 注意事項

使用 [`ROLLBACK`](sql-rollback.md) 來中止交易。

在交易外發出 `END` 不會造成損害，但會引發一則警告訊息。

<a id="id-1.9.3.146.8"></a>

## 範例

提交目前的交易，並使所有變更永久生效：

```

END;
```

<a id="id-1.9.3.146.9"></a>

## 相容性

`END` 是 PostgreSQL 的擴充功能，提供與 [`COMMIT`](sql-commit.md) 等同的功能，而 COMMIT 是 SQL 標準所規定的命令。

<a id="id-1.9.3.146.10"></a>

## 另請參閱

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-end.html)（原文版本：18.6；核對日期：2026-10-03）
