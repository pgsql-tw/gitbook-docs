# CREATE FUNCTION

CREATE FUNCTION — 定義一個新函數

## 語法

```text
CREATE [ OR REPLACE ] FUNCTION
  name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_namecolumn_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | IMMUTABLE | STABLE | VOLATILE | [ NOT ] LEAKPROOF
    | CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    | [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
  } ...
    [ WITH ( attribute [, ...] ) ]
```

## 說明

`CREATE FUNCTION 用來定義一個新函數。CREATE OR REPLACE FUNCTION 將建立一個新的函數，或是更換現有的函數定義。為了能夠定義一個函數，使用者必須具有該程式語言的 USAGE 權限。`

如果包含 schema，則該函數將在指定的 schema 中建立。否則它會在目前的 schema中建立。新函數的名稱不得與相同 schema 中具有相同輸入參數型別的任何現有函數相同。但是，不同參數型別的函數可以共享一個名稱（稱為多載 overloading）。

要更換現有函數的目前定義，請使用 CREATE OR REPLACE FUNCTION。以這種方式改變函數的名稱或參數型別是不可行的（如果你嘗試做了，實際上你會建立一個新的、不同的函數）。另外，CREATE OR REPLACE FUNCTION 不會讓你改變現有函數的回傳型別。為此，你必須刪除並重新建立該函數。（使用 OUT 參數時，這意味著你不能更改任何 OUT 參數的型別，除非移除該函數。）

當使用 CREATE OR REPLACE FUNCTION 替換現有函數時，該函數的所有權和權限都不會改變。所有其他的函數屬性都被分配了指令中指定或隱含的值。你必須擁有取代它的功能（這包括成為自己角色群組的成員）。

如果你刪除然後重新建立一個函數，那麼新函數與舊的函數不是同一個實體；你必須刪除引用舊功能的現有規則、view、觸發器等。使用 CREATE OR REPLACE FUNCTION 來更改函數定義而不會破壞引用該函數的物件。此外，ALTER FUNCTION 可用於更改現有函數的大部分輔助屬性。

建立函數的使用者會成為該函數的所有者。

為了能夠建立一個函數，你必須對參數型別和回傳型別具有 USAGE 權限。

## 參數

`name`

要建立的函數名稱（可以加上 schema）。

`argmode`

參數的模式：IN、OUT、INOUT 或 VARIADIC。如果省略的話，則預設為 IN。只有 OUT 參數可以接著 VARIADIC 之後。此外，OUT 和 INOUT 參數不能與 RETURNS TABLE 表示法一起使用。

`argname`

參數的名稱。在某些語言（包括 SQL 和 PL/pgSQL）可讓你在函數中使用該名稱。對於其他語言而言，就函數本身而言，輸入參數的名稱只是額外的文件；但可以在呼叫函數時使用輸入參數名稱，以提高可讀性（請參閱[第 4.3 節](../../sql/syntax/calling-funcs.md)）。在任何情況下，輸出參數的名稱都很重要，因為它會在結果的欄位型別中定義了欄位名稱。 （如果你省略輸出參數的名稱，系統將自行選擇一個預設的欄位名稱。）

`argtype`

如果有的話，函數參數的資料型別（可加上 schema）。參數型別可以是基本型別、複合型別或 domain 型別，也可以引用資料表欄位的型別。

根據實作語言的不同，它也可能被指定為「偽型別」，例如 cstring。偽型別表示實際參數型別或者是不完整指定的，或者是在普通 SQL 資料型別集合之外的型別。

透過寫成 table\_name.column\_name %TYPE來引用欄位的型別。使用此功能有時可以幫助建立獨立於資料表定義的修改功能。

`default_expr`

如果未指定參數，則將用作預設值的表示式。該表示式必須是參數的參數型別的強制性。 只有輸入（包括 INOUT）參數可以有一個預設值。具有預設值的參數之後的所有輸入參數也必須具有預設值。

`rettype`

回傳的資料型別（可加上 schema）。回傳型別可以是基本型別、複合型別或 domain 型別，也可以引用資料表欄位的型別。根據實作語言的不同，它也可能被指定為「偽型別」，例如 cstring。如果該函數不應該回傳一個值，則應指定 void 作為回傳型別。

當有 OUT 或 INOUT 參數時，可以省略 RETURNS 子句。如果存在的話，它就必須與輸出參數所暗示的結果型別一致：如果存在多個輸出參數，則為 RECORD，或者與單個輸出參數的型別相同。

SETOF 修飾字表示該函數將回傳一組值，而不是單個值。

以寫作 table\_name.column\_name %TYPE 的形式來引用欄位的型別。

`column_name`

RETURNS TABLE 語法中輸出欄位的名稱。這實際上是另一種宣告 OUT 參數的方式，除了 RETURNS TABLE 也意味著 RETURNS SETOF。

