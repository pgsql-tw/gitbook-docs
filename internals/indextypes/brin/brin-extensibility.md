# 65.5.3. 擴充性

<a id="BRIN-EXTENSIBILITY"></a>

## 65.5.3. 擴充性 [#](#brin-extensibility) <a href="#brin-extensibility" id="brin-extensibility"></a>

BRIN 介面具有高度的抽象性，只要求存取方法的實作者實作所存取資料型別的語意。BRIN 層本身會負責並行處理、日誌記錄以及索引結構的搜尋。

要讓 BRIN 存取方法運作，只需要實作幾個使用者定義的方法，這些方法定義了索引中所儲存之摘要值的行為，以及它們與掃描鍵互動的方式。簡而言之，BRIN 結合了擴充性與通用性、程式碼重用，以及簡潔的介面。

BRIN 的運算子類別必須提供四個方法：

`BrinOpcInfo *opcInfo(Oid type_oid)`

傳回被索引欄位之摘要資料的內部資訊。傳回值必須指向一個以 palloc 配置的 `BrinOpcInfo`，其定義如下：

```

    typedef struct BrinOpcInfo
    {
        /* Number of columns stored in an index column of this opclass */
        uint16      oi_nstored;

        /* Opaque pointer for the opclass' private use */
        void       *oi_opaque;

        /* Type cache entries of the stored columns */
        TypeCacheEntry *oi_typcache[FLEXIBLE_ARRAY_MEMBER];
    } BrinOpcInfo;
```

`BrinOpcInfo`.`oi_opaque` 可供運算子類別的常式在索引掃描期間於支援函式之間傳遞資訊。

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey *keys, int nkeys)`

傳回所有 ScanKey 項目是否都與某個範圍的給定索引值一致。要使用的屬性編號會作為掃描鍵的一部分傳入。同一屬性的多個掃描鍵可以一次傳入；項目數量由 `nkeys` 參數決定。

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey key)`

傳回 ScanKey 是否與某個範圍的給定索引值一致。要使用的屬性編號會作為掃描鍵的一部分傳入。這是 consistent 函式較舊、具向後相容性的變體。

`bool addValue(BrinDesc *bdesc, BrinValues *column, Datum newval, bool isnull)`

給定一個索引 tuple 與一個被索引的值，修改該 tuple 的指定屬性，使其額外代表這個新值。如果對該 tuple 做了任何修改，則傳回 `true`。

`bool unionTuples(BrinDesc *bdesc, BrinValues *a, BrinValues *b)`

合併兩個索引 tuple。給定兩個索引 tuple，修改其中第一個 tuple 的指定屬性，使其同時代表這兩個 tuple。第二個 tuple 不會被修改。

BRIN 的運算子類別可以選擇性地指定下列方法：

`void options(local_relopts *relopts)`

定義一組使用者可見的參數，用以控制運算子類別的行為。

`options` 函式會收到一個指向 `local_relopts` 結構的指標，該結構需要填入一組運算子類別專屬的選項。其他支援函式可以使用 `PG_HAS_OPCLASS_OPTIONS()` 與 `PG_GET_OPCLASS_OPTIONS()` 巨集存取這些選項。

由於被索引值的鍵擷取方式，以及鍵在 BRIN 中的表示方式都具有彈性，它們可能取決於使用者指定的參數。

核心發行版本支援四種運算子類別：minmax、minmax-multi、inclusion 與 bloom。使用它們的運算子類別定義會視情況隨附於核心內建的資料型別。使用者可以用等效的定義，為其他資料型別定義額外的運算子類別，而不必撰寫任何原始碼；只要宣告適當的系統目錄項目即可。請注意，關於運算子策略語意的假設已內嵌在支援函式的原始碼中。

也可以有實作完全不同語意的運算子類別，前提是撰寫了上述四個主要支援函式的實作。請注意，不保證跨主要版本的向後相容性：例如，之後的版本可能會需要額外的支援函式。

