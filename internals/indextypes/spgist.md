<a id="SPGIST"></a>

## 65.3. SP-GiST 索引 [#](#SPGIST)

[65.3.1. 簡介](spgist.md#SPGIST-INTRO)

[65.3.2. 內建運算子類別](spgist.md#SPGIST-BUILTIN-OPCLASSES)

[65.3.3. 擴充性](spgist.md#SPGIST-EXTENSIBILITY)

[65.3.4. 實作](spgist.md#SPGIST-IMPLEMENTATION)

[65.3.5. 範例](spgist.md#SPGIST-EXAMPLES)

<a id="id-1.10.17.4.2"></a>
<a id="SPGIST-INTRO"></a>

### 65.3.1. 簡介 [#](#SPGIST-INTRO)

SP-GiST 是 space-partitioned GiST（空間分割 GiST）的縮寫。SP-GiST 支援分割式搜尋樹，有助於開發各種不同的非平衡資料結構，例如四元樹（quad-tree）、k-d 樹與基數樹（radix tree，即 trie）。這些結構的共同特徵是會反覆將搜尋空間劃分成不必大小相等的分割區。與分割規則相當契合的搜尋可以非常快速。

這些常見的資料結構原本是為記憶體內使用而開發的。在主記憶體中，它們通常被設計成一組由指標連結、動態配置的節點。這並不適合直接儲存在磁碟上，因為這些指標鏈可能相當長，會需要過多的磁碟存取。相反地，以磁碟為基礎的資料結構應該具有高扇出（fanout），以將 I/O 降到最低。SP-GiST 所處理的挑戰，是將搜尋樹節點對應到磁碟頁面，使搜尋即使走訪許多節點，也只需要存取少數幾個磁碟頁面。

與 GiST 一樣，SP-GiST 的目的是讓資料型別領域的專家（而非資料庫專家）能夠開發具有適當存取方法的自訂資料型別。

這裡的部分資訊取自普渡大學（Purdue University）SP-GiST 索引專案的[網站](https://www.cs.purdue.edu/spgist/)。PostgreSQL 中的 SP-GiST 實作主要由 Teodor Sigaev 與 Oleg Bartunov 維護，在他們的[網站](http://www.sai.msu.su/~megera/wiki/spgist_dev)上有更多資訊。

<a id="SPGIST-BUILTIN-OPCLASSES"></a>

### 65.3.2. 內建運算子類別 [#](#SPGIST-BUILTIN-OPCLASSES)

PostgreSQL 核心發行版本包含[表 65.2](spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE) 所列的 SP-GiST 運算子類別。

<a id="SPGIST-BUILTIN-OPCLASSES-TABLE"></a>

**表 65.2. 內建 SP-GiST 運算子類別**

<table border="1" class="table" summary="內建 SP-GiST 運算子類別"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>可索引運算子</th><th>排序運算子</th></tr></thead><tbody><tr><td rowspan="12" valign="middle"><code class="literal">box_ops</code></td><td><code class="literal">&lt;&lt; (box,box)</code></td><td rowspan="12" valign="middle"><code class="literal">&lt;-&gt; (box,point)</code></td></tr><tr><td><code class="literal">&amp;&lt; (box,box)</code></td></tr><tr><td><code class="literal">&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&gt;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&lt;@ (box,box)</code></td></tr><tr><td><code class="literal">@&gt; (box,box)</code></td></tr><tr><td><code class="literal">~= (box,box)</code></td></tr><tr><td><code class="literal">&amp;&amp; (box,box)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (box,box)</code></td></tr><tr><td rowspan="11" valign="middle"><code class="literal">inet_ops</code></td><td><code class="literal">&lt;&lt; (inet,inet)</code></td><td rowspan="11" valign="middle"> </td></tr><tr><td><code class="literal">&lt;&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt;= (inet,inet)</code></td></tr><tr><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&amp;&amp; (inet,inet)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">kd_point_ops</code></td><td><code class="literal">|&gt;&gt; (point,point)</code></td><td rowspan="6" valign="middle"><code class="literal">&lt;-&gt; (point,point)</code></td></tr><tr><td><code class="literal">&lt;&lt; (point,point)</code></td></tr><tr><td><code class="literal">&gt;&gt; (point,point)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (point,point)</code></td></tr><tr><td><code class="literal">~= (point,point)</code></td></tr><tr><td><code class="literal">&lt;@ (point,box)</code></td></tr><tr><td rowspan="12" valign="middle"><code class="literal">poly_ops</code></td><td><code class="literal">&lt;&lt; (polygon,polygon)</code></td><td rowspan="12" valign="middle"><code class="literal">&lt;-&gt; (polygon,point)</code></td></tr><tr><td><code class="literal">&amp;&lt; (polygon,polygon)</code></td></tr><tr><td><code class="literal">&amp;&gt; (polygon,polygon)</code></td></tr><tr><td><code class="literal">&gt;&gt; (polygon,polygon)</code></td></tr><tr><td><code class="literal">&lt;@ (polygon,polygon)</code></td></tr><tr><td><code class="literal">@&gt; (polygon,polygon)</code></td></tr><tr><td><code class="literal">~= (polygon,polygon)</code></td></tr><tr><td><code class="literal">&amp;&amp; (polygon,polygon)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (polygon,polygon)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (polygon,polygon)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (polygon,polygon)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (polygon,polygon)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">quad_point_ops</code></td><td><code class="literal">|&gt;&gt; (point,point)</code></td><td rowspan="6" valign="middle"><code class="literal">&lt;-&gt; (point,point)</code></td></tr><tr><td><code class="literal">&lt;&lt; (point,point)</code></td></tr><tr><td><code class="literal">&gt;&gt; (point,point)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (point,point)</code></td></tr><tr><td><code class="literal">~= (point,point)</code></td></tr><tr><td><code class="literal">&lt;@ (point,box)</code></td></tr><tr><td rowspan="10" valign="middle"><code class="literal">range_ops</code></td><td><code class="literal">= (anyrange,anyrange)</code></td><td rowspan="10" valign="middle"> </td></tr><tr><td><code class="literal">&amp;&amp; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyelement)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;@ (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">-|- (anyrange,anyrange)</code></td></tr><tr><td rowspan="10" valign="middle"><code class="literal">text_ops</code></td><td><code class="literal">= (text,text)</code></td><td rowspan="10" valign="middle"> </td></tr><tr><td><code class="literal">&lt; (text,text)</code></td></tr><tr><td><code class="literal">&lt;= (text,text)</code></td></tr><tr><td><code class="literal">&gt; (text,text)</code></td></tr><tr><td><code class="literal">&gt;= (text,text)</code></td></tr><tr><td><code class="literal">~&lt;~ (text,text)</code></td></tr><tr><td><code class="literal">~&lt;=~ (text,text)</code></td></tr><tr><td><code class="literal">~&gt;=~ (text,text)</code></td></tr><tr><td><code class="literal">~&gt;~ (text,text)</code></td></tr><tr><td><code class="literal">^@ (text,text)</code></td></tr></tbody></table>

<br>

在 `point` 型別的兩個運算子類別中，`quad_point_ops` 是預設的。`kd_point_ops` 支援相同的運算子，但使用不同的索引資料結構，在某些應用中可能提供較佳的效能。

`quad_point_ops`、`kd_point_ops` 與 `poly_ops` 運算子類別支援 `<->` 排序運算子，可對被索引的點或多邊形資料集進行 k 最近鄰（`k-NN`）搜尋。

<a id="SPGIST-EXTENSIBILITY"></a>

### 65.3.3. 擴充性 [#](#SPGIST-EXTENSIBILITY)

SP-GiST 提供具有高度抽象性的介面，只要求存取方法的開發者實作特定資料型別專屬的方法。SP-GiST 核心負責有效率的磁碟對應以及樹狀結構的搜尋。它也會處理並行與日誌記錄方面的考量。

SP-GiST 樹的葉 tuple 通常包含與被索引欄位相同資料型別的值，不過它們也可以包含被索引欄位的有損表示。儲存在根層級的葉 tuple 會直接代表原始的被索引資料值，但較低層級的葉 tuple 可能只包含部分值，例如後綴。在這種情況下，運算子類別的支援函式必須能夠利用到達葉層級途中所經過之內部 tuple 累積的資訊，重建原始值。

使用 `INCLUDE` 欄位建立 SP-GiST 索引時，這些欄位的值也會儲存在葉 tuple 中。`INCLUDE` 欄位與 SP-GiST 運算子類別無關，因此這裡不再進一步討論。

內部 tuple 較為複雜，因為它們是搜尋樹中的分支點。每個內部 tuple 包含一組一個或多個*節點*，代表相似葉值的群組。節點包含一個下行連結（downlink），它要麼通往另一個較低層級的內部 tuple，要麼通往一份全部位於同一索引頁面上的葉 tuple 短清單。每個節點通常有一個描述它的*標籤*；例如，在基數樹中，節點標籤可以是字串值的下一個字元。（另外，如果運算子類別對所有內部 tuple 都使用一組固定的節點，則可以省略節點標籤；請參閱[第 65.3.4.2 節](spgist.md#SPGIST-NULL-LABELS)。）內部 tuple 可以選擇性地具有描述其所有成員的*前綴*值。在基數樹中，這可以是所代表字串的共同前綴。前綴值不一定真的是前綴，而可以是運算子類別所需的任何資料；例如，在四元樹中，它可以儲存作為四個象限劃分基準的中心點。如此一來，四元樹的內部 tuple 也會包含四個節點，分別對應這個中心點周圍的各個象限。

有些樹演算法需要知道目前 tuple 的層級（或深度），因此 SP-GiST 核心讓運算子類別可以在沿樹往下走訪時管理層級計數。它也支援在需要時逐步重建所代表的值，以及在沿樹往下走訪期間向下傳遞額外資料（稱為*遍歷值*，traverse values）。

### 注意

SP-GiST 核心程式碼會處理 null 項目。雖然 SP-GiST 索引確實會為被索引欄位中的 null 儲存項目，但這對索引運算子類別的程式碼是隱藏的：永遠不會有 null 索引項目或搜尋條件傳給運算子類別的方法。（這是假設 SP-GiST 運算子是嚴格的，因此對 null 值不可能成功。）因此這裡不再進一步討論 null 值。

SP-GiST 的索引運算子類別必須提供五個使用者定義的方法，另有兩個是選擇性的。這五個必要方法都遵循接受兩個 `internal` 引數的慣例，第一個引數是指向 C 結構的指標，該結構包含支援方法的輸入值；第二個引數則是指向 C 結構的指標，輸出值必須放在該結構中。其中四個必要方法只傳回 `void`，因為它們的所有結果都出現在輸出結構中；但 `leaf_consistent` 傳回 `boolean` 結果。這些方法不得修改其輸入結構的任何欄位。在所有情況下，輸出結構都會在呼叫使用者定義的方法之前初始化為零。選擇性的第六個方法 `compress` 接受要被索引的 `datum` 作為唯一引數，並傳回適合實體儲存在葉 tuple 中的值。選擇性的第七個方法 `options` 接受一個指向 C 結構的 `internal` 指標，運算子類別專屬的參數應該放在該結構中，並傳回 `void`。

五個必要的使用者定義方法如下：

`config`
:   傳回索引實作的靜態資訊，包括前綴與節點標籤資料型別的資料型別 OID。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE FUNCTION my_config(internal, internal) RETURNS void ...
    ```

    第一個引數是指向 `spgConfigIn` C 結構的指標，其中包含函式的輸入資料。第二個引數是指向 `spgConfigOut` C 結構的指標，函式必須在其中填入結果資料。

    ```

    typedef struct spgConfigIn
    {
        Oid         attType;        /* Data type to be indexed */
    } spgConfigIn;

    typedef struct spgConfigOut
    {
        Oid         prefixType;     /* Data type of inner-tuple prefixes */
        Oid         labelType;      /* Data type of inner-tuple node labels */
        Oid         leafType;       /* Data type of leaf-tuple values */
        bool        canReturnData;  /* Opclass can reconstruct original data */
        bool        longValuesOK;   /* Opclass can cope with values > 1 page */
    } spgConfigOut;
    ```

    傳入 `attType` 是為了支援多型的索引運算子類別；對於一般固定資料型別的運算子類別，它的值永遠相同，因此可以忽略。

    對於不使用前綴的運算子類別，可以將 `prefixType` 設為 `VOIDOID`。同樣地，對於不使用節點標籤的運算子類別，可以將 `labelType` 設為 `VOIDOID`。如果運算子類別能夠重建原本提供的索引值，應該將 `canReturnData` 設為 true。只有在 `attType` 為可變長度，且運算子類別能夠透過反覆取後綴來分段處理長值時（也就是每往下一層就移除一段前綴、只保留較短的後綴，與下方 picksplit 去除前綴的做法一致），才應該將 `longValuesOK` 設為 true（請參閱[第 65.3.4.1 節](spgist.md#SPGIST-LIMITS)）。

    `leafType` 應該與運算子類別的 `opckeytype` 系統目錄項目所定義的索引儲存型別相符。（請注意，`opckeytype` 可以是零，表示儲存型別與運算子類別的輸入型別相同，這是最常見的情況。）基於向後相容性的理由，`config` 方法可以將 `leafType` 設為其他值，而該值會被使用；但這種做法已被棄用，因為如此一來索引內容在系統目錄中會被錯誤識別。此外，也允許讓 `leafType` 保持未初始化（零）；這會被解讀為使用從 `opckeytype` 推導出的索引儲存型別。

    當 `attType` 與 `leafType` 不同時，必須提供選擇性的 `compress` 方法。`compress` 方法負責將要被索引的 datum 從 `attType` 轉換為 `leafType`。

`choose`
:   選擇將新值插入內部 tuple 的方式。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE FUNCTION my_choose(internal, internal) RETURNS void ...
    ```

    第一個引數是指向 `spgChooseIn` C 結構的指標，其中包含函式的輸入資料。第二個引數是指向 `spgChooseOut` C 結構的指標，函式必須在其中填入結果資料。

    ```

    typedef struct spgChooseIn
    {
        Datum       datum;          /* original datum to be indexed */
        Datum       leafDatum;      /* current datum to be stored at leaf */
        int         level;          /* current level (counting from zero) */

        /* Data from current inner tuple */
        bool        allTheSame;     /* tuple is marked all-the-same? */
        bool        hasPrefix;      /* tuple has a prefix? */
        Datum       prefixDatum;    /* if so, the prefix value */
        int         nNodes;         /* number of nodes in the inner tuple */
        Datum      *nodeLabels;     /* node label values (NULL if none) */
    } spgChooseIn;

    typedef enum spgChooseResultType
    {
        spgMatchNode = 1,           /* descend into existing node */
        spgAddNode,                 /* add a node to the inner tuple */
        spgSplitTuple               /* split inner tuple (change its prefix) */
    } spgChooseResultType;

    typedef struct spgChooseOut
    {
        spgChooseResultType resultType;     /* action code, see above */
        union
        {
            struct                  /* results for spgMatchNode */
            {
                int         nodeN;      /* descend to this node (index from 0) */
                int         levelAdd;   /* increment level by this much */
                Datum       restDatum;  /* new leaf datum */
            }           matchNode;
            struct                  /* results for spgAddNode */
            {
                Datum       nodeLabel;  /* new node's label */
                int         nodeN;      /* where to insert it (index from 0) */
            }           addNode;
            struct                  /* results for spgSplitTuple */
            {
                /* Info to form new upper-level inner tuple with one child tuple */
                bool        prefixHasPrefix;    /* tuple should have a prefix? */
                Datum       prefixPrefixDatum;  /* if so, its value */
                int         prefixNNodes;       /* number of nodes */
                Datum      *prefixNodeLabels;   /* their labels (or NULL for
                                                 * no labels) */
                int         childNodeN;         /* which node gets child tuple */

                /* Info to form new lower-level inner tuple with all old nodes */
                bool        postfixHasPrefix;   /* tuple should have a prefix? */
                Datum       postfixPrefixDatum; /* if so, its value */
            }           splitTuple;
        }           result;
    } spgChooseOut;
    ```

    `datum` 是要插入索引的原始 datum，型別為 `spgConfigIn`.`attType`。`leafDatum` 是型別為 `spgConfigOut`.`leafType` 的值，當有提供 `compress` 方法時，它最初是將 `compress` 方法套用於 `datum` 的結果，否則就是與 `datum` 相同的值。如果 `choose` 或 `picksplit` 方法改變了 `leafDatum`，它可能會在樹的較低層級改變。當插入搜尋到達葉頁面時，`leafDatum` 的目前值就是要儲存在新建立之葉 tuple 中的值。`level` 是目前內部 tuple 的層級，根層級從零開始。如果目前內部 tuple 被標記為包含多個等價節點，`allTheSame` 為 true（請參閱[第 65.3.4.3 節](spgist.md#SPGIST-ALL-THE-SAME)）。如果目前內部 tuple 包含前綴，`hasPrefix` 為 true；此時 `prefixDatum` 就是前綴的值。`nNodes` 是內部 tuple 所包含的子節點數量，`nodeLabels` 則是它們的標籤值陣列，若沒有標籤則為 NULL。

    `choose` 函式可以判定新值與現有的某個子節點相符，或必須新增一個子節點，或新值與 tuple 前綴不一致，因而必須分裂內部 tuple，以建立限制較寬鬆的前綴。

    如果新值與現有的某個子節點相符，請將 `resultType` 設為 `spgMatchNode`。將 `nodeN` 設為該節點在節點陣列中的索引（從零起算）。將 `levelAdd` 設為經由該節點往下走訪所造成的 `level` 增量；如果運算子類別不使用層級，則保持為零。如果運算子類別不會在層級之間修改 datum，請將 `restDatum` 設為等於 `leafDatum`，否則將它設為修改後的值，作為下一層級的 `leafDatum`。

    如果必須新增子節點，請將 `resultType` 設為 `spgAddNode`。將 `nodeLabel` 設為新節點要使用的標籤，並將 `nodeN` 設為在節點陣列中插入該節點的索引（從零起算）。新增節點之後，會以修改後的內部 tuple 再次呼叫 `choose` 函式；該次呼叫應該產生 `spgMatchNode` 結果。

    如果新值與 tuple 前綴不一致，請將 `resultType` 設為 `spgSplitTuple`。此動作會將所有現有節點移到一個新的較低層級內部 tuple 中，並以一個只有單一下行連結、指向該新的較低層級內部 tuple 的 tuple 取代現有的內部 tuple。設定 `prefixHasPrefix` 以表示新的上層 tuple 是否應該有前綴，若是，則將 `prefixPrefixDatum` 設為前綴值。這個新的前綴值必須比原本的前綴寬鬆到足以接受要被索引的新值。將 `prefixNNodes` 設為新 tuple 所需的節點數量，並將 `prefixNodeLabels` 設為一個以 palloc 配置、存放這些節點標籤的陣列，若不需要節點標籤則設為 NULL。請注意，新上層 tuple 的總大小不得超過它所取代之 tuple 的總大小；這限制了新前綴與新標籤的長度。將 `childNodeN` 設為將以下行連結指向新的較低層級內部 tuple 之節點的索引（從零起算）。設定 `postfixHasPrefix` 以表示新的較低層級內部 tuple 是否應該有前綴，若是，則將 `postfixPrefixDatum` 設為前綴值。這兩個前綴與下行連結節點的標籤（若有的話）的組合，必須與原本的前綴具有相同的意義，因為既沒有機會變更被移到新的較低層級 tuple 中的節點標籤，也無法變更任何子索引項目。節點分裂之後，會以取代後的內部 tuple 再次呼叫 `choose` 函式。如果 `spgSplitTuple` 動作沒有建立合適的節點，該次呼叫可能會傳回 `spgAddNode` 結果。最終 `choose` 必須傳回 `spgMatchNode`，讓插入作業得以往下走訪到下一層級。

`picksplit`
:   決定如何在一組葉 tuple 之上建立新的內部 tuple。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE FUNCTION my_picksplit(internal, internal) RETURNS void ...
    ```

    第一個引數是指向 `spgPickSplitIn` C 結構的指標，其中包含函式的輸入資料。第二個引數是指向 `spgPickSplitOut` C 結構的指標，函式必須在其中填入結果資料。

    ```

    typedef struct spgPickSplitIn
    {
        int         nTuples;        /* number of leaf tuples */
        Datum      *datums;         /* their datums (array of length nTuples) */
        int         level;          /* current level (counting from zero) */
    } spgPickSplitIn;

    typedef struct spgPickSplitOut
    {
        bool        hasPrefix;      /* new inner tuple should have a prefix? */
        Datum       prefixDatum;    /* if so, its value */

        int         nNodes;         /* number of nodes for new inner tuple */
        Datum      *nodeLabels;     /* their labels (or NULL for no labels) */

        int        *mapTuplesToNodes;   /* node index for each leaf tuple */
        Datum      *leafTupleDatums;    /* datum to store in each new leaf tuple */
    } spgPickSplitOut;
    ```

    `nTuples` 是所提供的葉 tuple 數量。`datums` 是它們的 datum 值陣列，型別為 `spgConfigOut`.`leafType`。`level` 是所有葉 tuple 共同的目前層級，它將成為新內部 tuple 的層級。

    設定 `hasPrefix` 以表示新的內部 tuple 是否應該有前綴，若是，則將 `prefixDatum` 設為前綴值。設定 `nNodes` 以表示新內部 tuple 將包含的節點數量，並將 `nodeLabels` 設為它們的標籤值陣列，若不需要節點標籤則設為 NULL。將 `mapTuplesToNodes` 設為一個陣列，提供每個葉 tuple 應指派到之節點的索引（從零起算）。將 `leafTupleDatums` 設為要儲存在新葉 tuple 中的值陣列（如果運算子類別不會在層級之間修改 datum，這些值會與輸入的 `datums` 相同）。請注意，`picksplit` 函式負責以 palloc 配置 `nodeLabels`、`mapTuplesToNodes` 與 `leafTupleDatums` 陣列。

    如果提供了超過一個葉 tuple，則預期 `picksplit` 函式會將它們分類到超過一個節點中；否則就無法將葉 tuple 分散到多個頁面，而這正是此操作的最終目的。因此，如果 `picksplit` 函式最後將所有葉 tuple 都放在同一個節點中，SP-GiST 核心程式碼會推翻該決定，並產生一個內部 tuple，其中的葉 tuple 會被隨機指派到數個標籤相同的節點。這樣的 tuple 會被標記為 `allTheSame`，以表示發生了這種情況。`choose` 與 `inner_consistent` 函式必須適當地處理這類內部 tuple。詳細資訊請參閱[第 65.3.4.3 節](spgist.md#SPGIST-ALL-THE-SAME)。

    只有在 `config` 函式將 `longValuesOK` 設為 true，且提供了大於一個頁面的輸入值時，`picksplit` 才可以套用於單一葉 tuple。在這種情況下，此操作的目的是去除一個前綴，產生一個新的、較短的葉 datum 值。此呼叫會反覆進行，直到產生出短到足以放進一個頁面的葉 datum 為止。詳細資訊請參閱[第 65.3.4.1 節](spgist.md#SPGIST-LIMITS)。

`inner_consistent`
:   傳回在樹搜尋期間要跟隨的節點（分支）集合。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE FUNCTION my_inner_consistent(internal, internal) RETURNS void ...
    ```

    第一個引數是指向 `spgInnerConsistentIn` C 結構的指標，其中包含函式的輸入資料。第二個引數是指向 `spgInnerConsistentOut` C 結構的指標，函式必須在其中填入結果資料。

    ```

    typedef struct spgInnerConsistentIn
    {
        ScanKey     scankeys;       /* array of operators and comparison values */
        ScanKey     orderbys;       /* array of ordering operators and comparison
                                     * values */
        int         nkeys;          /* length of scankeys array */
        int         norderbys;      /* length of orderbys array */

        Datum       reconstructedValue;     /* value reconstructed at parent */
        void       *traversalValue; /* opclass-specific traverse value */
        MemoryContext traversalMemoryContext;   /* put new traverse values here */
        int         level;          /* current level (counting from zero) */
        bool        returnData;     /* original data must be returned? */

        /* Data from current inner tuple */
        bool        allTheSame;     /* tuple is marked all-the-same? */
        bool        hasPrefix;      /* tuple has a prefix? */
        Datum       prefixDatum;    /* if so, the prefix value */
        int         nNodes;         /* number of nodes in the inner tuple */
        Datum      *nodeLabels;     /* node label values (NULL if none) */
    } spgInnerConsistentIn;

    typedef struct spgInnerConsistentOut
    {
        int         nNodes;         /* number of child nodes to be visited */
        int        *nodeNumbers;    /* their indexes in the node array */
        int        *levelAdds;      /* increment level by this much for each */
        Datum      *reconstructedValues;    /* associated reconstructed values */
        void      **traversalValues;        /* opclass-specific traverse values */
        double    **distances;              /* associated distances */
    } spgInnerConsistentOut;
    ```

    長度為 `nkeys` 的 `scankeys` 陣列描述索引搜尋條件。這些條件以 AND 結合——只有滿足所有條件的索引項目才是我們感興趣的。（請注意，`nkeys` = 0 表示所有索引項目都滿足查詢。）consistent 函式通常只關心每個陣列項目的 `sk_strategy` 與 `sk_argument` 欄位，它們分別提供可索引運算子與比較值。特別是，不需要檢查 `sk_flags` 來確認比較值是否為 NULL，因為 SP-GiST 核心程式碼會濾除這類條件。長度為 `norderbys` 的 `orderbys` 陣列以相同的方式描述排序運算子（若有的話）。`reconstructedValue` 是為父 tuple 重建的值；在根層級，或 `inner_consistent` 函式未在父層級提供值時，它為 `(Datum) 0`。`traversalValue` 是一個指標，指向前一次對父索引 tuple 呼叫 `inner_consistent` 時向下傳遞的任何遍歷資料，在根層級則為 NULL。`traversalMemoryContext` 是用來儲存輸出遍歷值的記憶體上下文（見下文）。`level` 是目前內部 tuple 的層級，根層級從零開始。如果此查詢需要重建資料，`returnData` 為 `true`；只有在 `config` 函式宣告了 `canReturnData` 時才會如此。如果目前內部 tuple 被標記為「all-the-same」，`allTheSame` 為 true；在這種情況下，所有節點都具有相同的標籤（若有的話），因此要麼全部與查詢相符，要麼全部不相符（請參閱[第 65.3.4.3 節](spgist.md#SPGIST-ALL-THE-SAME)）。如果目前內部 tuple 包含前綴，`hasPrefix` 為 true；此時 `prefixDatum` 就是前綴的值。`nNodes` 是內部 tuple 所包含的子節點數量，`nodeLabels` 則是它們的標籤值陣列，若節點沒有標籤則為 NULL。

    `nNodes` 必須設為搜尋需要造訪的子節點數量，而 `nodeNumbers` 必須設為它們的索引陣列。如果運算子類別會追蹤層級，請將 `levelAdds` 設為往下走訪到每個要造訪之節點時所需的層級增量陣列。（這些增量通常對所有節點都相同，但不一定如此，因此使用陣列。）如果需要重建值，請將 `reconstructedValues` 設為為每個要造訪之子節點所重建的值陣列；否則將 `reconstructedValues` 保持為 NULL。重建的值假設為 `spgConfigOut`.`leafType` 型別。（不過，由於核心系統除了可能複製它們之外，不會對它們做任何處理，因此只要它們具有與 `leafType` 相同的 `typlen` 與 `typbyval` 屬性就足夠了。）如果執行的是有序搜尋，請依照 `orderbys` 陣列將 `distances` 設為距離值陣列（距離最小的節點會最先處理）；否則將它保持為 NULL。如果想要將額外的頻外資訊（「遍歷值」）向下傳遞到樹搜尋的較低層級，請將 `traversalValues` 設為適當遍歷值的陣列，每個要造訪的子節點各一個；否則將 `traversalValues` 保持為 NULL。請注意，`inner_consistent` 函式負責在目前的記憶體上下文 中以 palloc 配置 `nodeNumbers`、`levelAdds`、`distances`、`reconstructedValues` 與 `traversalValues` 陣列。不過，`traversalValues` 陣列所指向的任何輸出遍歷值，都應該配置在 `traversalMemoryContext` 中。每個遍歷值都必須是單一的 palloc 配置區塊。

`leaf_consistent`
:   如果葉 tuple 滿足查詢，則傳回 true。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE FUNCTION my_leaf_consistent(internal, internal) RETURNS bool ...
    ```

    第一個引數是指向 `spgLeafConsistentIn` C 結構的指標，其中包含函式的輸入資料。第二個引數是指向 `spgLeafConsistentOut` C 結構的指標，函式必須在其中填入結果資料。

    ```

    typedef struct spgLeafConsistentIn
    {
        ScanKey     scankeys;       /* array of operators and comparison values */
        ScanKey     orderbys;       /* array of ordering operators and comparison
                                     * values */
        int         nkeys;          /* length of scankeys array */
        int         norderbys;      /* length of orderbys array */

        Datum       reconstructedValue;     /* value reconstructed at parent */
        void       *traversalValue; /* opclass-specific traverse value */
        int         level;          /* current level (counting from zero) */
        bool        returnData;     /* original data must be returned? */

        Datum       leafDatum;      /* datum in leaf tuple */
    } spgLeafConsistentIn;

    typedef struct spgLeafConsistentOut
    {
        Datum       leafValue;        /* reconstructed original data, if any */
        bool        recheck;          /* set true if operator must be rechecked */
        bool        recheckDistances; /* set true if distances must be rechecked */
        double     *distances;        /* associated distances */
    } spgLeafConsistentOut;
    ```

    長度為 `nkeys` 的 `scankeys` 陣列描述索引搜尋條件。這些條件以 AND 結合——只有滿足所有條件的索引項目才滿足查詢。（請注意，`nkeys` = 0 表示所有索引項目都滿足查詢。）consistent 函式通常只關心每個陣列項目的 `sk_strategy` 與 `sk_argument` 欄位，它們分別提供可索引運算子與比較值。特別是，不需要檢查 `sk_flags` 來確認比較值是否為 NULL，因為 SP-GiST 核心程式碼會濾除這類條件。長度為 `norderbys` 的 `orderbys` 陣列以相同的方式描述排序運算子。`reconstructedValue` 是為父 tuple 重建的值；在根層級，或 `inner_consistent` 函式未在父層級提供值時，它為 `(Datum) 0`。`traversalValue` 是一個指標，指向前一次對父索引 tuple 呼叫 `inner_consistent` 時向下傳遞的任何遍歷資料，在根層級則為 NULL。`level` 是目前葉 tuple 的層級，根層級從零開始。如果此查詢需要重建資料，`returnData` 為 `true`；只有在 `config` 函式宣告了 `canReturnData` 時才會如此。`leafDatum` 是儲存在目前葉 tuple 中、型別為 `spgConfigOut`.`leafType` 的鍵值。

    如果葉 tuple 與查詢相符，函式必須傳回 `true`，否則傳回 `false`。在 `true` 的情況下，如果 `returnData` 為 `true`，則必須將 `leafValue` 設為原本為此葉 tuple 提供以供索引的值（型別為 `spgConfigIn`.`attType`）。此外，如果是否相符並不確定，因而必須對實際的堆積 tuple 重新套用運算子以驗證是否相符，則可以將 `recheck` 設為 `true`。如果執行的是有序搜尋，請依照 `orderbys` 陣列將 `distances` 設為距離值陣列；否則將它保持為 NULL。如果傳回的距離中至少有一個不精確，請將 `recheckDistances` 設為 true。在這種情況下，執行器會在從堆積擷取 tuple 之後計算精確的距離，並在需要時重新排序這些 tuple。

選擇性的使用者定義方法如下：

`Datum compress(Datum in)`
:   將資料項目轉換為適合實體儲存在索引葉 tuple 中的格式。它接受型別為 `spgConfigIn`.`attType` 的值，並傳回型別為 `spgConfigOut`.`leafType` 的值。輸出值不得包含行外（out-of-line）TOAST 指標。

    注意：`compress` 方法只會套用於要儲存的值。consistent 方法收到的查詢 `scankeys` 保持不變，不會使用 `compress` 進行轉換。

`options`
:   定義一組使用者可見的參數，用以控制運算子類別的行為。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_options(internal)
    RETURNS void
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    此函式會收到一個指向 `local_relopts` 結構的指標，該結構需要填入一組運算子類別專屬的選項。其他支援函式可以使用 `PG_HAS_OPCLASS_OPTIONS()` 與 `PG_GET_OPCLASS_OPTIONS()` 巨集存取這些選項。

    由於鍵在 SP-GiST 中的表示方式具有彈性，它可能取決於使用者指定的參數。

所有 SP-GiST 支援方法通常都在短期存在的記憶體上下文 中呼叫；也就是說，每處理完一個 tuple，`CurrentMemoryContext` 就會被重設。因此，不太需要擔心是否以 pfree 釋放了所有以 palloc 配置的記憶體。（`config` 方法是例外：它應該盡量避免記憶體洩漏。但 `config` 方法通常只需要將常數指派給傳入的參數結構，不必做其他事。）

如果被索引的欄位屬於可定序的資料型別，索引的定序會透過標準的 `PG_GET_COLLATION()` 機制傳給所有支援方法。

<a id="SPGIST-IMPLEMENTATION"></a>

### 65.3.4. 實作 [#](#SPGIST-IMPLEMENTATION)

本節說明實作細節，以及其他對 SP-GiST 運算子類別實作者而言值得了解的技巧。

<a id="SPGIST-LIMITS"></a>

#### 65.3.4.1. SP-GiST 的限制 [#](#SPGIST-LIMITS)

個別的葉 tuple 與內部 tuple 都必須能放進單一索引頁面（預設為 8kB）。因此，在為可變長度資料型別的值建立索引時，只有像基數樹這類方法才能支援長值；在這類方法中，樹的每一層都包含一個短到足以放進一個頁面的前綴，而最終的葉層級則包含一個同樣短到足以放進一個頁面的後綴。只有在運算子類別已準備好做到這一點時，才應該將 `longValuesOK` 設為 true。否則，SP-GiST 核心會拒絕任何要為大到無法放進索引頁面之值建立索引的請求。

同樣地，確保內部 tuple 不會大到無法放進索引頁面，是運算子類別的責任；這限制了單一內部 tuple 中可使用的子節點數量，以及前綴值的最大大小。

另一個限制是，當內部 tuple 的節點指向一組葉 tuple 時，這些 tuple 必須全部位於同一個索引頁面中。（這是一項設計決策，目的是減少磁碟尋軌，並節省將這類 tuple 串連在一起之連結所需的空間。）如果這組葉 tuple 變得太大而無法放進一個頁面，就會執行分裂，並插入一個中間的內部 tuple。為了讓這樣做能解決問題，新的內部 tuple *必須*將這組葉值劃分到超過一個節點群組中。如果運算子類別的 `picksplit` 函式無法做到這一點，SP-GiST 核心會採取[第 65.3.4.3 節](spgist.md#SPGIST-ALL-THE-SAME)所述的特殊措施。

當 `longValuesOK` 為 true 時，預期 SP-GiST 樹的後續各層會將越來越多的資訊吸收到內部 tuple 的前綴與節點標籤中，使所需的葉 datum 越來越小，最終能夠放進一個頁面。為了防止運算子類別中的錯誤導致無限的插入迴圈，如果葉 datum 在十個 `choose` 方法呼叫週期內都沒有變得更小，SP-GiST 核心就會引發錯誤。

<a id="SPGIST-NULL-LABELS"></a>

#### 65.3.4.2. 沒有節點標籤的 SP-GiST [#](#SPGIST-NULL-LABELS)

有些樹演算法對每個內部 tuple 使用一組固定的節點；例如，在四元樹中，永遠恰好有四個節點，對應於內部 tuple 中心點周圍的四個象限。在這種情況下，程式碼通常以編號來處理節點，不需要明確的節點標籤。若要省略節點標籤（藉此節省一些空間），`picksplit` 函式可以對 `nodeLabels` 陣列傳回 NULL，同樣地，`choose` 函式在 `spgSplitTuple` 動作期間也可以對 `prefixNodeLabels` 陣列傳回 NULL。這接著會使 `nodeLabels` 在後續呼叫 `choose` 與 `inner_consistent` 時為 NULL。原則上，在同一個索引中，可以對某些內部 tuple 使用節點標籤，而對其他內部 tuple 省略節點標籤。

處理具有未加標籤節點的內部 tuple 時，`choose` 傳回 `spgAddNode` 是一種錯誤，因為在這種情況下，節點集合應該是固定的。

<a id="SPGIST-ALL-THE-SAME"></a>

#### 65.3.4.3. 「全部相同」（All-the-Same）的內部元組 [#](#SPGIST-ALL-THE-SAME)

當 `picksplit` 無法將所提供的葉值劃分到至少兩個節點類別中時，SP-GiST 核心可以推翻運算子類別之 `picksplit` 函式的結果。發生這種情況時，新的內部 tuple 會以多個節點建立，每個節點都具有與 `picksplit` 為它實際使用的那一個節點所指定的相同標籤（若有的話），而葉值會被隨機分配到這些等價的節點中。內部 tuple 上會設定 `allTheSame` 旗標，以警告 `choose` 與 `inner_consistent` 函式：該 tuple 不具有它們原本可能預期的節點集合。

處理 `allTheSame` tuple 時，`choose` 的 `spgMatchNode` 結果會被解讀為新值可以指派給任何一個等價節點；核心程式碼會忽略所提供的 `nodeN` 值，並隨機往下走訪到其中一個節點（以保持樹的平衡）。`choose` 傳回 `spgAddNode` 是一種錯誤，因為那會使節點不再全部等價；如果要插入的值與現有節點不相符，必須使用 `spgSplitTuple` 動作。

處理 `allTheSame` tuple 時，`inner_consistent` 函式應該將所有節點都傳回，或一個都不傳回，作為繼續索引搜尋的目標，因為它們全都是等價的。這可能需要、也可能不需要任何特殊情況的程式碼，取決於 `inner_consistent` 函式通常對節點的意義做了多少假設。

<a id="SPGIST-EXAMPLES"></a>

### 65.3.5. 範例 [#](#SPGIST-EXAMPLES)

PostgreSQL 原始碼發行版本包含數個 SP-GiST 索引運算子類別的範例，如[表 65.2](spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE) 所述。程式碼請參閱 `src/backend/access/spgist/` 與 `src/backend/utils/adt/`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spgist.html)（原文版本：18.6；核對日期：2026-10-17）