`column_type`

RETURNS TABLE 語法中輸出欄位的資料型別。

`lang_name`

該函數實作的程式語言名稱。它可以是 sql、c、internal 或使用者定義的程式語言的名稱，例如，PLPGSQL。將這個名字用單引號括起來，並且需要完全符合大小寫。

`TRANSFORM { FOR TYPEtype_name`} \[, ... \] }

對該函數如何套用型別轉換的呼叫列表。在 SQL 型別和特定於語言的資料型別之間進行轉換；請參閱 [CREATE TRANSFORM](create-transform.md)。程序語言實作通常具有內建型別的編碼知識，這些不需要在這裡列出。只是如果程序語言實作不知道如何處理這些資料型別並且沒有提供轉換方式，它將回退到轉換資料型別的預設行為，但這仍然取決於實作的情況而定。

`WINDOW`

`WINDOW 表示該函數是一個窗函數，而不是一個普通函數。目前這僅對用 C 寫成的函數有用。在替換現有函數定義時，不能更改 WINDOW 屬性。`

`IMMUTABLE`

`STABLE`

`VOLATILE`

這些屬性告知查詢優化器關於函數的行為。至多只能指定一個選項。如果沒有這些選項出現，VOLATILE 是基本的假設。

`IMMUTABLE 表示該函數不能修改資料庫，並且在給定相同的參數值時總是回傳相同的結果；也就是說，它不會執行資料庫查詢或以其他方式使用不直接存在於其參數列表中的訊息。如果給出這個選項，任何具有所有常量參數的函數呼叫都可以立即替換為函數值。`

`STABLE 表示該函數無法修改資料庫，並且在單個資料表掃描時，它將始終為相同的參數值回傳相同的結果，但其結果可能會跨 SQL 語句更改。對於結果取決於資料庫查詢，參數變數（如目前時區）等的函數，這是合適的選擇（對於希望查詢由目前命令修改資料列的 AFTER 觸發器並不合適）。另請注意，current_timestamp 類的函數符合穩定性，因為它們的值在事務中不會改變。`

`VOLATILE 表示即使在單個資料表掃描中函數值也會改變，因此不能進行優化。 在這個意義上，相對較少的資料庫功能是不穩定的，有一些例子是random ()、currval()、timeofday()。 但請注意，任何具有副作用的函數都必須分類為 VOLATILE，即使其結果具有相當的可預測性，以防止結果被優化掉，這樣例子是setval()。`

更多詳細訊息請參閱[第 37.6 節](../../server-programming/extending-sql/37.6.-function-volatility-categories.md)。

`LEAKPROOF`

`LEAKPROOF` 表示該函數不會有副作用。除了其回傳值之外，它沒有揭示任何關於它的參數訊息。例如，某些參數值引發了錯誤訊息但不引發其他錯誤訊息的函數，或者在任何錯誤訊息中包含參數值的函數都是不洩漏的。這會影響系統如何對使用這些 security\_barrier 選項建立的 view 或啟用資料列級別安全性的資料表執行查詢。在查詢本身包含非防漏功能的使用者提供的任何條件之前，系統將執行安全策略和安全屏障 view 的條件，以防止資料意外暴露。標記為防漏的功能和操作子被認為是可信的，並且可以在來自安全原則和安全障礙視圖的條件之前執行。另外，沒有參數或者沒有從安全屏障 view 或資料表中傳遞任何參數的函數在安全條件之前不必被標記為不可洩漏。請參閱 [CREATE VIEW](create-view.md) 和[第 40.5 節](../../server-programming/the-rule-system/rules-and-privileges.md)。此選項只能由超級使用者設定。

`CALLED ON NULL INPUT`

`RETURNS NULL ON NULL INPUT`

`STRICT`

`CALLED ON NULL INPUT`（預設值）表示當其某些參數為 null 時，該函數仍將被正常呼叫。那麼函數作者有責任在必要時檢查 null，並作出適當的處理。

`RETURNS NULL ON NULL INPUT` 或 `STRICT` 表示函數每當其任何參數為 null 時就回傳 null。如果指定了該參數，那麼當有 null 參數時，該函數就不會被執行；也就是，會自動假定結果為 null。

`[EXTERNAL] SECURITY INVOKER  
[EXTERNAL] SECURITY DEFINER`

`SECURITY INVOKER` 表示該函數將以呼叫它的使用者權限執行。這是預設的設定。 `SECURITY DEFINER` 指定該功能將以擁有它的使用者權限執行。

關鍵字 `EXTERNAL` 允許 SQL 一致性，但它是選擇性的。與 SQL 標準不同的是，此功能適用於所有函數。

`PARALLEL`

