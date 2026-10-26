<a id="SQL-CREATEAGGREGATE"></a><a id="id-1.9.3.57.1"></a>

## CREATE AGGREGATE

CREATE AGGREGATE — 定義新的彙總函式

<a id="id-1.9.3.57.4"></a>

## 語法

```

CREATE [ OR REPLACE ] AGGREGATE name ( [ argmode ] [ argname ] arg_data_type [ , ... ] ) (
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = combinefunc ]
    [ , SERIALFUNC = serialfunc ]
    [ , DESERIALFUNC = deserialfunc ]
    [ , INITCOND = initial_condition ]
    [ , MSFUNC = msfunc ]
    [ , MINVFUNC = minvfunc ]
    [ , MSTYPE = mstate_data_type ]
    [ , MSSPACE = mstate_data_size ]
    [ , MFINALFUNC = mffunc ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = minitial_condition ]
    [ , SORTOP = sort_operator ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
)

CREATE [ OR REPLACE ] AGGREGATE name ( [ [ argmode ] [ argname ] arg_data_type [ , ... ] ]
                        ORDER BY [ argmode ] [ argname ] arg_data_type [ , ... ] ) (
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , INITCOND = initial_condition ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
    [ , HYPOTHETICAL ]
)

or the old syntax

CREATE [ OR REPLACE ] AGGREGATE name (
    BASETYPE = base_type,
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = combinefunc ]
    [ , SERIALFUNC = serialfunc ]
    [ , DESERIALFUNC = deserialfunc ]
    [ , INITCOND = initial_condition ]
    [ , MSFUNC = msfunc ]
    [ , MINVFUNC = minvfunc ]
    [ , MSTYPE = mstate_data_type ]
    [ , MSSPACE = mstate_data_size ]
    [ , MFINALFUNC = mffunc ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = minitial_condition ]
    [ , SORTOP = sort_operator ]
)
```

<a id="id-1.9.3.57.5"></a>

## 說明

`CREATE AGGREGATE` 會定義一個新的彙總函式。`CREATE OR REPLACE AGGREGATE` 則會定義新的彙總函式，或取代現有的定義。發行版本中已內含一些基本且常用的彙總函式；它們記載於[第 9.21 節](../../the-sql-language/functions/functions-aggregate.md)。若有人定義了新的型別，或需要尚未提供的彙總函式，就可以使用 `CREATE AGGREGATE` 來提供所需的功能。

取代現有定義時，不可以變更引數型別、結果型別與直接引數的數量。此外，新的定義必須與舊的定義屬於同一種類（一般彙總函式、有序集合彙總函式或假設集合彙總函式）。

若有指定綱要名稱（例如 `CREATE AGGREGATE myschema.myagg ...`），彙總函式就會建立在指定的綱要中。否則，它會建立在目前的綱要中。

彙總函式是以其名稱與輸入資料型別來識別的。同一個綱要中的兩個彙總函式，若作用於不同的輸入型別，就可以有相同的名稱。彙總函式的名稱與輸入資料型別，也必須與同一個綱要中每個一般函式的名稱與輸入資料型別不同。此行為與一般函式名稱的多載完全相同（請參閱 [CREATE FUNCTION](sql-createfunction.md)）。

簡單的彙總函式由一個或兩個一般函式構成：狀態轉換函式 *`sfunc`*，以及選用的最終計算函式 *`ffunc`*。它們的使用方式如下：

```

sfunc( internal-state, next-data-values ) ---> next-internal-state
ffunc( internal-state ) ---> aggregate-value
```

PostgreSQL 會建立一個資料型別為 *`stype`* 的暫存變數，用來保存彙總函式目前的內部狀態。在每一筆輸入資料列上，會計算彙總引數的值，並以目前的狀態值與新的引數值呼叫狀態轉換函式，以計算新的內部狀態值。所有資料列都處理完之後，會呼叫一次最終函式，以計算彙總函式的傳回值。若沒有最終函式，則會原樣傳回結束時的狀態值。

彙總函式可以提供初始條件，也就是內部狀態值的初始值。它是以 `text` 型別的值來指定並儲存在資料庫中，但必須是狀態值資料型別之常數的有效外部表示形式。若未提供，狀態值一開始為 null。

