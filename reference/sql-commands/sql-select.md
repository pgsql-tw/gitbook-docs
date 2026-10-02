<a id="SQL-SELECT"></a><a id="id-1.9.3.172.1"></a><a id="id-1.9.3.172.2"></a><a id="id-1.9.3.172.3"></a>

## SELECT

SELECT, TABLE, WITH — 從資料表或檢視表擷取資料列

<a id="id-1.9.3.172.4"></a>

## 語法

```

[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    [ { * | expression [ [ AS ] output_name ] } [, ...] ]
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY [ ALL | DISTINCT ] grouping_element [, ...] ]
    [ HAVING condition ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF from_reference [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]

where from_item can be one of:

    [ ONLY ] table_name [ * ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
                [ TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ] ]
    [ LATERAL ] ( select ) [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    with_query_name [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] ) [ AS ] alias ( column_definition [, ...] )
    [ LATERAL ] function_name ( [ argument [, ...] ] ) AS ( column_definition [, ...] )
    [ LATERAL ] ROWS FROM( function_name ( [ argument [, ...] ] ) [ AS ( column_definition [, ...] ) ] [, ...] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    from_item join_type from_item { ON join_condition | USING ( join_column [, ...] ) [ AS join_using_alias ] }
    from_item NATURAL join_type from_item
    from_item CROSS JOIN from_item

and grouping_element can be one of:

    ( )
    expression
    ( expression [, ...] )
    ROLLUP ( { expression | ( expression [, ...] ) } [, ...] )
    CUBE ( { expression | ( expression [, ...] ) } [, ...] )
    GROUPING SETS ( grouping_element [, ...] )

and with_query is:

    with_query_name [ ( column_name [, ...] ) ] AS [ [ NOT ] MATERIALIZED ] ( select | values | insert | update | delete | merge )
        [ SEARCH { BREADTH | DEPTH } FIRST BY column_name [, ...] SET search_seq_col_name ]
        [ CYCLE column_name [, ...] SET cycle_mark_col_name [ TO cycle_mark_value DEFAULT cycle_mark_default ] USING cycle_path_col_name ]

TABLE [ ONLY ] table_name [ * ]
```

<a id="id-1.9.3.172.7"></a>

## 說明

`SELECT` 會從零個或多個資料表中擷取資料列。
`SELECT` 的一般處理方式如下：