PARALLEL UNSAFE 表示該函數不能在平行模式下執行，並且在 SQL 語句中存在此類函數會強制執行串列的執行計劃。這是預設的設定。PARALLEL RESTRICTED 表示該功能可以以平行模式執行，但執行僅限於平行群組領導。PARALLEL SAFE 表示該功能可以安全無限制地在平行模式下執行。

如果函數修改任何資料庫狀態，或者如果他們對交易事務進行了更新（如使用子事務，或者他們存取序列資料或試圖對設定進行永久性更改（例如 setval）），那麼函數就應該標記為 PARALLEL UNSAFE。如果它們存取臨時資料表、客戶端連線狀態、游標、prepared statement 或系統無法以平行模式同步的繁雜的後端狀態，它們應該被標記為 PARALLEL RESTRICTED（例如，設定種子不能由初始者執行，另一個流程所做的更改不會反映在初始者身上）。一般來說，如果一個函數在 RESTRICTED 或 UNSAFE 時被標記為 SAFE，或者當它實際上是 UNSAFE 的時候被標記為 RESTRICTED，那麼它在使用平行查詢時可能會引發錯誤或產生錯誤的結果。如果錯誤標記，C 語言函數在理論上可能表現出完全未定義的行為，因為系統無法保護自己免受任意 C 程式的影響，但在大多數情況下，結果不會比其他函數更差。只要有疑問，函數就應該標記為UNSAFE，這是預設值。

`execution_cost`

一個正數，以 cpu 執行成本為單位給予該函數的估計執行成本。如果函數回傳一個集合，則這是每個回傳資料列的成本。如果未指定成本，則假定 C 語言和內部函數為 1 個單元，其他語言為 100 個單元。較大的值會導致規劃單元嘗試避免比必要時更頻繁地評估該函數。

`result_rows`

一個正數，它給予規劃單元應該期望函數回傳的估計資料列數。只有在函數宣告回傳一個集合時才允許這樣做。預設是 1000 個資料列。

`configuration_parameter`

`value`

SET 子句在輸入函數時將指定的配置參數設定為指定的值，然後在函數退出時恢復為其先前的值。 SET FROM CURRENT 將執行 CREATE FUNCTION 時當時參數的值保存為輸入函數時要應用的值。

如果將一個 SET 子句附加到一個函數，那麼在該函數內對同一個變數執行的 SET LOCAL 命令的作用將僅限於該函數：配置參數的先前的值仍然會在函數離開時恢復。 然而，一個普通的 SET 命令（沒有 LOCAL）會覆蓋 SET 子句，就像它對於先前的 SET LOCAL 指令所做的那樣：除非當下的事務被回復，否則這種指令的效果將在函數退出後持續存在。

有關允許的參數名稱和值的更多訊息，請參閱 [SET](set.md) 和[第 19 章](../../server-administration/runtime-config/)。

`definition`

A string constant defining the function; the meaning depends on the language. It can be an internal function name, the path to an object file, an SQL command, or text in a procedural language.

It is often helpful to use dollar quoting \(see[Section 4.1.2.4](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING)\) to write the function definition string, rather than the normal single quote syntax. Without dollar quoting, any single quotes or backslashes in the function definition must be escaped by doubling them.

`obj_file`,`link_symbol`