要為實作全序集合的資料型別撰寫運算子類別，可以搭配相應的運算子使用 minmax 支援函式，如[表 65.5](#brin-extensibility-minmax-table) 所示。所有運算子類別成員（函式與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-MINMAX-TABLE"></a>

### 表 65.5. minmax 運算子類別的函式與支援編號 [#](#brin-extensibility-minmax-table) <a href="#brin-extensibility-minmax-table" id="brin-extensibility-minmax-table"></a>

<table border="1" class="table" summary="minmax 運算子類別的函式與支援編號"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援函式 1</td><td>內部函式 <code class="function">brin_minmax_opcinfo()</code></td></tr><tr><td>支援函式 2</td><td>內部函式 <code class="function">brin_minmax_add_value()</code></td></tr><tr><td>支援函式 3</td><td>內部函式 <code class="function">brin_minmax_consistent()</code></td></tr><tr><td>支援函式 4</td><td>內部函式 <code class="function">brin_minmax_union()</code></td></tr><tr><td>運算子策略 1</td><td>「小於」運算子</td></tr><tr><td>運算子策略 2</td><td>「小於或等於」運算子</td></tr><tr><td>運算子策略 3</td><td>「等於」運算子</td></tr><tr><td>運算子策略 4</td><td>「大於或等於」運算子</td></tr><tr><td>運算子策略 5</td><td>「大於」運算子</td></tr></tbody></table>

<br>

若要為某種複雜資料型別撰寫運算子類別，且該型別的值包含在另一種型別之中，可以搭配相應的運算子使用 inclusion 支援函式，如[表 65.6](#brin-extensibility-inclusion-table) 所示。它只需要一個額外的函式，而該函式可以用任何語言撰寫。可以定義更多函式來提供額外的功能。所有運算子都是選擇性的。某些運算子需要其他運算子，如表中的相依關係所示。

<a id="BRIN-EXTENSIBILITY-INCLUSION-TABLE"></a>

### 表 65.6. inclusion 運算子類別的函式與支援編號 [#](#brin-extensibility-inclusion-table) <a href="#brin-extensibility-inclusion-table" id="brin-extensibility-inclusion-table"></a>

<table border="1" class="table" summary="inclusion 運算子類別的函式與支援編號"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th><th>相依於</th></tr></thead><tbody><tr><td>支援函式 1</td><td>內部函式 <code class="function">brin_inclusion_opcinfo()</code></td><td> </td></tr><tr><td>支援函式 2</td><td>內部函式 <code class="function">brin_inclusion_add_value()</code></td><td> </td></tr><tr><td>支援函式 3</td><td>內部函式 <code class="function">brin_inclusion_consistent()</code></td><td> </td></tr><tr><td>支援函式 4</td><td>內部函式 <code class="function">brin_inclusion_union()</code></td><td> </td></tr><tr><td>支援函式 11</td><td>合併兩個元素的函式</td><td> </td></tr><tr><td>支援函式 12</td><td>檢查兩個元素是否可合併的選擇性函式</td><td> </td></tr><tr><td>支援函式 13</td><td>檢查某元素是否包含於另一元素之中的選擇性函式</td><td> </td></tr><tr><td>支援函式 14</td><td>檢查元素是否為空的選擇性函式</td><td> </td></tr><tr><td>運算子策略 1</td><td>「位於左側」運算子</td><td>運算子策略 4</td></tr><tr><td>運算子策略 2</td><td>「不延伸至右側」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 3</td><td>「重疊」運算子</td><td> </td></tr><tr><td>運算子策略 4</td><td>「不延伸至左側」運算子</td><td>運算子策略 1</td></tr><tr><td>運算子策略 5</td><td>「位於右側」運算子</td><td>運算子策略 2</td></tr><tr><td>運算子策略 6, 18</td><td>「相同或等於」運算子</td><td>運算子策略 7</td></tr><tr><td>運算子策略 7, 16, 24, 25</td><td>「包含或等於」運算子</td><td> </td></tr><tr><td>運算子策略 8, 26, 27</td><td>「被包含或等於」運算子</td><td>運算子策略 3</td></tr><tr><td>運算子策略 9</td><td>「不延伸至上方」運算子</td><td>運算子策略 11</td></tr><tr><td>運算子策略 10</td><td>「位於下方」運算子</td><td>運算子策略 12</td></tr><tr><td>運算子策略 11</td><td>「位於上方」運算子</td><td>運算子策略 9</td></tr><tr><td>運算子策略 12</td><td>「不延伸至下方」運算子</td><td>運算子策略 10</td></tr><tr><td>運算子策略 20</td><td>「小於」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 21</td><td>「小於或等於」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 22</td><td>「大於」運算子</td><td>運算子策略 1</td></tr><tr><td>運算子策略 23</td><td>「大於或等於」運算子</td><td>運算子策略 1</td></tr></tbody></table>

<br>

支援函式編號 1 到 10 保留給 BRIN 內部函式使用，因此 SQL 層級的函式從編號 11 開始。支援函式編號 11 是建立索引所需的主要函式。它應該接受兩個資料型別與運算子類別相同的引數，並傳回兩者的聯集。如果 inclusion 運算子類別是以 `STORAGE` 參數定義的，它可以儲存不同資料型別的聯集值。聯集函式的傳回值應該與 `STORAGE` 資料型別相符。

支援函式編號 12 與 14 用於支援內建資料型別的不規則之處。函式編號 12 用於支援來自不同位址家族、無法合併的網路位址。函式編號 14 用於支援空範圍。函式編號 13 是選擇性但建議提供的函式，它允許在新值傳給聯集函式之前先加以檢查。由於 BRIN 框架在聯集沒有改變時可以略過某些操作，使用此函式可以提升索引效能。

要為只實作等於運算子並支援雜湊的資料型別撰寫運算子類別，可以搭配相應的運算子使用 bloom 支援程序，如[表 65.7](#brin-extensibility-bloom-table) 所示。所有運算子類別成員（程序與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-BLOOM-TABLE"></a>

### 表 65.7. bloom 運算子類別的程序與支援編號 [#](#brin-extensibility-bloom-table) <a href="#brin-extensibility-bloom-table" id="brin-extensibility-bloom-table"></a>

<table border="1" class="table" summary="bloom 運算子類別的程序與支援編號"><colgroup><col/><col/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援程序 1</td><td>內部函式 <code class="function">brin_bloom_opcinfo()</code></td></tr><tr><td>支援程序 2</td><td>內部函式 <code class="function">brin_bloom_add_value()</code></td></tr><tr><td>支援程序 3</td><td>內部函式 <code class="function">brin_bloom_consistent()</code></td></tr><tr><td>支援程序 4</td><td>內部函式 <code class="function">brin_bloom_union()</code></td></tr><tr><td>支援程序 5</td><td>內部函式 <code class="function">brin_bloom_options()</code></td></tr><tr><td>支援程序 11</td><td>計算元素雜湊值的函式</td></tr><tr><td>運算子策略 1</td><td>「等於」運算子</td></tr></tbody></table>

<br>

支援程序編號 1-10 保留給 BRIN 內部函式使用，因此 SQL 層級的函式從編號 11 開始。支援函式編號 11 是建立索引所需的主要函式。它應該接受一個資料型別與運算子類別相同的引數，並傳回該值的雜湊。

minmax-multi 運算子類別同樣適用於實作全序集合的資料型別，可以視為 minmax 運算子類別的簡單延伸。minmax 運算子類別會將每個區塊範圍的值摘要成單一連續區間，而 minmax-multi 則允許摘要成多個較小的區間，以改善對離群值的處理。可以搭配相應的運算子使用 minmax-multi 支援程序，如[表 65.8](#brin-extensibility-minmax-multi-table) 所示。所有運算子類別成員（程序與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE"></a>

### 表 65.8. minmax-multi 運算子類別的程序與支援編號 [#](#brin-extensibility-minmax-multi-table) <a href="#brin-extensibility-minmax-multi-table" id="brin-extensibility-minmax-multi-table"></a>

<table border="1" class="table" summary="minmax-multi 運算子類別的程序與支援編號"><colgroup><col/><col/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援程序 1</td><td>內部函式 <code class="function">brin_minmax_multi_opcinfo()</code></td></tr><tr><td>支援程序 2</td><td>內部函式 <code class="function">brin_minmax_multi_add_value()</code></td></tr><tr><td>支援程序 3</td><td>內部函式 <code class="function">brin_minmax_multi_consistent()</code></td></tr><tr><td>支援程序 4</td><td>內部函式 <code class="function">brin_minmax_multi_union()</code></td></tr><tr><td>支援程序 5</td><td>內部函式 <code class="function">brin_minmax_multi_options()</code></td></tr><tr><td>支援程序 11</td><td>計算兩個值之間距離（範圍長度）的函式</td></tr><tr><td>運算子策略 1</td><td>「小於」運算子</td></tr><tr><td>運算子策略 2</td><td>「小於或等於」運算子</td></tr><tr><td>運算子策略 3</td><td>「等於」運算子</td></tr><tr><td>運算子策略 4</td><td>「大於或等於」運算子</td></tr><tr><td>運算子策略 5</td><td>「大於」運算子</td></tr></tbody></table>

<br>

minmax 與 inclusion 運算子類別都支援跨資料型別的運算子，不過如此一來相依關係會變得更複雜。minmax 運算子類別要求定義一整組兩個引數資料型別相同的運算子。它允許藉由定義額外幾組運算子來支援其他資料型別。inclusion 運算子類別的運算子策略相依於另一個運算子策略（如[表 65.6](#brin-extensibility-inclusion-table) 所示），或相依於與自身相同的運算子策略。它們要求相依的運算子以 `STORAGE` 資料型別作為左側引數，並以另一個受支援的資料型別作為受支援運算子的右側引數。minmax 的範例請參閱 `float4_minmax_ops`，inclusion 的範例請參閱 `box_inclusion_ops`。
[返回 65.5. BRIN 索引](../brin.md#brin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/brin.html)（原文版本：18.6；核對日期：2026-10-12）
