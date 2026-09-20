<a id="XAGGR"></a>
## 36.12. 使用者自訂聚合 [#](#XAGGR)

[36.12.1. 移動式聚合模式](xaggr.md#XAGGR-MOVING-AGGREGATES)

[36.12.2. 多型與可變引數聚合](xaggr.md#XAGGR-POLYMORPHIC-AGGREGATES)

[36.12.3. 有序集合聚合](xaggr.md#XAGGR-ORDERED-SET-AGGREGATES)

[36.12.4. 部分聚合](xaggr.md#XAGGR-PARTIAL-AGGREGATES)

[36.12.5. 聚合的支援函式](xaggr.md#XAGGR-SUPPORT-FUNCTIONS)

<a id="id-1.8.3.15.2"></a>

PostgreSQL 中的聚合函式
是以*狀態值（state value）*
與*狀態轉換函式（state transition function）*來定義的。
也就是說，聚合是使用一個狀態值來運作的，
每處理完一列輸入資料，這個狀態值就會更新一次。
要定義一個新的聚合
函式，需要選擇一個作為狀態值的資料型別、
一個狀態的初始值，以及一個狀態轉換
函式。狀態轉換函式接受先前的狀態
值，以及聚合針對目前這一列的輸入值，並
傳回一個新的狀態值。
若聚合所要的結果，與需要保留在
執行中狀態值裡的資料不同，也可以指定一個
*最終函式（final function）*。最終函式接受
最終的狀態值，並傳回聚合結果所需要的任何內容。
基本上，轉換函式與最終函式都只是普通的
函式，也可以在聚合的情境之外使用。（實務上，出於效能考量，
建立只能在被當作聚合的一部分呼叫時
才能運作的特化轉換函式，通常會有幫助。）

因此，除了聚合使用者所看到的引數與結果資料型別之外，
還存在一個內部的狀態值資料型別，
它可能與引數型別及結果型別皆不相同。

若我們定義一個不使用最終函式的聚合，
就會得到一個對每一列的欄位值計算執行中函式結果的聚合。
`sum` 就是這種聚合的
一個例子。`sum` 從零開始，
並且永遠將目前這一列的值加到
它的執行中總和上。舉例來說，若我們想讓 `sum`
聚合能用於複數的資料型別，
我們只需要該資料型別的加法函式即可。
該聚合的定義會是：

```

CREATE AGGREGATE sum (complex)
(
    sfunc = complex_add,
    stype = complex,
    initcond = '(0,0)'
);
```

我們可能會這樣使用它：

```

SELECT sum(a) FROM test_complex;

   sum
-----------
 (34,53.9)
```

（請注意，我們是依靠函式多載：名為 `sum`
的聚合不只一個，但
PostgreSQL 能判斷出，哪一種
sum 適用於型別為 `complex` 的欄位。）

上述 `sum` 的定義，在沒有任何非 null 輸入值時，
會傳回零（初始狀態值）。
也許我們反而希望在這種情況下傳回 null — SQL 標準
就是預期 `sum` 應該有這樣的行為。我們只要
省略 `initcond` 子句，就可以做到這一點，
如此一來初始狀態值就會是 null。一般而言，
這代表 `sfunc` 需要檢查狀態值輸入是否為 null。但對於
`sum` 以及其他一些簡單的聚合，像是
`max` 與 `min`，
只需要將第一個非 null 輸入值放入
狀態變數中，然後從第二個非 null 輸入值開始
套用轉換函式即可。若初始狀態值為 null，且
轉換函式被標記為「strict」（也就是說，遇到 null
輸入時不會被呼叫），PostgreSQL
會自動這麼做。

「strict」轉換函式的另一項預設行為，
是每當遇到 null 輸入值時，先前的狀態值會保持不變。
因此，null 值會被忽略。若您需要
對 null 輸入有其他行為，請不要將您的
轉換函式宣告為 strict；而是改為撰寫程式碼，檢查 null 輸入，
並執行所需的處理。

`avg`（平均值）是較為複雜的聚合範例。
它需要
兩項執行中的狀態：輸入值的總和，以及輸入值
的數量。最終結果是將這兩個數量相除而得。平均值
通常是以陣列作為狀態值來實作的。舉例來說，
`avg(float8)` 的內建實作
看起來像這樣：

```

CREATE AGGREGATE avg (float8)
(
    sfunc = float8_accum,
    stype = float8[],
    finalfunc = float8_avg,
    initcond = '{0,0,0}'
);
```

### 注意

`float8_accum` 需要一個三個元素的陣列，而不是
兩個元素，因為除了輸入值的總和與數量之外，
它還會累加平方和。這是為了讓它除了 `avg`
之外，也能用於其他一些聚合。

SQL 中的聚合函式呼叫，允許使用 `DISTINCT`
與 `ORDER BY` 選項，控制哪些資料列會被
餵給聚合的轉換函式，以及餵入的順序。這些
選項是在幕後實作的，並不是聚合的支援函式
所需要關心的事。

更多詳情請參閱
[CREATE AGGREGATE](../../reference/sql-commands/sql-createaggregate.md)
指令。

<a id="XAGGR-MOVING-AGGREGATES"></a>

### 36.12.1. 移動式聚合模式 [#](#XAGGR-MOVING-AGGREGATES)

<a id="id-1.8.3.15.12.2"></a><a id="id-1.8.3.15.12.3"></a>

聚合函式可以選擇性地支援*移動式聚合
模式（moving-aggregate mode）*，這能讓聚合函式在具有
移動式框架起始點的視窗內，執行速度大幅提升。
（關於將聚合函式作為視窗函式使用的資訊，
請參閱[3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)
與[4.2.8 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)。）
其基本概念是，除了一般的「正向」
轉換函式之外，聚合還提供一個*反向
轉換函式（inverse transition function）*，讓資料列
在離開視窗框架時，可以從聚合執行中的狀態值中被移除。
舉例來說，使用加法作為正向轉換函式的
`sum` 聚合，會使用減法作為反向
轉換函式。若沒有反向轉換函式，視窗
函式機制每次框架起始點移動時，都必須重新從頭計算聚合，
導致執行時間與輸入資料列數量乘以平均框架長度成正比。有了反向
轉換函式，執行時間就只會與
輸入資料列數量成正比。

反向轉換函式接收目前的狀態值，以及目前
狀態中所包含最早那一列的聚合輸入值。它必須
重新建構出，若給定的這一列輸入從未被聚合過，
只有它後面的那些列被聚合過，狀態值本應是什麼樣子。有時候
這需要正向轉換函式保留比一般聚合模式
所需更多的狀態。因此，
移動式聚合模式使用一套與一般模式完全獨立的實作：它有自己的
狀態資料型別、自己的正向轉換函式，以及（若有需要）自己的最終函式。
若不需要額外的狀態，這些也可以與
一般模式的資料型別及函式相同。

舉例來說，我們可以像這樣擴充上面給出的 `sum`
聚合，讓它支援移動式聚合模式：

```

CREATE AGGREGATE sum (complex)
(
    sfunc = complex_add,
    stype = complex,
    initcond = '(0,0)',
    msfunc = complex_add,
    minvfunc = complex_sub,
    mstype = complex,
    minitcond = '(0,0)'
);
```

名稱以 `m` 開頭的參數，定義了移動式
聚合的實作。除了反向轉換
函式 `minvfunc` 之外，它們都對應到
不帶 `m` 的一般聚合參數。

移動式聚合模式的正向轉換函式，不允許
將新狀態值傳回為 null。若反向轉換
函式傳回 null，這會被視為一個訊號，表示反向
函式無法針對這個特定的輸入，反轉狀態計算，
因此該聚合計算，將針對目前的框架起始位置，從頭重做一次。這項慣例讓
移動式聚合模式，能用於某些少數難以從執行中狀態值
反轉出來的情況。反向轉換函式可以對這些情況
「放棄」（punt），只要它在大多數情況下能正常運作，
最終結果依然會是划算的。舉例來說，處理浮點數的
聚合，可能會選擇在必須從執行中
狀態值移除 `NaN`（非數字）輸入時放棄。

在撰寫移動式聚合支援函式時，務必確保
反向轉換函式能夠精確地重新建構出正確的
狀態值。否則，根據是否使用移動式聚合模式，
結果可能會出現使用者可見的差異。
一個一開始看似容易加上反向轉換
函式，但實際上無法滿足這項要求的聚合範例，
就是對 `float4` 或 `float8` 輸入的 `sum`。
天真地宣告 `sum(float8)` 可能會像這樣：

```

CREATE AGGREGATE unsafe_sum (float8)
(
    stype = float8,
    sfunc = float8pl,
    mstype = float8,
    msfunc = float8pl,
    minvfunc = float8mi
);
```

然而，這個聚合可能會產生與沒有反向轉換函式時
截然不同的結果。舉例來說，請考慮：

```

SELECT
  unsafe_sum(x) OVER (ORDER BY n ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)
FROM (VALUES (1, 1.0e20::float8),
             (2, 1.0::float8)) AS v (n,x);
```

這個查詢的第二個結果會傳回 `0`，而不是
預期中的 `1`。原因在於浮點數值精確度
有限：將 `1` 加到 `1e20` 上，結果
仍然是 `1e20`，因此從中減去 `1e20`
會得到 `0`，而不是 `1`。請注意，這是
浮點數運算本身普遍存在的限制，並非
PostgreSQL 的限制。

<a id="XAGGR-POLYMORPHIC-AGGREGATES"></a>

### 36.12.2. 多型與可變引數聚合 [#](#XAGGR-POLYMORPHIC-AGGREGATES)

<a id="id-1.8.3.15.13.2"></a><a id="id-1.8.3.15.13.3"></a>

聚合函式可以使用多型的
狀態轉換函式或最終函式，如此一來，同一組函式
就可以用來實作多個聚合。
關於多型函式的說明，請參閱
[36.2.5 節](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)。
更進一步，聚合函式本身也可以指定為
多型的輸入型別與狀態型別，讓單一個
聚合定義，能為多種輸入資料型別服務。
以下是一個多型聚合的範例：

```

CREATE AGGREGATE array_accum (anycompatible)
(
    sfunc = array_append,
    stype = anycompatiblearray,
    initcond = '{}'
);
```

在這裡，對於任何給定的聚合呼叫，其實際的狀態型別，
就是以實際輸入型別為元素的陣列型別。這個聚合的
行為，就是將所有輸入串接成該型別的一個陣列。
（請注意：內建的聚合 `array_agg` 也提供了類似的
功能，且效能會比這個定義要來得好。）

以下是使用兩種不同的實際資料型別作為引數的輸出：

```

SELECT attrelid::regclass, array_accum(attname)
    FROM pg_attribute
    WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
    GROUP BY attrelid;

   attrelid    |              array_accum
---------------+---------------------------------------
 pg_tablespace | {spcname,spcowner,spcacl,spcoptions}
(1 row)

SELECT attrelid::regclass, array_accum(atttypid::regtype)
    FROM pg_attribute
    WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
    GROUP BY attrelid;

   attrelid    |        array_accum
---------------+---------------------------
 pg_tablespace | {name,oid,aclitem[],text[]}
(1 row)
```

一般而言，結果型別為多型的聚合函式，
其狀態型別也會是多型的，就如同上面的範例。這是必要的，
因為否則最終函式就無法合理地被宣告：它
會需要有一個多型的結果型別，卻沒有任何多型的引數
型別，而 `CREATE FUNCTION` 會以「結果型別無法從
呼叫中推導出」為由拒絕這樣的宣告。但有時候，
使用多型狀態型別並不方便。最常見的情況，
是聚合支援函式要以 C 撰寫，且
狀態型別應該宣告為 `internal`，因為它
沒有對應的 SQL 層級型別。為了處理這種情況，可以
將最終函式宣告為，接受額外的「虛設（dummy）」引數，
這些引數與聚合的輸入引數相符。這類虛設引數
永遠會以 null 值的形式傳遞，因為呼叫最終函式時，
並沒有可用的特定值。它們唯一的用途，是讓
多型最終函式的結果型別，能與聚合的輸入
型別建立關聯。舉例來說，內建的
聚合 `array_agg` 的定義，等同於：

```

CREATE FUNCTION array_agg_transfn(internal, anynonarray)
  RETURNS internal ...;
CREATE FUNCTION array_agg_finalfn(internal, anynonarray)
  RETURNS anyarray ...;

CREATE AGGREGATE array_agg (anynonarray)
(
    sfunc = array_agg_transfn,
    stype = internal,
    finalfunc = array_agg_finalfn,
    finalfunc_extra
);
```

在這裡，`finalfunc_extra` 選項指定了，除了狀態值之外，
最終函式還會接收與聚合的輸入引數相對應的
額外虛設引數。額外的
`anynonarray` 引數，讓
`array_agg_finalfn` 的宣告得以成立。

可以透過將聚合函式的最後一個引數宣告為
`VARIADIC` 陣列，讓該聚合函式能接受數量不定的引數，
其做法與一般函式大致相同；請參閱
[36.5.6 節](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)。聚合的轉換
函式，其最後一個引數必須是相同的陣列型別。該
轉換函式通常也會被標記為 `VARIADIC`，
但這並非嚴格必要。

### 注意

可變引數聚合，與 `ORDER BY` 選項
（請參閱[4.2.7 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)）搭配使用時，
很容易被誤用，因為剖析器無法判斷，在這種組合中，
所給定的實際引數數量是否有誤。請記得，
`ORDER BY` 右邊的所有內容，都是排序鍵，而不是
聚合的引數。舉例來說，在

```

SELECT myaggregate(a ORDER BY a, b, c) FROM ...
```

中，剖析器會將這解讀為單一個聚合函式引數，加上
三個排序鍵。然而，使用者原本的意圖可能是

```

SELECT myaggregate(a, b, c ORDER BY a) FROM ...
```

若 `myaggregate` 是可變引數的，這兩種呼叫
都可能完全有效。

基於同樣的原因，在建立名稱相同、
一般引數數量不同的聚合函式之前，最好三思。

<a id="XAGGR-ORDERED-SET-AGGREGATES"></a>

### 36.12.3. 有序集合聚合 [#](#XAGGR-ORDERED-SET-AGGREGATES)

<a id="id-1.8.3.15.14.2"></a>

我們到目前為止所描述的聚合，都是「一般」
聚合。PostgreSQL 也
支援*有序集合聚合（ordered-set aggregate）*，它在兩個
關鍵方面與一般聚合不同。首先，除了每一列輸入
都會求值一次的一般聚合引數之外，
有序集合聚合還可以擁有「直接（direct）」引數，這種引數
每次聚合運算只會求值一次。其次，一般
聚合引數的語法，明確為它們指定了排序方式。
有序集合聚合通常用來實作依賴於特定資料列
順序的計算，例如排名或百分位數，因此排序方式
是任何呼叫都必須具備的要件。舉例來說，內建的
`percentile_disc` 定義，等同於：

```

CREATE FUNCTION ordered_set_transition(internal, anyelement)
  RETURNS internal ...;
CREATE FUNCTION percentile_disc_final(internal, float8, anyelement)
  RETURNS anyelement ...;

CREATE AGGREGATE percentile_disc (float8 ORDER BY anyelement)
(
    sfunc = ordered_set_transition,
    stype = internal,
    finalfunc = percentile_disc_final,
    finalfunc_extra
);
```

這個聚合接受一個 `float8` 直接引數（百分位數
比例），以及一個可以是任何可排序資料型別的聚合輸入。
它可以像這樣用來取得家庭收入的中位數：

```

SELECT percentile_disc(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_disc
-----------------
           50489
```

在這裡，`0.5` 是一個直接引數；若百分位數
比例是一個在各列之間變動的值，那就沒有意義了。

與一般聚合不同的是，有序集合聚合輸入資料列的排序，
*不是*在幕後完成的，
而是聚合支援函式的責任。
典型的實作做法，是在聚合的狀態值中，保留一個指向
「tuplesort」物件的參照，將傳入的
資料列餵給該物件，然後在最終函式中完成排序並
讀出資料。這種設計讓
最終函式能執行一些特殊操作，例如在要排序的資料中，
注入額外的「假設（hypothetical）」資料列。
一般聚合通常可以用以 PL/pgSQL 或其他
PL 語言撰寫的支援函式來實作，
但有序集合聚合通常必須以 C 撰寫，因為
它們的狀態值無法定義為任何 SQL 資料型別。
（在上面的範例中，請注意狀態值被宣告為
`internal` 型別 — 這是常見的做法。）
此外，由於排序是由最終函式執行的，之後就不可能
再次執行轉換函式，繼續加入輸入資料列。這表示
最終函式不是 `READ_ONLY`；
必須在 [`CREATE AGGREGATE`](../../reference/sql-commands/sql-createaggregate.md)
中將其宣告為 `READ_WRITE`，或者，若額外的最終函式
呼叫有可能利用已排序好的狀態，
則宣告為 `SHAREABLE`。

有序集合聚合的狀態轉換函式，會接收
目前的狀態值，以及每一列的聚合輸入值，
並傳回更新後的狀態值。這與一般聚合的
定義相同，但請注意，直接
引數（若有的話）不會被提供。最終函式會接收
最後的狀態值、直接引數的值（若有的話），
以及（若指定了 `finalfunc_extra`）對應於聚合輸入的
null 值。與一般
聚合一樣，`finalfunc_extra` 只有在該
聚合是多型的情況下才真正有用；此時就需要額外的虛設引數，
將最終函式的結果型別，與聚合的輸入
型別建立關聯。

目前，有序集合聚合無法作為視窗函式使用，
因此也不需要它們支援移動式聚合模式。

<a id="XAGGR-PARTIAL-AGGREGATES"></a>

### 36.12.4. 部分聚合 [#](#XAGGR-PARTIAL-AGGREGATES)

<a id="id-1.8.3.15.15.2"></a>

聚合函式可以選擇性地支援*部分
聚合（partial aggregation）*。部分聚合的概念，是分別對輸入資料的
不同子集，獨立執行聚合的狀態轉換函式，
接著再合併這些子集所產生的狀態值，
以產生出如同在單一次運算中掃描完所有輸入資料
時所會得到的相同狀態值。這種模式可以透過讓不同的
工作處理程序，掃描資料表的不同部分，來實現平行聚合。
每個工作處理程序都會產生一個部分狀態值，
最後再將這些狀態值合併，以產生最終的狀態值。
（未來，這種模式也可能用於例如合併對本機與
遠端資料表的聚合等用途；但目前尚未實作。）

為了支援部分聚合，該聚合的定義必須提供
一個*合併函式（combine function）*，它接受兩個
聚合狀態型別的值（分別代表對輸入資料列
兩個子集進行聚合的結果），並產生一個新的狀態型別的值，
代表若對這兩個資料列集合的組合進行聚合，
狀態原本應該會是什麼樣子。這兩個集合的輸入資料列，
彼此之間的相對順序為何，並未特別規定。這表示，
對於那些對輸入資料列順序敏感的聚合而言，
通常不可能定義出有用的合併函式。

舉個簡單的例子，可以透過將合併函式指定為
與其轉換函式相同的「兩者取大」或「兩者取小」比較函式，
讓 `MAX` 與 `MIN` 聚合支援部分
聚合。`SUM` 聚合則只需要一個加法函式，
作為合併函式即可。（同樣地，除非狀態值比輸入資料
型別要寬，否則這會與它們的轉換函式相同。）

合併函式的處理方式，很類似於轉換函式，只不過它
接受的第二個引數，是狀態型別的值，而不是底層輸入
型別的值。特別是，處理 null 值與 strict 函式的規則，
與轉換函式類似。此外，若聚合的定義指定了非 null 的
`initcond`，請記得，該值不僅會用作每次部分
聚合執行時的初始狀態，也會用作合併函式的
初始狀態，該函式會被呼叫，將每個部分結果
合併到這個狀態中。

若聚合的狀態型別宣告為 `internal`，
則合併函式必須負責確保，其結果是在
正確的記憶體上下文中，為聚合狀態值配置的。特別是，
這代表當第一個輸入為 `NULL` 時，
直接傳回第二個輸入是不正確的，因為該值
會位於錯誤的上下文中，存活期也不足。

當聚合的狀態型別宣告為 `internal` 時，
通常也適合讓該聚合的定義提供
*序列化函式（serialization function）*與*反序列化
函式（deserialization function）*，讓這樣的狀態值
能夠從一個處理程序複製到另一個處理程序。若沒有這些函式，
就無法執行平行聚合，未來如本機／遠端聚合等
應用，大概也同樣無法運作。

序列化函式必須接受一個
`internal` 型別的單一引數，並傳回一個 `bytea` 型別的結果，
代表打包成一整塊位元組的狀態值。
反之，反序列化函式則會反轉這個轉換。它必須
接受兩個引數，型別分別為 `bytea` 與 `internal`，並
傳回一個 `internal` 型別的結果。（第二個引數未被使用，
且永遠為零，但基於型別安全的考量，它是必要的。）
反序列化函式的結果，應該單純在
目前的記憶體上下文中配置即可，因為與合併函式的結果不同，
它並不需要長期存活。

另外值得一提的是，要讓某個聚合以平行方式執行，
該聚合本身必須被標記為 `PARALLEL SAFE`。
其支援函式上的平行安全性標記，並不會被參考。

<a id="XAGGR-SUPPORT-FUNCTIONS"></a>

### 36.12.5. 聚合的支援函式 [#](#XAGGR-SUPPORT-FUNCTIONS)

<a id="id-1.8.3.15.16.2"></a>

以 C 撰寫的函式，可以透過呼叫
`AggCheckCallContext`，偵測自己是否是被當作
聚合支援函式呼叫的，例如：

```

if (AggCheckCallContext(fcinfo, NULL))
```

之所以要檢查這一點，其中一個原因是，當它為真時，
第一個輸入必然是一個暫存的狀態值，因此可以安全地
就地修改，而不需要另外配置一份複本。
可參考 `int8inc()` 作為範例。
（雖然聚合轉換函式永遠都可以就地修改
轉換值，但通常不建議聚合最終函式這麼做；若它們這麼做，
就必須在建立該聚合時宣告這項行為。詳情請參閱
[CREATE AGGREGATE](../../reference/sql-commands/sql-createaggregate.md)。）

`AggCheckCallContext` 的第二個引數，可以用來
取得目前保存聚合狀態值的記憶體上下文。
對於希望將「展開」物件
（請參閱[36.13.1 節](xtypes.md#XTYPES-TOAST)）作為狀態值使用的轉換函式而言，
這相當有用。在第一次呼叫時，轉換函式應該傳回一個
記憶體上下文為聚合狀態上下文子項的展開物件，
接著在後續呼叫時，持續傳回同一個展開物件。可參考
`array_append()` 作為範例。（`array_append()`
並不是任何內建聚合的轉換函式，但它的撰寫方式，
使其在作為自訂聚合的轉換函式使用時，能有效率地運作。）

以 C 撰寫的聚合函式，另一個可用的支援常式，
是 `AggGetAggref`，它會傳回定義該聚合呼叫的
`Aggref` 剖析節點。這主要適用於
有序集合聚合，它們可以檢視
`Aggref` 節點的子結構，找出它們
應該實作的排序方式。相關範例可以在
PostgreSQL 原始碼中的
`orderedsetaggs.c` 中找到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xaggr.html)（原文版本：18.6；核對日期：2026-09-16）
