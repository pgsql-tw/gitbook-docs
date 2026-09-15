<a id="RANGETYPES"></a>

## 8.17. 範圍型別 [#](#RANGETYPES)

[8.17.1. 內建的範圍與多重範圍型別](rangetypes.md#RANGETYPES-BUILTIN)

[8.17.2. 範例](rangetypes.md#RANGETYPES-EXAMPLES)

[8.17.3. 含端點與不含端點的界限](rangetypes.md#RANGETYPES-INCLUSIVITY)

[8.17.4. 無限（無界限）範圍](rangetypes.md#RANGETYPES-INFINITE)

[8.17.5. 範圍的輸入／輸出](rangetypes.md#RANGETYPES-IO)

[8.17.6. 建構範圍與多重範圍](rangetypes.md#RANGETYPES-CONSTRUCT)

[8.17.7. 離散範圍型別](rangetypes.md#RANGETYPES-DISCRETE)

[8.17.8. 定義新的範圍型別](rangetypes.md#RANGETYPES-DEFINING)

[8.17.9. 索引](rangetypes.md#RANGETYPES-INDEXING)

[8.17.10. 範圍上的限制條件](rangetypes.md#RANGETYPES-CONSTRAINT)

<a id="id-1.5.7.25.2"></a><a id="id-1.5.7.25.3"></a>

範圍型別是用來表示某種元素型別（稱為該範圍的*子型別*）之值範圍的資料型別。例如，`timestamp` 的範圍可以用來表示某間會議室被預約的時間範圍。在這個例子中，資料型別是 `tsrange`（「timestamp range」的簡稱），而 `timestamp` 是子型別。子型別必須具有全序關係，這樣才能明確定義元素值是落在某個值範圍之內、之前，還是之後。

範圍型別很有用，因為它們可以用單一個範圍值來表示許多元素值，而且像範圍重疊這類概念也能清楚地表達出來。把時間與日期範圍用於排程是最明顯的例子；但價格範圍、儀器的量測範圍等等也同樣好用。

每一種範圍型別都有一種對應的多重範圍型別。多重範圍是一份由不相鄰、非空、非 NULL 的範圍所組成的有序清單。大多數範圍運算子也可以用於多重範圍，而多重範圍另外還有幾個自己專屬的函式。

<a id="RANGETYPES-BUILTIN"></a>

### 8.17.1. 內建的範圍與多重範圍型別 [#](#RANGETYPES-BUILTIN)

PostgreSQL 內建了下列範圍型別：

* `int4range` — `integer` 的範圍，
  `int4multirange` — 對應的多重範圍
* `int8range` — `bigint` 的範圍，
  `int8multirange` — 對應的多重範圍
* `numrange` — `numeric` 的範圍，
  `nummultirange` — 對應的多重範圍
* `tsrange` — `timestamp without time zone` 的範圍，
  `tsmultirange` — 對應的多重範圍
* `tstzrange` — `timestamp with time zone` 的範圍，
  `tstzmultirange` — 對應的多重範圍
* `daterange` — `date` 的範圍，
  `datemultirange` — 對應的多重範圍

此外，你也可以定義自己的範圍型別；更多資訊請參閱 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md)。

<a id="RANGETYPES-EXAMPLES"></a>

### 8.17.2. 範例 [#](#RANGETYPES-EXAMPLES)

```

CREATE TABLE reservation (room int, during tsrange);
INSERT INTO reservation VALUES
    (1108, '[2010-01-01 14:30, 2010-01-01 15:30)');

-- Containment
SELECT int4range(10, 20) @> 3;

-- Overlaps
SELECT numrange(11.1, 22.2) && numrange(20.0, 30.0);

-- Extract the upper bound
SELECT upper(int8range(15, 25));

-- Compute the intersection
SELECT int4range(10, 20) * int4range(15, 25);

-- Is the range empty?
SELECT isempty(numrange(1, 5));
```

範圍型別上的運算子與函式完整清單，請參閱[表 9.58](../functions/functions-range.md#RANGE-OPERATORS-TABLE)與[表 9.60](../functions/functions-range.md#RANGE-FUNCTIONS-TABLE)。

<a id="RANGETYPES-INCLUSIVITY"></a>

### 8.17.3. 含端點與不含端點的界限 [#](#RANGETYPES-INCLUSIVITY)

每個非空範圍都有兩個界限，即下界與上界。這兩個值之間的所有點都包含在該範圍內。含端點的界限表示界限點本身也包含在範圍內，而不含端點的界限則表示界限點不包含在範圍內。

在範圍的文字形式中，含端點的下界以「`[`」表示，不含端點的下界則以「`(`」表示。同樣地，含端點的上界以「`]`」表示，而不含端點的上界則以「`)`」表示。（更多細節請參閱[第 8.17.5 節](rangetypes.md#RANGETYPES-IO)。）

函式 `lower_inc` 與 `upper_inc` 分別用來測試範圍值的下界與上界是否含端點。

<a id="RANGETYPES-INFINITE"></a>

### 8.17.4. 無限（無界限）範圍 [#](#RANGETYPES-INFINITE)

範圍的下界可以省略，表示所有小於上界的值都包含在該範圍內，例如 `(,3]`。同樣地，如果省略範圍的上界，則所有大於下界的值都包含在該範圍內。如果同時省略下界與上界，則元素型別的所有值都視為在該範圍內。將缺少的界限指定為含端點時，會自動轉換成不含端點，例如 `[,]` 會被轉換成 `(,)`。你可以把這些缺少的值想成正／負無限大，但它們其實是特殊的範圍型別值，並且被視為超出任何範圍元素型別的正／負無限大值。

具有「無限大」概念的元素型別，可以把它們當作明確的界限值使用。例如，對於 timestamp 範圍，`[today,infinity)` 不包含特殊的 `timestamp` 值 `infinity`，而 `[today,infinity]` 則包含它，`[today,)` 與 `[today,]` 也同樣包含它。

函式 `lower_inf` 與 `upper_inf` 分別用來測試範圍的下界與上界是否為無限。

<a id="RANGETYPES-IO"></a>

### 8.17.5. 範圍的輸入／輸出 [#](#RANGETYPES-IO)

範圍值的輸入必須符合下列其中一種模式：

```

(lower-bound,upper-bound)
(lower-bound,upper-bound]
[lower-bound,upper-bound)
[lower-bound,upper-bound]
empty
```

如同前面所述，小括號或中括號表示下界與上界是不含端點或含端點。請注意，最後一種模式是 `empty`，它代表空範圍（不包含任何點的範圍）。

*`lower-bound`* 可以是對子型別而言有效的輸入字串，也可以留空以表示沒有下界。同樣地，*`upper-bound`* 可以是對子型別而言有效的輸入字串，也可以留空以表示沒有上界。

每個界限值都可以使用 `"`（雙引號）字元括起來。如果界限值中含有小括號、中括號、逗號、雙引號或反斜線，就必須這麼做，否則這些字元會被當成範圍語法的一部分。若要在加上引號的界限值中放入雙引號或反斜線，請在它前面加上一個反斜線。（此外，在以雙引號括起的界限值中，連續兩個雙引號會被視為代表一個雙引號字元，這與 SQL 字面值字串中單引號的規則類似。）或者，你也可以不使用引號，改用反斜線跳脫來保護所有原本會被當成範圍語法的資料字元。另外，若要寫出值為空字串的界限，請寫成 `""`，因為什麼都不寫代表的是無限界限。

範圍值前後允許有空白字元，但小括號或中括號之間的任何空白字元，都會被視為下界或上界值的一部分。（依元素型別而定，這些空白字元可能有意義，也可能沒有意義。）

### 注意

這些規則與在複合型別常數中撰寫欄位值的規則非常相似。更多說明請參閱[第 8.16.6 節](rowtypes.md#ROWTYPES-IO-SYNTAX)。

範例：

```

-- includes 3, does not include 7, and does include all points in between
SELECT '[3,7)'::int4range;

-- does not include either 3 or 7, but includes all points in between
SELECT '(3,7)'::int4range;

-- includes only the single point 4
SELECT '[4,4]'::int4range;

-- includes no points (and will be normalized to 'empty')
SELECT '[4,4)'::int4range;
```

多重範圍的輸入是一對大括號（`{` 與 `}`），其中包含零個或多個以逗號分隔的有效範圍。大括號與逗號周圍允許有空白字元。這樣的設計是為了讓人聯想到陣列語法，不過多重範圍簡單得多：它們只有一個維度，而且內容不需要加引號。（但它們各個範圍的界限仍可以像上面所述那樣加上引號。）

範例：

```

SELECT '{}'::int4multirange;
SELECT '{[3,7)}'::int4multirange;
SELECT '{[3,7), [8,9)}'::int4multirange;
```

<a id="RANGETYPES-CONSTRUCT"></a>

### 8.17.6. 建構範圍與多重範圍 [#](#RANGETYPES-CONSTRUCT)

每一種範圍型別都有一個與該範圍型別同名的建構子函式。使用建構子函式通常比撰寫範圍常數方便，因為這樣就不需要為界限值額外加上引號。建構子函式接受兩個或三個引數。兩個引數的形式會建構標準形式的範圍（下界含端點、上界不含端點），而三個引數的形式則會建構界限形式由第三個引數指定的範圍。第三個引數必須是「`()`」、「`(]`」、「`[)`」或「`[]`」其中一個字串。例如：

```

-- The full form is: lower bound, upper bound, and text argument indicating
-- inclusivity/exclusivity of bounds.
SELECT numrange(1.0, 14.0, '(]');

-- If the third argument is omitted, '[)' is assumed.
SELECT numrange(1.0, 14.0);

-- Although '(]' is specified here, on display the value will be converted to
-- canonical form, since int8range is a discrete range type (see below).
SELECT int8range(1, 14, '(]');

-- Using NULL for either bound causes the range to be unbounded on that side.
SELECT numrange(NULL, 2.2);
```

每一種範圍型別也都有一個與該多重範圍型別同名的多重範圍建構子。這個建構子函式接受零個或多個引數，而這些引數都必須是對應型別的範圍。例如：

```

SELECT nummultirange();
SELECT nummultirange(numrange(1.0, 14.0));
SELECT nummultirange(numrange(1.0, 14.0), numrange(20.0, 25.0));
```

<a id="RANGETYPES-DISCRETE"></a>

### 8.17.7. 離散範圍型別 [#](#RANGETYPES-DISCRETE)

離散範圍是指元素型別具有明確定義之「步階」的範圍，例如 `integer` 或 `date`。在這類型別中，當兩個元素之間不存在其他有效值時，就可以說這兩個元素是相鄰的。這與連續範圍形成對比：在連續範圍中，總是（或幾乎總是）能夠在兩個給定值之間找出其他元素值。例如，`numeric` 型別上的範圍是連續的，`timestamp` 上的範圍也是。（即使 `timestamp` 的精度有限，理論上可以視為離散的，但把它當成連續的比較好，因為通常我們並不關心它的步階大小。）

另一種理解離散範圍型別的方式是：對於每一個元素值，都有明確的「下一個」或「上一個」值的概念。知道這一點之後，就可以藉由選取下一個或上一個元素值來取代原本給定的值，在範圍界限的含端點與不含端點表示法之間進行轉換。例如，在整數範圍型別中，`[4,8]` 與 `(3,9)` 表示相同的值集合；但對於 numeric 上的範圍就不是如此。

離散範圍型別應該要有一個*正規化*函式，這個函式清楚知道該元素型別所需的步階大小。正規化函式的職責是把範圍型別中等價的值轉換成相同的表示法，特別是讓界限一致地採用含端點或不含端點的形式。如果沒有指定正規化函式，那麼格式不同的範圍就一律會被視為不相等，即使它們實際上可能代表相同的值集合。

內建的範圍型別 `int4range`、`int8range` 與 `daterange` 都使用包含下界並排除上界的正規形式，也就是 `[)`。不過，使用者自訂的範圍型別可以採用其他慣例。

<a id="RANGETYPES-DEFINING"></a>

### 8.17.8. 定義新的範圍型別 [#](#RANGETYPES-DEFINING)

使用者可以定義自己的範圍型別。這麼做最常見的原因，是要在內建範圍型別未提供的子型別上使用範圍。例如，若要定義一個子型別為 `float8` 的新範圍型別：

```

CREATE TYPE floatrange AS RANGE (
    subtype = float8,
    subtype_diff = float8mi
);

SELECT '[1.234, 5.678]'::floatrange;
```

因為 `float8` 沒有有意義的「步階」，所以在這個例子中我們沒有定義正規化函式。

當你定義自己的範圍時，會自動獲得一個對應的多重範圍型別。

定義自己的範圍型別，也讓你能夠指定要使用不同的子型別 B-tree 運算子類別或定序，藉此改變決定哪些值落在某個範圍內的排序方式。

如果子型別被認為具有離散而非連續的值，`CREATE TYPE` 指令就應該指定一個 `canonical` 函式。正規化函式接受一個輸入的範圍值，並且必須回傳一個等價的範圍值，這個回傳值可以有不同的界限與格式。對於代表相同值集合的兩個範圍，例如整數範圍 `[1, 7]` 與 `[1,
8)`，它們的正規輸出必須完全相同。你選擇哪一種表示法作為正規形式並不重要，只要格式不同但等價的兩個值，永遠都被對應到具有相同格式的同一個值即可。除了調整含端點／不含端點的界限格式之外，正規化函式也可能會對界限值做捨入處理，以因應所需步階大小大於子型別所能儲存之精度的情況。例如，可以把 `timestamp` 上的範圍型別定義成步階大小為一小時，這時正規化函式就必須把不是一小時倍數的界限捨入，或者改為拋出錯誤。

此外，任何打算搭配 GiST 或 SP-GiST 索引使用的範圍型別，都應該定義一個子型別差值函式，也就是 `subtype_diff` 函式。（沒有 `subtype_diff` 索引仍然可以運作，但很可能會比提供差值函式時的效率低得多。）子型別差值函式接受兩個子型別的輸入值，並回傳它們的差（也就是 *`X`* 減 *`Y`*），以 `float8` 值表示。在上面的例子中，可以使用一般 `float8` 減法運算子底層所用的函式 `float8mi`；但對於其他子型別，就會需要做一些型別轉換。可能也需要一些創意來思考如何把差值表示成數字。`subtype_diff` 函式應該盡可能與所選運算子類別及定序所隱含的排序方式一致；也就是說，只要依該排序方式其第一個引數大於第二個引數，其結果就應該是正數。

以下是一個比較不那麼過度簡化的 `subtype_diff` 函式範例：

```

CREATE FUNCTION time_subtype_diff(x time, y time) RETURNS float8 AS
'SELECT EXTRACT(EPOCH FROM (x - y))' LANGUAGE sql STRICT IMMUTABLE;

CREATE TYPE timerange AS RANGE (
    subtype = time,
    subtype_diff = time_subtype_diff
);

SELECT '[11:10, 23:00]'::timerange;
```

關於建立範圍型別的更多資訊，請參閱 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md)。

<a id="RANGETYPES-INDEXING"></a>

### 8.17.9. 索引 [#](#RANGETYPES-INDEXING)

<a id="id-1.5.7.25.15.2"></a>

可以為範圍型別的資料表欄位建立 GiST 與 SP-GiST 索引。多重範圍型別的資料表欄位則可以建立 GiST 索引。例如，若要建立 GiST 索引：

```

CREATE INDEX reservation_idx ON reservation USING GIST (during);
```

範圍上的 GiST 或 SP-GiST 索引可以加速涉及下列範圍運算子的查詢：`=`、`&&`、`<@`、`@>`、`<<`、`>>`、`-|-`、`&<` 與 `&>`。多重範圍上的 GiST 索引可以加速涉及同一組多重範圍運算子的查詢。範圍上的 GiST 索引與多重範圍上的 GiST 索引，也可以分別加速涉及下列跨型別之範圍對多重範圍、以及多重範圍對範圍運算子的查詢：`&&`、`<@`、`@>`、`<<`、`>>`、`-|-`、`&<` 與 `&>`。更多資訊請參閱[表 9.58](../functions/functions-range.md#RANGE-OPERATORS-TABLE)。

此外，也可以為範圍型別的資料表欄位建立 B-tree 與 hash 索引。對於這些索引型別而言，基本上唯一有用的範圍運算就是等值比較。範圍值有定義 B-tree 排序方式以及對應的 `<` 與 `>` 運算子，但這個排序相當武斷，在實務上通常沒有什麼用。範圍型別的 B-tree 與 hash 支援，主要是為了讓查詢內部能夠進行排序與雜湊運算，而不是為了建立實際的索引。

<a id="RANGETYPES-CONSTRAINT"></a>

### 8.17.10. 範圍上的限制條件 [#](#RANGETYPES-CONSTRAINT)

<a id="id-1.5.7.25.16.2"></a>

雖然 `UNIQUE` 對純量值而言是很自然的限制條件，但它通常不適用於範圍型別。相對地，排除限制條件往往更為合適（請參閱 [CREATE TABLE
... CONSTRAINT ... EXCLUDE](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-EXCLUDE)）。排除限制條件讓你能夠在範圍型別上指定像「不重疊」這類的限制條件。例如：

```

CREATE TABLE reservation (
    during tsrange,
    EXCLUDE USING GIST (during WITH &&)
);
```

該限制條件會防止資料表中同時存在任何重疊的值：

```

INSERT INTO reservation VALUES
    ('[2010-01-01 11:30, 2010-01-01 15:00)');
INSERT 0 1

INSERT INTO reservation VALUES
    ('[2010-01-01 14:45, 2010-01-01 15:45)');
ERROR:  conflicting key value violates exclusion constraint "reservation_during_excl"
DETAIL:  Key (during)=(["2010-01-01 14:45:00","2010-01-01 15:45:00")) conflicts
with existing key (during)=(["2010-01-01 11:30:00","2010-01-01 15:00:00")).
```

你可以使用 [`btree_gist`](../../appendixes/contrib/btree-gist.md) 擴充套件，在一般的純量資料型別上定義排除限制條件，然後把它與範圍排除結合起來，以獲得最大的彈性。例如，在安裝 `btree_gist` 之後，下列限制條件只會在會議室號碼相同時才拒絕重疊的範圍：

```

CREATE EXTENSION btree_gist;
CREATE TABLE room_reservation (
    room text,
    during tsrange,
    EXCLUDE USING GIST (room WITH =, during WITH &&)
);

INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:00, 2010-01-01 15:00)');
INSERT 0 1

INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:30, 2010-01-01 15:30)');
ERROR:  conflicting key value violates exclusion constraint "room_reservation_room_during_excl"
DETAIL:  Key (room, during)=(123A, ["2010-01-01 14:30:00","2010-01-01 15:30:00")) conflicts
with existing key (room, during)=(123A, ["2010-01-01 14:00:00","2010-01-01 15:00:00")).

INSERT INTO room_reservation VALUES
    ('123B', '[2010-01-01 14:30, 2010-01-01 15:30)');
INSERT 0 1
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rangetypes.html)（原文版本：18.6；核對日期：2026-09-13）
