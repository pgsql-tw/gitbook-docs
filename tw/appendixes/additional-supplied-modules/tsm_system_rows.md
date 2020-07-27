# F.41. tsm\_system\_rows

tsm\_system\_rows 模組提供資料表抽樣方法 SYSTEM\_ROWS，此方法可在 [SELECT](../../reference/sql-commands/select.md) 指令的 TABLESAMPLE 子句中使用。

此資料表抽樣方法接受整數的參數，該參數是要讀取的最大資料筆數。除非資料表沒有足夠的資料，結果樣本將恰好包含那麼多筆資料；否則在這種情況下，將回傳整個資料表。

像內建的 SYSTEM 抽樣方法一樣，SYSTEM\_ROWS 執行區塊策略抽樣，因此抽樣並不是完全隨機的，但可能會有些群聚的效應，尤其是在僅要求少量資料的情況下。

SYSTEM\_ROWS 不支援 REPEATABLE 子句。

## F.41.1. 範例

使用 SYSTEM\_ROWS 選擇資料表樣本的範例。首先要安裝延伸功能：

```text
CREATE EXTENSION tsm_system_rows;
```

然後，您可以在 SELECT 指令中使用它，例如：

```text
SELECT * FROM my_table TABLESAMPLE SYSTEM_ROWS(100);
```

此命令將從資料表 my\_table 回傳 100 筆資料的樣本（除非該資料表沒有 100 筆資料，在這種情況下將回傳其所有資料）。

