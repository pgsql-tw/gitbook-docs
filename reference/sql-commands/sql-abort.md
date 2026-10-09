<a id="SQL-ABORT"></a><a id="id-1.9.3.3.1"></a>

## ABORT

ABORT — 中止目前的交易

<a id="id-1.9.3.3.4"></a>

## 語法

```

ABORT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.3.5"></a>

## 說明

`ABORT` 會回復目前的交易，並使該交易所做的所有更新都被捨棄。此命令的行為與標準 SQL 命令 [`ROLLBACK`](sql-rollback.md) 完全相同，僅因歷史因素而存在。

<a id="id-1.9.3.3.6"></a>

## 參數

`WORK`<br>`TRANSACTION`
:   可省略的關鍵字，沒有任何效果。

`AND CHAIN`
:   若指定 `AND CHAIN`，會立即以與剛結束的交易相同的交易特性（請參閱 [`SET TRANSACTION`](sql-set-transaction.md)）開始一個新的交易。否則，不會開始新的交易。

<a id="id-1.9.3.3.7"></a>

## 注意事項

請使用 [`COMMIT`](sql-commit.md) 來成功結束交易。

在交易區塊之外發出 `ABORT` 會產生警告，除此之外沒有任何作用。

<a id="id-1.9.3.3.8"></a>

## 範例

若要中止所有變更：

```

ABORT;
```

<a id="id-1.9.3.3.9"></a>

## 相容性

此命令是因歷史因素而存在的 PostgreSQL 擴充語法。`ROLLBACK` 是等效的標準 SQL 命令。

<a id="id-1.9.3.3.10"></a>

## 另請參閱

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-abort.html)（原文版本：18.6；核對日期：2026-10-09）
