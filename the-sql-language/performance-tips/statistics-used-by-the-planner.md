# 14.2. 統計資訊

## 14.2.1. 單一欄位統計資訊

正如我們在上一節中看到的那樣，查詢規劃程序需要估計查詢檢索的資料列數量，以便對查詢計劃做出正確的選擇。本節簡要介紹系統用於這些估算的統計訊息。

統計訊息的其中一部分是每個資料表和索引中的項目總數，以及每個資料表和索引佔用的磁磁區塊數。此訊息保存在資料表 [pg\_class](../../internals/system-catalogs/pg\_class.md) 中，列在 reltuples 和 relpages 欄位中。我們可以使用與此類似的查詢來查看它：

```
SELECT relname, relkind, reltuples, relpages
FROM pg_class
WHERE relname LIKE 'tenk1%';

       relname        | relkind | reltuples | relpages
----------------------+---------+-----------+----------
 tenk1                | r       |     10000 |      358
 tenk1_hundred        | i       |     10000 |       30
 tenk1_thous_tenthous | i       |     10000 |       30
 tenk1_unique1        | i       |     10000 |       30
 tenk1_unique2        | i       |     10000 |       30
(5 rows)
```

在這裡我們可以看到 tenk1 包含 10000 個資料列，其索引也是如此，但索引（不出所料）比資料表小得多。

由於效率因素，reltuples 和 relpup 並不會即時更新，因此它們通常包含一些過時的值。它們由 VACUUM，ANALYZE 和一些 DDL 指令（如 CREATE INDEX）更新。不掃描整個資料表的 VACUUM 或 ANALYZE 操作（通常是這種情況）將根據其掃描資料表的部分逐步更新 reltuples 計數，從而得到近似值。在任何情況下，規劃程序將縮放它在 pg\_class 中找到的值以匹配目前實際上資料表大小，從而獲得更接近的近似值。

由於 WHERE 子句會限制要檢查的資料列，因此大多數查詢僅檢索資料表中的一小部分行。因此，規劃程序需要估計 WHERE 子句的篩選性，即與 WHERE 子句中的每個條件匹配的資料列比率。用於此任務的訊息儲存在 [pg\_statistic](../../internals/system-catalogs/pg\_statistic.md) 系統目錄中。pg\_statistic 中的項目由 ANALYZE 和 VACUUM ANALYZE 指令更新，即使在剛更新時也都是近似值。

除了直接查看 pg\_statistic，最好在手動檢查統計訊息時查看其檢視表 [pg\_stats](../../internals/system-catalogs/pg\_stats.md)。pg\_stats 旨在於更容易閱讀。此外，所有人都可以讀取 pg\_stats，而 pg\_statistic 只能由超級使用者讀取。（這可以防止非特權使用者從統計訊息中學習有關其他人表的內容。pg\_stats 檢視表僅限於顯示目前使用者可以讀取的資料表資訊。）例如，我們可能會這樣做：

```
SELECT attname, inherited, n_distinct,
       array_to_string(most_common_vals, E'\n') as most_common_vals
FROM pg_stats
WHERE tablename = 'road';

 attname | inherited | n_distinct |          most_common_vals
---------+-----------+------------+------------------------------------
 name    | f         |  -0.363388 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp
 name    | t         |  -0.284859 | I- 880                        Ramp+
         |           |            | I- 580                        Ramp+
         |           |            | I- 680                        Ramp+
         |           |            | I- 580                            +
         |           |            | State Hwy 13                  Ramp
(2 rows)
```

請注意，同一欄位顯示兩行，一行對應於從路徑表開始的完整繼承層次結構（inherited = t），另一行僅包含路徑表本身（inherited = f）。

