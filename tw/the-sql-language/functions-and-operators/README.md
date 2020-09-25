# 9. 函式及運算子

PostgreSQL 為內建的資料型別提供了大量的函數和運算子。使用者還可以定義自己的函數和運算子，如[第 V 部分](../../server-programming/)所述。psql 指令 \df 和 \do 可分別用於列出所有可用的函數和運算子。

The notation used throughout this chapter to describe the argument and result data types of a function or operator is like this:

```text
repeat ( text, integer ) → text
```

which says that the function `repeat` takes one text and one integer argument and returns a result of type text. The right arrow is also used to indicate the result of an example, thus:

```text
repeat('Pg', 4) → PgPgPgPg
```

如果您擔心可移植性，那麼請注意，本章中描述的大多數函數和運算子（最常見的算術運算子和比較運算子以及一些明確標記的函數除外）都不是由 SQL 標準指定的。其他一些 SQL 資料庫管理系統提供了其中一些延伸功能，並且在許多情況下，這些功能在各種實作之間是相容和一致的。本章可能不夠完整；附加功能出現在手冊的其他相關章節中。

