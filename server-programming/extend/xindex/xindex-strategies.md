# 36.16.2. 索引方法策略

<a id="XINDEX-STRATEGIES"></a>

## 36.16.2. 索引方法策略 [#](#xindex-strategies) <a href="#xindex-strategies" id="xindex-strategies"></a>

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

B-tree 索引方法定義了五種策略，如[表 36.3](#xindex-btree-strat-table)所示。

<a id="XINDEX-BTREE-STRAT-TABLE"></a>

### 表 36.3. B-Tree 策略 [#](#xindex-btree-strat-table) <a href="#xindex-btree-strat-table" id="xindex-btree-strat-table"></a>

<table border="1" class="table" summary="B-Tree Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>小於</td><td>1</td></tr><tr><td>小於等於</td><td>2</td></tr><tr><td>等於</td><td>3</td></tr><tr><td>大於等於</td><td>4</td></tr><tr><td>大於</td><td>5</td></tr></tbody></table>

<br>

雜湊索引只支援相等比較，因此它們只使用一種
策略，如[表 36.4](#xindex-hash-strat-table)所示。

<a id="XINDEX-HASH-STRAT-TABLE"></a>

### 表 36.4. 雜湊策略 [#](#xindex-hash-strat-table) <a href="#xindex-hash-strat-table" id="xindex-hash-strat-table"></a>

<table border="1" class="table" summary="Hash Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>等於</td><td>1</td></tr></tbody></table>

<br>

GiST 索引更具彈性：它們根本沒有固定的一組
策略。取而代之，每個特定 GiST 運算子類別的「一致性」（consistency）支援常式，
會以自己的方式解讀策略編號。舉例來說，內建 GiST 索引
運算子類別中有幾個是用來對二維幾何物件建立索引，提供了
[表 36.5](#xindex-rtree-strat-table)所示的「R-tree」策略。其中四種是真正的
二維測試（重疊、相同、包含、被包含）；
另外四種只考慮 X 方向；其餘四種
則是在 Y 方向提供相同的測試。

<a id="XINDEX-RTREE-STRAT-TABLE"></a>

### 表 36.5. GiST 二維「R-tree」策略 [#](#xindex-rtree-strat-table) <a href="#xindex-rtree-strat-table" id="xindex-rtree-strat-table"></a>

<table border="1" class="table" summary="GiST Two-Dimensional R-tree Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>嚴格在左側</td><td>1</td></tr><tr><td>不延伸至右側</td><td>2</td></tr><tr><td>重疊</td><td>3</td></tr><tr><td>不延伸至左側</td><td>4</td></tr><tr><td>嚴格在右側</td><td>5</td></tr><tr><td>相同</td><td>6</td></tr><tr><td>包含</td><td>7</td></tr><tr><td>被包含</td><td>8</td></tr><tr><td>不延伸至上方</td><td>9</td></tr><tr><td>嚴格在下方</td><td>10</td></tr><tr><td>嚴格在上方</td><td>11</td></tr><tr><td>不延伸至下方</td><td>12</td></tr></tbody></table>

<br>

SP-GiST 索引在彈性方面與 GiST 索引類似：它們同樣沒有
固定的一組策略。取而代之，每個運算子
類別的支援常式會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建點（point）運算子類別所使用的策略編號如
[表 36.6](#xindex-spgist-point-strat-table)所示。

<a id="XINDEX-SPGIST-POINT-STRAT-TABLE"></a>

### 表 36.6. SP-GiST 點策略 [#](#xindex-spgist-point-strat-table) <a href="#xindex-spgist-point-strat-table" id="xindex-spgist-point-strat-table"></a>

<table border="1" class="table" summary="SP-GiST Point Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>嚴格在左側</td><td>1</td></tr><tr><td>嚴格在右側</td><td>5</td></tr><tr><td>相同</td><td>6</td></tr><tr><td>被包含</td><td>8</td></tr><tr><td>嚴格在下方</td><td>10</td></tr><tr><td>嚴格在上方</td><td>11</td></tr></tbody></table>

<br>

GIN 索引與 GiST、SP-GiST 索引類似，同樣沒有
固定的一組策略。取而代之，每個運算子類別的支援常式
會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建陣列運算子類別所使用的策略編號如
[表 36.7](#xindex-gin-array-strat-table)所示。

<a id="XINDEX-GIN-ARRAY-STRAT-TABLE"></a>

### 表 36.7. GIN 陣列策略 [#](#xindex-gin-array-strat-table) <a href="#xindex-gin-array-strat-table" id="xindex-gin-array-strat-table"></a>

<table border="1" class="table" summary="GIN Array Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>重疊</td><td>1</td></tr><tr><td>包含</td><td>2</td></tr><tr><td>被包含</td><td>3</td></tr><tr><td>等於</td><td>4</td></tr></tbody></table>

<br>

BRIN 索引與 GiST、SP-GiST 及 GIN 索引類似，同樣沒有
固定的一組策略。取而代之，每個運算子類別的支援常式
會依照該運算子類別的定義來解讀策略編號。舉例來說，
內建 `Minmax` 運算子類別所使用的策略編號如
[表 36.8](#xindex-brin-minmax-strat-table)所示。

<a id="XINDEX-BRIN-MINMAX-STRAT-TABLE"></a>

### 表 36.8. BRIN Minmax 策略 [#](#xindex-brin-minmax-strat-table) <a href="#xindex-brin-minmax-strat-table" id="xindex-brin-minmax-strat-table"></a>

<table border="1" class="table" summary="BRIN Minmax Strategies"><colgroup><col/><col/></colgroup><thead><tr><th>操作</th><th>策略編號</th></tr></thead><tbody><tr><td>小於</td><td>1</td></tr><tr><td>小於等於</td><td>2</td></tr><tr><td>等於</td><td>3</td></tr><tr><td>大於等於</td><td>4</td></tr><tr><td>大於</td><td>5</td></tr></tbody></table>

<br>

請注意，以上所列出的所有運算子都會傳回布林值。實際上，
所有被定義為索引方法搜尋運算子的運算子都必須
傳回 `boolean` 型別，因為它們必須出現在
`WHERE` 子句的最上層，才能搭配索引使用。
（有些索引存取方法也支援*排序運算子*，
這類運算子通常不會傳回布林值；此功能會在
[第 36.16.7 節](../xindex.md#xindex-ordering-ops)討論。）

[返回 36.16. 將擴充功能與索引介接](../xindex.md#xindex)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xindex.html)（原文版本：18.6；核對日期：2026-10-23）
