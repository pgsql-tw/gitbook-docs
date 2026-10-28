<a id="SQL-CREATEFUNCTION"></a><a id="id-1.9.3.67.1"></a>

## CREATE FUNCTION

CREATE FUNCTION — 定義新的函式

<a id="id-1.9.3.67.4"></a>

## 語法

```

CREATE [ OR REPLACE ] FUNCTION
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_name column_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | { IMMUTABLE | STABLE | VOLATILE }
    | [ NOT ] LEAKPROOF
    | { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT }
    | { [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER }
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SUPPORT support_function
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
    | sql_body
  } ...
```

<a id="SQL-CREATEFUNCTION-DESCRIPTION"></a>

## 說明

`CREATE FUNCTION` 會定義新的函式。`CREATE OR REPLACE FUNCTION` 會建立新的函式，或取代現有的定義。若要能夠定義函式，使用者必須擁有該語言的 `USAGE` 權限。

若包含綱要名稱，函式會建立在指定的綱要中；否則會建立在目前的綱要中。新函式的名稱不得與同一綱要中具有相同輸入引數型別的任何現有函式或程序相符。不過，引數型別不同的函式與程序可以共用名稱（這稱為*多載*）。

若要取代現有函式的目前定義，請使用 `CREATE OR REPLACE FUNCTION`。無法以這種方式變更函式的名稱或引數型別（若你嘗試這麼做，實際上會建立一個新的、不同的函式）。此外，`CREATE OR REPLACE FUNCTION` 不允許你變更現有函式的傳回型別。若要這麼做，你必須移除並重新建立該函式。（使用 `OUT` 參數時，這表示除非移除該函式，否則你無法變更任何 `OUT` 參數的型別。）

使用 `CREATE OR REPLACE FUNCTION` 取代現有函式時，函式的擁有權與權限不會改變。其他所有函式屬性，都會被指派為命令中指定或隱含的值。你必須擁有該函式才能取代它（這包括身為擁有者角色的成員）。

若你移除後再重新建立函式，新函式與舊函式並不是同一個實體；你必須移除參照舊函式的現有規則、檢視表、觸發程序等。使用 `CREATE OR REPLACE FUNCTION` 可以在不破壞參照該函式之物件的情況下變更函式定義。此外，`ALTER FUNCTION` 可以用來變更現有函式的大部分輔助屬性。

建立函式的使用者會成為該函式的擁有者。

若要能夠建立函式，你必須擁有引數型別與傳回型別上的 `USAGE` 權限。

關於撰寫函式的進一步資訊，請參閱[第 36.3 節](../../server-programming/extend/xfunc.md)。

<a id="id-1.9.3.67.6"></a>

## 參數

*`name`*
:   要建立之函式的名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。只有 `OUT` 引數可以接在 `VARIADIC` 引數之後。此外，`OUT` 與 `INOUT` 引數不能與 `RETURNS TABLE` 表示法一起使用。

*`argname`*
:   引數的名稱。某些語言（包括 SQL 與 PL/pgSQL）允許你在函式本體中使用此名稱。對於其他語言，就函式本身而言，輸入引數的名稱只是額外的說明文件；但你可以在呼叫函式時使用輸入引數名稱以提升可讀性（請參閱[第 4.3 節](../../the-sql-language/sql-syntax/sql-syntax-calling-funcs.md)）。無論如何，輸出引數的名稱都有意義，因為它定義了結果資料列型別中的欄位名稱。（若你省略輸出引數的名稱，系統會選擇一個預設的欄位名稱。）

*`argtype`*

函式引數的資料型別（可選擇以綱要限定），若有引數的話。引數型別可以是基本型別、複合型別或網域型別，也可以參照資料表欄位的型別。

依實作語言而定，也可能允許指定「虛擬型別」，例如 `cstring`。虛擬型別表示實際的引數型別未完整指定，或不屬於一般 SQL 資料型別的集合。

欄位的型別以 `table_name.column_name%TYPE` 的寫法參照。使用此功能有時有助於讓函式不受資料表定義變更的影響。

*`default_expr`*
:   未指定參數時用作預設值的運算式。此運算式必須能強制轉換為該參數的引數型別。只有輸入參數（包括 `INOUT`）可以有預設值。所有接在有預設值之參數後面的輸入參數，也都必須有預設值。

*`rettype`*

傳回的資料型別（可選擇以綱要限定）。傳回型別可以是基本型別、複合型別或網域型別，也可以參照資料表欄位的型別。依實作語言而定，也可能允許指定「虛擬型別」，例如 `cstring`。若函式不應傳回值，請指定 `void` 作為傳回型別。

