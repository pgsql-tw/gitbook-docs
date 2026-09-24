<a id="PLPGSQL-CONTROL-STRUCTURES"></a>

## 41.6. 控制結構 [#](#PLPGSQL-CONTROL-STRUCTURES)

[41.6.1. 從函式回傳](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING)

[41.6.2. 從程序回傳](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

[41.6.3. 呼叫程序](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

[41.6.4. 條件式](plpgsql-control-structures.md#PLPGSQL-CONDITIONALS)

[41.6.5. 簡單迴圈](plpgsql-control-structures.md#PLPGSQL-CONTROL-STRUCTURES-LOOPS)

[41.6.6. 走訪查詢結果](plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING)

[41.6.7. 走訪陣列](plpgsql-control-structures.md#PLPGSQL-FOREACH-ARRAY)

[41.6.8. 捕捉錯誤](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)

[41.6.9. 取得執行位置資訊](plpgsql-control-structures.md#PLPGSQL-CALL-STACK)

控制結構大概是 PL/pgSQL 之中最有用（也最重要）的部分。有了 PL/pgSQL 的控制結構，你就能以非常靈活而強大的方式操作 PostgreSQL 的資料。

<a id="PLPGSQL-STATEMENTS-RETURNING"></a>

### 41.6.1. 從函式回傳 [#](#PLPGSQL-STATEMENTS-RETURNING)

有兩個指令可以讓你從函式回傳資料：`RETURN` 與 `RETURN
NEXT`。

<a id="PLPGSQL-STATEMENTS-RETURNING-RETURN"></a>

#### 41.6.1.1. `RETURN` [#](#PLPGSQL-STATEMENTS-RETURNING-RETURN)

```

RETURN expression;
```

帶有運算式的 `RETURN` 會終止函式，並把 *`expression`* 的值回傳給呼叫端。這個形式用於不回傳集合的 PL/pgSQL 函式。

在回傳純量型別的函式中，運算式的結果會自動被轉換成函式的回傳型別，作法與指派時所述相同。但若要回傳複合（資料列）值，你必須寫出剛好產生所要求之欄位集合的運算式。這可能需要使用明確的型別轉換。

如果你宣告函式時帶有輸出參數，就只要寫 `RETURN` 而不加運算式。輸出參數變數當下的值將會被回傳。

如果你把函式宣告為回傳 `void`，可以用 `RETURN` 陳述式提早離開函式；但是不要在 `RETURN` 之後寫運算式。

函式的回傳值不能保持未定義。如果控制流程走到函式最上層區塊的結尾卻沒有遇到 `RETURN` 陳述式，就會發生執行期錯誤。不過，這項限制不適用於帶有輸出參數的函式以及回傳 `void` 的函式。在那些情況下，只要最上層區塊結束，就會自動執行一個 `RETURN` 陳述式。

一些範例：

```

-- functions returning a scalar type
RETURN 1 + 2;
RETURN scalar_var;

-- functions returning a composite type
RETURN composite_type_var;
RETURN (1, 2, 'three'::text);  -- must cast columns to correct types
```

<a id="PLPGSQL-STATEMENTS-RETURNING-RETURN-NEXT"></a>

#### 41.6.1.2. `RETURN NEXT` 與 `RETURN QUERY` [#](#PLPGSQL-STATEMENTS-RETURNING-RETURN-NEXT)

<a id="id-1.8.8.8.3.4.2"></a><a id="id-1.8.8.8.3.4.3"></a>

```

RETURN NEXT expression;
RETURN QUERY query;
RETURN QUERY EXECUTE command-string [ USING expression [, ... ] ];
```

當 PL/pgSQL 函式被宣告為回傳 `SETOF sometype` 時，接下來的作法就稍有不同。在那種情況下，要回傳的個別項目是以一連串的 `RETURN
NEXT` 或 `RETURN QUERY` 指令來指定，最後再用一個不帶引數的 `RETURN` 指令表示函式已執行完畢。`RETURN NEXT` 可以用於純量與複合資料型別；若是複合的結果型別，就會回傳一整個結果「資料表」。`RETURN QUERY` 會把執行某個查詢的結果附加到函式的結果集合上。`RETURN
NEXT` 與 `RETURN QUERY` 可以在同一個集合回傳函式中自由混用，在那種情況下它們的結果會被串接起來。

`RETURN NEXT` 與 `RETURN
QUERY` 實際上並不會從函式回傳——它們只是把零筆或多筆資料列附加到函式的結果集合上。接著執行流程會繼續進行到 PL/pgSQL 函式中的下一個陳述式。隨著一個接一個的 `RETURN NEXT` 或 `RETURN
QUERY` 指令被執行，結果集合就逐步被建立起來。最後一個不應帶有引數的 `RETURN` 會讓控制流程離開函式（或者你也可以就讓控制流程走到函式的結尾）。

`RETURN QUERY` 有一個變化形式 `RETURN QUERY EXECUTE`，用來指定要動態執行的查詢。參數運算式可以透過 `USING` 插入到所計算出的查詢字串中，作法與 `EXECUTE` 指令完全相同。

如果你宣告函式時帶有輸出參數，就只要寫 `RETURN NEXT` 而不加運算式。每次執行時，輸出參數變數當下的值都會被儲存下來，最終作為結果的一筆資料列回傳。請注意，若要建立帶有輸出參數的集合回傳函式，當有多個輸出參數時，你必須把函式宣告為回傳 `SETOF record`；而當只有一個型別為 *`sometype`* 的輸出參數時，則宣告為回傳 `SETOF sometype`。

以下是一個使用 `RETURN
NEXT` 的函式範例：

```

CREATE TABLE foo (fooid INT, foosubid INT, fooname TEXT);
INSERT INTO foo VALUES (1, 2, 'three');
INSERT INTO foo VALUES (4, 5, 'six');

CREATE OR REPLACE FUNCTION get_all_foo() RETURNS SETOF foo AS
$BODY$
DECLARE
    r foo%rowtype;
BEGIN
    FOR r IN
        SELECT * FROM foo WHERE fooid > 0
    LOOP
        -- can do some processing here
        RETURN NEXT r; -- return current row of SELECT
    END LOOP;
    RETURN;
END;
$BODY$
LANGUAGE plpgsql;

SELECT * FROM get_all_foo();
```

以下是一個使用 `RETURN
QUERY` 的函式範例：

```

CREATE FUNCTION get_available_flightid(date) RETURNS SETOF integer AS
$BODY$
BEGIN
    RETURN QUERY SELECT flightid
                   FROM flight
                  WHERE flightdate >= $1
                    AND flightdate < ($1 + 1);

    -- Since execution is not finished, we can check whether rows were returned
    -- and raise exception if not.
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No flight at %.', $1;
    END IF;

    RETURN;
 END;
$BODY$
LANGUAGE plpgsql;

-- Returns available flights or raises exception if there are no
-- available flights.
SELECT * FROM get_available_flightid(CURRENT_DATE);
```

### 注意

如上所述，`RETURN NEXT` 與 `RETURN QUERY` 目前的實作方式，會在從函式回傳之前先儲存整個結果集合。這表示如果一個 PL/pgSQL 函式產生非常龐大的結果集合，效能可能會很差：資料會被寫到磁碟以避免記憶體耗盡，但函式本身仍須等到整個結果集合都產生完畢才會回傳。未來版本的 PL/pgSQL 或許會允許使用者定義沒有這項限制的集合回傳函式。目前，資料開始被寫到磁碟的時機是由 [work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-WORK-MEM) 組態變數所控制。如果管理者有足夠的記憶體把較大的結果集合存放在記憶體中，就應該考慮調高這個參數。

<a id="PLPGSQL-STATEMENTS-RETURNING-PROCEDURE"></a>

### 41.6.2. 從程序回傳 [#](#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)

程序沒有回傳值。因此程序可以在沒有 `RETURN` 陳述式的情況下結束。如果你希望用 `RETURN` 陳述式提早離開程式碼，就只要寫 `RETURN` 而不加運算式。

如果程序帶有輸出參數，輸出參數變數的最終值會被回傳給呼叫端。

<a id="PLPGSQL-STATEMENTS-CALLING-PROCEDURE"></a>

### 41.6.3. 呼叫程序 [#](#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)

PL/pgSQL 的函式、程序或 `DO` 區塊可以使用 `CALL` 呼叫程序。輸出參數的處理方式與 `CALL` 在純 SQL 中的運作方式不同。程序的每一個 `OUT` 或 `INOUT` 參數都必須對應到 `CALL` 陳述式中的一個變數，程序回傳之後，它所回傳的內容便會被指派回該變數。例如：

```

CREATE PROCEDURE triple(INOUT x int)
LANGUAGE plpgsql
AS $$
BEGIN
    x := x * 3;
END;
$$;

DO $$
DECLARE myvar int := 5;
BEGIN
  CALL triple(myvar);
  RAISE NOTICE 'myvar = %', myvar;  -- prints 15
END;
$$;
```

對應到輸出參數的變數可以是簡單變數，也可以是複合型別變數的一個欄位。目前它還不能是陣列的元素。

<a id="PLPGSQL-CONDITIONALS"></a>

### 41.6.4. 條件式 [#](#PLPGSQL-CONDITIONALS)

`IF` 與 `CASE` 陳述式讓你可以依據特定條件執行不同的指令。PL/pgSQL 有三種形式的 `IF`：

* `IF ... THEN ... END IF`
* `IF ... THEN ... ELSE ... END IF`
* `IF ... THEN ... ELSIF ... THEN ... ELSE ... END IF`

以及兩種形式的 `CASE`：

* `CASE ... WHEN ... THEN ... ELSE ... END CASE`
* `CASE WHEN ... THEN ... ELSE ... END CASE`

<a id="PLPGSQL-CONDITIONALS-IF-THEN"></a>

#### 41.6.4.1. `IF-THEN` [#](#PLPGSQL-CONDITIONALS-IF-THEN)

```

IF boolean-expression THEN
    statements
END IF;
```

`IF-THEN` 陳述式是 `IF` 最簡單的形式。如果條件為真，位於 `THEN` 與 `END IF` 之間的陳述式就會被執行。否則它們會被略過。

範例：

```

IF v_user_id <> 0 THEN
    UPDATE users SET email = v_email WHERE user_id = v_user_id;
END IF;
```

<a id="PLPGSQL-CONDITIONALS-IF-THEN-ELSE"></a>

#### 41.6.4.2. `IF-THEN-ELSE` [#](#PLPGSQL-CONDITIONALS-IF-THEN-ELSE)

```

IF boolean-expression THEN
    statements
ELSE
    statements
END IF;
```

`IF-THEN-ELSE` 陳述式在 `IF-THEN` 的基礎上，讓你可以指定當條件不為真時應該執行的另一組陳述式。（請注意，這也包含條件求值結果為 NULL 的情況。）

範例：

```

IF parentid IS NULL OR parentid = ''
THEN
    RETURN fullname;
ELSE
    RETURN hp_true_filename(parentid) || '/' || fullname;
END IF;
```

```

IF v_count > 0 THEN
    INSERT INTO users_count (count) VALUES (v_count);
    RETURN 't';
ELSE
    RETURN 'f';
END IF;
```

<a id="PLPGSQL-CONDITIONALS-IF-THEN-ELSIF"></a>

#### 41.6.4.3. `IF-THEN-ELSIF` [#](#PLPGSQL-CONDITIONALS-IF-THEN-ELSIF)

```

IF boolean-expression THEN
    statements
[ ELSIF boolean-expression THEN
    statements
[ ELSIF boolean-expression THEN
    statements
    ...
]
]
[ ELSE
    statements ]
END IF;
```

有時候可供選擇的分支不只兩個。`IF-THEN-ELSIF` 提供了一個方便的方法，可以依序檢查數個分支。各個 `IF` 條件會被依序測試，直到找到第一個為真的條件為止。接著與它相關聯的陳述式就會被執行，之後控制流程便轉移到 `END IF` 之後的下一個陳述式。（後續的 `IF` 條件*不會*被測試。）如果沒有任何一個 `IF` 條件為真，那麼 `ELSE` 區塊（若有的話）就會被執行。

以下是一個範例：

```

IF number = 0 THEN
    result := 'zero';
ELSIF number > 0 THEN
    result := 'positive';
ELSIF number < 0 THEN
    result := 'negative';
ELSE
    -- hmm, the only other possibility is that number is null
    result := 'NULL';
END IF;
```

關鍵字 `ELSIF` 也可以寫成 `ELSEIF`。

達成同樣工作的另一種方式，是把 `IF-THEN-ELSE` 陳述式巢狀化，如下面的範例：

```

IF demo_row.sex = 'm' THEN
    pretty_sex := 'man';
ELSE
    IF demo_row.sex = 'f' THEN
        pretty_sex := 'woman';
    END IF;
END IF;
```

然而，這個方法必須為每一個 `IF` 都寫上對應的 `END IF`，因此在分支很多的時候，會比使用 `ELSIF` 麻煩許多。

<a id="PLPGSQL-CONDITIONALS-SIMPLE-CASE"></a>

#### 41.6.4.4. 簡單 `CASE` [#](#PLPGSQL-CONDITIONALS-SIMPLE-CASE)

```

CASE search-expression
    WHEN expression [, expression [ ... ]] THEN
      statements
  [ WHEN expression [, expression [ ... ]] THEN
      statements
    ... ]
  [ ELSE
      statements ]
END CASE;
```

`CASE` 的簡單形式依據運算元是否相等來提供條件執行。*`search-expression`* 會被求值（一次），並依序與 `WHEN` 子句中的每一個 *`expression`* 比較。如果找到相符者，就執行對應的 *`statements`*，然後控制流程轉移到 `END CASE` 之後的下一個陳述式。（後續的 `WHEN` 運算式不會被求值。）如果沒有找到相符者，就執行 `ELSE` 的 *`statements`*；但如果沒有 `ELSE`，則會拋出 `CASE_NOT_FOUND` 例外。

以下是一個簡單的範例：

```

CASE x
    WHEN 1, 2 THEN
        msg := 'one or two';
    ELSE
        msg := 'other value than one or two';
END CASE;
```

<a id="PLPGSQL-CONDITIONALS-SEARCHED-CASE"></a>

#### 41.6.4.5. 搜尋式 `CASE` [#](#PLPGSQL-CONDITIONALS-SEARCHED-CASE)

```

CASE
    WHEN boolean-expression THEN
      statements
  [ WHEN boolean-expression THEN
      statements
    ... ]
  [ ELSE
      statements ]
END CASE;
```

`CASE` 的搜尋形式依據布林運算式是否為真來提供條件執行。每一個 `WHEN` 子句的 *`boolean-expression`* 會被依序求值，直到找到一個結果為 `true` 者為止。接著對應的 *`statements`* 就會被執行，然後控制流程轉移到 `END CASE` 之後的下一個陳述式。（後續的 `WHEN` 運算式不會被求值。）如果沒有找到為真的結果，就執行 `ELSE` 的 *`statements`*；但如果沒有 `ELSE`，則會拋出 `CASE_NOT_FOUND` 例外。

以下是一個範例：

```

CASE
    WHEN x BETWEEN 0 AND 10 THEN
        msg := 'value is between zero and ten';
    WHEN x BETWEEN 11 AND 20 THEN
        msg := 'value is between eleven and twenty';
END CASE;
```

這種形式的 `CASE` 完全等同於 `IF-THEN-ELSIF`，差別只在於：走到被省略的 `ELSE` 子句時會導致錯誤，而不是什麼事都不做。

<a id="PLPGSQL-CONTROL-STRUCTURES-LOOPS"></a>

### 41.6.5. 簡單迴圈 [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS)

<a id="id-1.8.8.8.7.2"></a>

有了 `LOOP`、`EXIT`、`CONTINUE`、`WHILE`、`FOR` 與 `FOREACH` 陳述式，你可以讓你的 PL/pgSQL 函式重複執行一系列的指令。

<a id="PLPGSQL-CONTROL-STRUCTURES-LOOPS-LOOP"></a>

#### 41.6.5.1. `LOOP` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-LOOP)

```

[ <<label>> ]
LOOP
    statements
END LOOP [ label ];
```

`LOOP` 定義一個無條件的迴圈，會無止境地重複下去，直到被 `EXIT` 或 `RETURN` 陳述式終止為止。選用的 *`label`* 可以被巢狀迴圈中的 `EXIT` 與 `CONTINUE` 陳述式用來指定那些陳述式所指的是哪一個迴圈。

<a id="PLPGSQL-CONTROL-STRUCTURES-LOOPS-EXIT"></a>

#### 41.6.5.2. `EXIT` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-EXIT)

<a id="id-1.8.8.8.7.5.2"></a>

```

EXIT [ label ] [ WHEN boolean-expression ];
```

如果沒有給定 *`label`*，最內層的迴圈會被終止，接著執行 `END
LOOP` 之後的陳述式。如果有給定 *`label`*，它必須是目前這一層或某個外層巢狀迴圈或區塊的標籤。接著具名的那個迴圈或區塊會被終止，控制流程從該迴圈／區塊所對應的 `END` 之後的陳述式繼續。

如果有指定 `WHEN`，只有在 *`boolean-expression`* 為真時才會離開迴圈。否則控制流程會轉移到 `EXIT` 之後的陳述式。

`EXIT` 可以用於所有類型的迴圈；它並不限於用在無條件迴圈。

當與 `BEGIN` 區塊搭配使用時，`EXIT` 會把控制流程轉移到該區塊結束之後的下一個陳述式。請注意，為此必須使用標籤；沒有標籤的 `EXIT` 永遠不會被視為與 `BEGIN` 區塊相符。（這是相對於 PostgreSQL 8.4 之前版本的一項變更，那些版本會允許沒有標籤的 `EXIT` 與 `BEGIN` 區塊相符。）

範例：

```

LOOP
    -- some computations
    IF count > 0 THEN
        EXIT;  -- exit loop
    END IF;
END LOOP;

LOOP
    -- some computations
    EXIT WHEN count > 0;  -- same result as previous example
END LOOP;

<<ablock>>
BEGIN
    -- some computations
    IF stocks > 100000 THEN
        EXIT ablock;  -- causes exit from the BEGIN block
    END IF;
    -- computations here will be skipped when stocks > 100000
END;
```

<a id="PLPGSQL-CONTROL-STRUCTURES-LOOPS-CONTINUE"></a>

#### 41.6.5.3. `CONTINUE` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-CONTINUE)

<a id="id-1.8.8.8.7.6.2"></a>

```

CONTINUE [ label ] [ WHEN boolean-expression ];
```

如果沒有給定 *`label`*，就開始最內層迴圈的下一次迭代。也就是說，迴圈主體中剩下的所有陳述式都會被略過，控制流程回到迴圈的控制運算式（若有的話），以判斷是否還需要再進行一次迭代。如果有 *`label`*，它會指定要繼續執行的是哪一個迴圈的標籤。

如果有指定 `WHEN`，只有在 *`boolean-expression`* 為真時才會開始迴圈的下一次迭代。否則控制流程會轉移到 `CONTINUE` 之後的陳述式。

`CONTINUE` 可以用於所有類型的迴圈；它並不限於用在無條件迴圈。

範例：

```

LOOP
    -- some computations
    EXIT WHEN count > 100;
    CONTINUE WHEN count < 50;
    -- some computations for count IN [50 .. 100]
END LOOP;
```

<a id="PLPGSQL-CONTROL-STRUCTURES-LOOPS-WHILE"></a>

#### 41.6.5.4. `WHILE` [#](#PLPGSQL-CONTROL-STRUCTURES-LOOPS-WHILE)

<a id="id-1.8.8.8.7.7.2"></a>

```

[ <<label>> ]
WHILE boolean-expression LOOP
    statements
END LOOP [ label ];
```

只要 *`boolean-expression`* 的求值結果為真，`WHILE` 陳述式就會重複執行一系列的陳述式。這個運算式會在每次進入迴圈主體之前檢查。

例如：

```

WHILE amount_owed > 0 AND gift_certificate_balance > 0 LOOP
    -- some computations here
END LOOP;

WHILE NOT done LOOP
    -- some computations here
END LOOP;
```

<a id="PLPGSQL-INTEGER-FOR"></a>

#### 41.6.5.5. `FOR`（整數形式） [#](#PLPGSQL-INTEGER-FOR)

```

[ <<label>> ]
FOR name IN [ REVERSE ] expression .. expression [ BY expression ] LOOP
    statements
END LOOP [ label ];
```

這種形式的 `FOR` 會建立一個走訪某個整數值範圍的迴圈。變數 *`name`* 會自動被定義為 `integer` 型別，而且只存在於迴圈之內（該變數名稱既有的任何定義，在迴圈中都會被忽略）。給定範圍下界與上界的那兩個運算式，會在進入迴圈時求值一次。如果沒有指定 `BY` 子句，迭代的步進值為 1，否則就是 `BY` 子句中所指定的值，這個值同樣會在進入迴圈時求值一次。如果有指定 `REVERSE`，那麼每次迭代之後就是減去步進值，而不是加上去。

一些整數 `FOR` 迴圈的範例：

```

FOR i IN 1..10 LOOP
    -- i will take on the values 1,2,3,4,5,6,7,8,9,10 within the loop
END LOOP;

FOR i IN REVERSE 10..1 LOOP
    -- i will take on the values 10,9,8,7,6,5,4,3,2,1 within the loop
END LOOP;

FOR i IN REVERSE 10..1 BY 2 LOOP
    -- i will take on the values 10,8,6,4,2 within the loop
END LOOP;
```

如果下界大於上界（在 `REVERSE` 的情況下則是小於），迴圈主體完全不會被執行。並不會拋出錯誤。

如果 `FOR` 迴圈附有 *`label`*，那麼就可以用該 *`label`* 以限定名稱的方式參照這個整數迴圈變數。

<a id="PLPGSQL-RECORDS-ITERATING"></a>

### 41.6.6. 走訪查詢結果 [#](#PLPGSQL-RECORDS-ITERATING)

使用另一種類型的 `FOR` 迴圈，你可以走訪某個查詢的結果，並據以操作那些資料。語法是：

```

[ <<label>> ]
FOR target IN query LOOP
    statements
END LOOP [ label ];
```

*`target`* 是一個 record（記錄）變數、資料列變數，或是以逗號分隔的純量變數清單。*`target`* 會依序被指派 *`query`* 所產生的每一筆資料列，而迴圈主體則會針對每一筆資料列執行。以下是一個範例：

```

CREATE FUNCTION refresh_mviews() RETURNS integer AS $$
DECLARE
    mviews RECORD;
BEGIN
    RAISE NOTICE 'Refreshing all materialized views...';

    FOR mviews IN
       SELECT n.nspname AS mv_schema,
              c.relname AS mv_name,
              pg_catalog.pg_get_userbyid(c.relowner) AS owner
         FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_namespace n ON (n.oid = c.relnamespace)
        WHERE c.relkind = 'm'
     ORDER BY 1
    LOOP

        -- Now "mviews" has one record with information about the materialized view

        RAISE NOTICE 'Refreshing materialized view %.% (owner: %)...',
                     quote_ident(mviews.mv_schema),
                     quote_ident(mviews.mv_name),
                     quote_ident(mviews.owner);
        EXECUTE format('REFRESH MATERIALIZED VIEW %I.%I', mviews.mv_schema, mviews.mv_name);
    END LOOP;

    RAISE NOTICE 'Done refreshing materialized views.';
    RETURN 1;
END;
$$ LANGUAGE plpgsql;
```

如果迴圈是被 `EXIT` 陳述式終止的，最後被指派的那筆資料列值在迴圈之後仍然可以存取。

這類 `FOR` 陳述式所使用的 *`query`* 可以是任何會回傳資料列給呼叫端的 SQL 指令：最常見的情況是 `SELECT`，但你也可以使用帶有 `RETURNING` 子句的 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE`。某些工具指令，例如 `EXPLAIN`，也同樣可行。

PL/pgSQL 變數會被替換成查詢參數，而查詢計畫會被快取以便可能的重複使用，詳見 [第 41.11.1 節](plpgsql-implementation.md#PLPGSQL-VAR-SUBST) 與 [第 41.11.2 節](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)。

`FOR-IN-EXECUTE` 陳述式是走訪資料列的另一種方式：

```

[ <<label>> ]
FOR target IN EXECUTE text_expression [ USING expression [, ... ] ] LOOP
    statements
END LOOP [ label ];
```

這與前面的形式類似，差別在於來源查詢是以字串運算式來指定，而該運算式會在每次進入 `FOR` 迴圈時被求值並重新規劃。這讓程式設計者可以選擇預先規劃之查詢的速度，或是動態查詢的彈性，就和一般的 `EXECUTE` 陳述式一樣。與 `EXECUTE` 相同，參數值可以透過 `USING` 插入到動態指令中。

要指定其結果應被走訪的查詢，還有另一種方式，就是把它宣告為一個游標。這在 [第 41.7.4 節](plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP) 中說明。

<a id="PLPGSQL-FOREACH-ARRAY"></a>

### 41.6.7. 走訪陣列 [#](#PLPGSQL-FOREACH-ARRAY)

`FOREACH` 迴圈與 `FOR` 迴圈非常相似，但是它走訪的不是 SQL 查詢所回傳的資料列，而是某個陣列值的元素。（一般而言，`FOREACH` 的用意是走訪複合值運算式的各個組成部分；未來可能會加入走訪陣列以外之複合值的變化形式。）用來走訪陣列的 `FOREACH` 陳述式是：

```

[ <<label>> ]
FOREACH target [ SLICE number ] IN ARRAY expression LOOP
    statements
END LOOP [ label ];
```

若不使用 `SLICE`，或是指定 `SLICE 0`，迴圈會走訪由 *`expression`* 求值所產生之陣列的個別元素。*`target`* 變數會依序被指派每一個元素值，而迴圈主體則會針對每一個元素執行。以下是一個走訪整數陣列元素的範例：

```

CREATE FUNCTION sum(int[]) RETURNS int8 AS $$
DECLARE
  s int8 := 0;
  x int;
BEGIN
  FOREACH x IN ARRAY $1
  LOOP
    s := s + x;
  END LOOP;
  RETURN s;
END;
$$ LANGUAGE plpgsql;
```

不論陣列有幾個維度，元素都是依照儲存順序被走訪。雖然 *`target`* 通常只是單一個變數，但是在走訪由複合值（record）所組成的陣列時，它也可以是一份變數清單。在那種情況下，對於每一個陣列元素，這些變數會依序從複合值的各個欄位取得指派值。

若 `SLICE` 值為正數，`FOREACH` 走訪的就是陣列的切片，而不是單一元素。`SLICE` 值必須是不大於陣列維度數的整數常數。*`target`* 變數必須是一個陣列，它會依序接收陣列值的各個切片，而每一個切片的維度數則由 `SLICE` 所指定。以下是一個走訪一維切片的範例：

```

CREATE FUNCTION scan_rows(int[]) RETURNS void AS $$
DECLARE
  x int[];
BEGIN
  FOREACH x SLICE 1 IN ARRAY $1
  LOOP
    RAISE NOTICE 'row = %', x;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT scan_rows(ARRAY[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]);

NOTICE:  row = {1,2,3}
NOTICE:  row = {4,5,6}
NOTICE:  row = {7,8,9}
NOTICE:  row = {10,11,12}
```

<a id="PLPGSQL-ERROR-TRAPPING"></a>

### 41.6.8. 捕捉錯誤 [#](#PLPGSQL-ERROR-TRAPPING)

<a id="id-1.8.8.8.10.2"></a>

在預設情況下，PL/pgSQL 函式中發生的任何錯誤都會中止該函式以及外圍交易的執行。你可以使用帶有 `EXCEPTION` 子句的 `BEGIN` 區塊來捕捉錯誤並從中復原。其語法是 `BEGIN` 區塊一般語法的延伸：

```

[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
EXCEPTION
    WHEN condition [ OR condition ... ] THEN
        handler_statements
    [ WHEN condition [ OR condition ... ] THEN
          handler_statements
      ... ]
END;
```

如果沒有發生錯誤，這種形式的區塊就只是執行所有的 *`statements`*，然後控制流程轉移到 `END` 之後的下一個陳述式。但如果在這些 *`statements`* 之中發生錯誤，對 *`statements`* 的後續處理就會被放棄，控制流程轉移到 `EXCEPTION` 清單。系統會在該清單中尋找第一個與所發生之錯誤相符的 *`condition`*。如果找到相符者，就執行對應的 *`handler_statements`*，然後控制流程轉移到 `END` 之後的下一個陳述式。如果沒有找到相符者，錯誤就會向外傳播，彷彿 `EXCEPTION` 子句根本不存在一般：該錯誤可以被外圍帶有 `EXCEPTION` 的區塊捕捉，如果沒有這樣的區塊，它就會中止該函式的處理。

*`condition`* 名稱可以是 [附錄 A](../../appendixes/errcodes-appendix/README.md) 中所列出的任何一個。類別名稱會與其類別之內的任何錯誤相符。特殊的條件名稱 `OTHERS` 會與除了 `QUERY_CANCELED` 與 `ASSERT_FAILURE` 以外的每一種錯誤型別相符。（要依名稱捕捉那兩種錯誤型別是可行的，但通常並不明智。）條件名稱不區分大小寫。此外，錯誤條件也可以用 `SQLSTATE` 碼來指定；例如下列兩者是等價的：

```

WHEN division_by_zero THEN ...
WHEN SQLSTATE '22012' THEN ...
```

如果在所選定的 *`handler_statements`* 之中發生新的錯誤，它無法被這個 `EXCEPTION` 子句捕捉，而是會向外傳播。外圍的 `EXCEPTION` 子句則有可能捕捉到它。

當錯誤被 `EXCEPTION` 子句捕捉時，PL/pgSQL 函式的區域變數會維持在錯誤發生當下的狀態，但是該區塊之內對持續性資料庫狀態所做的所有變更都會被回復。舉例來說，考慮下面這段程式片段：

```

INSERT INTO mytab(firstname, lastname) VALUES('Tom', 'Jones');
BEGIN
    UPDATE mytab SET firstname = 'Joe' WHERE lastname = 'Jones';
    x := x + 1;
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'caught division_by_zero';
        RETURN x;
END;
```

當控制流程走到對 `y` 的指派時，它會以 `division_by_zero` 錯誤失敗。這個錯誤會被 `EXCEPTION` 子句捕捉。`RETURN` 陳述式所回傳的值會是遞增之後的 `x` 值，但是 `UPDATE` 指令的效果則已經被回復。不過，位於該區塊之前的 `INSERT` 指令並不會被回復，所以最終的結果是資料庫中存放的是 `Tom Jones` 而不是 `Joe Jones`。

### 提示

含有 `EXCEPTION` 子句的區塊，其進入與離開的成本明顯高於沒有該子句的區塊。因此，不要在沒有必要時使用 `EXCEPTION`。

<a id="PLPGSQL-UPSERT-EXAMPLE"></a>

**範例 41.2. 搭配 `UPDATE`/`INSERT` 的例外處理**

這個範例使用例外處理，視情況執行 `UPDATE` 或 `INSERT`。建議應用程式使用帶有 `ON CONFLICT DO UPDATE` 的 `INSERT`，而不要真的採用這種模式。這個範例的主要用意是示範 PL/pgSQL 控制流程結構的用法：

```

CREATE TABLE db (a INT PRIMARY KEY, b TEXT);

CREATE FUNCTION merge_db(key INT, data TEXT) RETURNS VOID AS
$$
BEGIN
    LOOP
        -- first try to update the key
        UPDATE db SET b = data WHERE a = key;
        IF found THEN
            RETURN;
        END IF;
        -- not there, so try to insert the key
        -- if someone else inserts the same key concurrently,
        -- we could get a unique-key failure
        BEGIN
            INSERT INTO db(a,b) VALUES (key, data);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

SELECT merge_db(1, 'david');
SELECT merge_db(1, 'dennis');
```

這段程式碼假設 `unique_violation` 錯誤是由該 `INSERT` 所造成，而不是由例如該資料表上某個觸發程序函式中的 `INSERT` 所造成。如果該資料表上有一個以上的唯一值索引，它也可能會有不正確的行為，因為不論錯誤是由哪一個索引所引起，它都會重試該操作。若使用接下來要討論的功能來檢查所捕捉到的錯誤是否就是所預期的那一個，就能得到更高的安全性。

<br><a id="PLPGSQL-EXCEPTION-DIAGNOSTICS"></a>

#### 41.6.8.1. 取得錯誤的相關資訊 [#](#PLPGSQL-EXCEPTION-DIAGNOSTICS)

例外處理常式經常需要識別發生的特定錯誤。在 PL/pgSQL 中有兩種方式可以取得目前例外的相關資訊：特殊變數，以及 `GET STACKED DIAGNOSTICS` 指令。

在例外處理常式之內，特殊變數 `SQLSTATE` 含有對應於所拋出之例外的錯誤碼（可能的錯誤碼清單請參閱 [表 A.1](../../appendixes/errcodes-appendix/README.md#ERRCODES-TABLE)）。特殊變數 `SQLERRM` 則含有與該例外相關聯的錯誤訊息。這些變數在例外處理常式之外是未定義的。

在例外處理常式之內，也可以使用 `GET STACKED DIAGNOSTICS` 指令取得目前例外的相關資訊，其形式為：

```

GET STACKED DIAGNOSTICS variable { = | := } item [ , ... ];
```

每一個 *`item`* 都是一個關鍵字，用以指出要指派給指定之 *`variable`*（其資料型別應該要能接收該值）的狀態值。目前可用的狀態項目列於 [表 41.2](plpgsql-control-structures.md#PLPGSQL-EXCEPTION-DIAGNOSTICS-VALUES)。

<a id="PLPGSQL-EXCEPTION-DIAGNOSTICS-VALUES"></a>

**表 41.2. 錯誤診斷資訊項目**

<table border="1" class="table" summary="錯誤診斷資訊項目"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">RETURNED_SQLSTATE</code></td><td><code class="type">text</code></td><td>該例外的 SQLSTATE 錯誤碼</td></tr><tr><td><code class="literal">COLUMN_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之欄位的名稱</td></tr><tr><td><code class="literal">CONSTRAINT_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之限制條件的名稱</td></tr><tr><td><code class="literal">PG_DATATYPE_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之資料型別的名稱</td></tr><tr><td><code class="literal">MESSAGE_TEXT</code></td><td><code class="type">text</code></td><td>該例外主要訊息的文字內容</td></tr><tr><td><code class="literal">TABLE_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之資料表的名稱</td></tr><tr><td><code class="literal">SCHEMA_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之綱要的名稱</td></tr><tr><td><code class="literal">PG_EXCEPTION_DETAIL</code></td><td><code class="type">text</code></td><td>該例外詳細訊息的文字內容（若有的話）</td></tr><tr><td><code class="literal">PG_EXCEPTION_HINT</code></td><td><code class="type">text</code></td><td>該例外提示訊息的文字內容（若有的話）</td></tr><tr><td><code class="literal">PG_EXCEPTION_CONTEXT</code></td><td><code class="type">text</code></td><td>描述例外發生當時之呼叫堆疊的文字行（見 <a class="xref" href="plpgsql-control-structures.md#PLPGSQL-CALL-STACK">第 41.6.9 節</a>）</td></tr></tbody></table>

<br>

如果該例外並未為某個項目設定值，回傳的就會是空字串。

以下是一個範例：

```

DECLARE
  text_var1 text;
  text_var2 text;
  text_var3 text;
BEGIN
  -- some processing which might cause an exception
  ...
EXCEPTION WHEN OTHERS THEN
  GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
                          text_var2 = PG_EXCEPTION_DETAIL,
                          text_var3 = PG_EXCEPTION_HINT;
END;
```

<a id="PLPGSQL-CALL-STACK"></a>

### 41.6.9. 取得執行位置資訊 [#](#PLPGSQL-CALL-STACK)

先前在 [第 41.5.5 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS) 中所述的 `GET DIAGNOSTICS` 指令，會取得目前執行狀態的相關資訊（而上面討論的 `GET STACKED
DIAGNOSTICS` 指令則是回報先前某個錯誤發生當時之執行狀態的資訊）。它的 `PG_CONTEXT` 狀態項目對於辨識目前的執行位置很有用。`PG_CONTEXT` 會回傳一個文字字串，其中含有描述呼叫堆疊的文字行。第一行指的是目前的函式以及目前正在執行的 `GET DIAGNOSTICS` 指令。第二行以及後續各行指的則是呼叫堆疊中更上層的呼叫端函式。例如：

```

CREATE OR REPLACE FUNCTION outer_func() RETURNS integer AS $$
BEGIN
  RETURN inner_func();
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION inner_func() RETURNS integer AS $$
DECLARE
  stack text;
BEGIN
  GET DIAGNOSTICS stack = PG_CONTEXT;
  RAISE NOTICE E'--- Call Stack ---\n%', stack;
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

SELECT outer_func();

NOTICE:  --- Call Stack ---
PL/pgSQL function inner_func() line 5 at GET DIAGNOSTICS
PL/pgSQL function outer_func() line 3 at RETURN
CONTEXT:  PL/pgSQL function outer_func() line 3 at RETURN
 outer_func
 ------------
           1
(1 row)
```

`GET STACKED DIAGNOSTICS ... PG_EXCEPTION_CONTEXT` 會回傳同一類的堆疊追蹤，但描述的是偵測到錯誤的位置，而不是目前的位置。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-control-structures.html)（原文版本：18.6；核對日期：2026-09-24）
