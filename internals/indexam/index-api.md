<a id="INDEX-API"></a>

## 63.1. 索引的基本 API 結構 [#](#INDEX-API)

每個索引存取方法都由
[`pg_am`](../catalogs/catalog-pg-am.md)
系統目錄中的一筆資料列來描述。`pg_am` 項目
為該索引存取方法指定名稱與*處理函式*（handler function）。這些項目可以使用
[CREATE ACCESS METHOD](../../reference/sql-commands/sql-create-access-method.md) 與
[DROP ACCESS METHOD](../../reference/sql-commands/sql-drop-access-method.md) SQL 命令建立與刪除。

索引存取方法的處理函式必須宣告為接受單一個 `internal` 型別的參數，並傳回
虛擬型別 `index_am_handler`。此參數是一個虛設值，僅用於防止處理函式直接從
SQL 命令中被呼叫。函式的結果必須是一個以 palloc 配置、型別為
`IndexAmRoutine` 的結構，其中包含核心程式碼使用該索引存取方法所需知道的一切。
`IndexAmRoutine` 結構也稱為該存取方法的 *API 結構*，其中包含指定存取方法各種
固定特性的欄位，例如它能否支援多欄索引。更重要的是，它包含指向該存取方法之支援函式的
指標，這些支援函式負責存取索引的所有實際工作。這些支援函式是一般的 C 函式，
在 SQL 層級既不可見，也無法呼叫。支援函式的說明請參閱[第 63.2 節](index-functions.md)。

`IndexAmRoutine` 結構的定義如下：

```

typedef struct IndexAmRoutine
{
    NodeTag     type;

    /*
     * Total number of strategies (operators) by which we can traverse/search
     * this AM.  Zero if AM does not have a fixed set of strategy assignments.
     */
    uint16      amstrategies;
    /* total number of support functions that this AM uses */
    uint16      amsupport;
    /* opclass options support function number or 0 */
    uint16      amoptsprocnum;
    /* does AM support ORDER BY indexed column's value? */
    bool        amcanorder;
    /* does AM support ORDER BY result of an operator on indexed column? */
    bool        amcanorderbyop;
    /* does AM support hashing using API consistent with the hash AM? */
    bool        amcanhash;
    /* do operators within an opfamily have consistent equality semantics? */
    bool        amconsistentequality;
    /* do operators within an opfamily have consistent ordering semantics? */
    bool        amconsistentordering;
    /* does AM support backward scanning? */
    bool        amcanbackward;
    /* does AM support UNIQUE indexes? */
    bool        amcanunique;
    /* does AM support multi-column indexes? */
    bool        amcanmulticol;
    /* does AM require scans to have a constraint on the first index column? */
    bool        amoptionalkey;
    /* does AM handle ScalarArrayOpExpr quals? */
    bool        amsearcharray;
    /* does AM handle IS NULL/IS NOT NULL quals? */
    bool        amsearchnulls;
    /* can index storage data type differ from column data type? */
    bool        amstorage;
    /* can an index of this type be clustered on? */
    bool        amclusterable;
    /* does AM handle predicate locks? */
    bool        ampredlocks;
    /* does AM support parallel scan? */
    bool        amcanparallel;
    /* does AM support parallel build? */
    bool        amcanbuildparallel;
    /* does AM support columns included with clause INCLUDE? */
    bool        amcaninclude;
    /* does AM use maintenance_work_mem? */
    bool        amusemaintenanceworkmem;
    /* does AM summarize tuples, with at least all tuples in the block
     * summarized in one summary */
    bool        amsummarizing;
    /* OR of parallel vacuum flags */
    uint8       amparallelvacuumoptions;
    /* type of data stored in index, or InvalidOid if variable */
    Oid         amkeytype;

    /* interface functions */
    ambuild_function ambuild;
    ambuildempty_function ambuildempty;
    aminsert_function aminsert;
    aminsertcleanup_function aminsertcleanup;   /* can be NULL */
    ambulkdelete_function ambulkdelete;
    amvacuumcleanup_function amvacuumcleanup;
    amcanreturn_function amcanreturn;   /* can be NULL */
    amcostestimate_function amcostestimate;
    amgettreeheight_function amgettreeheight;   /* can be NULL */
    amoptions_function amoptions;
    amproperty_function amproperty;     /* can be NULL */
    ambuildphasename_function ambuildphasename;   /* can be NULL */
    amvalidate_function amvalidate;
    amadjustmembers_function amadjustmembers; /* can be NULL */
    ambeginscan_function ambeginscan;
    amrescan_function amrescan;
    amgettuple_function amgettuple;     /* can be NULL */
    amgetbitmap_function amgetbitmap;   /* can be NULL */
    amendscan_function amendscan;
    ammarkpos_function ammarkpos;       /* can be NULL */
    amrestrpos_function amrestrpos;     /* can be NULL */

    /* interface functions to support parallel index scans */
    amestimateparallelscan_function amestimateparallelscan;    /* can be NULL */
    aminitparallelscan_function aminitparallelscan;    /* can be NULL */
    amparallelrescan_function amparallelrescan;    /* can be NULL */

    /* interface functions to support planning */
    amtranslate_strategy_function amtranslatestrategy;  /* can be NULL */
    amtranslate_cmptype_function amtranslatecmptype;    /* can be NULL */
} IndexAmRoutine;
```

