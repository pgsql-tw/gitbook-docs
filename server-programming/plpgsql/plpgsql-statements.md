<a id="PLPGSQL-STATEMENTS"></a>

## 41.5. 基本陳述式 [#](#PLPGSQL-STATEMENTS)

[41.5.1. 指派](plpgsql-statements.md#PLPGSQL-STATEMENTS-ASSIGNMENT)

[41.5.2. 執行 SQL 指令](plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)

[41.5.3. 執行只回傳單一資料列的指令](plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)

[41.5.4. 執行動態指令](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)

[41.5.5. 取得結果狀態](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)

[41.5.6. 什麼都不做](plpgsql-statements.md#PLPGSQL-STATEMENTS-NULL)

在本節與接下來的幾節中，我們會說明所有 PL/pgSQL 明確認得的陳述式型式。任何不被認定為這些陳述式型式之一的東西，都會被視為是一個 SQL 指令，並送到主要的資料庫引擎去執行，如[第 41.5.2 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)所述。

<a id="PLPGSQL-STATEMENTS-ASSIGNMENT"></a>

### 41.5.1. 指派 [#](#PLPGSQL-STATEMENTS-ASSIGNMENT)

要把一個值指派給 PL/pgSQL 變數，寫法是：

```

variable { := | = } expression;
```

如同先前所解釋的，這種陳述式中的運算式，是藉由送往主要資料庫引擎的一個 SQL `SELECT` 指令來計算的。該運算式必須產生單一一個值（如果變數是資料列變數或 record 變數，也可以是一個資料列值）。目標變數可以是一個簡單變數（可以選擇性地用區塊名稱加以限定）、資料列或 record 目標的一個欄位，或是陣列目標的一個元素或切片。等號（`=`）可以用來取代符合 PL/SQL 規範的 `:=`。

如果運算式的結果資料型別與變數的資料型別不相符，該值會如同經由指派型別轉換一般被強制轉換（參閱[第 10.4 節](../../the-sql-language/typeconv/typeconv-query.md)）。如果所涉及的這組資料型別之間沒有已知的指派型別轉換，PL/pgSQL 直譯器會試著以文字方式轉換該結果值，也就是先套用結果型別的輸出函式，再套用變數型別的輸入函式。請注意，如果結果值的字串形式無法被輸入函式接受，這可能會導致輸入函式產生執行期錯誤。

範例：

```

tax := subtotal * 0.06;
my_record.user_id := 20;
my_array[j] := 20;
my_array[1:3] := array[1,2,3];
complex_array[n].realpart = 12.3;
```

<a id="PLPGSQL-STATEMENTS-GENERAL-SQL"></a>

### 41.5.2. 執行 SQL 指令 [#](#PLPGSQL-STATEMENTS-GENERAL-SQL)

一般來說，任何不回傳資料列的 SQL 指令，只要把該指令寫出來，就可以在 PL/pgSQL 函式中執行。例如，你可以這樣寫來建立一個資料表並填入資料：

```

CREATE TABLE mytable (id int primary key, data text);
INSERT INTO mytable VALUES (1,'one'), (2,'two');
```

如果該指令確實會回傳資料列（例如 `SELECT`，或帶有 `RETURNING` 的 `INSERT`／`UPDATE`／`DELETE`／`MERGE`），則有兩種做法。當該指令最多只會回傳一筆資料列，或是你只在意輸出的第一筆資料列時，照常寫出該指令，但加上一個 `INTO` 子句來擷取輸出，詳見[第 41.5.3 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)。若要處理所有的輸出資料列，就把該指令寫成 `FOR` 迴圈的資料來源，詳見[第 41.6.6 節](plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING)。

通常只執行靜態定義的 SQL 指令是不夠的。一般來說，你會希望指令能使用不同的資料值，甚至希望它在更根本的層面上有所變化，例如在不同時候使用不同的資料表名稱。同樣地，依情況不同有兩種做法。

PL/pgSQL 的變數值可以自動插入到可最佳化的 SQL 指令中，這些指令是 `SELECT`、`INSERT`、`UPDATE`、`DELETE`、`MERGE`，以及某些包含上述指令之一的公用指令，例如 `EXPLAIN` 與 `CREATE TABLE ... AS SELECT`。在這些指令中，任何出現在指令文字裡的 PL/pgSQL 變數名稱都會被替換成一個查詢參數，然後在執行期以該變數目前的值作為參數值提供。這與先前針對運算式所描述的處理方式完全相同；細節請見[第 41.11.1 節](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)。

以這種方式執行可最佳化的 SQL 指令時，PL/pgSQL 可能會快取並重複使用該指令的執行計畫，詳見[第 41.11.2 節](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)。

不可最佳化的 SQL 指令（也稱為公用指令）無法接受查詢參數。因此在這類指令中，PL/pgSQL 變數的自動替換並不會生效。若要在從 PL/pgSQL 執行的公用指令中加入非常數的文字，你必須把該公用指令組成一個字串，然後用 `EXECUTE` 執行它，詳見[第 41.5.4 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)。

如果你想以提供資料值以外的其他方式修改指令，例如更換資料表名稱，也必須使用 `EXECUTE`。

有時候計算一個運算式或 `SELECT` 查詢但捨棄其結果是有用的，例如在呼叫一個有副作用但沒有有用回傳值的函式時。要在 PL/pgSQL 中做到這件事，請使用 `PERFORM` 陳述式：

```

PERFORM query;
```

這會執行 *`query`* 並捨棄其結果。撰寫 *`query`* 的方式和你寫 SQL `SELECT` 指令時一樣，只是把開頭的關鍵字 `SELECT` 換成 `PERFORM`。對於 `WITH` 查詢，請使用 `PERFORM` 然後把查詢放在括號中。（在這種情況下，該查詢只能回傳一筆資料列。）PL/pgSQL 變數會如同上述方式被替換進查詢中，執行計畫也以相同方式快取。此外，如果該查詢產生了至少一筆資料列，特殊變數 `FOUND` 會被設為 true；若沒有產生任何資料列則為 false（參閱[第 41.5.5 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)）。

### 注意

有人可能會以為直接寫 `SELECT` 就能達到這個效果，但目前唯一被接受的做法是 `PERFORM`。像 `SELECT` 這種可能回傳資料列的 SQL 指令，除非帶有下一節所述的 `INTO` 子句，否則會被視為錯誤而遭拒絕。

一個例子：

```

PERFORM create_mv('cs_session_page_requests_mv', my_query);
```

<a id="PLPGSQL-STATEMENTS-SQL-ONEROW"></a>

### 41.5.3. 執行只回傳單一資料列的指令 [#](#PLPGSQL-STATEMENTS-SQL-ONEROW)

<a id="id-1.8.8.7.5.2"></a><a id="id-1.8.8.7.5.3"></a>

產生單一資料列（可能有多個欄位）的 SQL 指令，其結果可以指派給一個 record 變數、資料列型別變數，或是一串純量變數。做法是寫出基本的 SQL 指令並加上 `INTO` 子句。例如，

```

SELECT select_expressions INTO [STRICT] target FROM ...;
INSERT ... RETURNING expressions INTO [STRICT] target;
UPDATE ... RETURNING expressions INTO [STRICT] target;
DELETE ... RETURNING expressions INTO [STRICT] target;
MERGE ... RETURNING expressions INTO [STRICT] target;
```

其中 *`target`* 可以是一個 record 變數、一個資料列變數，或是以逗號分隔的一串簡單變數與 record／資料列欄位。PL/pgSQL 變數會如同上述方式被替換進指令的其餘部分（也就是除了 `INTO` 子句以外的所有內容），執行計畫也以相同方式快取。這對 `SELECT`、帶有 `RETURNING` 的 `INSERT`／`UPDATE`／`DELETE`／`MERGE`，以及某些會回傳資料列集合的公用指令（例如 `EXPLAIN`）都適用。除了 `INTO` 子句之外，這個 SQL 指令與在 PL/pgSQL 之外撰寫時完全相同。

### 提示

請注意，這種帶 `INTO` 的 `SELECT` 解讀方式，與 PostgreSQL 一般的 `SELECT INTO` 指令大不相同；在後者中，`INTO` 的目標是一個新建立的資料表。如果你想在 PL/pgSQL 函式內部從 `SELECT` 的結果建立資料表，請使用 `CREATE TABLE ... AS SELECT` 語法。

如果使用資料列變數或變數清單作為目標，該指令的結果欄位在數量與資料型別上都必須與目標的結構完全相符，否則會發生執行期錯誤。當目標是 record 變數時，它會自動依該指令結果欄位的資料列型別來設定自己。

`INTO` 子句幾乎可以出現在 SQL 指令中的任何地方。習慣上，它會寫在 `SELECT` 指令的 *`select_expressions`* 清單之前或之後，或是寫在其他型式指令的結尾。建議你遵循這個慣例，以免未來版本的 PL/pgSQL 剖析器變得更嚴格。

如果 `INTO` 子句中沒有指定 `STRICT`，那麼 *`target`* 會被設為該指令回傳的第一筆資料列；若指令沒有回傳任何資料列，則被設為 NULL。（請注意，除非你使用了 `ORDER BY`，否則「第一筆資料列」並沒有明確的定義。）第一筆之後的任何結果資料列都會被捨棄。你可以檢查特殊變數 `FOUND`（參閱[第 41.5.5 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)）來判斷是否有回傳資料列：

```

SELECT * INTO myrec FROM emp WHERE empname = myname;
IF NOT FOUND THEN
    RAISE EXCEPTION 'employee % not found', myname;
END IF;
```

如果指定了 `STRICT` 選項，該指令就必須剛好回傳一筆資料列，否則會回報執行期錯誤，錯誤可能是 `NO_DATA_FOUND`（沒有資料列）或 `TOO_MANY_ROWS`（超過一筆資料列）。如果你想攔截這個錯誤，可以使用例外區塊，例如：

```

BEGIN
    SELECT * INTO STRICT myrec FROM emp WHERE empname = myname;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'employee % not found', myname;
        WHEN TOO_MANY_ROWS THEN
            RAISE EXCEPTION 'employee % not unique', myname;
END;
```

帶有 `STRICT` 的指令若成功執行，一定會把 `FOUND` 設為 true。

對於帶有 `RETURNING` 的 `INSERT`／`UPDATE`／`DELETE`／`MERGE`，即使沒有指定 `STRICT`，只要回傳超過一筆資料列，PL/pgSQL 就會回報錯誤。這是因為沒有像 `ORDER BY` 這樣的選項可以用來決定應該回傳哪一筆受影響的資料列。

如果該函式啟用了 `print_strict_params`，那麼當因為未滿足 `STRICT` 的要求而拋出錯誤時，錯誤訊息的 `DETAIL` 部分會包含傳給該指令的參數資訊。你可以透過設定 `plpgsql.print_strict_params` 來變更所有函式的 `print_strict_params` 設定，不過只有之後才編譯的函式會受到影響。你也可以使用編譯器選項，以個別函式為單位啟用它，例如：

```

CREATE FUNCTION get_userid(username text) RETURNS int
AS $$
#print_strict_params on
DECLARE
userid int;
BEGIN
    SELECT users.userid INTO STRICT userid
        FROM users WHERE users.username = get_userid.username;
    RETURN userid;
END;
$$ LANGUAGE plpgsql;
```

失敗時，這個函式可能會產生類似這樣的錯誤訊息：

```

ERROR:  query returned no rows
DETAIL:  parameters: username = 'nosuchuser'
CONTEXT:  PL/pgSQL function get_userid(text) line 6 at SQL statement
```

### 注意

`STRICT` 選項的行為與 Oracle PL/SQL 的 `SELECT INTO` 及相關陳述式一致。

<a id="PLPGSQL-STATEMENTS-EXECUTING-DYN"></a>

### 41.5.4. 執行動態指令 [#](#PLPGSQL-STATEMENTS-EXECUTING-DYN)

你常常會想在 PL/pgSQL 函式內部產生動態指令，也就是每次執行時會牽涉到不同資料表或不同資料型別的指令。在這種情境下，PL/pgSQL 平常快取指令執行計畫的做法（詳見[第 41.11.2 節](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)）就派不上用場。為了處理這類問題，於是提供了 `EXECUTE` 陳述式：

```

EXECUTE command-string [ INTO [STRICT] target ] [ USING expression [, ... ] ];
```

其中 *`command-string`* 是一個會產生字串（`text` 型別）的運算式，該字串包含要執行的指令。選擇性的 *`target`* 是一個 record 變數、一個資料列變數，或是以逗號分隔的一串簡單變數與 record／資料列欄位，指令的結果會被存進其中。選擇性的 `USING` 運算式則提供要插入指令中的值。

系統不會對算出來的指令字串做任何 PL/pgSQL 變數替換。任何需要的變數值都必須在組建指令字串時就插入其中；或者你也可以使用下面所述的參數。

此外，透過 `EXECUTE` 執行的指令沒有執行計畫快取。取而代之的是，每次執行該陳述式時都會重新規劃該指令。因此，可以在函式內部動態建立指令字串，以對不同的資料表與欄位執行動作。

`INTO` 子句指定了會回傳資料列的 SQL 指令，其結果應該被指派到哪裡。如果提供的是資料列變數或變數清單，它必須與該指令結果的結構完全相符；如果提供的是 record 變數，它會自動設定自己以符合結果的結構。如果回傳了多筆資料列，只有第一筆會被指派給 `INTO` 變數。如果沒有回傳任何資料列，則會把 NULL 指派給 `INTO` 變數。如果沒有指定 `INTO` 子句，指令的結果就會被捨棄。

如果給定了 `STRICT` 選項，除非該指令剛好產生一筆資料列，否則就會回報錯誤。

指令字串可以使用參數值，在指令中以 `$1`、`$2` 等等來參照。這些符號指的是 `USING` 子句中所提供的值。這種做法通常比把資料值以文字形式插入指令字串來得好：它避免了把值轉成文字再轉回來的執行期負擔，而且因為不需要加引號或跳脫，也不容易遭受 SQL 注入攻擊。一個例子是：

```

EXECUTE 'SELECT count(*) FROM mytable WHERE inserted_by = $1 AND inserted <= $2'
   INTO c
   USING checked_user, checked_date;
```

請注意，參數符號只能用於資料值——如果你想使用動態決定的資料表或欄位名稱，就必須以文字方式把它們插入指令字串中。例如，如果前面的查詢需要針對動態選擇的資料表來執行，你可以這樣做：

```

EXECUTE 'SELECT count(*) FROM '
    || quote_ident(tabname)
    || ' WHERE inserted_by = $1 AND inserted <= $2'
   INTO c
   USING checked_user, checked_date;
```

更乾淨的做法是使用 `format()` 的 `%I` 指定方式來插入資料表或欄位名稱，並自動加上引號：

```

EXECUTE format('SELECT count(*) FROM %I '
   'WHERE inserted_by = $1 AND inserted <= $2', tabname)
   INTO c
   USING checked_user, checked_date;
```

（這個例子仰賴一項 SQL 規則：以換行分隔的字串常數會被隱含地串接起來。）

參數符號的另一個限制是，它們只在可最佳化的 SQL 指令中有效（`SELECT`、`INSERT`、`UPDATE`、`DELETE`、`MERGE`，以及某些包含上述指令之一的指令）。在其他型式的陳述式中（通稱為公用陳述式），即使只是資料值，你也必須以文字方式插入。

如同上面第一個例子那樣，帶有簡單常數指令字串與若干 `USING` 參數的 `EXECUTE`，在功能上等同於直接在 PL/pgSQL 中寫出該指令並讓 PL/pgSQL 變數自動被替換。重要的差別在於，`EXECUTE` 每次執行時都會重新規劃該指令，產生一個針對目前參數值的執行計畫；而 PL/pgSQL 在其他情況下可能會建立一個泛用計畫並快取起來重複使用。在最佳計畫高度取決於參數值的情況下，使用 `EXECUTE` 來確實避免選到泛用計畫可能會有幫助。

目前 `EXECUTE` 中還不支援 `SELECT INTO`；請改為執行單純的 `SELECT` 指令，並把 `INTO` 指定為 `EXECUTE` 本身的一部分。

### 注意

PL/pgSQL 的 `EXECUTE` 陳述式與 PostgreSQL 伺服器所支援的 [`EXECUTE`](../../reference/sql-commands/sql-execute.md) SQL 陳述式無關。伺服器的 `EXECUTE` 陳述式不能直接在 PL/pgSQL 函式中使用（也不需要用到）。

<a id="PLPGSQL-QUOTE-LITERAL-EXAMPLE"></a>

**範例 41.1. 為動態查詢中的值加上引號**

<a id="id-1.8.8.7.6.13.2"></a><a id="id-1.8.8.7.6.13.3"></a><a id="id-1.8.8.7.6.13.4"></a><a id="id-1.8.8.7.6.13.5"></a>

在處理動態指令時，你常常必須處理單引號的跳脫問題。在函式主體中為固定文字加引號，建議的方式是使用錢號引號（dollar quoting）。（如果你有沒使用錢號引號的舊程式碼，請參考[第 41.12.1 節](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)中的概觀，在把那些程式碼改寫成較合理的方式時，它能省下你一些工夫。）

動態值需要小心處理，因為它們可能含有引號字元。以下是使用 `format()` 的例子（這裡假設你是用錢號引號括住函式主體，所以引號不需要重複兩次）：

```

EXECUTE format('UPDATE tbl SET %I = $1 '
   'WHERE key = $2', colname) USING newvalue, keyvalue;
```

也可以直接呼叫加引號的函式：

```

EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = '
        || quote_literal(newvalue)
        || ' WHERE key = '
        || quote_literal(keyvalue);
```

這個例子示範了 `quote_ident` 與 `quote_literal` 函式的用法（參閱[第 9.4 節](../../the-sql-language/functions/functions-string.md)）。為了安全起見，含有欄位或資料表識別符號的運算式，應該先經過 `quote_ident` 處理後再插入動態查詢中。含有在所組建指令中應該是字串常數之值的運算式，則應該先經過 `quote_literal` 處理。這些函式會採取適當的步驟，分別回傳以雙引號或單引號括住的輸入文字，並且把其中任何內嵌的特殊字元適當地跳脫。

由於 `quote_literal` 被標示為 `STRICT`，它在以 NULL 引數呼叫時一定會回傳 NULL。在上面的例子中，如果 `newvalue` 或 `keyvalue` 是 NULL，整個動態查詢字串就會變成 NULL，導致 `EXECUTE` 發生錯誤。你可以使用 `quote_nullable` 函式來避免這個問題，它的作用和 `quote_literal` 相同，只是當以 NULL 引數呼叫時，它會回傳字串 `NULL`。例如，

```

EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = '
        || quote_nullable(newvalue)
        || ' WHERE key = '
        || quote_nullable(keyvalue);
```

如果你處理的值有可能是 NULL，通常應該使用 `quote_nullable` 來取代 `quote_literal`。

一如往常，必須小心確保查詢中的 NULL 值不會帶來非預期的結果。例如以下這個 `WHERE` 子句

```

'WHERE key = ' || quote_nullable(keyvalue)
```

在 `keyvalue` 為 NULL 時永遠不會成立，因為以 NULL 作為運算元使用等號運算子 `=` 的結果一定是 NULL。如果你希望 NULL 能像一般的鍵值那樣運作，就必須把上面的寫法改寫成

```

'WHERE key IS NOT DISTINCT FROM ' || quote_nullable(keyvalue)
```

（目前 `IS NOT DISTINCT FROM` 的處理效率遠不如 `=`，所以除非必要，不要這樣做。關於 NULL 與 `IS DISTINCT` 的更多資訊，請參閱[第 9.2 節](../../the-sql-language/functions/functions-comparison.md)。）

請注意，錢號引號只在為固定文字加引號時才有用。想把這個例子寫成下面這樣會是非常糟糕的主意：

```

EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = $$'
        || newvalue
        || '$$ WHERE key = '
        || quote_literal(keyvalue);
```

因為萬一 `newvalue` 的內容剛好含有 `$$`，它就會出問題。你所挑選的任何其他錢號引號分隔符號，也會有同樣的疑慮。因此，若要安全地為事先未知的文字加引號，你*必須*視情況使用 `quote_literal`、`quote_nullable` 或 `quote_ident`。

動態 SQL 陳述式也可以使用 `format` 函式安全地組建（參閱[第 9.4.1 節](../../the-sql-language/functions/functions-string.md#FUNCTIONS-STRING-FORMAT)）。例如：

```

EXECUTE format('UPDATE tbl SET %I = %L '
   'WHERE key = %L', colname, newvalue, keyvalue);
```

`%I` 等同於 `quote_ident`，而 `%L` 等同於 `quote_nullable`。`format` 函式可以搭配 `USING` 子句使用：

```

EXECUTE format('UPDATE tbl SET %I = $1 WHERE key = $2', colname)
   USING newvalue, keyvalue;
```

這種寫法比較好，因為變數是以其原生的資料型別格式來處理，而不是無條件地把它們轉成文字再透過 `%L` 加引號。這樣也比較有效率。

<br>

一個規模大得多的動態指令與 `EXECUTE` 例子，可以在[範例 41.10](plpgsql-porting.md#PLPGSQL-PORTING-EX2) 中看到，它會組建並執行一個 `CREATE FUNCTION` 指令來定義一個新的函式。

<a id="PLPGSQL-STATEMENTS-DIAGNOSTICS"></a>

### 41.5.5. 取得結果狀態 [#](#PLPGSQL-STATEMENTS-DIAGNOSTICS)

有好幾種方式可以判斷一個指令的效果。第一種方式是使用 `GET DIAGNOSTICS` 指令，其形式為：

```

GET [ CURRENT ] DIAGNOSTICS variable { = | := } item [ , ... ];
```

這個指令可以取得系統的狀態指標。`CURRENT` 是一個無作用的字詞（但另請參閱[第 41.6.8.1 節](plpgsql-control-structures.md#PLPGSQL-EXCEPTION-DIAGNOSTICS)中的 `GET STACKED DIAGNOSTICS`）。每一個 *`item`* 都是一個關鍵字，用來標明要指派給指定之 *`variable`*（該變數的資料型別應該要能接收它）的狀態值。目前可用的狀態項目列於[表 41.1](plpgsql-statements.md#PLPGSQL-CURRENT-DIAGNOSTICS-VALUES)。冒號等號（`:=`）可以用來取代 SQL 標準的 `=` 語彙單元。一個例子：

```

GET DIAGNOSTICS integer_var = ROW_COUNT;
```

<a id="PLPGSQL-CURRENT-DIAGNOSTICS-VALUES"></a>

**表 41.1. 可用的診斷資訊項目**

<table border="1" class="table" summary="可用的診斷資訊項目"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="varname">ROW_COUNT</code></td><td><code class="type">bigint</code></td><td>最近一個 <acronym class="acronym">SQL</acronym> 指令所處理的資料列數</td></tr><tr><td><code class="literal">PG_CONTEXT</code></td><td><code class="type">text</code></td><td>描述目前呼叫堆疊的文字行（參閱<a class="xref" href="plpgsql-control-structures.md#PLPGSQL-CALL-STACK">第 41.6.9 節</a>）</td></tr><tr><td><code class="literal">PG_ROUTINE_OID</code></td><td><code class="type">oid</code></td><td>目前函式的 OID</td></tr></tbody></table>

<br>

判斷指令效果的第二種方式，是檢查名為 `FOUND` 的特殊變數，其型別為 `boolean`。在每次 PL/pgSQL 函式呼叫中，`FOUND` 一開始是 false。它會被下列各種陳述式設定：

* `SELECT INTO` 陳述式在有資料列被指派時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。
* `PERFORM` 陳述式在產生（並捨棄）一筆以上的資料列時把 `FOUND` 設為 true，若沒有產生資料列則設為 false。
* `UPDATE`、`INSERT`、`DELETE` 與 `MERGE` 陳述式在至少有一筆資料列受影響時把 `FOUND` 設為 true，若沒有資料列受影響則設為 false。
* `FETCH` 陳述式在回傳一筆資料列時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。
* `MOVE` 陳述式在成功重新定位游標時把 `FOUND` 設為 true，否則設為 false。
* `FOR` 或 `FOREACH` 陳述式在迭代一次以上時把 `FOUND` 設為 true，否則設為 false。`FOUND` 是在迴圈離開時才這樣設定；在迴圈的執行過程中，`FOUND` 不會被該迴圈陳述式修改，不過它有可能被迴圈主體內其他陳述式的執行所改變。
* `RETURN QUERY` 與 `RETURN QUERY EXECUTE` 陳述式在查詢至少回傳一筆資料列時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。

其他的 PL/pgSQL 陳述式不會改變 `FOUND` 的狀態。特別要注意的是，`EXECUTE` 會改變 `GET DIAGNOSTICS` 的輸出，但不會改變 `FOUND`。

`FOUND` 在每個 PL/pgSQL 函式中都是一個區域變數；對它所做的任何變更都只影響目前的函式。

<a id="PLPGSQL-STATEMENTS-NULL"></a>

### 41.5.6. 什麼都不做 [#](#PLPGSQL-STATEMENTS-NULL)

有時候，一個什麼都不做的佔位陳述式是有用的。例如，它可以表明 if/then/else 串鏈中的某一支是刻意留空的。為此，請使用 `NULL` 陳述式：

```

NULL;
```

例如，以下兩段程式碼是等價的：

```

BEGIN
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN
        NULL;  -- ignore the error
END;
```

```

BEGIN
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN  -- ignore the error
END;
```

哪一種比較好則見仁見智。

### 注意

在 Oracle 的 PL/SQL 中不允許空的陳述式清單，因此在這類情況下*必須*使用 `NULL` 陳述式。PL/pgSQL 則允許你什麼都不寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-statements.html)（原文版本：18.6；核對日期：2026-09-13）