當有 `OUT` 或 `INOUT` 參數時，可以省略 `RETURNS` 子句。若有提供，它必須與輸出參數所隱含的結果型別一致：若有多個輸出參數則為 `RECORD`，或者是與單一輸出參數相同的型別。

`SETOF` 修飾詞表示函式會傳回一組項目，而不是單一項目。

欄位的型別以 `table_name.column_name%TYPE` 的寫法參照。

*`column_name`*
:   `RETURNS TABLE` 語法中輸出欄位的名稱。這實際上是宣告具名 `OUT` 參數的另一種方式，只是 `RETURNS TABLE` 還隱含了 `RETURNS SETOF`。

*`column_type`*
:   `RETURNS TABLE` 語法中輸出欄位的資料型別。

*`lang_name`*
:   實作該函式所用之語言的名稱。可以是 `sql`、`c`、`internal`，或使用者定義之程序語言的名稱，例如 `plpgsql`。若指定了 *`sql_body`*，預設為 `sql`。以單引號括住名稱的寫法已不建議使用，而且需要大小寫相符。

`TRANSFORM { FOR TYPE type_name } [, ... ] }`
:   列出呼叫此函式時應套用哪些轉換。轉換會在 SQL 型別與語言特定的資料型別之間進行轉換；請參閱 [CREATE TRANSFORM](sql-createtransform.md)。程序語言的實作通常已內建處理內建型別的知識，因此這些型別不需要列在這裡。若程序語言的實作不知道如何處理某個型別，且未提供轉換，它會退回使用預設的資料型別轉換行為，但這取決於實作。

`WINDOW`
:   `WINDOW` 表示該函式是*視窗函式*，而不是一般函式。目前這只對以 C 撰寫的函式有用。取代現有函式定義時，無法變更 `WINDOW` 屬性。

`IMMUTABLE`<br>`STABLE`<br>`VOLATILE`

這些屬性告知查詢最佳化器該函式的行為。最多只能指定其中一個。若都未出現，預設假設為 `VOLATILE`。

`IMMUTABLE` 表示該函式不能修改資料庫，且在給定相同引數值時一律傳回相同的結果；也就是說，它不進行資料庫查詢，也不以其他方式使用未直接出現在其引數清單中的資訊。若指定此選項，對該函式的任何引數全為常數的呼叫，都可以立即以函式值取代。

`STABLE` 表示該函式不能修改資料庫，且在單一資料表掃描內，對於相同的引數值會一致地傳回相同結果，但其結果可能在不同 SQL 陳述式之間改變。對於結果取決於資料庫查詢、參數變數（例如目前時區）等的函式，這是適當的選擇。（對於想要查詢被目前命令修改之資料列的 `AFTER` 觸發程序，這並不適當。）也請注意，`current_timestamp` 系列函式屬於穩定（stable）函式，因為它們的值在一個交易內不會改變。

`VOLATILE` 表示即使在單一資料表掃描內，函式值也可能改變，因此無法進行任何最佳化。在這個意義上屬於揮發性（volatile）的資料庫函式相對較少；一些例子是 `random()`、`currval()`、`timeofday()`。但請注意，任何具有副作用的函式都必須歸類為揮發性，即使其結果相當可預測也一樣，以避免呼叫被最佳化掉；一個例子是 `setval()`。

更多細節請參閱[第 36.7 節](../../server-programming/extend/xfunc-volatility.md)。

`LEAKPROOF`
:   `LEAKPROOF` 表示該函式沒有副作用。除了透過其傳回值之外，它不會揭露任何關於其引數的資訊。例如，對某些引數值會擲出錯誤訊息、對其他引數值則不會的函式，或在任何錯誤訊息中包含引數值的函式，都不是 leakproof 的。這會影響系統如何執行針對以 `security_barrier` 選項建立之檢視表、或已啟用資料列層級安全性之資料表的查詢。對於來自查詢本身、且包含非 leakproof 函式的任何使用者提供條件，系統會在它們之前先強制執行來自安全性政策與安全屏障檢視表的條件，以防止資料意外外洩。標記為 leakproof 的函式與運算子被假定為可信任的，並且可以在來自安全性政策與安全屏障檢視表的條件之前執行。此外，不接受引數、或未從安全屏障檢視表或資料表接收任何引數的函式，不需要標記為 leakproof 就可以在安全性條件之前執行。請參閱 [CREATE VIEW](sql-createview.md) 與[第 39.5 節](../../server-programming/rules/rules-privileges.md)。此選項只能由超級使用者設定。

