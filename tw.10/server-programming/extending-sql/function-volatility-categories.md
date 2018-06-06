---
description: 版本：10
---

# 37.6. 函數易變性類別

每個函數都有易變性的分類，可能為 VOLATILE、STABLE 或 IMMUTABLE。如果 CREATE FUNCTION 指令沒有指定類別，則 VOLATILE 是預設值。易變性類別用於是函數最佳化時的依據：

* 一個 VOLATILE 函數可以做任何事情，包括修改資料庫。它可以使用相同的參數在連續呼叫中回傳不同的結果。優化器不對這些函數的行為做任何假設。使用 volatile 函數的查詢將在需要其值的每一個資料列重新運算該函數。
* STABLE 函數不能修改資料庫，並且保證在單個語句中給予所有資料列相同參數的情況下回傳相同的結果。此類別允許優化器將函數的多個呼叫優化為單個呼叫。 特別是，在索引掃描條件下使用包含這種函數的表示式是安全的。（由於索引掃描只會計算一次比較值，而不是每個資料列一次，因此在索引掃描條件下使用 VOLATILE 函數無效）。
* IMMUTABLE 函數不能修改資料庫，並且保證相同輸入永遠回傳相同的結果。這個類別允許最佳化時在查詢用常數參數呼叫函數時預先運算函數。例如，像 SELECT ... WHERE x = 2 + 2 這樣的查詢可以簡化為 SELECT ... WHERE x = 4，因為整數加法運算子下的函數被標記為 IMMUTABLE。

為獲得最佳化結果，您應該使用對他們有效的最嚴格的易變性類別來標記您的函數。

任何會有預期以外結果的函數必須標註為 VOLATILE，以便對其進行優化時不能被優化。即使是不會有預期以外結果的函數，如果它的值可能在單個查詢中改變，也需要標記為 VOLATILE；一些例子是 random\(\)，currval\(\)，timeofday\(\)。

另一個重要的例子是 current\_timestamp 函數家族被限定為 STABLE，因為它們的值在交易事務中不會改變。

在考慮到查詢計劃並且立即執行的簡單交互式查詢時，STABLE 和 IMMUTABLE 類別之間的差別相對較小：函數在計劃期間執行一次，或者在查詢執行啟動期間執行一次並不重要。但是，如果查詢計劃保存並稍後再使用，則會有很大差異。如果標記一個函數 IMMUTABLE，那麼它可能會在查詢計劃過程中過早地將其簡化為常數，導致在隨後的計劃使用過程中重新使用舊值。使用預準備語句或使用暫存計劃的函數語言（如PL/pgSQL）時，這會是一種風險。

對於使用 SQL 或任何標準程序語言撰寫的函數，由易變性類別確定的第二個重要屬性，即由正在呼叫該函數的 SQL 指令所做的任何資料變更的可見性。一個 VOLATILE 函數會看到這樣的變化，一個 STABLE 或 IMMUTABLE 函數則不會。此行為是使用 MVCC 的快照行為實現的（請參閱[第 13 章](../../sql/mvcc/)）：STABLE 和 IMMUTABLE 函數使用從呼叫查詢開始時所建立的快照，而 VOLATILE 函數在執行每個查詢的開始時獲取新的快照。

#### Note

Functions written in C can manage snapshots however they want, but it's usually a good idea to make C functions work this way too.

Because of this snapshotting behavior, a function containing only `SELECT` commands can safely be marked `STABLE`, even if it selects from tables that might be undergoing modifications by concurrent queries. PostgreSQL will execute all commands of a `STABLE` function using the snapshot established for the calling query, and so it will see a fixed view of the database throughout that query.

The same snapshotting behavior is used for `SELECT` commands within `IMMUTABLE` functions. It is generally unwise to select from database tables within an `IMMUTABLE` function at all, since the immutability will be broken if the table contents ever change. However, PostgreSQL does not enforce that you do not do that.

A common error is to label a function `IMMUTABLE` when its results depend on a configuration parameter. For example, a function that manipulates timestamps might well have results that depend on the [TimeZone](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TIMEZONE) setting. For safety, such functions should be labeled `STABLE` instead.

#### Note

PostgreSQL requires that `STABLE` and `IMMUTABLE` functions contain no SQL commands other than `SELECT` to prevent data modification. \(This is not a completely bulletproof test, since such functions could still call `VOLATILE` functions that modify the database. If you do that, you will find that the `STABLE` or `IMMUTABLE` function does not notice the database changes applied by the called function, since they are hidden from its snapshot.\)

