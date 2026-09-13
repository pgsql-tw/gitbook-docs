<a id="PLPGSQL-DEVELOPMENT-TIPS"></a>

## 41.12. PL/pgSQL 開發技巧 [#](#PLPGSQL-DEVELOPMENT-TIPS)

[41.12.1. 引號的處理](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)

[41.12.2. 額外的編譯期與執行期檢查](plpgsql-development-tips.md#PLPGSQL-EXTRA-CHECKS)

開發 PL/pgSQL 的一種好方法，是用你慣用的文字編輯器來撰寫函式，然後在另一個視窗中用 psql 載入並測試這些函式。如果你採用這種做法，建議使用 `CREATE OR REPLACE FUNCTION` 來撰寫函式。這樣一來，你只要重新載入該檔案就能更新函式定義。例如：

```

CREATE OR REPLACE FUNCTION testfunc(integer) RETURNS integer AS $$
          ....
$$ LANGUAGE plpgsql;
```

在執行 psql 時，你可以用下列指令載入或重新載入這樣的函式定義檔：

```

\i filename.sql
```

接著就能立即下 SQL 指令來測試該函式。

開發 PL/pgSQL 的另一種好方法，是使用便於以程序語言開發的圖形化資料庫存取工具。pgAdmin 就是這類工具的一個例子，當然也還有其他選擇。這些工具通常會提供一些方便的功能，例如跳脫單引號，以及讓重建與除錯函式更為容易。

<a id="PLPGSQL-QUOTE-TIPS"></a>

### 41.12.1. 引號的處理 [#](#PLPGSQL-QUOTE-TIPS)

PL/pgSQL 函式的程式碼在 `CREATE FUNCTION` 中是以字串常數的形式指定的。如果你以一般方式、用前後單引號來撰寫這個字串常數，那麼函式本體中的任何單引號都必須加倍；同樣地，任何反斜線也都必須加倍（假設使用的是跳脫字串語法）。把引號加倍充其量只是件麻煩事，但在比較複雜的情況下，程式碼會變得完全難以理解，因為你很容易就會發現自己需要連寫半打甚至更多的引號。建議你改以「錢字號引用（dollar-quoted）」的字串常數來撰寫函式本體（請參閱[第 4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）。在錢字號引用的做法中，你完全不需要把任何引號加倍，只要注意為每一層需要的巢狀結構選用不同的錢字號引用分隔字串即可。例如，你可以把 `CREATE FUNCTION` 指令寫成：

```

CREATE OR REPLACE FUNCTION testfunc(integer) RETURNS integer AS $PROC$
          ....
$PROC$ LANGUAGE plpgsql;
```

在其中，你可以用引號來表示 SQL 指令裡單純的字串常數，並用 `$$` 來界定你以字串方式組合出來的 SQL 指令片段。如果你需要引用包含 `$$` 的文字，可以改用 `$Q$`，依此類推。

下面這張表列出了在不使用錢字號引用時，撰寫引號所必須採取的做法。當你要把錢字號引用出現之前的舊程式碼改寫成比較容易理解的形式時，它或許會很有用。

<a id="PLPGSQL-QUOTE-TIPS-1-QUOT"></a>

1 個引號 [#](#PLPGSQL-QUOTE-TIPS-1-QUOT)
:   用來開始與結束函式本體，例如：

    ```

    CREATE FUNCTION foo() RETURNS integer AS '
              ....
    ' LANGUAGE plpgsql;
    ```

    在以單引號括住的函式本體中，任何位置的引號*都必須*成對出現。
<a id="PLPGSQL-QUOTE-TIPS-2-QUOT"></a>

2 個引號 [#](#PLPGSQL-QUOTE-TIPS-2-QUOT)
:   用於函式本體內的字串常數，例如：

    ```

    a_output := ''Blah'';
    SELECT * FROM users WHERE f_name=''foobar'';
    ```

    在錢字號引用的做法中，你只要寫成：

    ```

    a_output := 'Blah';
    SELECT * FROM users WHERE f_name='foobar';
    ```

    這正是 PL/pgSQL 剖析器在兩種情況下所看到的內容。
<a id="PLPGSQL-QUOTE-TIPS-4-QUOT"></a>

4 個引號 [#](#PLPGSQL-QUOTE-TIPS-4-QUOT)
:   當你需要在函式本體內的字串常數中放入一個單引號時，例如：

    ```

    a_output := a_output || '' AND name LIKE ''''foobar'''' AND xyz''
    ```

    實際附加到 `a_output` 的值會是：
     `AND name LIKE 'foobar' AND xyz`。

    在錢字號引用的做法中，你會寫成：

    ```

    a_output := a_output || $$ AND name LIKE 'foobar' AND xyz$$
    ```

    但要注意，包住這段內容的錢字號引用分隔字串不能剛好是 `$$`。
<a id="PLPGSQL-QUOTE-TIPS-6-QUOT"></a>

6 個引號 [#](#PLPGSQL-QUOTE-TIPS-6-QUOT)
:   當函式本體內某個字串中的單引號緊接在該字串常數的結尾時，例如：

    ```

    a_output := a_output || '' AND name LIKE ''''foobar''''''
    ```

    此時附加到 `a_output` 的值會是：
     `AND name LIKE 'foobar'`。

    在錢字號引用的做法中，這會變成：

    ```

    a_output := a_output || $$ AND name LIKE 'foobar'$$
    ```
<a id="PLPGSQL-QUOTE-TIPS-10-QUOT"></a>

10 個引號 [#](#PLPGSQL-QUOTE-TIPS-10-QUOT)
:   當你想在字串常數中放入兩個單引號（這占了 8 個引號），而且它緊接在該字串常數的結尾時（再加 2 個）。你大概只有在撰寫會產生其他函式的函式時才會需要這樣做，就像[範例 41.10](plpgsql-porting.md#PLPGSQL-PORTING-EX2) 那樣。例如：

    ```

    a_output := a_output || '' if v_'' ||
        referrer_keys.kind || '' like ''''''''''
        || referrer_keys.key_string || ''''''''''
        then return ''''''  || referrer_keys.referrer_type
        || ''''''; end if;'';
    ```

    此時 `a_output` 的值會是：

    ```

    if v_... like ''...'' then return ''...''; end if;
    ```

    在錢字號引用的做法中，這會變成：

    ```

    a_output := a_output || $$ if v_$$ || referrer_keys.kind || $$ like '$$
        || referrer_keys.key_string || $$'
        then return '$$  || referrer_keys.referrer_type
        || $$'; end if;$$;
    ```

    這裡我們假設只需要把單引號放進 `a_output` 中，因為它在使用前還會再被重新加上引號。

<a id="PLPGSQL-EXTRA-CHECKS"></a>

### 41.12.2. 額外的編譯期與執行期檢查 [#](#PLPGSQL-EXTRA-CHECKS)

為了協助使用者在簡單但常見的問題造成損害之前就先找出它們，PL/pgSQL 提供了額外的檢查（*`checks`*）。啟用之後，依組態而定，它們可以在函式編譯期間發出 `WARNING` 或 `ERROR`。收到 `WARNING` 的函式仍然可以執行而不會再產生其他訊息，因此建議你在獨立的開發環境中進行測試。

在開發與／或測試環境中，建議視情況把 `plpgsql.extra_warnings` 或 `plpgsql.extra_errors` 設為 `"all"`。

這些額外檢查是透過組態變數 `plpgsql.extra_warnings`（警告）與 `plpgsql.extra_errors`（錯誤）來啟用。兩者都可以設為以逗號分隔的檢查項目清單、`"none"` 或 `"all"`。預設值是 `"none"`。目前可用的檢查項目包括：

<a id="PLPGSQL-EXTRA-CHECKS-SHADOWED-VARIABLES"></a>

`shadowed_variables` [#](#PLPGSQL-EXTRA-CHECKS-SHADOWED-VARIABLES)
:   檢查某個宣告是否遮蔽了先前已定義的變數。
<a id="PLPGSQL-EXTRA-CHECKS-STRICT-MULTI-ASSIGNMENT"></a>

`strict_multi_assignment` [#](#PLPGSQL-EXTRA-CHECKS-STRICT-MULTI-ASSIGNMENT)
:   有些 PL/pgSQL 指令允許一次指派值給多個變數，例如 `SELECT INTO`。一般來說，目標變數的數量與來源變數的數量應該要相符，不過 PL/pgSQL 會對缺少的值使用 `NULL`，並忽略多餘的變數。啟用這項檢查會使 PL/pgSQL 在目標變數數量與來源變數數量不同時拋出 `WARNING` 或 `ERROR`。
<a id="PLPGSQL-EXTRA-CHECKS-TOO-MANY-ROWS"></a>

`too_many_rows` [#](#PLPGSQL-EXTRA-CHECKS-TOO-MANY-ROWS)
:   啟用這項檢查會使 PL/pgSQL 在使用 `INTO` 子句時，檢查指定的查詢是否回傳超過一筆資料列。由於 `INTO` 陳述式永遠只會用到一筆資料列，讓查詢回傳多筆資料列通常可能效率不彰、結果不確定，或兩者兼具，因此很可能是個錯誤。

下面的例子顯示把 `plpgsql.extra_warnings` 設為 `shadowed_variables` 的效果：

```

SET plpgsql.extra_warnings TO 'shadowed_variables';

CREATE FUNCTION foo(f1 int) RETURNS int AS $$
DECLARE
f1 int;
BEGIN
RETURN f1;
END;
$$ LANGUAGE plpgsql;
WARNING:  variable "f1" shadows a previously defined variable
LINE 3: f1 int;
        ^
CREATE FUNCTION
```

下面的例子則顯示把 `plpgsql.extra_warnings` 設為 `strict_multi_assignment` 的效果：

```

SET plpgsql.extra_warnings TO 'strict_multi_assignment';

CREATE OR REPLACE FUNCTION public.foo()
 RETURNS void
 LANGUAGE plpgsql
AS $$
DECLARE
  x int;
  y int;
BEGIN
  SELECT 1 INTO x, y;
  SELECT 1, 2 INTO x, y;
  SELECT 1, 2, 3 INTO x, y;
END;
$$;

SELECT foo();
WARNING:  number of source and target fields in assignment does not match
DETAIL:  strict_multi_assignment check of extra_warnings is active.
HINT:  Make sure the query returns the exact list of columns.
WARNING:  number of source and target fields in assignment does not match
DETAIL:  strict_multi_assignment check of extra_warnings is active.
HINT:  Make sure the query returns the exact list of columns.

 foo
-----

(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-development-tips.html)（原文版本：18.6；核對日期：2026-09-13）