譯註：上方結構中 amoptionalkey 的註解寫作「does AM require scans to have a constraint on the first index column?」（存取方法是否要求掃描在第一個索引欄位上具有限制條件？），與欄位名稱及下方正文的語意相反。依正文說明，此旗標為 true 表示允許第一個索引欄位沒有限制條件；為 false 才表示要求第一個索引欄位必須具有限制條件。本譯文保留原始程式碼，僅在此說明。

索引存取方法要能發揮作用，還必須在
[`pg_opfamily`](../catalogs/catalog-pg-opfamily.md)、
[`pg_opclass`](../catalogs/catalog-pg-opclass.md)、
[`pg_amop`](../catalogs/catalog-pg-amop.md) 與
[`pg_amproc`](../catalogs/catalog-pg-amproc.md)
中定義一個或多個*運算子家族*與*運算子類別*。
這些項目讓規劃器能夠判斷哪些種類的查詢條件（query qualifications）可以搭配
此存取方法的索引使用。運算子家族與運算子類別的說明請參閱[第 36.16 節](../../server-programming/extend/xindex.md)，那是閱讀本章前的必備知識。

個別索引由一筆
[`pg_class`](../catalogs/catalog-pg-class.md)
項目將其描述為實體關聯，再加上一筆
[`pg_index`](../catalogs/catalog-pg-index.md)
項目顯示索引的邏輯內容 — 也就是它擁有的索引欄位集合，以及由相關運算子類別
所表達的這些欄位的語意。索引欄位（鍵值）可以是底層資料表的單純欄位，也可以是
針對資料表資料列的運算式。索引存取方法通常不在意索引鍵值來自何處（它拿到的一律是
預先計算好的鍵值），但會非常在意
`pg_index` 中的運算子類別資訊。這兩個目錄項目都可以透過
`Relation` 資料結構存取，該結構會傳遞給索引上的所有操作。

`IndexAmRoutine` 的某些旗標欄位有不明顯的
含義。`amcanunique` 的要求
在[第 63.5 節](index-unique-checks.md)中討論。
`amcanmulticol` 旗標宣告該存取方法支援多鍵欄索引，而
`amoptionalkey` 宣告它允許在第一個索引欄位沒有給定可用於索引之限制子句的情況下進行掃描。
當 `amcanmulticol` 為 false 時，
`amoptionalkey` 基本上表示該存取方法是否支援
不帶任何限制子句的全索引掃描。
支援多個索引欄位的存取方法*必須*支援
省略第一個欄位之後任一或全部欄位之限制的掃描；不過它們可以要求第一個索引欄位
必須出現某些限制，這是透過將
`amoptionalkey` 設為 false 來表示。
索引 AM 可能將
`amoptionalkey` 設為 false 的一個原因，是它不為
null 值建立索引。由於大多數可用於索引的運算子都是
嚴格的（strict），因此對 null 輸入不可能傳回 true，
乍看之下，不為 null 值儲存索引項目很有吸引力：
反正索引掃描永遠不可能傳回它們。然而，當索引掃描對某個
索引欄位沒有限制子句時，這個論點就不成立了。實務上這表示
`amoptionalkey` 為 true 的索引必須
為 null 建立索引，因為規劃器可能決定在完全沒有掃描鍵的情況下使用這種索引。
相關的限制是：支援多個索引欄位的索引存取方法*必須*
支援為第一個欄位之後各欄位中的 null 值建立索引，因為規劃器
會假設該索引可用於不限制這些欄位的查詢。例如，考慮一個建立在 (a,b) 上的索引，以及一個帶有
`WHERE a = 4` 的查詢。系統會假設該索引可以
用來掃描 `a = 4` 的資料列；若該索引省略了 `b` 為 null 的資料列，這就是錯的。
不過，省略第一個索引欄位為 null 的資料列則沒有問題。
確實為 null 建立索引的索引存取方法也可以設定
`amsearchnulls`，表示它支援以
`IS NULL` 與 `IS NOT NULL` 子句作為搜尋條件。

`amcaninclude` 旗標表示該
存取方法是否支援「內含」（included）欄位，也就是它能夠
在鍵欄位之外儲存（但不處理）額外的欄位。
上一段的要求只適用於鍵欄位。特別是，
`amcanmulticol`=`false`
與 `amcaninclude`=`true` 的組合是
合理的：這表示只能有一個鍵欄位，但也可以
有內含欄位。此外，無論 `amoptionalkey` 為何，內含欄位都必須允許為
null。

`amsummarizing` 旗標表示該
存取方法是否會彙總已建立索引的元組（tuple），彙總粒度
至少為每個區塊。
不指向個別元組、而是指向區塊範圍的存取方法
（例如 BRIN）可以允許 HOT 最佳化
繼續進行。這不適用於索引述詞中所參照的屬性；更新這類屬性一律會停用 HOT。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/index-api.html)（原文版本：18.6；核對日期：2026-10-17）
