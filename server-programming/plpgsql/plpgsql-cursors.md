<a id="PLPGSQL-CURSORS"></a>

## 41.7. 游標 [#](#PLPGSQL-CURSORS)

[41.7.1. 宣告游標變數](plpgsql-cursors.md#PLPGSQL-CURSOR-DECLARATIONS)

[41.7.2. 開啟游標](plpgsql-cursors.md#PLPGSQL-CURSOR-OPENING)

[41.7.3. 使用游標](plpgsql-cursors.md#PLPGSQL-CURSOR-USING)

[41.7.4. 走訪游標的結果](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)

<a id="id-1.8.8.9.2"></a>

除了一次執行完整個查詢之外，也可以設定一個把查詢封裝起來的 *游標*（cursor），然後每次只讀取查詢結果中的少數幾筆資料列。這麼做的理由之一，是當結果包含大量資料列時可避免記憶體用盡。（不過 PL/pgSQL 的使用者通常不需要擔心這件事，因為 `FOR` 迴圈內部會自動使用游標來避免記憶體問題。）更有趣的用法，是回傳一個指向函式所建立之游標的參照，讓呼叫端可以讀取這些資料列。這提供了一種從函式回傳大量資料列集合的有效方式。

<a id="PLPGSQL-CURSOR-DECLARATIONS"></a>

### 41.7.1. 宣告游標變數 [#](#PLPGSQL-CURSOR-DECLARATIONS)

在 PL/pgSQL 中，對游標的所有存取都是透過游標變數進行的，而這種變數的型別一律是特別的資料型別 `refcursor`。建立游標變數的方式之一，就是直接把它宣告為 `refcursor` 型別的變數。另一種方式是使用游標宣告語法，其一般形式為：

```

name [ [ NO ] SCROLL ] CURSOR [ ( arguments ) ] FOR query;
```

（為了與 Oracle 相容，`FOR` 可以用 `IS` 取代。）若指定了 `SCROLL`，該游標將能夠向後捲動；若指定了 `NO SCROLL`，則向後讀取會被拒絕；若兩者都沒有指定，是否允許向後讀取就取決於查詢本身。*`arguments`* 若有指定，則是一串以逗號分隔的 `name
datatype` 配對，用來定義在給定查詢中要被參數值替換掉的名稱。這些名稱實際要替換成什麼值，會在稍後開啟游標時才指定。

一些範例：

```

DECLARE
    curs1 refcursor;
    curs2 CURSOR FOR SELECT * FROM tenk1;
    curs3 CURSOR (key integer) FOR SELECT * FROM tenk1 WHERE unique1 = key;
```

這三個變數的資料型別都是 `refcursor`，但第一個可以搭配任何查詢使用，第二個已經*繫結*了一個完整指定的查詢，而最後一個則繫結了一個帶參數的查詢。（`key` 會在游標開啟時被一個整數參數值替換掉。）變數 `curs1` 由於沒有繫結到任何特定查詢，因此稱為*未繫結的*。

當游標的查詢使用了 `FOR UPDATE/SHARE` 時，不能使用 `SCROLL` 選項。另外，若查詢牽涉到 volatile 函式，最好使用 `NO SCROLL`。`SCROLL` 的實作假設重新讀取查詢的輸出會得到一致的結果，而 volatile 函式可能無法做到這一點。

<a id="PLPGSQL-CURSOR-OPENING"></a>

### 41.7.2. 開啟游標 [#](#PLPGSQL-CURSOR-OPENING)

在游標能用來取得資料列之前，必須先*開啟*它。（這相當於 SQL 指令 [`DECLARE
CURSOR`](../../reference/sql-commands/sql-declare.md) 的動作。）PL/pgSQL 有三種形式的 `OPEN` 陳述式，其中兩種使用未繫結的游標變數，第三種則使用已繫結的游標變數。

### 注意

已繫結的游標變數也可以不用明確開啟游標就直接使用，也就是透過[第 41.7.4 節](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)所述的 `FOR` 陳述式。`FOR` 迴圈會開啟游標，並在迴圈結束時再次將其關閉。

<a id="id-1.8.8.9.5.4"></a>

開啟游標會牽涉到建立一個稱為 *portal* 的伺服器內部資料結構，它保存了該游標查詢的執行狀態。portal 具有名稱，而該名稱在此 portal 存在的期間內，必須在工作階段中是唯一的。預設情況下，PL/pgSQL 會為它所建立的每個 portal 指派一個唯一的名稱。不過，如果你把一個非空值的字串值指派給游標變數，該字串就會被用作它的 portal 名稱。這項功能的用法在[第 41.7.3.5 節](plpgsql-cursors.md#PLPGSQL-CURSOR-RETURNING)中有所說明。

<a id="PLPGSQL-CURSOR-OPENING-OPEN-FOR-QUERY"></a>

#### 41.7.2.1. `OPEN FOR` *`query`* [#](#PLPGSQL-CURSOR-OPENING-OPEN-FOR-QUERY)

```

OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR query;
```

這個游標變數會被開啟，並被賦予所指定的查詢來執行。該游標不能已經處於開啟狀態，而且它必須被宣告為未繫結的游標變數（也就是單純的 `refcursor` 變數）。查詢必須是 `SELECT`，或其他會回傳資料列的東西（例如 `EXPLAIN`）。這個查詢的處理方式與 PL/pgSQL 中其他 SQL 指令相同：PL/pgSQL 變數名稱會被替換，而查詢的執行計畫會被快取以便重複使用。當某個 PL/pgSQL 變數被替換進游標查詢中時，被替換進去的是它在 `OPEN` 當下所具有的值；之後對該變數的變更不會影響游標的行為。`SCROLL` 與 `NO SCROLL` 選項的意義與已繫結游標的情況相同。

一個例子：

```

OPEN curs1 FOR SELECT * FROM foo WHERE key = mykey;
```

<a id="PLPGSQL-CURSOR-OPENING-OPEN-FOR-EXECUTE"></a>

#### 41.7.2.2. `OPEN FOR EXECUTE` [#](#PLPGSQL-CURSOR-OPENING-OPEN-FOR-EXECUTE)

```

OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR EXECUTE query_string
                                     [ USING expression [, ... ] ];
```

這個游標變數會被開啟，並被賦予所指定的查詢來執行。該游標不能已經處於開啟狀態，而且它必須被宣告為未繫結的游標變數（也就是單純的 `refcursor` 變數）。查詢是以字串運算式的形式指定，方式與 `EXECUTE` 指令中相同。一如往常，這提供了彈性，使得查詢的執行計畫可以每次執行都不一樣（請參閱[第 41.11.2 節](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)），同時也意味著不會對指令字串進行變數替換。與 `EXECUTE` 一樣，參數值可以透過 `format()` 與 `USING` 插入到動態指令中。`SCROLL` 與 `NO SCROLL` 選項的意義與已繫結游標的情況相同。

一個例子：

```

OPEN curs1 FOR EXECUTE format('SELECT * FROM %I WHERE col1 = $1',tabname) USING keyvalue;
```

在這個例子中，資料表名稱是透過 `format()` 插入查詢中的。用來與 `col1` 比較的值則是透過 `USING` 參數插入的，因此不需要加上引號。

<a id="PLPGSQL-OPEN-BOUND-CURSOR"></a>

#### 41.7.2.3. 開啟已繫結的游標 [#](#PLPGSQL-OPEN-BOUND-CURSOR)

```

OPEN bound_cursorvar [ ( [ argument_name { := | => } ] argument_value [, ...] ) ];
```

這種形式的 `OPEN` 用來開啟宣告時就已繫結查詢的游標變數。該游標不能已經處於開啟狀態。當且僅當該游標宣告時帶有引數時，才必須出現一串實際引數值的運算式清單。這些值會被替換進查詢中。

已繫結游標的查詢執行計畫一律被視為可快取的；這種情況下沒有相當於 `EXECUTE` 的東西。請注意 `SCROLL` 與 `NO SCROLL` 不能在 `OPEN` 中指定，因為該游標的捲動行為早已決定。

引數值可以使用*位置式*或*具名式*標示法來傳遞。在位置式標示法中，所有引數都依序指定。在具名式標示法中，每個引數的名稱都以 `:=` 或 `=>` 與引數運算式分隔開來。與[第 4.3 節](../../the-sql-language/sql-syntax/sql-syntax-calling-funcs.md)所述的函式呼叫類似，位置式與具名式標示法也可以混用。

範例（以下使用前面的游標宣告範例）：

```

OPEN curs2;
OPEN curs3(42);
OPEN curs3(key := 42);
OPEN curs3(key => 42);
```

由於已繫結游標的查詢會進行變數替換，因此實際上有兩種方式可以把值傳進游標：一是透過 `OPEN` 的明確引數，二是隱含地在查詢中參照某個 PL/pgSQL 變數。不過，只有在該已繫結游標宣告之前就已宣告的變數，才會被替換進去。不論是哪一種情況，要傳遞的值都是在 `OPEN` 當下決定的。舉例來說，要達到與上面 `curs3` 範例相同的效果，另一種做法是

```

DECLARE
    key integer;
    curs4 CURSOR FOR SELECT * FROM tenk1 WHERE unique1 = key;
BEGIN
    key := 42;
    OPEN curs4;
```

<a id="PLPGSQL-CURSOR-USING"></a>

### 41.7.3. 使用游標 [#](#PLPGSQL-CURSOR-USING)

游標一旦開啟之後，就可以用這裡所描述的陳述式來操作它。

這些操作不一定要發生在最初開啟該游標的同一個函式中。你可以從函式回傳一個 `refcursor` 值，讓呼叫端去操作這個游標。（在內部，`refcursor` 值其實就是保存該游標作用中查詢之 portal 的字串名稱。這個名稱可以四處傳遞、指派給其他 `refcursor` 變數等等，而不會干擾到該 portal。）

所有 portal 都會在交易結束時隱含地被關閉。因此 `refcursor` 值只有在交易結束之前，才能用來指涉一個開啟中的游標。

<a id="PLPGSQL-CURSOR-USING-FETCH"></a>

#### 41.7.3.1. `FETCH` [#](#PLPGSQL-CURSOR-USING-FETCH)

```

FETCH [ direction { FROM | IN } ] cursor INTO target;
```

`FETCH` 會從游標取出（指定方向的）下一筆資料列到一個目標中，這個目標可以是資料列變數、record 變數，或是以逗號分隔的一串簡單變數，就和 `SELECT INTO` 一樣。若沒有合適的資料列，目標會被設為 NULL。與 `SELECT
INTO` 一樣，可以檢查特殊變數 `FOUND` 來判斷是否取得了資料列。若沒有取得任何資料列，則游標會依移動方向被定位在最後一筆資料列之後或第一筆資料列之前。

*`direction`* 子句可以是 SQL [FETCH](../../reference/sql-commands/sql-fetch.md) 指令所允許的任何變化形式，但不包含可取出超過一筆資料列的那些；也就是說，它可以是 `NEXT`、`PRIOR`、`FIRST`、`LAST`、`ABSOLUTE` *`count`*、`RELATIVE` *`count`*、`FORWARD` 或 `BACKWARD`。省略 *`direction`* 就等同於指定 `NEXT`。在使用 *`count`* 的形式中，*`count`* 可以是任何整數值的運算式（不像 SQL `FETCH` 指令只允許整數常數）。需要向後移動的 *`direction`* 值，除非該游標宣告或開啟時帶有 `SCROLL` 選項，否則很可能會失敗。

*`cursor`* 必須是某個指涉開啟中游標 portal 的 `refcursor` 變數的名稱。

範例：

```

FETCH curs1 INTO rowvar;
FETCH curs2 INTO foo, bar, baz;
FETCH LAST FROM curs3 INTO x, y;
FETCH RELATIVE -2 FROM curs4 INTO x;
```

<a id="PLPGSQL-CURSOR-USING-MOVE"></a>

#### 41.7.3.2. `MOVE` [#](#PLPGSQL-CURSOR-USING-MOVE)

```

MOVE [ direction { FROM | IN } ] cursor;
```

`MOVE` 會重新定位游標，但不會取出任何資料。`MOVE` 的運作方式與 `FETCH` 指令相同，差別在於它只會重新定位游標，而不會回傳所移動到的那筆資料列。*`direction`* 子句可以是 SQL [FETCH](../../reference/sql-commands/sql-fetch.md) 指令所允許的任何變化形式，包含可取出超過一筆資料列的那些；此時游標會被定位在最後一筆這樣的資料列上。（不過，*`direction`* 子句只是一個沒有關鍵字的 *`count`* 運算式的情況，在 PL/pgSQL 中已不建議使用。該語法與完全省略 *`direction`* 子句的情況有歧義，因此若 *`count`* 不是常數，它可能會失敗。）與 `SELECT
INTO` 一樣，可以檢查特殊變數 `FOUND` 來判斷是否有資料列可供移動。若沒有這樣的資料列，則游標會依移動方向被定位在最後一筆資料列之後或第一筆資料列之前。

範例：

```

MOVE curs1;
MOVE LAST FROM curs3;
MOVE RELATIVE -2 FROM curs4;
MOVE FORWARD 2 FROM curs4;
```

<a id="PLPGSQL-CURSOR-USING-UPDATE-DELETE"></a>

#### 41.7.3.3. `UPDATE/DELETE WHERE CURRENT OF` [#](#PLPGSQL-CURSOR-USING-UPDATE-DELETE)

```

UPDATE table SET ... WHERE CURRENT OF cursor;
DELETE FROM table WHERE CURRENT OF cursor;
```

當游標定位在某筆資料表資料列上時，可以利用該游標來指出該資料列，進而更新或刪除它。對於游標的查詢可以是什麼樣子有一些限制（特別是不能有分組），而且最好在游標中使用 `FOR UPDATE`。更多資訊請參閱 [DECLARE](../../reference/sql-commands/sql-declare.md) 參考頁面。

一個例子：

```

UPDATE foo SET dataval = myval WHERE CURRENT OF curs1;
```

<a id="PLPGSQL-CURSOR-USING-CLOSE"></a>

#### 41.7.3.4. `CLOSE` [#](#PLPGSQL-CURSOR-USING-CLOSE)

```

CLOSE cursor;
```

`CLOSE` 會關閉一個開啟中游標底下的 portal。這可以用來比交易結束更早釋放資源，或是把該游標變數空出來以便再次開啟。

一個例子：

```

CLOSE curs1;
```

<a id="PLPGSQL-CURSOR-RETURNING"></a>

#### 41.7.3.5. 回傳游標 [#](#PLPGSQL-CURSOR-RETURNING)

PL/pgSQL 函式可以把游標回傳給呼叫端。這在要回傳多筆資料列或多個欄位時很有用，尤其是結果集合非常龐大的時候。要做到這一點，函式會開啟游標並把游標名稱回傳給呼叫端（或者直接使用呼叫端所指定、或以其他方式已知的 portal 名稱來開啟游標）。接著呼叫端就可以從該游標取出資料列。這個游標可以由呼叫端關閉，或者在交易結束時自動被關閉。

游標所用的 portal 名稱可以由程式設計師指定，也可以自動產生。若要指定 portal 名稱，只要在開啟該 `refcursor` 變數所代表的游標之前，先指派一個字串給該變數即可。`OPEN` 會把該 `refcursor` 變數的字串值當作底層 portal 的名稱。不過，如果該 `refcursor` 變數的值是空值（預設就是如此），那麼 `OPEN` 會自動產生一個不會與任何既有 portal 衝突的名稱，並把它指派給該 `refcursor` 變數。

### 注意

在 PostgreSQL 16 之前，已繫結的游標變數會被初始化為包含它們自己的名稱，而不是保留為空值，因此底層的 portal 名稱預設會與游標變數的名稱相同。之所以改掉這個行為，是因為它造成不同函式中名稱相似的游標太容易發生衝突。

下面的例子展示了由呼叫端提供游標名稱的一種做法：

```

CREATE TABLE test (col text);
INSERT INTO test VALUES ('123');

CREATE FUNCTION reffunc(refcursor) RETURNS refcursor AS '
BEGIN
    OPEN $1 FOR SELECT col FROM test;
    RETURN $1;
END;
' LANGUAGE plpgsql;

BEGIN;
SELECT reffunc('funccursor');
FETCH ALL IN funccursor;
COMMIT;
```

下面的例子使用自動產生游標名稱的方式：

```

CREATE FUNCTION reffunc2() RETURNS refcursor AS '
DECLARE
    ref refcursor;
BEGIN
    OPEN ref FOR SELECT col FROM test;
    RETURN ref;
END;
' LANGUAGE plpgsql;

-- need to be in a transaction to use cursors.
BEGIN;
SELECT reffunc2();

      reffunc2
--------------------
 <unnamed cursor 1>
(1 row)

FETCH ALL IN "<unnamed cursor 1>";
COMMIT;
```

下面的例子展示了從單一函式回傳多個游標的一種做法：

```

CREATE FUNCTION myfunc(refcursor, refcursor) RETURNS SETOF refcursor AS $$
BEGIN
    OPEN $1 FOR SELECT * FROM table_1;
    RETURN NEXT $1;
    OPEN $2 FOR SELECT * FROM table_2;
    RETURN NEXT $2;
END;
$$ LANGUAGE plpgsql;

-- need to be in a transaction to use cursors.
BEGIN;

SELECT * FROM myfunc('a', 'b');

FETCH ALL FROM a;
FETCH ALL FROM b;
COMMIT;
```

<a id="PLPGSQL-CURSOR-FOR-LOOP"></a>

### 41.7.4. 走訪游標的結果 [#](#PLPGSQL-CURSOR-FOR-LOOP)

`FOR` 陳述式有一種變化形式，可以走訪某個游標所回傳的資料列。其語法為：

```

[ <<label>> ]
FOR recordvar IN bound_cursorvar [ ( [ argument_name { := | => } ] argument_value [, ...] ) ] LOOP
    statements
END LOOP [ label ];
```

該游標變數必須在宣告時就已繫結某個查詢，而且它*不能*已經處於開啟狀態。`FOR` 陳述式會自動開啟該游標，並在迴圈離開時再次將其關閉。當且僅當該游標宣告時帶有引數時，才必須出現一串實際引數值的運算式清單。這些值會被替換進查詢中，方式與 `OPEN` 期間完全相同（請參閱[第 41.7.2.3 節](plpgsql-cursors.md#PLPGSQL-OPEN-BOUND-CURSOR)）。

變數 *`recordvar`* 會自動被定義為 `record` 型別，而且只存在於迴圈內部（迴圈內會忽略該變數名稱任何既有的定義）。游標所回傳的每一筆資料列都會依序被指派給這個 record 變數，然後執行迴圈主體。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-cursors.html)（原文版本：18.6；核對日期：2026-09-13）
