<a id="XINDEX"></a>
## 36.16. 將擴充功能與索引介接 [#](#XINDEX)

[36.16.1. 索引方法與運算子類別](xindex.md#XINDEX-OPCLASS)

[36.16.2. 索引方法策略](xindex.md#XINDEX-STRATEGIES)

[36.16.3. 索引方法支援常式](xindex.md#XINDEX-SUPPORT)

[36.16.4. 一個範例](xindex.md#XINDEX-EXAMPLE)

[36.16.5. 運算子類別與運算子家族](xindex.md#XINDEX-OPFAMILY)

[36.16.6. 系統對運算子類別的相依性](xindex.md#XINDEX-OPCLASS-DEPENDENCIES)

[36.16.7. 排序運算子](xindex.md#XINDEX-ORDERING-OPS)

[36.16.8. 運算子類別的特殊功能](xindex.md#XINDEX-OPCLASS-FEATURES)

<a id="id-1.8.3.19.2"></a>

到目前為止所描述的做法，讓你可以定義新的型別、新的
函式，以及新的運算子。然而，我們還無法在新資料型別的欄位上
定義索引。要做到這一點，我們必須為這個新資料型別定義一個
*運算子類別*（operator class）。在本節稍後，我們會以一個範例來說明這個概念：
為 B-tree 索引方法定義一個新的運算子類別，用來以絕對值遞增的順序
儲存並排序複數。

運算子類別可以群組成*運算子家族*（operator family），
用來表示語意相容的類別之間的關係。
當只涉及單一資料型別時，一個運算子類別就已足夠，
因此我們會先專注於這種情況，之後再回頭討論運算子家族。

<a id="XINDEX-OPCLASS"></a>

### 36.16.1. 索引方法與運算子類別 [#](#XINDEX-OPCLASS)

運算子類別與索引存取方法相關聯，例如
[B-Tree](../../internals/indextypes/btree.md)
或 [GIN](../../internals/indextypes/gin.md)。自訂的索引存取方法可以
使用 [CREATE ACCESS METHOD](../../reference/sql-commands/sql-create-access-method.md) 來定義。詳情請參閱
[第 63 章](../../internals/indexam/README.md)。

索引方法的常式並不直接知道任何
關於索引方法所要操作之資料型別的資訊。
相反地，*運算子
類別*<a id="id-1.8.3.19.5.3.2"></a>
會識別出索引方法要處理特定資料型別時所需使用的操作集合。
運算子類別之所以如此命名，是因為它們所指定的其中一項內容，
就是可以搭配索引使用的 `WHERE` 子句運算子集合
（也就是可以轉換為索引掃描限定條件的運算子）。一個
運算子類別也可以指定索引方法內部操作所需要的某些*支援
函式*（support function），這些函式並不直接對應到任何可以搭配索引使用的
`WHERE` 子句運算子。

同一個資料型別與索引方法可以定義多個運算子類別。
藉此，可以為單一資料型別定義
多組索引語意。
舉例來說，B-tree 索引要求為其所處理的每種資料型別
定義一種排序順序。
對於複數資料型別來說，擁有一個依複數
絕對值排序的 B-tree 運算子類別、另一個依實部排序的類別等等，
可能會很有用。
通常其中一個運算子類別會被認為最普遍
實用，並會被標記為該資料型別與索引方法的預設運算子類別。

同一個運算子類別名稱
可以用於多個不同的索引方法（舉例來說，B-tree
與雜湊索引方法都各自有一個名為
`int4_ops` 的運算子類別），但每個這樣的類別都是獨立的
實體，必須分別定義。

<a id="XINDEX-STRATEGIES"></a>

### 36.16.2. 索引方法策略 [#](#XINDEX-STRATEGIES)

與運算子類別相關聯的運算子，是以「策略編號」（strategy number）
來識別的，這些編號用來在其運算子類別的情境中識別
每個運算子的語意。
舉例來說，B-tree 對鍵值強制施加嚴格的排序，由小到大，
因此諸如「小於」與「大於等於」
這類的運算子，對 B-tree 而言相當重要。
由於
PostgreSQL 允許使用者自行定義運算子，
PostgreSQL 無法單憑運算子的名稱
（例如 `<` 或 `>=`）來判斷它是哪一種
比較方式。因此，索引方法定義了一組
「策略」，可以將其視為廣義化的運算子。
每個運算子類別會針對特定的資料型別與索引語意的解讀方式，
指定哪一個實際的運算子對應到哪一種策略。

B-tree 索引方法定義了五種策略，如[表 36.3](xindex.md#XINDEX-BTREE-STRAT-TABLE)所示。

<a id="XINDEX-BTREE-STRAT-TABLE"></a>

**表 36.3. B-Tree 策略**

<table border="1" class="table" summary="B-Tree Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>小於</td><td>1</td></tr><tr><td>小於等於</td><td>2</td></tr><tr><td>等於</td><td>3</td></tr><tr><td>大於等於</td><td>4</td></tr><tr><td>大於</td><td>5</td></tr></tbody></table>

<br>

雜湊索引只支援相等比較，因此它們只使用一種
策略，如[表 36.4](xindex.md#XINDEX-HASH-STRAT-TABLE)所示。

<a id="XINDEX-HASH-STRAT-TABLE"></a>

**表 36.4. 雜湊策略**

<table border="1" class="table" summary="Hash Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>等於</td><td>1</td></tr></tbody></table>

<br>

GiST 索引更具彈性：它們根本沒有固定的一組
策略。取而代之，每個特定 GiST 運算子類別的「一致性」（consistency）支援常式，
會以自己的方式解讀策略編號。舉例來說，內建 GiST 索引
運算子類別中有幾個是用來對二維幾何物件建立索引，提供了
[表 36.5](xindex.md#XINDEX-RTREE-STRAT-TABLE)所示的「R-tree」策略。其中四種是真正的
二維測試（重疊、相同、包含、被包含）；
另外四種只考慮 X 方向；其餘四種
則是在 Y 方向提供相同的測試。

<a id="XINDEX-RTREE-STRAT-TABLE"></a>

**表 36.5. GiST 二維「R-tree」策略**

<table border="1" class="table" summary="GiST Two-Dimensional R-tree Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>嚴格在左側</td><td>1</td></tr><tr><td>不延伸至右側</td><td>2</td></tr><tr><td>重疊</td><td>3</td></tr><tr><td>不延伸至左側</td><td>4</td></tr><tr><td>嚴格在右側</td><td>5</td></tr><tr><td>相同</td><td>6</td></tr><tr><td>包含</td><td>7</td></tr><tr><td>被包含</td><td>8</td></tr><tr><td>不延伸至上方</td><td>9</td></tr><tr><td>嚴格在下方</td><td>10</td></tr><tr><td>嚴格在上方</td><td>11</td></tr><tr><td>不延伸至下方</td><td>12</td></tr></tbody></table>

<br>

SP-GiST 索引在彈性方面與 GiST 索引類似：它們同樣沒有
固定的一組策略。取而代之，每個運算子
類別的支援常式會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建點（point）運算子類別所使用的策略編號如
[表 36.6](xindex.md#XINDEX-SPGIST-POINT-STRAT-TABLE)所示。

<a id="XINDEX-SPGIST-POINT-STRAT-TABLE"></a>

**表 36.6. SP-GiST 點策略**

<table border="1" class="table" summary="SP-GiST Point Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>嚴格在左側</td><td>1</td></tr><tr><td>嚴格在右側</td><td>5</td></tr><tr><td>相同</td><td>6</td></tr><tr><td>被包含</td><td>8</td></tr><tr><td>嚴格在下方</td><td>10</td></tr><tr><td>嚴格在上方</td><td>11</td></tr></tbody></table>

<br>

GIN 索引與 GiST、SP-GiST 索引類似，同樣沒有
固定的一組策略。取而代之，每個運算子類別的支援常式
會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建陣列運算子類別所使用的策略編號如
[表 36.7](xindex.md#XINDEX-GIN-ARRAY-STRAT-TABLE)所示。

<a id="XINDEX-GIN-ARRAY-STRAT-TABLE"></a>

**表 36.7. GIN 陣列策略**

<table border="1" class="table" summary="GIN Array Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>重疊</td><td>1</td></tr><tr><td>包含</td><td>2</td></tr><tr><td>被包含</td><td>3</td></tr><tr><td>等於</td><td>4</td></tr></tbody></table>

<br>

BRIN 索引與 GiST、SP-GiST 及 GIN 索引類似，同樣沒有
固定的一組策略。取而代之，每個運算子類別的支援常式
會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建 `Minmax` 運算子類別所使用的策略編號如
[表 36.8](xindex.md#XINDEX-BRIN-MINMAX-STRAT-TABLE)所示。

<a id="XINDEX-BRIN-MINMAX-STRAT-TABLE"></a>

**表 36.8. BRIN Minmax 策略**

<table border="1" class="table" summary="BRIN Minmax Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>小於</td><td>1</td></tr><tr><td>小於等於</td><td>2</td></tr><tr><td>等於</td><td>3</td></tr><tr><td>大於等於</td><td>4</td></tr><tr><td>大於</td><td>5</td></tr></tbody></table>

<br>

請注意，以上所列出的所有運算子都會傳回布林值。實際上，
所有被定義為索引方法搜尋運算子的運算子都必須
傳回 `boolean` 型別，因為它們必須出現在
`WHERE` 子句的最上層，才能搭配索引使用。
（有些索引存取方法也支援*排序運算子*，
這類運算子通常不會傳回布林值；此功能會在
[第 36.16.7 節](xindex.md#XINDEX-ORDERING-OPS)討論。）

<a id="XINDEX-SUPPORT"></a>

### 36.16.3. 索引方法支援常式 [#](#XINDEX-SUPPORT)

光有策略通常還不足以讓系統知道如何
使用索引。實務上，索引方法還需要
額外的支援常式才能運作。舉例來說，B-tree
索引方法必須能夠比較兩個鍵值，並判斷其中一個
是大於、等於還是小於另一個。同樣地，
雜湊索引方法必須能夠為鍵值計算雜湊碼。
這些操作並不對應到 SQL 命令中
用於限定條件的運算子；它們是索引方法內部
使用的管理性常式。

如同策略一樣，運算子類別會識別出對於給定的資料型別
與語意解讀方式，應由哪個特定函式來扮演這些角色。索引方法會定義
它所需要的函式集合，而運算子類別則透過將函式指派給索引方法所指定的
「支援函式編號」，來識別要使用的正確函式。

此外，有些運算子類別（opclass）允許使用者指定
控制其行為的參數。每個內建的索引存取方法都有一個可選的
`options` 支援函式，用來定義一組
運算子類別專屬的參數。

B-tree 需要一個比較支援函式，
並允許運算子類別的作者依需要另外提供四個
支援函式，如[表 36.9](xindex.md#XINDEX-BTREE-SUPPORT-TABLE)所示（原文此處寫作「四個」，但表 36.9 實際列出編號 2～6 共五個可選的支援函式）。
這些支援函式的要求進一步說明於
[第 65.1.3 節](../../internals/indextypes/btree.md#BTREE-SUPPORT-FUNCS)。

<a id="XINDEX-BTREE-SUPPORT-TABLE"></a>

**表 36.9. B-Tree 支援函式**

<table border="1" class="table" summary="B-Tree Support Functions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>函式</th><th>支援編號</th></tr></thead><tbody><tr><td>
        比較兩個鍵值，並傳回小於零、等於零或
        大於零的整數，表示第一個鍵值是小於、
        等於還是大於第二個
       </td><td>1</td></tr><tr><td>
        傳回可由 C 呼叫的排序支援函式的位址（可選）
       </td><td>2</td></tr><tr><td>
        將測試值與某個基準值加減某個偏移量進行比較，並依比較
        結果傳回 true 或 false（可選）
       </td><td>3</td></tr><tr><td>
        判斷使用此運算子類別的索引，套用 B-tree 去重複（deduplication）最佳化
        是否安全（可選）
       </td><td>4</td></tr><tr><td>
        定義此運算子類別專屬的選項
        （可選）
       </td><td>5</td></tr><tr><td>
        傳回可由 C 呼叫的跳躍支援（skip support）函式的位址（可選）
       </td><td>6</td></tr></tbody></table>

<br>

雜湊索引需要一個支援函式，並允許依運算子類別作者的需要
另外提供兩個，如[表 36.10](xindex.md#XINDEX-HASH-SUPPORT-TABLE)所示。

<a id="XINDEX-HASH-SUPPORT-TABLE"></a>

**表 36.10. 雜湊支援函式**

<table border="1" class="table" summary="Hash Support Functions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>函式</th><th>支援編號</th></tr></thead><tbody><tr><td>計算鍵值的 32 位元雜湊值</td><td>1</td></tr><tr><td>
         在給定 64 位元鹽值（salt）的情況下計算鍵值的 64 位元雜湊值；若
         鹽值為 0，結果的低 32 位元必須與函式 1
         所計算出的值相符
         （可選）
       </td><td>2</td></tr><tr><td>
        定義此運算子類別專屬的選項
        （可選）
       </td><td>3</td></tr></tbody></table>

<br>

GiST 索引有十二個支援函式，其中七個是可選的，
如[表 36.11](xindex.md#XINDEX-GIST-SUPPORT-TABLE)所示。
（更多資訊請參閱[第 65.2 節](../../internals/indextypes/gist.md)。）

<a id="XINDEX-GIST-SUPPORT-TABLE"></a>

**表 36.11. GiST 支援函式**

<table border="1" class="table" summary="GiST Support Functions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>函式</th><th>說明</th><th>支援編號</th></tr></thead><tbody><tr><td><code class="function">consistent</code></td><td>判斷鍵值是否滿足
        查詢限定條件</td><td>1</td></tr><tr><td><code class="function">union</code></td><td>計算一組鍵值的聯集</td><td>2</td></tr><tr><td><code class="function">compress</code></td><td>計算欲索引的鍵值或值的壓縮表示形式
        （可選）</td><td>3</td></tr><tr><td><code class="function">decompress</code></td><td>計算
        壓縮鍵值的解壓縮表示形式（可選）</td><td>4</td></tr><tr><td><code class="function">penalty</code></td><td>計算將新鍵值插入子樹時，相對於
       給定子樹鍵值的懲罰值</td><td>5</td></tr><tr><td><code class="function">picksplit</code></td><td>判斷某頁的哪些項目要
       移到新頁，並計算結果頁的聯集鍵值</td><td>6</td></tr><tr><td><code class="function">same</code></td><td>比較兩個鍵值，若相等則傳回 true</td><td>7</td></tr><tr><td><code class="function">distance</code></td><td>判斷鍵值到查詢值的距離（可選）</td><td>8</td></tr><tr><td><code class="function">fetch</code></td><td>為索引專用掃描計算壓縮鍵值的原始
       表示形式（可選）</td><td>9</td></tr><tr><td><code class="function">options</code></td><td>定義此運算子類別專屬的選項
        （可選）</td><td>10</td></tr><tr><td><code class="function">sortsupport</code></td><td>提供用於快速索引建置的排序比較器
        （可選）</td><td>11</td></tr><tr><td><code class="function">translate_cmptype</code></td><td>將比較型別轉換為此運算子類別
        所使用的策略編號（可選）</td><td>12</td></tr></tbody></table>

<br>

SP-GiST 索引有六個支援函式，其中一個是可選的，如
[表 36.12](xindex.md#XINDEX-SPGIST-SUPPORT-TABLE)所示。
（更多資訊請參閱[第 65.3 節](../../internals/indextypes/spgist.md)。）

<a id="XINDEX-SPGIST-SUPPORT-TABLE"></a>

**表 36.12. SP-GiST 支援函式**

<table border="1" class="table" summary="SP-GiST Support Functions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>函式</th><th>說明</th><th>支援編號</th></tr></thead><tbody><tr><td><code class="function">config</code></td><td>提供運算子類別的基本資訊</td><td>1</td></tr><tr><td><code class="function">choose</code></td><td>判斷如何將新值插入內部元組（inner tuple）</td><td>2</td></tr><tr><td><code class="function">picksplit</code></td><td>判斷如何分割一組值</td><td>3</td></tr><tr><td><code class="function">inner_consistent</code></td><td>判斷查詢需要搜尋哪些
        子分區</td><td>4</td></tr><tr><td><code class="function">leaf_consistent</code></td><td>判斷鍵值是否滿足
        查詢限定條件</td><td>5</td></tr><tr><td><code class="function">options</code></td><td>定義此運算子類別專屬的選項
        （可選）</td><td>6</td></tr></tbody></table>

<br>

GIN 索引有七個支援函式，其中四個是可選的，
如[表 36.13](xindex.md#XINDEX-GIN-SUPPORT-TABLE)所示。
（更多資訊請參閱[第 65.4 節](../../internals/indextypes/gin.md)。）

<a id="XINDEX-GIN-SUPPORT-TABLE"></a>

**表 36.13. GIN 支援函式**

<table border="1" class="table" summary="GIN Support Functions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>函式</th><th>說明</th><th>支援編號</th></tr></thead><tbody><tr><td><code class="function">compare</code></td><td>
        比較兩個鍵值，並傳回小於零、等於零，
        或大於零的整數，表示第一個鍵值是小於、
        等於還是大於第二個
       </td><td>1</td></tr><tr><td><code class="function">extractValue</code></td><td>從欲索引的值中擷取鍵值</td><td>2</td></tr><tr><td><code class="function">extractQuery</code></td><td>從查詢條件中擷取鍵值</td><td>3</td></tr><tr><td><code class="function">consistent</code></td><td>
        判斷值是否符合查詢條件（布林變體）
        （若存在支援函式 6 則為可選）
       </td><td>4</td></tr><tr><td><code class="function">comparePartial</code></td><td>
        比較查詢中的部分鍵值與索引中的鍵值，並傳回小於零、等於零，
        或大於零的整數，表示 GIN 應忽略此索引
        項目、將此項目視為相符，還是停止索引掃描（可選）
       </td><td>5</td></tr><tr><td><code class="function">triConsistent</code></td><td>
        判斷值是否符合查詢條件（三態變體）
        （若存在支援函式 4 則為可選）
       </td><td>6</td></tr><tr><td><code class="function">options</code></td><td>
        定義此運算子類別專屬的選項
        （可選）
       </td><td>7</td></tr></tbody></table>

<br>

BRIN 索引有五個基本支援函式，其中一個是可選的，
如[表 36.14](xindex.md#XINDEX-BRIN-SUPPORT-TABLE)所示。某些基本函式變體
需要提供額外的支援函式。
（更多資訊請參閱[第 65.5.3 節](../../internals/indextypes/brin.md#BRIN-EXTENSIBILITY)。）

<a id="XINDEX-BRIN-SUPPORT-TABLE"></a>

**表 36.14. BRIN 支援函式**

<table border="1" class="table" summary="BRIN Support Functions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>函式</th><th>說明</th><th>支援編號</th></tr></thead><tbody><tr><td><code class="function">opcInfo</code></td><td>
        傳回描述已索引欄位摘要資料的內部
        資訊
       </td><td>1</td></tr><tr><td><code class="function">add_value</code></td><td>將新值加入現有的摘要索引元組</td><td>2</td></tr><tr><td><code class="function">consistent</code></td><td>判斷值是否符合查詢條件</td><td>3</td></tr><tr><td><code class="function">union</code></td><td>
        計算兩個摘要元組的聯集
       </td><td>4</td></tr><tr><td><code class="function">options</code></td><td>
        定義此運算子類別專屬的選項
        （可選）
       </td><td>5</td></tr></tbody></table>

<br>

與搜尋運算子不同，支援函式會傳回該特定索引方法所預期的
資料型別；舉例來說，就 B-tree 的比較函式而言，
傳回的是帶正負號的整數。每個支援函式的引數數量與型別，
同樣取決於索引方法。就 B-tree 與雜湊而言，比較函式與
雜湊函式所接受的輸入資料型別，與運算子類別中所含運算子相同，
但大多數 GiST、SP-GiST、GIN 與 BRIN 的支援函式則並非如此。

<a id="XINDEX-EXAMPLE"></a>

### 36.16.4. 一個範例 [#](#XINDEX-EXAMPLE)

現在我們已經了解了這些概念，以下是先前所承諾的
建立新運算子類別的範例。
（你可以在原始碼發行套件的
`src/tutorial/complex.c` 與
`src/tutorial/complex.sql`
中找到此範例的可運作副本。）
此運算子類別封裝了依絕對值順序排序複數的
運算子，因此我們選擇 `complex_abs_ops` 這個
名稱。首先，我們需要一組運算子。定義運算子的方法
已在[第 36.14 節](xoper.md)中討論過。對於 B-tree 運算子類別，
我們所需要的運算子為：

* 絕對值小於（策略 1）
* 絕對值小於等於（策略 2）
* 絕對值等於（策略 3）
* 絕對值大於等於（策略 4）
* 絕對值大於（策略 5）

定義一組相關比較運算子時，最不容易出錯的方式，
是先撰寫 B-tree 比較支援函式，再將其他函式寫成
圍繞該支援函式的單行包裝函式。這樣可以
降低邊界情況產生不一致結果的機率。
依照這個做法，我們先撰寫：

```

#define Mag(c)  ((c)->x*(c)->x + (c)->y*(c)->y)

static int
complex_abs_cmp_internal(Complex *a, Complex *b)
{
    double      amag = Mag(a),
                bmag = Mag(b);

    if (amag < bmag)
        return -1;
    if (amag > bmag)
        return 1;
    return 0;
}
```

現在小於函式看起來像這樣：

```

PG_FUNCTION_INFO_V1(complex_abs_lt);

Datum
complex_abs_lt(PG_FUNCTION_ARGS)
{
    Complex    *a = (Complex *) PG_GETARG_POINTER(0);
    Complex    *b = (Complex *) PG_GETARG_POINTER(1);

    PG_RETURN_BOOL(complex_abs_cmp_internal(a, b) < 0);
}
```

其餘四個函式的差異只在於如何將內部
函式的結果與零做比較。

接下來，我們要向 SQL 宣告這些函式，以及
以這些函式為基礎的運算子：

```

CREATE FUNCTION complex_abs_lt(complex, complex) RETURNS bool
    AS 'filename', 'complex_abs_lt'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR < (
   leftarg = complex, rightarg = complex, procedure = complex_abs_lt,
   commutator = > , negator = >= ,
   restrict = scalarltsel, join = scalarltjoinsel
);
```

指定正確的交換子（commutator）與否定子（negator）運算子，
以及合適的限制與連接選擇性函式相當重要，
否則最佳化器將無法有效地
利用索引。

這裡還發生了一些值得注意的事：

* 名稱為（比如說）`=`、且兩個運算元都接受
  `complex` 型別的運算子只能有一個。在
  這個例子中，我們並沒有為
  `complex` 定義其他的 `=` 運算子，但如果我們是在
  建立一個實用的資料型別，我們可能會希望
  `=` 是複數的一般相等運算
  （而不是絕對值的相等）。在那種情況下，我們就需要為
  `complex_abs_eq` 使用其他的運算子名稱。
* 雖然 PostgreSQL 可以處理
  SQL 名稱相同、但引數資料型別不同的函式，但 C
  語言只能處理一個具有特定名稱的全域函式。因此我們不應該將 C 函式命名為
  類似 `abs_eq` 這種簡單的名稱。通常
  比較好的做法是在 C 函式名稱中
  加入資料型別名稱，以免與其他資料型別的函式
  衝突。
* 我們原本可以將函式的 SQL 名稱
  取為 `abs_eq`，依賴
  PostgreSQL 依引數資料型別
  來與其他同名的 SQL 函式做區分。
  為了讓範例保持簡單，我們讓此函式在
  C 語言層級與 SQL 層級使用相同的名稱。

下一步是註冊 B-tree 所需要的
支援常式。實作此功能的 C 範例程式碼位於
包含運算子函式的同一個檔案中。我們如下宣告
這個函式：

```

CREATE FUNCTION complex_abs_cmp(complex, complex)
    RETURNS integer
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;
```

既然我們已經有了所需要的運算子與支援常式，
我們終於可以建立此運算子類別了：

```

CREATE OPERATOR CLASS complex_abs_ops
    DEFAULT FOR TYPE complex USING btree AS
        OPERATOR        1       < ,
        OPERATOR        2       <= ,
        OPERATOR        3       = ,
        OPERATOR        4       >= ,
        OPERATOR        5       > ,
        FUNCTION        1       complex_abs_cmp(complex, complex);
```

大功告成！現在應該可以在
`complex` 欄位上建立並使用 B-tree 索引了。

我們原本也可以將運算子項目寫得更詳細一些，例如：

```

        OPERATOR        1       < (complex, complex) ,
```

但由於運算子所接受的資料型別與我們正在定義運算子類別的
資料型別相同，因此不需要這麼做。

上述範例假設你想要將這個新運算子類別
設為 `complex` 資料型別的預設 B-tree 運算子類別。
若不是這樣，只要省略 `DEFAULT` 這個字即可。

<a id="XINDEX-OPFAMILY"></a>

### 36.16.5. 運算子類別與運算子家族 [#](#XINDEX-OPFAMILY)

到目前為止，我們一直隱含地假設一個運算子類別只處理
單一資料型別。雖然在特定的索引欄位中確實只能有一種資料型別，
但為索引欄位與不同資料型別的值之間的比較操作建立索引，
通常也相當有用。此外，若某個運算子類別會用到
跨資料型別的運算子，通常另一種資料型別
也會有自己相關的運算子類別。將相關類別之間的關聯
明確表示出來會很有幫助，因為這有助於規劃器
最佳化 SQL 查詢（尤其是對 B-tree 運算子類別而言，因為
規劃器擁有大量關於如何處理它們的知識）。

為了處理這些需求，PostgreSQL
採用了*運算子
家族*<a id="id-1.8.3.19.9.3.3"></a>的概念。
一個運算子家族包含一個或多個運算子類別，也可以
包含屬於整個家族、但不屬於家族中任何單一類別的
可索引運算子與對應支援函式。我們稱這類運算子與函式在家族中是
「鬆散的」（loose），與被綁定在特定類別中相對。
通常每個運算子類別會包含單一資料型別的運算子，
而跨資料型別的運算子則鬆散地存在於家族中。

一個運算子家族中的所有運算子與函式，語意上都必須
相容，相容性的要求則由索引方法所決定。因此你可能會想，
為什麼還要特別把家族中的某些子集合獨立成運算子類別；
事實上，對許多用途而言，
類別的劃分並不重要，家族才是唯一有意義的分組方式。之所以要定義運算子類別，
是因為它們指定了要支援某個特定索引，需要家族中的
多少內容。
如果有索引使用了某個運算子類別，那麼該運算子類別
就無法在不刪除該索引的情況下被移除——但運算子家族中的
其他部分，也就是其他運算子類別與鬆散的運算子，
則可以被移除。因此，運算子類別應該只包含
在特定資料型別的索引上運作所合理需要的最少
一組運算子與函式，而相關但非必要的運算子
則可以另外加入，作為運算子家族中鬆散的成員。

舉例來說，PostgreSQL 內建了一個
B-tree 運算子家族 `integer_ops`，其中包含運算子
類別 `int8_ops`、`int4_ops` 與
`int2_ops`，分別用於 `bigint`（`int8`）、
`integer`（`int4`）與 `smallint`（`int2`）
欄位的索引。此家族還包含跨資料型別的比較
運算子，讓這些型別中任兩者可以互相比較，因此
其中一種型別的索引，也可以用另一種型別的比較值來
搜尋。這個家族可以用以下的定義重現：

```

CREATE OPERATOR FAMILY integer_ops USING btree;

CREATE OPERATOR CLASS int8_ops
DEFAULT FOR TYPE int8 USING btree FAMILY integer_ops AS
  -- standard int8 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint8cmp(int8, int8) ,
  FUNCTION 2 btint8sortsupport(internal) ,
  FUNCTION 3 in_range(int8, int8, int8, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint8skipsupport(internal) ;

CREATE OPERATOR CLASS int4_ops
DEFAULT FOR TYPE int4 USING btree FAMILY integer_ops AS
  -- standard int4 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint4cmp(int4, int4) ,
  FUNCTION 2 btint4sortsupport(internal) ,
  FUNCTION 3 in_range(int4, int4, int4, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint4skipsupport(internal) ;

CREATE OPERATOR CLASS int2_ops
DEFAULT FOR TYPE int2 USING btree FAMILY integer_ops AS
  -- standard int2 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint2cmp(int2, int2) ,
  FUNCTION 2 btint2sortsupport(internal) ,
  FUNCTION 3 in_range(int2, int2, int2, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint2skipsupport(internal) ;

ALTER OPERATOR FAMILY integer_ops USING btree ADD
  -- cross-type comparisons int8 vs int2
  OPERATOR 1 < (int8, int2) ,
  OPERATOR 2 <= (int8, int2) ,
  OPERATOR 3 = (int8, int2) ,
  OPERATOR 4 >= (int8, int2) ,
  OPERATOR 5 > (int8, int2) ,
  FUNCTION 1 btint82cmp(int8, int2) ,

  -- cross-type comparisons int8 vs int4
  OPERATOR 1 < (int8, int4) ,
  OPERATOR 2 <= (int8, int4) ,
  OPERATOR 3 = (int8, int4) ,
  OPERATOR 4 >= (int8, int4) ,
  OPERATOR 5 > (int8, int4) ,
  FUNCTION 1 btint84cmp(int8, int4) ,

  -- cross-type comparisons int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- cross-type comparisons int4 vs int8
  OPERATOR 1 < (int4, int8) ,
  OPERATOR 2 <= (int4, int8) ,
  OPERATOR 3 = (int4, int8) ,
  OPERATOR 4 >= (int4, int8) ,
  OPERATOR 5 > (int4, int8) ,
  FUNCTION 1 btint48cmp(int4, int8) ,

  -- cross-type comparisons int2 vs int8
  OPERATOR 1 < (int2, int8) ,
  OPERATOR 2 <= (int2, int8) ,
  OPERATOR 3 = (int2, int8) ,
  OPERATOR 4 >= (int2, int8) ,
  OPERATOR 5 > (int2, int8) ,
  FUNCTION 1 btint28cmp(int2, int8) ,

  -- cross-type comparisons int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ,

  -- cross-type in_range functions
  FUNCTION 3 in_range(int4, int4, int8, boolean, boolean) ,
  FUNCTION 3 in_range(int4, int4, int2, boolean, boolean) ,
  FUNCTION 3 in_range(int2, int2, int8, boolean, boolean) ,
  FUNCTION 3 in_range(int2, int2, int4, boolean, boolean) ;
```

請注意，這個定義「多載」（overload）了運算子策略與
支援函式編號：每個編號在家族中都出現了不只一次。只要
同一編號的每個實例各自具有不同的輸入資料型別，這樣做就是允許的。
兩個輸入型別都與某個運算子類別的輸入型別相同的實例，
就是該運算子類別的主要運算子與支援函式，
在大多數情況下，應該被宣告為運算子類別的一部分，而不是
作為家族中鬆散的成員。

在 B-tree 運算子家族中，家族內所有的運算子都必須以相容的方式排序，
詳情請見[第 65.1.2 節](../../internals/indextypes/btree.md#BTREE-BEHAVIOR)。對於家族中的每個
運算子，都必須有一個支援函式，其兩個輸入資料型別與該運算子
相同。建議一個家族應該是完整的，也就是說，對於
每一種資料型別組合，都應包含所有的運算子。每個運算子類別
應只包含其資料型別的非跨型別運算子與支援函式。

要建立一個支援多種資料型別的雜湊運算子家族，必須為
此家族所支援的每一種資料型別，建立相容的雜湊
支援函式。這裡所謂的相容性，是指這些函式必須保證
對於任兩個被家族的相等運算子視為相等的值，
即使這些值屬於不同型別，也都會傳回相同的雜湊碼。
當這些型別具有不同的實體表示方式時，通常很難做到這一點，
但在某些情況下是可行的。
此外，將某個值從運算子家族中表示的一種資料型別，
以隱含或二進位轉型（coercion cast）轉換為運算子家族中表示的另一種資料型別時，
也不能改變計算出的雜湊值。
請注意，每種資料型別只有一個支援函式，而不是每個
相等運算子都各有一個。建議一個家族應該是完整的，也就是為
每一種資料型別組合都提供一個相等運算子。每個運算子類別
應只包含其資料型別的非跨型別相等運算子與
支援函式。

GiST、SP-GiST 與 GIN 索引並沒有任何明確的
跨資料型別操作概念。所支援的運算子集合，
就是特定運算子類別的主要支援函式所能處理的內容。

在 BRIN 中，其要求則取決於提供
運算子類別的框架。對於以 `minmax` 為基礎的運算子類別，
所要求的行為與 B-tree 運算子家族相同：
家族中所有的運算子都必須以相容的方式排序，而轉型
也不能改變相關聯的排序順序。

### 注意

在 PostgreSQL 8.3 之前，並沒有運算子
家族的概念，因此任何打算搭配索引使用的跨資料型別
運算子，都必須直接綁定到索引的運算子
類別中。雖然這種做法仍然可行，但已不建議使用，因為
這樣會讓索引的相依性變得過於廣泛，而且當兩種資料型別
都在同一個運算子家族中擁有運算子時，規劃器能夠更有效地
處理跨資料型別的比較。

<a id="XINDEX-OPCLASS-DEPENDENCIES"></a>

### 36.16.6. 系統對運算子類別的相依性 [#](#XINDEX-OPCLASS-DEPENDENCIES)

<a id="id-1.8.3.19.10.2"></a>

PostgreSQL 使用運算子類別來推斷運算子的
屬性，其用途不僅限於判斷它們是否可以搭配索引使用。因此，
即使你完全不打算為自訂資料型別的任何欄位建立索引，
你可能還是會想要建立運算子類別。

具體來說，有一些 SQL 功能，例如 `ORDER BY` 與
`DISTINCT`，需要對值進行比較與排序。
為了在使用者定義的資料型別上實作這些功能，
PostgreSQL 會尋找該資料型別的預設 B-tree 運算子
類別。此運算子類別中的「等於」成員，定義了系統對於
`GROUP BY` 與 `DISTINCT` 而言的值相等概念，
而該運算子類別所施加的排序順序，則定義了預設的
`ORDER BY` 排序方式。

若某個資料型別沒有預設的 B-tree 運算子類別，系統
會尋找預設的雜湊運算子類別。但由於這種
運算子類別只提供相等性，因此它只能支援分組，
而無法支援排序。

當某個資料型別沒有預設運算子類別時，若你嘗試對該
資料型別使用這些 SQL 功能，就會出現類似「無法識別排序運算子」（could
not identify an ordering operator）的錯誤。

### 注意

在 PostgreSQL 7.4 之前的版本中，
排序與分組操作會隱含地使用名為
`=`、`<` 與 `>` 的運算子。新的
行為改為依賴預設運算子類別，如此便可避免對特定名稱的
運算子行為做出任何假設。

若要依非預設的 B-tree 運算子類別排序，可以在
`USING` 選項中指定該類別的小於運算子，
例如：

```

SELECT * FROM mytable ORDER BY somecol USING ~<~;
```

或者，在 `USING` 中指定該類別的大於運算子，
可以選擇遞減順序排序。

使用者定義型別的陣列比較，同樣依賴該型別預設
B-tree 運算子類別所定義的語意。若沒有
預設的 B-tree 運算子類別，但有預設的雜湊運算子類別，
則支援陣列相等性比較，但不支援排序比較。

另一項需要更多資料型別專屬知識的 SQL 功能，
是視窗函式（window function）的 `RANGE`
*`offset`*
`PRECEDING`／`FOLLOWING` 框架選項
（請參閱[第 4.2.8 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)）。
對於這樣的查詢：

```

SELECT sum(x) OVER (ORDER BY x RANGE BETWEEN 5 PRECEDING AND 10 FOLLOWING)
  FROM mytable;
```

光是知道如何依 `x` 排序是不夠的；
資料庫還必須理解如何對目前資料列的 `x` 值
「減去 5」或「加上 10」，才能確定目前
視窗框架的邊界。要比較所得出的邊界與其他資料列的
`x` 值，可以使用定義 `ORDER BY` 排序方式的
B-tree 運算子類別所提供的比較運算子——但
加法與減法運算子並不屬於該運算子類別的一部分，那麼
應該使用哪一個呢？將這個選擇寫死並不理想，
因為不同的排序順序（不同的 B-tree 運算子類別）可能
需要不同的行為。因此，一個 B-tree 運算子類別可以指定
一個 *in_range* 支援函式，用來封裝符合其排序順序的
加法與減法行為。它甚至可以提供超過一個 in_range 支援函式，
以應付在 `RANGE` 子句中，有超過一種資料型別
適合用作偏移量的情況。
若視窗的 `ORDER
BY` 子句所關聯的 B-tree 運算子類別沒有相符的 in_range 支援函式，
則不支援 `RANGE` *`offset`*
`PRECEDING`／`FOLLOWING`
選項。

另一個重要的重點是，出現在雜湊運算子家族中的相等運算子，
是雜湊連接（hash join）、雜湊彙總（hash aggregation）以及相關最佳化
的候選對象。雜湊運算子家族在此不可或缺，因為它
識別出要使用的雜湊函式。

<a id="XINDEX-ORDERING-OPS"></a>

### 36.16.7. 排序運算子 [#](#XINDEX-ORDERING-OPS)

某些索引存取方法（目前僅有 GiST 與 SP-GiST）支援
*排序運算子*（ordering operator）的概念。到目前為止我們所討論的，
都是*搜尋運算子*（search operator）。搜尋運算子是指
可以搜尋索引，找出所有滿足
`WHERE`
*`indexed_column`*
*`operator`*
*`constant`*
的資料列所使用的運算子。
請注意，這裡並沒有承諾相符資料列會以何種順序
傳回。相對地，排序運算子並不限制
可傳回的資料列集合，而是決定它們的順序。
排序運算子是指可以掃描索引、以
`ORDER BY`
*`indexed_column`*
*`operator`*
*`constant`*
所表示的順序傳回資料列所使用的運算子。
之所以如此定義排序運算子，是因為如果該運算子是用來
測量距離的，這樣的定義就能支援最近鄰搜尋。
舉例來說，像這樣的查詢：

```

SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

會找出離指定目標點最近的十個地點。「location」
欄位上的 GiST 索引之所以能有效率地完成此操作，是因為
`<->` 是一個排序運算子。

搜尋運算子必須傳回布林結果，而排序運算子
通常會傳回其他型別的值，例如用於距離的 float 或 numeric。
這個型別通常與被索引的資料型別不同。
為了避免對不同資料型別的行為做出寫死的假設，
排序運算子的定義必須指名
一個 B-tree 運算子家族，用來指定結果資料型別的排序方式。
如同前一節所述，B-tree 運算子家族定義了
PostgreSQL 對排序的概念，因此這是一種
自然的表示方式。由於點（point）型別的 `<->`
運算子傳回 `float8`，因此可以在建立運算子類別的命令中
這樣指定：

```

OPERATOR 15    <-> (point, point) FOR ORDER BY float_ops
```

其中 `float_ops` 是內建的運算子家族，其中包含
對 `float8` 的操作。此宣告表示此索引
能夠以 `<->` 運算子遞增值的順序，
傳回資料列。

<a id="XINDEX-OPCLASS-FEATURES"></a>

### 36.16.8. 運算子類別的特殊功能 [#](#XINDEX-OPCLASS-FEATURES)

還有兩項我們尚未討論到的運算子類別特殊功能，
之所以尚未討論，主要是因為它們對最常用的
索引方法而言並不實用。

通常，將某個運算子宣告為某個運算子類別（或家族）的成員，
表示索引方法可以精確地找出使用該運算子
滿足 `WHERE` 條件的資料列集合。舉例來說：

```

SELECT * FROM table WHERE integer_column < 4;
```

可以由整數欄位上的 B-tree 索引精確地滿足。
但也有一些情況，索引只能做為找出相符資料列的
不精確指引。舉例來說，若 GiST 索引只儲存幾何物件的
外框（bounding box），那麼它就無法精確地滿足測試
非矩形物件（例如多邊形）之間重疊關係的 `WHERE`
條件。不過我們仍然可以利用索引，找出外框與
目標物件的外框重疊的物件，然後只對索引所找出的
物件執行精確的重疊測試。若適用這種情境，
就稱此索引對該運算子而言是「有損的」（lossy）。有損的索引
搜尋，是透過讓索引方法在某資料列可能符合、也可能不符合
查詢條件時傳回一個*重新檢查*（recheck）旗標來實作的。
核心系統接著會對取出的資料列測試原始的查詢條件，
以判斷是否應該將其傳回，視為有效的相符結果。只要索引保證會傳回
所有必要的資料列（可能再加上一些額外的資料列，這些額外的資料列
可以透過執行原始的運算子呼叫來排除），這種做法就可行。支援有損搜尋的索引方法
（目前為 GiST、SP-GiST 與 GIN）允許個別
運算子類別的支援函式設定重新檢查旗標，因此本質上
這是一項運算子類別層級的功能。

再次考慮我們只在索引中儲存複雜物件（例如多邊形）
外框的情況。在這種
情況下，在索引項目中儲存整個多邊形並沒有太大的價值——
我們不妨只儲存一個更簡單的
`box` 型別物件。這種情況可以透過 `CREATE OPERATOR CLASS`
中的 `STORAGE` 選項來表示：我們可以這樣寫：

```

CREATE OPERATOR CLASS polygon_ops
    DEFAULT FOR TYPE polygon USING gist AS
        ...
        STORAGE box;
```

目前，只有 GiST、SP-GiST、GIN 與 BRIN 索引方法支援與
欄位資料型別不同的 `STORAGE` 型別。
GiST 的 `compress` 與 `decompress` 支援
常式，在使用 `STORAGE` 時必須處理資料型別的
轉換。同樣地，當儲存型別不同時，SP-GiST 也需要一個
`compress` 支援函式來轉換為儲存型別；
若某個 SP-GiST 運算子類別也支援取回資料，則反向的
轉換必須由 `consistent` 函式來處理。
在 GIN 中，`STORAGE` 型別識別的是
「鍵值」的型別，這通常與被索引欄位的型別
不同——舉例來說，用於整數陣列欄位的運算子類別，
其鍵值可能就只是整數。GIN 的
`extractValue` 與 `extractQuery` 支援
常式負責從已索引的值中擷取鍵值。
BRIN 與 GIN 類似：`STORAGE` 型別識別的是
所儲存摘要值的型別，運算子類別的支援
程序則負責正確地解讀這些摘要值。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xindex.html)（原文版本：18.6；核對日期：2026-10-23）
