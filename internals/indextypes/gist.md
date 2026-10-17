<a id="GIST"></a>

## 65.2. GiST 索引 [#](#GIST)

[65.2.1. 簡介](gist.md#GIST-INTRO)

[65.2.2. 內建運算子類別](gist.md#GIST-BUILTIN-OPCLASSES)

[65.2.3. 擴充性](gist.md#GIST-EXTENSIBILITY)

[65.2.4. 實作](gist.md#GIST-IMPLEMENTATION)

[65.2.5. 範例](gist.md#GIST-EXAMPLES)

<a id="id-1.10.17.3.2"></a>

<a id="GIST-INTRO"></a>

### 65.2.1. 簡介 [#](#GIST-INTRO)

GiST 代表通用搜尋樹（Generalized Search Tree）。它是一種平衡的樹狀結構存取方法，作為實作任意索引機制的基礎範本。B-tree、R-tree 以及許多其他索引機制都可以在 GiST 中實作。

GiST 的一項優點是，它讓具備適當存取方法的自訂資料型別，可以由該資料型別領域的專家來開發，而不必由資料庫專家來開發。

此處的部分資訊取自加州大學柏克萊分校 GiST 索引專案的[網站](http://gist.cs.berkeley.edu/)，以及 Marcel Kornacker 的論文「[Access Methods for Next-Generation Database Systems](http://www.sai.msu.su/~megera/postgres/gist/papers/concurrency/access-methods-for-next-generation.pdf.gz)」。PostgreSQL 中的 GiST 實作主要由 Teodor Sigaev 與 Oleg Bartunov 維護，更多資訊請見他們的[網站](http://www.sai.msu.su/~megera/postgres/gist/)。

<a id="GIST-BUILTIN-OPCLASSES"></a>

### 65.2.2. 內建運算子類別 [#](#GIST-BUILTIN-OPCLASSES)

核心 PostgreSQL 發行版本包含[表 65.1](gist.md#GIST-BUILTIN-OPCLASSES-TABLE) 所列的 GiST 運算子類別。（[附錄 F](../../appendixes/contrib/README.md) 中所述的部分選用模組提供了額外的 GiST 運算子類別。）

<a id="GIST-BUILTIN-OPCLASSES-TABLE"></a>

**表 65.1. 內建 GiST 運算子類別**

<table border="1" class="table" summary="內建 GiST 運算子類別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>可索引運算子</th><th>排序運算子</th></tr></thead><tbody><tr><td rowspan="12" valign="middle"><code class="literal">box_ops</code></td><td><code class="literal">&lt;&lt; (box, box)</code></td><td rowspan="12" valign="middle"><code class="literal">&lt;-&gt; (box, point)</code></td></tr><tr><td><code class="literal">&amp;&lt; (box, box)</code></td></tr><tr><td><code class="literal">&amp;&amp; (box, box)</code></td></tr><tr><td><code class="literal">&amp;&gt; (box, box)</code></td></tr><tr><td><code class="literal">&gt;&gt; (box, box)</code></td></tr><tr><td><code class="literal">~= (box, box)</code></td></tr><tr><td><code class="literal">@&gt; (box, box)</code></td></tr><tr><td><code class="literal">&lt;@ (box, box)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (box, box)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (box, box)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (box, box)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (box, box)</code></td></tr><tr><td rowspan="12" valign="middle"><code class="literal">circle_ops</code></td><td><code class="literal">&lt;&lt; (circle, circle)</code></td><td rowspan="12" valign="middle"><code class="literal">&lt;-&gt; (circle, point)</code></td></tr><tr><td><code class="literal">&amp;&lt; (circle, circle)</code></td></tr><tr><td><code class="literal">&amp;&gt; (circle, circle)</code></td></tr><tr><td><code class="literal">&gt;&gt; (circle, circle)</code></td></tr><tr><td><code class="literal">&lt;@ (circle, circle)</code></td></tr><tr><td><code class="literal">@&gt; (circle, circle)</code></td></tr><tr><td><code class="literal">~= (circle, circle)</code></td></tr><tr><td><code class="literal">&amp;&amp; (circle, circle)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (circle, circle)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (circle, circle)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (circle, circle)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (circle, circle)</code></td></tr><tr><td rowspan="11" valign="middle"><code class="literal">inet_ops</code></td><td><code class="literal">&lt;&lt; (inet, inet)</code></td><td rowspan="11" valign="middle"> </td></tr><tr><td><code class="literal">&lt;&lt;= (inet, inet)</code></td></tr><tr><td><code class="literal">&gt;&gt; (inet, inet)</code></td></tr><tr><td><code class="literal">&gt;&gt;= (inet, inet)</code></td></tr><tr><td><code class="literal">= (inet, inet)</code></td></tr><tr><td><code class="literal">&lt;&gt; (inet, inet)</code></td></tr><tr><td><code class="literal">&lt; (inet, inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet, inet)</code></td></tr><tr><td><code class="literal">&gt; (inet, inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet, inet)</code></td></tr><tr><td><code class="literal">&amp;&amp; (inet, inet)</code></td></tr><tr><td rowspan="18" valign="middle"><code class="literal">multirange_ops</code></td><td><code class="literal">= (anymultirange, anymultirange)</code></td><td rowspan="18" valign="middle"> </td></tr><tr><td><code class="literal">&amp;&amp; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&amp;&amp; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">@&gt; (anymultirange, anyelement)</code></td></tr><tr><td><code class="literal">@&gt; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">@&gt; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">&lt;@ (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&lt;@ (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anymultirange, anyrange)</code></td></tr><tr><td><code class="literal">-|- (anymultirange, anymultirange)</code></td></tr><tr><td><code class="literal">-|- (anymultirange, anyrange)</code></td></tr><tr><td rowspan="8" valign="middle"><code class="literal">point_ops</code></td><td><code class="literal">|&gt;&gt; (point, point)</code></td><td rowspan="8" valign="middle"><code class="literal">&lt;-&gt; (point, point)</code></td></tr><tr><td><code class="literal">&lt;&lt; (point, point)</code></td></tr><tr><td><code class="literal">&gt;&gt; (point, point)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (point, point)</code></td></tr><tr><td><code class="literal">~= (point, point)</code></td></tr><tr><td><code class="literal">&lt;@ (point, box)</code></td></tr><tr><td><code class="literal">&lt;@ (point, polygon)</code></td></tr><tr><td><code class="literal">&lt;@ (point, circle)</code></td></tr><tr><td rowspan="12" valign="middle"><code class="literal">poly_ops</code></td><td><code class="literal">&lt;&lt; (polygon, polygon)</code></td><td rowspan="12" valign="middle"><code class="literal">&lt;-&gt; (polygon, point)</code></td></tr><tr><td><code class="literal">&amp;&lt; (polygon, polygon)</code></td></tr><tr><td><code class="literal">&amp;&gt; (polygon, polygon)</code></td></tr><tr><td><code class="literal">&gt;&gt; (polygon, polygon)</code></td></tr><tr><td><code class="literal">&lt;@ (polygon, polygon)</code></td></tr><tr><td><code class="literal">@&gt; (polygon, polygon)</code></td></tr><tr><td><code class="literal">~= (polygon, polygon)</code></td></tr><tr><td><code class="literal">&amp;&amp; (polygon, polygon)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (polygon, polygon)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (polygon, polygon)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (polygon, polygon)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (polygon, polygon)</code></td></tr><tr><td rowspan="18" valign="middle"><code class="literal">range_ops</code></td><td><code class="literal">= (anyrange, anyrange)</code></td><td rowspan="18" valign="middle"> </td></tr><tr><td><code class="literal">&amp;&amp; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&amp;&amp; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange, anyelement)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">&lt;@ (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&lt;@ (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anyrange, anymultirange)</code></td></tr><tr><td><code class="literal">-|- (anyrange, anyrange)</code></td></tr><tr><td><code class="literal">-|- (anyrange, anymultirange)</code></td></tr><tr><td rowspan="2" valign="middle"><code class="literal">tsquery_ops</code></td><td><code class="literal">&lt;@ (tsquery, tsquery)</code></td><td rowspan="2" valign="middle"> </td></tr><tr><td><code class="literal">@&gt; (tsquery, tsquery)</code></td></tr><tr><td valign="middle"><code class="literal">tsvector_ops</code></td><td><code class="literal">@@ (tsvector, tsquery)</code></td><td> </td></tr></tbody></table>

<br>

由於歷史因素，`inet_ops` 運算子類別並不是 `inet` 與 `cidr` 型別的預設類別。若要使用它，請在 `CREATE INDEX` 中指明該類別名稱，例如

```

CREATE INDEX ON my_table USING GIST (my_inet_column inet_ops);
```

<a id="GIST-EXTENSIBILITY"></a>

### 65.2.3. 擴充性 [#](#GIST-EXTENSIBILITY)

傳統上，實作新的索引存取方法意味著大量困難的工作。必須了解資料庫的內部運作，例如鎖定管理器與預寫式日誌（Write-Ahead Log）。GiST 介面具有高度抽象性，只要求存取方法實作者實作被存取資料型別的語意。GiST 層本身會處理並行、日誌記錄以及樹狀結構的搜尋。

不應將這種擴充性，與其他標準搜尋樹在可處理之資料方面的擴充性混為一談。例如，PostgreSQL 支援可擴充的 B-tree 與雜湊索引。這表示你可以使用 PostgreSQL 在任何想要的資料型別上建立 B-tree 或雜湊索引。但 B-tree 只支援範圍謂詞（`<`、`=`、`>`），而雜湊索引只支援相等查詢。

因此，如果你用 PostgreSQL 的 B-tree 為一組影像集合建立索引，你只能發出像「imagex 是否等於 imagey」、「imagex 是否小於 imagey」以及「imagex 是否大於 imagey」這類查詢。視你在此情境下如何定義「等於」、「小於」與「大於」而定，這可能會有用處。然而，透過使用以 GiST 為基礎的索引，你可以建立提出領域特定問題的方式，例如「找出所有馬的影像」或「找出所有過度曝光的影像」。

要讓 GiST 存取方法開始運作，只需要實作幾個使用者自訂的方法，這些方法定義了樹中鍵值的行為。當然，要支援花俏的查詢，這些方法也必須相當花俏；但對於所有標準查詢（B-tree、R-tree 等）而言，它們相對簡單。簡而言之，GiST 結合了擴充性、通用性、程式碼重複使用以及清晰的介面。

GiST 的索引運算子類別必須提供五個方法，另有七個是選用的。索引的正確性由 `same`、`consistent` 與 `union` 方法的正確實作來確保，而索引的效率（大小與速度）則取決於 `penalty` 與 `picksplit` 方法。兩個選用方法是 `compress` 與 `decompress`，它們允許索引的內部樹狀資料使用與其所索引資料不同的型別。葉節點代表的是被索引資料型別的值，而其他樹節點則可以是任何 C 結構（但你在此仍必須遵循 PostgreSQL 的資料型別規則，關於可變長度資料請參閱 `varlena` 的說明）。（原文此處寫作「葉節點必須是被索引的資料型別」，說法過於絕對：如後文 compress 與 fetch 方法所述，葉項目實際儲存的可以是經 compress 轉換後的型別，需要時再由 fetch 還原為原始的被索引型別。）如果樹的內部資料型別存在於 SQL 層級，可以使用 `CREATE OPERATOR CLASS` 命令的 `STORAGE` 選項。選用的第八個方法是 `distance`，如果運算子類別想要支援有序掃描（最近鄰搜尋），就需要這個方法。選用的第九個方法 `fetch`，在運算子類別想要支援僅索引掃描時需要，除非省略了 `compress` 方法。選用的第十個方法 `options`，在運算子類別具有使用者指定的參數時需要。選用的第十一個方法 `sortsupport` 用來加速建立 GiST 索引。選用的第十二個方法 `stratnum`（原文此處寫作 stratnum，但本節下方的詳細說明與 FUNCTION 12 的註冊範例使用的名稱都是 translate_cmptype；PostgreSQL 18 的第十二個支援方法應為 translate_cmptype）用來將比較類型（來自 `src/include/access/cmptype.h`）轉換為運算子類別所使用的策略編號。這讓核心程式碼可以為時態限制條件索引查找運算子。

`consistent`
:   給定索引項目 `p` 與查詢值 `q`，此函式判斷該索引項目是否與查詢「一致」；也就是說，對於該索引項目所代表的任何資料列，謂詞「*`indexed_column`* *`indexable_operator`* `q`」是否可能為真？對於葉索引項目，這等同於測試可索引條件；而對於內部樹節點，這會判斷是否需要掃描該樹節點所代表的索引子樹。當結果為 `true` 時，也必須傳回一個 `recheck` 旗標。它表示該謂詞是確定為真，還是只是可能為真。如果 `recheck` = `false`，表示索引已精確地測試過謂詞條件；而如果 `recheck` = `true`，則該資料列只是候選的符合項目。在這種情況下，系統會自動對實際的資料列值計算 *`indexable_operator`*，以確認它是否真的符合。這項慣例讓 GiST 能夠同時支援無損與有損的索引結構。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_consistent(internal, data_type, smallint, oid, internal)
    RETURNS bool
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_consistent);

    Datum
    my_consistent(PG_FUNCTION_ARGS)
    {
        GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0);
        data_type  *query = PG_GETARG_DATA_TYPE_P(1);
        StrategyNumber strategy = (StrategyNumber) PG_GETARG_UINT16(2);
        /* Oid subtype = PG_GETARG_OID(3); */
        bool       *recheck = (bool *) PG_GETARG_POINTER(4);
        data_type  *key = DatumGetDataType(entry->key);
        bool        retval;

        /*
         * determine return value as a function of strategy, key and query.
         *
         * Use GIST_LEAF(entry) to know where you're called in the index tree,
         * which comes handy when supporting the = operator for example (you could
         * check for non empty union() in non-leaf nodes and equality in leaf
         * nodes).
         */

        *recheck = true;        /* or false if check is exact */

        PG_RETURN_BOOL(retval);
    }
    ```

    其中，`key` 是索引中的一個元素，而 `query` 是在索引中查找的值。`StrategyNumber` 參數表示正在套用運算子類別中的哪一個運算子——它對應 `CREATE OPERATOR CLASS` 命令中的其中一個運算子編號。

    視你在類別中納入了哪些運算子而定，`query` 的資料型別可能會隨運算子而不同，因為它會是運算子右側的任何型別，而這可能與出現在左側的被索引資料型別不同。（上述程式碼骨架假設只可能有一種型別；如果不是這樣，擷取 `query` 引數值的方式就必須取決於運算子。）建議 `consistent` 函式的 SQL 宣告對 `query` 引數使用運算子類別的被索引資料型別，即使實際的型別可能依運算子而為其他型別。

`union`
:   此方法整合樹中的資訊。給定一組項目，此函式會產生一個新的索引項目，代表所有給定的項目。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_union(internal, internal)
    RETURNS storage_type
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_union);

    Datum
    my_union(PG_FUNCTION_ARGS)
    {
        GistEntryVector *entryvec = (GistEntryVector *) PG_GETARG_POINTER(0);
        GISTENTRY  *ent = entryvec->vector;
        data_type  *out,
                   *tmp,
                   *old;
        int         numranges,
                    i = 0;

        numranges = entryvec->n;
        tmp = DatumGetDataType(ent[0].key);
        out = tmp;

        if (numranges == 1)
        {
            out = data_type_deep_copy(tmp);

            PG_RETURN_DATA_TYPE_P(out);
        }

        for (i = 1; i < numranges; i++)
        {
            old = out;
            tmp = DatumGetDataType(ent[i].key);
            out = my_union_implementation(out, tmp);
        }

        PG_RETURN_DATA_TYPE_P(out);
    }
    ```

    如你所見，在這個骨架中，我們處理的是 `union(X, Y, Z) = union(union(X, Y), Z)` 成立的資料型別。要支援此等式不成立的資料型別也很容易，只要在這個 GiST 支援方法中實作適當的聯集演算法即可。

    `union` 函式的結果必須是索引儲存型別的值，不論該型別為何（它可能與被索引欄位的型別不同，也可能相同）。`union` 函式應該傳回指向以 `palloc()` 新配置之記憶體的指標。即使型別沒有改變，也不能直接原樣傳回輸入值。

    如上所示，`union` 函式的第一個 `internal` 引數實際上是一個 `GistEntryVector` 指標。第二個引數是指向一個整數變數的指標，可以忽略。（過去曾要求 `union` 函式將其結果值的大小儲存到該變數中，但現在已不再需要。）

`compress`
:   將資料項目轉換為適合實際儲存在索引頁面中的格式。如果省略了 `compress` 方法，資料項目會不經修改地儲存在索引中。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_compress(internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_compress);

    Datum
    my_compress(PG_FUNCTION_ARGS)
    {
        GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0);
        GISTENTRY  *retval;

        if (entry->leafkey)
        {
            /* replace entry->key with a compressed version */
            compressed_data_type *compressed_data = palloc(sizeof(compressed_data_type));

            /* fill *compressed_data from entry->key ... */

            retval = palloc(sizeof(GISTENTRY));
            gistentryinit(*retval, PointerGetDatum(compressed_data),
                          entry->rel, entry->page, entry->offset, FALSE);
        }
        else
        {
            /* typically we needn't do anything with non-leaf entries */
            retval = entry;
        }

        PG_RETURN_POINTER(retval);
    }
    ```

    當然，你必須將 *`compressed_data_type`* 調整為你為了壓縮葉節點而要轉換成的特定型別。

`decompress`
:   將資料項目的儲存表示法，轉換為運算子類別中其他 GiST 方法可以操作的格式。如果省略了 `decompress` 方法，則假設其他 GiST 方法可以直接處理所儲存的資料格式。（`decompress` 不一定是 `compress` 方法的反向操作；特別是，如果 `compress` 是有損的，`decompress` 就不可能精確地重建原始資料。`decompress` 也不一定等同於 `fetch`，因為其他 GiST 方法可能不需要完整重建資料。）

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_decompress(internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_decompress);

    Datum
    my_decompress(PG_FUNCTION_ARGS)
    {
        PG_RETURN_POINTER(PG_GETARG_POINTER(0));
    }
    ```

    上述骨架適用於不需要解壓縮的情況。（不過，當然，完全省略此方法會更簡單，在這種情況下也建議這麼做。）

`penalty`
:   傳回一個值，表示將新項目插入樹中特定分支的「成本」。項目會沿著樹中 `penalty` 最小的路徑往下插入。`penalty` 所傳回的值應該是非負數。如果傳回負值，會被視為零。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_penalty(internal, internal, internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;  -- in some cases penalty functions need not be strict
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_penalty);

    Datum
    my_penalty(PG_FUNCTION_ARGS)
    {
        GISTENTRY  *origentry = (GISTENTRY *) PG_GETARG_POINTER(0);
        GISTENTRY  *newentry = (GISTENTRY *) PG_GETARG_POINTER(1);
        float      *penalty = (float *) PG_GETARG_POINTER(2);
        data_type  *orig = DatumGetDataType(origentry->key);
        data_type  *new = DatumGetDataType(newentry->key);

        *penalty = my_penalty_implementation(orig, new);
        PG_RETURN_POINTER(penalty);
    }
    ```

    由於歷史因素，`penalty` 函式並不只是傳回一個 `float` 結果；而是必須將該值儲存在第三個引數所指示的位置。傳回值本身會被忽略，不過慣例上會傳回該引數的位址。

    `penalty` 函式對索引的良好效能至關重要。在插入時，它會被用來決定在選擇要將新項目加入樹中何處時，應該依循哪一個分支。在查詢時，索引越平衡，查找就越快。

`picksplit`
:   當需要分裂索引頁面時，此函式會決定頁面上的哪些項目留在舊頁面，哪些項目移到新頁面。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_picksplit(internal, internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_picksplit);

    Datum
    my_picksplit(PG_FUNCTION_ARGS)
    {
        GistEntryVector *entryvec = (GistEntryVector *) PG_GETARG_POINTER(0);
        GIST_SPLITVEC *v = (GIST_SPLITVEC *) PG_GETARG_POINTER(1);
        OffsetNumber maxoff = entryvec->n - 1;
        GISTENTRY  *ent = entryvec->vector;
        int         i,
                    nbytes;
        OffsetNumber *left,
                   *right;
        data_type  *tmp_union;
        data_type  *unionL;
        data_type  *unionR;
        GISTENTRY **raw_entryvec;

        maxoff = entryvec->n - 1;
        nbytes = (maxoff + 1) * sizeof(OffsetNumber);

        v->spl_left = (OffsetNumber *) palloc(nbytes);
        left = v->spl_left;
        v->spl_nleft = 0;

        v->spl_right = (OffsetNumber *) palloc(nbytes);
        right = v->spl_right;
        v->spl_nright = 0;

        unionL = NULL;
        unionR = NULL;

        /* Initialize the raw entry vector. */
        raw_entryvec = (GISTENTRY **) malloc(entryvec->n * sizeof(void *));
        for (i = FirstOffsetNumber; i <= maxoff; i = OffsetNumberNext(i))
            raw_entryvec[i] = &(entryvec->vector[i]);

        for (i = FirstOffsetNumber; i <= maxoff; i = OffsetNumberNext(i))
        {
            int         real_index = raw_entryvec[i] - entryvec->vector;

            tmp_union = DatumGetDataType(entryvec->vector[real_index].key);
            Assert(tmp_union != NULL);

            /*
             * Choose where to put the index entries and update unionL and unionR
             * accordingly. Append the entries to either v->spl_left or
             * v->spl_right, and care about the counters.
             */

            if (my_choice_is_left(unionL, curl, unionR, curr))
            {
                if (unionL == NULL)
                    unionL = tmp_union;
                else
                    unionL = my_union_implementation(unionL, tmp_union);

                *left = real_index;
                ++left;
                ++(v->spl_nleft);
            }
            else
            {
                /*
                 * Same on the right
                 */
            }
        }

        v->spl_ldatum = DataTypeGetDatum(unionL);
        v->spl_rdatum = DataTypeGetDatum(unionR);
        PG_RETURN_POINTER(v);
    }
    ```

    譯註：上方骨架中的 curl 與 curr 沒有宣告，也沒有賦值（原文如此）。實際實作時須自行宣告並計算這兩個變數，用來表示目前項目放到左側或右側分組時的對應值（例如加入後的聯集或懲罰值），讓 my_choice_is_left 能據以判斷該項目應放到哪一側。本譯文保留原始程式碼，僅在此說明。

    請注意，`picksplit` 函式的結果是藉由修改傳入的 `v` 結構來傳遞的。傳回值本身會被忽略，不過慣例上會傳回 `v` 的位址。

    與 `penalty` 一樣，`picksplit` 函式對索引的良好效能至關重要。設計合適的 `penalty` 與 `picksplit` 實作，正是實作高效能 GiST 索引的挑戰所在。

`same`
:   如果兩個索引項目相同就傳回 true，否則傳回 false。（「索引項目」是索引儲存型別的值，不一定是原始被索引欄位的型別。）

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_same(storage_type, storage_type, internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_same);

    Datum
    my_same(PG_FUNCTION_ARGS)
    {
        prefix_range *v1 = PG_GETARG_PREFIX_RANGE_P(0);
        prefix_range *v2 = PG_GETARG_PREFIX_RANGE_P(1);
        bool       *result = (bool *) PG_GETARG_POINTER(2);

        *result = my_eq(v1, v2);
        PG_RETURN_POINTER(result);
    }
    ```

    由於歷史因素，`same` 函式並不只是傳回一個布林結果；而是必須將該旗標儲存在第三個引數所指示的位置。傳回值本身會被忽略，不過慣例上會傳回該引數的位址。

`distance`
:   給定索引項目 `p` 與查詢值 `q`，此函式判斷該索引項目與查詢值之間的「距離」。如果運算子類別包含任何排序運算子，就必須提供此函式。使用排序運算子的查詢，會以優先傳回「距離」值最小之索引項目的方式來實作，因此其結果必須與該運算子的語意一致。對於葉索引項目，結果只代表到該索引項目的距離；對於內部樹節點，結果必須是任何子項目可能具有的最小距離。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_distance(internal, data_type, smallint, oid, internal)
    RETURNS float8
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而 C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_distance);

    Datum
    my_distance(PG_FUNCTION_ARGS)
    {
        GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0);
        data_type  *query = PG_GETARG_DATA_TYPE_P(1);
        StrategyNumber strategy = (StrategyNumber) PG_GETARG_UINT16(2);
        /* Oid subtype = PG_GETARG_OID(3); */
        /* bool *recheck = (bool *) PG_GETARG_POINTER(4); */
        data_type  *key = DatumGetDataType(entry->key);
        double      retval;

        /*
         * determine return value as a function of strategy, key and query.
         */

        PG_RETURN_FLOAT8(retval);
    }
    ```

    `distance` 函式的引數與 `consistent` 函式的引數完全相同。

    在判斷距離時允許某種程度的近似，只要結果永遠不大於該項目的實際距離即可。因此，例如在幾何應用中，到外接矩形（bounding box）的距離通常就已足夠。對於內部樹節點，傳回的距離不得大於到任何子節點的距離。如果傳回的距離不精確，函式必須將 `*recheck` 設為 true。（對內部樹節點而言不需要這麼做；對它們來說，計算一律被假設為不精確。）在這種情況下，執行器會在從堆積中擷取元組之後計算精確的距離，並在必要時重新排序這些元組。

    如果距離函式對任何葉節點傳回 `*recheck = true`，原始排序運算子的傳回型別就必須是 `float8` 或 `float4`，而且距離函式的結果值必須能與原始排序運算子的結果值相比較，因為執行器會同時使用距離函式的結果與重新計算的排序運算子結果來排序。否則，距離函式的結果值可以是任何有限的 `float8` 值，只要結果值的相對順序與排序運算子所傳回的順序相符即可。（無限大與負無限大在內部用來處理空值等情況，因此不建議 `distance` 函式傳回這些值。）

`fetch`
:   為了僅索引掃描，將資料項目的壓縮索引表示法轉換為原始資料型別。傳回的資料必須是原始被索引值的精確、無損副本。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_fetch(internal)
    RETURNS internal
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    引數是指向 `GISTENTRY` 結構的指標。進入函式時，其 `key` 欄位包含一個壓縮形式的非 NULL 葉資料（datum）。傳回值是另一個 `GISTENTRY` 結構，其 `key` 欄位包含相同資料的原始未壓縮形式。如果運算子類別的 compress 函式對葉項目不做任何處理，`fetch` 方法可以原樣傳回引數。或者，如果運算子類別沒有 compress 函式，也可以省略 `fetch` 方法，因為它必然不會做任何事。

    C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_fetch);

    Datum
    my_fetch(PG_FUNCTION_ARGS)
    {
        GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0);
        input_data_type *in = DatumGetPointer(entry->key);
        fetched_data_type *fetched_data;
        GISTENTRY  *retval;

        retval = palloc(sizeof(GISTENTRY));
        fetched_data = palloc(sizeof(fetched_data_type));

        /*
         * Convert 'fetched_data' into the a Datum of the original datatype.
         */

        /* fill *retval from fetched_data. */
        gistentryinit(*retval, PointerGetDatum(converted_datum),
                      entry->rel, entry->page, entry->offset, FALSE);

        PG_RETURN_POINTER(retval);
    }
    ```

    譯註：上方骨架中的 converted_datum 沒有宣告，也沒有賦值（原文如此）。實際實作時須先把 fetched_data 轉換成原始資料型別的 Datum，存入一個已宣告的變數（例如 converted_datum），再傳給 gistentryinit。本譯文保留原始程式碼，僅在此說明。

    如果 compress 方法對葉項目是有損的，該運算子類別就無法支援僅索引掃描，而且不得定義 `fetch` 函式。

`options`
:   允許定義使用者可見的參數，用來控制運算子類別的行為。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_options(internal)
    RETURNS void
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    此函式會收到一個指向 `local_relopts` 結構的指標，該結構需要填入一組運算子類別特定的選項。其他支援函式可以使用 `PG_HAS_OPCLASS_OPTIONS()` 與 `PG_GET_OPCLASS_OPTIONS()` 巨集來存取這些選項。

    以下是 my_options() 的範例實作，以及其他支援函式如何使用參數：

    ```

    typedef enum MyEnumType
    {
        MY_ENUM_ON,
        MY_ENUM_OFF,
        MY_ENUM_AUTO
    } MyEnumType;

    typedef struct
    {
        int32   vl_len_;    /* varlena header (do not touch directly!) */
        int     int_param;  /* integer parameter */
        double  real_param; /* real parameter */
        MyEnumType enum_param; /* enum parameter */
        int     str_param;  /* string parameter */
    } MyOptionsStruct;

    /* String representation of enum values */
    static relopt_enum_elt_def myEnumValues[] =
    {
        {"on", MY_ENUM_ON},
        {"off", MY_ENUM_OFF},
        {"auto", MY_ENUM_AUTO},
        {(const char *) NULL}   /* list terminator */
    };

    static char *str_param_default = "default";

    /*
     * Sample validator: checks that string is not longer than 8 bytes.
     */
    static void
    validate_my_string_relopt(const char *value)
    {
        if (strlen(value) > 8)
            ereport(ERROR,
                    (errcode(ERRCODE_INVALID_PARAMETER_VALUE),
                     errmsg("str_param must be at most 8 bytes")));
    }

    /*
     * Sample filler: switches characters to lower case.
     */
    static Size
    fill_my_string_relopt(const char *value, void *ptr)
    {
        char   *tmp = str_tolower(value, strlen(value), DEFAULT_COLLATION_OID);
        int     len = strlen(tmp);

        if (ptr)
            strcpy(ptr, tmp);

        pfree(tmp);
        return len + 1;
    }

    PG_FUNCTION_INFO_V1(my_options);

    Datum
    my_options(PG_FUNCTION_ARGS)
    {
        local_relopts *relopts = (local_relopts *) PG_GETARG_POINTER(0);

        init_local_reloptions(relopts, sizeof(MyOptionsStruct));
        add_local_int_reloption(relopts, "int_param", "integer parameter",
                                100, 0, 1000000,
                                offsetof(MyOptionsStruct, int_param));
        add_local_real_reloption(relopts, "real_param", "real parameter",
                                 1.0, 0.0, 1000000.0,
                                 offsetof(MyOptionsStruct, real_param));
        add_local_enum_reloption(relopts, "enum_param", "enum parameter",
                                 myEnumValues, MY_ENUM_ON,
                                 "Valid values are: \"on\", \"off\" and \"auto\".",
                                 offsetof(MyOptionsStruct, enum_param));
        add_local_string_reloption(relopts, "str_param", "string parameter",
                                   str_param_default,
                                   &validate_my_string_relopt,
                                   &fill_my_string_relopt,
                                   offsetof(MyOptionsStruct, str_param));

        PG_RETURN_VOID();
    }

    PG_FUNCTION_INFO_V1(my_compress);

    Datum
    my_compress(PG_FUNCTION_ARGS)
    {
        int     int_param = 100;
        double  real_param = 1.0;
        MyEnumType enum_param = MY_ENUM_ON;
        char   *str_param = str_param_default;

        /*
         * Normally, when opclass contains 'options' method, then options are always
         * passed to support functions.  However, if you add 'options' method to
         * existing opclass, previously defined indexes have no options, so the
         * check is required.
         */
        if (PG_HAS_OPCLASS_OPTIONS())
        {
            MyOptionsStruct *options = (MyOptionsStruct *) PG_GET_OPCLASS_OPTIONS();

            int_param = options->int_param;
            real_param = options->real_param;
            enum_param = options->enum_param;
            str_param = GET_STRING_RELOPTION(options, str_param);
        }

        /* the rest implementation of support function */
    }
    ```

    由於 GiST 中鍵值的表示法很有彈性，它可能取決於使用者指定的參數。例如，可以指定鍵值簽章的長度。範例請參閱 `gtsvector_options()`。

`sortsupport`
:   傳回一個比較子函式，以保留局部性的方式排序資料。`CREATE INDEX` 與 `REINDEX` 命令會使用它。所建立索引的品質，取決於比較子函式所決定的排序順序能多好地保留輸入的局部性。

    `sortsupport` 方法是選用的。如果沒有提供，`CREATE INDEX` 會使用 `penalty` 與 `picksplit` 函式將每個元組插入樹中來建立索引，這樣會慢得多。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_sortsupport(internal)
    RETURNS void
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    引數是指向 `SortSupport` 結構的指標。此函式至少必須填入其 comparator 欄位。比較子接受三個引數：兩個要比較的 Datum，以及一個指向 `SortSupport` 結構的指標。這兩個 Datum 是以其儲存在索引中之格式表示的兩個被索引值；也就是 `compress` 方法所傳回的格式。完整的 API 定義在 `src/include/utils/sortsupport.h` 中。

    C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_sortsupport);

    static int
    my_fastcmp(Datum x, Datum y, SortSupport ssup)
    {
      /* establish order between x and y by computing some sorting value z */

      int z1 = ComputeSpatialCode(x);
      int z2 = ComputeSpatialCode(y);

      return z1 == z2 ? 0 : z1 > z2 ? 1 : -1;
    }

    Datum
    my_sortsupport(PG_FUNCTION_ARGS)
    {
      SortSupport ssup = (SortSupport) PG_GETARG_POINTER(0);

      ssup->comparator = my_fastcmp;
      PG_RETURN_VOID();
    }
    ```

`translate_cmptype`
:   給定一個來自 `src/include/access/cmptype.h` 的 `CompareType` 值，傳回此運算子類別用於對應功能的策略編號。如果運算子類別沒有對應的策略，此函式應該傳回 `InvalidStrategy`。

    這用於時態索引限制條件（亦即 `PRIMARY
    KEY` 與 `UNIQUE`）。如果運算子類別提供了此函式，且它對 `COMPARE_EQ` 傳回結果，就可以將它用在索引限制條件中非 `WITHOUT OVERLAPS` 的部分。

    此支援函式對應於索引存取方法的回呼函式 `amtranslatecmptype`（請參閱[第 63.2 節](../indexam/index-functions.md)）。GiST 索引的 `amtranslatecmptype` 回呼函式只是向下呼叫對應運算子家族的 `translate_cmptype` 支援函式，因為 GiST 索引存取方法本身沒有固定的策略編號。

    此函式的 SQL 宣告必須如下所示：

    ```

    CREATE OR REPLACE FUNCTION my_translate_cmptype(integer)
    RETURNS smallint
    AS 'MODULE_PATHNAME'
    LANGUAGE C STRICT;
    ```

    而運算子家族的註冊必須如下所示：

    ```

    ALTER OPERATOR FAMILY my_opfamily USING gist ADD
        FUNCTION 12 ("any", "any") my_translate_cmptype(int);
    ```

    C 模組中對應的程式碼可以依循以下骨架：

    ```

    PG_FUNCTION_INFO_V1(my_translate_cmptype);

    Datum
    my_translate_cmptype(PG_FUNCTION_ARGS)
    {
        CompareType cmptype = PG_GETARG_INT32(0);
        StrategyNumber ret = InvalidStrategy;

        switch (cmptype)
        {
            case COMPARE_EQ:
                ret = BTEqualStrategyNumber;
        }

        PG_RETURN_UINT16(ret);
    }
    ```

    PostgreSQL 提供了一個轉換函式：`gist_translate_cmptype_common` 用於使用 `RT*StrategyNumber` 常數的運算子類別。`btree_gist` 擴充功能定義了第二個轉換函式 `gist_translate_cmptype_btree`，用於使用 `BT*StrategyNumber` 常數的運算子類別。

所有 GiST 支援方法通常都是在短生命週期的記憶體上下文 中被呼叫的；也就是說，每處理完一個元組，`CurrentMemoryContext` 就會被重設。因此，不太需要費心對你 palloc 的所有東西進行 pfree。不過，在某些情況下，讓支援方法跨多次呼叫快取資料是有用的。為此，請在 `fcinfo->flinfo->fn_mcxt` 中配置生命週期較長的資料，並在 `fcinfo->flinfo->fn_extra` 中保留指向它的指標。這類資料會在整個索引操作（例如單一 GiST 索引掃描、索引建立或索引元組插入）的生命週期內存續。替換 `fn_extra` 值時，請小心 pfree 先前的值，否則洩漏會在操作期間不斷累積。

<a id="GIST-IMPLEMENTATION"></a>

### 65.2.4. 實作 [#](#GIST-IMPLEMENTATION)

<a id="GIST-BUFFERING-BUILD"></a>

#### 65.2.4.1. GiST 索引建立方法 [#](#GIST-BUFFERING-BUILD)

建立 GiST 索引最簡單的方式，就是將所有項目逐一插入。對於大型索引來說，這往往很慢，因為如果索引元組散布在整個索引中，而且索引大到無法放入快取，就會需要大量的隨機 I/O。PostgreSQL 支援兩種替代方法來初次建立 GiST 索引：*排序*（sorted）模式與*緩衝*（buffered）模式。

只有在索引所使用的每個運算子類別都提供 `sortsupport` 函式（如[第 65.2.3 節](gist.md#GIST-EXTENSIBILITY)所述）時，才能使用排序方法。如果都有提供，這種方法通常是最好的，因此預設會使用它。

緩衝方法的運作方式是不立即將元組直接插入索引。對於未排序的資料集，它可以大幅減少所需的隨機 I/O 量。對於排序良好的資料集，好處較小或不存在，因為每次只有少數頁面會收到新的元組，而且即使整個索引放不進快取，這些頁面也放得進去。

緩衝方法比簡單方法更常呼叫 `penalty` 函式，這會消耗一些額外的 CPU 資源。此外，緩衝區需要暫存磁碟空間，最多可達最終索引的大小。緩衝也可能影響最終索引的品質，影響可能是正面的，也可能是負面的。這種影響取決於多種因素，例如輸入資料的分布以及運算子類別的實作。

如果無法排序，則預設情況下，當索引大小達到 [effective_cache_size](../../server-administration/runtime-config/runtime-config-query.md#GUC-EFFECTIVE-CACHE-SIZE) 時，GiST 索引建立會切換為緩衝方法。可以透過 CREATE INDEX 命令的 `buffering` 參數，手動強制使用或防止使用緩衝。預設行為適用於大多數情況，但如果輸入資料是有序的，關閉緩衝可能會讓建立速度稍微加快。

<a id="GIST-EXAMPLES"></a>

### 65.2.5. 範例 [#](#GIST-EXAMPLES)

PostgreSQL 原始碼發行版本包含數個使用 GiST 實作之索引方法的範例。核心系統目前提供文字搜尋支援（為 `tsvector` 與 `tsquery` 建立索引），以及為部分內建幾何資料型別提供相當於 R-Tree 的功能（請參閱 `src/backend/access/gist/gistproc.c`）。下列 `contrib` 模組也包含 GiST 運算子類別：

`btree_gist`
:   為數種資料型別提供相當於 B-tree 的功能

`cube`
:   為多維立方體建立索引

`hstore`
:   用來儲存（鍵, 值）配對的模組

`intarray`
:   用於 int4 值一維陣列的 RD-Tree

`ltree`
:   為樹狀結構建立索引

`pg_trgm`
:   使用三連詞（trigram）比對的文字相似度

`seg`
:   為「浮點數範圍」建立索引

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gist.html)（原文版本：18.6；核對日期：2026-10-17）