若狀態轉換函式被宣告為「strict」，就不能以 null 輸入來呼叫它。使用這樣的轉換函式時，彙總函式的執行行為如下。任何輸入值為 null 的資料列都會被忽略（不會呼叫該函式，並保留先前的狀態值）。若初始狀態值為 null，則在第一筆輸入值全部非 null 的資料列上，第一個引數值會取代狀態值，之後在每一筆輸入值全部非 null 的資料列上都會呼叫轉換函式。這對於實作像 `max` 這樣的彙總函式很方便。請注意，只有在 *`state_data_type`* 與第一個 *`arg_data_type`* 相同時，才能使用此行為。當這些型別不同時，你必須提供非 null 的初始條件，或使用非 strict 的轉換函式。

若狀態轉換函式不是 strict，則在每一筆輸入資料列上都會無條件地呼叫它，而且它必須自行處理 null 輸入與 null 狀態值。這讓彙總函式的作者可以完全掌控彙總函式對 null 值的處理方式。

若最終函式被宣告為「strict」，則在結束時的狀態值為 null 時不會呼叫它；而是會自動傳回 null 結果。（當然，這只是 strict 函式的正常行為。）無論如何，最終函式都可以選擇傳回 null 值。例如，`avg` 的最終函式在發現輸入資料列為零筆時會傳回 null。

有時候，將最終函式宣告為不只接受狀態值，還接受與彙總函式輸入值相對應的額外參數，會很有用。這麼做的主要理由，是最終函式為多型，而狀態值的資料型別不足以確定結果型別的情況。這些額外參數一律以 NULL 傳入（因此使用 `FINALFUNC_EXTRA` 選項時，最終函式不可以是 strict），但它們仍然是有效的參數。例如，最終函式可以利用 `get_fn_expr_argtype` 來識別目前呼叫中實際的引數型別。