ANALYZE 儲存在 pg\_statistic 中的資訊量，特別是每欄位的 most\_common\_vals 和 histogram\_bounds 陣列中的最大項目數，可以使用 ALTER TABLE SET STATISTICS 指令逐個欄位設定，也可以透過設定全域的 [default\_statistics\_target](../../server-administration/server-configuration/query-planning.md#19-7-4-other-planner-options) 組態變數。預設限制目前是 100 個項目。提高限制可能允許進行更準確的計劃程序估算，特別是對於具有不規則資料分佈的欄位，其代價是在 pg\_statistic 中消耗更多空間並且計算估計的時間稍長。相反地，對於具有簡單資料分佈的欄位，下限可能就足夠了。

有關規劃程序使用統計資料的更多詳細訊息，請參閱[第 68 章](https://github.com/pgsql-tw/gitbook-docs/tree/67cc71691219133f37b9a33df9c691a2dd9c2642/tw/internals/68.-how-the-planner-uses-statistics)。

## 14.2.2. 延伸統計資訊

通常會看到執行錯誤執行計劃的緩慢查詢，因為查詢子句中使用的多個欄位是相關的。規劃程序通常假設多個條件彼此獨立，這一假設在欄位值相關時並不成立。由於每個欄位的性質，一般的統計數據無法捕獲有關跨欄位關聯的任何知識。但是，PostgreSQL 能夠計算此類信息的多變量統計訊息。

由於可能的欄位組合數量非常大，因此自動計算多變量統計數據是不切實際的。相反，可以建立延伸統計物件（通常稱為統計物件），以指示伺服器獲取有趣的欄位集合之間的統計訊息。

使用 [CREATE STATISTICS](../../reference/sql-commands/create-statistics.md) 建立統計物件，可以查看更多詳細訊息。建立這樣的物件僅建立表示對統計訊息感興趣的目錄項目。實際數據收集由 ANALYZE（手動命令或背景自動分析）執行。可以在 [pg\_statistic\_ext](../../internals/system-catalogs/pg\_statistic\_ext.md) 目錄中檢查收集的數據。

ANALYZE 根據計算一般單欄位統計訊息所需的資料表中資料列樣本計算延伸統計訊息。由於透過增加資料表或其任何欄位的統計目標來增加樣本大小（如上一節中所述），因此較大的統計目標通常會産生更準確的延伸統計訊息，但也會讓計算它們時間花費更多。

以下小節介紹了目前支援延伸統計訊息的種類。

### **14.2.2.1.** 功能相依性

最簡單的延伸統計訊息是追踪功能相依性，這是資料庫一般資料表定義中所使用的概念。我們說如果 a 的值足以決定 b 的值，那麼欄位 b 在功能上相依於欄位 a，即沒有兩個資料列具有相同的 a 值而是具有不同的 b 值。在完全正規化的資料庫中，功能相依性應僅存在於主鍵和超級鍵（superkey）上。 然而，在實務中，由於各種原因，許多資料集未完全正規化；出於效能原因的故意非正規化是一種常見的例子。即使在完全正規化的資料庫中，某些欄位之間也可能存在部分關連性，這可以表示為部分功能相依性。

功能相依性的存在直接影響某些查詢中估計的準確性。如果查詢包含獨立欄位和從屬欄位的條件，則相依欄位上的條件不會進一步減小結果大小；但是，如果不了解功能相依性，查詢計劃程序將假定條件是獨立的，從而導致低估結果大小。

為了向計劃程序告知功能相依性，ANALYZE 可以收集跨欄位相依性的度量。評估所有欄位集合之間的相依程度非常昂貴，因此數據收集僅限於在使用 dependencies 選項定義的統計物件中一起出現的那些欄位組合。建議僅為強關聯的欄位組合建立相依關係統計訊息，以避免在 ANALYZE 和以後的查詢規劃中產生不必要的開銷。

以下是收集功能相依性統計訊息的範例：

```
CREATE STATISTICS stts (dependencies) ON zip, city FROM zipcodes;

ANALYZE zipcodes;

SELECT stxname, stxkeys, stxdependencies
  FROM pg_statistic_ext
  WHERE stxname = 'stts';
 stxname | stxkeys |             stxdependencies               
---------+---------+------------------------------------------
 stts    | 1 5     | {"1 => 5": 1.000000, "5 => 1": 0.423130}
(1 row)
```

在這裡可以看出，第 1 欄位（zip code）完全決定第 5 欄位（city），因此係數為 1.0，而 city 僅在 42％ 的時間內決定 zip code，這意味著有許多城市（58％）是由多個郵政編碼所代表。

在計算涉及功能相關欄位的查詢的選擇性時，計劃程序使用相依性係數調整每個條件的選擇性估計，以便不低估它們。

#### **14.2.2.1.1.** 功能相依性的限制

功能相依性目前僅在考慮將欄位與常數值進行比較的簡單相等條件時套用。它們不會用於改善比較兩欄位或將欄位與表示式進行比較等式條件的估計，也不用於範圍子句，LIKE 或任何其他類型的條件。

在使用函數相依性進行估計時，計劃程序假定所涉及欄位的條件是相容的，因此是多餘的。如果它們不相容，則正確的估計值將為零個資料列，但不考慮這種可能性。例如，給出一個類似的查詢

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '94105';
```

規劃程序將忽視 city 子句，因為不改變選擇性，這是正確的。但是，它會做出相同的假設

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '90210';
```

即使確實有零個資料列滿足此查詢。但是，功能相依性統計訊息不能提供足夠的訊息來得到結論。

在許多實際情況中，通常會滿足這種假設; 例如，應用程序中可能存在一個 GUI，它只允許選擇要在查詢中使用的相容的城市和郵政編碼值。但如果情況並非如此，那麼功能相依性可能不是一個可行的選擇。

### **14.2.2.2.** 多變量 N-Distinct 計數

單欄位統計訊息儲存每欄位中不同值的數量。當計劃程序僅具有單欄位統計數據時，估計組合多個欄位時的不同值的數量（例如，對於 GROUP BY a, b）通常是錯誤的，從而導致它選擇錯誤的計劃。

為了改進這樣的估計，ANALYZE 可以為欄位組合收集 n 個不同的統計數據。和以前一樣，為每個可能的欄位分組執行此操作是不切實際的，因此僅為在使用 ndistinct 選項定義的統計物件中出現的那些欄位組合收集數據。將從列出的欄位集合中的兩個或更多欄位的每個可能組合收集數據。

繼續前面的範例，郵政編碼表中的 n 個不同計數可能如下所示：

```
CREATE STATISTICS stts2 (ndistinct) ON zip, state, city FROM zipcodes;

ANALYZE zipcodes;

SELECT stxkeys AS k, stxndistinct AS nd
  FROM pg_statistic_ext
  WHERE stxname = 'stts2';
-[ RECORD 1 ]--------------------------------------------------------
k  | 1 2 5
nd | {"1, 2": 33178, "1, 5": 33178, "2, 5": 27435, "1, 2, 5": 33178}
(1 row)
```

這表明有三種具有 33,178 個不同值的欄位組合：ZIP code 和 state；ZIP code 和 city；和 ZIP code，city 和 state（由於此表中的郵政編碼是唯一的，因此預計它們都是相同的）。另一方面，city 和 state 的組合只有 27,435 個不同的值。

建議僅在實際用於 GROUP 的欄位組合上建立 ndistinct 統計物件，對於那些因為群組數量錯誤估計導致錯誤計劃的組合。否則，ANALYZE 工作只是一種浪費。