`CALLED ON NULL INPUT`<br>`RETURNS NULL ON NULL INPUT`<br>`STRICT`

`CALLED ON NULL INPUT`（預設值）表示當部分引數為 null 時，仍會正常呼叫該函式。此時由函式作者負責在必要時檢查 null 值並適當回應。

`RETURNS NULL ON NULL INPUT` 或 `STRICT` 表示只要有任何引數為 null，該函式一律傳回 null。若指定此參數，當有 null 引數時不會執行該函式；而是自動假定結果為 null。

`[EXTERNAL] SECURITY INVOKER`<br>`[EXTERNAL] SECURITY DEFINER`

`SECURITY INVOKER` 表示函式要以呼叫它之使用者的權限執行。這是預設值。`SECURITY DEFINER` 指定函式要以擁有它之使用者的權限執行。關於如何安全地撰寫 `SECURITY DEFINER` 函式，[請參閱下文](sql-createfunction.md#SQL-CREATEFUNCTION-SECURITY)。

關鍵字 `EXTERNAL` 是為了符合 SQL 而允許使用，但它是選擇性的，因為與 SQL 不同，此功能適用於所有函式，而不只是外部函式。

`PARALLEL`

`PARALLEL UNSAFE` 表示該函式不能在平行模式中執行；SQL 陳述式中出現這類函式，會強制使用序列執行計畫。這是預設值。`PARALLEL RESTRICTED` 表示該函式可以在平行模式中執行，但只能在平行群組的領導程序中執行。`PARALLEL SAFE` 表示該函式可以不受限制地安全地在平行模式中執行，包括在平行工作程序中。

若函式會修改任何資料庫狀態、變更交易狀態（使用子交易進行錯誤復原除外）、存取序列（例如呼叫 `currval`），或對設定做出永久性變更，就應該標記為平行不安全（parallel unsafe）。若函式會存取暫存資料表、用戶端連線狀態、游標、預備陳述式，或系統無法在平行模式中同步的其他各種後端本地狀態，就應該標記為平行受限（parallel restricted）（例如，`setseed` 只能由群組領導程序執行，因為其他程序所做的變更不會反映到領導程序中）。一般而言，若函式實際上是受限或不安全的，卻被標記為安全；或者實際上是不安全的，卻被標記為受限，則在平行查詢中使用時，它可能會擲出錯誤或產生錯誤的答案。若標記錯誤，C 語言函式理論上可能表現出完全未定義的行為，因為系統無法保護自己免受任意 C 程式碼的影響；但在大多數可能的情況下，結果不會比其他任何函式更糟。若有疑慮，函式應該標記為 `UNSAFE`，這是預設值。

`COST` *`execution_cost`*
:   一個正數，表示函式的估計執行成本，以 [cpu_operator_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-OPERATOR-COST) 為單位。若函式傳回集合，這是每傳回一筆資料列的成本。若未指定成本，C 語言與 internal 函式假定為 1 單位，其他所有語言的函式則假定為 100 單位。較大的值會使規劃器嘗試避免超過必要地頻繁計算該函式。

`ROWS` *`result_rows`*
:   一個正數，表示規劃器應預期函式傳回的估計資料列數。只有在函式宣告為傳回集合時才允許使用。預設假設為 1000 筆資料列。

`SUPPORT` *`support_function`*
:   此函式要使用之*規劃器支援函式*的名稱（可選擇以綱要限定）。詳情請參閱[第 36.11 節](../../server-programming/extend/xfunc-optimization.md)。你必須是超級使用者才能使用此選項。

*`configuration_parameter`*<br>*`value`*

`SET` 子句會在進入函式時，將指定的組態參數設為指定的值，並在函式結束時將其還原為先前的值。`SET FROM CURRENT` 會將執行 `CREATE FUNCTION` 時該參數的目前值，儲存為進入函式時要套用的值。

若函式附加了 `SET` 子句，則在函式內針對同一變數執行的 `SET LOCAL` 命令，其效果僅限於該函式：函式結束時，該組態參數仍會還原為先前的值。不過，一般的 `SET` 命令（不帶 `LOCAL`）會覆寫 `SET` 子句，就像它會覆寫先前的 `SET LOCAL` 命令一樣：除非目前交易被回滾，否則這類命令的效果在函式結束後仍會持續。

關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

*`definition`*

定義函式的字串常數；其意義取決於語言。它可以是內部函式名稱、目的檔的路徑、SQL 命令，或以程序語言撰寫的文字。

撰寫函式定義字串時，使用錢字號引用（請參閱[第 4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）通常比一般的單引號語法更有幫助。若不使用錢字號引用，函式定義中的任何單引號或反斜線都必須以重複兩次的方式跳脫。

`obj_file, link_symbol`

當 C 語言原始碼中的函式名稱與 SQL 函式的名稱不同時，`AS` 子句的這種形式用於可動態載入的 C 語言函式。字串 *`obj_file`* 是包含已編譯 C 函式之共享函式庫檔案的名稱，其解讀方式與 [`LOAD`](sql-load.md) 命令相同。字串 *`link_symbol`* 是函式的連結符號，也就是該函式在 C 語言原始碼中的名稱。若省略連結符號，會假定它與所定義之 SQL 函式的名稱相同。所有函式的 C 名稱都必須不同，因此你必須為多載的 C 函式指定不同的 C 名稱（例如，將引數型別作為 C 名稱的一部分）。

當重複的 `CREATE FUNCTION` 呼叫參照同一個目的檔時，每個工作階段只會載入該檔案一次。若要卸載並重新載入該檔案（也許是在開發期間），請開始一個新的工作階段。

*`sql_body`*
:   `LANGUAGE SQL` 函式的本體。這可以是單一陳述式

    ```

    RETURN expression
    ```

    或是一個區塊

    ```

    BEGIN ATOMIC
      statement;
      statement;
      ...
      statement;
    END
    ```

    這類似於將函式本體的文字寫成字串常數（請參閱上方的 *`definition`*），但有一些差異：此形式只適用於 `LANGUAGE SQL`，字串常數形式則適用於所有語言。此形式在函式定義時剖析，字串常數形式則在執行時剖析；因此，此形式無法支援多型引數型別，以及其他在函式定義時無法解析的結構。此形式會追蹤函式與函式本體中所使用之物件之間的相依性，因此 `DROP ... CASCADE` 能正確運作，而使用字串常值的形式則可能留下懸置的函式。最後，此形式與 SQL 標準及其他 SQL 實作更相容。

<a id="SQL-CREATEFUNCTION-OVERLOADING"></a>

## 多載

PostgreSQL 允許函式*多載*；也就是說，只要輸入引數型別不同，同一個名稱就可以用於多個不同的函式。無論你是否使用此功能，在某些使用者不信任其他使用者的資料庫中呼叫函式時，此功能都使得你需要採取安全性防範措施；請參閱[第 10.3 節](../../the-sql-language/typeconv/typeconv-func.md)。

若兩個函式的名稱與*輸入*引數型別相同，就會被視為相同的函式，任何 `OUT` 參數都會被忽略。因此，例如下列宣告會互相衝突：

```

CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, out text) ...
```

引數型別清單不同的函式在建立時不會被視為衝突，但若提供了預設值，在使用時就可能發生衝突。例如，考慮

```

CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, int default 42) ...
```

呼叫 `foo(10)` 會失敗，因為無法確定應該呼叫哪一個函式。

<a id="SQL-CREATEFUNCTION-NOTES"></a>

## 注意事項

宣告函式的引數與傳回值時，允許使用完整的 SQL 型別語法。不過，括號括起來的型別修飾詞（例如 `numeric` 型別的精確度欄位）會被 `CREATE FUNCTION` 捨棄。因此，例如 `CREATE FUNCTION foo (varchar(10)) ...` 與 `CREATE FUNCTION foo (varchar) ...` 完全相同。

以 `CREATE OR REPLACE FUNCTION` 取代現有函式時，變更參數名稱會受到限制。你不能變更已指派給任何輸入參數的名稱（不過你可以為先前沒有名稱的參數加上名稱）。若有超過一個輸出參數，你就不能變更輸出參數的名稱，因為這會改變描述函式結果之匿名複合型別的欄位名稱。這些限制是為了確保函式被取代時，對它的現有呼叫不會停止運作。

若函式以 `STRICT` 宣告且帶有 `VARIADIC` 引數，嚴格性檢查會測試 variadic 陣列*整體*是否為非 null。若陣列包含 null 元素，函式仍會被呼叫。

<a id="SQL-CREATEFUNCTION-EXAMPLES"></a>

## 範例

使用 SQL 函式將兩個整數相加：

```

CREATE FUNCTION add(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
```

以更符合 SQL 標準的風格撰寫的相同函式，使用引數名稱與未加引號的本體：

```

CREATE FUNCTION add(a integer, b integer) RETURNS integer
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    RETURN a + b;
```

在 PL/pgSQL 中利用引數名稱，將整數加一：

```

CREATE OR REPLACE FUNCTION increment(i integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
```

傳回包含多個輸出參數的紀錄：

```

CREATE FUNCTION dup(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

你可以使用明確命名的複合型別，以更冗長的方式做同樣的事：

```

CREATE TYPE dup_result AS (f1 int, f2 text);

CREATE FUNCTION dup(int) RETURNS dup_result
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

傳回多個欄位的另一種方法是使用 `TABLE` 函式：

```

CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

不過，`TABLE` 函式與前面的範例不同，因為它實際上傳回的是紀錄的*集合*，而不只是一筆紀錄。

<a id="SQL-CREATEFUNCTION-SECURITY"></a>

## 安全地撰寫 `SECURITY DEFINER` 函式

<a id="id-1.9.3.67.10.2"></a><a id="id-1.9.3.67.10.3"></a>

由於 `SECURITY DEFINER` 函式是以擁有它之使用者的權限執行，因此需要謹慎確保該函式不會被濫用。為了安全起見，應該將 [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 設定為排除任何不受信任使用者可寫入的綱要。這可以防止惡意使用者建立會遮蔽函式原本要使用之物件的物件（例如資料表、函式與運算子）。在這方面特別重要的是暫存資料表綱要，它預設會最先被搜尋，而且通常任何人都可以寫入。強制讓暫存綱要最後才被搜尋，就可以得到安全的配置。做法是將 `pg_temp`<a id="id-1.9.3.67.10.4.4"></a> 寫成 `search_path` 中的最後一個項目。此函式示範了安全的用法：

```

CREATE FUNCTION check_password(uname TEXT, pass TEXT)
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
BEGIN
        SELECT  (pwd = $2) INTO passed
        FROM    pwds
        WHERE   username = $1;

        RETURN passed;
END;
$$  LANGUAGE plpgsql
    SECURITY DEFINER
    -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
    SET search_path = admin, pg_temp;
```

此函式的用意是存取資料表 `admin.pwds`。但若沒有 `SET` 子句，或 `SET` 子句只提到 `admin`，就可以藉由建立名為 `pwds` 的暫存資料表來顛覆此函式。

若 SECURITY DEFINER 函式打算建立角色，且它是以非超級使用者身分執行，則也應該使用 `SET` 子句將 `createrole_self_grant` 設為已知的值。

另一個要記住的重點是，預設情況下，新建立的函式會將執行權限授予 `PUBLIC`（更多資訊請參閱[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)）。你經常會希望將 SECURITY DEFINER 函式的使用限制為只有部分使用者。若要這麼做，你必須撤銷預設的 `PUBLIC` 權限，然後選擇性地授予執行權限。為了避免出現新函式可被所有人存取的空窗期，請在單一交易中建立它並設定權限。例如：

```

BEGIN;
CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER;
REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins;
COMMIT;
```

<a id="SQL-CREATEFUNCTION-COMPAT"></a>

## 相容性

SQL 標準中定義了 `CREATE FUNCTION` 命令。PostgreSQL 的實作可以用相容的方式使用，但有許多擴充。反之，SQL 標準也指定了許多 PostgreSQL 未實作的選擇性功能。

以下是重要的相容性問題：

* `OR REPLACE` 是 PostgreSQL 的擴充語法。
* 為了與某些其他資料庫系統相容，*`argmode`* 可以寫在 *`argname`* 之前或之後。但只有第一種寫法符合標準。
* 對於參數預設值，SQL 標準只指定使用 `DEFAULT` 關鍵字的語法。使用 `=` 的語法用於 T-SQL 與 Firebird。
* `SETOF` 修飾詞是 PostgreSQL 的擴充語法。
* 只有 `SQL` 是標準化的語言。
* 除了 `CALLED ON NULL INPUT` 與 `RETURNS NULL ON NULL INPUT` 之外，其他所有屬性都未標準化。
* 對於 `LANGUAGE SQL` 函式的本體，SQL 標準只指定 *`sql_body`* 形式。

簡單的 `LANGUAGE SQL` 函式可以用既符合標準、又可移植到其他實作的方式撰寫。使用進階功能、最佳化屬性或其他語言的較複雜函式，必然會在相當程度上專屬於 PostgreSQL。

<a id="id-1.9.3.67.12"></a>

## 另請參閱

[ALTER FUNCTION](sql-alterfunction.md), [DROP FUNCTION](sql-dropfunction.md), [GRANT](sql-grant.md), [LOAD](sql-load.md), [REVOKE](sql-revoke.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createfunction.html)（原文版本：18.6；核對日期：2026-10-04）
