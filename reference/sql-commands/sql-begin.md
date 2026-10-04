<a id="SQL-BEGIN"></a><a id="id-1.9.3.47.1"></a>

## BEGIN

BEGIN — 開始一個交易區塊

<a id="id-1.9.3.47.4"></a>

## 語法

```

BEGIN [ WORK | TRANSACTION ] [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

<a id="id-1.9.3.47.5"></a>

## 說明

`BEGIN` 會開始一個交易區塊，也就是說，在 `BEGIN` 命令之後的所有陳述式都會在單一交易中執行，直到明確下達 [`COMMIT`](sql-commit.md) 或 [`ROLLBACK`](sql-rollback.md) 為止。預設情況下（沒有 `BEGIN` 時），PostgreSQL 會以「自動提交」（autocommit）模式執行交易，也就是說，每個陳述式都在自己的交易中執行，並在陳述式結束時隱含地執行提交（若執行成功；否則執行回復）。

在交易區塊中執行陳述式會比較快，因為交易的開始／提交需要可觀的 CPU 與磁碟活動。在一個交易內執行多個陳述式，也有助於在進行數項相關變更時確保一致性：其他工作階段將無法看到尚未完成所有相關更新的中間狀態。

若指定了隔離等級、讀寫模式或可延遲模式，新的交易就會具有這些特性，如同執行了 [`SET TRANSACTION`](sql-set-transaction.md) 一樣。

<a id="id-1.9.3.47.6"></a>

## 參數

`WORK`<br>`TRANSACTION`
:   可省略的關鍵字，沒有任何效果。

關於此陳述式其他參數的意義，請參閱 [SET TRANSACTION](sql-set-transaction.md)。

<a id="id-1.9.3.47.7"></a>

## 注意事項

[`START TRANSACTION`](sql-start-transaction.md) 具有與 `BEGIN` 相同的功能。

請使用 [`COMMIT`](sql-commit.md) 或 [`ROLLBACK`](sql-rollback.md) 結束交易區塊。

在已經位於交易區塊內時下達 `BEGIN`，會引發一則警告訊息。交易的狀態不受影響。若要在交易區塊內巢狀使用交易，請使用儲存點（請參閱 [SAVEPOINT](sql-savepoint.md)）。

基於向後相容性的理由，連續的 *`transaction_modes`* 之間的逗號可以省略。

<a id="id-1.9.3.47.8"></a>

## 範例

開始一個交易區塊：

```

BEGIN;
```

<a id="id-1.9.3.47.9"></a>

## 相容性

`BEGIN` 是 PostgreSQL 的語言擴充。它等同於 SQL 標準命令 [`START TRANSACTION`](sql-start-transaction.md)，該命令的參考頁面包含更多相容性資訊。

`DEFERRABLE` *`transaction_mode`* 是 PostgreSQL 的語言擴充。

順帶一提，`BEGIN` 關鍵字在嵌入式 SQL 中有不同的用途。移植資料庫應用程式時，建議你謹慎留意交易的語意。

<a id="id-1.9.3.47.10"></a>

## 另請參閱

[COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md), [START TRANSACTION](sql-start-transaction.md), [SAVEPOINT](sql-savepoint.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-begin.html)（原文版本：18.6；核對日期：2026-10-04）
