# F.47. tsm\_system\_time

tsm\_system\_time 模組提供資料表抽樣方法 SYSTEM\_TIME，此方法可在 [SELECT](../../reference/sql-commands/select.md) 指令的 TABLESAMPLE 子句中使用。

此資料表抽樣方法接受一個浮點數參數，該參數是讀取資料表所花費的最大毫秒數(milliseconds)。這使您可以直接控制查詢所花費的時間，而代價是樣本大小變得難以預測。結果樣本將包含在指定時間內可以讀取的盡可能多的資料，除非已經讀取了整個資料表。

像內建的 SYSTEM 抽樣方法一樣，SYSTEM\_ROWS 執行區塊策略抽樣，因此抽樣並不是完全隨機的，但可能會有些群聚的效應，尤其是在僅要求少量資料的情況下。

SYSTEM\_ROWS 不支援 REPEATABLE 子句。

## F.47.1. Examples

這是一個使用 SYSTEM\_TIME 選擇資料表樣本的範例。首先要安裝延伸功能：

```
CREATE EXTENSION tsm_system_time;
```

然後，您可以在 SELECT 指令中使用它，例如：

```
SELECT * FROM my_table TABLESAMPLE SYSTEM_TIME(1000);
```

此指令將回傳 1 秒鐘（1,000 毫秒）內讀取 my\_table 的樣本。 當然，如果可以在 1 秒內讀取整個資料表，則將回傳其所有資料。
