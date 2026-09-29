<a id="id-1.9.3.175.1"></a>

## SET CONSTRAINTS

SET CONSTRAINTS — 設定目前交易中限制條件的檢查時機

<a id="id-1.9.3.175.2"></a>

## 語法

```

SET CONSTRAINTS { ALL | name [, ...] } { DEFERRED | IMMEDIATE }
```

<a id="id-1.9.3.175.5"></a>

## 說明

`SET CONSTRAINTS` 用來設定目前交易內限制條件檢查的行為。
`IMMEDIATE`（立即）限制條件會在每個陳述式結束時檢查。
`DEFERRED`（延遲）限制條件則要到交易提交時才會檢查。每個限制條件都有各自的
`IMMEDIATE` 或 `DEFERRED` 模式。

限制條件在建立時，會被賦予下列三種特性之一：
`DEFERRABLE INITIALLY DEFERRED`、
`DEFERRABLE INITIALLY IMMEDIATE`，或
`NOT DEFERRABLE`。第三種類別一律為
`IMMEDIATE`，且不受 `SET CONSTRAINTS` 命令影響。前兩種類別會在每個交易開始時採用所指定的模式，但其行為可在交易內以
`SET CONSTRAINTS` 更改。

`SET CONSTRAINTS` 若附上限制條件名稱清單，只會變更這些限制條件
（這些限制條件都必須是可延遲的）的模式。每個限制條件名稱都可以加上綱要名稱限定。
若未指定綱要名稱，則會使用目前的綱要搜尋路徑來找出第一個相符的名稱。
`SET CONSTRAINTS ALL` 會變更所有可延遲限制條件的模式。

當 `SET CONSTRAINTS` 將某限制條件的模式從 `DEFERRED`
改為 `IMMEDIATE` 時，新模式會回溯生效：任何原本要在交易結束時才檢查的
尚待檢查的資料修改，會改在執行 `SET CONSTRAINTS` 命令期間檢查。
若有任何這類限制條件被違反，則 `SET CONSTRAINTS`
會失敗（且不會變更限制條件模式）。因此，`SET CONSTRAINTS`
可用來強制在交易中的特定時間點進行限制條件檢查。

目前，只有 `UNIQUE`、`PRIMARY KEY`、
`REFERENCES`（外鍵）以及 `EXCLUDE`
限制條件會受此設定影響。
`NOT NULL` 與 `CHECK` 限制條件永遠會在資料列被插入或修改時立即檢查
（*而非*在陳述式結束時）。
未宣告為 `DEFERRABLE` 的唯一值與排他限制條件，同樣會被立即檢查。

宣告為「限制條件觸發程序（constraint triggers）」的觸發程序何時觸發，也受此設定控制——它們會在對應的限制條件應該被檢查的同一時間點觸發。

<a id="id-1.9.3.175.6"></a>

## 注意事項

由於 PostgreSQL 並不要求限制條件名稱在同一綱要內必須是唯一的
（只要求在同一資料表內唯一），因此指定的限制條件名稱有可能找到一筆以上的相符結果。
在這種情況下，`SET CONSTRAINTS` 會作用於所有相符的限制條件。
對於未以綱要限定的名稱，一旦在搜尋路徑中的某個綱要找到相符結果，
路徑中排在後面的綱要就不會再被搜尋。

此命令只會變更限制條件在目前交易內的行為。若在交易區塊之外執行此命令，
會發出警告，且不會產生其他任何效果。

<a id="id-1.9.3.175.7"></a>

## 相容性

此命令符合 SQL 標準所定義的行為，唯一的限制是在 PostgreSQL 中，
它不適用於 `NOT NULL` 與 `CHECK` 限制條件。
此外，PostgreSQL 會立即檢查不可延遲的唯一值限制條件，
而非如標準所建議的在陳述式結束時檢查。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-set-constraints.html)（原文版本：18.6；核對日期：2026-09-28）