彙總函式可以選擇支援*移動彙總模式*，如[第 36.12.1 節](../../server-programming/extend/xaggr.md#xaggr-moving-aggregates)所述。這需要指定 `MSFUNC`、`MINVFUNC` 與 `MSTYPE` 參數，並可選擇指定 `MSSPACE`、`MFINALFUNC`、`MFINALFUNC_EXTRA`、`MFINALFUNC_MODIFY` 與 `MINITCOND` 參數。除了 `MINVFUNC` 之外，這些參數的作用都與不帶 `M` 的對應簡單彙總參數相同；它們為彙總函式定義了另一套包含反向轉換函式的實作。

在參數清單中使用 `ORDER BY` 的語法，會建立一種稱為*有序集合彙總函式*的特殊彙總函式；若指定了 `HYPOTHETICAL`，則會建立*假設集合彙總函式*。這些彙總函式以與順序相關的方式，作用於已排序之值所構成的群組，因此指定輸入排序順序是呼叫中不可或缺的一部分。此外，它們可以有*直接*引數，也就是每次彙總只求值一次、而不是每筆輸入資料列求值一次的引數。假設集合彙總函式是有序集合彙總函式的一個子類別，其中部分直接引數必須在數量與資料型別上與彙總引數欄位相符。這使得這些直接引數的值，可以作為一筆額外的「假設」資料列，加入彙總輸入資料列的集合中。

彙總函式可以選擇支援*部分彙總*，如[第 36.12.4 節](../../server-programming/extend/xaggr.md#xaggr-partial-aggregates)所述。這需要指定 `COMBINEFUNC` 參數。若 *`state_data_type`* 為 `internal`，通常也適合提供 `SERIALFUNC` 與 `DESERIALFUNC` 參數，以便能夠進行平行彙總。請注意，彙總函式也必須標示為 `PARALLEL SAFE`，才能啟用平行彙總。

行為類似 `MIN` 或 `MAX` 的彙總函式，有時可以藉由查詢索引而非掃描每一筆輸入資料列來最佳化。若此彙總函式可以這樣最佳化，請指定一個*排序運算子*來表明。基本的要求是，彙總函式必須產生由該運算子所導出之排序順序中的第一個元素；換句話說：

```

SELECT agg(col) FROM tab;
```

必須等同於：

```

SELECT col FROM tab ORDER BY col USING sortop LIMIT 1;
```

進一步的假設是，彙總函式會忽略 null 輸入，並且若且唯若沒有任何非 null 輸入時，才產生 null 結果。通常，資料型別的 `<` 運算子是適用於 `MIN` 的排序運算子，而 `>` 是適用於 `MAX` 的排序運算子。請注意，除非所指定的運算子是 B-tree 索引運算子類別中的「小於」或「大於」策略成員，否則此最佳化永遠不會真正生效。

要能建立彙總函式，你必須具有引數型別、狀態型別與傳回型別上的 `USAGE` 權限，以及支援函式上的 `EXECUTE` 權限。

<a id="id-1.9.3.57.6"></a>

## 參數

*`name`*
:   要建立之彙總函式的名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN` 或 `VARIADIC`。（彙總函式不支援 `OUT` 引數。）若省略，預設為 `IN`。只有最後一個引數可以標示為 `VARIADIC`。

*`argname`*
:   引數的名稱。目前這只在文件用途上有用。若省略，該引數就沒有名稱。

*`arg_data_type`*
:   此彙總函式所作用的輸入資料型別。要建立零引數的彙總函式，請以 `*` 取代引數規格清單。（這類彙總函式的一個例子是 `count(*)`。）

*`base_type`*
:   在 `CREATE AGGREGATE` 的舊語法中，輸入資料型別是由 `basetype` 參數指定，而不是寫在彙總函式名稱旁邊。請注意，此語法只允許一個輸入參數。要以此語法定義零引數的彙總函式，請將 `basetype` 指定為 `"ANY"`（而不是 `*`）。有序集合彙總函式不能以舊語法定義。

*`sfunc`*
:   要對每一筆輸入資料列呼叫的狀態轉換函式名稱。對於一般的 *`N`* 個引數的彙總函式，*`sfunc`* 必須接受 *`N`*+1 個引數，第一個引數的型別為 *`state_data_type`*，其餘引數則與彙總函式所宣告的輸入資料型別相符。此函式必須傳回 *`state_data_type`* 型別的值。此函式接受目前的狀態值與目前的輸入資料值，並傳回下一個狀態值。

    對於有序集合（包括假設集合）彙總函式，狀態轉換函式只接收目前的狀態值與彙總引數，而不接收直接引數。除此之外都相同。

*`state_data_type`*
:   彙總函式狀態值的資料型別。

*`state_data_size`*
:   彙總函式狀態值的大約平均大小（以位元組為單位）。若省略此參數或其為零，則會根據 *`state_data_type`* 使用預設的估計值。規劃器會使用此值來估計分組彙總查詢所需的記憶體。

*`ffunc`*
:   在走訪完所有輸入資料列之後，為計算彙總函式結果而呼叫的最終函式名稱。對於一般的彙總函式，此函式必須接受單一個 *`state_data_type`* 型別的引數。彙總函式的傳回資料型別被定義為此函式的傳回型別。若未指定 *`ffunc`*，則會使用結束時的狀態值作為彙總函式的結果，且傳回型別為 *`state_data_type`*。

    對於有序集合（包括假設集合）彙總函式，最終函式不只接收最終狀態值，還會接收所有直接引數的值。

    若指定了 `FINALFUNC_EXTRA`，則除了最終狀態值與任何直接引數之外，最終函式還會接收與彙總函式一般（彙總）引數相對應的額外 NULL 值。這主要用於在定義多型彙總函式時，讓彙總函式的結果型別能夠被正確解析。

`FINALFUNC_MODIFY` = { `READ_ONLY` | `SHAREABLE` | `READ_WRITE` }
:   此選項指定最終函式是否為不修改其引數的純函式。`READ_ONLY` 表示它不會修改；另外兩個值則表示它可能會變更轉換狀態值。更多細節請參閱下文的[注意事項](sql-createaggregate.md#SQL-CREATEAGGREGATE-NOTES)。預設為 `READ_ONLY`，但有序集合彙總函式除外，其預設為 `READ_WRITE`。

*`combinefunc`*
:   可以選擇指定 *`combinefunc`* 函式，讓彙總函式支援部分彙總。若有提供，*`combinefunc`* 必須將兩個 *`state_data_type`* 值合併——每個值都包含對輸入值之某個子集進行彙總的結果——以產生一個新的 *`state_data_type`*，代表對兩組輸入進行彙總的結果。此函式可以被視為一種 *`sfunc`*，只是它不是作用於單一筆輸入資料列並將其加入累計中的彙總狀態，而是將另一個彙總狀態加入累計中的狀態。

    *`combinefunc`* 必須宣告為接受兩個 *`state_data_type`* 的引數，並傳回 *`state_data_type`* 的值。此函式可以選擇為「strict」。在這種情況下，當任一輸入狀態為 null 時，就不會呼叫此函式；另一個狀態會被當作正確的結果。

    對於 *`state_data_type`* 為 `internal` 的彙總函式，*`combinefunc`* 不可以是 strict。在這種情況下，*`combinefunc`* 必須確保 null 狀態能被正確處理，並且所傳回的狀態被妥善儲存在彙總記憶體上下文（memory context）中。

*`serialfunc`*
:   *`state_data_type`* 為 `internal` 的彙總函式，只有在具有 *`serialfunc`* 函式時才能參與平行彙總；該函式必須將彙總狀態序列化為 `bytea` 值，以便傳送到另一個程序。此函式必須接受單一個 `internal` 型別的引數，並傳回 `bytea` 型別。同時也需要對應的 *`deserialfunc`*。

*`deserialfunc`*
:   將先前序列化的彙總狀態反序列化回 *`state_data_type`*。此函式必須接受兩個型別分別為 `bytea` 與 `internal` 的引數，並產生 `internal` 型別的結果。（注意：第二個 `internal` 引數不會被使用，但基於型別安全的理由而必須存在。）

*`initial_condition`*
:   狀態值的初始設定。這必須是資料型別 *`state_data_type`* 可接受之形式的字串常數。若未指定，狀態值一開始為 null。

*`msfunc`*
:   在移動彙總模式中，要對每一筆輸入資料列呼叫的正向狀態轉換函式名稱。它與一般的轉換函式完全相同，只是它的第一個引數與結果的型別為 *`mstate_data_type`*，而這可能與 *`state_data_type`* 不同。

*`minvfunc`*
:   在移動彙總模式中使用的反向狀態轉換函式名稱。此函式的引數與結果型別與 *`msfunc`* 相同，但它是用來從目前的彙總狀態中移除一個值，而不是將一個值加入其中。反向轉換函式必須與正向狀態轉換函式具有相同的 strict 屬性。

*`mstate_data_type`*
:   使用移動彙總模式時，彙總函式狀態值的資料型別。

*`mstate_data_size`*
:   使用移動彙總模式時，彙總函式狀態值的大約平均大小（以位元組為單位）。其作用與 *`state_data_size`* 相同。

*`mffunc`*
:   使用移動彙總模式時，在走訪完所有輸入資料列之後，為計算彙總函式結果而呼叫的最終函式名稱。其作用與 *`ffunc`* 相同，只是它的第一個引數型別為 *`mstate_data_type`*，而額外的虛擬引數是藉由寫出 `MFINALFUNC_EXTRA` 來指定的。由 *`mffunc`* 或 *`mstate_data_type`* 所決定的彙總結果型別，必須與彙總函式一般實作所決定的結果型別相符。

`MFINALFUNC_MODIFY` = { `READ_ONLY` | `SHAREABLE` | `READ_WRITE` }
:   此選項類似 `FINALFUNC_MODIFY`，但它描述的是移動彙總最終函式的行為。

*`minitial_condition`*
:   使用移動彙總模式時，狀態值的初始設定。其作用與 *`initial_condition`* 相同。

*`sort_operator`*
:   類似 `MIN` 或 `MAX` 之彙總函式的相關排序運算子。這只是一個運算子名稱（可以用綱要限定）。此運算子被假定具有與彙總函式相同的輸入資料型別（彙總函式必須是單一引數的一般彙總函式）。

`PARALLEL =` { `SAFE` | `RESTRICTED` | `UNSAFE` }
:   `PARALLEL SAFE`、`PARALLEL RESTRICTED` 與 `PARALLEL UNSAFE` 的意義與 [`CREATE FUNCTION`](sql-createfunction.md) 中的相同。若彙總函式被標示為 `PARALLEL UNSAFE`（這是預設值！）或 `PARALLEL RESTRICTED`，就不會被考慮進行平行化。請注意，規劃器不會參考彙總函式之支援函式的平行安全性標示，只會參考彙總函式本身的標示。

`HYPOTHETICAL`
:   僅適用於有序集合彙總函式，此旗標指定彙總引數要依照假設集合彙總函式的要求來處理：也就是說，最後幾個直接引數必須與彙總（`WITHIN GROUP`）引數的資料型別相符。`HYPOTHETICAL` 旗標對執行期的行為沒有影響，只會影響剖析時對彙總函式引數之資料型別與定序的解析。

`CREATE AGGREGATE` 的參數可以用任何順序撰寫，而不只是上面所示的順序。

<a id="SQL-CREATEAGGREGATE-NOTES"></a>

## 注意事項

在指定支援函式名稱的參數中，你可以視需要寫出綱要名稱，例如 `SFUNC = public.sum`。不過，不要在那裡寫出引數型別——支援函式的引數型別是由其他參數決定的。

通常，PostgreSQL 函式被預期是不修改其輸入值的真正函式。不過，彙總轉換函式*在彙總的情境中使用時*，被允許取巧，就地修改其轉換狀態引數。與每次都建立一份新的轉換狀態複本相比，這可以帶來可觀的效能優勢。

同樣地，雖然一般預期彙總最終函式不會修改其輸入值，但有時要避免修改轉換狀態引數並不實際。這樣的行為必須使用 `FINALFUNC_MODIFY` 參數來宣告。`READ_WRITE` 值表示最終函式會以未指定的方式修改轉換狀態。此值會使該彙總函式無法作為視窗函式使用，也會阻止對共用相同輸入值與轉換函式的彙總呼叫合併其轉換狀態。`SHAREABLE` 值表示在最終函式之後不能再套用轉換函式，但可以對結束時的轉換狀態值進行多次最終函式呼叫。此值會使該彙總函式無法作為視窗函式使用，但允許合併轉換狀態。（也就是說，此處所關注的最佳化並不是重複套用同一個最終函式，而是將不同的最終函式套用到同一個結束時的轉換狀態值。只要沒有任何最終函式被標示為 `READ_WRITE`，就允許這麼做。）

若彙總函式支援移動彙總模式，當它被用作框架起點會移動之視窗（也就是框架起始模式不是 `UNBOUNDED PRECEDING` 的視窗）的視窗函式時，將會提升計算效率。概念上，正向轉換函式會在輸入值從底部進入視窗框架時，將它們加入彙總函式的狀態；而反向轉換函式則會在它們從頂部離開框架時，再將它們移除。因此，移除值時，總是以與加入時相同的順序移除。所以，每當呼叫反向轉換函式時，它都會收到最早加入但尚未移除的引數值。反向轉換函式可以假定在它移除最舊的資料列之後，目前的狀態中至少還會留下一筆資料列。（若情況並非如此，視窗函式機制只會重新開始一次新的彙總，而不會使用反向轉換函式。）

移動彙總模式的正向轉換函式不被允許傳回 NULL 作為新的狀態值。若反向轉換函式傳回 NULL，這會被視為一個指示，表示該反向函式無法針對這筆特定的輸入反轉狀態計算，因此會針對目前的框架起始位置從頭重新進行彙總計算。此慣例讓移動彙總模式可以用在某些情境中：在這些情境裡，有少數不常發生的情況，要從累計中的狀態值反轉回去並不實際。

若未提供移動彙總實作，彙總函式仍然可以搭配移動的框架使用，但每當框架起點移動時，PostgreSQL 都會重新計算整個彙總。請注意，無論彙總函式是否支援移動彙總模式，PostgreSQL 都能在不重新計算的情況下處理框架終點的移動；這是藉由持續將新的值加入彙總函式的狀態來完成的。這就是為什麼將彙總函式作為視窗函式使用時，要求最終函式必須是唯讀的：它不可以破壞彙總函式的狀態值，如此一來，即使已經針對某一組框架邊界取得彙總結果值，彙總仍然可以繼續進行。

有序集合彙總函式的語法允許對最後一個直接參數與最後一個彙總（`WITHIN GROUP`）參數都指定 `VARIADIC`。不過，目前的實作以兩種方式限制 `VARIADIC` 的使用。第一，有序集合彙總函式只能使用 `VARIADIC "any"`，而不能使用其他可變引數陣列型別。第二，若最後一個直接參數是 `VARIADIC "any"`，則只能有一個彙總參數，而且它也必須是 `VARIADIC "any"`。（在系統目錄所使用的表示方式中，這兩個參數會合併為單一個 `VARIADIC "any"` 項目，因為 `pg_proc` 無法表示具有超過一個 `VARIADIC` 參數的函式。）若彙總函式是假設集合彙總函式，則與 `VARIADIC "any"` 參數相符的直接引數就是假設的引數；任何在其之前的參數則代表額外的直接引數，這些引數不受必須與彙總引數相符的限制。

目前，有序集合彙總函式不需要支援移動彙總模式，因為它們不能作為視窗函式使用。

目前不支援對有序集合彙總函式進行部分彙總（包括平行彙總）。此外，對於包含 `DISTINCT` 或 `ORDER BY` 子句的彙總呼叫，永遠不會使用部分彙總，因為在部分彙總期間無法支援這些語意。

<a id="id-1.9.3.57.8"></a>

## 範例

請參閱[第 36.12 節](../../server-programming/extend/xaggr.md)。

<a id="id-1.9.3.57.9"></a>

## 相容性

`CREATE AGGREGATE` 是 PostgreSQL 的語言擴充。SQL 標準並未提供使用者自訂的彙總函式。

<a id="id-1.9.3.57.10"></a>

## 另請參閱

[ALTER AGGREGATE](sql-alteraggregate.md), [DROP AGGREGATE](sql-dropaggregate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createaggregate.html)（原文版本：18.6；核對日期：2026-10-04）