1. `WITH` 清單中的所有查詢都會先計算。
   這些查詢實際上會作為可在 `FROM` 清單中參照的
   暫存資料表。在 `FROM` 中被參照超過一次的
   `WITH` 查詢，只會被計算一次，
   除非以 `NOT MATERIALIZED` 另行指定。
   （詳見下文[WITH 子句](sql-select.md#SQL-WITH)。）
2. `FROM` 清單中的所有元素都會被計算。
   （`FROM` 清單中的每個元素，都是一個實際或
   虛擬的資料表。）若 `FROM` 清單中指定了超過一個
   元素，它們會互相進行交叉連接（cross join）。
   （詳見下文[FROM 子句](sql-select.md#SQL-FROM)。）
3. 若指定了 `WHERE` 子句，所有不滿足
   該條件的資料列都會從輸出中剔除。（詳見下文
   [WHERE 子句](sql-select.md#SQL-WHERE)。）
4. 若指定了 `GROUP BY` 子句，
   或存在彙總函式呼叫，
   輸出會依一個或多個值相符的資料列合併為群組，
   並計算彙總函式的結果。
   若存在 `HAVING` 子句，它會剔除不滿足
   給定條件的群組。（詳見下文
   [GROUP BY 子句](sql-select.md#SQL-GROUPBY)與
   [HAVING 子句](sql-select.md#SQL-HAVING)。）
   雖然查詢輸出欄位名義上是在下一個步驟才計算，
   但它們仍可以（以名稱或序號）在
   `GROUP BY` 子句中被參照。
5. 針對每個被選取的資料列或資料列群組，
   使用 `SELECT` 輸出運算式計算出實際的輸出資料列。
   （詳見下文[SELECT 清單](sql-select.md#SQL-SELECT-LIST)。）
6. `SELECT DISTINCT` 會從結果中剔除重複的資料列。
   `SELECT DISTINCT ON` 會剔除彼此在所有指定運算式上
   都相符的重複資料列。`SELECT ALL`
   （預設值）會傳回所有候選資料列，包含重複者在內。
   （詳見下文[DISTINCT 子句](sql-select.md#SQL-DISTINCT)。）
7. 使用 `UNION`、
   `INTERSECT` 與 `EXCEPT` 運算子，
   可以將超過一個 `SELECT` 陳述式的輸出
   合併成單一結果集。
   `UNION` 運算子會傳回出現在
   任一或兩個結果集中的所有資料列。
   `INTERSECT` 運算子會傳回確實同時出現在
   兩個結果集中的所有資料列。`EXCEPT`
   運算子會傳回出現在第一個結果集、但不在第二個結果集中的
   資料列。這三種情況下，除非指定 `ALL`，
   否則都會剔除重複的資料列。可以加上贅字
   `DISTINCT` 來明確指定要剔除重複的資料列。
   請注意，此處 `DISTINCT` 是預設行為，
   即便 `ALL` 才是 `SELECT`
   本身的預設值。（詳見下文
   [UNION 子句](sql-select.md#SQL-UNION)、[INTERSECT 子句](sql-select.md#SQL-INTERSECT)與
   [EXCEPT 子句](sql-select.md#SQL-EXCEPT)。）
8. 若指定了 `ORDER BY` 子句，傳回的資料列
   會依所指定的順序排序。若未給定
   `ORDER BY`，資料列會以系統認為
   產生速度最快的順序傳回。（詳見下文
   [ORDER BY 子句](sql-select.md#SQL-ORDERBY)。）
9. 若指定了 `LIMIT`（或 `FETCH FIRST`）或 `OFFSET`
   子句，`SELECT` 陳述式只會傳回
   結果資料列的一個子集。（詳見下文[LIMIT 子句](sql-select.md#SQL-LIMIT)。）
10. 若指定了 `FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE`
    或 `FOR KEY SHARE`，
    `SELECT` 陳述式會鎖定所選取的資料列，
    以防止並行的更新。（詳見下文[鎖定子句](sql-select.md#SQL-FOR-UPDATE-SHARE)。）

你必須對 `SELECT` 命令中所用到的每個欄位都具有
`SELECT` 權限。使用 `FOR NO KEY UPDATE`、
`FOR UPDATE`、
`FOR SHARE` 或 `FOR KEY SHARE`
還需要具有 `UPDATE` 權限（至少對每個被如此選取的
資料表中的一個欄位）。

<a id="id-1.9.3.172.8"></a>

## 參數

<a id="SQL-WITH"></a>

### `WITH` 子句

`WITH` 子句可讓你指定一個或多個子查詢，並可在主查詢中以名稱參照它們。
在主查詢執行期間，這些子查詢實際上會作為暫存資料表或檢視表運作。
每個子查詢可以是 `SELECT`、`TABLE`、`VALUES`、
`INSERT`、`UPDATE`、
`DELETE` 或 `MERGE` 陳述式。
在 `WITH` 中撰寫資料修改陳述式（`INSERT`、
`UPDATE`、`DELETE` 或 `MERGE`）時，
通常會附上 `RETURNING` 子句。
構成主查詢所讀取之暫存資料表的，是 `RETURNING` 的輸出，
*而非*該陳述式所修改的底層資料表。若省略 `RETURNING`，
該陳述式仍會執行，但不會產生任何輸出，因此主查詢無法將其
當作資料表來參照。

每個 `WITH` 查詢都必須指定一個名稱（不含綱要限定）。
也可以選擇性地指定欄位名稱清單；若省略此項，
欄位名稱會從子查詢推斷而來。

若指定了 `RECURSIVE`，就能讓 `SELECT`
子查詢以名稱參照自身。這樣的子查詢必須具有下列形式

```

non_recursive_term UNION [ ALL | DISTINCT ] recursive_term
```

其中遞迴自我參照必須出現在 `UNION` 的右側。
每個查詢只允許有一個遞迴自我參照。目前不支援遞迴式的
資料修改陳述式，但你可以在資料修改陳述式中使用遞迴
`SELECT` 查詢的結果。範例請參閱
[7.8 節](../../the-sql-language/queries/queries-with.md)。

`RECURSIVE` 的另一項效果是：`WITH`
查詢不必依序排列——某個查詢可以參照清單中排在它之後的
另一個查詢。（不過，循環參照與互相遞迴目前皆未實作。）
若不使用 `RECURSIVE`，`WITH` 查詢
只能參照 `WITH` 清單中排在它之前的同層
`WITH` 查詢。

當 `WITH` 子句中有多個查詢時，`RECURSIVE`
只應寫一次，緊接在 `WITH` 之後。它會套用到
`WITH` 子句中的所有查詢，不過對於既未使用遞迴、
也未使用前向參照的查詢，並不會有任何效果。

選擇性的 `SEARCH` 子句會計算出一個*搜尋順序欄位*，
可用於將遞迴查詢的結果依廣度優先或深度優先順序排序。
所提供的欄位名稱清單，指定了用於追蹤已造訪資料列的資料列鍵值。
名為 *`search_seq_col_name`* 的欄位，會被加入
該 `WITH` 查詢的結果欄位清單中。在外層查詢中，
可以依此欄位排序，以達成相應的排序方式。範例請參閱
[7.8.2.1 節](../../the-sql-language/queries/queries-with.md#QUERIES-WITH-SEARCH)。

選擇性的 `CYCLE` 子句用於偵測遞迴查詢中的循環。
所提供的欄位名稱清單，指定了用於追蹤已造訪資料列的資料列鍵值。
名為 *`cycle_mark_col_name`* 的欄位，會被加入
該 `WITH` 查詢的結果欄位清單中。當偵測到循環時，
此欄位會被設為 *`cycle_mark_value`*，否則會被
設為 *`cycle_mark_default`*。此外，一旦偵測到循環，
遞迴聯集的處理就會停止。*`cycle_mark_value`*
與 *`cycle_mark_default`* 必須是常數，且必須能
強制轉型為共同的資料型別，該資料型別也必須具有不等於運算子。
（SQL 標準要求它們必須是布林常數或字元字串，但
PostgreSQL 並無此要求。）預設會使用
`TRUE` 與 `FALSE`（型別為
`boolean`）。此外，名為
*`cycle_path_col_name`* 的欄位，也會被加入該
`WITH` 查詢的結果欄位清單中。此欄位是內部用於
追蹤已造訪資料列的欄位。範例請參閱[7.8.2.2 節](../../the-sql-language/queries/queries-with.md#QUERIES-WITH-CYCLE)。

`SEARCH` 與 `CYCLE` 子句
都只適用於遞迴式的 `WITH` 查詢。
*`with_query`* 必須是兩個 `SELECT`
（或等效項目）命令的 `UNION`
（或 `UNION ALL`）（不可巢狀 `UNION`）。
若兩個子句都有使用，`SEARCH` 子句所加入的欄位，
會出現在 `CYCLE` 子句所加入的欄位之前。

主查詢與所有 `WITH` 查詢，（就概念而言）都是同時執行的。
這代表 `WITH` 中資料修改陳述式的效果，除了透過讀取其
`RETURNING` 輸出之外，查詢的其他部分都無法看見。
若有兩個這樣的資料修改陳述式嘗試修改同一筆資料列，
結果未指定。

`WITH` 查詢的一項關鍵特性是：即使主查詢參照它們超過一次，
它們在主查詢每次執行時通常也只會被求值一次。
特別是，無論主查詢是否讀取其全部或任何輸出，
資料修改陳述式都保證只會被執行一次、且只執行一次。

不過，`WITH` 查詢可以標記為
`NOT MATERIALIZED`，以移除這項保證。在這種情況下，
`WITH` 查詢可以被折疊併入主查詢，其方式就如同它是
主查詢 `FROM` 子句中的一個單純子
`SELECT` 一樣。若主查詢對該 `WITH`
查詢的參照超過一次，這會導致重複計算；但若每次使用
都只需要 `WITH` 查詢全部輸出中的少數幾筆資料列，
`NOT MATERIALIZED` 則可透過讓兩個查詢被聯合最佳化，
帶來淨效益。若 `NOT MATERIALIZED` 被附加在
遞迴的、或非無副作用（也就是說，並非不含揮發性函式的
單純 `SELECT`）的 `WITH` 查詢上，
則會被忽略。

預設情況下，若一個無副作用的 `WITH` 查詢在主查詢的
`FROM` 子句中恰好只被使用一次，它就會被折疊併入
主查詢。這讓兩個查詢層級可以在語意上應為不可見的情況下
進行聯合最佳化。不過，可以透過將該 `WITH` 查詢
標記為 `MATERIALIZED` 來阻止這種折疊。
舉例來說，若該 `WITH` 查詢是被用作最佳化屏障，
以避免規劃器選擇不良的執行計畫，這種做法就可能有用。
v12 之前的 PostgreSQL 版本從不進行
這種折疊，因此為舊版本撰寫的查詢，可能仰賴
`WITH` 具有最佳化屏障的作用。

更多資訊請參閱[7.8 節](../../the-sql-language/queries/queries-with.md)。

<a id="SQL-FROM"></a>

### `FROM` 子句

`FROM` 子句為 `SELECT` 指定一個或多個來源資料表。
若指定了多個來源，結果就是所有來源的笛卡兒積（交叉連接）。
不過通常會（透過 `WHERE`）加上限定條件，將傳回的資料列
限縮為笛卡兒積的一小部分子集。

`FROM` 子句可以包含下列元素：

*`table_name`*
:   既有資料表或檢視表的名稱（可加上綱要限定）。
    若在資料表名稱前指定 `ONLY`，則只會掃描該資料表。
    若未指定 `ONLY`，則會掃描該資料表及其所有後代資料表
    （若有的話）。也可以選擇在資料表名稱後加上
    `*`，以明確表示包含後代資料表。

*`alias`*
:   包含此別名之 `FROM` 項目的替代名稱。使用別名
    是為了簡潔，或是為了消除自我連接（同一資料表被
    掃描多次）時的歧義。當提供別名時，它會完全隱藏
    該資料表或函式的實際名稱；舉例來說，給定
    `FROM foo AS f`，`SELECT` 其餘部分
    必須以 `f`、而非 `foo` 來參照此
    `FROM` 項目。若寫了別名，也可以寫欄位別名清單，
    為該資料表的一個或多個欄位提供替代名稱。

`TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ]`
:   *`table_name`* 之後的 `TABLESAMPLE`
    子句，表示應使用指定的
    *`sampling_method`* 來擷取該資料表中
    資料列的子集。此取樣動作會先於任何其他篩選條件
    （例如 `WHERE` 子句）套用之前進行。
    標準的 PostgreSQL 發行版包含兩種取樣方法，
    `BERNOULLI` 與 `SYSTEM`，
    其他取樣方法則可透過擴充功能安裝到資料庫中。

    `BERNOULLI` 與 `SYSTEM` 這兩種取樣方法，
    各自接受單一個 *`argument`*
    引數，代表要取樣的資料表比例，以 0 到 100 之間的
    百分比表示。此引數可以是任何 `real` 型別的運算式。
    （其他取樣方法可能接受更多或不同的引數。）
    這兩種方法都會傳回該資料表的隨機樣本，所含資料列
    約為該資料表全部資料列的指定百分比。
    `BERNOULLI` 方法會掃描整個資料表，並以指定的
    機率獨立地選取或忽略個別資料列。
    `SYSTEM` 方法則進行區塊層級的取樣，每個區塊
    都有指定的機率被選中；每個被選中區塊中的所有資料列
    都會被傳回。
    當指定的取樣百分比很小時，`SYSTEM` 方法會比
    `BERNOULLI` 方法快上許多，但由於群聚效應，
    它傳回的資料表樣本隨機性可能較低。

    選擇性的 `REPEATABLE` 子句，指定了取樣方法
    在產生亂數時要使用的 *`seed`* 數字或
    運算式。種子值可以是任何非空值的浮點數。若兩個查詢
    指定了相同的種子值與 *`argument`* 值，
    只要該資料表在期間未被變更，就會選取相同的資料表樣本。
    但不同的種子值通常會產生不同的樣本。
    若未給定 `REPEATABLE`，則每次查詢都會依據
    系統產生的種子值，選取一個新的隨機樣本。
    請注意，某些外掛的取樣方法不接受
    `REPEATABLE`，每次使用時一律會產生新的樣本。

*`select`*
:   子 `SELECT` 可以出現在 `FROM`
    子句中。其效果就如同其輸出，在這一次
    `SELECT` 命令執行期間，被建立為一個暫存資料表。
    請注意，子 `SELECT` 必須以括號括住，
    且可以像資料表一樣提供別名。這裡也可以使用
    [`VALUES`](sql-values.md) 命令。

*`with_query_name`*
:   `WITH` 查詢是透過寫出其名稱來參照，
    就如同該查詢的名稱是資料表名稱一般。
    （事實上，就主查詢而言，`WITH` 查詢會隱藏
    任何同名的實際資料表。如有需要，你可以透過為
    資料表名稱加上綱要限定，來參照同名的實際資料表。）
    可以像資料表一樣提供別名。

*`function_name`*
:   函式呼叫可以出現在 `FROM` 子句中。
    （這對於傳回結果集的函式特別有用，但任何函式
    都可以使用。）其效果就如同該函式的輸出，
    在這一次 `SELECT` 命令執行期間，被建立為一個
    暫存資料表。若函式的結果型別是複合型別（包括具有
    多個 `OUT` 參數的函式），每個屬性都會成為
    這個隱含資料表中的一個獨立欄位。

    當函式呼叫加上選擇性的 `WITH ORDINALITY`
    子句時，會在函式的結果欄位之後附加一個
    `bigint` 型別的額外欄位。此欄位會對函式
    結果集的資料列編號，從 1 開始。此欄位預設命名為
    `ordinality`。

    可以像資料表一樣提供別名。若寫了別名，
    也可以寫欄位別名清單，為函式複合傳回型別的
    一個或多個屬性（包含序數欄位，若存在的話）提供
    替代名稱。

    可以用 `ROWS FROM( ... )` 將多個函式呼叫
    組合成單一個 `FROM` 子句項目。這種項目的輸出，
    是先取每個函式的第一筆資料列串接、再取每個函式的
    第二筆資料列串接，依此類推。若某些函式產生的資料列
    比其他函式少，缺少的資料會以空值代入，因此傳回的
    資料列總數，一律會等於產生最多資料列之函式的資料列數。

    若函式被定義為傳回 `record` 資料型別，
    則必須有別名或 `AS` 關鍵字，並接著以
    `( column_name data_type [, ...
    ])` 的形式寫出欄位定義清單。欄位定義清單
    必須與函式實際傳回的欄位數量與型別相符。

    使用 `ROWS FROM( ... )` 語法時，若其中一個函式
    需要欄位定義清單，建議將欄位定義清單放在
    `ROWS FROM( ... )` 內、該函式呼叫之後。
    只有在只有單一函式、且沒有 `WITH ORDINALITY`
    子句的情況下，才能將欄位定義清單放在
    `ROWS FROM( ... )` 結構之後。

    若要將 `ORDINALITY` 與欄位定義清單一起使用，
    你必須使用 `ROWS FROM( ... )` 語法，並將
    欄位定義清單放在 `ROWS FROM( ... )` 內。

*`join_type`*
:   下列其中之一

    * `[ INNER ] JOIN`
    * `LEFT [ OUTER ] JOIN`
    * `RIGHT [ OUTER ] JOIN`
    * `FULL [ OUTER ] JOIN`

    對於 `INNER` 與 `OUTER` 連接型別，
    必須指定連接條件，即以下三者恰好其中之一：
    `ON join_condition`、
    `USING (join_column [, ...])`，
    或 `NATURAL`。其意義詳見下文。

    `JOIN` 子句會結合兩個 `FROM`
    項目——為方便起見，我們將其稱為「資料表」，
    儘管實際上它們可以是任何型別的 `FROM` 項目。
    如有需要，可使用括號來決定巢狀順序。
    在沒有括號的情況下，`JOIN` 會由左至右巢狀組合。
    無論如何，`JOIN` 的結合力都強於分隔
    `FROM` 清單項目的逗號。
    所有的 `JOIN` 選項都只是為了書寫方便，
    因為它們做不到任何以單純的 `FROM` 與
    `WHERE` 無法做到的事。

    `LEFT OUTER JOIN` 會傳回符合條件的笛卡兒積中
    的所有資料列（也就是所有通過其連接條件的合併資料列），
    再加上左側資料表中，找不到任何通過連接條件之右側資料列的
    每一筆資料列各一份。這些左側資料列會透過在右側欄位
    填入空值，延伸到合併資料表的完整寬度。請注意，
    在決定哪些資料列有相符項目時，只會考慮 `JOIN`
    子句本身的條件。外部條件則是之後才套用。

    相對地，`RIGHT OUTER JOIN` 會傳回所有合併後的
    資料列，再加上每一筆未相符的右側資料列各一列
    （左側以空值延伸）。這只是為了書寫方便，因為你
    只要交換左右兩個資料表，就能把它轉換成
    `LEFT OUTER JOIN`。

    `FULL OUTER JOIN` 會傳回所有合併後的資料列，
    再加上每一筆未相符的左側資料列各一列（右側以空值延伸），
    再加上每一筆未相符的右側資料列各一列（左側以空值延伸）。

`ON join_condition`
:   *`join_condition`* 是一個結果為
    `boolean` 型別值的運算式（類似 `WHERE`
    子句），用於指定連接中哪些資料列會被視為相符。

`USING ( join_column [, ...] ) [ AS join_using_alias ]`
:   形式為 `USING ( a, b, ... )` 的子句，
    是 `ON left_table.a = right_table.a AND
    left_table.b = right_table.b ...` 的簡寫。
    此外，`USING` 意味著每一對相等欄位中，
   連接輸出中只會包含其中一個，而非兩個都包含。

    若指定了 *`join_using_alias`* 名稱，
    它會為連接欄位提供一個資料表別名。透過此名稱，
    只有 `USING` 子句中列出的連接欄位可以被存取。
    與一般的 *`alias`* 不同，這不會讓查詢
    其餘部分看不到被連接資料表的名稱。同樣與一般的
    *`alias`* 不同，你不能寫欄位別名清單——
   連接欄位的輸出名稱，會與它們在 `USING`
    清單中出現的名稱相同。

`NATURAL`
:   `NATURAL` 是 `USING` 清單的簡寫，
    會列出兩個資料表中名稱相符的所有欄位。若沒有
    相同名稱的欄位，`NATURAL` 就相當於
    `ON TRUE`。

`CROSS JOIN`
:   `CROSS JOIN` 相當於 `INNER JOIN ON
    (TRUE)`，也就是說，不會因限定條件而移除任何資料列。
    它們會產生單純的笛卡兒積，與在 `FROM` 頂層
    列出兩個資料表所得到的結果相同，但若有連接條件，
    則會受其限制。

`LATERAL`
:   `LATERAL` 關鍵字可以放在子 `SELECT`
    `FROM` 項目之前。這讓子 `SELECT`
    能夠參照 `FROM` 清單中排在它之前的
    `FROM` 項目的欄位。（若不使用
    `LATERAL`，每個子 `SELECT` 都會
    被獨立求值，因此無法交叉參照任何其他
    `FROM` 項目。）

    `LATERAL` 也可以放在函式呼叫的
    `FROM` 項目之前，但在這種情況下它只是個
    無作用的贅字，因為函式運算式本來就可以參照
    更早的 `FROM` 項目。

    `LATERAL` 項目可以出現在 `FROM`
    清單的頂層，也可以出現在 `JOIN` 樹狀結構內。
    在後者的情況下，它也可以參照位於某個 `JOIN` 左側的任何項目，前提是該 LATERAL 項目本身位於這個 JOIN 的右側。

    當某個 `FROM` 項目包含 `LATERAL`
    交叉參照時，求值方式如下：針對提供該交叉參照欄位的
    `FROM` 項目的每一筆資料列，或針對提供這些欄位的
    多個 `FROM` 項目的每一組資料列，都會使用
    該資料列（或資料列組）的欄位值來對 `LATERAL`
    項目求值。所得到的資料列，會照常與計算它們所依據的
    資料列進行連接。針對欄位來源資料表的每一筆資料列
    或每一組資料列，都會重複此過程。

    欄位來源資料表必須以 `INNER` 或
    `LEFT` 連接方式與 `LATERAL` 項目結合，
    否則就不會有一組定義明確的資料列，可用來計算
    `LATERAL` 項目的每一組資料列。因此，
    雖然像 `X RIGHT JOIN
    LATERAL Y` 這樣的結構在語法上是有效的，
    但實際上並不允許 *`Y`* 參照
    *`X`*。

<a id="SQL-WHERE"></a>

### `WHERE` 子句


選擇性的 `WHERE` 子句，其一般形式為

```

WHERE condition
```

其中 *`condition`* 是任何求值結果為
`boolean` 型別的運算式。任何不滿足此條件的資料列，
都會從輸出中被剔除。若以實際的資料列值代入所有變數參照後，
運算式回傳 true，則該資料列即滿足此條件。

<a id="SQL-GROUPBY"></a>

### `GROUP BY` 子句

選擇性的 `GROUP BY` 子句，其一般形式為

```

GROUP BY [ ALL | DISTINCT ] grouping_element [, ...]
```

`GROUP BY` 會將所有在分組運算式上具有相同值的
選取資料列，濃縮成單一資料列。*`grouping_element`*
內所使用的 *`expression`*，可以是輸入欄位名稱、
輸出欄位（`SELECT` 清單項目）的名稱或序號，
或是由輸入欄位值組成的任意運算式。若有歧義，
`GROUP BY` 中的名稱會被解讀為輸入欄位名稱，
而非輸出欄位名稱。

若分組元素中存在 `GROUPING SETS`、`ROLLUP`
或 `CUBE` 之一，則整個 `GROUP BY`
子句會定義若干個獨立的*分組集合（`grouping sets`）*。
其效果等同於在多個子查詢之間建構 `UNION ALL`，
每個子查詢各以其中一個分組集合作為其
`GROUP BY` 子句。選擇性的 `DISTINCT`
子句會在處理之前先移除重複的集合；它*不會*把
`UNION ALL` 轉換成 `UNION DISTINCT`。
關於分組集合處理方式的更多細節，請參閱
[7.2.4 節](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-GROUPING-SETS)。

若有使用彙總函式，會針對組成每個群組的所有資料列進行計算，
為每個群組產生一個獨立的值。（若存在彙總函式，但沒有
`GROUP BY` 子句，則該查詢會被視為只有一個群組，
由所有被選取的資料列組成。）
可以為彙總函式呼叫加上 `FILTER` 子句，
進一步篩選餵入每個彙總函式的資料列集合；詳見
[4.2.7 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)。
當存在 `FILTER` 子句時，只有符合該子句的資料列，
才會被納入該彙總函式的輸入中。

當存在 `GROUP BY`，或存在任何彙總函式時，
`SELECT` 清單運算式參照未分組欄位是無效的，
除非該參照是在彙總函式內，或是該未分組欄位函數相依於
分組欄位，因為否則對於某個未分組欄位，
就會有超過一個可能傳回的值。若分組欄位（或其子集）
是包含該未分組欄位之資料表的主鍵，則存在函數相依關係。

請記住，所有彙總函式都會先求值，才會對
`HAVING` 子句或 `SELECT` 清單中的任何
「純量」運算式求值。這代表，舉例來說，無法使用
`CASE` 運算式來跳過某個彙總函式的求值；詳見
[4.2.14 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-EXPRESS-EVAL)。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 與 `FOR KEY SHARE` 皆無法與
`GROUP BY` 一併指定。

<a id="SQL-HAVING"></a>

### `HAVING` 子句

選擇性的 `HAVING` 子句，其一般形式為

```

HAVING condition
```

其中 *`condition`* 與 `WHERE` 子句中
所指定者相同。

`HAVING` 會剔除不滿足該條件的群組資料列。
`HAVING` 與 `WHERE` 不同：`WHERE`
是在套用 `GROUP
BY` 之前，篩選個別資料列；而 `HAVING`
則是篩選由 `GROUP BY` 所建立的群組資料列。
*`condition`* 中所參照的每個欄位，都必須
明確地參照某個分組欄位，除非該參照是出現在彙總函式內，
或該未分組欄位函數相依於分組欄位。

即使沒有 `GROUP BY` 子句，`HAVING`
的存在仍會使查詢變成一個分組查詢。這與查詢含有彙總函式
但沒有 `GROUP BY` 子句時的情況相同。所有被選取的
資料列會被視為組成單一群組，且 `SELECT` 清單與
`HAVING` 子句只能在彙總函式內參照資料表欄位。
若 `HAVING` 條件為真，這樣的查詢會產生單一資料列；
若不為真，則產生零筆資料列。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 與 `FOR KEY SHARE` 皆無法與
`HAVING` 一併指定。

<a id="SQL-WINDOW"></a>

### `WINDOW` 子句


選擇性的 `WINDOW` 子句，其一般形式為

```

WINDOW window_name AS ( window_definition ) [, ...]
```

其中 *`window_name`* 是一個名稱，
可以在 `OVER` 子句或後續的視窗定義中被參照，
而 *`window_definition`* 則是

```

[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

若指定了 *`existing_window_name`*，
它必須參照 `WINDOW` 清單中較早的項目；
新視窗會複製該項目的分割子句，以及其排序子句（若有的話）。
在這種情況下，新視窗不能指定自己的 `PARTITION BY`
子句，且只有在被複製的視窗沒有 `ORDER BY` 時，
才能指定 ORDER BY。新視窗一律使用自己的框架子句；
被複製的視窗則不得指定框架子句。

`PARTITION BY` 清單中的元素，解讀方式與
[`GROUP BY`](sql-select.md#SQL-GROUPBY) 子句中的元素大致相同，
差別在於它們一律是單純的運算式，絕不會是輸出欄位的
名稱或序號。另一個差異是，這些運算式可以包含彙總函式呼叫，
這在一般的 `GROUP BY` 子句中是不允許的。之所以在此允許，
是因為視窗化是在分組與彙總之後才進行的。

同樣地，`ORDER BY` 清單中的元素，解讀方式
與陳述式層級 [`ORDER BY`](sql-select.md#SQL-ORDERBY) 子句中的元素
大致相同，差別在於這些運算式一律被視為單純的運算式，
絕不會是輸出欄位的名稱或序號。

選擇性的 *`frame_clause`*，為依賴框架
（並非所有視窗函式都依賴框架）的視窗函式，定義了
*視窗框架*。視窗框架是查詢中每一筆資料列（稱為
*目前資料列*）所對應的一組相關資料列。
*`frame_clause`* 可以是下列其中之一

```

{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
```

其中 *`frame_start`*
與 *`frame_end`* 可以是下列其中之一

```

UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
```

而 *`frame_exclusion`* 可以是下列其中之一

```

EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

若省略 *`frame_end`*，預設為 `CURRENT
ROW`。限制條件是：*`frame_start`*
不能是 `UNBOUNDED FOLLOWING`，
*`frame_end`* 不能是 `UNBOUNDED PRECEDING`，
且 *`frame_end`* 所選的選項，在上述
*`frame_start`* 與 *`frame_end`*
選項清單中，不能排在 *`frame_start`* 所選選項的
更前面——舉例來說，不允許
`RANGE BETWEEN CURRENT ROW AND offset
PRECEDING`。

預設的框架選項是 `RANGE UNBOUNDED PRECEDING`，
與 `RANGE BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW` 相同；它會將框架設為從該分割的開頭，
一直到目前資料列最後一個*同儕（peer）*（也就是視窗的
`ORDER BY` 子句認定與目前資料列等效的資料列；
若沒有 `ORDER BY`，則所有資料列皆互為同儕）
為止的所有資料列。一般而言，`UNBOUNDED PRECEDING`
代表框架從該分割的第一筆資料列開始，同樣地，
`UNBOUNDED FOLLOWING` 代表框架在該分割的最後一筆
資料列結束，無論是 `RANGE`、`ROWS`
還是 `GROUPS` 模式皆然。
在 `ROWS` 模式下，`CURRENT ROW` 代表
框架以目前資料列作為起點或終點；但在 `RANGE`
或 `GROUPS` 模式下，則代表框架以目前資料列在
`ORDER BY` 排序中的第一個或最後一個同儕
作為起點或終點。*`offset`* `PRECEDING`
與 *`offset`* `FOLLOWING` 選項的意義，
會依框架模式而有所不同。在 `ROWS` 模式下，
*`offset`* 是一個整數，表示框架的起點或終點，
是在目前資料列之前或之後多少筆資料列。
在 `GROUPS` 模式下，*`offset`*
是一個整數，表示框架的起點或終點，是在目前資料列的
同儕群組之前或之後多少個同儕群組，其中*同儕群組*
是依視窗的 `ORDER BY` 子句判定為等效的一組資料列。
在 `RANGE` 模式下，使用 *`offset`*
選項時，視窗定義中必須恰好有一個 `ORDER BY` 欄位。
此時，框架會包含那些排序欄位值與目前資料列排序欄位值
相差不超過 *`offset`*（`PRECEDING`
為較小、`FOLLOWING` 為較大）的資料列。在這些情況下，
*`offset`* 運算式的資料型別，取決於排序欄位的
資料型別。對於數值型的排序欄位，通常與排序欄位的型別相同，
但對於日期時間型的排序欄位，則是 `interval` 型別。
在以上所有情況中，*`offset`* 的值都必須非空值
且非負值。此外，雖然 *`offset`* 不一定要是
單純的常數，但它不能包含變數、彙總函式，或視窗函式。

*`frame_exclusion`* 選項可將目前資料列周圍的
資料列排除於框架之外，即使依框架起點與終點選項，
它們原本會被包含在內。`EXCLUDE CURRENT ROW`
會將目前資料列排除於框架之外。
`EXCLUDE GROUP` 會將目前資料列及其排序同儕
排除於框架之外。
`EXCLUDE TIES` 會將目前資料列的任何同儕排除於
框架之外，但不包括目前資料列本身。
`EXCLUDE NO OTHERS` 只是明確指定不排除目前資料列
或其同儕的預設行為。

請留意，若 `ORDER BY` 排序無法唯一地排序資料列，
`ROWS` 模式可能會產生無法預期的結果。`RANGE`
與 `GROUPS` 模式則設計為確保在 `ORDER BY`
排序中互為同儕的資料列會被一致地處理：給定同儕群組的
所有資料列，要嘛全部都在框架內，要嘛全部都被排除在框架外。

`WINDOW` 子句的目的，是為查詢的
[`SELECT` 清單](sql-select.md#SQL-SELECT-LIST)或
[`ORDER BY`](sql-select.md#SQL-ORDERBY) 子句中出現的
*視窗函式*指定行為。這些函式可以在其
`OVER` 子句中以名稱參照 `WINDOW` 子句項目。
不過，`WINDOW` 子句項目不一定要在任何地方被參照；
若查詢中未使用它，就會被單純忽略。即使完全不使用
`WINDOW` 子句，也可以使用視窗函式，因為視窗函式呼叫
可以直接在其 `OVER` 子句中指定視窗定義。不過，
當同一個視窗定義需要被超過一個視窗函式使用時，
`WINDOW` 子句可以省去重複輸入的麻煩。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 與 `FOR KEY SHARE` 皆無法與
`WINDOW` 一併指定。

視窗函式的詳細說明，請參閱
[3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)、
[4.2.8 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)，以及
[7.2.5 節](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-WINDOW)。

<a id="SQL-SELECT-LIST"></a>

### `SELECT` 清單


`SELECT` 清單（位於 `SELECT` 與 `FROM`
關鍵字之間）指定了構成 `SELECT` 陳述式輸出資料列的
運算式。這些運算式可以（也通常會）參照
`FROM` 子句中計算出來的欄位。

如同資料表一樣，`SELECT` 的每個輸出欄位都有一個名稱。
在單純的 `SELECT` 中，此名稱只用於為顯示的欄位加上標籤，
但當該 `SELECT` 是較大查詢的子查詢時，較大的查詢
會將此名稱視為該子查詢所產生虛擬資料表的欄位名稱。
若要指定輸出欄位所要使用的名稱，請在該欄位的運算式之後
寫上 `AS` *`output_name`*。
（你可以省略 `AS`，但僅限於所要的輸出名稱
不與任何 PostgreSQL 關鍵字相符時（見
[附錄 C](../../appendixes/sql-keywords-appendix/README.md)）。為了防範未來可能新增的
關鍵字，建議一律寫出 `AS`，或以雙引號括住輸出名稱。）
若你未指定欄位名稱，PostgreSQL 會自動
選擇一個名稱。若該欄位的運算式是單純的欄位參照，
所選的名稱就會與該欄位的名稱相同。在較複雜的情況下，
可能會使用函式或型別名稱，或者系統可能會退而使用
像 `?column?` 這樣自動產生的名稱。

輸出欄位的名稱可以用於在 `ORDER BY` 與
`GROUP BY` 子句中參照該欄位的值，但不能用於
`WHERE` 或 `HAVING` 子句中；在那些子句中，
你必須改為寫出完整的運算式。

也可以在輸出清單中寫 `*`，作為所有選取資料列
所有欄位的簡寫，以取代運算式。你也可以寫
`table_name.*`，作為僅來自該資料表之欄位的簡寫。
在這些情況下，無法以 `AS` 指定新名稱；
輸出欄位名稱會與資料表欄位的名稱相同。

依照 SQL 標準，輸出清單中的運算式應在套用
`DISTINCT`、`ORDER
BY` 或 `LIMIT` 之前計算。當使用
`DISTINCT` 時，這顯然是必要的，否則就不清楚
究竟是對哪些值做去重複。不過，在許多情況下，
若輸出運算式是在 `ORDER
BY` 與 `LIMIT` 之後才計算，會比較方便；
特別是當輸出清單中包含任何揮發性或成本較高的函式時。
在這種行為下，函式求值的順序會更符合直覺，
也不會出現對應到從未出現在輸出中之資料列的求值動作。
只要這些運算式未在 `DISTINCT`、`ORDER BY`
或 `GROUP BY` 中被參照，PostgreSQL 實際上
就會在排序與限制之後才計算輸出運算式。（舉一個反例，
`SELECT
f(x) FROM tab ORDER BY 1` 顯然必須在排序之前
先計算 `f(x)`。）含有傳回集合函式的輸出運算式，
實際上會在排序之後、限制之前計算，如此一來
`LIMIT` 才能有效截斷傳回集合函式的輸出。

<a id="SQL-SELECT-LIST-NOTE"></a>

### 注意

9.6 版之前的 PostgreSQL，並未對輸出運算式的
求值時機相對於排序與限制之先後順序提供任何保證；
這取決於所選取查詢計畫的形式。

<a id="SQL-DISTINCT"></a>

### `DISTINCT` 子句


若指定了 `SELECT DISTINCT`，結果集中所有重複的資料列
都會被移除（每組重複的資料列中，只保留一筆）。
`SELECT ALL` 指定相反的行為：保留所有資料列；
這是預設值。

`SELECT DISTINCT ON ( expression [, ...] )`
只會保留每組給定運算式求值結果相等之資料列中的第一筆。
`DISTINCT ON` 運算式的解讀規則，與
`ORDER BY`（見上文）相同。請注意，除非使用
`ORDER
BY` 確保所要的資料列排在最前面，否則每組資料列的
「第一筆」是無法預期的。舉例來說：

```

SELECT DISTINCT ON (location) location, time, report
    FROM weather_reports
    ORDER BY location, time DESC;
```

會擷取每個地點最近一次的天氣報告。但若我們沒有使用
`ORDER BY` 強制讓每個地點的 time 值以遞減順序排列，
我們每個地點取得的報告，其時間就會是無法預期的。

`DISTINCT ON` 運算式必須與最左側的
`ORDER BY` 運算式相符。`ORDER BY` 子句
通常還會包含其他運算式，用來決定每個
`DISTINCT ON` 群組內資料列所要的優先順序。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 與 `FOR KEY SHARE` 皆無法與
`DISTINCT` 一併指定。

<a id="SQL-UNION"></a>

### `UNION` 子句

`UNION` 子句的一般形式如下：

```

select_statement UNION [ ALL | DISTINCT ] select_statement
```

*`select_statement`* 是任何不含
`ORDER
BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 或 `FOR KEY SHARE` 子句的
`SELECT` 陳述式。
（若以括號括住某個子運算式，`ORDER BY` 與
`LIMIT` 可以附加在該子運算式上。若未加括號，
這些子句會被視為套用於 `UNION` 的結果，
而非其右側的輸入運算式。）

`UNION` 運算子會計算所涉及 `SELECT`
陳述式所傳回資料列的集合聯集。若某資料列出現在
兩個結果集中至少一個裡面，它就會出現在這兩個結果集
的聯集中。作為 `UNION` 直接運算元的兩個
`SELECT` 陳述式，必須產生相同數量的欄位，
且對應的欄位必須具有相容的資料型別。

除非指定了 `ALL` 選項，否則 `UNION`
的結果不會包含任何重複的資料列。`ALL`
會防止重複資料列被移除。（因此，`UNION ALL`
通常會比 `UNION` 快上不少；可以的話請使用
`ALL`。）可以寫 `DISTINCT` 來明確指定
消除重複資料列的預設行為。

同一個 `SELECT` 陳述式中的多個 `UNION`
運算子，除非以括號另行指示，否則會由左至右求值。

目前，無論是對 `UNION` 的結果，還是對
`UNION` 的任何輸入，都無法指定
`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或
`FOR KEY SHARE`。

<a id="SQL-INTERSECT"></a>

### `INTERSECT` 子句


`INTERSECT` 子句的一般形式如下：

```

select_statement INTERSECT [ ALL | DISTINCT ] select_statement
```

*`select_statement`* 是任何不含
`ORDER
BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 或 `FOR KEY SHARE` 子句的
`SELECT` 陳述式。

`INTERSECT` 運算子會計算所涉及 `SELECT`
陳述式所傳回資料列的集合交集。若某資料列同時出現在
兩個結果集中，它就會出現在這兩個結果集的交集中。

除非指定了 `ALL` 選項，否則 `INTERSECT`
的結果不會包含任何重複的資料列。使用 `ALL` 時，
若某資料列在左側資料表中有 *`m`* 筆重複，
在右側資料表中有 *`n`* 筆重複，則它會在結果集中
出現 min(*`m`*,*`n`*) 次。可以寫
`DISTINCT` 來明確指定消除重複資料列的預設行為。

同一個 `SELECT` 陳述式中的多個 `INTERSECT`
運算子，除非括號另有規定，否則會由左至右求值。
`INTERSECT` 的結合力比 `UNION` 強。
也就是說，`A UNION B INTERSECT
C` 會被解讀為 `A UNION (B INTERSECT
C)`。

目前，無論是對 `INTERSECT` 的結果，還是對
`INTERSECT` 的任何輸入，都無法指定
`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或
`FOR KEY SHARE`。

<a id="SQL-EXCEPT"></a>

### `EXCEPT` 子句

`EXCEPT` 子句的一般形式如下：

```

select_statement EXCEPT [ ALL | DISTINCT ] select_statement
```

*`select_statement`* 是任何不含
`ORDER
BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、
`FOR SHARE` 或 `FOR KEY SHARE` 子句的
`SELECT` 陳述式。

`EXCEPT` 運算子會計算出現在左側 `SELECT`
陳述式結果中、但不出現在右側結果中的資料列集合。

除非指定了 `ALL` 選項，否則 `EXCEPT`
的結果不會包含任何重複的資料列。使用 `ALL` 時，
若某資料列在左側查詢結果中有 *`m`* 筆重複，
在右側查詢結果中有 *`n`* 筆重複，則它會在結果集中
出現 max(*`m`*-*`n`*,0) 次。可以寫
`DISTINCT` 來明確指定消除重複資料列的預設行為。

同一個 `SELECT` 陳述式中的多個 `EXCEPT`
運算子，除非括號另有規定，否則會由左至右求值。
`EXCEPT` 的結合力與 `UNION` 相同。

目前，無論是對 `EXCEPT` 的結果，還是對
`EXCEPT` 的任何輸入，都無法指定
`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或
`FOR KEY SHARE`。

<a id="SQL-ORDERBY"></a>

### `ORDER BY` 子句


選擇性的 `ORDER BY` 子句，其一般形式如下：

```

ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...]
```

`ORDER BY` 子句會使結果資料列依照所指定的運算式排序。
若兩筆資料列依最左側的運算式判定為相等，
就會依下一個運算式比較，依此類推。若依所有指定的運算式
判定皆為相等，則它們會以取決於實作方式的順序傳回。

每個 *`expression`* 可以是輸出欄位
（`SELECT` 清單項目）的名稱或序號，
也可以是由輸入欄位值組成的任意運算式。

序號指的是輸出欄位（由左至右）的序數位置。此功能讓你
可以依據沒有唯一名稱的欄位來定義排序方式。這其實
絕非必要，因為永遠都可以用 `AS` 子句為
輸出欄位指定名稱。

在 `ORDER BY` 子句中，也可以使用任意運算式，
包括未出現在 `SELECT` 輸出清單中的欄位。
因此，下列陳述式是有效的：

```

SELECT name FROM distributors ORDER BY code;
```

此功能的一項限制是：套用於 `UNION`、
`INTERSECT` 或 `EXCEPT` 子句結果的
`ORDER BY` 子句，只能指定輸出欄位的名稱或序號，
不能指定運算式。

若某個 `ORDER BY` 運算式是同時與某個輸出欄位名稱
及某個輸入欄位名稱相符的單純名稱，`ORDER BY`
會將其解讀為輸出欄位名稱。這與 `GROUP BY`
在相同情況下的選擇恰好相反。之所以有這種不一致，
是為了與 SQL 標準相容。

在 `ORDER BY` 子句中，可以選擇在任何運算式之後
加上關鍵字 `ASC`（遞增）或 `DESC`（遞減）。
若未指定，預設會假定為 `ASC`。或者，也可以在
`USING` 子句中指定特定的排序運算子名稱。
排序運算子必須是某個 B 樹運算子家族中的小於或大於成員。
`ASC` 通常等同於 `USING <`，而
`DESC` 通常等同於 `USING >`。
（不過，使用者自訂資料型別的建立者，可以明確定義
其預設排序方式，這可能對應到其他名稱的運算子。）

若指定 `NULLS LAST`，空值會排在所有非空值之後；
若指定 `NULLS FIRST`，空值會排在所有非空值之前。
若兩者皆未指定，預設行為是：當指定或隱含
`ASC` 時為 `NULLS LAST`，
指定 `DESC` 時則為 `NULLS FIRST`
（因此，預設行為就如同空值大於非空值一般）。
當指定了 `USING` 時，空值的預設排序方式，
取決於該運算子是小於運算子還是大於運算子。

請注意，排序選項只會套用於它所緊接的運算式；
舉例來說，`ORDER BY x, y DESC` 與
`ORDER BY x DESC, y DESC` 意義並不相同。

字元字串資料會依適用於被排序欄位的定序（collation）
排序。如有需要，可以在 *`expression`* 中
加入 `COLLATE` 子句來覆寫，舉例來說
`ORDER BY mycolumn COLLATE "en_US"`。
更多資訊請參閱[4.2.10 節](../../the-sql-language/sql-syntax/sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS)以及
[23.2 節](../../server-administration/charset/collation.md)。

<a id="SQL-LIMIT"></a>

### `LIMIT` 子句


`LIMIT` 子句由兩個各自獨立的子句組成：

```

LIMIT { count | ALL }
OFFSET start
```

參數 *`count`* 指定要傳回的最大資料列數，
而 *`start`* 則指定在開始傳回資料列之前
要跳過的資料列數。若兩者皆有指定，會先跳過
*`start`* 筆資料列，才開始計算要傳回的
*`count`* 筆資料列。

若 *`count`* 運算式求值結果為 NULL，
會被視為 `LIMIT ALL`，也就是不限制。若
*`start`* 求值結果為 NULL，會被視為與
`OFFSET 0` 相同。

SQL:2008 引進了另一種語法來達成相同的結果，
PostgreSQL 也支援此語法。其形式為：

```

OFFSET start { ROW | ROWS }
FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES }
```

在此語法中，標準要求 *`start`*
或 *`count`* 值必須是字面常數、參數，
或變數名稱；作為 PostgreSQL 的擴充功能，
也允許使用其他運算式，但為避免歧義，一般需要以括號括住。
若在 `FETCH` 子句中省略 *`count`*，
其預設值為 1。`WITH TIES` 選項用於
依 `ORDER BY` 子句，傳回任何與結果集最後一名
並列的額外資料列；在此情況下 `ORDER BY`
為必要項目，且不允許使用 `SKIP LOCKED`。
`ROW` 與 `ROWS`，以及
`FIRST` 與 `NEXT`，都是不影響
這些子句效果的贅字。依標準規定，若兩者同時存在，
`OFFSET` 子句必須寫在 `FETCH` 子句之前；但
PostgreSQL 較為寬鬆，允許任一順序。

使用 `LIMIT` 時，最好搭配使用能將結果資料列
限定為唯一順序的 `ORDER BY` 子句。否則，
你會得到查詢資料列中無法預期的一個子集——你或許是要
第十到第二十筆資料列，但在什麼排序方式下的第十到
第二十筆？除非你指定了 `ORDER BY`，
否則你並不知道是什麼排序方式。

查詢規劃器在產生查詢計畫時，會將 `LIMIT`
納入考量，因此依你為 `LIMIT` 與 `OFFSET`
所使用的值，很可能會得到不同的計畫（產生不同的資料列順序）。
因此，除非你以 `ORDER BY` 強制規定可預期的
結果順序，否則使用不同的 `LIMIT`／`OFFSET`
值來選取查詢結果的不同子集，*會得到不一致的結果*。
這並非臭蟲（bug）；這是 SQL 並不保證在未使用
`ORDER BY` 限定順序的情況下，以任何特定順序
傳回查詢結果這項事實所必然帶來的結果。

若沒有 `ORDER BY` 來強制選取具確定性的子集，
即使是重複執行同一個 `LIMIT` 查詢，也有可能
傳回資料表中不同子集的資料列。同樣地，這並非臭蟲；
在這種情況下，結果的確定性本來就無法保證。

<a id="SQL-FOR-UPDATE-SHARE"></a>

### 鎖定子句


`FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE`
與 `FOR KEY SHARE`
是*鎖定子句*；它們會影響 `SELECT`
在從資料表取得資料列時，如何鎖定這些資料列。

鎖定子句的一般形式為

```

FOR lock_strength [ OF from_reference [, ...] ] [ NOWAIT | SKIP LOCKED ]
```

其中 *`lock_strength`* 可以是下列其中之一

```

UPDATE
NO KEY UPDATE
SHARE
KEY SHARE
```

*`from_reference`* 必須是 `FROM`
子句中所參照的資料表 *`alias`*，
或未被隱藏的 *`table_name`*。
關於各個資料列層級鎖定模式的更多資訊，請參閱
[13.3.2 節](../../the-sql-language/mvcc/explicit-locking.md#LOCKING-ROWS)。

若要避免此操作等待其他交易提交，可使用
`NOWAIT` 或 `SKIP LOCKED` 選項。
使用 `NOWAIT` 時，若某個被選取的資料列
無法立即被鎖定，該陳述式會回報錯誤，而非等待。
使用 `SKIP LOCKED` 時，任何無法立即被鎖定的
被選取資料列都會被略過。略過已鎖定的資料列，
會導致資料視圖不一致，因此不適合用於一般用途，
但可用於避免多個消費者存取類似佇列的資料表時
發生鎖定爭用。請注意，`NOWAIT` 與
`SKIP LOCKED` 只適用於資料列層級的鎖——
所需的 `ROW SHARE` 資料表層級鎖仍會以一般方式取得
（見[第 13 章](../../the-sql-language/mvcc/README.md)）。若你需要
在不等待的情況下取得資料表層級鎖，可以先搭配
`NOWAIT` 選項使用
[`LOCK`](sql-lock.md)。

若鎖定子句中指名了特定的資料表，則只有來自那些
資料表的資料列會被鎖定；`SELECT` 中使用到的
其他資料表，則只是照常讀取而已。不含資料表清單的鎖定子句，
會影響該陳述式中所使用的所有資料表。若鎖定子句套用於
檢視表或子查詢，它會影響該檢視表或子查詢中所使用的
所有資料表。不過，這些子句並不適用於主查詢所參照的
`WITH` 查詢。若你希望資料列鎖定發生在
`WITH` 查詢內，請在該 `WITH` 查詢內
指定鎖定子句。

若有必要為不同的資料表指定不同的鎖定行為，
可以寫多個鎖定子句。若同一個資料表被超過一個鎖定子句
提及（或隱含地受其影響），則會以如同只被強度最強的
那一個子句指定的方式處理。同樣地，若影響某個資料表的
任一子句中指定了 `NOWAIT`，該資料表就會以此方式
處理。否則，若影響該資料表的任一子句中
指定了 `SKIP LOCKED`，則會以此方式
處理。

在傳回的資料列無法明確對應到個別資料表資料列的情境中，
無法使用鎖定子句；舉例來說，它們不能與彙總一起使用。

當鎖定子句出現在 `SELECT` 查詢的頂層時，
被鎖定的資料列，恰好就是該查詢所傳回的資料列；
在連接查詢的情況下，被鎖定的資料列，是那些
對所傳回的連接資料列有貢獻的資料列。此外，
在查詢快照時滿足查詢條件的資料列都會被鎖定，
儘管若它們在快照之後被更新、且不再滿足查詢條件，
就不會被傳回。若使用了 `LIMIT`，一旦已傳回
足夠滿足該限制的資料列，鎖定就會停止（但請注意，
被 `OFFSET` 略過的資料列仍會被鎖定）。同樣地，
若在游標的查詢中使用了鎖定子句，則只有該游標實際
擷取或跳過的資料列，才會被鎖定。

當鎖定子句出現在子 `SELECT` 中時，
被鎖定的資料列，是子查詢傳回給外層查詢的那些資料列。
由於外層查詢的條件，可能會被用來最佳化子查詢的執行，
這可能會涉及比單獨檢視該子查詢時所預期更少的資料列。
舉例來說，

```

SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss WHERE col1 = 5;
```

只會鎖定 `col1 = 5` 的資料列，儘管該條件
在文字上並不在子查詢之內。

先前的發行版本，未能保留由較晚儲存點升級的鎖定。舉例來說，下列程式碼：

```

BEGIN;
SELECT * FROM mytable WHERE key = 1 FOR UPDATE;
SAVEPOINT s;
UPDATE mytable SET ... WHERE key = 1;
ROLLBACK TO s;
```

在 `ROLLBACK TO` 之後，會無法保留
`FOR UPDATE` 鎖定。此問題已在 9.3 版中修復。

<a id="SQL-FOR-UPDATE-SHARE-CAUTION"></a>

### 小心


在 `READ
COMMITTED` 交易隔離等級下執行、同時使用 `ORDER
BY` 與鎖定子句的 `SELECT` 命令，
有可能傳回順序錯亂的資料列。這是因為 `ORDER BY`
是先被套用的。該命令會先排序結果，但接著可能在嘗試取得
一個或多個資料列的鎖定時被阻塞。一旦該 `SELECT`
解除阻塞，部分排序欄位的值可能已被修改，導致這些資料列
看起來順序錯亂（不過就原始欄位值而言，它們其實是依序的）。
如有需要，可以透過將 `FOR UPDATE/SHARE` 子句
放在子查詢中來解決此問題，舉例來說

```

SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss ORDER BY column1;
```

請注意，這會導致 `mytable` 的所有資料列都被鎖定，
而在頂層使用 `FOR UPDATE` 則只會鎖定實際傳回的資料列。
這可能會造成顯著的效能差異，特別是當 `ORDER BY`
與 `LIMIT` 或其他限制條件併用時。因此，
只有在預期排序欄位會有並行更新、且需要嚴格排序結果的情況下，
才建議使用此技巧。

在 `REPEATABLE READ` 或 `SERIALIZABLE`
交易隔離等級下，這會導致序列化失敗（`SQLSTATE`
為 `'40001'`），因此在這些隔離等級下，
不可能收到順序錯亂的資料列。

<a id="SQL-TABLE"></a>

### `TABLE` 命令

命令

```

TABLE name
```

等同於

```

SELECT * FROM name
```

它可以作為頂層命令使用，也可以在複雜查詢的某些部分中，
作為節省輸入的語法變體使用。與 `TABLE` 一併使用時，
只能使用 `WITH`、`UNION`、`INTERSECT`、`EXCEPT`、
`ORDER BY`、`LIMIT`、`OFFSET`、
`FETCH` 與 `FOR` 鎖定子句；不能使用
`WHERE` 子句以及任何形式的彙總。

<a id="id-1.9.3.172.9"></a>

## 範例


要將資料表 `films` 與資料表
`distributors` 進行連接：

```

SELECT f.title, f.did, d.name, f.date_prod, f.kind
    FROM distributors d JOIN films f USING (did);

       title       | did |     name     | date_prod  |   kind
-------------------+-----+--------------+------------+----------
 The Third Man     | 101 | British Lion | 1949-12-23 | Drama
 The African Queen | 101 | British Lion | 1951-08-11 | Romantic
 ...
```

要加總所有影片 `len` 欄位的值，並依
`kind` 將結果分組：

```

SELECT kind, sum(len) AS total FROM films GROUP BY kind;

   kind   | total
----------+-------
 Action   | 07:34
 Comedy   | 02:58
 Drama    | 14:28
 Musical  | 06:42
 Romantic | 04:38
```

要加總所有影片 `len` 欄位的值，依 `kind`
將結果分組，並只顯示總計小於 5 小時的群組：

```

SELECT kind, sum(len) AS total
    FROM films
    GROUP BY kind
    HAVING sum(len) < interval '5 hours';

   kind   | total
----------+-------
 Comedy   | 02:58
 Romantic | 04:38
```

下列兩個範例，是依第二欄（`name`）的內容
排序個別結果的兩種相同做法：

```

SELECT * FROM distributors ORDER BY name;
SELECT * FROM distributors ORDER BY 2;

 did |       name
-----+------------------
 109 | 20th Century Fox
 110 | Bavaria Atelier
 101 | British Lion
 107 | Columbia
 102 | Jean Luc Godard
 113 | Luso films
 104 | Mosfilm
 103 | Paramount
 106 | Toho
 105 | United Artists
 111 | Walt Disney
 112 | Warner Bros.
 108 | Westward
```

下一個範例顯示如何取得資料表 `distributors`
與 `actors` 的聯集，並將結果限制為兩個資料表中
以字母 W 開頭的資料列。由於只需要相異的資料列，
因此省略了關鍵字 `ALL`。

```

distributors:               actors:
 did |     name              id |     name
-----+--------------        ----+----------------
 108 | Westward               1 | Woody Allen
 111 | Walt Disney            2 | Warren Beatty
 112 | Warner Bros.           3 | Walter Matthau
 ...                         ...

SELECT distributors.name
    FROM distributors
    WHERE distributors.name LIKE 'W%'
UNION
SELECT actors.name
    FROM actors
    WHERE actors.name LIKE 'W%';

      name
----------------
 Walt Disney
 Walter Matthau
 Warner Bros.
 Warren Beatty
 Westward
 Woody Allen
```

此範例顯示如何在 `FROM` 子句中使用函式，
分別展示有無欄位定義清單的情況：

```

CREATE FUNCTION distributors(int) RETURNS SETOF distributors AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors(111);
 did |    name
-----+-------------
 111 | Walt Disney

CREATE FUNCTION distributors_2(int) RETURNS SETOF record AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors_2(111) AS (f1 int, f2 text);
 f1  |     f2
-----+-------------
 111 | Walt Disney
```

以下是加上序數欄位之函式的範例：

```

SELECT * FROM unnest(ARRAY['a','b','c','d','e','f']) WITH ORDINALITY;
 unnest | ordinality
--------+----------
 a      |        1
 b      |        2
 c      |        3
 d      |        4
 e      |        5
 f      |        6
(6 rows)
```

此範例顯示如何使用單純的 `WITH` 子句：

```

WITH t AS (
    SELECT random() as x FROM generate_series(1, 3)
  )
SELECT * FROM t
UNION ALL
SELECT * FROM t;
         x
--------------------
  0.534150459803641
  0.520092216785997
 0.0735620250925422
  0.534150459803641
  0.520092216785997
 0.0735620250925422
```

請注意，該 `WITH` 查詢只被求值一次，
因此我們得到了兩組相同的三個隨機值。

此範例使用 `WITH RECURSIVE`，從一個只顯示直屬
部屬關係的資料表中，找出員工 Mary 的所有部屬
（直屬或間接部屬），以及他們的間接層級：

```

WITH RECURSIVE employee_recursive(distance, employee_name, manager_name) AS (
    SELECT 1, employee_name, manager_name
    FROM employee
    WHERE manager_name = 'Mary'
  UNION ALL
    SELECT er.distance + 1, e.employee_name, e.manager_name
    FROM employee_recursive er, employee e
    WHERE er.employee_name = e.manager_name
  )
SELECT distance, employee_name FROM employee_recursive;
```

請注意遞迴查詢的典型形式：一個初始條件，接著是
`UNION`，再接著是查詢的遞迴部分。請務必確保
查詢的遞迴部分最終會傳回零筆資料列，否則該查詢會
無限迴圈。（更多範例請參閱[7.8 節](../../the-sql-language/queries/queries-with.md)。）

此範例使用 `LATERAL`，為 `manufacturers`
資料表的每一筆資料列，套用一個傳回集合的函式
`get_product_names()`：

```

SELECT m.name AS mname, pname
FROM manufacturers m, LATERAL get_product_names(m.id) pname;
```

由於這是內部連接，目前沒有任何產品的製造商，
不會出現在結果中。若我們希望結果中也包含這類製造商的名稱，
可以這樣做：

```

SELECT m.name AS mname, pname
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true;
```

<a id="id-1.9.3.172.10"></a>

## 相容性


當然，`SELECT` 陳述式與 SQL 標準相容。
但存在一些擴充功能，以及一些缺少的特性。

<a id="id-1.9.3.172.10.3"></a>

### 省略 `FROM` 子句

PostgreSQL 允許省略 `FROM` 子句。
這在計算單純運算式的結果時，有直接的用途：

```

SELECT 2+2;

 ?column?
----------
        4
```

其他一些 SQL 資料庫除非引入一個虛設的單資料列資料表
來執行 `SELECT`，否則無法做到這一點。

<a id="id-1.9.3.172.10.4"></a>

### 空的 `SELECT` 清單

`SELECT` 後方的輸出運算式清單可以為空，
這會產生一個零欄位的結果資料表。
依 SQL 標準，這並非有效的語法。
PostgreSQL 為了與允許零欄位資料表的做法保持一致，
允許這種寫法。不過，使用 `DISTINCT` 時，
不允許使用空清單。

<a id="id-1.9.3.172.10.5"></a>

### 省略 `AS` 關鍵字

在 SQL 標準中，只要新欄位名稱是有效的欄位名稱
（也就是說，與任何保留關鍵字都不相同），輸出欄位名稱前
選擇性的 `AS` 關鍵字就可以省略。PostgreSQL
的限制稍微嚴格一些：只要新欄位名稱與任何關鍵字相符
（無論是否為保留字），就需要使用 `AS`。建議的做法是
使用 `AS`，或以雙引號括住輸出欄位名稱，以防範
未來可能新增關鍵字所造成的衝突。

在 `FROM` 項目中，標準與 PostgreSQL
都允許在屬於非保留關鍵字的別名之前省略 `AS`。
但對於輸出欄位名稱而言，由於語法上的歧義，
這種做法並不實用。

<a id="id-1.9.3.172.10.6"></a>

### 省略 `FROM` 中子 `SELECT` 的別名

依 SQL 標準，`FROM` 清單中的子 `SELECT`
必須有別名。在 PostgreSQL 中，
可以省略此別名。

<a id="id-1.9.3.172.10.7"></a>

### `ONLY` 與繼承

SQL 標準要求，在撰寫 `ONLY` 時，資料表名稱
必須以括號括住，舉例來說 `SELECT * FROM ONLY
(tab1), ONLY (tab2) WHERE ...`。
PostgreSQL 則將這些括號視為選擇性的。

PostgreSQL 允許在後方加上 `*`，
以明確指定包含子資料表的非 `ONLY` 行為。
標準並不允許這種寫法。

（這些要點同樣適用於所有支援 `ONLY`
選項的 SQL 命令。）

<a id="id-1.9.3.172.10.8"></a>

### `TABLESAMPLE` 子句的限制

目前，`TABLESAMPLE` 子句只接受用於一般資料表
與具體化檢視表。依 SQL 標準，應該可以將它套用於
任何 `FROM` 項目。

<a id="id-1.9.3.172.10.9"></a>

### `FROM` 中的函式呼叫

PostgreSQL 允許將函式呼叫直接寫成
`FROM` 清單的成員。在 SQL 標準中，這樣的函式呼叫
必須包在子 `SELECT` 中；也就是說，語法
`FROM func(...) alias`
大致等同於
`FROM LATERAL (SELECT func(...)) alias`。
請注意，`LATERAL` 在此被視為隱含的；這是因為
標準要求 `FROM` 中的 `UNNEST()` 項目
具有 `LATERAL` 語意。PostgreSQL
則將 `UNNEST()` 與其他傳回集合的函式一視同仁。

<a id="id-1.9.3.172.10.10"></a>

### `GROUP BY` 與 `ORDER BY` 可用的命名空間

在 SQL-92 標準中，`ORDER BY` 子句只能使用
輸出欄位名稱或序號，而 `GROUP
BY` 子句只能使用以輸入欄位名稱為基礎的運算式。
PostgreSQL 擴充了這兩個子句，
讓它們也都能使用另一種選擇（但若有歧義，
則採用標準的解讀方式）。PostgreSQL
也允許這兩個子句指定任意運算式。請注意，
出現在運算式中的名稱，一律會被視為輸入欄位名稱，
而非輸出欄位名稱。

SQL:1999 及之後的版本，採用了與 SQL-92 略有不同、
並非完全向上相容的定義。不過在大多數情況下，
PostgreSQL 對 `ORDER BY` 或 `GROUP
BY` 運算式的解讀方式，會與 SQL:1999 相同。

<a id="id-1.9.3.172.10.11"></a>

### 函數相依關係

只有當資料表的主鍵包含在 `GROUP BY` 清單中時，
PostgreSQL 才會辨識函數相依關係
（允許從 `GROUP BY` 中省略欄位）。
SQL 標準則指定了應辨識的其他額外條件。

<a id="id-1.9.3.172.10.12"></a>

### `LIMIT` 與 `OFFSET`

`LIMIT` 與 `OFFSET` 子句是
PostgreSQL 特有的語法，MySQL
也使用相同語法。SQL:2008 標準引進了
`OFFSET ... FETCH {FIRST|NEXT}
...` 子句以達成相同的功能，如前文
[LIMIT 子句](sql-select.md#SQL-LIMIT)所示。
IBM DB2 也使用此語法。
（為 Oracle 撰寫的應用程式，
經常使用一種涉及自動產生之 `rownum` 欄位的
變通做法，來實作這些子句的效果，而
PostgreSQL 中並沒有這個欄位。）

<a id="id-1.9.3.172.10.13"></a>

### `FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE`、`FOR KEY SHARE`

雖然 `FOR UPDATE` 出現在 SQL 標準中，
但標準只允許將它作為 `DECLARE CURSOR` 的選項。
PostgreSQL 允許在任何 `SELECT`
查詢以及子 `SELECT` 中使用它，但這是一項擴充功能。
`FOR NO KEY UPDATE`、`FOR SHARE` 與
`FOR KEY SHARE` 這些變體，以及 `NOWAIT`
與 `SKIP LOCKED` 選項，都未出現在標準中。

<a id="id-1.9.3.172.10.14"></a>

### `WITH` 中的資料修改陳述式

PostgreSQL 允許將 `INSERT`、
`UPDATE`、`DELETE` 與
`MERGE` 用作 `WITH` 查詢。
這在 SQL 標準中並不存在。

<a id="id-1.9.3.172.10.15"></a>

### 非標準子句

`DISTINCT ON ( ... )` 是 SQL 標準的擴充功能。

`ROWS FROM( ... )` 是 SQL 標準的擴充功能。

`WITH` 的 `MATERIALIZED` 與 `NOT
MATERIALIZED` 選項，是 SQL 標準的擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-select.html)（原文版本：18.6；核對日期：2026-10-03）
