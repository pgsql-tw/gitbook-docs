<a id="XOPER-OPTIMIZATION"></a>
## 36.15. 運算子最佳化資訊 [#](#XOPER-OPTIMIZATION)

[36.15.1. `COMMUTATOR`](xoper-optimization.md#XOPER-COMMUTATOR)

[36.15.2. `NEGATOR`](xoper-optimization.md#XOPER-NEGATOR)

[36.15.3. `RESTRICT`](xoper-optimization.md#XOPER-RESTRICT)

[36.15.4. `JOIN`](xoper-optimization.md#XOPER-JOIN)

[36.15.5. `HASHES`](xoper-optimization.md#XOPER-HASHES)

[36.15.6. `MERGES`](xoper-optimization.md#XOPER-MERGES)

<a id="id-1.8.3.18.2"></a>

PostgreSQL 的運算子定義可以包含
數個選用子句，用以告訴系統該運算子行為的實用資訊。只要適用，就應該
提供這些子句，因為它們可以大幅加快使用該運算子之查詢的執行速度。但若您提供了這些子句，
就必須確保其內容正確無誤！最佳化子句若使用不當，
可能導致查詢速度變慢、輸出結果出現細微錯誤，或其他不良後果。
若您不確定，隨時都可以省略某個最佳化子句；這麼做唯一的後果，
是查詢執行速度可能會比原本可以達到的還要慢。

未來版本的 PostgreSQL 中，可能會加入更多的最佳化子句。
此處所描述的，就是 18.6 版本所能理解的所有子句。

您也可以為運算子背後所依附的函式附加規劃器支援函式，
藉此提供另一種方式，讓系統得知該運算子的行為。
詳情請參閱[36.11 節](xfunc-optimization.md)。

<a id="XOPER-COMMUTATOR"></a>

### 36.15.1. `COMMUTATOR` [#](#XOPER-COMMUTATOR)

`COMMUTATOR` 子句（若有提供）會指出某個運算子，作為
目前所定義運算子的交換子（commutator）。我們稱運算子 A 是運算子 B 的
交換子，若對所有可能的輸入值 x、y，(x A y) 都等於 (y B x)。請注意，B
同時也是 A 的交換子。舉例來說，對於特定資料型別而言，運算子 `<` 與 `>` 通常互為
交換子，而運算子 `+` 通常與其自身互為交換。
但運算子 `-` 通常與任何運算子都不具交換性。

可交換運算子的左運算元型別，與其交換子的右運算元型別相同，
反之亦然。因此，PostgreSQL 只需要交換運算子的名稱，
即可查出交換子，而這也是 `COMMUTATOR` 子句中
唯一需要提供的內容。

為將用於索引與連接子句的運算子提供交換子資訊，是相當重要的，
因為這讓查詢最佳化器得以將這類子句「翻轉」為
不同計畫類型所需要的形式。舉例來說，考慮一個帶有
`tab1.x = tab2.y` 這類 WHERE 子句的查詢，其中 `tab1.x`
與 `tab2.y` 屬於使用者定義的型別，並假設
`tab2.y` 已建立索引。除非最佳化器能判斷如何將該子句翻轉為
`tab2.y = tab1.x`，否則便無法產生索引
掃描，因為索引掃描機制預期在其所收到的運算子左側看到已建立索引的欄位。
PostgreSQL *不會*單純
假設這是一項有效的轉換——`=` 運算子的建立者
必須透過為該運算子標記交換子資訊，明確指出這項轉換是有效的。

<a id="XOPER-NEGATOR"></a>

### 36.15.2. `NEGATOR` [#](#XOPER-NEGATOR)

`NEGATOR` 子句（若有提供）會指出某個運算子，作為
目前所定義運算子的否定子（negator）。我們稱運算子 A
是運算子 B 的否定子，若兩者都傳回布林值，且對所有可能的輸入 x、y，
(x A y) 都等於 NOT (x B y)。請注意，B 同時也是 A 的否定子。
舉例來說，對於大多數資料型別而言，`<` 與 `>=` 互為否定子配對。
運算子絕不可能有效地作為自身的否定子。

與交換子不同的是，一對一元運算子有可能有效地互相標記為
彼此的否定子；這意味著對所有 x 而言，(A x) 都等於 NOT (B x)。

某個運算子的否定子，其左運算元及／或右運算元型別，必須與
所定義的運算子相同，因此就如同 `COMMUTATOR` 一樣，`NEGATOR`
子句中只需要提供運算子名稱即可。

提供否定子對查詢最佳化器極有幫助，因為
這讓 `NOT (x = y)` 這樣的運算式，得以簡化為
`x <> y`。這種情況出現的頻率比您想像的還要高，因為
`NOT` 運算可能是其他重新排列動作所產生的結果。

<a id="XOPER-RESTRICT"></a>

### 36.15.3. `RESTRICT` [#](#XOPER-RESTRICT)

`RESTRICT` 子句（若有提供）會為該運算子指出一個限制選擇率
估算函式。（請注意，這裡指的是函式名稱，而非運算子名稱。）`RESTRICT`
子句只適用於傳回 `boolean` 的二元運算子。限制選擇率
估算器背後的概念，是猜測資料表中有多少比例的資料列，會滿足
以下形式的 `WHERE` 子句條件：

```

column OP constant
```

（針對目前的運算子及某個特定的常數值）。
這有助於最佳化器，讓它了解具有此形式的 `WHERE`
子句，大致會刪除多少資料列。（您或許會想，若常數在
左側會發生什麼事？嗯，這正是 `COMMUTATOR`
的用途之一……）

撰寫新的限制選擇率估算函式，遠超出本章的範疇，
但幸運的是，對於您自訂的許多運算子，通常都可以直接使用
系統標準估算器之一。以下是標準的限制估算器：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="function">eqsel</code>：用於 <code class="literal">=</code></td></tr><tr><td><code class="function">neqsel</code>：用於 <code class="literal">&lt;&gt;</code></td></tr><tr><td><code class="function">scalarltsel</code>：用於 <code class="literal">&lt;</code></td></tr><tr><td><code class="function">scalarlesel</code>：用於 <code class="literal">&lt;=</code></td></tr><tr><td><code class="function">scalargtsel</code>：用於 <code class="literal">&gt;</code></td></tr><tr><td><code class="function">scalargesel</code>：用於 <code class="literal">&gt;=</code></td></tr></table>

對於選擇率非常高或非常低的運算子，即使它們並非真正的等於或不等於，
您通常仍可以直接使用 `eqsel` 或 `neqsel`。舉例來說，
近似相等的幾何運算子便使用 `eqsel`，因為其假設
這類運算子通常只會比對出資料表中一小部分的項目。

對於那些擁有某種合理方式、可轉換為數值純量以進行範圍比較的
資料型別，您可以使用 `scalarltsel`、`scalarlesel`、
`scalargtsel` 與 `scalargesel` 進行比較。若有可能，請將
該資料型別加入 `src/backend/utils/adt/selfuncs.c` 中
`convert_to_scalar()` 函式所能理解的型別清單。
（最終，此函式應會由透過 `pg_type` 系統目錄某個欄位所識別的各資料型別專屬函式取代；
但目前尚未實現。）若您未這麼做，系統仍可正常運作，
只是最佳化器的估算結果不會如原本可以達到的那麼理想。

另一個實用的內建選擇率估算函式
是 `matchingsel`，只要有為輸入資料型別收集標準的 MCV 及／或
直方圖統計資訊，它幾乎可用於任何
二元運算子。其預設估算值，設為 `eqsel`
所用預設估算值的兩倍，因此最適合用於
嚴謹程度略低於相等的比較運算子。（或者，您也可以呼叫
底層的 `generic_restriction_selectivity`
函式，並提供不同的預設估算值。）

`src/backend/utils/adt/geo_selfuncs.c` 中還有專為幾何
運算子設計的額外選擇率估算函式：`areasel`、`positionsel`
以及 `contsel`。撰寫本文件當下，這些函式都只是空殼，但您或許仍會想
使用它們（或者更好的做法是加以改進）。

<a id="XOPER-JOIN"></a>

### 36.15.4. `JOIN` [#](#XOPER-JOIN)

`JOIN` 子句（若有提供）會為該運算子指出一個連接選擇率
估算函式。（請注意，這裡指的是函式名稱，而非運算子名稱。）`JOIN`
子句只適用於傳回 `boolean` 的二元運算子。連接
選擇率估算器背後的概念，是猜測一對資料表中，有多少比例的資料列，會滿足
以下形式的 `WHERE` 子句條件：

```

table1.column1 OP table2.column2
```

（針對目前的運算子）。與 `RESTRICT` 子句一樣，這對最佳化器
有非常大的幫助，讓它得以判斷在數種可能的連接順序中，
哪一種所需的工作量可能最少。

與先前一樣，本章不會嘗試說明如何撰寫
連接選擇率估算函式，而只會建議您在適用的情況下，
使用某個標準估算器：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="function">eqjoinsel</code>：用於 <code class="literal">=</code></td></tr><tr><td><code class="function">neqjoinsel</code>：用於 <code class="literal">&lt;&gt;</code></td></tr><tr><td><code class="function">scalarltjoinsel</code>：用於 <code class="literal">&lt;</code></td></tr><tr><td><code class="function">scalarlejoinsel</code>：用於 <code class="literal">&lt;=</code></td></tr><tr><td><code class="function">scalargtjoinsel</code>：用於 <code class="literal">&gt;</code></td></tr><tr><td><code class="function">scalargejoinsel</code>：用於 <code class="literal">&gt;=</code></td></tr><tr><td><code class="function">matchingjoinsel</code>：用於一般比對運算子</td></tr><tr><td><code class="function">areajoinsel</code>：用於二維面積比較</td></tr><tr><td><code class="function">positionjoinsel</code>：用於二維位置比較</td></tr><tr><td><code class="function">contjoinsel</code>：用於二維包含關係比較</td></tr></table>

<a id="XOPER-HASHES"></a>

### 36.15.5. `HASHES` [#](#XOPER-HASHES)

`HASHES` 子句（若有出現）會告訴系統，
可以針對以此運算子為基礎的連接，使用雜湊連接方法。`HASHES`
只適用於傳回 `boolean` 的二元運算子，而實務上，該運算子
必須代表某個資料型別或某對資料型別之間的相等關係。

雜湊連接背後所依據的假設，是連接運算子只有在左、右值
雜湊至相同雜湊碼時，才可能傳回 true。若兩個值被放入不同的
雜湊桶（bucket），連接運算就完全不會對它們進行比較，並隱含假設
該連接運算子的結果必為 false。因此，對於並不代表
某種相等關係的運算子而言，指定 `HASHES` 永遠是沒有意義的。
在大多數情況下，只有當運算子兩側採用相同資料型別時，支援雜湊才具實用性。
不過，有時仍可能為兩種或多種資料型別設計相容的雜湊
函式；也就是說，即使值的表示法不同，這些函式仍能為「相等」的值產生
相同的雜湊碼。舉例來說，在對不同寬度的整數進行雜湊時，要達成這項特性相當簡單。

若要標記為 `HASHES`，該連接運算子必須出現
於某個雜湊索引運算子家族中。建立該運算子時，系統並不會強制檢查這一點，
因為會參照這個運算子的，正是那個運算子家族，而它在建立當下當然還不存在。但若不存在這樣的運算子家族，
嘗試在雜湊連接中使用該運算子，將會在執行期失敗。系統需要
該運算子家族，才能找到該運算子輸入資料型別所專屬的雜湊函式。當然，
您也必須先建立適當的雜湊函式，才能建立該運算子家族。

準備雜湊函式時應格外謹慎，因為存在一些
與機器相關的方式，可能導致它無法正確運作。舉例來說，若您的資料型別是
一個結構，其中可能包含無意義的填補位元，您就不能單純將整個結構傳給
`hash_any`。（除非您撰寫其他運算子與
函式時，確保未使用的位元永遠為零，這正是建議採用的策略。）
另一個例子是，在符合 IEEE
浮點數標準的機器上，負零與正零是不同的
值（不同的位元樣式），但依定義應被視為相等。
若某個浮點值可能含有負零，就需要額外的步驟，
確保它產生的雜湊值與正零相同。

一個可用於雜湊連接的運算子，必須具有一個交換子
（若兩個運算元資料型別相同，則為其自身；若不同，則為相關的相等運算子），
且該交換子必須出現在同一個運算子家族中。
若非如此，在使用該運算子時，可能會發生規劃器錯誤。此外，
對於支援多種資料型別的雜湊運算子家族而言，為每一種資料型別組合提供
相等運算子也是一個好主意（但並非嚴格要求）；這可帶來更好的最佳化效果。

### 注意

可用於雜湊連接之運算子背後所依附的函式，必須標記為
immutable 或 stable。若標記為 volatile，系統將永遠不會
嘗試將該運算子用於雜湊連接。

### 注意

若某個可用於雜湊連接的運算子，其背後依附的函式標記為
strict，則該函式也必須是完整的：也就是說，對於任何兩個
非 null 的輸入，它都應傳回 true 或 false，絕不傳回 null。若未遵循此規則，
`IN` 運算的雜湊最佳化，可能會產生錯誤的結果。（具體來說，
根據標準，正確答案應為 null 的情況下，`IN` 可能會傳回
false；或者可能會產生一個抱怨它未準備好處理
null 結果的錯誤。）

<a id="XOPER-MERGES"></a>

### 36.15.6. `MERGES` [#](#XOPER-MERGES)

`MERGES` 子句（若有出現）會告訴系統，
可以針對以此運算子為基礎的連接，使用合併連接方法。`MERGES`
只適用於傳回 `boolean` 的二元運算子，而實務上，該運算子
必須代表某個資料型別或某對資料型別之間的相等關係。

合併連接是以將左、右資料表排序後，
再平行掃描這兩份已排序的資料表為基礎的概念。因此，兩種資料型別都必須
能夠完全排序，且連接運算子必須是一種只有在
一對值落在排序順序中「相同位置」時，才能成功的運算子。
實務上，這代表連接運算子的行為必須如同相等運算一般。但只要邏輯上相容，
仍可以對兩種不同的資料型別進行合併連接。舉例來說，
`smallint` 與 `integer` 之間的
相等運算子即可進行合併連接。
我們只需要能將兩種資料型別，帶入一個邏輯上相容之順序的排序運算子即可。

若要標記為 `MERGES`，該連接運算子必須以相等成員的身分，
出現於某個 `btree` 索引運算子家族中。
建立該運算子時，系統並不會強制檢查這一點，
因為會參照這個運算子的，正是那個運算子家族，而它在建立當下當然還不存在。但除非能找到相符的運算子家族，
否則該運算子實際上並不會被用於合併連接。因此，
`MERGES` 旗標的作用，就是向規劃器提示
值得去尋找一個相符的運算子家族。

一個可用於合併連接的運算子，必須具有一個交換子
（若兩個運算元資料型別相同，則為其自身；若不同，則為相關的相等運算子），
且該交換子必須出現在同一個運算子家族中。
若非如此，在使用該運算子時，可能會發生規劃器錯誤。此外，
對於支援多種資料型別的 `btree` 運算子家族而言，為每一種資料型別組合提供
相等運算子也是一個好主意（但並非嚴格要求）；這可帶來更好的最佳化效果。

### 注意

可用於合併連接之運算子背後所依附的函式，必須標記為
immutable 或 stable。若標記為 volatile，系統將永遠不會
嘗試將該運算子用於合併連接。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xoper-optimization.html)（原文版本：18.6；核對日期：2026-09-24）
