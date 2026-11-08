# 36.16.3. 索引方法支援常式

<a id="XINDEX-SUPPORT"></a>

## 36.16.3. 索引方法支援常式 [#](#xindex-support) <a href="#xindex-support" id="xindex-support"></a>

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
支援函式，如[表 36.9](#xindex-btree-support-table)所示（原文此處寫作「四個」，但表 36.9 實際列出編號 2～6 共五個可選的支援函式）。
這些支援函式的要求進一步說明於
[第 65.1.3 節](../../../internals/indextypes/btree.md#btree-support-funcs)。

<a id="XINDEX-BTREE-SUPPORT-TABLE"></a>

### 表 36.9. B-Tree 支援函式 [#](#xindex-btree-support-table) <a href="#xindex-btree-support-table" id="xindex-btree-support-table"></a>

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
另外提供兩個，如[表 36.10](#xindex-hash-support-table)所示。

<a id="XINDEX-HASH-SUPPORT-TABLE"></a>

### 表 36.10. 雜湊支援函式 [#](#xindex-hash-support-table) <a href="#xindex-hash-support-table" id="xindex-hash-support-table"></a>

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
如[表 36.11](#xindex-gist-support-table)所示。
（更多資訊請參閱[第 65.2 節](../../../internals/indextypes/gist.md)。）

<a id="XINDEX-GIST-SUPPORT-TABLE"></a>

### 表 36.11. GiST 支援函式 [#](#xindex-gist-support-table) <a href="#xindex-gist-support-table" id="xindex-gist-support-table"></a>

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
[表 36.12](#xindex-spgist-support-table)所示。
（更多資訊請參閱[第 65.3 節](../../../internals/indextypes/spgist.md)。）

<a id="XINDEX-SPGIST-SUPPORT-TABLE"></a>

### 表 36.12. SP-GiST 支援函式 [#](#xindex-spgist-support-table) <a href="#xindex-spgist-support-table" id="xindex-spgist-support-table"></a>

<table border="1" class="table" summary="SP-GiST Support Functions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>函式</th><th>說明</th><th>支援編號</th></tr></thead><tbody><tr><td><code class="function">config</code></td><td>提供運算子類別的基本資訊</td><td>1</td></tr><tr><td><code class="function">choose</code></td><td>判斷如何將新值插入內部元組（inner tuple）</td><td>2</td></tr><tr><td><code class="function">picksplit</code></td><td>判斷如何分割一組值</td><td>3</td></tr><tr><td><code class="function">inner_consistent</code></td><td>判斷查詢需要搜尋哪些
        子分區</td><td>4</td></tr><tr><td><code class="function">leaf_consistent</code></td><td>判斷鍵值是否滿足
        查詢限定條件</td><td>5</td></tr><tr><td><code class="function">options</code></td><td>定義此運算子類別專屬的選項
        （可選）</td><td>6</td></tr></tbody></table>

<br>

GIN 索引有七個支援函式，其中四個是可選的，
如[表 36.13](#xindex-gin-support-table)所示。
（更多資訊請參閱[第 65.4 節](../../../internals/indextypes/gin.md)。）

<a id="XINDEX-GIN-SUPPORT-TABLE"></a>

### 表 36.13. GIN 支援函式 [#](#xindex-gin-support-table) <a href="#xindex-gin-support-table" id="xindex-gin-support-table"></a>

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
如[表 36.14](#xindex-brin-support-table)所示。某些基本函式變體
需要提供額外的支援函式。
（更多資訊請參閱[第 65.5.3 節](../../../internals/indextypes/brin/brin-extensibility.md#brin-extensibility)。）

<a id="XINDEX-BRIN-SUPPORT-TABLE"></a>

### 表 36.14. BRIN 支援函式 [#](#xindex-brin-support-table) <a href="#xindex-brin-support-table" id="xindex-brin-support-table"></a>

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

[返回 36.16. 將擴充功能與索引介接](../xindex.md#xindex)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xindex.html)（原文版本：18.6；核對日期：2026-10-23）