This form of the`AS`clause is used for dynamically loadable C language functions when the function name in the C language source code is not the same as the name of the SQL function. The string`obj_file`_\_is the name of the shared library file containing the compiled C function, and is interpreted as for the_[_LOAD_](https://www.postgresql.org/docs/10/static/sql-load.html)_command. The string_`link_symbol`\_is the function's link symbol, that is, the name of the function in the C language source code. If the link symbol is omitted, it is assumed to be the same as the name of the SQL function being defined.

When repeated`CREATE FUNCTION`calls refer to the same object file, the file is only loaded once per session. To unload and reload the file \(perhaps during development\), start a new session.

`attribute`

The historical way to specify optional pieces of information about the function. The following attributes can appear here:

`isStrict`

Equivalent to`STRICT`or`RETURNS NULL ON NULL INPUT`.

`isCachable`

`isCachable`is an obsolete equivalent of`IMMUTABLE`; it's still accepted for backwards-compatibility reasons.

Attribute names are not case-sensitive.

Refer to[Section 37.3](https://www.postgresql.org/docs/10/static/xfunc.html)for further information on writing functions.

## 函數多載（Overloading）

PostgreSQL 允許函數多載；也就是說，只要具有不同的輸入參數類型，相同的名稱可以用於多個不同的函數。但是，所有 C 的函數名稱必須不同，因此你必須為 C 函數重載不同C 的名稱（例如，使用參數型別作為 C 名稱的一部分）。

如果兩個函數具有相同的名稱和輸入參數型別，則忽略任何 OUT 參數將被視為相同。 因此，像這些聲明就會有衝突：

```text
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, out text) ...
```

具有不同參數型別列表的函數在建立時不會被視為衝突，但如果提供了預設值，則它們可能會在使用中發生衝突。 例如下面的例子：

```text
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, int default 42) ...
```

呼叫 foo\(10\) 的話會因為不知道應該呼叫哪個函數而失敗。

## 注意

以完整的 SQL 型別語法來宣告函數的參數和回傳值是可以。 但是，帶括號的型別修飾字（例如數字型別的精確度修飾字）將被 CREATE FUNCTION 丟棄。 因此，例如 CREATE FUNCTION foo（varchar（10））...與 CREATE FUNCTION foo（varchar）....完全相同。

使用 CREATE OR REPLACE FUNCTION 替換現有函數時，對於更改參數名稱是有限制的。你不能更改已分配給任何輸入參數的名稱（儘管你可以將名稱增加先前沒有的參數）。如果有多個輸出參數，則不能更改輸出參數的名稱，因為這會更改描述函數結果的匿名組合類型的欄位名稱。 這些限制是為了確保函數的現有的呼叫在更換時不會停止工作。

如果使用 VARIADIC 參數將函數聲明為 STRICT，則嚴格性檢查會測試整個動態陣列是否為 non-null。如果陣列有 null，該函數仍然可以被呼叫。

## 範例

這裡有一些簡單的例子可以幫助你開始。有關更多訊息和範例，請參閱[第 37.3 節](../../server-programming/extending-sql/user-defined-functions.md)。

```text
CREATE FUNCTION add(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
```

將一個整數遞增，在 PL/pgSQL 中使用參數名稱：

```text
CREATE OR REPLACE FUNCTION increment(i integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
```

回傳包含多個輸出參數的結果：

```text
CREATE FUNCTION dup(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

你可以使用明確命名的複合型別更加詳細地完成同樣的事情：

```text
CREATE TYPE dup_result AS (f1 int, f2 text);

CREATE FUNCTION dup(int) RETURNS dup_result
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

回傳多個欄位的另一種方法是使用 TABLE 函數：

```text
CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

但是，TABLE 函數與前面的例子不同，因為它實際上回傳一堆記錄，而不僅僅是一條記錄。

## 安全地撰寫 SECURITY DEFINER 函數

由於SECURITY DEFINER函數是以擁有它的用戶的權限執行的，因此需要注意確保該函數不會被濫用。為了安全起見，應設定 search\_path 以排除任何不受信任的使用者可以寫入的 schema。這可以防止惡意使用者建立掩蓋物件的物件（例如資料表、函數和運算元），使得該物件被函數使用。在這方面特別重要的是臨時資料表的 schema，它預設是首先被搜尋的，並且通常允許由任何人寫入。透過強制最後才搜尋臨時 schema 可以得到較為安全的處理。 為此，請將 pg\_temp 作為 search\_path 中的最後一個項目。此函數說明安全的使用情況：

```text
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

這個函數的意圖是存取一個資料表 admin.pwds。但是，如果沒有 SET 子句，或者只提及 admin 的 SET 子句，則可以透過建立名為 pwds 的臨時資料表來破壞該函數。

在 PostgreSQL 8.3 之前，SET 子句還不能使用，所以舊的函數可能需要相當複雜的邏輯來儲存、設定和恢復 search\_path。有了 SET 子句便更容易用於此目的。

還有一點需要注意的是，預設情況下，對於新建立的函數，將會把權限授予 PUBLIC（請參閱 [GRANT](grant.md) 以獲取更多訊息）。通常情況下，你只希望將安全定義函數的使用僅限於某些使用者。為此，你必須撤銷預設的 PUBLIC 權限，然後選擇性地授予執行權限。為了避免出現一個破口，使得所有人都可以訪問新功能，可以在一個交易事務中建立它並設定權限。例如：

```text
BEGIN;
CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER;
REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins;
COMMIT;
```

## 相容性

SQL:1999 及其更新的版本中定義了一個 CREATE FUNCTION 指令。與 PostgreSQL 版本的指令類似但不完全相容。這些屬性並不是可移植的，不同的程序語言之間也無法移植。

為了與其他資料庫系統相容，可以在 argname 之前或之後編寫 argmode。但只有第一種方法符合標準。

對於參數預設值，SQL標準僅使用 DEFAULT 關鍵字指定語法。帶有 = 的語法在 T-SQL 和 Firebird 中使用。

## 延伸閱讀

[ALTER FUNCTION](alter-function.md), [DROP FUNCTION](drop-function.md), [GRANT](grant.md), [LOAD](load.md), [REVOKE](revoke.md)

