<a id="PLANNER-STATS"></a>

## 14.2. 規劃器使用的統計資訊 [#](#PLANNER-STATS)

[14.2.1. 單一欄位統計資訊](planner-stats.md#PLANNER-STATS-SINGLE-COLUMN)

[14.2.2. 擴充統計資訊](planner-stats.md#PLANNER-STATS-EXTENDED)

<a id="id-1.5.13.5.2"></a><a id="PLANNER-STATS-SINGLE-COLUMN"></a>

### 14.2.1. 單一欄位統計資訊 [#](#PLANNER-STATS-SINGLE-COLUMN)

如同我們在上一節所看到的，查詢規劃器需要估計查詢會取得的資料列數量，才能對查詢計畫做出良好的選擇。本節將簡要介紹系統用來進行這些估計的統計資訊。

統計資訊的其中一個組成部分，是每個資料表與索引中的項目總數，以及每個資料表與索引所占用的磁碟區塊數。這些資訊保存在資料表 [`pg_class`](../../internals/catalogs/catalog-pg-class.md) 的 `reltuples` 與 `relpages` 欄位中。我們可以用類似下面的查詢來查看它：

```

SELECT relname, relkind, reltuples, relpages
FROM pg_class
WHERE relname LIKE 'tenk1%';

       relname        | relkind | reltuples | relpages
----------------------+---------+-----------+----------
 tenk1                | r       |     10000 |      345
 tenk1_hundred        | i       |     10000 |       11
 tenk1_thous_tenthous | i       |     10000 |       30
 tenk1_unique1        | i       |     10000 |       30
 tenk1_unique2        | i       |     10000 |       30
(5 rows)
```

在這裡我們可以看到，`tenk1` 包含 10000 筆資料列，它的索引也是如此，但索引（不出所料）比資料表小得多。

基於效率考量，`reltuples` 與 `relpages` 不會即時更新，因此它們通常包含有些過時的值。它們會由 `VACUUM`、`ANALYZE` 以及少數 DDL 命令（例如 `CREATE INDEX`）更新。沒有掃描整個資料表的 `VACUUM` 或 `ANALYZE` 操作（這是常見的情況），會根據它所掃描的那部分資料表逐步更新 `reltuples` 計數，因此得到的是近似值。無論如何，規劃器都會依照目前資料表的實體大小，按比例調整它在 `pg_class` 中找到的值，從而得到更接近的近似值。

<a id="id-1.5.13.5.3.5"></a>

由於 `WHERE` 子句會限制要檢查的資料列，大多數查詢只會取得資料表中一部分的資料列。因此，規劃器需要估計 `WHERE` 子句的*選擇率*（selectivity），也就是符合 `WHERE` 子句中每個條件之資料列所占的比例。用於這項工作的資訊，儲存在 [`pg_statistic`](../../internals/catalogs/catalog-pg-statistic.md) 系統目錄中。`pg_statistic` 中的項目由 `ANALYZE` 與 `VACUUM ANALYZE` 命令更新，而且即使剛更新過，也一律是近似值。

<a id="id-1.5.13.5.3.7"></a>

手動檢查統計資訊時，與其直接查看 `pg_statistic`，不如查看它的視圖 [`pg_stats`](../../internals/views/view-pg-stats.md)。`pg_stats` 的設計比較容易閱讀。此外，`pg_stats` 所有人都可以讀取，而 `pg_statistic` 只有超級使用者可以讀取。（這可以防止沒有權限的使用者從統計資訊中得知其他人資料表的內容。`pg_stats` 視圖只會顯示目前使用者可以讀取之資料表的相關資料列。）例如，我們可以這樣做：

```

SELECT attname, inherited, n_distinct,
       array_to_string(most_common_vals, E'\n') as most_common_vals
FROM pg_stats
WHERE tablename = 'road';

 attname | inherited | n_distinct |          most_common_vals
---------+-----------+------------+------------------------------------
 name    | f         | -0.5681108 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp+
         |           |            | I- 80                         Ramp+
         |           |            | 14th                          St  +
         |           |            | I- 880                            +
         |           |            | Mac Arthur                    Blvd+
         |           |            | Mission                       Blvd+
...
 name    | t         |    -0.5125 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp+
         |           |            | I- 80                         Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 880                            +
         |           |            | State Hwy 13                  Ramp+
         |           |            | I- 80                             +
         |           |            | State Hwy 24                  Ramp+
...
 thepath | f         |          0 |
 thepath | t         |          0 |
(4 rows)
```

請注意，同一個欄位顯示了兩筆資料列，一筆對應從 `road` 資料表開始的完整繼承階層（`inherited`=`t`），另一筆則只包含 `road` 資料表本身（`inherited`=`f`）。（為了簡潔起見，我們只顯示了 `name` 欄位的前十個最常見值。）

`ANALYZE` 儲存在 `pg_statistic` 中的資訊量，特別是每個欄位的 `most_common_vals` 與 `histogram_bounds` 陣列中的最大項目數，可以使用 `ALTER TABLE SET STATISTICS` 命令逐欄設定，或藉由設定組態變數 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 進行全域設定。目前預設的上限是 100 個項目。提高上限也許能讓規劃器做出更準確的估計，特別是對於資料分布不規則的欄位，代價則是在 `pg_statistic` 中占用更多空間，並稍微多花一些時間計算估計值。相反地，對於資料分布單純的欄位，較低的上限可能就已足夠。

關於規劃器如何使用統計資訊的更多細節，請參閱[第 69 章](../../internals/planner-stats-details/README.md)。

<a id="PLANNER-STATS-EXTENDED"></a>

### 14.2.2. 擴充統計資訊 [#](#PLANNER-STATS-EXTENDED)

<a id="id-1.5.13.5.4.2"></a><a id="id-1.5.13.5.4.3"></a><a id="id-1.5.13.5.4.4"></a><a id="id-1.5.13.5.4.5"></a>

由於查詢子句中使用的多個欄位彼此相關，而使慢速查詢採用了不好的執行計畫，是很常見的情況。規劃器通常會假設多個條件彼此獨立，但當欄位值彼此相關時，這個假設就不成立。一般的統計資訊由於是針對個別欄位的，因此無法掌握任何關於跨欄位相關性的知識。不過，PostgreSQL 能夠計算*多變量統計資訊*（multivariate statistics），可以掌握這類資訊。

由於可能的欄位組合數量非常龐大，自動計算多變量統計資訊並不切實際。取而代之的是，可以建立*擴充統計資訊物件*（extended statistics object，更常直接稱為*統計資訊物件*），指示伺服器針對感興趣的欄位集合取得跨欄位的統計資訊。

統計資訊物件是使用 [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md) 命令建立的。建立這樣的物件，只是在系統目錄中建立一個表示對該統計資訊感興趣的項目。實際的資料收集由 `ANALYZE`（手動命令或背景的自動分析）執行。收集到的值可以在 [`pg_statistic_ext_data`](../../internals/catalogs/catalog-pg-statistic-ext-data.md) 系統目錄中查看。

`ANALYZE` 計算擴充統計資訊時，所依據的資料表資料列樣本，與它計算一般單一欄位統計資訊時所取的樣本相同。由於提高資料表或其任一欄位的統計目標（如上一節所述）會增加樣本大小，因此較大的統計目標通常會產生更準確的擴充統計資訊，但計算它們所花的時間也會更多。

下列小節說明目前支援的擴充統計資訊種類。

<a id="PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS"></a>

#### 14.2.2.1. 函數相依性 [#](#PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS)

最簡單的一種擴充統計資訊會追蹤*函數相依性*（functional dependency），這是在定義資料庫正規形式時所使用的概念。如果知道 `a` 的值就足以決定 `b` 的值，也就是說，不存在兩筆 `a` 值相同但 `b` 值不同的資料列，我們就說欄位 `b` 函數相依於欄位 `a`。在完全正規化的資料庫中，函數相依性應該只存在於主鍵與超鍵上。不過在實務上，許多資料集由於各種原因並未完全正規化；為了效能而刻意反正規化就是常見的例子。即使在完全正規化的資料庫中，某些欄位之間也可能存在部分相關性，這可以表示為部分函數相依性。

函數相依性的存在，會直接影響某些查詢中估計的準確度。如果查詢同時包含對獨立欄位與相依欄位的條件，那麼相依欄位上的條件並不會進一步縮小結果的大小；但如果不知道這項函數相依性，查詢規劃器就會假設這些條件彼此獨立，導致低估結果的大小。

為了讓規劃器得知函數相依性，`ANALYZE` 可以收集跨欄位相依性的量測值。評估所有欄位集合之間的相依程度會耗費過高的成本，因此資料收集只限於一起出現在以 `dependencies` 選項定義之統計資訊物件中的那些欄位群組。建議只為高度相關的欄位群組建立 `dependencies` 統計資訊，以避免在 `ANALYZE` 與之後的查詢規劃中產生不必要的額外負擔。

以下是收集函數相依性統計資訊的範例：

```

CREATE STATISTICS stts (dependencies) ON city, zip FROM zipcodes;

ANALYZE zipcodes;

SELECT stxname, stxkeys, stxddependencies
  FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid)
  WHERE stxname = 'stts';
 stxname | stxkeys |             stxddependencies
---------+---------+------------------------------------------
 stts    | 1 5     | {"1 => 5": 1.000000, "5 => 1": 0.423130}
(1 row)
```

在這裡可以看到，第 1 欄（郵遞區號）完全決定了第 5 欄（城市），因此係數為 1.0；而城市只有大約 42% 的時候能決定郵遞區號，這表示有許多城市（58%）是以不只一個郵遞區號來表示的。

計算涉及函數相依欄位之查詢的選擇率時，規劃器會使用相依係數來調整每個條件的選擇率估計值，以免產生低估。

<a id="PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS-LIMITS"></a>

##### 14.2.2.1.1. 函數相依性的限制 [#](#PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS-LIMITS)

目前，函數相依性只會在考量將欄位與常數值比較的簡單相等條件，以及帶有常數值的 `IN` 子句時套用。它們不會用來改善比較兩個欄位或比較欄位與運算式之相等條件的估計，也不會用於範圍子句、`LIKE` 或任何其他類型的條件。

使用函數相依性進行估計時，規劃器會假設相關欄位上的條件是相容的，因此是多餘的。如果它們不相容，正確的估計應該是零筆資料列，但這種可能性並不會被考慮。例如，給定下面這樣的查詢

```

SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '94105';
```

規劃器會忽略 `city` 子句，認為它不會改變選擇率，這是正確的。然而，它對下面這個查詢也會做出相同的假設

```

SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '90210';
```

即使實際上沒有任何資料列能滿足這個查詢。不過，函數相依性統計資訊並未提供足夠的資訊來得出這個結論。

在許多實際情況下，這個假設通常都能滿足；例如，應用程式中可能有一個 GUI，只允許選取相容的城市與郵遞區號值來用於查詢。但如果不是這樣，函數相依性可能就不是可行的選擇。

<a id="PLANNER-STATS-EXTENDED-N-DISTINCT-COUNTS"></a>

#### 14.2.2.2. 多變量相異值計數 [#](#PLANNER-STATS-EXTENDED-N-DISTINCT-COUNTS)

單一欄位統計資訊會儲存每個欄位中相異值的數量。當規劃器只有單一欄位的統計資料時，對於組合多個欄位時的相異值數量估計（例如用於 `GROUP BY a, b`）往往是錯誤的，導致它選擇不好的計畫。

為了改善這類估計，`ANALYZE` 可以收集欄位群組的相異值（n-distinct）統計資訊。和前面一樣，對每一種可能的欄位分組都這麼做並不切實際，因此只會為一起出現在以 `ndistinct` 選項定義之統計資訊物件中的欄位群組收集資料。資料會針對所列欄位集合中，由兩個或更多欄位組成的每一種可能組合進行收集。

延續前面的範例，郵遞區號資料表中的相異值計數可能如下所示：

```

CREATE STATISTICS stts2 (ndistinct) ON city, state, zip FROM zipcodes;

ANALYZE zipcodes;

SELECT stxkeys AS k, stxdndistinct AS nd
  FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid)
  WHERE stxname = 'stts2';
-[ RECORD 1 ]------------------------------------------------------​--
k  | 1 2 5
nd | {"1, 2": 33178, "1, 5": 33178, "2, 5": 27435, "1, 2, 5": 33178}
(1 row)
```

這表示有三種欄位組合具有 33178 個相異值：郵遞區號與州；郵遞區號與城市；以及郵遞區號、城市與州（由於在這個資料表中郵遞區號本身就是唯一的，因此它們全都相等是預料中的事）。另一方面，城市與州的組合只有 27435 個相異值。

建議只在實際用於分組、而且群組數量的錯誤估計會導致不好計畫的欄位組合上，建立 `ndistinct` 統計資訊物件。否則，`ANALYZE` 的運算只是白白浪費。

<a id="PLANNER-STATS-EXTENDED-MCV-LISTS"></a>

#### 14.2.2.3. 多變量 MCV 清單 [#](#PLANNER-STATS-EXTENDED-MCV-LISTS)

為每個欄位儲存的另一種統計資訊是最常見值（most-common value）清單。這可以為個別欄位提供非常準確的估計，但對於在多個欄位上帶有條件的查詢，可能會造成顯著的錯誤估計。

為了改善這類估計，`ANALYZE` 可以收集欄位組合上的 MCV 清單。與函數相依性及相異值係數類似，對每一種可能的欄位分組都這麼做並不切實際。在這種情況下更是如此，因為 MCV 清單（不同於函數相依性與相異值係數）確實會儲存常見的欄位值。因此，只會為一起出現在以 `mcv` 選項定義之統計資訊物件中的欄位群組收集資料。

延續前面的範例，郵遞區號資料表的 MCV 清單可能如下所示（與較簡單的統計資訊類型不同，檢視 MCV 內容需要使用函式）：

```

CREATE STATISTICS stts3 (mcv) ON city, state FROM zipcodes;

ANALYZE zipcodes;

SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts3';

 index |         values         | nulls | frequency | base_frequency
-------+------------------------+-------+-----------+----------------
     0 | {Washington, DC}       | {f,f} |  0.003467 |        2.7e-05
     1 | {Apo, AE}              | {f,f} |  0.003067 |        1.9e-05
     2 | {Houston, TX}          | {f,f} |  0.002167 |       0.000133
     3 | {El Paso, TX}          | {f,f} |     0.002 |       0.000113
     4 | {New York, NY}         | {f,f} |  0.001967 |       0.000114
     5 | {Atlanta, GA}          | {f,f} |  0.001633 |        3.3e-05
     6 | {Sacramento, CA}       | {f,f} |  0.001433 |        7.8e-05
     7 | {Miami, FL}            | {f,f} |    0.0014 |          6e-05
     8 | {Dallas, TX}           | {f,f} |  0.001367 |        8.8e-05
     9 | {Chicago, IL}          | {f,f} |  0.001333 |        5.1e-05
   ...
(99 rows)
```

這表示最常見的城市與州組合是 DC 的 Washington，其實際頻率（在樣本中）大約是 0.35%。而該組合的基本頻率（由簡單的各欄位頻率計算而得）只有 0.0027%，導致低估了兩個數量級。

建議只在實際一起用於條件中、而且群組數量的錯誤估計會導致不好計畫的欄位組合上，建立 MCV 統計資訊物件。否則，`ANALYZE` 與規劃的運算只是白白浪費。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/planner-stats.html)（原文版本：18.6；核對日期：2026-09-11）
